---
name: reflect
description: Review recent session patterns and propose CLAUDE.md or MEMORY.md updates proactively. Includes a quarterly skill audit reminder. Designed for periodic use during cowork sessions or via /loop 1w.
---

# Reflect

Review recent sessions and vault activity to identify patterns worth persisting. Propose specific edits to CLAUDE.md, MEMORY.md, or vault context files for Matt's approval.

## ROLE

Act as a meta-analyst of Matt's Claude Code workflow. Look for repeated patterns, corrections, context that keeps getting re-explained, and preferences that have solidified. Be selective. Only propose changes that will save future time or improve output quality.

## CONSTANTS

```
VAULT_ROOT=/Users/matthewcowsert/Obsidian
MEMORY_DIR=/Users/matthewcowsert/.claude/projects/-Users-matthewcowsert-claude-code-config/memory
GLOBAL_CLAUDE=/Users/matthewcowsert/.claude/CLAUDE.md
```

## PROCESS

### 1. Gather signals

Read these sources to understand recent patterns:

**Recent daily notes** (last 7 days):
```bash
find $VAULT_ROOT/daily -name "*.md" -mtime -7 | sort -r
```

**Recent vault notes** (last 7 days):
```bash
find -L $VAULT_ROOT -name "*.md" -mtime -7 -not -path "*/.obsidian/*" -not -path "*/templates/*" | sort -r
```

**Current CLAUDE.md files**: Read all CLAUDE.md files in the vault and the global one.

**Current MEMORY.md**: Read `$MEMORY_DIR/MEMORY.md` and any referenced memory files.

**Session conversation history**: Review the current session for any corrections, repeated context explanations, or preference signals.

### 2. Identify patterns

Look for these categories:

**Repeated corrections**: Things Matt keeps correcting across sessions. These should become CLAUDE.md rules.

**Missing context**: Information that keeps getting re-explained or re-fetched. This should be persisted in a CLAUDE.md or vault note.

**Preference solidification**: Approaches Matt has consistently chosen that aren't yet documented. These should become memory entries or CLAUDE.md preferences.

**Stale context**: CLAUDE.md entries or memory files that reference things that have changed (completed projects, outdated deadlines, old workflows).

**Workflow friction**: Patterns where the current skill or CLAUDE.md setup causes unnecessary steps or confusion.

### 3. Quarterly skill audit check

Check the current date. If it's been 90+ days since the last skill audit (check for a `meta/skill-audit-*.md` file), flag it:

```
Quarterly skill audit due. Last audit: {date or "never"}.
Run a full audit? (Check git history, usage patterns, composition chains)
```

If not due, skip silently.

### 4. Present proposals

Show a numbered table of proposed changes:

```
Reflection findings:

| # | Type | Target | Proposal |
|---|------|--------|----------|
| 1 | Add rule | ~/.claude/CLAUDE.md | "When generating CSV examples, always include..." |
| 2 | Update | work/CLAUDE.md | Add contributor handle for new TF member |
| 3 | Remove | MEMORY.md | Stale entry about 1.3 release timeline |
| 4 | Add context | personal/hoa/CLAUDE.md | Board meeting cadence is quarterly |
| 5 | Skill audit | -- | 92 days since last audit, recommend running |

Approve all, drop some, or edit?
```

Wait for Matt's response.

### 5. Apply approved changes

For each approved item:
- **Add/update CLAUDE.md**: show the exact lines being added, with before/after context
- **Add/update MEMORY.md**: create or update memory files following the memory system conventions (front matter with name, description, type)
- **Remove stale entries**: show what's being removed and why
- **Skill audit**: run the audit (check git log for each skill, cross-references, last-modified dates) and present recommendations

### 6. Report

```
Reflection complete:

| # | Type | Applied to |
|---|------|-----------|
| 1 | Add rule | ~/.claude/CLAUDE.md (appended to Code & Technical) |
| 2 | Update | work/CLAUDE.md (added to Key References) |

{N} changes applied. Next reflection recommended: {date}.
```

## CADENCE

- Manual invocation: `/reflect` during cowork sessions
- Automated: can be used with `/loop 1w` for weekly check-ins
- Quarterly skill audit: auto-flagged when 90+ days since last audit

## ERROR HANDLING

- No daily notes found: use vault file modification dates as the signal instead
- No patterns identified: say "No changes to propose. Your context files look current." and stop.
- Conflicting signals: present both observations and let Matt decide.
