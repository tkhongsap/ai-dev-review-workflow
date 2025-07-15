# GitLab Issue Review Workflow for Dev Leads

A comprehensive workflow for extracting, reviewing, and managing GitLab issues with automated branch reviews and intelligent feedback.

## Overview

This workflow enables dev leads to:
1. **Extract issues** from GitLab boards automatically
2. **Document issues** in organized markdown format
3. **Review associated branches** systematically against requirements
4. **Provide feedback** to developers through GitLab comments

## Prerequisites

### Required Tools
- **Claude Code** (claude.ai/code) or similar AI assistant
- **GitLab API access** with appropriate permissions
- **Git CLI** with repository access
- **curl** or **GitLab CLI** for API interactions

### Environment Setup

```bash
# Required GitLab configuration in .env or environment
export GITLAB_URL="https://your-gitlab-instance.com"
export GITLAB_TOKEN="your-gitlab-token"
export PROJECT_PATH="group/subgroup/project-name"
```

## Workflow Steps

### Phase 1: Issue Extraction and Documentation

#### Step 1.1: Extract Issues from GitLab Board

```bash
# Fetch all open issues
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues?state=opened" > issues.json

# Or use specific filters
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues?state=opened&labels=In%20progress,Critical" > issues.json
```

#### Step 1.2: Generate Issue Documentation

Create `gitlab-issues.md` with this structure:

```markdown
# GitLab Issues - [Project Name]

**Project**: `[project-path]`  
**Board URL**: [board-url]  
**Generated**: [date]

## 🟡 In Progress Issues

### #[number] - [title]
- **Status**: [status]
- **Labels**: [labels]
- **Assignee**: [assignee] (@username)
- **Due Date**: [due-date]
- **URL**: [issue-url]
- **Description**: [brief-description]

## 🟢 Open Issues

[similar format]

## Summary

- **Total Open Issues**: [count]
- **In Progress Issues**: [count] 
- **Critical Issues**: [count]
- **Overdue Issues**: [count]

### Priority Actions Needed:
1. **[Priority 1]** - [description]
2. **[Priority 2]** - [description]
```

### Phase 2: Branch-Issue Mapping

#### Step 2.1: List Available Branches

```bash
# List all branches
git branch -a

# Find branches matching issue patterns
git branch -a | grep -E "(issue-[0-9]+|RTRER-[0-9]+|feature/issue-[0-9]+)"
```

#### Step 2.2: Map Branches to Issues

Create mapping table:

| Branch | Issue | Developer | Status | Priority |
|--------|--------|-----------|---------|----------|
| `feature/issue-8` | #8 | @developer | In Progress | High |
| `RTRER-387-AI-issue-10` | #10 | @developer | In Progress | High |

### Phase 3: Systematic Branch Review

#### Step 3.1: Review Process Template

For each branch, follow this checklist:

```bash
# 1. Switch to branch
git checkout [branch-name]

# 2. Pull latest changes
git pull origin [branch-name]

# 3. Review against issue requirements
# Use Claude Code or AI assistant:
```

**Review Prompt Template:**
```
Review this branch implementation against Issue #[number] requirements:

Issue Requirements:
[paste issue requirements]

Branch: [branch-name]

Please check:
1. All requirements implemented
2. Code quality and best practices
3. Security considerations
4. Test coverage
5. Documentation completeness
6. Ready for merge assessment

Focus on providing specific, actionable feedback for [developer-name].
```

#### Step 3.2: Quality Assessment Criteria

**✅ Ready to Merge Criteria:**
- All issue requirements completed
- Code follows project standards
- Adequate test coverage
- No security vulnerabilities
- Proper error handling
- Documentation updated

**🚨 Critical Issues Criteria:**
- Security vulnerabilities
- Broken functionality
- Missing core requirements
- Poor error handling

**📝 Minor Improvements Criteria:**
- Code style issues
- Missing edge case handling
- Optimization opportunities
- Documentation gaps

### Phase 4: Feedback and Communication

#### Step 4.1: Comment Templates

**Ready to Merge Template:**
```markdown
## ✅ EXCELLENT WORK - READY TO MERGE!

@[developer] Your implementation of [feature-name] is **outstanding** and **exceeds all requirements**!

### 🎯 Perfect Implementation

**All requirements completed** with exceptional quality:
- ✅ [requirement 1]
- ✅ [requirement 2]
- ✅ [requirement 3]

### 🚀 Bonus Features You Added

- **[Feature 1]**: [description]
- **[Feature 2]**: [description]

### 📊 Quality Score: [X]/10

**Why this is excellent**:
- [reason 1]
- [reason 2]
- [reason 3]

## 🎉 Action: MERGE IMMEDIATELY

Your branch `[branch-name]` is **approved for production**. Great work!
```

**Critical Issues Template:**
```markdown
## 🚨 CRITICAL SECURITY ISSUE - MUST FIX IMMEDIATELY

Hi @[developer]! I reviewed your implementation and found a **critical security vulnerability** that must be fixed before merge.

### 🔥 Critical Problem

**File**: `[file-path]` line [number]

```[language]
[problematic-code]
```

**Why this is dangerous**: [explanation]

### ✅ How to Fix ([time-estimate])

**Step 1**: [specific instruction]
```[language]
[corrected-code]
```

**Step 2**: [specific instruction]

**Priority**: Fix [specific issue] TODAY - this is blocking the merge!
```

**Minor Improvements Template:**
```markdown
## ✅ GOOD WORK - READY TO MERGE WITH MINOR SUGGESTIONS

@[developer] Your [feature-name] implementation is **solid** and meets all requirements!

### 🎯 All Requirements Met

**Core implementation complete:**
- ✅ [requirement 1]
- ✅ [requirement 2]

### 🔧 Optional Enhancements (Post-merge)

1. **[Enhancement 1]**: [description]
2. **[Enhancement 2]**: [description]

## 🎉 Action: MERGE WITH CONFIDENCE

Your `[branch-name]` branch is **approved**. Consider the suggestions for future iterations.
```

#### Step 4.2: Post Comments to GitLab

```bash
# Post comment to GitLab issue
curl -X POST -H "Authorization: Bearer $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues/[issue-number]/notes" \
  -d '{"body": "[escaped-markdown-comment]"}'
```

### Phase 5: Automation Scripts

#### Script 1: Issue Extraction (`extract-issues.sh`)

```bash
#!/bin/bash
# Extract issues and generate markdown

PROJECT_ID="your-project-id"
curl -H "Authorization: Bearer $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/issues?state=opened" | \
  jq -r '.[] | "### #\(.iid) - \(.title)\n- **Status**: \(.state)\n- **Assignee**: \(.assignee.name // "Unassigned")\n- **Due Date**: \(.due_date // "Not set")\n- **URL**: \(.web_url)\n"'
```

#### Script 2: Branch Review (`review-branch.sh`)

```bash
#!/bin/bash
# Automated branch review setup

BRANCH_NAME=$1
ISSUE_NUMBER=$2

git checkout $BRANCH_NAME
git pull origin $BRANCH_NAME

echo "Branch $BRANCH_NAME checked out for Issue #$ISSUE_NUMBER"
echo "Ready for manual review..."
```

#### Script 3: Post Comment (`post-comment.sh`)

```bash
#!/bin/bash
# Post comment to GitLab issue

ISSUE_NUMBER=$1
COMMENT_FILE=$2

curl -X POST -H "Authorization: Bearer $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_PATH/issues/$ISSUE_NUMBER/notes" \
  -d "{\"body\": \"$(cat $COMMENT_FILE | sed 's/"/\\"/g' | tr '\n' ' ')\"}"
```

## Best Practices

### For Dev Leads

1. **Be Specific**: Always reference exact file paths and line numbers
2. **Be Constructive**: Focus on solutions, not just problems
3. **Be Encouraging**: Acknowledge good work and effort
4. **Be Timely**: Review within 24 hours of completion
5. **Be Educational**: Explain the "why" behind suggestions

### For Feedback Quality

- **Use Examples**: Show correct code alongside explanations
- **Provide Time Estimates**: Help developers plan their fixes
- **Prioritize Issues**: Clearly distinguish critical vs. minor issues
- **Reference Documentation**: Link to coding standards and best practices

### Comment Guidelines

- **Keep It Short**: 2-3 paragraphs maximum per issue
- **Use Emojis Strategically**: Visual cues for quick scanning
- **Action-Oriented**: Clear next steps and deadlines
- **Professional Tone**: Encouraging but direct

## Integration with Development Workflow

### Pre-Review Checklist

- [ ] All branches pulled and up-to-date
- [ ] Issue requirements clearly understood
- [ ] Review environment prepared
- [ ] Adequate time allocated for thorough review

### Post-Review Actions

- [ ] Comments posted to all reviewed issues
- [ ] Developers notified of urgent issues
- [ ] Merge-ready branches identified
- [ ] Follow-up reviews scheduled if needed

### Metrics to Track

- **Review Turnaround Time**: Target < 24 hours
- **Issue Resolution Rate**: Track fixed vs. total issues
- **Developer Satisfaction**: Regular feedback on review quality
- **Code Quality Improvement**: Measure reduction in critical issues over time

## Troubleshooting

### Common Issues

**GitLab API Rate Limits**
- Use pagination for large issue sets
- Implement retry logic with exponential backoff

**Large Diff Reviews**
- Break down into focused review sessions
- Use AI assistance for initial screening

**Complex Merge Conflicts**
- Document resolution strategy
- Provide step-by-step merge guidance

### Emergency Procedures

**Critical Security Issues**
1. Immediately notify developer and team lead
2. Create urgent GitLab issue if not exists
3. Provide fix within 2-4 hours
4. Document incident for future prevention

## Customization

### Project-Specific Adaptations

- Modify issue extraction filters for your labels
- Adapt comment templates to your team culture
- Configure branch naming patterns to match your conventions
- Add project-specific quality criteria

### Tool Integration

- **IDE Integration**: Use with VS Code GitLab extensions
- **CI/CD Integration**: Trigger reviews on merge request creation
- **Slack/Teams Integration**: Notify teams of review completions

---

**Template Version**: 1.0  
**Last Updated**: July 2025  
**Compatible With**: GitLab 15.0+, Claude Code, GitHub Codespaces

## Usage Example

```bash
# 1. Extract issues
./extract-issues.sh > current-issues.md

# 2. Review branches
./review-branch.sh feature/issue-8 8

# 3. Post feedback
./post-comment.sh 8 review-comments/ready-to-merge.md
```

This workflow has been tested successfully on the ThaiBev E-Recruitment Suite project with excellent results in developer productivity and code quality.