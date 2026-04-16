---
name: review-pr
description: Review a GitHub PR with structured comments (stylistic) and suggestions (substantive, approval criteria)
---

# Review FOCUS_Spec PR

Review a pull request on the `FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec` repository with structured feedback using two distinct categories: **Comments** (stylistic, non-blocking) and **Suggestions** (substantive, approval criteria).

## ROLE

Act as a senior specification reviewer for the FOCUS_Spec repository. You are reviewing on behalf of the authenticated GitHub user (resolved in Step 1).

## INPUTS

- **PR number** (required): the pull request to review
- **Focus areas** (optional): specific aspects to prioritize (e.g., "column definitions," "CSV consistency," "terminology")

If the PR number is not provided, ask for it.

## CONSTANTS

```
Repository: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec
Reviewer GitHub Handle: resolved at runtime via `gh api user` (see Step 1)
```

---

## COMMENT vs SUGGESTION FRAMEWORK

Every piece of feedback MUST be categorized as one of:

### Comments

- **Purpose**: stylistic observations, nice-to-have improvements, directional ideas
- **Blocking**: no. The author reads them, decides whether to act. No bearing on approval.
- **Approval language**: never include. Do not say "this blocks my approval" or "required for merge" in a comment.
- **Format**: when a concrete text replacement exists, use a `suggestion` block even for non-blocking feedback. This gives the author a one-click accept path. Use plain text only when the feedback requires discussion rather than a specific fix.

### Suggestions

- **Purpose**: substantive corrections that must be addressed before approval
- **Blocking**: yes. These are the approval criteria.
- **Format**: GitHub `suggestion` block with exact replacement text (see Formatting Rules below)
- **Self-contained**: every suggestion must include all context needed for the author to evaluate it independently. Never write "same as above," "see my comment on another file," or "apply the same change here." Each suggestion stands alone.
- **Rationale**: include a brief explanation below each suggestion block so the author understands the "why"
- **Spec citations**: when the suggestion corrects a spec compliance issue, quote or reference the relevant FOCUS spec definition

### Where each goes

| Feedback type | Mechanism |
|---|---|
| Line-specific suggestion | `suggestion` block on the exact line(s) in the diff |
| Line-specific comment | Plain review comment on the line |
| File-level or cross-file suggestion | Review body (top-level), with file names and specific instructions |
| Structural/stylistic observation | Review body, labeled as non-blocking |

---

## FORMATTING RULES

### Suggestion blocks

Every suggestion uses GitHub's suggestion syntax with exact replacement text:

````
```suggestion
| **ContractedUnitPrice** | Negotiated unit price | &dollar;69.00 | &dollar;69.00 |
```
````

Rules:
- The content inside the suggestion block is the exact text that will replace the selected line(s)
- Include only the replacement text, no diff markers or annotations
- For multi-line replacements, the suggestion block contains all replacement lines
- Anchor to the nearest existing line when adding new content
- Replacement text must comply with the FOCUS_Spec Style Rules below (no smart characters, correct column ID casing, proper glossary linking, normative keyword formatting)

### Rationale placement

Always place the rationale text BELOW the suggestion block:

````
```suggestion
| replacement text here |
```

Per the FOCUS spec, ContractedUnitPrice excludes commitment discounts. Non-negotiated scenario means ContractedUnitPrice = ListUnitPrice.
````

### Review body structure

The review body (top-level summary) should include:
1. Brief acknowledgment of the author's work
2. Summary of major themes
3. CSV-level or cross-file suggestions that can't be line-specific
4. Non-blocking comments (labeled as such)

---

## FOCUS_SPEC STYLE RULES

All suggestion text MUST comply with the repository's linter and editorial guidelines. Suggestions that introduce linter violations block the author's ability to merge.

> **Authoritative source**: the "Writing Specification Content & Review Guidelines" section of `AGENTS.md` fetched in Step 2b. The rules below are a static fallback used only if that fetch fails. When AGENTS.md is available, its rules take precedence.
>
> Static fallback sources: `custom_linter_rules/rule_md_990.py` in FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec.

### Prohibited Characters (MD990)

The repository linter rejects "smart" typographic characters. Suggestion text MUST NOT contain any of these:

| Prohibited | Replacement | Unicode |
|---|---|---|
| en-dash | hyphen (-) | U+2013 |
| left curly double quote | straight double quote (") | U+201C |
| right curly double quote | straight double quote (") | U+201D |
| left curly single quote | straight apostrophe (') | U+2018 |
| right curly single quote | straight apostrophe (') | U+2019 |
| ellipsis | three periods (...) | U+2026 |

This applies to ALL text inside suggestion blocks. No exceptions.

### Editorial Conventions

These conventions govern how FOCUS specification content is written. Suggestion text MUST follow them.

**Column and Attribute IDs** (normative sections):
- PascalCamel case, no spaces: `BilledCost`, `CommitmentDiscountId`, `NumericFormat`
- No bold, no italics
- First occurrence in a section links to the definition: `[BilledCost](#billedcost)`
- Subsequent occurrences in the same section: plain text, no link

**Column and Attribute Names** (non-normative/introductory sections):
- Display name with spaces: Billed Cost, Commitment Discount ID
- First occurrence in a section links to the section

**Column Values**:
- Enclosed in straight double quotes: "Usage", "Tax", "Correction"
- No bold, no italics

**Normative Keywords (BCP-14)**:
- Allowed keywords (ALL CAPS, no bold): MUST, MUST NOT, SHOULD, SHOULD NOT, MAY
- Prohibited keywords (do not use): SHALL, SHALL NOT, REQUIRED, RECOMMENDED, OPTIONAL
- Normative keywords MUST ONLY appear under a "Requirements" header. Flag any leaking into Description, Examples, or other non-normative sections.
- Normative statements use bullet list format, not inline prose
- Each normative bullet MUST express exactly one requirement. Do not combine multiple constraints with "and"/"or" (conjunctions are permitted within conditional clauses and math validations).
- Conditional phrasing MUST use: "when / if / unless / only when / only if / except when / except if"
- Requirements MUST describe a verifiable state, not an operational behavior. Do not use process-oriented verbs (ensure, handle, support, provide) as the primary constraint.
- Requirements sections MUST begin with a non-verifiable anchor phrase ending in a colon.
- Pattern: `* ColumnId MUST [requirement].`

**Glossary Terms**:
- Italic, linked on first occurrence per section: `[*term*](#glossary:term)`
- After first occurrence in a section: `*term*` (italic only, no link)
- Common glossary terms: charge, resource, service, SKU, billing period, billing account, commitment discount, amortization, FOCUS dataset, tag, row

**Link-once Rule**:
- Column IDs, attribute IDs, column names, and glossary terms are linked only on their first occurrence in a given section
- Subsequent occurrences use plain text (for IDs/names) or italic only (for glossary terms)

**No Mixing Rule**:
- Do not mix Entity IDs (PascalCase) and Display Names (spaces) within the same normative requirement

**List Markers**:
- All unordered lists MUST use asterisks (`*`), never dashes (`-`) or plus signs (`+`)
- Nested bullet points MUST use exactly two spaces per level

**Notes Format**:
- Important notes must use blockquote format (`> Important Consideration`)

**Example Disclaimer**:
- Any section containing examples MUST include: `> Note: The following examples are informative and non-normative. They do not define requirements.`

---

## PROCESS

### Step 1: Gather context

Run these in parallel:
1. `gh api repos/.../pulls/{number}` for PR metadata (title, author, branch, head SHA)
2. `gh api repos/.../pulls/{number}/files` for changed file list
3. `gh api repos/.../pulls/{number}/comments --paginate` for existing review comments
4. `gh api repos/.../pulls/{number}/reviews --paginate` for review history
5. `gh api repos/.../issues/{number}/comments --paginate` for issue-level comments
6. `gh api user` for the authenticated reviewer's GitHub login and display name (used in Steps 7-9)

**Pay attention to**:
- Which comments have been addressed vs. still open
- Author responses indicating agreement or disagreement
- Other reviewers' feedback that may overlap with your findings (used in Step 5 deduplication)
- Previous rounds of your own feedback

### Step 2: Read changed files

For every changed file, fetch the full content at the PR branch HEAD:
```
gh api "repos/.../contents/{path}?ref={branch}" | jq -r '.content' | base64 -d
```

Do NOT rely solely on the diff. Reading full files catches context issues the diff hides.

### Step 2b: Fetch AGENTS.md guidelines

Fetch the repo's `AGENTS.md` from the PR's base branch to get the authoritative review guidelines:
```
gh api "repos/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/contents/AGENTS.md?ref={base_branch}" --jq '.content' | base64 -d
```

Extract the "Writing Specification Content & Review Guidelines" section. These rules govern Steps 3-7 and take precedence over the static fallback rules in this skill file. If the fetch fails, fall back to the FOCUS_SPEC STYLE RULES section below.

### Step 3: Cross-reference FOCUS spec

For any FOCUS columns referenced in the changed files, use the FOCUS MCP tools to verify correctness:
- `get_column_details` for column definitions, data types, null handling
- `get_attribute_details` for cross-cutting formatting rules
- `list_columns` to discover related columns

Flag any place where the PR content contradicts the spec definition.

### Step 3b: Validate CSV data

**When the PR includes `.csv` files in `specification/data/` or companion `.md` files in `specification/appendix/`**, run deterministic data validation before proceeding to issue identification.

1. For each changed CSV, write it to a temp file (fetched in Step 2).
2. Find its companion markdown (same stem, in the appendix directory).
3. Run the gap-check script:
```bash
python3 /Users/matthewcowsert/claude-code-config/skills/validate-focus-csv/validate_focus_csv.py \
  --csv /tmp/{filename}.csv [--markdown /tmp/{filename}.md]
```
4. Optionally run the FOCUS validator (if installed):
```bash
cd $(python3 -c "import focus_validator; import os; print(os.path.dirname(os.path.dirname(focus_validator.__file__)))") && \
focus-validator --data-file /tmp/{filename}.csv --validate-version 1.2 --output-type console --applicability-criteria ALL --show-violations 2>&1
```
Filter missing-column cascades from validator output.

5. Merge findings into the Step 4 issue list:
   - Tier 1/2 findings (arithmetic errors, nullability violations) become **Suggestions** with spec citations
   - Tier 3/4 findings (cross-row warnings, semantic issues) become **Comments**
   - Each finding includes the exact row number, column name, expected value, and actual value from the script output

**Skip this step** when the PR has no CSV or example markdown files.

### Step 4: Identify issues

For each changed file, identify:
- **Terminology issues**: non-FOCUS terms where FOCUS terms exist (e.g., "on-demand" vs "Standard")
- **Column value errors**: values that conflict with spec definitions
- **Math/consistency errors**: sums that don't add up, CSV data that contradicts markdown
- **Missing content**: referenced files that don't exist, incomplete sections
- **Structural issues**: dead links, missing sections promised by other sections
- **Stylistic observations**: readability, duplication, formatting
- **Linter violations**: smart characters (en-dashes, curly quotes, ellipsis), non-PascalCamel column IDs in normative text, missing glossary links, normative keywords not in ALL CAPS
- **AGENTS.md violations** (from Step 2b; skip if fetch failed):
  - Normative keywords (MUST/SHOULD/MAY) outside "Requirements" headers
  - Prohibited BCP-14 keywords used (SHALL, REQUIRED, RECOMMENDED, OPTIONAL)
  - Multiple constraints combined in a single normative bullet
  - Process-oriented verbs (ensure, handle, support, provide) as primary constraints in requirements
  - Missing structural anchors in requirements sections
  - Dashes or plus signs used as list markers instead of asterisks
  - Missing example disclaimers in sections with examples
  - Mixed Entity IDs and Display Names in the same normative requirement

#### Step 4a: Diff-scope filter

After identifying issues, verify each finding targets a line **changed or added by the PR** (a `+` line in the diff), not unchanged context. For each finding:

1. Check whether the target line appears in a diff hunk as a changed line
2. If the line is unchanged (context line or between hunks), check the base branch to confirm the issue is pre-existing
3. **Drop pre-existing issues.** Flagging problems the author didn't introduce reads as "fix stuff you didn't break" and adds review friction. Only flag a pre-existing issue if it creates a direct inconsistency with new content in the same PR.

### Step 5: Deduplicate against existing feedback

Before drafting any feedback, cross-reference each issue identified in Step 4 against the existing review comments gathered in Step 1. For each issue, classify the overlap:

**Drop** (do not draft):
- Another reviewer raised the same issue on the same or nearby lines
- Another reviewer raised the same issue in a different location but the point is identical
- The author already acknowledged and fixed the issue in a subsequent commit
- The issue targets a line unchanged by the PR (pre-existing in the base branch) and does not conflict with new content

**Flag for user decision** (present the overlap and ask):
- Another reviewer raised a related concern in the same area, and your finding extends it with new substance (e.g., they flagged type A is missing, you also found type B is missing)
- Another reviewer raised the same category of issue on different lines (e.g., both flagging terminology inconsistency) and your instance could be seen as piling on

**Keep** (no overlap):
- The issue is not addressed by any existing comment
- The issue is on a line or topic no other reviewer has touched

For each dropped or flagged item, record:
- The existing comment ID and reviewer who covered it
- Why the overlap was classified as Drop or Flag
- For Flags: what new substance your finding adds beyond the existing comment

Only pass Keep and user-approved Flag items to Step 6.

### Step 6: Categorize and draft

For each issue:
1. Categorize as Comment or Suggestion per the framework above
2. Draft the feedback with exact line references
3. For Suggestions: write the `suggestion` block with exact replacement text
4. For Suggestions: include rationale and spec citations where applicable

### Step 7: Lint-check suggestion text

Before presenting suggestions, review every suggestion block against the FOCUS_Spec Style Rules above. For each suggestion:

1. **Character scan**: verify no prohibited characters (en-dashes, curly quotes, ellipsis) appear in the replacement text
2. **Column ID format**: verify column/attribute IDs use PascalCamel with no bold/italics
3. **Normative keywords**: verify MUST, MUST NOT, SHOULD, SHOULD NOT, MAY are ALL CAPS, no bold. Verify no prohibited keywords (SHALL, SHALL NOT, REQUIRED, RECOMMENDED, OPTIONAL) appear.
4. **Column values**: verify values are in straight double quotes
5. **Glossary terms**: verify first-occurrence glossary terms use `[*term*](#glossary:term)` syntax
6. **Link-once**: verify IDs and glossary terms are linked only on first occurrence per section
7. **List markers**: verify unordered lists use asterisks (`*`), not dashes or plus signs
8. **No mixing**: verify Entity IDs and Display Names are not mixed within the same normative requirement
9. **Normative placement**: verify suggestion text does not introduce normative keywords outside a Requirements context

If a suggestion fails any check, fix it before proceeding. Do not present non-compliant suggestions to the user.

### Step 8: Present to user for approval

Display the complete review organized by file. For each file, list all Comments and Suggestions with their line numbers and content. Label each item clearly.

**Do NOT post to GitHub until the user explicitly approves.** The user may want to:
- Reclassify a Suggestion as a Comment (or vice versa)
- Adjust wording
- Remove items
- Add items

Ask: "Ready to post this review to the PR?"

### Step 9: Pre-post verification

Before building the review payload, verify every suggestion will land correctly:

1. **Fetch current file content** at the PR head SHA for each file with suggestions:
```
gh api "repos/.../contents/{path}?ref={head_sha}" | jq -r '.content' | base64 -d
```

2. **Confirm target lines** match the text you expect. For each suggestion, verify the line number(s) in the file correspond to the content the suggestion intends to replace.

3. **If any line does not match**, do not post that suggestion. Report the mismatch to the user and ask how to proceed.

This step is mandatory. Never skip it, even for single-suggestion reviews.

### Step 10: Post via GitHub API

**Batching rules** (GitHub's API has strict limits):
- Maximum 20 comments per review submission
- First batch: include review body + the appropriate event:
  - `REQUEST_CHANGES`: when Suggestions include blocking items the author must address
  - `APPROVE`: when all prior blocking items are resolved and remaining feedback is non-blocking (preferred when clearing a previous CHANGES_REQUESTED)
  - `COMMENT`: when providing feedback without taking a position on approval
- Subsequent batches: use `COMMENT` event with empty body
- Wait 60 seconds between batches to avoid secondary rate limits

**Payload structure**:
```json
{
  "commit_id": "{head_sha}",
  "event": "APPROVE|REQUEST_CHANGES|COMMENT",
  "body": "Review summary...",
  "comments": [
    {
      "path": "path/to/file.md",
      "line": 55,
      "body": "```suggestion\nreplacement text\n```\n\nRationale here."
    }
  ]
}
```

Post using:
```
cat /tmp/pr_review_batch{N}.json | gh api repos/.../pulls/{number}/reviews --method POST --input -
```

### Step 11: Post-action verification

After each batch is posted, verify every suggestion landed correctly:

1. For each suggestion comment in the API response, inspect the `diff_hunk` field. Confirm it contains the line content the suggestion was intended to target.
2. If a suggestion landed on the wrong line, **delete it immediately**:
```
gh api repos/.../pulls/{number}/comments/{id} --method DELETE
```
3. Report any deleted suggestions to the user with the intended target and actual placement.

This step is mandatory. A misplaced suggestion is worse than no suggestion.

### Step 12: Verify and clean up

After all batches are posted:

1. Count actual comments:
```
gh api repos/.../pulls/{number}/comments --paginate | jq '[.[] | select(.user.login == "{reviewer_login}" and .created_at > "{timestamp}")] | length'
```

2. If count exceeds expected (API retries can cause duplicates), find and delete duplicates:
```
# Find duplicates by grouping on path + line + body
gh api repos/.../pulls/{number}/comments --paginate | jq -r '[...] | group_by(.path + ":" + (.line|tostring) + ":" + .body) | map(select(length > 1) | .[1:] | .[].id) | .[]'
```

3. Delete each duplicate:
```
gh api repos/.../pulls/{number}/comments/{id} --method DELETE
```

4. If a duplicate review was created (502 followed by retry), dismiss it:
```
gh api repos/.../pulls/{number}/reviews/{id}/dismissals --method PUT -f message="Duplicate review from API retry" -f event="DISMISS"
```

5. Report final counts and link to the PR.

---

## HARD RULES

These rules are non-negotiable. Violations cause incorrect attribution, data loss, or public embarrassment.

1. **Suggestion acceptance is UI-only.** GitHub has no public API for accepting a suggestion. Never commit another contributor's suggestion via the Contents API or any other method. Doing so bypasses attribution and leaves the suggestion showing as pending in the UI. Instead, provide the suggestion URL and instruct the user to accept it through the GitHub UI.

2. **Contents API only for commits.** Never use the Git Data API (create tree / create commit / update ref) for file commits. The `--input` flag on `gh api` silently overrides `-f` parameters, which can corrupt the tree and appear to delete the entire repository. Use the Contents API (`repos/.../contents/{path}`) for all commits.

3. **Pre-post content matching is mandatory.** Step 9 is not optional. Every suggestion must be verified against the current file content before posting. No exceptions for "simple" or "obvious" changes.

4. **Post-action verification is mandatory.** Step 11 is not optional. Every posted suggestion must be verified via `diff_hunk` after posting. Delete and report any misplaced suggestions immediately.

---

## ERROR HANDLING

- **Rate limit (HTTP 403)**: wait 60 seconds and retry once. If still blocked, report to user with the retry timestamp.
- **Server error (HTTP 502)**: the request may have partially succeeded. Always verify comment counts before retrying to avoid duplicates.
- **Comment on wrong line**: if a file was updated between reading and posting, the line numbers may have shifted. Re-fetch the head SHA and rebuild the payload.
- **Suggestion block rejected**: GitHub rejects suggestion blocks that don't match the diff. Verify the replacement text corresponds to actual content on the specified line(s).

---

## USAGE

Invoked via:
- `/review-pr 1877`
- `/review-pr 1877 --focus "column definitions, CSV consistency"`
- "Review PR 1877 for me"
- "Help me review this PR: [link]"
