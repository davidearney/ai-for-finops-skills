---
name: capture
description: End-of-session knowledge capture. Reviews the session, identifies decisions, context updates, action items, and insights, then writes them as Obsidian notes with Matt's approval.
---

# Capture

Review what happened during this Claude Code session and capture what's worth preserving in the Obsidian vault. Be selective, not exhaustive.

## ROLE

Act as a session analyst and knowledge curator. Identify what's worth preserving and where it should live. Ask Matt what to keep rather than dumping everything.

## CONSTANTS

```
VAULT_ROOT=/Users/matthewcowsert/Obsidian
```

## PROCESS

### 1. Session scan

Review the full conversation history. Categorize findings into four buckets:

**Decisions**: Points where Matt chose a direction, approved a plan, or resolved an open question. Include the rationale and what was rejected.

**Context**: Facts, relationships, or patterns worth persisting for future sessions. Things that belong in a CLAUDE.md file (about how to work) or in a vault note (about a domain).

**Action items**: Tasks identified during the session that weren't immediately completed. Things Matt said he'd do, or things flagged as next steps.

**Insights**: Analysis, framing, or reasoning Matt would want to reference later. Stress test conclusions, research findings, strategic observations.

### 2. Triage presentation

Present findings in a numbered table:

```
Session capture candidates:

| # | Type | Domain | Summary | Proposed Output |
|---|------|--------|---------|-----------------|
| 1 | Decision | work | Chose Option A for PR #1957 | decision-log in work/ |
| 2 | Context | work | TF3 operating model change | Update work/CLAUDE.md |
| 3 | Action | personal/va-claim | Schedule audiology appt | Append to va-claim/index.md |
| 4 | Insight | personal/hoa | PayHOA cost comparison | New note in hoa/ |

Keep all, drop some, or edit?
```

**Wait for Matt's response.** He may:
- Approve as-is
- Drop items by number ("drop 2 and 4")
- Edit items ("change 3 to just a reminder")
- Add items ("also capture the thing about...")
- Change the proposed output type or domain

If the session was a quick one-off with nothing substantive, say: "This session doesn't have material worth capturing." and stop.

### 3. Write approved items

For each approved item, write to the appropriate location:

**Decisions**: Write as a decision-log note.
- Path: `$VAULT_ROOT/{domain}/{YYYY-MM-DD}-{kebab-case-title}.md`
- For cross-domain or vault-level decisions, use `$VAULT_ROOT/meta/` instead
- Use the decision-log template structure (Context, Options Considered, Decision, Rationale)
- Tags: `[decision, {domain-tag}]`

**Context updates**: Append to the relevant CLAUDE.md file.
- Identify which CLAUDE.md is appropriate (root, work, personal, or domain-specific)
- Append under the most relevant existing section, or create a new section if none fits
- Keep additions concise: 1-3 lines per fact
- Show the diff of what was added

**Action items**: Append to the most relevant existing note.
- If the action relates to an existing tracking file (like `va-claim/index.md`), append there
- If no natural home exists, append to today's daily note (`$VAULT_ROOT/daily/{YYYY-MM-DD}-daily.md`)
- If no daily note exists, create one with the daily-note template structure
- Format as `- [ ] {action item}`

**Insights**: Write as a new note.
- Path: `$VAULT_ROOT/{domain}/{YYYY-MM-DD}-{kebab-case-title}.md`
- For cross-domain or vault-level insights, use `$VAULT_ROOT/meta/` instead
- Tags: `[{domain-tag}, capture]`
- Include enough context that the note stands alone in two weeks
- Simple structure: YAML front matter, a heading, the insight content

### 4. Report

After writing all items, display a summary:

```
Session capture complete:

| # | Type | Written to |
|---|------|-----------|
| 1 | Decision | work/2026-04-12-pr1957-terminology.md |
| 3 | Action | personal/va-claim/index.md (appended) |

{N} items captured. {N} CLAUDE.md files updated.
```

## TAG RULES

Apply tags from the vault's tag vocabulary (defined in `$VAULT_ROOT/CLAUDE.md`):
- Decisions: `[decision, {domain-tag}]`
- Insights: `[{domain-tag}, capture]`
- Action items: add `action` tag to the modified file if not already present
- Do not invent new tags

## ERROR HANDLING

- Session has no meaningful content: say so and stop. Don't force capture.
- Target file doesn't exist: create it with appropriate front matter and tags.
- CLAUDE.md update would duplicate existing content: skip it and note why.
- Domain is ambiguous for an item: ask Matt before writing.
- Vault path doesn't exist: output error and exit.
