---
name: today
description: Assemble a daily briefing across all domains and write an enriched daily note to the Obsidian vault. Designed for morning use to surface what needs attention across work and personal.
---

# Today

Gather signals from GitHub, Granola, and the Obsidian vault, then synthesize a single morning briefing. Write it to the vault and display in terminal.

## ROLE

Act as a daily briefing compiler. Be concise. Surface what needs attention, not a comprehensive dump. Prioritize actionable items over informational ones.

## CONSTANTS

```
FOCUS_REPO=FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec
TASKS_REPO=Matt-Cowsert/Matt-tasks
GITHUB_USER=Matt-Cowsert
VAULT_ROOT=/Users/matthewcowsert/Library/Mobile Documents/iCloud~md~obsidian/Documents/Matt
VA_INDEX=/Users/matthewcowsert/Library/Mobile Documents/iCloud~md~obsidian/Documents/Matt/personal/va-claim/index.md
ITF_DEADLINE=2027-04-12
```

## PROCESS

Run steps 0-5 in parallel where possible. Then synthesize in step 6.

### 0. Sweep inbox

Read `$VAULT_ROOT/inbox.md`. If there are any items below the header (lines starting with `- `):
1. Collect all items
2. Include them in the daily note under a "## Inbox" section (before Today's Actions)
3. Clear the items from `inbox.md` (keep the front matter and header, remove the items)

If inbox is empty, skip this section in the daily note.

### 1. FOCUS GitHub snapshot

Run these queries (same patterns as `/check-focus-github`):

```bash
# PRs awaiting review
gh pr list --repo $FOCUS_REPO --search "review-requested:Matt-Cowsert" --state open --json number,title,author,updatedAt

# Matt's open issues (both repos)
gh issue list --repo $FOCUS_REPO --assignee $GITHUB_USER --state open --json number,title,updatedAt --limit 20
gh issue list --repo $TASKS_REPO --assignee $GITHUB_USER --state open --json number,title,updatedAt,labels --limit 20

# New feature/feedback issues (last 24h)
gh issue list --repo $FOCUS_REPO --label "feature" --state open --json number,title,createdAt,author --limit 10
gh issue list --repo $FOCUS_REPO --label "feedback" --state open --json number,title,createdAt,author --limit 10
```

Filter new issues to those created in the last 24 hours. Deduplicate by issue number.

### 2. Granola meetings (last 24h)

Use `mcp__granola__list_meetings` with `time_range: custom`, setting `custom_start` to yesterday and `custom_end` to today.

For each meeting returned, get details via `mcp__granola__get_meetings`. List all meetings, then determine processed/unprocessed status using two signals:

**Signal 1: GitHub issue match**
```bash
gh issue list --repo $TASKS_REPO --search "<meeting title keyword>" --json number,title,createdAt
```

**Signal 2: Vault note match**
Search for a vault note referencing the meeting date and a title keyword:
```bash
grep -r "<title keyword>" "$VAULT_ROOT" --include="*.md" -l
```
Also check for date-matched files (e.g., a meeting on 2026-04-12 matches files starting with `2026-04-12-`).

**Status logic:**
- If either signal matches: mark as "processed"
- If neither matches: mark as "unprocessed"

For unprocessed meetings, suggest the appropriate skill:
- TF meeting indicators (title contains "Task Force", "FOCUS TF", "TF Meeting", or 5+ attendees): suggest `/analyze-tf-meeting`
- All others: suggest `/extract-meeting-tasks`

Display all meetings (processed and unprocessed) in the briefing, with status indicators.

### 3. Vault open tasks

Search for open task items across the vault:

```bash
grep -r "\- \[ \]" "$VAULT_ROOT" --include="*.md" -l
```

Exclude these from task counts:
- `.obsidian/` and `templates/` directories
- `work/meetings/` files (these contain verification checklists for meeting analysis, not standalone action items)
- `CLAUDE.md` files (these reference `- [ ]` in documentation, not as tasks)

Only count `- [ ]` items from files that represent action tracking (e.g., `va-claim/index.md`, daily notes, domain-specific notes).

For each file with open tasks:
- Count open (`- [ ]`) and completed (`- [x]`) items
- Map file path to domain (work, va-claim, hoa, nextvets, fitness, family, learning)
- Surface specific open items from files modified in the last 7 days

### 4. VA claim status

Read `VA_INDEX` file. Calculate days remaining until `ITF_DEADLINE`. Extract the next unchecked action item from each section:
- Pre-Filing
- Medical Evaluations Needed
- Claim Prep

### 5. Date context

Note current date and day of week. If it's Monday, flag any items from the weekend. If it's Friday, note upcoming deadlines.

### 6. Synthesize and write

Assemble all gathered data into the daily note format (see OUTPUT FORMAT). Write to `$VAULT_ROOT/daily/{YYYY-MM-DD}-daily.md`.

If a file already exists for today, append a separator (`---`) with a timestamp and add the new briefing below. Do not overwrite.

Also display the full briefing in terminal.

## OUTPUT FORMAT

```markdown
---
date: {YYYY-MM-DD}
type: daily
tags: [briefing, action]
---

# {Day of Week}, {Month DD, YYYY}

## FOCUS

### PRs Awaiting Review ({count})
- #{number} "{title}" (@{author})

### Open Issues ({N} FOCUS_Spec, {N} Matt-tasks)
{Top 5 most recently updated, one-line each}

### New Issues (last 24h)
- #{number} "{title}" (@{author}) [{labels}]
{Or: "None."}

### Recent Meetings ({count})
- [x] "{title}" ({time}) -- processed
- [ ] "{title}" ({time}) -- run /analyze-tf-meeting
- [ ] "{title}" ({time}) -- run /extract-meeting-tasks
{Or: "No meetings in last 24h."}

## Personal

### Open Tasks by Domain
| Domain | Open | Done |
|--------|------|------|
| va-claim | {n} | {n} |
| hoa | {n} | {n} |
| nextvets | {n} | {n} |
| fitness | {n} | {n} |
| family | {n} | {n} |
| learning | {n} | {n} |

### Recently Active (modified in last 7 days)
- {filename}: {count} open tasks

### VA Claim
**ITF deadline: {date} ({N} days remaining)**

Pull ALL open `- [ ]` items from `va-claim/index.md` and list them here, grouped by section (Pre-Filing, Medical Evaluations, Claim Prep). This gives a running view of the full checklist rather than just the next item per category.

## Inbox
{Items swept from inbox.md, if any. Omit section if inbox was empty.}
- {timestamp}: {captured thought}

## Today's Actions
- [ ] {Highest priority from FOCUS}
- [ ] {Highest priority from personal}
- [ ] {Any other surfaced item}
```

End with a one-line summary in terminal:

```
{N} PRs to review | {N} open issues | {N} unprocessed meetings | {N} days to ITF | {N} open vault tasks
```

## ERROR HANDLING

- `gh` unavailable: skip FOCUS section, show "GitHub unavailable"
- Granola unavailable: skip meetings section, show "Granola unavailable"
- VA claim index missing: skip VA Claim subsection
- No open tasks found: show "No open tasks" per domain
- Vault path doesn't exist: output error and exit

## VERIFICATION

After writing the file:
1. Confirm the file path was written
2. Display the one-line summary
