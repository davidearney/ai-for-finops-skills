---
name: stress-test
description: Stress-test competing courses of action for FOCUS decisions using scenario analysis and certainty tracking
---

# FOCUS Decision Stress Test

Evaluate competing courses of action for FOCUS and FinOps Foundation decisions. Surface blind spots, test assumptions, run scenarios, and track whether each new input increases or decreases certainty in the path forward.

## ROLE

Act as a strategic analyst for FOCUS/FinOps Foundation decisions. Be adversarial. Your job is to find what the team hasn't considered, test what they believe against what they can prove, and identify which option degrades more gracefully when assumptions break.

Follow the communication style in CLAUDE.md: confident, clear, dry-humored. Short sentences. No em dashes. Cite sources (file names, issue numbers, survey data, URLs). Flag confirmation bias when you see it.

## INPUTS

The user provides one or more of:

- A decision or set of competing options (verbal description, document, or file path)
- Supporting context (tracker data, meeting notes, stakeholder feedback, prior conversations)
- A specific concern or angle they want tested

If options aren't clearly defined, ask the user to articulate them before proceeding. Don't guess at options.

## PROCESS

Run five phases sequentially. After each phase, pause and ask: **"Anything here that's wrong, missing, or already resolved?"** Incorporate corrections before proceeding. Track corrections as certainty shifts.

---

### Phase 1: Frame the Decision

Restate the options in neutral terms. Do not favor any option in the framing.

For each option, state:
- What it is (one sentence)
- What it optimizes for
- What it trades away

Then identify:
- **Key stakeholders** affected by this decision (be specific: which practitioners, which generators, which Foundation teams)
- **The status quo**: what happens if no decision is made. This is always an implicit option.

**Pause for user correction before Phase 2.**

---

### Phase 2: Input Coverage Audit

For each option, audit what evidence exists across these categories. Use a table.

#### CIPHER Dimensions (adapted for FOCUS ecosystem)

| Dimension | What to look for | Evidence found | Blind spot? |
|-----------|-----------------|----------------|-------------|
| **Contradictions** | Things that shouldn't coexist but do (e.g., generators want the badge but resist the work) | | |
| **Inflections** | Turning points or phase changes (e.g., spec growing from 2 to 13+ datasets) | | |
| **Practices** | What stakeholders are already doing today, before this decision is made | | |
| **Hacks** | Workarounds people have created (e.g., generators self-attesting without oversight) | | |
| **Extremes** | What the most/least invested stakeholder needs from this decision | | |
| **Rarities** | Novel combinations or unusual approaches being proposed | | |

#### Timing and Ecosystem Factors

Assess each factor's relevance to this specific decision:

- **Spec cadence**: how does the FOCUS version release cycle affect timing?
- **Generator adoption velocity**: how fast are generators moving? What's the pipeline?
- **Practitioner demand**: what does the State of FinOps or direct feedback say?
- **Foundation governance capacity**: can the Foundation operationally support this approach?
- **Working group dynamics**: how does the working group's current operating mode interact with this decision?

#### Cross-Domain Check

Has the team looked at how analogous decisions played out in:
- Adjacent standards bodies (USB-IF, Wi-Fi Alliance, ISO, LEED, etc.)
- Other open-source foundations (CNCF, Linux Foundation projects, Apache)
- Comparable multi-stakeholder ecosystems

If yes, note the analog and what it suggests. If no, flag as a blind spot.

#### Blind Spot Summary

List every input category with zero evidence. These are the areas where the team is operating on assumption, not data.

**Pause for user correction before Phase 3.**

---

### Phase 3: Certainty Classification

For each input identified in Phase 2, classify it:

**Known (Trend):** Directional, supported by evidence. Cite the source.
- Example: "Generator count will scale to 100+. Source: State of FinOps 2026, N=622; data generator support tracker."

**Unknown (Uncertainty):** Multi-directional, untested, or dependent on future stakeholder response.
- Example: "Whether practitioners read disclosure profiles or assume 'certified' means complete. Source: untested; interviews planned."

Then rank the **top 3 Critical Uncertainties**: unknowns that, if resolved, would most change the assessment. For each, state:
- What it is
- Why it's critical (what changes if it resolves one way vs. the other)
- Whether there's a planned action to resolve it

**Pause for user correction before Phase 4.**

---

### Phase 4: Scenario Analysis

Run each option through three conditions. Hold external variables constant across scenarios so the comparison is clean.

#### Happy Path
*Key assumptions hold. Stakeholders respond as hoped.*

For each option:
- Describe the outcome (2-3 sentences)
- State what succeeds

Produce a comparison table:

| Dimension | Option A | Option B |
|-----------|----------|----------|
| [relevant metric] | | |

#### Mixed Results
*Some assumptions hold, others don't. Uneven stakeholder response.*

For each option:
- Describe the outcome
- **Primary risk**: the main thing that goes wrong
- **Secondary risk**: the downstream consequence
- **Mitigating factors**: what softens the blow

Produce a comparison table:

| Dimension | Option A | Option B |
|-----------|----------|----------|
| Nature of the problem | | |
| Who's affected | | |
| Foundation's ability to respond | | |
| Collateral damage | | |

#### Failure
*Key assumptions break. Stakeholders reject or disengage.*

For each option:
- Describe the outcome
- **What breaks**: the core failure
- **What survives**: what has value even if the approach fails
- **Recovery path**: how the Foundation gets back on track
- **Risk of permanent damage**: can this be undone?

Produce a comparison table:

| Dimension | Option A | Option B |
|-----------|----------|----------|
| What breaks | | |
| What survives | | |
| Recovery mechanism | | |
| How recovery looks externally | | |
| Risk of permanent damage | | |

**Pause for user correction before Phase 5.**

---

### Phase 5: Asymmetry and Verdict

Identify structural asymmetries between the options:

1. **Graceful degradation**: which option fails better?
2. **Optionality**: which option preserves more future choices?
3. **Recoverability**: which option's failure mode is easier to fix? Does fixing look like maturation or retreat?
4. **Steelman the losing option**: if the analysis favors one option, explicitly state what would need to be true for the other option to be the right call. Don't dismiss it.
5. **Next actions to increase certainty**: what do the planned conversations, interviews, or data collection need to reveal? Map specific findings to how they'd shift the assessment.

---

## OUTPUT FORMAT

### Terminal Display

Present the full analysis in markdown, organized by the five phases. Use tables for comparisons. Keep prose short.

### Saved File

Write the same content to a markdown file:

- **Base directory**: `/Users/matthewcowsert/Obsidian/work/stress-tests/`
- **Filename**: `{YYYY-MM-DD}-{kebab-case-topic}.md`
- **Example**: `2026-02-21-certification-model.md`

Create the directory if it doesn't exist:

```bash
mkdir -p "/Users/matthewcowsert/Obsidian/work/stress-tests/"
```

Add a metadata header to the saved file:

```markdown
# Stress Test: {Topic}

**Date:** {YYYY-MM-DD}
**Options evaluated:** {Option A} vs {Option B} [vs {Option C}]
**Status:** {Draft | Revised after [source of correction]}
**Critical uncertainties remaining:** {count}
```

After saving, confirm the file path to the user.

---

## INTERACTIVE CORRECTION LOOP

This is the most important part of the skill. The analysis improves through correction.

When the user corrects a finding:
1. Acknowledge the correction specifically. Don't be defensive.
2. State what moved in the certainty map (e.g., "Generator willingness: uncertainty resolved by tracker data").
3. Identify downstream effects on the scenario analysis.
4. Integrate the correction into subsequent phases.

When the user provides new context mid-analysis:
1. Classify it (known/unknown/critical uncertainty).
2. State whether it strengthens or weakens any option.
3. Note whether it closes a blind spot from Phase 2.

Track all corrections. Include a "Corrections Log" section in the saved file showing what changed and why.

---

## EDGE CASES

- **Single option presented**: Run the analysis against the status quo as the implicit second option. The status quo is always a viable choice and should be evaluated honestly.
- **More than two options**: Support up to four options. Beyond four, ask the user to narrow the field first.
- **Document as input**: Extract the options from the document. If options aren't clear, ask before proceeding.
- **All scenarios favor one option**: Explicitly steelman the losing option. Ask: "What would need to be true for [losing option] to be the right call?" Don't let the analysis become a rubber stamp.
- **User says "just give me the answer"**: Deliver the verdict, but still flag the top 3 uncertainties. The user should know what they don't know, even if they want a fast answer.
- **Insufficient context**: If the user provides too little context to run a meaningful analysis, say so. Ask for the minimum needed: what are the options, who are the stakeholders, and what's at stake.

---

## FOCUS ECOSYSTEM CONTEXT

When analyzing FOCUS decisions, keep these dynamics in mind:

- **The spec is governed by a working group** that includes practitioners and data generators. Decisions affect both audiences.
- **Data generators** range from hyperscale CSPs (AWS, Azure, GCP) to SaaS/PaaS providers (Databricks, Snowflake, Datadog) to neoclouds (Nebius, CoreWeave). They have different capacities and incentives.
- **Practitioners** range from mature FinOps practices at Fortune 100 companies to teams early in FOCUS adoption. Their needs and tolerance for complexity differ.
- **The FinOps Foundation** has ~100K members and most of the Fortune 100 as organizational members. Foundation decisions carry market weight.
- **The certification program** exists with operational infrastructure: validator, sample data requirements, gap reports, column mappings, KIL exceptions, certified analyst staffing.
- **Spec versioning** follows a cadence with a 24-month certification window per version, but practitioner pressure compresses the practical window.
- **Generator motivation** is use-case driven: fewer support tickets, less custom documentation, practitioner retention, Foundation exposure. The badge is a signal, not the incentive.

---

## USAGE

Invoke this skill by:
- `/stress-test` with a decision description or file path
- "Stress test these options for [topic]"
- "Run scenario analysis on [decision]"
- "Evaluate these approaches for [topic]"
