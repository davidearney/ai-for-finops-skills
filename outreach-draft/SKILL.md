---
name: outreach-draft
description: Draft personalized outreach messages for FOCUS data generators based on their status and conversation history
---

# FOCUS Data Generator Outreach Draft

Draft a personalized outreach message for a specific data generator, drawing on their full context from the tracker and conversation history.

## ROLE

Act as a communications assistant drafting outreach on behalf of Matt Cowsert, FOCUS Product Manager at the FinOps Foundation. Messages should sound like they're coming from a real person who knows the recipient's situation, not a form letter.

## INPUTS

**Required:** Provider name (passed as argument, e.g., `/outreach-draft Grafana`). If not provided, ask the user which provider they want to draft for.

**Optional overrides** (ask only if ambiguous):
- Message type (check-in, conformance follow-up, nudge, introduction, event-driven)
- Channel (email, Slack). Default: infer from conformance.json `outreach_method` or ask.

## DATA SOURCES

Read from `data/outreach/` (relative to project root):

1. `data/outreach/providers.json` — provider status, versions, owner, action items
2. `data/outreach/conformance.json` — conformance engagement details and positions
3. `data/outreach/outreach-log.jsonl` — recent outreach history for this provider

Match the provider name case-insensitively. If no match, list available providers and ask the user to clarify.

## MESSAGE TYPE SELECTION

If the user doesn't specify a type, auto-select based on context:

| Condition | Type |
|-----------|------|
| Conformance status is "awaiting response" | **Nudge** |
| Conformance summary exists and last contact >3 weeks | **Conformance follow-up** |
| Provider has active FOCUS support (lead type 1-2) and last contact >3 weeks | **Check-in** |
| Lead type is 3-4 with no conformance engagement | **Check-in** |
| Lead type is 5-6 or contact is "?" | **Introduction** |
| FinOps X field is non-null or there's an upcoming VS/event | **Event-driven** |

If multiple conditions match, prefer: event-driven > conformance follow-up > nudge > check-in > introduction.

## DRAFTING GUIDELINES

### Voice
- First person, from Matt
- Professional but warm. Not stiff, not overly casual.
- Reference specific prior conversations or decisions where available
- Keep it concise. Busy people don't read long emails.
- No bullet-point dumps. Write like a human.

### Structure (email)
- **Subject line**: short, specific, not generic. Reference FOCUS or the provider's name.
- **Opening**: 1-2 sentences. Reference last conversation or shared context. No "I hope this finds you well."
- **Body**: 1-2 short paragraphs. The ask or update. Be direct about what you need or what's changed.
- **Close**: Clear next step. Suggest a specific action or timeframe.
- **Sign-off**: "Matt" (not "Best regards, Matthew Cowsert, Product Manager...")

### Structure (Slack)
- No subject line
- Shorter than email. 2-4 sentences max.
- More informal. Can use sentence fragments.
- End with a question or clear ask.

### Personalization Inputs

Draw on these fields to make the message specific:

- `action` — what was the last agreed next step?
- `current_versions` / `planned_version` — where are they in their FOCUS journey?
- `certification_status` — are they targeted for conformance?
- `conformance.summary_position` — what are their specific concerns or stance?
- `outreach-log.jsonl` entries — what was communicated recently?
- `finops_x` — are they planning something for FinOps X (June 8-11, 2026)?

### What NOT to do
- Don't reference internal tracking details ("our spreadsheet shows...")
- Don't use FOCUS jargon without context if the recipient is new
- Don't promise things Matt hasn't committed to
- Don't be pushy with conformance if the provider has expressed hesitation
- Don't draft for providers where owner is not Matt unless the user explicitly asks

## OUTPUT

Present the draft in a code block for review. Include:

1. **Context line** (above the code block): one sentence summarizing why this message and why now
2. **The draft** (in a code block): ready to copy-paste into email or Slack
3. **Suggested log entry** (below the code block): pre-formatted for approval

Example output structure:

---

**Context:** Grafana's Rich Kreitz hasn't responded to the Feb 9 conformance email. This is a gentle nudge before the March VS.

```
Subject: FOCUS conformance check-in

Hey Rich,

[draft body]

Matt
```

**Log entry** (will be recorded after your approval):
- Provider: Grafana
- Contact: Rich Kreitz
- Channel: email
- Summary: [one-line summary of what was sent]
- Next action: [suggested follow-up]
- Next date: [suggested date]

---

## AFTER APPROVAL

Once the user approves the draft (or provides an edited version):

1. Append the log entry to `data/outreach/outreach-log.jsonl` as a single JSON line:
   ```json
   {"date": "YYYY-MM-DD", "provider": "...", "contact": "...", "channel": "...", "summary": "...", "next_action": "...", "next_date": "YYYY-MM-DD"}
   ```
2. Confirm the log entry was written.

If the user says they'll send it later or want to edit it themselves, still offer to log it. The log tracks the draft, not the send.

## EDGE CASES

- If owner is not Matt, warn before drafting: "This provider is owned by [Owner]. Want me to draft anyway?"
- If there's no contact name, flag it: "No contact on file. You'll need to identify a recipient first."
- If conformance summary shows strong resistance (e.g., Datadog's "too strict and binary" position), adjust tone to be less direct about conformance asks and more about listening.
- If the provider is very new (lead type 5-6, no prior contact), draft an introduction that briefly explains FOCUS value without assuming familiarity.
