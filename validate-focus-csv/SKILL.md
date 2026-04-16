---
name: validate-focus-csv
description: Validate FOCUS CSV example files for arithmetic, nullability, cross-row, and semantic correctness. Runs the FOCUS validator and a deterministic Python gap-check script. Use when reviewing PRs with CSV data files, validating generated examples, or checking existing spec CSVs for compliance. Trigger on mentions of "validate CSV", "check the CSV", "run validation", or when CSV files appear in a FOCUS_Spec PR being reviewed.
---

# Validate FOCUS CSV

Validate FOCUS-compliant CSV example files using two layers: the FOCUS validator (200+ spec rules via DuckDB SQL) and a deterministic Python gap-check script that catches arithmetic, nullability, and cross-referencing errors the validator does not cover.

## ROLE

Act as a FOCUS specification QA engineer. Run deterministic validation checks that catch errors LLM-based review misses. Report findings with exact row numbers, column names, expected values, and actual values.

## INPUTS

Two modes:

- **Standalone mode**: one or more CSV file paths, or a directory path
- **PR mode**: a PR number on `FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec`

Optional:
- **FOCUS version** (default: 1.2): which spec version to validate against
- **Companion markdown** (auto-detected): markdown files with Row Summary tables to cross-reference

## CONSTANTS

```
Repository: FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec
Script: /Users/matthewcowsert/claude-code-config/skills/validate-focus-csv/validate_focus_csv.py
Spec Repo: /Users/matthewcowsert/Documents/Manual Library/GitHub/FOCUS_Spec
```

---

## PROCESS

### Phase 1: Identify Targets

**Standalone mode:**
- Resolve file paths. If a directory, glob for `*.csv`.
- For each CSV, look for a companion markdown with the same stem:
  1. Same directory: `{stem}.md`
  2. Parent directory: `../{stem}.md`
  3. If CSV is under `specification/data/`, check `specification/appendix/` subdirectories

**PR mode:**
1. Fetch changed files: `gh api repos/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/pulls/{n}/files --paginate --jq '.[].filename'`
2. Filter for `.csv` files
3. Get the PR HEAD SHA: `gh api repos/.../pulls/{n} --jq '.head.sha'`
4. For each CSV, fetch content at HEAD:
```bash
gh api "repos/FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec/contents/{path}?ref={sha}" --jq '.content' | base64 -d > /tmp/{filename}
```
5. Also fetch companion `.md` files (same stem, in the appendix directory)

### Phase 2: Run FOCUS Validator

For each CSV, invoke the FOCUS validator:

```bash
cd $(python3 -c "import focus_validator; import os; print(os.path.dirname(os.path.dirname(focus_validator.__file__)))") && \
focus-validator \
  --data-file {csv_path} \
  --validate-version {version} \
  --output-type console \
  --applicability-criteria ALL \
  --show-violations 2>&1
```

**Filter results:**
- Remove missing-column cascades: lines containing "missing column", "required column not present", "Upstream dependency failed"
- Flag the known false positive: CommitmentDiscountStatus "MUST NOT be NULL" on Purchase rows where CommitmentDiscountId is populated (spec only requires non-null when ChargeCategory = "Usage")
- Report remaining real failures

**If the validator is not installed:** skip Phase 2, note it in the output, and proceed with Phase 3 only.

### Phase 3: Run Gap-Check Script

```bash
python3 /Users/matthewcowsert/claude-code-config/skills/validate-focus-csv/validate_focus_csv.py \
  --csv {csv_path} [--markdown {md_path}]
```

Or for a directory:
```bash
python3 /Users/matthewcowsert/claude-code-config/skills/validate-focus-csv/validate_focus_csv.py \
  --directory {dir_path}
```

The script outputs JSON with findings grouped by tier:
- **Tier 1 (Arithmetic)**: pricing equation checks, markdown total cross-references
- **Tier 2 (Nullability)**: spec-required non-null fields
- **Tier 3 (Cross-row)**: amortization balance, purchase/usage cost relationships
- **Tier 4 (Semantic)**: charge period alignment, cross-file column consistency

### Phase 4: Present Results

For each file, show:

1. **FOCUS validator**: pass count, fail count (excluding filtered cascades), sample violations
2. **Gap-check findings**: grouped by tier, each with:
   - Check name and severity (error/warning/info)
   - Row number (if applicable)
   - Affected columns
   - Expected vs actual values

If all checks pass across both layers, report clean.

### Phase 5: Recommendations

**Standalone mode:** summarize findings and offer to explain fixes.

**PR mode:** draft review feedback using the review-pr framework:
- Tier 1/2 failures (arithmetic errors, nullability violations): draft as **Suggestions** with spec citations
- Tier 3/4 findings (cross-row warnings, semantic issues): draft as **Comments**
- Include spec column definition references for nullability violations
- Present drafted feedback for approval before posting

---

## ERROR HANDLING

| Failure | Detection | Recovery |
|---|---|---|
| FOCUS validator not installed | `which focus-validator` fails | Skip Phase 2, note in output, run Phase 3 only |
| CSV has no header row | `csv.DictReader` returns no fieldnames | Report error, skip file |
| Companion markdown not found | `.md` file doesn't exist at expected paths | Skip markdown cross-reference checks |
| CSV uses dollar-formatted values | Values like `"$10,000.00 "` | Parser strips `$`, commas, quotes, spaces |
| CSV uses empty string for null | `,,` in data | Parser normalizes to None |

---

## USAGE

```
/validate-focus-csv /path/to/file.csv
/validate-focus-csv /path/to/directory/
/validate-focus-csv --pr 1877
/validate-focus-csv --pr 1877 --version 1.3
```
