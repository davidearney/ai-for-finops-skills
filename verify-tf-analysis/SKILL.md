---
name: verify-tf-analysis
description: Verify FOCUS Task Force meeting analysis output for completeness and accuracy
---

# FOCUS TF Analysis Verification Skill

Run this skill after generating Task Force meeting analysis to verify output quality.

## VERIFICATION CHECKLIST

Systematically verify the following requirements and report results:

### 1. Structural Requirements
- [ ] Action Items are in the first code block
- [ ] Issue Summaries are in the second code block
- [ ] All output is wrapped in triple-backtick code fences
- [ ] Markdown syntax is valid (headers, checkboxes, links)

### 2. Action Item Completeness
For each Action Item, verify:
- [ ] Title starts with `[AI]` and uses verb-first construction
- [ ] Has `**Assignee(s):**` field with @github-handle
- [ ] Has `**Parent Issue:**` field with #FR or #PR number (or flagged as missing)
- [ ] Has `**Detailed Description**` with meeting context
- [ ] Has `**Definition of Done**` with `- [ ]` checkboxes (not bullets)
- [ ] Assignee was explicitly mentioned in the transcript
- [ ] Task represents an explicit commitment, not a "should" or "maybe"

### 3. Issue Summary Completeness
For each Issue Summary, verify:
- [ ] Uses format: `## Status Update - TF{#} – {Meeting Date}` (triggers auto-pinning by focus-automation bot)
- [ ] Contains `### Decisions Made` section (or notes "no new decisions")
- [ ] Contains `### Next Steps` section
- [ ] All AI references use `#TBD` for newly created AIs
- [ ] All AI references use actual numbers for existing AIs
- [ ] AI titles match exactly between Action Items and Issue Summaries

### 4. Cross-Reference Integrity
- [ ] Every AI has a parent FR/PR number (or is flagged for clarification)
- [ ] Every Issue Summary has a TF number
- [ ] #TBD placeholders are documented and consistent
- [ ] Existing AI/FR/PR references use correct numbers

### 5. Content Accuracy
- [ ] "Shawn" is spelled correctly throughout (not "Sean")
- [ ] No decisions from prior meetings unless explicitly re-confirmed
- [ ] Decisions are attributed to speakers when it matters
- [ ] Open questions are clearly marked as unresolved

### 6. Edge Cases
- [ ] If no AIs exist, outputs "No action items identified in this meeting."
- [ ] If FR/PR had no decisions, outputs "TF{#} - No new decisions this meeting."

## OUTPUT FORMAT

Provide verification results in this format:

```
## Verification Results

### ✅ Passed (X/Y checks)
- List all checks that passed

### ⚠️ Issues Found (X items)
1. [Issue type] Description of issue and location
2. [Issue type] Description of issue and location

### 📋 Manual Review Needed
- Items that require human judgment
- Ambiguous cases flagged for user decision

### Summary
Overall assessment: READY / NEEDS REVISION / INCOMPLETE
```

## PROCESS

1. Read the generated Action Items and Issue Summaries
2. Run through the checklist systematically
3. Document any failures with specific locations and descriptions
4. Provide actionable feedback for corrections
5. Give overall assessment

## USAGE

Invoke this skill immediately after generating TF meeting analysis:

```
/verify-tf-analysis
```

Or have Claude invoke it automatically by including in the main prompt:

```
After generating the analysis, invoke the verify-tf-analysis skill to check your work.
```
