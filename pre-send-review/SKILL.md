---
name: pre-send-review
description: Review a document for accuracy, spec compliance, and audience readiness before sharing
---

# Pre-Send Review

Systematically verify a document's claims, check FOCUS spec compliance, anticipate audience questions, and flag confirmation bias before it leaves the author's desk. Find what breaks before the audience does.

## ROLE

Act as a skeptical technical reviewer. Be adversarial toward the document's claims, not the author. Your job is to catch the errors and gaps that would undermine credibility with the stated audience.

Follow the communication style in CLAUDE.md: confident, clear, dry-humored. Short sentences. No em dashes. Cite sources (file names, line numbers, URLs) for every finding. Don't manufacture issues to justify the review. If the document is solid, say so.

## INPUTS

- **Document path** (required): absolute path to the file being reviewed
- **Audience** (required): who's receiving it. Determines which checks get extra scrutiny. Examples: "CTO", "Task Force", "provider outreach", "co-workers", "board"
- **Focus areas** (optional): specific concerns to prioritize (e.g., "FOCUS column mappings", "pricing accuracy", "sample data math")

If the document path or audience is not provided, ask before proceeding.

## PROCESS

Run six phases sequentially. After each phase, present findings and ask: **"Anything here that's wrong, already addressed, or not worth flagging?"** Incorporate corrections before proceeding.

---

### Phase 1: Source Verification

Re-read every external source cited in the document. For each factual claim tied to a source, confirm it matches.

**What to check:**
- Fetch/read every URL in the Sources section (use WebFetch for web URLs, Read for local files)
- For each factual claim, verify it against the cited source
- Check counts explicitly: if the document says "7 endpoints," count them in the source
- Flag misquotes, outdated information, and claims that overstate what the source says
- Check that links are valid and point to the right content

**Deliverable:** Table of claims checked.

| Claim (doc location) | Source | Status | Issue |
|---|---|---|---|
| "8 usage endpoints" (line 52) | OpenAI Usage API Reference | Pass | |
| "5 token types" (line 178) | Anthropic Pricing page | Pass | |

**Pause for user correction before Phase 2.**

---

### Phase 2: Spec Compliance

For any FOCUS column, value, or concept referenced in the document, verify against the spec.

**First**, fetch the FOCUS_Spec repo's authoring guidelines:
```
gh api "repos/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/contents/AGENTS.md" --jq '.content' | base64 -d
```
Extract the "Writing Specification Content & Review Guidelines" section. These rules apply to spec content and Task Force-facing documents. For provider outreach or internal docs that don't contain normative language, skip the authoring rules and check only column/value accuracy.

**What to check:**
- Read the relevant column definition files from the FOCUS_Spec repo
- Read the **glossary** definitions, not just column descriptions. Terms like "commitment discount," "negotiated discount," and "on-demand" have precise glossary definitions that may differ from casual usage.
- Verify allowed values match the spec (e.g., ChargeCategory allowed values, PricingCategory conditions)
- Check nullability rules (when MUST a column be null vs MUST NOT be null)
- Verify unit format compliance (whole numbers in quantity position, capitalized count-based units)
- Check that example values in sample rows use correct formats and valid values
- **If the document contains normative language** (MUST/SHOULD/MAY), verify it follows the AGENTS.md authoring rules: bullet list format, single constraint per bullet, under Requirements headers, no prohibited keywords (SHALL, REQUIRED, RECOMMENDED, OPTIONAL), no process-oriented verbs as primary constraints
- **If the document contains examples**, verify the non-normative disclaimer is present
- **If the document uses column references**, verify no mixing of Entity IDs (PascalCase) and Display Names (spaces) within the same normative requirement

**Deliverable:** List of spec compliance issues with citations.

| Issue | Doc location | Spec reference | Details |
|---|---|---|---|
| PricingUnit format | Line 90 | unit_format.md | "1M Tokens" is not a valid quantity. Must be whole number. |

If the document does not reference FOCUS spec concepts, skip this phase and note why.

**Pause for user correction before Phase 3.**

---

### Phase 3: Internal Consistency

Cross-reference numbers, terminology, and claims across all sections of the document.

**What to check:**
- Counts match between prose and tables (e.g., "7 endpoints" in text vs 8 rows in table)
- Terminology is consistent (same concept uses same term everywhere)
- Sample data math is correct (verify every computed value: ListUnitPrice * PricingQuantity = ListCost, row totals match stated totals)
- Forward references are fulfilled (if Section 1 says "see Section 3," confirm Section 3 delivers)
- Column headers in tables match FOCUS column names exactly (case-sensitive)
- Metadata is consistent (dates, version numbers, status labels)
- **Repetition across sections**: Is the same concept explained in full more than once? Teach it once in the first relevant section, then reference back (e.g., "see Section X for a full explanation"). Repeated explanations dilute impact and add maintenance burden.
- **Derivation transparency**: Does every computed value in narrative or sample data show a traceable derivation path? Flag values that appear without showing the formula or inputs used to produce them.

**Deliverable:** List of inconsistencies with the two conflicting locations.

**Pause for user correction before Phase 4.**

---

### Phase 4: Audience Anticipation

Given the stated audience, identify the questions they will ask and the claims they will probe.

**Audience-specific focus areas:**

| Audience | Primary check | What they'll probe |
|---|---|---|
| CTO / leadership | Stress-test the core thesis | Where are judgment calls presented as certainties? What would falsify the conclusion? Is the scope appropriately bounded? |
| Task Force / spec community | Spec compliance + pedagogical clarity | Are column mappings defensible per spec text, or do they require interpretation? Are there edge cases not addressed? For documents with examples: do unique teaching points lead each section, or are they buried after boilerplate? Are categorical claims ("Unlike X, Y...") warranted, or do they assign properties to entire categories based on limited instances? |
| Provider outreach | Product accuracy | Every claim about the provider's billing model. Mischaracterizing their product kills credibility instantly. |
| Co-workers / internal | Completeness | What obvious questions does the doc leave unanswered? Are there gaps a reasonable reviewer would flag? |
| Board / executive | Strategic framing | Does the analysis support a clear recommendation? Are risks and mitigations included? |

**Deliverable:** List of anticipated questions with assessment of whether the document answers them.

| Question the audience will ask | Answered? | Where / gap |
|---|---|---|
| "What FOCUS version is this based on?" | Yes | Header, line 6 |
| "Does this generalize beyond these two providers?" | Partially | Section 4, but claims from n=2 |

**Pause for user correction before Phase 5.**

---

### Phase 5: Confirmation Bias Scan

Explicitly look for places where the analysis presents a judgment call as settled, overstates coverage, or dismisses counterarguments.

**What to check:**
- Mappings rated as "direct fit" that actually require interpretation or have caveats
- Claims that generalize from limited evidence (n=2, single source, one provider's behavior assumed universal)
- Missing caveats on ambiguous mappings (e.g., PricingCategory for a service tier that could be "Standard" or "Other")
- Asymmetric treatment: more detail on why something works, less on where it's imperfect
- Every claim of "no gaps" or "full coverage" tested against the harshest reading of the spec
- Absence of gradient: if every mapping is "clean" with no caveats, that's a signal

**Deliverable:** List of bias flags with suggested recharacterizations.

| Location | Current framing | Concern | Suggested recharacterization |
|---|---|---|---|
| Line 196 | Flex = "Dynamic" | Flex has published fixed rates. "Dynamic" means provider can change price without notice. | "Standard" or "Other" (defensible either way) |

**Pause for user correction before Phase 6.**

---

### Phase 6: Findings Summary

Categorize all findings from Phases 1-5 by severity:

#### Fix Before Sending
Accuracy or credibility issues the audience will catch. These undermine the document's thesis if left uncorrected.

#### Consider Adding
Completeness gaps that would strengthen the analysis. Not wrong, but conspicuously absent.

#### Polish
Presentation improvements that increase professionalism. Formatting, terminology consistency, column header naming.

---

Present the categorized findings. Then ask: **"Want me to apply the fixes?"**

If yes, make the edits directly to the document. Present each edit for confirmation if the change is substantive (not just formatting).

---

## EDGE CASES

- **Document has no external sources**: skip Phase 1. Note that uncited claims are untestable and flag any claims that should have citations.
- **Document doesn't reference FOCUS spec**: skip Phase 2. Note why.
- **Audience not specified**: ask before proceeding. The audience determines the emphasis across all phases.
- **All findings are minor**: say so. Don't inflate severity to justify the review. "This is clean. Three polish items, nothing blocking." is a valid outcome.
- **Document was authored in the current conversation**: still run the full review. Proximity bias means errors in recently-authored content are the hardest to catch.
- **User says "just give me the summary"**: skip to Phase 6 with abbreviated findings. Still flag anything in "Fix Before Sending" with enough detail to act on.
- **Very long document**: prioritize Phases 1-3 (factual accuracy) over Phases 4-5 (judgment). Accuracy errors are always worse than missing nuance.

---

## USAGE

Invoke this skill by:
- `/pre-send-review path/to/doc.md --audience "CTO"`
- `/pre-send-review path/to/doc.md --audience "Task Force" --focus "column definitions"`
- "Review this before I send it to [audience]"
- "Pre-send review on the mapping doc for my CTO"
