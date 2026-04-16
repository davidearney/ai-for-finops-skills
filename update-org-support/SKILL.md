---
name: update-org-support
description: Fetch org support counts from GitHub and update the Prioritization Framework sheet
---

# Update Org Support Data

Fetch fresh organizational support counts from GitHub feature request issues and update the Org Support tab in the Prioritization Framework Google Sheet.

## ROLE

Act as an automation assistant that runs the update script, presents the diff for review, and optionally promotes validated data to the live columns.

## PREREQUISITES

- `gh` CLI installed and authenticated with `repo` scope
- Python packages: `gspread`, `google-auth` (`pip install gspread google-auth`)
- Service account key at `~/.config/gcloud/gh-fr-updates-sa-key.json`
- Google Sheet shared with `sheets-updater@gh-fr-updates.iam.gserviceaccount.com` (Editor)

## PROCESS

### Step 1: Fetch and Update Validation Columns

Run the script from the repo root:

```bash
python3 scripts/update-org-support.py
```

This fetches all issues with the `feature` label (open and closed) from `FinOps-Open-Cost-and-Usage-Spec/FOCUS_Spec`, parses org support sections, writes fresh data to validation columns E:G, and outputs a diff against current live data.

### Step 2: Present the Diff

Relay the script's diff output to the user. The diff has three sections:

- **Org count changes**: Issues where the count went up or down since the last update
- **New issues not in sheet**: Feature requests on GitHub that aren't in the live data yet
- **Missing 'feature' label**: Issues in the sheet whose GitHub issue no longer has the `feature` label

If there are new issues not in the sheet, note that promoting will NOT add them to the live data automatically. The promote step only overwrites existing live data with validation data. To add new issues to the Framework, use `--add-to-framework` (see below).

### Step 3: Promote to Live (Optional)

After the user reviews the diff, ask:

> Validation columns updated. Want me to promote this to the live data?

If yes, run:

```bash
python3 scripts/update-org-support.py --promote
```

This reads the validation columns (E:G) and copies them to the live columns (A:C) with the column reorder (E:G = Issue/Title/Count, A:C = Issue/Count/Title). VLOOKUPs on the Prioritization Framework tab will pick up the new values automatically.

### Step 4: Add Issues to Prioritization Framework (On Demand)

To see which issues exist in Org Support but aren't in the Framework:

```bash
python3 scripts/update-org-support.py --show-candidates
```

To add specific issues to the Framework tab:

```bash
python3 scripts/update-org-support.py --add-to-framework 1943 2012 2045
```

This appends rows at the bottom of the Prioritization Framework tab with all 14 formula columns pre-filled. Manual columns (expected version, TAM, adoption blocker, SCO, maintainer advocacy) are left blank. Rows will remain unranked until those scoring inputs are provided.

This is pull-based by design: the script never suggests issues to add. The user decides which issues belong in the framework.

## FLAGS

| Flag | Behavior |
|------|----------|
| (none) | Fetch from GitHub, write validation columns E:G, show diff |
| `--promote` | Copy validation E:G to live A:C (no GitHub fetch) |
| `--dry-run` | Fetch and show diff only, no sheet writes |
| `--show-candidates` | List issues in Org Support but not in Framework (read-only) |
| `--add-to-framework N [N...]` | Append specified issues to Framework tab with formulas |

## ERROR HANDLING

- If `gh` auth fails: instruct user to run `gh auth login`
- If service account key missing: check `~/.config/gcloud/gh-fr-updates-sa-key.json`
- If sheet access fails: verify sheet is shared with the service account email
- If zero issues returned: warn that the `feature` label filter may have changed

## USAGE

User can invoke this skill by:
- `/update-org-support`
- "Update the org support counts"
- "Refresh the prioritization framework org data"
- "Pull fresh org support from GitHub"
- "Show me candidate issues for the framework"
- "Add issue 1943 to the prioritization framework"
