# GitLab Issues - {{PROJECT_NAME}}

**Project**: `{{PROJECT_PATH}}`  
**Board URL**: {{BOARD_URL}}  
**Generated**: {{CURRENT_DATE}}

## 🟡 In Progress Issues

{{#IN_PROGRESS_ISSUES}}
### #{{number}} - {{title}}
- **Status**: {{status}}
- **Labels**: {{labels}}
- **Assignee**: {{assignee_name}} (@{{assignee_username}})
- **Due Date**: {{due_date}}
- **URL**: {{url}}
{{#description}}
- **Description**: {{description}}
{{/description}}

{{/IN_PROGRESS_ISSUES}}

## 🟢 Open Issues

{{#OPEN_ISSUES}}
### #{{number}} - {{title}}
- **Status**: {{status}}
- **Labels**: {{labels}}
- **Assignee**: {{assignee_name}} (@{{assignee_username}})
- **Due Date**: {{due_date}}
- **URL**: {{url}}
{{#description}}
- **Description**: {{description}}
{{/description}}

{{/OPEN_ISSUES}}

## 🔴 Critical Issues

{{#CRITICAL_ISSUES}}
### #{{number}} - {{title}}
- **Status**: {{status}}
- **Labels**: {{labels}}
- **Assignee**: {{assignee_name}} (@{{assignee_username}})
- **Due Date**: {{due_date}}
- **URL**: {{url}}
- **Description**: {{description}}

{{/CRITICAL_ISSUES}}

## Summary

- **Total Open Issues**: {{TOTAL_OPEN}}
- **In Progress Issues**: {{TOTAL_IN_PROGRESS}}
- **Critical Issues**: {{TOTAL_CRITICAL}}
- **Security-related Issues**: {{TOTAL_SECURITY}}
- **Overdue Issues**: {{TOTAL_OVERDUE}}

### Priority Actions Needed:
{{#PRIORITY_ACTIONS}}
{{index}}. **{{title}}** - {{description}}
{{/PRIORITY_ACTIONS}}

### Branch Mapping

| Branch | Issue | Developer | Status | Priority |
|--------|--------|-----------|---------|----------|
{{#BRANCH_MAPPINGS}}
| `{{branch_name}}` | #{{issue_number}} | @{{developer}} | {{status}} | {{priority}} |
{{/BRANCH_MAPPINGS}}

---
*Last updated: {{TIMESTAMP}}*