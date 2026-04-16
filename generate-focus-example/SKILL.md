---
name: generate-focus-example
description: Generate FOCUS specification examples with CSV data and markdown narrative, validated against spec rules
---

# Generate FOCUS Specification Example

Generate a FOCUS-compliant CSV data file and companion markdown narrative for a given billing scenario. Validate the output against the specification's column definitions, mathematical relationships, and the FOCUS validator.

## ROLE

Act as a FOCUS specification data engineer. Produce examples that are mathematically rigorous, spec-compliant, and formatted to match existing repo conventions. Every value must be traceable to a spec rule or an explicit assumption.

Follow the communication style in CLAUDE.md: confident, clear, short sentences. No em dashes. Cite spec files and line numbers for rule references.

## INPUTS

The user provides one or more of:

- **Scenario description** (required): verbal description, spreadsheet, or file path describing the billing scenario
- **CSV format** (optional): "full" (all ~48 columns, alphabetical, dollar-formatted) or "relevant" (scenario-relevant columns, logically grouped, plain decimals). Default: "relevant"
- **Target directory** (optional): where to place the CSV and markdown. Default: infer from scenario type

If the scenario is ambiguous, ask clarifying questions before proceeding. Don't guess at pricing, quantities, or commitment terms.

## CONSTANTS

```
Repository: /Users/matthewcowsert/Documents/Manual Library/GitHub/FOCUS_Spec
Spec columns: specification/datasets/cost_and_usage/columns/
Appendix examples: specification/appendix/
Data files: specification/data/
Requirements model: specification/requirements_model/
Editorial guidelines: guidelines/editorial-guidelines.md
```

---

## PROCESS

Run six phases sequentially. Present results after Phase 3 (data table) and Phase 6 (final output) for review. Do not write files until the user approves.

---

### Phase 1: Parse Scenario

Extract from the source material:

1. **Services and SKUs**: service names, SKU IDs, SKU price IDs, pricing units
2. **Commitment terms**: quantity, unit, frequency (one-time, recurring), contracted vs. list pricing
3. **Usage patterns**: consumed quantities, charge periods, utilization levels
4. **Accounts and resources**: billing account IDs, resource IDs, commitment discount IDs

**Rules for this phase:**

- Discard non-FOCUS columns from source data (e.g., provider-specific fields)
- If the source lacks purchase rows, flag this and synthesize them from commitment terms
- If the source lacks list or contracted unit prices, ask the user or derive from available cost/quantity data
- Map source column names to FOCUS column IDs using the spec definitions
- Use placeholder IDs following existing conventions: `<cd-*>` for commitment discount IDs, `<my-*-resource>` for resource IDs
- Use string-like values for BillingAccountId (e.g., `account-1`, not `1`) to avoid type inference issues

Present: a structured summary of extracted data with assumptions called out.

---

### Phase 2: Read Spec Context

Read the column definition files for every column that will appear in the output. For each column, extract:

1. **Data type** and format constraints
2. **Nullability rules** (conditional on ChargeCategory, ChargeClass, CommitmentDiscountStatus, SkuPriceId, etc.)
3. **Allowed values** (if enumerated)
4. **Mathematical relationships** (e.g., ListCost = ListUnitPrice x PricingQuantity)
5. **Cross-column dependencies** (e.g., CommitmentDiscountStatus depends on CommitmentDiscountId and ChargeCategory)

**BilledCost and EffectiveCost definitions (per PR #1678, merged Jan 2026):**

- **BilledCost** ([*cash-based*](#glossary:cash-based-accounting)): Cost of a charge as invoiced by the invoice issuer in a given billing period. Reflects all pricing adjustments (negotiated/commitment discounts). For usage charges, excludes any portion covered by related purchase charges. For purchase charges, includes any portion invoiced in the given billing period.
- **EffectiveCost** ([*accrual-based*](#glossary:accrual-based-accounting)): Cost of a charge based on resources used, services used, or contract commitments recognized in a given charge period. Reflects all pricing adjustments. For usage charges, includes the recognized portion of BilledCost from related purchases (e.g., amortized prepayments, drawdowns). For purchase charges, excludes amounts recognized in related usage charges.
- BilledCost and EffectiveCost differ when charges are invoiced separately from usage (e.g., commitment discounts, marketplace purchases). They align when no related purchase exists.

**Key column rules (encoded from spec):**

Cost relationships (when both operands are non-null):
- `ListCost = ListUnitPrice x PricingQuantity`
- `ContractedCost = ContractedUnitPrice x PricingQuantity`

Commitment discount purchase rows:
- `ChargeCategory = "Purchase"`
- `PricingCategory = "Standard"`
- `ResourceId = CommitmentDiscountId` (the CD is the resource being purchased)
- `BilledCost > 0` (invoiced amount for the purchase)
- `EffectiveCost = 0` (purchase covers future charges; cost recognized when usage occurs)
- `CommitmentDiscountStatus` is null (only required when ChargeCategory = "Usage")
- `ConsumedQuantity` and `ConsumedUnit` are null (ChargeCategory is not "Usage")
- `CommitmentDiscountCategory` MUST NOT be null when CommitmentDiscountId is not null

Commitment discount usage rows (Used):
- `ChargeCategory = "Usage"`, `PricingCategory = "Committed"`
- `BilledCost = 0` (usage covered by purchase; no additional invoiced amount)
- `EffectiveCost = ContractedCost` (accrual-basis: recognized portion of the commitment)
- `CommitmentDiscountStatus = "Used"`
- `ResourceId` = the actual resource consuming the commitment

Commitment discount usage rows (Unused):
- `ChargeCategory = "Usage"`, `PricingCategory = "Committed"`
- `BilledCost = 0` (usage covered by purchase; no additional invoiced amount)
- `EffectiveCost = ContractedCost` (accrual-basis: recognized portion of unused commitment)
- `CommitmentDiscountStatus = "Unused"`
- `ResourceId = CommitmentDiscountId` (unused capacity belongs to the CD itself)
- `ConsumedQuantity` and `ConsumedUnit` are null

On-demand overage rows:
- `ChargeCategory = "Usage"`, `PricingCategory = "Standard"`
- `BilledCost = EffectiveCost` (no related purchase; cash and accrual basis align)
- `CommitmentDiscountId`, `CommitmentDiscountCategory`, `CommitmentDiscountQuantity`, `CommitmentDiscountStatus`, `CommitmentDiscountUnit` are all null
- `ContractedUnitPrice = ListUnitPrice` (no negotiated discount on overage)

FOCUS Unit Format (from `specification/attributes/unit_format.md`):
- Count-based units MUST be capitalized: `Hosts`, `Tokens`, `Requests` (not `hosts`)
- Compound units use `Singular-Plural` format: `Host-Hours`, `GB-Hours` (not `host-hours`)
- Time units: `Year`, `Month`, `Day`, `Hour`, `Minute`, `Second`
- Rate units use slash: `GB/Hour`, `Requests/Second`

---

### Phase 3: Compute Data

Generate each row with full mathematical derivations.

**Rules for this phase:**

- Always use explicit decimal format for numeric columns (e.g., `0.0` not `0`, `37500.0` not `37500`). This prevents type inference issues in downstream tools.
- Empty cells represent null. Use `,,` in CSV (no literal "null" string).
- For each Used/Unused pair in a charge period, the sum of their CommitmentDiscountQuantity must equal the commitment's total quantity for that period.
- For each commitment discount, `sum(EffectiveCost) across all Usage rows` must equal `sum(BilledCost) across all Purchase rows` over the billing period.

Present: a numbered data table with all rows and columns, plus the mathematical derivation for each non-obvious value.

---

### Phase 4a: Self-Validate

Run these checks against every row:

**Per-row checks:**

| Check | Rule |
|---|---|
| Cost math | `ListCost == ListUnitPrice * PricingQuantity` (when both non-null) |
| Cost math | `ContractedCost == ContractedUnitPrice * PricingQuantity` (when both non-null) |
| Purchase EffectiveCost | `EffectiveCost == 0` when ChargeCategory = "Purchase" and BilledCost > 0 |
| Nullability: ConsumedQuantity | Null when ChargeCategory != "Usage" OR CommitmentDiscountStatus = "Unused" |
| Nullability: ConsumedUnit | Null when ConsumedQuantity is null; non-null when ConsumedQuantity is non-null |
| Nullability: CommitmentDiscountStatus | Null when CommitmentDiscountId is null; non-null when CDId is not null AND ChargeCategory = "Usage" |
| Nullability: CommitmentDiscountCategory | Null when CommitmentDiscountId is null; non-null when CDId is not null |
| Nullability: CommitmentDiscountUnit | Null when CommitmentDiscountQuantity is null |
| Allowed values: ChargeCategory | One of: Usage, Purchase, Tax, Credit, Adjustment |
| Allowed values: PricingCategory | One of: Standard, Dynamic, Committed, Other |
| Allowed values: CommitmentDiscountStatus | One of: Used, Unused |
| Allowed values: CommitmentDiscountCategory | One of: Spend, Usage |
| Unit format | All unit columns conform to FOCUS Unit Format (capitalized, correct compound format) |
| Purchase ResourceId | ResourceId == CommitmentDiscountId on Purchase rows for commitment discounts |

**Cross-row checks:**

| Check | Rule |
|---|---|
| CD balance | For each CD + charge period: sum(CDQuantity where Used) + sum(CDQuantity where Unused) == Purchase CDQuantity for that period |
| Amortization | For each CD over the billing period: sum(EffectiveCost where Usage) == sum(BilledCost where Purchase) |
| Overage isolation | Overage rows have no CommitmentDiscountId and PricingCategory = "Standard" |

Report: pass/fail for each check with the specific values tested. If any check fails, fix the data before proceeding.

---

### Phase 4b: FOCUS Validator

Write the CSV to a temp file and run the FOCUS validator.

**Invocation (workaround for relative path bug in v2.0.1):**

```bash
cd $(python3 -c "import focus_validator; import os; print(os.path.dirname(os.path.dirname(focus_validator.__file__)))") && \
focus-validator \
  --data-file <csv-path> \
  --validate-version 1.2 \
  --output-type console \
  --applicability-criteria ALL \
  --show-violations
```

**Interpreting results:**

- **Missing column cascades**: For "relevant" format CSVs, the majority of failures will be missing-column cascades. These are expected and should be ignored. Filter with: `grep "^❌" | grep -v "missing column" | grep -v "required column not present" | grep -v "Upstream dependency failed"`
- **Type inference issues**: If columns like BilledCost show "MUST be of type DECIMAL" failures, ensure all decimal values have explicit `.0` suffixes. If BillingAccountId shows "MUST be of type VARCHAR", ensure IDs are string-like (not bare integers).
- **Unit format violations**: Check against FOCUS Unit Format rules in Phase 2.
- **CommitmentDiscountStatus on Purchase rows**: The validator may flag "MUST NOT be NULL" for CDStatus on Purchase rows where CDId is populated. This is a known false positive; the spec only requires non-null when ChargeCategory = "Usage".
- **Generic "Validation rule X failed"**: These often depend on missing columns (especially ChargeClass) for conditional evaluation. If the column they reference is present and the data looks correct per the spec, these are likely false positives from incomplete conditional context.

Report: count of total/pass/fail/skipped, count of failures attributable to missing columns, and any remaining failures that indicate real data issues.

---

### Phase 5: Generate Markdown

Write a companion markdown narrative following existing repo conventions.

**Structure** (matches `specification/appendix/commitment_discounts/commitment_discounts.md` pattern):

```
# <Example Title>

## Context
<Brief description of the provider, services, and pricing model>
<SKU catalog table if multiple SKUs are involved>

## Scenario <A/B/C/...>: <Short description>
<Bullet list of commitment terms, charge periods, and usage patterns>

### Outcome
<Bullet list of resulting rows, costs, and key observations>

## Scenario <next>...

[CSV Example](/specification/data/<path>/<filename>.csv)
```

**Editorial rules** (from `guidelines/editorial-guidelines.md`):

- Use `&dollar;` for dollar signs in markdown (not `$`)
- Link glossary terms on first use: `[*commitment discount*](#glossary:commitment-discount)`
- Link column names on first use: `[BilledCost](#datasets.costandusage.billedcost)`
- Column names in PascalCase, italicize glossary terms
- Show derivation formulas in backtick-wrapped expressions: `` `24 hours * 365 days * &dollar;1.00` ``
- Short sentences, no em dashes
- When describing BilledCost, frame as the invoiced amount (cash-basis). When describing EffectiveCost, frame as the recognized cost at time of usage (accrual-basis). Use glossary links on first use: `[*cash-based*](#glossary:cash-based-accounting)` and `[*accrual-based*](#glossary:accrual-based-accounting)`

---

### Phase 6: Present for Review

Present both outputs in code blocks:

1. **CSV** in a ```csv code block
2. **Markdown** in a ```markdown code block
3. **Validation summary**: self-validation results + validator results

Do NOT write files to the repo or commit until the user explicitly approves. Once approved:

- Write the CSV to the appropriate `specification/data/` subdirectory
- Write the markdown to the appropriate `specification/appendix/` subdirectory
- Follow existing naming conventions in the target directory (lowercase, underscores, descriptive)

---

## FORMAT MODES

### Relevant (default)

- Include only columns that are meaningful for the scenario
- Group columns logically (temporal, categorical, identification, quantity, cost, commitment discount)
- Use plain decimal values with explicit `.0` suffix
- Use `,,` for null (empty cell)
- Use placeholder IDs: `<cd-service-name>`, `<my-service-resource>`, `account-N`

### Full

- Include all ~48 FOCUS columns, sorted alphabetically by Column ID
- Use dollar-formatted values with trailing space for cost columns: `"$10,000.00 "`
- Use realistic placeholder names (e.g., company names like those in `specification/data/saas_examples/`)
- Wrap values containing commas or dollar signs in double quotes
