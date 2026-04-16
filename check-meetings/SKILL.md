---
name: check-meetings
description: Check Granola for recent meetings that haven't had action items extracted. Designed for use with /loop 1h to surface unprocessed meetings during work sessions.
---

# Check Meetings

Surface Granola meetings that happened since the last check and haven't been processed for action items yet.

## ROLE

Act as a meeting triage monitor. Quietly check for new meetings, determine which ones need action item extraction, and surface only unprocessed ones. Be silent when there's nothing to report.

## PROCESS

### 1. Determine time window

Read the timestamp from `.claude/hooks/.last-meeting-check`. If the file doesn't exist or can't be read, default to 2 hours ago.

### 2. Query Granola

Use `mcp__granola__list_meetings` with a time range covering the window from last check to now.

If no meetings are returned, write the current timestamp to `.last-meeting-check` and **output nothing**. A silent loop iteration means no new work.

### 3. Identify unprocessed meetings

For each meeting returned, check whether it's already been processed:

1. Use `mcp__granola__get_meetings` to get meeting details (title, time, duration, attendees)
2. Check `Matt-Cowsert/Matt-tasks` for issues created on the same date with a title referencing the meeting (use `gh issue list --repo Matt-Cowsert/Matt-tasks --search "<meeting title keyword>" --json number,title,createdAt`)
3. If matching issues exist, consider the meeting processed. Skip it.

If `gh` is unavailable, skip the processed-check and surface all meetings. Better to re-alert than miss one.

### 4. Classify each unprocessed meeting

Determine whether each meeting is a FOCUS Task Force meeting or a general meeting.

**TF meeting indicators** (any one is sufficient):
- Title contains: "Task Force", "FOCUS TF", "TF Meeting", "FOCUS Working", "FOCUS 1.x Scoping" (where x is any version number)
- 5+ attendees AND multiple attendees match entries in `skills/extract-meeting-tasks/references/people.md` under "FOCUS Contributors"

**General meeting**: Everything else.

### 5. Output summary

Only output if there are unprocessed meetings. Format:

```
[N] unprocessed meeting(s) since last check ([previous timestamp]):

1. "[Meeting Title]" ([time], [duration]) - [attendee count] attendees
   → Run /analyze-tf-meeting

2. "[Meeting Title]" ([time], [duration]) - [attendee count] attendees
   → Run /extract-meeting-tasks

Updated check window to [current time].
```

### 6. Update timestamp

Write the current ISO timestamp to `.claude/hooks/.last-meeting-check`.

## STATE FILE

- **Path:** `.claude/hooks/.last-meeting-check`
- **Format:** Single line, ISO 8601 timestamp (e.g., `2026-04-05T14:30:00`)
- **Lifecycle:** Created on first run, updated every run (even when no meetings found). Gitignored.

## ERROR HANDLING

- Granola MCP unavailable: output "Granola not available. Skipping meeting check." and exit.
- `gh` unavailable: skip the processed-meeting check, surface all meetings found. Note "(unverified)" next to each.
- Timestamp file unreadable: default to 2 hours ago and note the fallback.

## OUTPUT FORMAT

Terminal only. No files written (except the timestamp state file). Be concise. If nothing to report, output nothing at all.
