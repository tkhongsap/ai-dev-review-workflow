## 🚨 CRITICAL {{ISSUE_TYPE}} ISSUE - MUST FIX IMMEDIATELY

Hi @{{DEVELOPER}}! I reviewed your {{FEATURE_NAME}} implementation and found a **critical {{ISSUE_TYPE}} vulnerability** that must be fixed before merge.

### 🔥 Critical Problem

**File**: `{{FILE_PATH}}` line {{LINE_NUMBER}}

```{{LANGUAGE}}
{{PROBLEMATIC_CODE}}
```

**Why this is dangerous**: {{EXPLANATION}}

### ✅ How to Fix ({{TIME_ESTIMATE}})

{{#FIX_STEPS}}
**Step {{step_number}}**: {{instruction}}
{{#HAS_CODE}}
```{{language}}
{{corrected_code}}
```
{{/HAS_CODE}}

{{/FIX_STEPS}}

### 🧪 Quick Test

After fixing, test with:
```bash
{{TEST_COMMANDS}}
```

**Priority**: Fix {{SPECIFIC_ISSUE}} {{DEADLINE}} - this is blocking the merge!

{{#ADDITIONAL_RESOURCES}}
### 📚 Additional Resources
{{#RESOURCES}}
- {{resource}}
{{/RESOURCES}}
{{/ADDITIONAL_RESOURCES}}