---
name: classify-fr
description: Classify FOCUS feature requests by impacted parties, ambiguity, and FinOps scope
---

# Classify Feature Request

Classify a FOCUS feature request across three Maintainer Assessment fields: **Impacted Parties**, **Level of Ambiguity** (1-5 with rationale), and **FinOps Scope Alignment**. Best run after `/assess-fr-impact` so that Ambiguity can draw on the Supported Features Alignment output.

## ROLE

Act as a FOCUS specification product analyst performing triage classification. Your job is to categorize the FR's impact surface, rate its definitional maturity, and map it to FinOps scopes. Every classification should be traceable to evidence in the FR body.

Follow the communication style in CLAUDE.md: confident, clear, short sentences. No em dashes. Cite the FR fields you draw from.

## INPUTS

- **Issue number** (required): the FOCUS feature request to classify
- **Guidance** (optional): additional context about scope, priority, or constraints

If the issue number is not provided, ask for it. Multiple issue numbers may be provided; process them sequentially.

## CONSTANTS

```
Repository: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec
FinOps Scopes (public): https://www.finops.org/framework/scopes/
```

---

## PROCESS

Run three phases sequentially. Present results after Phase 2 for review. Do not update the issue until the user approves.

---

### Phase 1: Read FR Context

Fetch the issue body and extract:

1. **Problem Statement**: what gap or pain point exists
2. **Use Case / User Story**: who needs this and what they want to do
3. **Success Criteria**: what "done" looks like
4. **Type of Request**: Standardization, Enhancement, Net New, Enablement, or Tech Debt
5. **Organizations Requesting**: org names and blocker/nice-to-have signals
6. **Data Generator Support**: Yes/Partially/No/Unknown
7. **Proposed Solution / Approach** (if present)
8. **Supporting Documentation** (if present): note any provider-specific references

Use `gh issue view <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --json body -q .body` to fetch.

**Read upstream skill output:** Check the Maintainer Assessment section for content written by `/assess-fr-impact`:

- **Supported Features Alignment**: If filled (non-placeholder), use it to inform the Ambiguity rating. It tells you whether this FR maps to existing features or charts new territory.
- **Adoption Impact + Justification**: If filled, use as secondary context for Impacted Parties and Ambiguity.

**Check existing content:** Inspect the Impacted Parties, Level of Ambiguity, and FinOps Scope Alignment sections. Handle each independently:

- If a section contains non-placeholder content, flag it and ask whether to replace or skip that section.
- Impacted Parties and FinOps Scope checkboxes may be pre-checked by the requester. These are requester estimates. Assess independently and flag discrepancies in the Phase 2 presentation.

**Legacy template detection:** If the issue body does not contain `## Maintainer Assessment`, the FR uses a legacy template. Report this to the user and ask whether to append the current Maintainer Assessment structure before proceeding.

---

### Phase 2: Draft Classification

Generate all three outputs. Present them together, then ask: **"Want me to adjust anything before updating the issue?"**

**2a. Impacted Parties**

Check all that apply based on the FR's impact surface:

| Party | Check when... |
|-------|--------------|
| **FinOps Practitioner** | FR affects how practitioners analyze, allocate, report, or act on cost data. Almost always checked unless pure internal tech debt. |
| **FOCUS Data Generator** | FR changes the data schema, adds/modifies columns, changes nullability, or alters how data generators must produce FOCUS output. |
| **Vendor Supporting FOCUS** | FR changes how FinOps tools, platforms, or UIs that ingest FOCUS data need to display, interpret, or process the data. |
| **Other** | Rarely used. Specify if the FR affects a party not covered above (e.g., auditors, regulators). |

Signals: Problem Statement (who's affected), Use Cases (whose workflow changes), Type of Request (Tech Debt rarely impacts practitioners), Proposed Solution (schema changes impact data generators).

If the requester pre-checked boxes, compare your assessment. Flag any differences: "Requester checked [X]; this assessment [agrees/disagrees] because [reason]."

**2b. Level of Ambiguity**

Rate from 1 to 5. Provide a rationale calibrated to the complexity.

**Ambiguity factors:**

| Factor | Reduces Ambiguity | Increases Ambiguity |
|--------|-------------------|---------------------|
| Problem clarity | Well-defined gap with practitioner examples | Vague or conceptual problem statement |
| Solution maturity | Proposed solution exists, TF discussion captured | No solution direction, competing approaches |
| Scope boundaries | Clear FR boundary, no overlap with other FRs | Broad scope, overlaps other FRs or datasets |
| Data generator readiness | Providers already expose this data | Net new concept, no provider data exists |
| Spec impact breadth | Touches one column or one dataset | Touches multiple columns, datasets, or glossary |
| Community consensus | Agreement on approach in TF or community | Competing views, unresolved design questions |
| Supported Features alignment | Maps cleanly to existing feature | Unclear where it lands, may need new feature |

**Inputs:**
1. Requester sections (always available)
2. Supported Features Alignment from `/assess-fr-impact` (if filled). This is the strongest signal for whether the FR maps cleanly to existing spec structure.
3. If `/assess-fr-impact` has not been run, derive from Requester sections alone and note in the rationale: "Supported Features Alignment not yet assessed; confidence is reduced."

**Rationale format:**
- For ratings 1-2: 2-3 sentences on what makes this well-defined.
- For ratings 3-5: structured as factors reducing ambiguity, then remaining complexity. 4-8 sentences total.

**Calibration examples:**

FR #1997 (Payment Currency, Enhancement, detailed proposed solution, one org):

> **2** — The problem is well-defined (billing vs. payment currency gap) with clear practitioner impact. A phased solution is already proposed with specific column names and dataset targets. The main complexity is the grain mismatch between line-item and invoice-level conversion, which the proposed solution explicitly addresses. Low remaining ambiguity.

FR #958 (Commitment Eligibility, Standardization + Net New, 10 orgs, extensive TF discussion):

> **3** — Scope was clarified through multiple TF sessions (July-December 2025), and community discussion established the boundary between hypothetical and real costs. Provider eligibility patterns are documented. Remaining complexity: the solution approach (boolean vs. JSON eligibility metadata) is unsettled, overlapping eligibility across commitment types needs resolution, and SaaS pricing tiers use different terminology than CSP commitments. Cross-provider variation in granularity (service-level vs. SKU-level) adds implementation decisions.

**2c. FinOps Scope Alignment**

Check all that apply:

| Scope | Check when... |
|-------|--------------|
| **Public Cloud** | FR references AWS, Azure, GCP, OCI, or general IaaS/PaaS concepts |
| **SaaS** | FR references SaaS providers (Snowflake, Salesforce, Datadog), marketplace purchases, or subscription-based services |
| **Data Center** | FR references on-prem compute, colocation, or physical infrastructure |
| **Licensing** | FR references subscription or usage-based licensing models |
| **AI** | FR references AI/ML models, tokens, inference, training costs, or AI platforms |
| **Custom** | FR references internal tooling, custom infrastructure, or specialized environments |

Signals: Problem Statement (what environment), Use Cases (what providers), Supporting Documentation (provider docs linked), Data Generator Support, Proposed Solution.

If the requester pre-checked scopes, compare your assessment. Flag differences.

**Format for presentation:**

```
### Specification Impact

**Impacted Parties:**
- [x] FinOps Practitioner – end users who analyze or act on the data
- [x] FOCUS Data Generator – data generators producing output aligned to the spec
- [ ] Vendor Supporting FOCUS – vendors or tools ingesting the spec or using the spec language in their UI
- [ ] Other: [specify]

[If requester pre-checked differently, note discrepancy here]

**Level of Ambiguity:**

[1-5]

[Rationale]

### FinOps Scope Alignment

- [x] Public Cloud – e.g., AWS, Azure, GCP, OCI
- [ ] Software-as-a-Service (SaaS) – e.g., Salesforce, Snowflake
- [ ] Data Center – on-prem compute and infrastructure
- [ ] Licensing – subscription or usage-based licensing models
- [ ] AI – cost and usage for AI models and platforms
- [ ] Custom – internal tooling, specialized infra

[If requester pre-checked differently, note discrepancy here]
```

---

### Phase 3: Apply

Once the user approves:

1. Fetch the current issue body with `gh issue view <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --json body -q .body`
2. In the Specification Impact section:
   - Replace the Impacted Parties checkboxes entirely with the approved set
   - Replace the Level of Ambiguity placeholder with the approved rating and rationale
3. In the FinOps Scope Alignment section:
   - Replace the checkboxes entirely with the approved set
4. Write the updated body to a temp file
5. Update via `gh issue edit <number> -R FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec --body-file <path>`
6. Clean up the temp file
7. Report the update with a link to the issue

**Section targeting:** Use heading markers (`### Specification Impact`, `### FinOps Scope Alignment`) and the next `---` or `###` or `##` heading to bound each section. Replace content within those bounds. Leave all other sections untouched.

**Overwrite behavior:** The skill's assessment supersedes any requester pre-checks. Replace the entire checkbox set for Impacted Parties and FinOps Scope rather than attempting a partial merge.

---

## EDGE CASES

- **`/assess-fr-impact` not yet run**: Ambiguity assessment proceeds with lower confidence. Note this in the rationale.
- **Requester pre-checked Impacted Parties or FinOps Scope**: Assess independently. Flag discrepancies in the presentation. Overwrite with skill's assessment on apply.
- **FR uses legacy template** (no `## Maintainer Assessment`): Detect and report. Offer to append the Maintainer Assessment structure.
- **Multiple issue numbers**: Process sequentially. Present classification for each before moving to the next.
- **Tech Debt / Enablement FRs**: Ambiguity is often low (1-2). FinOps Scope may not apply (none checked is valid). Impacted Parties may be limited to spec authors or data generators.
- **FR has no Problem Statement or Use Case**: Flag the gap. Classify based on available fields. Note reduced confidence.
- **Ambiguity is genuinely a 5**: This is fine. A rating of 5 signals that the FR needs significant discovery work before implementation. Don't deflate the rating to be polite.

---

## USAGE

Invoke this skill by:
- `/classify-fr 1997`
- `/classify-fr 2018 --guidance "AI working group has discussed this extensively"`
- "Classify FR #1997"
- "Classify issues 1997, 2018, and 1943"
