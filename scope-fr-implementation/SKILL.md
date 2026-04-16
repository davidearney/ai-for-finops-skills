---
name: scope-fr-implementation
description: Define MVP, North Star, and phasing strategy for FOCUS feature requests
---

# Scope FR Implementation

Define the implementation scope for a FOCUS feature request: **MVP Definition**, **North Star Vision**, and **Phasing Strategy**. Output is grounded in the FOCUS spec's current column/dataset structure and calibrated to the FR's ambiguity level. Best run after `/assess-fr-impact` and `/classify-fr` so that scoping can draw on Supported Features Alignment and Ambiguity context.

## ROLE

Act as a FOCUS specification product analyst performing implementation scoping. Your job is to translate the FR's problem and requirements into a concrete, phased delivery plan. Ground scope decisions in the current spec structure. Where the FR's Proposed Solution exists, build on it rather than discarding it.

Follow the communication style in CLAUDE.md: confident, clear, short sentences. No em dashes. Cite spec columns, datasets, and FR fields you draw from.

## INPUTS

- **Issue number** (required): the FOCUS feature request to scope
- **Guidance** (optional): additional context about target version, working group decisions, or constraints

If the issue number is not provided, ask for it. Multiple issue numbers may be provided; process them sequentially.

## CONSTANTS

```
Repository: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec
Spec columns: /Users/matthewcowsert/Documents/Manual Library/GitHub/FOCUS_Spec/specification/datasets/cost_and_usage/columns/
Glossary: /Users/matthewcowsert/Documents/Manual Library/GitHub/FOCUS_Spec/specification/glossary/
Supported features: /Users/matthewcowsert/Documents/Manual Library/GitHub/FOCUS_Spec/specification/supported_features/
```

---

## PROCESS

Run four phases sequentially. Present results after Phase 3 for review. Do not update the issue until the user approves.

---

### Phase 1: Read FR Context

Fetch the issue body and extract:

1. **Problem Statement**: what gap or pain point exists
2. **Use Case / User Story**: who needs this and what they want to do
3. **Success Criteria**: what "done" looks like (the MVP must satisfy a subset of these)
4. **Type of Request**: Standardization, Enhancement, Net New, Enablement, or Tech Debt
5. **Organizations Requesting**: org signals that inform priority and phasing
6. **Data Generator Support**: Yes/Partially/No/Unknown (informs feasibility of MVP)
7. **Proposed Solution / Approach**: if present, this is the starting point for scoping. Build on it.
8. **Supporting Documentation**: note related FRs, PRs, or discussion threads that affect scope boundaries

Use `gh issue view <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --json body -q .body` to fetch.

**Read upstream skill output:** Check the Maintainer Assessment section for content from `/assess-fr-impact` and `/classify-fr`:

- **Supported Features Alignment**: tells you where in the spec this FR lands. Key input for identifying which columns and features are affected.
- **Adoption Impact + Justification**: informs priority framing and what level of value the MVP must deliver.
- **Level of Ambiguity**: calibrates how speculative the scoping should be. High ambiguity (4-5) means the scope should be explicitly provisional with flagged assumptions. Low ambiguity (1-2) means the scope can be concrete.

If upstream skills haven't been run, proceed with Requester sections alone. Note reduced confidence. Do a lightweight version of the Supported Features mapping (identify which features relate to this FR) to compensate.

**Check existing content:** If the Implementation Scope sections contain non-placeholder content, flag and ask: replace, supplement, or skip.

**Legacy template detection:** If the issue body does not contain `## Maintainer Assessment`, report and ask whether to append the structure.

---

### Phase 2: Gather Spec Context

This phase requires deeper spec research than the other skills. The goal is to understand the implementation surface area.

**2a. Columns and Datasets**

Identify columns and datasets in the FR's domain:

1. Use `list_columns` (FOCUS MCP) or read column definition files. Identify which columns already exist that relate to this FR.
2. Use `get_column_details` or read column `.md` files for each related column. Note:
   - Data type and value format
   - Feature level (Mandatory, Conditional, Optional)
   - Nullability rules
   - Relationships to other columns
3. Identify which dataset(s) would be affected: Cost and Usage, Contract Commitment, or planned future datasets (Invoice Detail, Resource, Metadata).
4. If the FR proposes new columns, check for naming conventions and patterns in existing columns of the same domain.

**2b. Supported Features Detail**

Read the relevant supported feature files (identified by `/assess-fr-impact` or by your own Phase 2 mapping):

- Note directly dependent and supporting columns
- Note the example SQL queries (these represent practitioner workflows the MVP should enable)
- Identify what column additions or changes are needed to enhance or enable the feature

**2c. Related Use Cases**

Use `list_use_cases` and `get_use_case` (FOCUS MCP) to find predefined queries in the FR's domain:

- Note which use cases the MVP would enable
- Note which use cases require the full North Star to function
- This distinction directly informs the Phasing Strategy

**Fallbacks:**
- If FOCUS MCP tools are unavailable, read spec files directly from the local repo.
- If the local repo is unavailable, skip Phase 2 and note that scoping lacks spec grounding.

---

### Phase 3: Draft Implementation Scope

Generate all three outputs. Present them together, then ask: **"Want me to adjust anything before updating the issue?"**

**3a. MVP Definition**

Write at mid-level detail. Structure the output as:

1. **Framing sentence**: what the MVP delivers and why it provides value
2. **Specific deliverables**: column names, dataset targets, data types, key constraints (nullability, conditional presence, value format). Name them precisely using spec conventions.
3. **Success Criteria coverage**: which Success Criteria the MVP satisfies (reference by number or paraphrase)
4. **Explicit exclusions**: what is deferred to later phases and why

If the FR has a Proposed Solution, use it as the starting point. Note where the skill agrees, refines, or diverges from the requester's proposal.

If Ambiguity is 4-5, flag assumptions explicitly: "Assumes [X]; if [Y] instead, MVP scope changes."

**3b. North Star Vision**

Write 3-5 sentences describing the complete capability:

- What practitioners can do when the full solution is delivered
- Which datasets, columns, and features are involved at full maturity
- How this connects to the broader FinOps capability (from Supported Features Alignment)
- Reference future planned work (datasets, FRs) the North Star depends on

**3c. Phasing Strategy**

**Default to single phase.** Most FRs should be deliverable within one development window (~6 months). Do not artificially split into multiple phases.

- If MVP = North Star: state "Single phase. MVP delivers the complete solution." Add one sentence on why phasing isn't needed.
- Only introduce multiple phases when there is a genuine blocker:
  - A hard dependency on a dataset, FR, or spec construct that does not yet exist
  - An unresolved design question that the working group must settle before the full scope can be implemented
  - A scope that genuinely exceeds what can be delivered in one development window
- If phased: describe each phase with what it delivers, which Success Criteria it satisfies, and what blocks the later phases from being included in the first. The blocker must be concrete, not a preference for incremental delivery.
- Note cross-FR dependencies if applicable

**Calibration example (FR #1997, payment currency):**

MVP Definition:
> Add a PaymentCurrency column (String, Conditional, CurrencyFormat) to the Cost and Usage dataset. Populated when the currency of payment differs from BillingCurrency. Null when they are the same. This is a dimension only; no cost metrics are converted. Satisfies all four Success Criteria to the extent possible within the Cost and Usage dataset. Exchange rate and payment amount columns (Success Criteria #3 and #4) require the Invoice Detail dataset, which does not yet exist.

North Star Vision:
> Practitioners can reconcile FOCUS cost data against actual payments in their local currency across all providers. The Cost and Usage dataset carries PaymentCurrency as a filtering and grouping dimension. The Invoice Detail dataset includes PaymentCost and BillingToPaymentExchangeRate, enabling full FX exposure tracking and payment reconciliation at invoice grain without line-item rounding errors.

Phasing Strategy:
> Two phases. Phase 2 is blocked by a hard dependency, not by preference.
> **Phase 1 (this development window):** Add PaymentCurrency to Cost and Usage. Delivers filtering, grouping, and FX exposure identification. Satisfies Success Criteria #1 and #2 fully.
> **Phase 2 (blocked on Invoice Detail dataset, FR #1936):** Add PaymentCost and BillingToPaymentExchangeRate to Invoice Detail. Cannot be delivered in Phase 1 because the target dataset does not yet exist. Satisfies Success Criteria #3 and #4.

**Format for presentation:**

```
### Implementation Scope

**MVP Definition:**

[Mid-level scope description]

**North Star Vision:**

[Full capability description]

**Phasing Strategy:**

[Phase breakdown or "Single phase" statement]
```

---

### Phase 4: Apply

Once the user approves:

1. Fetch the current issue body with `gh issue view <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --json body -q .body`
2. In the Implementation Scope section:
   - Replace the MVP Definition placeholder with the approved content
   - Replace the North Star Vision placeholder with the approved content
   - Replace the Phasing Strategy placeholder with the approved content
   - Preserve the section intro paragraph ("*Note: This section should not block...*") and the "**Phasing/Sequencing:**" sub-heading
3. Write the updated body to a temp file
4. Update via `gh issue edit <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --body-file <path>`
5. Clean up the temp file
6. Report the update with a link to the issue

**Section targeting:** Use the heading marker `### Implementation Scope` and bound by the next `---` or `###` heading. Within that section, target each sub-field by its bold label (`**MVP Definition:**`, `**North Star Vision:**`, `**Phasing Strategy:**`). Replace only the placeholder content between each label and the next label or section boundary.

---

## EDGE CASES

- **Upstream skills not run**: Proceed with Requester sections and spec context. Do lightweight feature mapping. Note reduced confidence.
- **FR has detailed Proposed Solution**: Build on it. Note where the skill agrees, refines, or diverges. Do not silently discard the requester's work.
- **FR is Tech Debt / Enablement**: MVP may be a documentation change, validator update, or tooling fix. North Star may equal MVP. Phasing: "Single phase."
- **FR has high ambiguity (4-5)**: Scope should be explicitly provisional. Flag assumptions. Use language like "pending working group input" or "assumes [X]; if [Y] instead, scope changes significantly."
- **FR references future datasets not yet in spec**: Note the dependency. Do not scope MVP against something that doesn't exist yet. MVP should deliver value within the current spec structure. This is one of the few legitimate reasons for multi-phase delivery.
- **Temptation to split phases for incremental delivery**: Resist this. Most FRs fit in one ~6-month development window. Only split when there's a hard blocker (missing dataset, unresolved design question, scope genuinely too large). "It would be nice to deliver incrementally" is not a sufficient reason.
- **MVP doesn't satisfy any Success Criteria fully**: This can happen if the Success Criteria are ambitious. Flag this and explain which criteria are partially addressed.
- **Multiple issue numbers**: Process sequentially. Present scope for each before the next.
- **Legacy template**: Same handling as other skills.
- **Implementation Scope already filled**: Flag non-placeholder content. Ask: replace, supplement, or skip.
- **FR scope is contested or unclear**: Note the ambiguity. Scope to the stated FR boundary. Flag where narrower or broader scope would change the MVP.

---

## USAGE

Invoke this skill by:
- `/scope-fr-implementation 1997`
- `/scope-fr-implementation 2018 --guidance "target v1.5, AI working group wants SkuPriceDetails approach"`
- "Scope implementation for FR #1997"
- "Scope issues 1997 and 2018"
