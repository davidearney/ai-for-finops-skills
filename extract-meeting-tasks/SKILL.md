---
name: extract-meeting-tasks
description: Extract action items from meeting transcripts (Granola or pasted notes) and create GitHub issues in Matt-Cowsert/Matt-tasks with labels, project assignment, and field values. Use this skill when the user wants to process a meeting for action items, create tasks from a meeting, or extract follow-ups from any non-FOCUS Task Force meeting. Also trigger when the user mentions Granola meetings, meeting notes, or action item extraction for personal task tracking.
---

# Extract Meeting Tasks

Extract action items from meeting transcripts and create tracked GitHub issues in `Matt-Cowsert/Matt-tasks` with proper labels, project board assignment, and field values.

This skill handles all non-FOCUS Task Force meetings. For TF meetings, use `/analyze-tf-meeting` instead.

## ROLE

Act as a meeting analyst and task manager. Read meeting transcripts or notes, identify everything that requires follow-up, and turn those into well-structured GitHub issues with full project board integration.

## INPUTS

Two input paths:

**Path A: Granola transcript**
1. Use `mcp__granola__list_meetings` to show recent meetings
2. Let the user pick one
3. Use `mcp__granola__get_meeting_transcript` to pull the transcript

**Path B: Pasted notes**
The user pastes meeting notes or a transcript directly into the conversation.

If the user says something like "extract tasks from my last meeting" without specifying, assume Granola and start with Path A.

## PARTICIPANT IDENTIFICATION

Before extracting action items, identify and confirm the people in the meeting. Speech-to-text frequently misspells names, especially non-English ones (e.g., "Arena" for Irina, "Udem" for Udam, "Wakeen" for Joaquin).

1. **Load `references/people.md`** for the known people directory and common misspellings
2. **Cross-reference the Granola participant list** (names + emails from meeting metadata) with names mentioned in the transcript
3. **Present a participant confirmation table** before extraction:

```
Participants identified in this meeting:

| Transcript Name | Matched To | Confidence | Stakeholder Field |
|---|---|---|---|
| Arena | Irena Jurica (Neos) | High (known misspelling) | -- |
| Mike | Mike Fuller (FinOps Foundation) | High (participant list match) | Mike |
| Udem | Udam Dewaraja (StitcherAI) | Medium (likely misspelling) | -- |
| Sarah | [unknown] | -- | -- |

Any corrections?
```

4. **Wait for confirmation** (or quick approval) before proceeding to extraction
5. Use corrected names throughout all issue bodies

For pasted notes (Path B), skip the Granola participant list cross-reference and rely on the known people directory plus user confirmation.

When names appear that aren't in the reference file and the user provides corrections, note them so the reference file can be updated.

## EXTRACTION LOGIC

### What to extract

Go beyond explicit action items. Look for:

- **Explicit commitments**: "I'll send that over," "I can take that on," "I'll draft something"
- **Delegated tasks**: "Can you handle X?", "Matt, would you mind...", "Let's have [person] look into..."
- **Decisions requiring follow-up**: A decision was made but someone needs to communicate it, document it, or act on it
- **Open loops**: "Let's circle back on...", "We need to figure out...", "TBD on..." -- these become tasks to prevent them from falling through
- **Scheduling commitments**: "Let's meet next week about...", "I'll set up a call with..."
- **Waiting-on items**: Someone else promised to deliver something Matt needs to track

### What NOT to extract

- General discussion points with no action owner
- Decisions that are fully resolved and require no follow-up
- Recurring standing items that already have their own tracking (unless something new came up)

### Meeting type and labels

Identify the meeting type and suggest labels from this fixed set (do not create new labels):

| Label | Use when |
|---|---|
| `spec` | FOCUS spec development, feature requests |
| `recurring` | Cyclical activity that never fully closes |
| `data-generators` | Vendor onboarding, conformance, outreach |
| `practitioners` | Practitioner adoption, training, community content |
| `f2-internal` | FinOps Foundation ops, shared services, website |
| `focus-internal` | FOCUS project ops, GitHub ops |
| `leadership` | SC, strategy, cross-cutting decisions |
| `vendors` | FinOps vendor engagement, F2 membership, partnerships |

Multiple labels are fine when an item spans categories. Default to the single most specific label when possible.

### Owner classification

Each action item has an owner:
- **Matt**: He committed to doing it, or it was assigned to him
- **Someone else**: Another person committed to it, but Matt needs to track completion

This drives the Status field (see below).

### Populating issue fields

For each action item, write:

**Title**: Short, imperative, specific. Like a commit message. Examples:
- "Send conformance timeline to AWS contact"
- "Schedule follow-up with Datadog on billing data gaps"
- "Draft practitioner FAQ on commitment discounts"

**Body** (using the repo's issue template):

```markdown
### Context
[What's the situation? Why does this matter? Include enough meeting context that the issue stands alone -- someone reading it in two weeks should understand what happened and why this task exists.]

### Next Action
[What specifically needs to happen next? Name the person responsible. If this relates to other tasks from the same meeting, add "See also: [title of related task]" here -- these will be updated with issue numbers after creation.]

### Definition of Done
[Clear exit criteria. How do you know this is complete? Prefer observable outcomes over subjective assessments.]
```

### Project field values

Determine values for these project fields:

**Status** (required):
- `Active` -- Matt owns the next action
- `Waiting` -- Someone else owns the next action; Matt is tracking
- `Scheduled` -- Has a specific future date; nothing to do until then

**Stakeholder** (optional): Set when a known person is the primary contact or owner. Match first names to this list:
Shawn, Mike, Joaquin, J.R., Kevin, Vas, Rob, Steve, Andrew, James, Joe, Suha, Natalie, Charlotte.
If the person isn't on this list, mention them by name in the issue body but skip the field.

**Inform** (optional): Set when Shawn, J.R., or Mike should have visibility on the item. Only set this when there's a real reason they'd want to know -- not as a default.

**Due date** (optional): Only set when the transcript contains a specific deadline ("by Friday," "before the March meeting," "EOD Tuesday").

**Next Touch** (optional): Set when there's a follow-up timing cue ("check in next week," "revisit after the April release," "ping them in two weeks"). Calculate the actual date.

## REVIEW STEP

This step is mandatory. Never create issues without explicit approval.

After extraction, present a numbered table:

```
| # | Title | Label(s) | Status | Stakeholder | Owner | Next Action (short) |
|---|-------|----------|--------|-------------|-------|---------------------|
| 1 | Send conformance timeline... | data-generators | Active | Kevin | Matt | Email Kevin the Q2 timeline |
| 2 | Follow up on billing data... | data-generators | Waiting | -- | Datadog team | They owe sample export by 3/21 |
```

Below the table, list any project field values that will be set (Due date, Next Touch, Inform) so they're visible before creation.

Then ask: **"Ready to create these? You can edit, remove, or add items."**

Wait for explicit approval. The user may:
- Approve as-is
- Remove items by number ("drop 3 and 5")
- Edit items ("change 2's status to Active, I'll handle it")
- Add items ("also add: follow up with Riley on the metadata deck")
- Change labels or field values

Apply all edits before proceeding to creation.

## ISSUE CREATION

### Constants

```
Repository:          Matt-Cowsert/Matt-tasks
Repository Node ID:  R_kgDOQ6itpA
Project ID:          PVT_kwHODBVHlM4BMszj

Status Field ID:     PVTSSF_lAHODBVHlM4BMszjzg76JUc
Status Option IDs:
  Inbox:      f5116cc5
  Active:     406af05e
  Waiting:    0c7f98c6
  Scheduled:  0645138d
  Done:       6ff1f3d2

Stakeholder Field ID: PVTSSF_lAHODBVHlM4BMszjzg9vCsQ
Stakeholder Option IDs:
  Shawn:     91d62124
  Mike:      09f85192
  Joaquin:   2927f5cf
  J.R.:      3711c65c
  Kevin:     9e1c9e47
  Vas:       34ee389b
  Rob:       65b9f2f1
  Steve:     abfd1057
  Andrew:    e11a5dc9
  James:     73e4e3f1
  Joe:       c84c0869
  Suha:      ddf52ab1
  Natalie:   766065a6
  Charlotte: e6291452

Inform Field ID:     PVTSSF_lAHODBVHlM4BMszjzg9vJ4c
Inform Option IDs:
  Shawn:  8cb1880a
  J.R.:   e91ffeb6
  Mike:   8fcaeda7

Due Date Field ID:   PVTF_lAHODBVHlM4BMszjzg76Jdg
Next Touch Field ID: PVTF_lAHODBVHlM4BMszjzg9vCtk
```

### Step 1: Create issues

For each approved action item, create the issue:

```bash
gh issue create --repo Matt-Cowsert/Matt-tasks \
  --title "{title}" \
  --label "{label1},{label2}" \
  --assignee Matt-Cowsert \
  --body "$(cat <<'EOF'
### Context
{context}

### Next Action
{next_action}

### Definition of Done
{definition_of_done}
EOF
)"
```

Capture the issue URL and number from the output.

### Step 2: Add to project board

For each created issue, get its node ID and add it to the project:

```graphql
mutation {
  addProjectV2ItemById(input: {
    projectId: "PVT_kwHODBVHlM4BMszj"
    contentId: "{issue_node_id}"
  }) {
    item { id }
  }
}
```

Capture the returned `item.id` for use in field updates.

### Step 3: Set project fields

For each project item, build a single batched mutation with all applicable fields. Only include fields that have values to set.

Example with all fields:

```graphql
mutation {
  setStatus: updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHODBVHlM4BMszj"
    itemId: "{item_id}"
    fieldId: "PVTSSF_lAHODBVHlM4BMszjzg76JUc"
    value: { singleSelectOptionId: "{status_option_id}" }
  }) { projectV2Item { id } }

  setStakeholder: updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHODBVHlM4BMszj"
    itemId: "{item_id}"
    fieldId: "PVTSSF_lAHODBVHlM4BMszjzg9vCsQ"
    value: { singleSelectOptionId: "{stakeholder_option_id}" }
  }) { projectV2Item { id } }

  setInform: updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHODBVHlM4BMszj"
    itemId: "{item_id}"
    fieldId: "PVTSSF_lAHODBVHlM4BMszjzg9vJ4c"
    value: { singleSelectOptionId: "{inform_option_id}" }
  }) { projectV2Item { id } }

  setDueDate: updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHODBVHlM4BMszj"
    itemId: "{item_id}"
    fieldId: "PVTF_lAHODBVHlM4BMszjzg76Jdg"
    value: { date: "{YYYY-MM-DD}" }
  }) { projectV2Item { id } }

  setNextTouch: updateProjectV2ItemFieldValue(input: {
    projectId: "PVT_kwHODBVHlM4BMszj"
    itemId: "{item_id}"
    fieldId: "PVTF_lAHODBVHlM4BMszjzg9vCtk"
    value: { date: "{YYYY-MM-DD}" }
  }) { projectV2Item { id } }
}
```

Omit any mutation alias (e.g., `setStakeholder`) if that field doesn't apply to the item.

### Step 4: Resolve cross-references

If any issues contain "See also: [title]" references to other items created in this batch:
1. Map titles to their newly created issue numbers
2. Update those issue bodies to replace "See also: [title]" with "See also: #[number]"

Use `gh issue edit` to update the body:

```bash
gh issue edit {number} --repo Matt-Cowsert/Matt-tasks --body "{updated_body}"
```

### Step 5: Report

Display a final summary:

```
## Created Tasks

| # | Title | Issue | Status | Stakeholder | Labels | Due | Next Touch |
|---|-------|-------|--------|-------------|--------|-----|------------|
| 1 | Send conformance timeline... | #12 | Active | Kevin | data-generators | 2026-03-21 | -- |
| 2 | Follow up on billing data... | #13 | Waiting | -- | data-generators | -- | 2026-03-21 |

All issues added to @Matt-Cowsert's Tasks project board.
```

## ERROR HANDLING

- **`gh` not authenticated**: Print `Run: gh auth login`
- **Missing `project` scope**: Print `Run: gh auth refresh -h github.com -s project` and skip project field steps
- **Issue creation fails**: Report the error, continue with remaining items
- **Project item add fails**: Report the error, skip field updates for that item, continue
- **Field update fails**: Report which field failed, continue with remaining fields and items
- **Stakeholder name not in list**: Use the name in the issue body, skip the Stakeholder field, note it in the report
- **Cross-reference update fails**: Report but don't fail the workflow

Never let a single failure stop the entire batch. Report all errors at the end.

## USAGE

Invoke this skill with:
- `/extract-meeting-tasks`
- "Extract tasks from my last meeting"
- "Process this meeting for action items"
- "Create tasks from these meeting notes"
- "What are my action items from this call?"
- "Pull action items from Granola"
