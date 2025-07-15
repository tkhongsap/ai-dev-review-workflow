# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a simplified GitLab issue review workflow system for development leads to systematically extract, review, and provide feedback on GitLab issues and branches. The workflow reduces review time from 4 hours to 45 minutes per feature through AI assistance and standardized templates.

## Repository Structure

**Root-level files (flat structure):**
- `README.md` - Main documentation and quick start guide
- `extract-issues-template.md` - Mustache template for GitLab issue extraction
- `branch-review-template.md` - Unified template for comprehensive branch reviews
- `CLAUDE.md` - This guidance file

## Core Workflow

1. **Issue Extraction**: Use GitLab API to fetch issues, format with `extract-issues-template.md`
2. **Branch Review**: Review branches against issue requirements using AI assistance
3. **Feedback Generation**: Select appropriate template and substitute variables
4. **Post to GitLab**: Use API to post formatted comments

## Template System

All templates use Mustache syntax:
- Variables: `{{VARIABLE_NAME}}`
- Conditional sections: `{{#SECTION}}...{{/SECTION}}`
- Lists: `{{#LIST}}{{item}}{{/LIST}}`

## GitLab Integration

### Required Environment Variables
```bash
export GITLAB_URL="https://your-gitlab-instance.com"
export GITLAB_TOKEN="your-gitlab-token" 
export PROJECT_PATH="group/subgroup/project-name"
```

### API Endpoints
- Issues: `GET /api/v4/projects/$PROJECT_PATH/issues?state=opened`
- Comments: `POST /api/v4/projects/$PROJECT_PATH/issues/$ISSUE_NUMBER/notes`

## Quality Assessment Framework

Use the unified `branch-review-template.md` for all reviews. It handles:

### ✅ Excellent Work Sections
- Highlight outstanding implementations
- Acknowledge bonus features
- Praise good practices

### 🚨 Critical Issues Sections  
- Security vulnerabilities
- Broken functionality
- Missing requirements
- Blocking issues

### 🔧 Improvement Sections
- Code quality suggestions
- Performance optimizations
- Best practice recommendations

## Branch Naming Recognition

Automatically map these patterns:
- `issue-[number]` → Issue #[number]
- `RTRER-[number]` → Issue #[number]
- `feature/issue-[number]` → Issue #[number]

## AI Review Process

When reviewing branches:
1. Extract issue requirements from GitLab
2. Analyze branch implementation
3. Apply quality assessment criteria
4. Select appropriate template
5. Substitute template variables with findings
6. Format for GitLab posting

## Best Practices for AI Assistance

- Always reference specific file paths and line numbers
- Provide time estimates for fixes
- Use encouraging but direct tone
- Focus on actionable feedback
- Maintain consistency through templates