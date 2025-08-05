import os
import subprocess
from openai import AzureOpenAI
import re
from pathlib import Path
from typing import List, Set, Optional
from dotenv import load_dotenv
from datetime import datetime
import sys

# Load environment variables
load_dotenv()

# Initialize Azure OpenAI client
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

if not azure_api_key:
    raise ValueError("AZURE_OPENAI_API_KEY environment variable is not set")
if not azure_endpoint:
    raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is not set")

client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=azure_endpoint,
    api_key=azure_api_key,
)

# Configuration for file filtering
CODE_EXTENSIONS: Set[str] = {
    # Web development
    '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.scss', '.sass',
    # Backend
    '.py', '.java', '.go', '.rb', '.php',
    # Systems programming
    '.c', '.cpp', '.h', '.hpp', '.rs',
    # Configuration and data
    '.json', '.yaml', '.yml', '.xml'
}

IGNORED_PATHS: Set[str] = {
    # Development artifacts
    '.git/', 'node_modules/', 'venv/', '__pycache__/',
    # Build outputs
    'dist/', 'build/', 'target/',
    # Dependencies
    'vendor/', 'packages/',
    # Test coverage reports
    'coverage/',
    # Media and binary files
    'assets/', 'images/', 'videos/',
    # Code review outputs
    'code-review-scores/'
}

def get_commit_sha() -> str:
    """
    Get the current commit SHA, first trying GitHub Actions environment variable,
    then falling back to git command.
    
    Returns:
        str: Short commit SHA (first 7 characters)
    """
    # Try GitHub Actions environment variable first
    github_sha = os.getenv("GITHUB_SHA")
    if github_sha:
        return github_sha[:7]  # Return first 7 characters
    
    try:
        # Fallback to git command
        sha = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            text=True
        ).strip()
        return sha[:7]  # Return first 7 characters
    except subprocess.CalledProcessError:
        return "unknown"

def get_pr_info() -> tuple[str, str]:
    """
    Get Pull Request number and title from GitHub environment variables.
    
    Returns:
        tuple[str, str]: PR number and PR title, or ('none', 'none') if not a PR
    """
    # Check if this is a push event (not a PR)
    event_type = os.getenv("GITHUB_EVENT_NAME", "")
    if event_type == "push":
        return "none", "none"
    
    pr_number = os.getenv("GITHUB_EVENT_NUMBER", "none")
    pr_title = os.getenv("GITHUB_EVENT_TITLE", "none")
    return pr_number, pr_title

def get_commit_info() -> tuple[str, str]:
    """
    Get commit information including SHA and message.
    
    Returns:
        tuple[str, str]: Short SHA and commit message
    """
    # Get SHA
    sha = get_commit_sha()
    
    # Get commit message
    try:
        message = subprocess.check_output(
            ["git", "log", "-1", "--pretty=%B"],
            text=True
        ).strip().split('\n')[0][:50]  # Get first line, limit to 50 chars
        # Clean the message for filename
        message = re.sub(r'[^\w\-]', '_', message)
    except subprocess.CalledProcessError:
        message = "unknown"
    
    return sha, message

def save_review_results(review_text: str, files_reviewed: List[str]) -> str:
    """
    Save the review results to a markdown file in the code-review-scores directory.
    Filename includes GitHub context and commit information.
    """
    output_dir = Path("code-review-scores")
    output_dir.mkdir(exist_ok=True)
    
    # Get all context information
    github_actor = os.getenv("GITHUB_ACTOR", "unknown")
    commit_sha, commit_msg = get_commit_info()
    pr_number, pr_title = get_pr_info()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create filename with all context
    if pr_number != "none":
        filename = f"review_PR{pr_number}_{github_actor}_{commit_sha}_{timestamp}.md"
    else:
        filename = f"review_commit_{github_actor}_{commit_sha}_{timestamp}.md"
    
    output_file = output_dir / filename
    
    # Format the content with all context information
    content = f"""# Code Review Report
Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Reviewer: {github_actor}
Commit: {commit_sha}
Commit Message: {commit_msg}
Pull Request: {f"#{pr_number}" if pr_number != "none" else "N/A"}
PR Title: {pr_title if pr_title != "none" else "N/A"}

## Files Reviewed
{chr(10).join('- ' + file for file in files_reviewed)}

## Review Details
{review_text}
"""
    
    # Write the content to the file
    output_file.write_text(content, encoding='utf-8')
    print(f"Created review file: {output_file}")  # Add debug output
    return str(output_file)

def get_changed_code_files() -> List[str]:
    """
    Retrieve a list of changed files (from HEAD~1 to HEAD),
    filtering to only include relevant code files.
    
    Returns:
        List[str]: List of file paths that have changed and match our criteria
    """
    try:
        # Get the changed files since last commit
        changed_files_output = subprocess.check_output(
            ["git", "diff", "--name-only", "HEAD~1", "HEAD"],
            stderr=subprocess.STDOUT,
            text=True  # Automatically decode output
        ).splitlines()
        
        # Filter the files based on extension and ignored paths
        code_files = [
            file_path for file_path in changed_files_output
            if (Path(file_path).suffix in CODE_EXTENSIONS and
                not any(ignored in file_path for ignored in IGNORED_PATHS))
        ]
        
        # Verify files exist and are readable
        code_files = [
            file_path for file_path in code_files
            if Path(file_path).is_file() and os.access(file_path, os.R_OK)
        ]
        
        return code_files
        
    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {e.output}")
        return []
    except Exception as e:
        print(f"Unexpected error while getting changed files: {e}")
        return []

def get_file_diff(file_path: str) -> str:
    """
    Get the diff for a specific file between HEAD~1 and HEAD.
    
    Args:
        file_path (str): Path to the file
        
    Returns:
        str: The diff content or empty string if error
    """
    try:
        diff = subprocess.check_output(
            ["git", "diff", "HEAD~1", "HEAD", "--", file_path],
            text=True
        )
        return diff
    except subprocess.CalledProcessError as e:
        print(f"Error getting diff for {file_path}: {e.output}")
        return ""

def get_file_content(file_path: str) -> str:
    """Get the complete content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return ""

def main():
    """
    Main function to run the code review process.
    """
    # Get changed files that match our criteria
    code_files = get_changed_code_files()
    if not code_files:
        print("No relevant code files found for review. Exiting.")
        return

    print(f"Found {len(code_files)} files to review:")
    for file in code_files:
        print(f"- {file}")

    # Collect complete files instead of just diffs
    combined_content = ""
    for file_path in code_files:
        content = get_file_content(file_path)
        if content:
            combined_content += f"\n=== COMPLETE FILE: {file_path} ===\n{content}"
            
            # Optionally also include the diff for focus
            diff = get_file_diff(file_path)
            if diff:
                combined_content += f"\n--- CHANGES IN {file_path} ---\n{diff}"

    if not combined_content.strip():
        print("No content found in the relevant files. Exiting review.")
        return

    prompt = f"""
You are a senior software engineer and technical lead with 15+ years of experience tasked with performing an extremely rigorous code review of CHANGES made to files. You are known for your exacting standards and will not accept mediocre code.

The following files have been changed:
{', '.join(code_files)}

Please evaluate the technical quality of the CHANGES across these dimensions (each scored 1-10). Apply STRICT professional standards - treat this as production code for a critical system:

1.	Correctness of the Changes: (Are the changes functionally sound, bug-free, and do they fully address the intended requirements? Scrutinize for edge cases, race conditions, null pointer exceptions, and any potential regressions. Any functional issue should severely impact the score.)
2.	Code Quality of Modified Sections: (Assess clarity, conciseness, maintainability, and strict adherence to established programming principles. Is the code elegant and follows SOLID principles, or is it convoluted, overly complex, or prone to errors? Poor naming, excessive complexity, or code smells should be penalized heavily.)
3.	Performance Impact of Changes: (Evaluate potential bottlenecks, inefficient algorithms, memory leaks, or excessive resource consumption. Are there more performant alternatives? Any O(n²) where O(n) is possible, or unnecessary operations should significantly reduce the score.)
4.	Security Implications of Changes: (Identify any new vulnerabilities introduced, input validation failures, or security anti-patterns. Is the code resilient against injection attacks, buffer overflows, and other common vulnerabilities? Any security concern should be treated as critical.)
5.	Consistency with Visible Code Style: (Beyond superficial formatting, does the new code integrate seamlessly with existing architectural patterns? Inconsistencies in naming conventions, design patterns, or code organization should be penalized.)
6.	Potential Impact on System Extensibility: (Do the changes facilitate future development or create technical debt? Hard-coded values, tight coupling, or lack of abstraction should significantly impact the score.)
7.	Error Handling in Changed Code: (Is error handling comprehensive, graceful, and follows best practices? Missing error handling, generic exceptions, or poor logging should be heavily penalized.)

STRICT SCORING GUIDELINES:
- 1-3: Critical issues, code is unacceptable for production (security vulnerabilities, major bugs, completely unreadable)
- 4-5: Significant issues requiring major rework (functional problems, poor design, maintainability concerns)
- 6-7: Moderate issues that need addressing (code smells, minor inefficiencies, incomplete error handling)
- 8-9: Good code with minor improvements needed (small optimizations, style consistency issues)
- 10: Exceptional code that demonstrates mastery (clean, efficient, secure, well-documented)

For each dimension, provide:
- Score: X/10
- Explanation: A brutally honest assessment highlighting every weakness found. Be specific about line numbers or code patterns when possible.
- Improvement Suggestion(s): Concrete, actionable recommendations with code examples where applicable.

Additionally, provide specific code recommendations or snippets that directly improve the identified issues.

Finally, provide an Overall Score: X.XX/10 (weighted heavily toward correctness, security, and code quality - any score above 8.0 should represent truly excellent code), and a prioritized list of MANDATORY improvements that must be addressed before this code can be considered production-ready.

Here is the combined content of the code changes to review:

====================
{combined_content}
====================
"""


    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a helpful, expert code reviewer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.25
        )

        ai_review_text = response.choices[0].message.content
        print("\n=== AI CODE REVIEW (DETAILED REPORT) ===\n")
        print(ai_review_text)

        # Save the review results
        output_file = save_review_results(ai_review_text, code_files)
        print(f"\nReview results saved to: {output_file}")

        # Extract overall score
        overall_score = None
        match = re.search(r"Overall Score:\s*([\d\.]+)/10", ai_review_text)
        if match:
            overall_score = float(match.group(1))
            print(f"\n=== FINAL OVERALL SCORE: {overall_score}/10 ===")
            
            # Exit with error if score is too low
            if overall_score < 7.0:
                print(f"\nCode review score ({overall_score}) is below minimum threshold (7.0)")
                sys.exit(1)
            print(f"\nCode review score ({overall_score}) meets quality standards")
        else:
            print("\nNo Overall Score found in the response.")
            sys.exit(1)  # Exit with error if no score found

    except Exception as e:
        print(f"Error during code review process: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()