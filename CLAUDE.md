# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a GitLab issue review workflow system designed for development leads to systematically extract, review, and provide feedback on GitLab issues and associated branches. The workflow reduces review time from 4 hours to 45 minutes per feature through automation and standardized templates.

## Core Workflow Architecture

The system implements a 5-phase review process:

1. **Issue Extraction**: Automated GitLab API calls to generate structured issue documentation
2. **Branch Mapping**: Link branches to issues using naming conventions (issue-N, RTRER-N, feature/issue-N)
3. **Systematic Review**: Template-driven code review against issue requirements
4. **Feedback Generation**: Mustache template system for consistent review comments
5. **Automation**: Script-based posting to GitLab issues

## Key Components

### Template System (`templates/`)
- **`issue-extraction-template.md`**: Mustache template for generating GitLab issue summaries with variable substitution
- **`review-comments/`**: Three standardized review outcomes:
  - `ready-to-merge.md`: Excellence recognition with quality scores
  - `critical-issues.md`: Security/critical issue reporting with fix instructions
  - `minor-improvements.md`: Minor suggestions with optional enhancements

### Mustache Variable Pattern
Templates use `{{VARIABLE}}` syntax for substitution and `{{#SECTION}}...{{/SECTION}}` for conditional blocks.

## GitLab Integration

### Required Environment Variables
```bash
export GITLAB_URL="https://your-gitlab-instance.com"
export GITLAB_TOKEN="your-gitlab-token" 
export PROJECT_PATH="group/subgroup/project-name"
```

### API Patterns
- Issue extraction: `GET /api/v4/projects/$PROJECT_PATH/issues?state=opened`
- Comment posting: `POST /api/v4/projects/$PROJECT_PATH/issues/$ISSUE_NUMBER/notes`

## Branch Naming Conventions

The workflow recognizes these patterns for automatic branch-to-issue mapping:
- `issue-[number]`
- `RTRER-[number]` 
- `feature/issue-[number]`

## Quality Assessment Criteria

### Ready to Merge (✅)
- All issue requirements completed
- Code follows project standards
- Adequate test coverage
- No security vulnerabilities
- Proper error handling
- Documentation updated

### Critical Issues (🚨)
- Security vulnerabilities
- Broken functionality
- Missing core requirements
- Poor error handling

### Minor Improvements (📝)
- Code style issues
- Missing edge case handling
- Optimization opportunities
- Documentation gaps

## Referenced Scripts (Not Yet Implemented)

The documentation references these automation scripts in `scripts/`:
- `extract-issues.sh <project-id>`: GitLab API issue extraction
- `review-branch.sh <branch-name> <issue-number>`: Branch checkout and review setup
- `post-comment.sh <issue-number> <template-file>`: Automated GitLab comment posting

## Review Process Template

When reviewing branches:
1. Extract issue requirements from GitLab
2. Check out target branch and pull latest
3. Review against requirements using quality criteria
4. Select appropriate template (ready-to-merge/critical-issues/minor-improvements)
5. Substitute template variables with specific findings
6. Post formatted comment to GitLab issue

## AI Assistant Integration

This workflow is optimized for AI-assisted reviews. When working with branches:
- Always reference specific file paths and line numbers
- Use the established template system for consistency
- Focus on actionable, time-estimated feedback
- Maintain encouraging but direct professional tone