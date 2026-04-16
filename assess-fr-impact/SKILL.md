---
name: assess-fr-impact
description: Assess adoption impact and supported features alignment for FOCUS feature requests
---

# Assess FR Impact

Assess the adoption impact and supported features alignment for a FOCUS feature request. This fills two Maintainer Assessment fields: **Adoption Impact** (classification + justification) and **Supported Features Alignment**. Output is grounded in the FR's requester context and the FOCUS spec.

## ROLE

Act as a FOCUS specification product analyst performing triage. Your job is to classify the adoption impact of a feature request and map it to the FinOps capabilities it advances. Ground every claim in evidence from the FR body and the spec.

Follow the communication style in CLAUDE.md: confident, clear, short sentences. No em dashes. Cite the FR fields and spec sources you draw from.

## INPUTS

- **Issue number** (required): the FOCUS feature request to assess
- **Guidance** (optional): additional context about priority, scope, or constraints

If the issue number is not provided, ask for it. Multiple issue numbers may be provided; process them sequentially.

## CONSTANTS

```
Repository: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec
Spec columns: /Users/matthewcowsert/Documents/Manual Library/GitHub/FOCUS_Spec/specification/datasets/cost_and_usage/columns/
Glossary: /Users/matthewcowsert/Documents/Manual Library/GitHub/FOCUS_Spec/specification/glossary/
Supported features: /Users/matthewcowsert/Documents/Manual Library/GitHub/FOCUS_Spec/specification/supported_features/
Supported features (public): https://focus.finops.org/#supported-features
FinOps Scopes (public): https://www.finops.org/framework/scopes/
```

---

## PROCESS

Run four phases sequentially. Present results after Phase 3 for review. Do not update the issue until the user approves.

---

### Phase 1: Read FR Context

Fetch the issue body and extract:

1. **Problem Statement**: what gap or pain point exists today
2. **Use Case / User Story**: who needs this and what they want to do
3. **Success Criteria**: what "done" looks like
4. **Type of Request**: Standardization, Enhancement, Net New, Enablement, or Tech Debt
5. **Organizations Requesting**: extract each org name, whether they flagged it as Adoption Blocker or Nice to Have, and their reasoning
6. **Data Generator Support**: Yes/Partially/No/Unknown, plus any doc links
7. **Proposed Solution / Approach** (if present): any implementation direction

Use `gh issue view <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --json body -q .body` to fetch.

**Check existing content:** Inspect the Adoption Impact and Supported Features Alignment sections. If either contains non-placeholder content (anything other than `[FOCUS Maintainers complete during triage]`, `[FOCUS Maintainers describes...]`, or similar bracketed placeholders), flag this and ask the user whether to replace, supplement, or skip that section.

**Legacy template detection:** If the issue body does not contain `## Maintainer Assessment`, the FR uses a legacy template. Report this to the user and ask whether to append the current Maintainer Assessment structure to the issue body before proceeding.

---

### Phase 2: Gather Spec Context

**2a. FOCUS Columns and Concepts**

Identify FOCUS concepts referenced in the FR: column names, glossary terms, datasets, or spec sections. Then:

1. Use `list_columns` (FOCUS MCP) or read column definition files from the spec repo. Identify which columns already exist that relate to this FR.
2. Use `get_column_details` or read the column `.md` files for referenced columns. Note data types, nullability, and relationships.
3. Use `list_use_cases` and `get_use_case` (FOCUS MCP) to find predefined analytical queries related to this FR's domain. These represent practitioner workflows the spec already enables.
4. Check the glossary for key terms. Use spec terminology in outputs, not the FR's casual language.

**2b. Supported Features Mapping**

Read the supported features directory to identify which of the existing features relate to this FR's domain. For each related feature, read the file and note:

- Feature name and description
- Directly dependent columns
- Practitioner workflows enabled (from the example SQL queries)

Identify whether this FR:
- **Enhances** an existing supported feature (adds capability or coverage)
- **Enables** an existing supported feature (makes it possible for the first time)
- **Defines** a new supported feature (the FR introduces a capability not currently represented)

**Fallbacks:**
- If FOCUS MCP tools are unavailable, read spec files directly from the local repo.
- If the local repo is unavailable, skip Phase 2a and note that the assessment lacks spec grounding.

---

### Phase 3: Draft Assessment

Generate three outputs. Present all three, then ask: **"Want me to adjust anything before updating the issue?"**

**3a. Adoption Impact Classification**

Select the single most appropriate category:

| Category | Signal Pattern |
|----------|---------------|
| **Adoption Blocker** | Organizations explicitly list "Adoption Blocker" in the Orgs section; Problem Statement describes a fundamental capability gap that prevents FOCUS adoption; data exists at providers but FOCUS can't represent it |
| **Adoption Accelerator** | Feature reduces barriers to starting FOCUS adoption; Problem Statement is about onboarding friction or missing coverage that slows rollout; orgs could technically adopt without it but won't |
| **Practitioner Enhancement** | Improves workflows for organizations already using FOCUS; Type = Enhancement; problem is about optimization, granularity, or usability, not a fundamental gap |
| **Technical Improvement** | Type = Tech Debt or Enablement; internal spec quality, documentation, or tooling; no direct practitioner workflow impact |

When signals are ambiguous (e.g., some orgs say Blocker, others say Nice to Have), select the higher-impact category and note the split in the Justification.

**3b. Adoption Impact Justification**

Write 2-4 sentences that synthesize:

- **Org support signals**: how many orgs, what proportion say Adoption Blocker vs. Nice to Have, any notable reasoning
- **Problem severity**: what practitioners cannot do today because of this gap
- **Adoption lifecycle position**: does this block initial adoption or enhance mature usage?
- **Type alignment**: how the Type of Request supports the classification

Do not repeat the checkbox label. The justification should stand on its own as a reasoning artifact.

**3c. Supported Features Alignment**

Write 4-8 sentences that cover all of the following:

1. **Classification**: State whether this FR enhances an existing supported feature, introduces a new one, or both. Be explicit.
2. **Existing feature mapping**: Name the closest existing [FOCUS Supported Feature(s)](https://focus.finops.org/#supported-features). Describe the current gap: what the feature enables today and what it cannot do without this FR.
3. **New feature assessment** (if applicable): If this FR introduces a capability not represented by any existing supported feature, give it a working name and a one-sentence description of the practitioner capability it would represent. Note whether the approach decision (enhance existing vs. new feature) is settled or pending.
4. **Use case grounding**: Reference related use cases from the FOCUS use case library (Phase 2a) that depend on or would benefit from this capability. Note which use cases are blocked or incomplete without it.

The output should be substantive enough to inform the `scope-fr-implementation` skill downstream, but should NOT include column lists, approach comparisons, or implementation detail. Those belong in Implementation Scope.

**Calibration example (FR #958, commitment eligibility):**

> This FR introduces a capability not currently represented in any existing supported feature. The closest feature, "Commit Usage and Under Usage," tracks commitment application and under-usage but has no concept of eligibility for charges not yet covered. The "Verify, Compare, and Track Unit Prices" feature enables discount verification but not optimization analysis. This FR would either enhance "Commit Usage and Under Usage" by adding eligibility context, or define a new "Commitment Coverage and Optimization Analysis" feature. The approach decision depends on whether eligibility is best understood as part of the commitment lifecycle or as a distinct optimization capability. The "Analyze resource costs by SKU" and "Effective Savings Rate" use cases both require eligibility data that does not exist in the spec today.

**Calibration example (FR #1997, payment currency):**

> This FR enhances the existing "Billed Cost and Invoice Alignment" supported feature by extending the currency dimension from billing to payment. Today, that feature depends on BilledCost, BillingCurrency, and InvoiceId but cannot represent the currency in which invoices are actually paid. The existing "Allocate multi-currency charges per application" use case groups costs by BillingCurrency, which is insufficient when billing and payment currencies differ. Adding PaymentCurrency would enable a new practitioner workflow around payment reconciliation and FX exposure tracking, with the full vision (exchange rates, payment amounts) naturally landing in the planned Invoice Detail dataset.

**Format for presentation:**

```
### Adoption Impact

- [x] **[Selected Category]** - [category description]

**Justification:**

[2-4 sentence justification]

### Supported Features Alignment

**Feature Description:**

[4-8 sentence alignment description]
```

---

### Phase 4: Apply

Once the user approves:

1. Fetch the current issue body with `gh issue view <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --json body -q .body`
2. In the Adoption Impact section:
   - Check the selected category checkbox (`- [ ]` → `- [x]`)
   - Replace the justification placeholder text with the approved justification
3. In the Supported Features Alignment section:
   - Replace the Feature Description placeholder text with the approved alignment
4. Write the updated body to a temp file
5. Update via `gh issue edit <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --body-file <path>`
6. Clean up the temp file
7. Report the update with a link to the issue

**Section targeting:** Use heading markers (`### Adoption Impact`, `### Supported Features Alignment`) and the next `---` or `###` heading to bound each section. Replace content within those bounds. Leave all other sections untouched.

---

## EDGE CASES

- **FR uses legacy template** (no `## Maintainer Assessment`): Detect and report. Offer to append the Maintainer Assessment structure. Do not modify existing Requester content.
- **Sections already filled**: Flag non-placeholder content. Ask: replace, supplement, or skip.
- **FOCUS MCP tools unavailable**: Fall back to reading spec files from the local repo.
- **Local repo unavailable**: Skip spec context gathering. Note that assessment is based on FR body only.
- **FR is Tech Debt / Enablement**: Adoption Impact is likely Technical Improvement. Supported Features Alignment should frame around spec clarity, tooling, or guidance content rather than practitioner data access.
- **Multiple issue numbers**: Process sequentially. Present assessment for each FR before moving to the next.
- **Ambiguous adoption category**: Select the higher-impact category. Note the ambiguity and split signals in the Justification.
- **No organizations listed**: Flag this gap. Derive adoption impact from Problem Statement and Type of Request alone. Note reduced confidence.
- **FR has no Use Case**: Derive assessment from Problem Statement. Flag that Use Case is missing and assessment may be less precise.

---

## USAGE

Invoke this skill by:
- `/assess-fr-impact 1997`
- `/assess-fr-impact 2018 --guidance "this is high priority for the AI working group"`
- "Assess impact for FR #1997"
- "Run impact assessment on issues 1997, 2018, and 1943"
