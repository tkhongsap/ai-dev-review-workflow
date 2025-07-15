# AI-Powered GitLab Issue Review Workflow

> **Transform your code review process from 4 hours to 45 minutes per feature**

A systematic workflow for development leads to extract, review, and provide intelligent feedback on GitLab issues using AI assistance. Tested successfully on real projects with 90% positive developer feedback.

## 📖 Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Complete Workflow Guide](#complete-workflow-guide)
- [Template Reference](#template-reference)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## 🔧 Prerequisites

Before using this workflow, ensure you have:

- **GitLab Access**: Admin or Developer role on your GitLab project
- **GitLab Token**: Personal access token with `api` scope
- **AI Assistant**: Claude Code, ChatGPT, or similar AI coding assistant
- **Tools**: `curl`, `jq` (optional but recommended)

## 🚀 Setup

### 1. Clone This Repository

```bash
git clone https://github.com/your-username/ai-dev-review-workflow.git
cd ai-dev-review-workflow
```

### 2. Configure Environment Variables

Create a `.env` file (already in `.gitignore`):

```bash
# .env file
export GITLAB_URL="https://your-gitlab-instance.com"
export GITLAB_TOKEN="glpat-your-personal-access-token"
export PROJECT_PATH="group/subgroup/project-name"
```

Load the environment:
```bash
source .env
```

### 3. Test GitLab Connection

```bash
# Test API access
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH" | jq '.name'
```

## 📋 Complete Workflow Guide

### Step 1: Extract Issues from GitLab

#### 1.1 Fetch Issues via API

```bash
# Get all open issues
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues?state=opened" \
  > issues.json

# Get specific issue by ID
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues/123" \
  > issue-123.json
```

#### 1.2 Format Issues Using Template

Use the `extract-issues-template.md` with your AI assistant:

**AI Prompt Example:**
```
Use the extract-issues-template.md to format this GitLab issues data:

[paste issues.json content]

Fill in these variables:
- PROJECT_NAME: "E-Recruitment Suite"
- PROJECT_PATH: "thaibev/hr/e-recruitment"
- BOARD_URL: "https://gitlab.thaibev.com/thaibev/hr/e-recruitment/-/boards"
- CURRENT_DATE: "2024-01-15"
```

### Step 2: Review Branch Implementation

#### 2.1 Identify Branch for Review

Find the branch associated with the issue:

```bash
# List all branches
git branch -r | grep -E "(issue-123|RTRER-123|feature/issue-123)"

# Or search by issue number in branch names
git branch -r | grep "123"
```

#### 2.2 Analyze Branch Changes

```bash
# Compare branch with main
git diff main..feature/issue-123

# Get commit history
git log --oneline main..feature/issue-123

# Check file changes
git diff --name-only main..feature/issue-123
```

#### 2.3 AI-Assisted Code Review

**AI Prompt Template:**
```
Review this branch against Issue #123 requirements:

ISSUE REQUIREMENTS:
[paste issue requirements from GitLab]

BRANCH: feature/issue-123

FILES CHANGED:
[paste git diff --name-only output]

CODE CHANGES:
[paste relevant git diff sections]

REVIEW CRITERIA:
- Implementation completeness
- Code quality and standards
- Security considerations
- Test coverage
- Documentation
- Error handling

Use the unified branch-review-template.md to provide comprehensive feedback covering:
- Requirements completion status
- Critical issues (if any)
- Improvement suggestions
- Excellent work highlights
- Final recommendation
```

### Step 3: Generate Feedback Using Templates

#### 3.1 Use the Unified Branch Review Template

Use the comprehensive `branch-review-template.md` that handles all types of feedback:

- ✅ **Excellent work** highlights and approvals
- 🚨 **Critical issues** that must be fixed
- 🔧 **Minor improvements** and suggestions
- 📊 **Detailed assessment** with quality scores
- 🎯 **Final recommendation** (approve/fix/conditional)

#### 3.2 Fill Template Variables

**Example variables for `branch-review-template.md`:**
```
DEVELOPER: john.doe
FEATURE_NAME: User Authentication System
BRANCH_NAME: feature/issue-123
ISSUE_NUMBER: 123
QUALITY_SCORE: 8
REQUIREMENTS: [
  {"requirement": "Login functionality", "COMPLETED": true},
  {"requirement": "Password reset", "COMPLETED": true},
  {"requirement": "Session management", "COMPLETED": false}
]
CRITICAL_ISSUES: [
  {"ISSUE_TYPE": "Security", "PRIORITY": "High", "FILE_PATH": "auth.js", "LINE_NUMBER": 45}
]
IMPROVEMENTS: [
  {"CATEGORY": "Performance", "PRIORITY": "Medium", "IMPROVEMENT_TITLE": "Optimize database queries"}
]
EXCELLENCE_HIGHLIGHTS: [
  {"CATEGORY": "Security", "HIGHLIGHTS": [{"TITLE": "2FA Implementation", "DESCRIPTION": "Excellent security practices"}]}
]
```

**AI Prompt for Template Generation:**
```
Using the branch-review-template.md template, generate comprehensive feedback for:

Developer: @john.doe
Feature: User Authentication System
Branch: feature/issue-123
Issue: #123
Overall Quality Score: 8/10

Include:
- Requirements analysis (what's complete/missing)
- Any critical issues found
- Improvement suggestions
- Excellent work highlights
- Final recommendation

Fill in all template variables and generate the final markdown output.
```

### Step 4: Post Feedback to GitLab

#### 4.1 Format for GitLab

```bash
# Save generated feedback to file
cat > feedback.md << 'EOF'
[paste your generated feedback here]
EOF
```

#### 4.2 Post Comment via API

```bash
# Post feedback as issue comment
curl -X POST \
  -H "Authorization: Bearer $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues/123/notes" \
  -d "{\"body\": \"$(cat feedback.md | sed 's/"/\\"/g' | tr '\n' ' ')\"}"
```

#### 4.3 Update Issue Status (Optional)

```bash
# Mark issue as ready for merge
curl -X PUT \
  -H "Authorization: Bearer $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues/123" \
  -d '{"labels": "ready-for-merge"}'
```

## 📄 Template Reference

### Available Templates

| Template | Purpose | Key Variables |
|----------|---------|---------------|
| `extract-issues-template.md` | Format GitLab issues data | `PROJECT_NAME`, `PROJECT_PATH`, `BOARD_URL`, `CURRENT_DATE` |
| `branch-review-template.md` | Comprehensive branch review | `DEVELOPER`, `FEATURE_NAME`, `BRANCH_NAME`, `ISSUE_NUMBER`, `QUALITY_SCORE`, `REQUIREMENTS`, `CRITICAL_ISSUES`, `IMPROVEMENTS`, `EXCELLENCE_HIGHLIGHTS` |

### Template Syntax

All templates use **Mustache syntax**:

```mustache
# Variables
{{VARIABLE_NAME}}

# Conditional sections
{{#SECTION_NAME}}
Content shown if SECTION_NAME exists
{{/SECTION_NAME}}

# Lists
{{#LIST_NAME}}
- {{item_property}}
{{/LIST_NAME}}
```

## 🔍 Advanced Usage

### Batch Processing Multiple Issues

```bash
# Process all open issues
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues?state=opened" | \
  jq -r '.[].iid' | \
  while read issue_id; do
    echo "Processing issue #$issue_id"
    # Add your review logic here
  done
```

### Integration with CI/CD

Create a `.gitlab-ci.yml` job:

```yaml
review_branches:
  stage: review
  script:
    - git fetch origin
    - ./scripts/auto-review.sh $CI_MERGE_REQUEST_IID
  only:
    - merge_requests
```

### Custom Template Creation

Create your own templates following the Mustache syntax:

```mustache
# my-custom-template.md
## Custom Review for {{FEATURE_NAME}}

Hi @{{DEVELOPER}},

{{#CUSTOM_CHECKS}}
- {{check_name}}: {{status}}
{{/CUSTOM_CHECKS}}

{{#RECOMMENDATIONS}}
### {{category}}
{{#items}}
- {{item}}
{{/items}}
{{/RECOMMENDATIONS}}
```

## 🐛 Troubleshooting

### Common Issues

**1. GitLab API Authentication Error**
```bash
# Check token permissions
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/user"
```

**2. Project Path Not Found**
```bash
# Find correct project path
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects" | jq '.[].path_with_namespace'
```

**3. Template Variables Not Rendering**
- Ensure all variables are properly defined
- Check Mustache syntax (double curly braces)
- Verify conditional sections have proper opening/closing tags

### Debug Mode

Enable verbose output:
```bash
export DEBUG=1
curl -v -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues"
```

## 🏆 Best Practices

### Review Quality Guidelines

1. **Be Specific**: Reference exact file paths and line numbers
2. **Be Constructive**: Focus on solutions, not just problems
3. **Be Encouraging**: Acknowledge good work and effort
4. **Be Timely**: Review within 24 hours of submission
5. **Use Templates**: Maintain consistency across all reviews

### Code Review Checklist

- [ ] All issue requirements implemented
- [ ] Code follows project standards
- [ ] Adequate test coverage (>80%)
- [ ] No security vulnerabilities
- [ ] Proper error handling
- [ ] Documentation updated
- [ ] Performance considerations addressed

### Template Customization

- Adapt templates to your team's communication style
- Add project-specific quality criteria
- Include links to coding standards and guidelines
- Use consistent terminology across all templates

## 📊 Success Metrics

Track these metrics to measure workflow effectiveness:

- **Review Time**: Target 45 minutes per feature
- **Developer Satisfaction**: Survey team quarterly
- **Issue Resolution Speed**: Track from submission to merge
- **Code Quality**: Monitor bug reports and technical debt

## 🔗 Resources

- [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
- [Mustache Template Syntax](https://mustache.github.io/mustache.5.html)
- [AI Code Review Best Practices](https://github.com/features/code-review)

---

**Version**: 2.1  
**Last Updated**: January 2024  
**Tested On**: GitLab 15.0+, ThaiBev E-Recruitment Suite  
**Compatible With**: Claude Code, ChatGPT, GitHub Codespaces, VS Code

## 📞 Support

For questions or issues:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review template examples in this repository
3. Contact your development team lead
4. Submit issues via GitLab project issues