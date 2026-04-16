---
name: generate-success-criteria
description: Generate testable, practitioner-centric success criteria for FOCUS feature requests
---

# Generate Success Criteria

Draft 2-4 testable success criteria for a FOCUS feature request based on its Problem Statement, Use Cases, and available context. Output is practitioner-centric, outcome-focused, and formatted for the current FR template.

## ROLE

Act as a FOCUS specification product analyst. Your job is to articulate what "done" looks like for a feature request, not from the spec author's perspective but from the practitioner consuming the data. Every criterion you write should be verifiable by a practitioner working with a FOCUS-compliant dataset.

Follow the communication style in CLAUDE.md: confident, clear, short sentences. No em dashes. Cite the FR fields you're drawing from when explaining your reasoning.

## INPUTS

- **Issue number** (required): the FOCUS feature request to generate criteria for
- **Guidance** (optional): any additional context the user provides about scope, priority, or constraints

If the issue number is not provided, ask for it.

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

1. **Problem Statement**: what gap or pain point exists today
2. **Use Case / User Story**: who needs this and what they want to do
3. **Type of Request**: standardization, enhancement, net new, enablement, or tech debt
4. **Proposed Solution** (if present): any implementation direction already captured
5. **Existing Success Criteria** (if present): check if criteria already exist and assess quality
6. **Supporting Documentation** (if present): note any provider doc URLs for Phase 2

Use `gh issue view <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --json body -q .body` to fetch.

If Success Criteria already contains substantive, testable content (not `_No response_` or misplaced solution content), flag this and ask whether the user wants to replace, supplement, or skip.

---

### Phase 2: Spec and Provider Context

Gather external context to ground the criteria in spec reality and provider data.

**2a. FOCUS Spec Context**

Identify FOCUS concepts referenced in the FR (column names, glossary terms, datasets, supported features). Then:

1. **Check existing columns**: Use `list_columns` (FOCUS MCP) or read column definition files from the spec repo. Identify which columns already exist that relate to this FR. This prevents criteria that ask for something the spec already provides.
2. **Read relevant definitions**: Use `get_column_details` or read the column `.md` files for any referenced columns. Extract data types, nullability rules, allowed values, and relationships. This grounds criteria in precise spec language.
3. **Check related use cases**: Use `list_use_cases` and `get_use_case` (FOCUS MCP) to find predefined analytical queries related to this FR's domain. These represent practitioner workflows the spec already enables and reveal gaps.
4. **Check glossary**: Read glossary definitions for key terms. Use spec terminology in criteria, not the FR's casual language.

**2b. Provider Context**

If the FR's Supporting Documentation contains provider doc URLs:

1. Fetch up to 3 provider doc links using WebFetch
2. Note what data each provider already exposes (strengthens "Standardization" criteria)
3. Note gaps where providers don't expose data (strengthens "Net New" criteria)

If no provider URLs are present but the FR references specific providers, note this as a limitation. Do not speculatively search for provider docs.

**Present:** A brief context summary (not the full spec text). Example:

> **Spec context:** FOCUS v1.2 defines 5 commitment-related columns (CommitmentDiscountId, CommitmentDiscountCategory, CommitmentDiscountQuantity, CommitmentDiscountStatus, CommitmentDiscountUnit). None cover commitment term dates, quantities at purchase, or convertibility. The "Commitment Discount" use cases enable utilization analysis but not expiration tracking.
>
> **Provider context:** AWS exposes reservation start/end dates in CUR. Azure exposes term length in Reservations API. GCP exposes CUD start/end in commitment resources. All three have the underlying data; it's not normalized.

---

### Phase 3: Draft Criteria

Generate 2-4 success criteria using the FR context (Phase 1) and spec/provider context (Phase 2). Each criterion must pass all five quality checks:

**Quality checks:**

| Check | Requirement | Anti-pattern |
|---|---|---|
| Practitioner-centric | States what a practitioner (or data engineer, finance team) can DO | "FOCUS adds a column for X" |
| Testable | A reviewer can verify yes/no against a FOCUS-compliant dataset | "Improved consistency across providers" |
| Outcome-focused | Describes the end state, not the implementation path | "Create a lookup table mapping SKUs to categories" |
| Specific | Tied to this FR's domain, not generic to any FR | "Data is available from all supporting data generators" |
| Non-redundant | Each criterion covers a distinct facet of success | Two criteria that both test "data is available" |

**Criterion lenses (use 2-4 of these per FR):**

| Lens | What it tests | Template |
|---|---|---|
| Data availability | Can practitioners access the specific data this FR introduces? | "Practitioners can [identify/query/segment] [specific data point] for [purpose]" |
| Cross-provider consistency | Is the data normalized across data generators? | "[Data/concept] is consistently [represented/structured] across data generators that support this capability" |
| Actionability | Can practitioners act on the data without workarounds? | "Practitioners can [perform analysis/build report/automate process] using [the data] without [manual step/external data]" |
| Clarity | Are ambiguous concepts now distinguishable? | "[Concept A] is clearly [distinguishable/defined] relative to [Concept B]" |
| Guidance | Do data generators know what to implement? | "Data generators have clear guidance on [how to represent/when to populate/what values to use for] [the data]" |

**Using spec context to strengthen criteria:**

- If Phase 2 found existing columns that overlap, reference them by name. Example: "Practitioners can determine commitment expiration dates, which is not currently derivable from CommitmentDiscountId or CommitmentDiscountStatus alone"
- If Phase 2 found related use cases, criteria should enable the gap. Example: if "Commitment Utilization" queries exist but "Commitment Renewal Planning" does not, frame a criterion around the missing workflow.
- If Phase 2 found provider data exists, lean toward consistency criteria. If provider data doesn't exist, lean toward guidance criteria.
- Use spec glossary terms, not casual FR language. Link terms where they have glossary definitions.

**Format:**

```markdown
- [ ] Criterion text here
- [ ] Criterion text here
- [ ] Criterion text here
```

**Present:**

Show the drafted criteria in a code block, followed by a reasoning table:

| # | Criterion | Lens | Derived from | Spec grounding |
|---|---|---|---|---|
| 1 | "Practitioners can..." | Data availability | Problem Statement, para 2 | No existing column covers this (Phase 2a) |
| 2 | "Cost analysis can be..." | Actionability | Use Case 1 | Extends "Commitment Utilization" use case |
| 3 | "[Concept] is consistently..." | Consistency | Type: Standardization | AWS/Azure/GCP all expose this data (Phase 2b) |
| 4 | "Data generators have..." | Guidance | Type: Net New | No provider currently normalizes this |

Then ask: **"Want me to adjust any of these before updating the issue?"**

---

### Phase 4: Apply

Once approved, update the issue body:

1. Fetch the current body
2. Replace the Success Criteria section content with the approved criteria
3. Write to a temp file and update via `gh issue edit <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --body-file <path>`

Report the update status.

---

## CALIBRATION EXAMPLES

These are real "Good" criteria from existing FRs to calibrate quality:

**FR #2018 (AI execution parameters):**
```
- [ ] Practitioners can identify which model was used and what configuration parameters were set for each charge
- [ ] Cost-per-token analysis can be segmented by model configuration (e.g., high-temperature creative tasks vs. low-temperature deterministic tasks)
- [ ] Data generators have clear guidance on which AI execution parameters to expose in FOCUS data
```

**FR #982 (Clarify EffectiveCost vs BilledCost):**
```
- Can perform accrual-based cost allocation across all providers without custom filtering
- EffectiveCost is clearly distinguishable from BilledCost in both definition and use case
- Commitment discount rows balance correctly without requiring provider-specific logic
```

**FR #958 (Commitment eligibility):**
```
- Practitioners can calculate commitment coverage without relying on external provider data
- Tooling can provide commitment optimization recommendations using only FOCUS data
- ESR calculations are achievable with FOCUS columns alone
```

Notice the pattern: each criterion starts with who can do what, stays specific to the FR's domain, and is testable against a dataset.

---

## EDGE CASES

- **FR has no Use Case**: derive criteria from Problem Statement alone. Flag that Use Case is missing and criteria may be less specific.
- **FR is tech debt or enablement**: criteria may be about spec clarity, consistency, or maintainability rather than practitioner data access. That's fine. Frame as "Spec authors can..." or "Data generators can..." instead.
- **FR has very rich existing content**: if the FR already has a detailed "Success Metrics" subsection (common in the enriched FRs like #958, #982), extract and reformat rather than regenerating from scratch. Preserve the author's intent.
- **FR scope is contested**: note in the reasoning that scope affects criteria. Draft criteria for the stated scope, and flag where narrower/broader scope would change them.
- **Multiple FRs requested**: process each sequentially, presenting criteria for each before moving to the next.
- **FOCUS MCP tools unavailable**: fall back to reading spec files directly from the local repo. If the local repo is also unavailable, skip Phase 2a and note that criteria are not spec-grounded.
- **No provider docs linked**: skip Phase 2b. Do not speculatively search for provider documentation. Note in the reasoning table that provider grounding is absent.
- **FR references columns not yet in spec**: the FR may propose new columns. Don't treat "column doesn't exist yet" as a problem. Instead, use it to inform whether criteria should emphasize guidance (data generators need clarity on something new) vs. consistency (something already exists but varies).

---

## USAGE

Invoke this skill by:
- `/generate-success-criteria 1041`
- `/generate-success-criteria 1384 --guidance "scope this to just the AmortizedCost column, not AmortizedUnitPrice"`
- "Generate success criteria for FR #1070"
- "Draft success criteria for issues 1027, 1028, and 1039"
