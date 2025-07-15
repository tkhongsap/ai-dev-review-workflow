# Codebase Context Gathering

Gather comprehensive context about the current codebase and project structure to better understand the development environment and make informed decisions.

## Instructions for Claude Code

When gathering context for: `$ARGUMENTS`

1. **Project Structure Analysis**:
   - Read package.json, requirements.txt, or equivalent dependency files
   - Examine directory structure and organization
   - Identify main entry points and configuration files
   - Check for build tools, frameworks, and development setup

2. **Codebase Overview**:
   - Scan for main application files and modules
   - Identify architectural patterns and coding conventions
   - Look for existing components, services, and utilities
   - Examine test files and testing frameworks

3. **Development Environment**:
   - Check for .env files and environment configuration
   - Identify development scripts and build processes
   - Look for linting, formatting, and code quality tools
   - Examine CI/CD configurations if present

4. **Documentation and Configuration**:
   - Read README files and documentation
   - Check for API documentation or comments
   - Examine configuration files (tsconfig, eslint, etc.)
   - Look for project-specific guidelines or standards

5. **Context Gathering Strategy**:
   - Use parallel file reading for efficiency
   - Search for key patterns and file types
   - Analyze imports and dependencies
   - Map relationships between modules

6. **Key Files to Prioritize**:
   - `package.json`, `requirements.txt`, `Cargo.toml`, etc.
   - `README.md`, `CONTRIBUTING.md`
   - Main application files (`index.js`, `main.py`, `app.ts`)
   - Configuration files (`.env`, `config/`, `tsconfig.json`)
   - Test directories and files
   - Build and deployment scripts

7. **Output Format**:
   - Provide a structured summary of findings
   - Highlight important patterns and conventions
   - Identify potential areas of interest for the given task
   - Suggest next steps based on context

Execute comprehensive context gathering to provide a solid foundation for understanding the project and making informed development decisions.