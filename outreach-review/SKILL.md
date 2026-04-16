---
name: outreach-review
description: Review FOCUS data generator outreach status, flag overdue contacts, and recommend next actions
---

# FOCUS Data Generator Outreach Review

Produce a prioritized briefing of which data generators need attention, who's overdue, and what to do next.

## ROLE

Act as an outreach operations assistant. Read local tracker data, apply cadence rules, and surface what needs Matt's attention right now.

## DATA SOURCES

Read all three files from the `data/outreach/` directory (relative to the project root):

1. `data/outreach/providers.json` — master provider list with status, owner, last update
2. `data/outreach/conformance.json` — conformance program engagement details
3. `data/outreach/outreach-log.jsonl` — local log of outreach actions taken

If any file is missing or empty, warn the user and work with what's available. If `providers.json` is missing, stop and tell the user to run `python3 data/outreach/import-tracker.py`.

## DETERMINING LAST CONTACT DATE

For each provider, the effective last contact date is the **most recent** of:
- `last_update` from `providers.json`
- `last_outreach_date` from `conformance.json` (if the provider appears there)
- The most recent `date` from `outreach-log.jsonl` for that provider

## CADENCE RULES

Flag a provider as overdue if days since last contact exceed:

| Lead Type | Max Days |
|-----------|----------|
| 1 - Current | 21 |
| 2 - Future | 21 |
| 3 - Hot | 14 |
| 4 - Warm | 28 |
| 5 - TBD | 42 |
| 6 - Cold | 42 |

## OUTPUT SECTIONS

Produce these sections in order. Skip any section that has zero items.

### 1. Upcoming This Week

Providers with meetings, deadlines, or next-action dates within the next 7 days. Source: `when` field, `next_date` from outreach log, or dates mentioned in `action` text.

Format:

```
| Provider | What | Date | Contact |
```

### 2. Overdue Contacts

Providers past their cadence threshold. Sort by most overdue first.

Format:

```
| Provider | Lead Type | Last Contact | Days Overdue | Owner | Recommended Action |
```

For **Recommended Action**, be specific:
- If there's a pending action in the `action` field, reference it
- If conformance outreach is "awaiting response," recommend a nudge
- If owner is Matt, phrase as "You should..." If owner is someone else, phrase as "[Owner] should..."

### 3. Conformance Awaiting Response

Providers from `conformance.json` where `status` contains "awaiting" and last outreach was >14 days ago.

Format:

```
| Provider | Contact | Last Outreach | Days Waiting | Method |
```

### 4. Needs Ownership

Providers where `owner` is "?" or `contact` is "?".

Format:

```
| Provider | Lead Type | Missing |
```

### 5. Summary Stats

One-liner counts:
- Total providers tracked
- Current / Future / Hot / Warm / TBD / Cold breakdown
- Number overdue
- Number awaiting conformance response

## EDGE CASES

- If a provider appears in the outreach log with a more recent date than `providers.json`, use the log date and note "(log)" next to the date.
- If `last_update` is null and there's no log entry, treat the provider as overdue regardless of lead type.
- Providers where owner is not "Matt" should still appear in overdue lists but the recommended action should reference the actual owner.
- Today's date is determined at runtime. Do not hardcode dates.

## OUTPUT FORMAT

Terminal only. No files written. Use markdown tables as shown above.
