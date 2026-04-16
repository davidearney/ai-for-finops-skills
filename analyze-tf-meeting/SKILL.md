---
name: analyze-tf-meeting
description: Analyze FOCUS Task Force meeting transcripts to extract action items and issue summaries with correct GitHub handles
---

# FOCUS Task Force Meeting Analysis

Analyze FOCUS Task Force meeting transcripts and chat logs to extract action items and synthesize issue summaries.

## ROLE

Act as a senior meeting analyst for FOCUS Task Force meetings. Extract action items and synthesize issue summaries from meeting transcripts and chat logs.

## INPUTS

If not provided, ask the user for:
1. Full meeting transcript (Zoom VTT) - primary source of truth
2. Zoom chat log - supplementary context and links

## OUTPUTS

**File Output**: Automatically save analysis to a file with smart naming and monthly folder structure:
- **Base Directory**: `/Users/matthewcowsert/Obsidian/work/meetings/`
- **Folder Structure**: `{YYYY}/{MM-MonthName}/`
- **Filename Format**: `{YYYY-MM-DD}-TF{#}-Analysis.md` (extract date and TF number from transcript filename)
- **Example**: `2026/02-February/2026-01-30-TF3-Analysis.md`

**Terminal Output**: Also display the analysis in terminal for immediate review.

Deliver two sections in raw markdown, wrapped in code blocks:

1. **Action Items** (first, so they can be created and numbered before updating summaries)
   - **Standalone Action Items** - work with no specific PR target. These become GitHub issues.
   - **PR Action Items** - work targeting a specific PR. These get posted as comments on the PR.
2. **Issue Summaries** (with AI placeholders for linking after creation)

**DELIVERY ORDER**: Always deliver Action Items BEFORE Issue Summaries, in two separate code blocks:
- First code block: All Action Items (both Standalone and PR Action subsections)
- Second code block: All Issue Summaries

All final deliverables must be enclosed in triple-backtick code fences so the user can inspect raw markdown syntax before copying to GitHub.

**EDGE CASES**:
- If no action items of either type exist, output: `No action items identified in this meeting.`
- If only one type exists (all standalone or all PR actions), still include both subsection headers but note "None" under the empty one
- If a referenced FR/PR had no new decisions, output: `TF{#} - No new decisions this meeting.`

---

## ACTION ITEM CATEGORIZATION

Before formatting, classify each action item into one of two categories:

- **Standalone AI**: The action does NOT target a specific PR. It produces an independent deliverable (e.g., research, new content, a new PR, a new AI). These become GitHub issues via `/create-tf-issues`.
- **PR Action**: The action explicitly targets an existing PR (e.g., "address comments on PR #1966", "add summary section to PR #1877", "update phrasing on PR #1871"). These get posted as comments on the PR via `/create-tf-issues`.

**Classification rule**: If the action's deliverable is a change *on* a specific, numbered PR, it is a PR Action. If the deliverable exists independently of any PR, it is a Standalone AI.

---

## ACTION ITEM FORMAT

Output both subsections under a single `## Action Items` header:

### Standalone Action Items

For each standalone AI, output:

```markdown
---
### [AI] {Verb-first task description}

**Assignee(s):** @{github-handle}
**Parent Issue:** #{FR or PR number}

**Detailed Description**
{Why this action is needed. Include context from the meeting discussion and any dependencies on other issues or decisions.}

**Definition of Done**
- [ ] {First completion criterion}
- [ ] {Second completion criterion}
- [ ] {Additional criteria as needed}
---
```

### PR Action Items

For each PR action, output:

```markdown
---
### [PR Action] {Verb-first task description}

**Assignee(s):** @{github-handle}
**Target PR:** #{PR number}
**Comment Type:** {review-comment | general-comment}
**File/Line Hint:** {filename and/or line context from transcript, or "N/A"}

**Description**
{What remaining work blocks this PR from progressing? Focus on concrete changes, unresolved feedback, and open questions that the assignee needs to address. Avoid process commentary or meeting dynamics.}

**Scope**
- [ ] {Specific change to make on the PR}
- [ ] {Additional items as needed}
Note: Every scope item should be a concrete action the PR author can check off (e.g., "resolve Shawn's comment on delivery handling", "remove .context file before merge"). Meta-tasks like "post a summary" or "tag reviewers" are not valid scope items.
---
```

**PR Action field guidance:**
- `**Comment Type:**` - Use `review-comment` when the action targets a specific file/line in the PR diff. Use `general-comment` for broader PR-level feedback.
- `**File/Line Hint:**` - Extract from transcript context (e.g., "billedcost.md, row 18 normative requirement", "effectivecost.md, the MUST NOT clause"). Use "N/A" if no specific location was discussed.

### AI Guidelines

- Titles must use a verb-first construction
- Standalone AI titles start with `[AI]`; PR Action titles start with `[PR Action]`
- Keep items atomic: one action, simple scope
- If a task is compound, split into multiple items
- Capture the owner based on who explicitly accepted or was assigned the task in the meeting
- Reference related FR/PR/AI numbers in the description when dependencies exist
- Keep standalone AI titles consistent between Action Items and Issue Summaries sections for easy find-and-replace when updating #TBD placeholders

**Examples of Standalone AIs (no specific PR target):**
- "Create consistency review AI for dataset instance terminology"
- "Draft new appendix section for column mapping guidance"
- "Research how other specs handle marketplace billing scenarios"

**Examples of PR Actions (target a specific PR):**
- "Address comments on PR #1871 and update phrasing"
- "Add summary section to PR #1877"
- "Clean up comments on PR #1816 for member review"
- "Split the EffectiveCost requirement on PR #1966 row 18"

**Examples of INVALID AIs (review-only, no deliverable):**
- "Review PR #1871 and provide feedback"
- "Look at the PR tonight"
- "I'll take a look and get back to you"
- "Provide comments on the approach"

**Examples of INVALID PR Action scope items (meta-tasks, not PR work):**
- "Post summary comment on PR #1800 with remaining work items" (the PR Action comment IS the summary)
- "Tag @flanakin as a relevant party" (tagging is a byproduct of the Assignee field, not a scope item)
- "Announce process shift to the team" (process commentary, not PR work)

**Commitment Pattern Examples:**
- Direct assignment: "Michael, can you clean up the PR?" followed by "Yes, I'll do that tonight"
- Volunteered: "When no one volunteered, I volunteered to create the AI and the group agreed"
- Implicit acceptance: "I'll create the consistency review AI for this"

---

## ISSUE SUMMARY FORMAT

For each FR/PR discussed, output:

**CRITICAL**: The `## Status Update` heading MUST be `##` (h2), not `###` (h3). The `publish-fr-updates` skill posts this verbatim as a GitHub comment, and the focus-automation bot only pins comments whose first line matches `## Status Update - TF{#} – {date}`. Downgrading to `###` for visual hierarchy in the analysis file will break pinning.

```markdown
## Status Update - TF{#} – {Meeting Date}

### Decisions Made
* {Decision with context. Reference speaker if attribution matters.}
* {Next decision}

### {Optional: Context Section Title - e.g., "Why These Two Options"}
{Include this section ONLY if the meeting spent significant time (3+ minutes) discussing rationale, trade-offs, or comparing approaches. Otherwise, omit this section entirely.}

### Open Questions
1. {Unresolved question surfaced during discussion}
2. {Next question}

### Next Steps
* **@{handle}**: {Task description} (`[AI] {Title} #TBD`)
* **@{handle}**: {Task description} (references existing `[AI] {Title} #{number}`)
* **@{handle}**: {Task description} -> PR #{number}
```

### Summary Guidelines

- Use `#TBD` as placeholder for standalone AIs you just extracted (to be replaced after creation by `/create-tf-issues`)
- The `/create-tf-issues` skill will replace the entire `` (`[AI] {Title} #TBD`) `` pattern (including backticks and parentheses) with just the issue number `#{number}`. GitHub auto-renders the issue title, so the redundant title text is removed once the real number exists.
- Keep standalone AI title text identical between Action Items and Issue Summaries sections -- the `/create-tf-issues` skill matches on this exact text to perform the replacement
- For PR Actions, use the `-> PR #{number}` format in Next Steps. No `#TBD` placeholder is needed since PR Actions are posted as PR comments, not created as issues.
- Reference existing AI/FR/PR numbers when continuing prior work (use just `#{number}` for previously created issues, not the backtick-wrapped pattern)
- Flex the section structure if meeting content warrants (e.g., add "Deferred Items" or "Blocked By")

---

## CRITICAL CONSTRAINTS

1. **Incremental decisions only:** Capture what was decided *in this meeting*. Do not conflate prior discussions or decisions from previous meetings with outcomes from this session. If uncertain whether something is a new decision or a restatement, flag it for clarification.

2. **Explicit commitments only - with deliverables:** An action item requires someone to have accepted or been assigned a task that produces a deliverable during the meeting. Valid commitment patterns include:
   - "Karl, can you take that?" followed by acceptance
   - "I'll create the PR for X"
   - "When no one volunteered, I volunteered to do X and the group agreed"

   **NOT valid as action items:**
   - "Review PR and provide feedback" (review-only, no deliverable)
   - "Look at the PR" (review-only)
   - "I'll take a look" (no concrete deliverable)

   **Valid as Standalone AIs:**
   - "Create consistency review AI for X" (deliverable: new AI)
   - "Draft new appendix section for Y" (deliverable: new content)

   **Valid as PR Actions:**
   - "Address comments on PR #1871 and update" (deliverable: updated PR)
   - "Clean up comments on PR #1816" (deliverable: cleaned up PR)
   - "Add summary section to PR #1877" (deliverable: new section on PR)

3. **Cross-reference everything:** Every AI and summary must include the parent FR/PR number. If a topic lacks an issue number in the transcript/chat, flag it for clarification.

4. **Raw markdown output:** All output must be copy-paste ready for GitHub. Wrap all final output in code blocks (triple backticks) so the user can review raw markdown syntax before pasting into GitHub. Use checkboxes (`- [ ]`) for Definition of Done, not bullets. Separate Action Items and Issue Summaries into distinct code blocks.

5. **Known spelling corrections:** The following names are frequently mistranscribed in Zoom VTT files. Always use the correct spelling:
   - "Shawn" (not "Sean") - FOCUS working group chair

6. **"FOCUS" capitalization:** When the transcript says "focus" referring to the FOCUS project, specification, dataset, column, or any FOCUS-defined concept, always write it as "FOCUS" (all caps) in the output. Only use lowercase "focus" when it is used as a verb (e.g., "focusing on", "let's focus on"). Examples:
   - "focus dataset" → "FOCUS dataset"
   - "focus column" → "FOCUS column"
   - "focus validator" → "FOCUS Validator"
   - "focus spec" → "FOCUS spec"
   - "let's focus on this topic" → keep lowercase (verb usage)

7. **BCP 14 / RFC 2119 keyword capitalization:** When the transcript discusses normative requirements using terms like "must", "should", "may", "must not", "should not", etc., always write these as ALL CAPS (MUST, SHOULD, MAY, MUST NOT, SHOULD NOT, etc.) in the output when they are being discussed in the context of normative requirements, specification language, or BCP 14 keywords. Keep them lowercase only when used in casual/non-normative conversation. Examples:
   - "we think it should be a must" → "the group discussed using MUST"
   - "change must to should" → "change MUST to SHOULD"
   - "add a may default line" → "add a MAY default line"
   - "we should review this PR" → keep lowercase (casual usage, not normative)

---

## PROCESS

1. **Load GitHub handle mapping** - Read the contributor mapping to ensure correct handles are used:

   | Name | GitHub Handle |
   |------|---------------|
   | Michael Flanakin (Salesforce) | @flanakin |
   | Irena Jurica (Neos) | @ijurica |
   | Karl Kraft (Walmart) | @kk09v |
   | Matt Cowsert (FinOps Foundation) | @matt-cowsert |
   | Sai Pydiganta (AWS) | @pydi-aws |
   | Andrew "Q" Quigley (Northwestern Mutual) | @qquigley |
   | Larry Advey (Twilio/CloudZero) | @ljadvey |
   | Shawn Alpay (FinOps Foundation) | @shawnalpay |
   | Joaquin Prado (FinOps Foundation) | @jpradocueva |
   | Graham Murphy (TechnologyOne) | @thecloudman |
   | David Earney (American Express) | @davidearney |
   | Riley Jenkins (Domo) | @rileyjenk |
   | Chris/Christopher Harris (Datadog) | @cnharris10 |
   | Mike Fuller (FinOps Foundation) | @mikefinopsorg |
   | Sanjna Srivatsa (Broadcom) | @SanjnaSrivatsaVMware |
   | Udam Dewaraja (StitcherAI) | @udam-stitcher |
   | Alexandra McCoy (A.M. Tech Consulting) | @TechinMama |
   | George Parker (Salesforce) | @gparker-at-sf |
   | Alfred Francis | @alfredfran91 |

2. Parse transcript for: decisions, commitments with deliverables, owner assignments, issue references, open questions
3. **Track FR/PR context throughout transcript** - note which FR/PR is being discussed in each section to correctly attribute action items
4. Cross-reference chat log for: links, issue numbers, corrections, +1 confirmations
5. **Match contributor names to GitHub handles** using the mapping (case-insensitive, account for name variations like "Chris"/"Christopher", "Q"/"Andrew")
6. Extract action items with full metadata using correct GitHub handles:
   - **Only extract actions with concrete deliverables** (not review-only tasks)
   - Look for volunteered commitments: "When no one volunteered, I volunteered to X and the group agreed"
   - Ensure FR/PR attribution matches the discussion context
   - **Categorize each item**: If the deliverable targets a specific, numbered PR, classify as PR Action. Otherwise, classify as Standalone AI.
   - For PR Actions, infer File/Line Hint from transcript context where possible
7. **Validate PR Actions against current PR state** before including them in the output:
   - For each candidate PR Action, extract the meeting date from the transcript filename.
   - Check the target PR for commits after the meeting date: `gh api "repos/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/pulls/{PR#}/commits?per_page=100" --jq '.[] | select(.commit.author.date > "{meeting_date}T00:00:00Z") | .commit.message'`
   - If commits exist after the meeting, fetch the current file content for files referenced in the scope items and check whether the described changes are already reflected in the current PR state.
   - If all scope items are already addressed: **do not include the PR Action** in the output. Note in the summary that the changes were already implemented.
   - If some scope items are addressed: include only the remaining unaddressed items in the PR Action scope.
   - If no post-meeting commits exist, or scope items are not yet addressed: include the PR Action as normal.
   - Report validation results in the verification checklist.
   - **Important**: Use `per_page=100` when fetching PR commits to avoid pagination cutting off recent activity.
8. Synthesize summaries organized by FR/PR discussed
9. **Validate Next Steps in Issue Summaries against current PR state**:
   - After drafting summaries, scan each "Next Steps" section for references to PRs (e.g., "@flanakin to update PR #1800").
   - For each referenced PR, check for commits after the meeting date (same method as step 7, with `per_page=100`).
   - If the author has already pushed changes addressing the next step, update the wording to reflect completion (e.g., "PR #1800 updated post-meeting" or past tense) rather than framing it as outstanding work.
   - This prevents summaries from reading as stale when PR authors move fast after the meeting.
10. Flag any discrepancies, unclear ownership, or missing issue references
11. **Flag any contributors not found in the mapping** for manual review
12. Wrap all final deliverables in code blocks for user review
13. If no action items exist, output: "No action items identified in this meeting."
14. If a referenced FR/PR had no new decisions, output: "TF{#} - No new decisions this meeting."

---

## VERIFICATION

After generating output, verify the following and present a verification checklist:

**Pre-Delivery Checklist:**
- [ ] GitHub handle mapping was loaded and applied
- [ ] Every action item has an assignee explicitly mentioned in the transcript
- [ ] All assignee GitHub handles match the mapping exactly
- [ ] Any unmapped contributors are flagged for manual review
- [ ] Every action item has a concrete deliverable (not just "review" or "provide feedback")
- [ ] Every action item's FR/PR attribution matches the discussion context (not misattributed)
- [ ] Every action item and summary references a parent FR/PR number (or is flagged as missing)
- [ ] All markdown syntax is properly formatted (triple backticks, checkboxes, headers)
- [ ] "Shawn" spelling is corrected throughout (not "Sean")
- [ ] "FOCUS" is capitalized when referring to the project/spec/datasets/columns (not lowercase "focus")
- [ ] BCP 14 keywords (MUST, SHOULD, MAY, etc.) are ALL CAPS when discussed in normative requirement context
- [ ] No decisions from prior meetings are included unless explicitly re-confirmed in this meeting
- [ ] Action Items are in the first code block, Issue Summaries in the second
- [ ] Standalone AI titles are identical in both sections for easy #TBD replacement
- [ ] All #TBD placeholders are clearly marked and documented
- [ ] Volunteered commitments were captured (e.g., "when no one volunteered, I volunteered...")
- [ ] PR Actions are correctly categorized (all reference a specific PR number)
- [ ] Standalone AIs do not include PR-specific work that should be a PR Action
- [ ] Comment Type is set for each PR Action (review-comment or general-comment)
- [ ] File/Line Hint is populated for PR Actions where transcript provides location context
- [ ] PR Actions validated against current PR state (post-meeting commits checked; already-implemented items excluded)
- [ ] Issue Summary next steps validated against current PR state (completed work reflected in past tense, not framed as outstanding)

**Present this checklist** before delivering final output, noting any items that failed verification.

---

## IF INFORMATION IS INCOMPLETE

Before generating output, ask clarifying questions if:
- Owner of a task is ambiguous
- Issue number is referenced but not stated
- A decision's scope is unclear (this meeting vs. prior)

**Ask all clarifying questions in a single batch**, not iteratively, to minimize back-and-forth.

---

## EFFICIENCY GUIDELINES

- If transcript file is >500 lines, use subagents to parse and extract initial data
- Process chat log in parallel with transcript analysis where possible
- If >10 AIs are identified, confirm the list summary before generating full descriptions
- Use find/search commands to quickly locate issue numbers, names, and decisions

---

## FILE SAVING WORKFLOW

After generating analysis output:

1. **Extract meeting metadata** from transcript filename:
   - Meeting date (format: YYYYMMDD from filename like `GMT20260130-155818_Recording.transcript.vtt`)
   - Task Force number (default to TF-3 if not detectable)

2. **Determine save location**:
   - Base: `/Users/matthewcowsert/Obsidian/work/meetings/`
   - Year folder: `{YYYY}/`
   - Month folder: `{MM-MonthName}/` (e.g., `01-January`, `02-February`)
   - Filename: `{YYYY-MM-DD}-TF{#}-Analysis.md`

3. **Create directories if needed**:
   ```bash
   mkdir -p "{base}/{year}/{month}"
   ```

4. **Write file** with complete analysis including:
   - Meeting date and metadata header
   - Action Items section (in code block)
   - Issue Summaries section (in code block)
   - Verification checklist results

5. **Confirm to user**:
   - Display saved file path
   - Show file size
   - Remind user about #TBD replacement workflow

**Example output path**:
```
/Users/matthewcowsert/Obsidian/work/meetings/2026/01-January/2026-01-30-TF3-Analysis.md
```

---

## USAGE

User can invoke this skill by:
- `/analyze-tf-meeting`
- "Analyze this TF meeting" with attached files
- "Process this Task Force transcript"

You will automatically recognize TF meeting analysis requests and apply this skill.

The skill will automatically save output to the Meeting Analysis directory with smart naming based on the transcript filename.
