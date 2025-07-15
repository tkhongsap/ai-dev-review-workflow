# Branch Review: {{FEATURE_NAME}}

**Developer**: @{{DEVELOPER}}  
**Branch**: `{{BRANCH_NAME}}`  
**Issue**: #{{ISSUE_NUMBER}}  
**Review Date**: {{REVIEW_DATE}}  
**Overall Quality Score**: {{QUALITY_SCORE}}/10

---

## 📋 Requirements Analysis

{{#REQUIREMENTS}}
- {{#COMPLETED}}✅{{/COMPLETED}}{{#NOT_COMPLETED}}❌{{/NOT_COMPLETED}} {{requirement}}
{{/REQUIREMENTS}}

{{#MISSING_REQUIREMENTS}}
### ⚠️ Missing Requirements
{{#MISSING_ITEMS}}
- **{{requirement}}**: {{explanation}}
{{/MISSING_ITEMS}}
{{/MISSING_REQUIREMENTS}}

---

## 🚨 Critical Issues (Must Fix Before Merge)

{{#CRITICAL_ISSUES}}
### {{ISSUE_TYPE}} - Priority: {{PRIORITY}}

**File**: `{{FILE_PATH}}`{{#LINE_NUMBER}} (Line {{LINE_NUMBER}}){{/LINE_NUMBER}}

**Problem**: {{DESCRIPTION}}

{{#PROBLEMATIC_CODE}}
```{{LANGUAGE}}
{{PROBLEMATIC_CODE}}
```
{{/PROBLEMATIC_CODE}}

**Why this is critical**: {{EXPLANATION}}

**Fix Required** ({{TIME_ESTIMATE}}):
{{#FIX_STEPS}}
{{step_number}}. {{instruction}}
{{#HAS_CODE}}
```{{language}}
{{corrected_code}}
```
{{/HAS_CODE}}
{{/FIX_STEPS}}

{{#TEST_COMMANDS}}
**Test after fix**:
```bash
{{TEST_COMMANDS}}
```
{{/TEST_COMMANDS}}

---
{{/CRITICAL_ISSUES}}

{{#NO_CRITICAL_ISSUES}}
✅ **No critical issues found** - code is secure and functional!
{{/NO_CRITICAL_ISSUES}}

---

## 🔧 Improvements & Suggestions

{{#IMPROVEMENTS}}
### {{CATEGORY}} - {{PRIORITY}}

**{{IMPROVEMENT_TITLE}}**

{{DESCRIPTION}}

{{#HAS_CODE_EXAMPLE}}
**Current approach**:
```{{language}}
{{current_code}}
```

**Suggested improvement**:
```{{language}}
{{suggested_code}}
```
{{/HAS_CODE_EXAMPLE}}

**Benefits**: {{BENEFITS}}  
**Effort**: {{EFFORT_ESTIMATE}}

---
{{/IMPROVEMENTS}}

{{#NO_IMPROVEMENTS}}
✅ **Code quality is excellent** - no improvements needed!
{{/NO_IMPROVEMENTS}}

---

## 🚀 Excellent Work Highlights

{{#EXCELLENCE_HIGHLIGHTS}}
### {{CATEGORY}}

{{#HIGHLIGHTS}}
- **{{TITLE}}**: {{DESCRIPTION}}
{{/HIGHLIGHTS}}

{{/EXCELLENCE_HIGHLIGHTS}}

{{#BONUS_FEATURES}}
### 🎁 Bonus Features Implemented

{{#FEATURES}}
- **{{feature_name}}**: {{description}}
{{/FEATURES}}
{{/BONUS_FEATURES}}

---

## 📊 Detailed Assessment

### ✅ Strengths
{{#STRENGTHS}}
- {{strength}}
{{/STRENGTHS}}

### 🔍 Code Quality Areas
{{#QUALITY_AREAS}}
- **{{area}}**: {{score}}/10 - {{comment}}
{{/QUALITY_AREAS}}

### 🧪 Testing & Coverage
{{#TESTING}}
- **Test Coverage**: {{coverage}}%
- **Test Quality**: {{quality}}/10
{{#TEST_COMMENTS}}
- {{comment}}
{{/TEST_COMMENTS}}
{{/TESTING}}

### 🔒 Security Assessment
{{#SECURITY}}
- **Security Score**: {{score}}/10
{{#SECURITY_NOTES}}
- {{note}}
{{/SECURITY_NOTES}}
{{/SECURITY}}

---

## 🎯 Final Recommendation

{{#READY_TO_MERGE}}
## ✅ APPROVED FOR MERGE

Your implementation is **{{APPROVAL_LEVEL}}** and ready for production!

**Why this is approved**:
{{#APPROVAL_REASONS}}
- {{reason}}
{{/APPROVAL_REASONS}}

{{SPECIFIC_PRAISE}}
{{/READY_TO_MERGE}}

{{#NEEDS_FIXES}}
## ⏳ NEEDS FIXES BEFORE MERGE

Please address the critical issues above before merging.

**Estimated fix time**: {{TOTAL_FIX_TIME}}

{{#BLOCKING_ISSUES}}
**Blocking issues**:
{{#ISSUES}}
- {{issue}}
{{/ISSUES}}
{{/BLOCKING_ISSUES}}
{{/NEEDS_FIXES}}

{{#CONDITIONAL_APPROVAL}}
## 🔄 CONDITIONAL APPROVAL

This can be merged after addressing:
{{#CONDITIONS}}
- {{condition}}
{{/CONDITIONS}}

**Estimated time**: {{CONDITION_FIX_TIME}}
{{/CONDITIONAL_APPROVAL}}

---

## 📚 Learning & Next Steps

{{#LEARNING_NOTES}}
### 💡 Learning Opportunities
{{#NOTES}}
- {{note}}
{{/NOTES}}
{{/LEARNING_NOTES}}

{{#FUTURE_ENHANCEMENTS}}
### 🔮 Future Enhancements (Post-merge)
{{#ENHANCEMENTS}}
- {{enhancement}}
{{/ENHANCEMENTS}}
{{/FUTURE_ENHANCEMENTS}}

{{#RESOURCES}}
### 📖 Helpful Resources
{{#RESOURCE_LINKS}}
- [{{title}}]({{url}})
{{/RESOURCE_LINKS}}
{{/RESOURCES}}

---

**Review completed by**: {{REVIEWER}}  
**Next review**: {{#NEEDS_RECHECK}}After fixes are applied{{/NEEDS_RECHECK}}{{#NO_RECHECK}}Not needed{{/NO_RECHECK}} 