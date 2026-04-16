---
name: check-focus-github
description: Monitor FOCUS_Spec GitHub repo for PRs awaiting review, new feature/feedback issues, and action items assigned to Matt. Designed for use with /loop 1h to surface new work during sessions.
---

# Check FOCUS GitHub

Surface new PRs needing review, recently created feature/feedback issues, and Matt's open action items across FOCUS_Spec and Matt-tasks repos. One consolidated briefing per check.

## ROLE

Act as a GitHub triage monitor for FOCUS spec work. Check multiple signals, filter to what's new or actionable, and present a single concise briefing. Be silent when nothing has changed.

## PREREQUISITES

This skill requires the `gh` CLI authenticated with access to:
- `FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec`
- `Matt-Cowsert/Matt-tasks`

If `gh` is unavailable, output "gh CLI not available. Skipping GitHub check." and exit.

## CONSTANTS

```
FOCUS_REPO=FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec
TASKS_REPO=Matt-Cowsert/Matt-tasks
GITHUB_USER=Matt-Cowsert
STATE_FILE=.claude/hooks/.last-github-check
```

## PROCESS

### 1. Read last-check timestamp

Read ISO timestamp from `STATE_FILE`. If missing, default to 4 hours ago.

### 2. Check PRs awaiting review

```bash
gh pr list --repo $FOCUS_REPO --search "review-requested:Matt-Cowsert" --state open --json number,title,author,updatedAt
```

Include all open PRs where Matt's review is requested (not filtered by time, since outstanding reviews are always relevant).

### 3. Check new feature/feedback/triage issues

For each label (`feature`, `feedback`, `needs triage`), fetch open issues:

```bash
gh issue list --repo $FOCUS_REPO --label "<label>" --state open --json number,title,createdAt,author,labels --limit 10
```

Filter to issues created **after** the last-check timestamp. If an issue has multiple tracked labels, show it once (deduplicate by issue number).

### 4. Check Matt's open action items

Fetch from both repos:

```bash
gh issue list --repo $FOCUS_REPO --assignee $GITHUB_USER --state open --json number,title,updatedAt --limit 50
gh issue list --repo $TASKS_REPO --assignee $GITHUB_USER --state open --json number,title,updatedAt,labels --limit 50
```

Report total counts for each repo. Show the 5 most recently updated items across both repos.

### 5. Determine whether to output

Build the briefing from sections 2-4. If ALL of the following are true, output nothing (silent iteration):
- No PRs awaiting review
- No new issues since last check
- Action item counts haven't changed since last report

Otherwise, output the briefing.

### 6. Output briefing

Format:

```
FOCUS GitHub Update (since [last check time]):

PRs awaiting your review ([count]):
- #[number] "[title]" (@[author])
- ...

New issues since last check ([count]):
- #[number] "[title]" (@[author]) [labels]
- ...

Open action items: [N] in FOCUS_Spec, [N] in Matt-tasks
Recently updated:
- [repo]#[number]: [title]
- ...

Suggested actions:
- Run /review-pr [number] to review [PR title]
- Triage #[number] — new feature request
```

### 7. Update timestamp

Write current ISO timestamp to `STATE_FILE`.

## SUGGESTED ACTIONS

At the end of each briefing, suggest concrete next steps:

- For PRs awaiting review: "Run `/review-pr [number]`"
- For issues labeled `needs triage`: "Triage #[number] — [brief reason]"
- For feature issues: "Run `/classify-fr [number]` to classify" (only if unclassified)
- For overdue action items (>7 days without update): flag them

## ERROR HANDLING

- `gh` not installed or not authenticated: output one-line warning and exit
- API rate limit: output "GitHub API rate limited. Will retry next cycle." and exit without updating timestamp
- One section fails but others succeed: output what worked, note the failure

## OUTPUT FORMAT

Terminal only. No files written (except the timestamp state file). Concise. If nothing to report, output nothing at all.
