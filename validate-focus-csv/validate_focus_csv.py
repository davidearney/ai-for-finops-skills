#!/usr/bin/env python3
"""Deterministic gap-check validator for FOCUS CSV example files.

Checks arithmetic, nullability, cross-row, and semantic rules that the
FOCUS validator does not cover. Outputs structured JSON.

Dependencies: stdlib only (csv, json, decimal, re, argparse, datetime, pathlib).
"""

import argparse
import csv
import json
import re
import sys
from datetime import datetime, timedelta
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from pathlib import Path


__version__ = "1.0.0"

DEFAULT_TOLERANCE = Decimal("0.015")


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def _normalize_null(value):
    """Return None for null-like values, stripped string otherwise."""
    if value is None:
        return None
    v = value.strip()
    if v == "" or v.lower() == "null":
        return None
    return v


def parse_decimal(value):
    """Parse a string to Decimal. Returns None for null/empty.

    Strips leading '$', '&dollar;', trailing spaces, commas, and bold markers.
    """
    v = _normalize_null(value)
    if v is None:
        return None
    # Strip markdown bold, HTML entities, dollar signs, commas
    v = v.replace("**", "").replace("&dollar;", "").replace("$", "")
    v = v.replace(",", "").strip()
    if v == "" or v.lower() == "null":
        return None
    try:
        return Decimal(v)
    except InvalidOperation:
        return None


def parse_datetime(value):
    """Parse ISO 8601 datetime string. Returns None for null/empty."""
    v = _normalize_null(value)
    if v is None:
        return None
    try:
        return datetime.fromisoformat(v.replace("Z", "+00:00"))
    except (ValueError, TypeError):
        return None


def load_csv(path):
    """Load a CSV file, return (headers, rows_as_dicts).

    Empty cells become None. Preserves original string values;
    numeric parsing happens in individual check functions.
    """
    with open(path, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = list(reader.fieldnames or [])
        rows = []
        for row in reader:
            normalized = {}
            for k, v in row.items():
                normalized[k] = _normalize_null(v)
            rows.append(normalized)
    return headers, rows


def _has_columns(headers, *cols):
    """Check if all columns exist in headers."""
    return all(c in headers for c in cols)


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

def load_markdown(path):
    """Parse companion markdown for Row Summary table.

    Returns dict with 'row_summary' list and 'found' bool.
    Each entry: {'row_type': str, 'count': int,
                 'billed_cost': Decimal, 'effective_cost': Decimal}
    """
    result = {"row_summary": [], "found": False}
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return result

    lines = text.split("\n")
    return _parse_row_summary(lines, result)


def _parse_row_summary(lines, result):
    """Find and parse the Row Summary table in markdown lines."""
    # Find the Row Summary heading or table header with Row Type
    table_start = None
    for i, line in enumerate(lines):
        if re.match(r"^#{1,4}\s+Row\s+Summary", line, re.IGNORECASE):
            # Find the table after this heading
            for j in range(i + 1, min(i + 10, len(lines))):
                if "|" in lines[j] and "Row" in lines[j]:
                    table_start = j
                    break
            if table_start:
                break
        # Also match if the table header itself contains "Row Type"
        if re.search(r"\|\s*Row\s+Type\s*\|", line, re.IGNORECASE):
            table_start = i
            break

    if table_start is None:
        return result

    # Parse the header row to find column positions
    header_line = lines[table_start]
    header_cells = [c.strip() for c in header_line.split("|")]
    header_cells = [c for c in header_cells if c]  # remove empty from leading/trailing |

    # Map column names to indices
    col_map = {}
    for idx, cell in enumerate(header_cells):
        cell_lower = cell.lower().replace("**", "").strip()
        if "row" in cell_lower and "type" in cell_lower:
            col_map["row_type"] = idx
        elif "count" in cell_lower:
            col_map["count"] = idx
        elif "billed" in cell_lower:
            col_map["billed_cost"] = idx
        elif "effective" in cell_lower:
            col_map["effective_cost"] = idx

    if "row_type" not in col_map:
        return result

    # Skip separator row (---) and parse data rows
    data_start = table_start + 1
    if data_start < len(lines) and re.match(r"^\s*\|[\s\-:|]+\|", lines[data_start]):
        data_start += 1

    for i in range(data_start, len(lines)):
        line = lines[i].strip()
        if not line or not line.startswith("|"):
            break
        cells = [c.strip() for c in line.split("|")]
        cells = [c for c in cells if c != ""]

        if len(cells) < len(col_map):
            continue

        entry = {}
        if "row_type" in col_map and col_map["row_type"] < len(cells):
            rt = cells[col_map["row_type"]].replace("**", "").strip()
            entry["row_type"] = rt
        if "count" in col_map and col_map["count"] < len(cells):
            count_str = cells[col_map["count"]].replace("**", "").strip()
            try:
                entry["count"] = int(count_str)
            except ValueError:
                entry["count"] = None
        if "billed_cost" in col_map and col_map["billed_cost"] < len(cells):
            entry["billed_cost"] = parse_decimal(cells[col_map["billed_cost"]])
        if "effective_cost" in col_map and col_map["effective_cost"] < len(cells):
            entry["effective_cost"] = parse_decimal(cells[col_map["effective_cost"]])

        if entry.get("row_type"):
            result["row_summary"].append(entry)

    result["found"] = len(result["row_summary"]) > 0
    return result


# ---------------------------------------------------------------------------
# Tier 1: Arithmetic checks
# ---------------------------------------------------------------------------

def check_list_cost_product(row, row_num, headers, tolerance):
    """ListCost == ListUnitPrice * PricingQuantity (when both non-null)."""
    if not _has_columns(headers, "ListCost", "ListUnitPrice", "PricingQuantity"):
        return None
    lc = parse_decimal(row.get("ListCost"))
    lup = parse_decimal(row.get("ListUnitPrice"))
    pq = parse_decimal(row.get("PricingQuantity"))
    if lc is None or lup is None or pq is None:
        return None
    expected = lup * pq
    if abs(lc - expected) > tolerance:
        return {
            "tier": "arithmetic", "check": "list_cost_product",
            "severity": "error", "row": row_num,
            "message": "ListCost != ListUnitPrice * PricingQuantity",
            "expected": str(expected), "actual": str(lc),
            "columns": ["ListCost", "ListUnitPrice", "PricingQuantity"],
        }
    return None


def check_contracted_cost_product(row, row_num, headers, tolerance):
    """ContractedCost == ContractedUnitPrice * PricingQuantity."""
    if not _has_columns(headers, "ContractedCost", "ContractedUnitPrice", "PricingQuantity"):
        return None
    cc = parse_decimal(row.get("ContractedCost"))
    cup = parse_decimal(row.get("ContractedUnitPrice"))
    pq = parse_decimal(row.get("PricingQuantity"))
    if cc is None or cup is None or pq is None:
        return None
    expected = cup * pq
    if abs(cc - expected) > tolerance:
        return {
            "tier": "arithmetic", "check": "contracted_cost_product",
            "severity": "error", "row": row_num,
            "message": "ContractedCost != ContractedUnitPrice * PricingQuantity",
            "expected": str(expected), "actual": str(cc),
            "columns": ["ContractedCost", "ContractedUnitPrice", "PricingQuantity"],
        }
    return None


def check_md_billed_cost_total(rows, headers, md_summary, csv_name):
    """Markdown Total BilledCost == sum of CSV BilledCost."""
    if not md_summary.get("found") or not _has_columns(headers, "BilledCost"):
        return None
    total_entry = None
    for entry in md_summary["row_summary"]:
        if entry.get("row_type", "").lower().startswith("total"):
            total_entry = entry
            break
    if total_entry is None or total_entry.get("billed_cost") is None:
        return None

    csv_sum = Decimal("0")
    for row in rows:
        bc = parse_decimal(row.get("BilledCost"))
        if bc is not None:
            csv_sum += bc

    md_total = total_entry["billed_cost"]
    if abs(csv_sum - md_total) > DEFAULT_TOLERANCE:
        return {
            "tier": "arithmetic", "check": "md_billed_cost_total",
            "severity": "error", "row": None,
            "message": f"Markdown Total BilledCost ({md_total}) != sum of CSV BilledCost ({csv_sum})",
            "expected": str(csv_sum), "actual": str(md_total),
            "columns": ["BilledCost"],
        }
    return None


def check_md_effective_cost_total(rows, headers, md_summary, csv_name):
    """Markdown Total EffectiveCost == sum of CSV EffectiveCost."""
    if not md_summary.get("found") or not _has_columns(headers, "EffectiveCost"):
        return None
    total_entry = None
    for entry in md_summary["row_summary"]:
        if entry.get("row_type", "").lower().startswith("total"):
            total_entry = entry
            break
    if total_entry is None or total_entry.get("effective_cost") is None:
        return None

    csv_sum = Decimal("0")
    for row in rows:
        ec = parse_decimal(row.get("EffectiveCost"))
        if ec is not None:
            csv_sum += ec

    md_total = total_entry["effective_cost"]
    if abs(csv_sum - md_total) > DEFAULT_TOLERANCE:
        return {
            "tier": "arithmetic", "check": "md_effective_cost_total",
            "severity": "error", "row": None,
            "message": f"Markdown Total EffectiveCost ({md_total}) != sum of CSV EffectiveCost ({csv_sum})",
            "expected": str(csv_sum), "actual": str(md_total),
            "columns": ["EffectiveCost"],
        }
    return None


def check_md_row_count(rows, headers, md_summary, csv_name):
    """Markdown Total row count == number of CSV data rows."""
    if not md_summary.get("found"):
        return None
    total_entry = None
    for entry in md_summary["row_summary"]:
        if entry.get("row_type", "").lower().startswith("total"):
            total_entry = entry
            break
    if total_entry is None or total_entry.get("count") is None:
        return None

    csv_count = len(rows)
    md_count = total_entry["count"]
    if csv_count != md_count:
        return {
            "tier": "arithmetic", "check": "md_row_count",
            "severity": "error", "row": None,
            "message": f"Markdown Total row count ({md_count}) != CSV row count ({csv_count})",
            "expected": str(csv_count), "actual": str(md_count),
            "columns": [],
        }
    return None


# ---------------------------------------------------------------------------
# Tier 2: Nullability checks
# ---------------------------------------------------------------------------

def _is_usage_or_purchase(row):
    cc = (row.get("ChargeCategory") or "").strip()
    return cc in ("Usage", "Purchase")


def _is_not_correction(row):
    charge_class = (row.get("ChargeClass") or "").strip()
    return charge_class != "Correction"


def check_cd_quantity_not_null(row, row_num, headers):
    """CommitmentDiscountQuantity MUST NOT be null when ChargeCategory in
    (Usage, Purchase) AND CommitmentDiscountId not null AND ChargeClass != Correction.
    """
    if not _has_columns(headers, "CommitmentDiscountQuantity", "ChargeCategory", "CommitmentDiscountId"):
        return None
    if not _is_usage_or_purchase(row):
        return None
    if _normalize_null(row.get("CommitmentDiscountId")) is None:
        return None
    if not _is_not_correction(row):
        return None
    if _normalize_null(row.get("CommitmentDiscountQuantity")) is None:
        return {
            "tier": "nullability", "check": "cd_quantity_not_null",
            "severity": "error", "row": row_num,
            "message": "CommitmentDiscountQuantity is null but MUST NOT be null (ChargeCategory is Usage/Purchase, CommitmentDiscountId is not null)",
            "expected": "non-null", "actual": "null",
            "columns": ["CommitmentDiscountQuantity"],
        }
    return None


def check_sku_price_id_not_null(row, row_num, headers):
    """SkuPriceId MUST NOT be null when ChargeCategory in (Usage, Purchase)
    AND ChargeClass != Correction.
    """
    if not _has_columns(headers, "SkuPriceId", "ChargeCategory"):
        return None
    if not _is_usage_or_purchase(row):
        return None
    if not _is_not_correction(row):
        return None
    if _normalize_null(row.get("SkuPriceId")) is None:
        return {
            "tier": "nullability", "check": "sku_price_id_not_null",
            "severity": "error", "row": row_num,
            "message": "SkuPriceId is null but MUST NOT be null (ChargeCategory is Usage/Purchase)",
            "expected": "non-null", "actual": "null",
            "columns": ["SkuPriceId"],
        }
    return None


def check_list_unit_price_not_null(row, row_num, headers):
    """ListUnitPrice MUST NOT be null when SkuPriceId is not null."""
    if not _has_columns(headers, "ListUnitPrice", "SkuPriceId"):
        return None
    if _normalize_null(row.get("SkuPriceId")) is None:
        return None
    if _normalize_null(row.get("ListUnitPrice")) is None:
        return {
            "tier": "nullability", "check": "list_unit_price_not_null",
            "severity": "error", "row": row_num,
            "message": "ListUnitPrice is null but MUST NOT be null (SkuPriceId is not null)",
            "expected": "non-null", "actual": "null",
            "columns": ["ListUnitPrice"],
        }
    return None


def check_pricing_category_not_null(row, row_num, headers):
    """PricingCategory MUST NOT be null when ChargeCategory in (Usage, Purchase)
    AND ChargeClass != Correction.
    """
    if not _has_columns(headers, "PricingCategory", "ChargeCategory"):
        return None
    if not _is_usage_or_purchase(row):
        return None
    if not _is_not_correction(row):
        return None
    if _normalize_null(row.get("PricingCategory")) is None:
        return {
            "tier": "nullability", "check": "pricing_category_not_null",
            "severity": "error", "row": row_num,
            "message": "PricingCategory is null but MUST NOT be null (ChargeCategory is Usage/Purchase)",
            "expected": "non-null", "actual": "null",
            "columns": ["PricingCategory"],
        }
    return None


def check_cd_status_not_null(row, row_num, headers):
    """CommitmentDiscountStatus MUST NOT be null when CommitmentDiscountId
    is not null AND ChargeCategory == Usage.
    """
    if not _has_columns(headers, "CommitmentDiscountStatus", "CommitmentDiscountId", "ChargeCategory"):
        return None
    if _normalize_null(row.get("CommitmentDiscountId")) is None:
        return None
    if (row.get("ChargeCategory") or "").strip() != "Usage":
        return None
    if _normalize_null(row.get("CommitmentDiscountStatus")) is None:
        return {
            "tier": "nullability", "check": "cd_status_not_null",
            "severity": "error", "row": row_num,
            "message": "CommitmentDiscountStatus is null but MUST NOT be null (CommitmentDiscountId set, ChargeCategory is Usage)",
            "expected": "non-null", "actual": "null",
            "columns": ["CommitmentDiscountStatus"],
        }
    return None


def check_cd_category_not_null(row, row_num, headers):
    """CommitmentDiscountCategory MUST NOT be null when CommitmentDiscountId is not null."""
    if not _has_columns(headers, "CommitmentDiscountCategory", "CommitmentDiscountId"):
        return None
    if _normalize_null(row.get("CommitmentDiscountId")) is None:
        return None
    if _normalize_null(row.get("CommitmentDiscountCategory")) is None:
        return {
            "tier": "nullability", "check": "cd_category_not_null",
            "severity": "error", "row": row_num,
            "message": "CommitmentDiscountCategory is null but MUST NOT be null (CommitmentDiscountId is not null)",
            "expected": "non-null", "actual": "null",
            "columns": ["CommitmentDiscountCategory"],
        }
    return None


# ---------------------------------------------------------------------------
# Tier 3: Cross-row checks
# ---------------------------------------------------------------------------

def check_purchase_effective_cost_zero(row, row_num, headers):
    """Purchase EffectiveCost MUST be 0 when BilledCost > 0."""
    if not _has_columns(headers, "EffectiveCost", "BilledCost", "ChargeCategory"):
        return None
    if (row.get("ChargeCategory") or "").strip() != "Purchase":
        return None
    bc = parse_decimal(row.get("BilledCost"))
    ec = parse_decimal(row.get("EffectiveCost"))
    if bc is None or ec is None:
        return None
    if bc > Decimal("0") and ec != Decimal("0"):
        return {
            "tier": "cross_row", "check": "purchase_effective_cost_zero",
            "severity": "error", "row": row_num,
            "message": f"Purchase row EffectiveCost ({ec}) MUST be 0 when BilledCost ({bc}) > 0",
            "expected": "0", "actual": str(ec),
            "columns": ["EffectiveCost", "BilledCost"],
        }
    return None


def check_used_billed_cost_zero(row, row_num, headers):
    """Used commitment usage row BilledCost MUST be 0."""
    if not _has_columns(headers, "BilledCost", "CommitmentDiscountStatus"):
        return None
    if (row.get("CommitmentDiscountStatus") or "").strip() != "Used":
        return None
    bc = parse_decimal(row.get("BilledCost"))
    if bc is None:
        return None
    if bc != Decimal("0"):
        return {
            "tier": "cross_row", "check": "used_billed_cost_zero",
            "severity": "error", "row": row_num,
            "message": f"Used commitment row BilledCost ({bc}) MUST be 0",
            "expected": "0", "actual": str(bc),
            "columns": ["BilledCost"],
        }
    return None


def check_amortization_balance(rows, headers, tolerance, csv_name):
    """Per CommitmentDiscountId: sum(EffectiveCost on Usage) should relate
    to sum(BilledCost on Purchase) via amortization.

    For single-day snapshots against annual commitments, we verify:
    hourly_effective * 8760 approx == annual purchase BilledCost (for one-time)
    hourly_effective * hours_in_billing_period approx == purchase BilledCost (for recurring)
    """
    if not _has_columns(headers, "EffectiveCost", "BilledCost", "ChargeCategory",
                        "CommitmentDiscountId", "ChargePeriodStart", "ChargePeriodEnd"):
        return []

    findings = []
    # Group by CommitmentDiscountId
    cd_ids = set()
    for row in rows:
        cd_id = _normalize_null(row.get("CommitmentDiscountId"))
        if cd_id:
            cd_ids.add(cd_id)

    for cd_id in cd_ids:
        purchase_total = Decimal("0")
        is_onetime = False
        is_recurring = False
        billing_period_start = None
        billing_period_end = None

        usage_effective_costs = []

        for row in rows:
            if _normalize_null(row.get("CommitmentDiscountId")) != cd_id:
                continue
            cc = (row.get("ChargeCategory") or "").strip()
            if cc == "Purchase":
                bc = parse_decimal(row.get("BilledCost"))
                if bc:
                    purchase_total += bc
                freq = (row.get("ChargeFrequency") or "").strip()
                if freq == "One-Time":
                    is_onetime = True
                elif freq == "Recurring":
                    is_recurring = True
                # Capture billing period from purchase row
                if _has_columns(headers, "BillingPeriodStart", "BillingPeriodEnd"):
                    bp_start = parse_datetime(row.get("BillingPeriodStart"))
                    bp_end = parse_datetime(row.get("BillingPeriodEnd"))
                    if bp_start:
                        billing_period_start = bp_start
                    if bp_end:
                        billing_period_end = bp_end
            elif cc == "Usage":
                ec = parse_decimal(row.get("EffectiveCost"))
                if ec is not None:
                    usage_effective_costs.append(ec)

        if not usage_effective_costs or purchase_total == Decimal("0"):
            continue

        # Count distinct charge period hours in file
        usage_hours = len(usage_effective_costs)
        if usage_hours == 0:
            continue

        # Get hourly effective cost (assume uniform within file)
        hourly_effective = usage_effective_costs[0]
        # Verify uniformity
        non_uniform = any(abs(ec - hourly_effective) > tolerance for ec in usage_effective_costs)

        if is_onetime and not is_recurring:
            # All upfront: hourly * 8760 should approximate annual purchase
            projected_annual = hourly_effective * Decimal("8760")
            # Allow tolerance proportional to the number of hours (rounding accumulates)
            annual_tolerance = tolerance * Decimal("8760")
            if abs(projected_annual - purchase_total) > annual_tolerance:
                findings.append({
                    "tier": "cross_row", "check": "amortization_balance",
                    "severity": "warning", "row": None,
                    "message": (
                        f"CD {cd_id}: hourly EffectiveCost ({hourly_effective}) * 8760 = "
                        f"{projected_annual}, but Purchase BilledCost = {purchase_total} "
                        f"(delta: {projected_annual - purchase_total})"
                    ),
                    "expected": str(purchase_total),
                    "actual": str(projected_annual),
                    "columns": ["EffectiveCost", "BilledCost"],
                })
        elif is_recurring and not is_onetime:
            # No upfront: hourly * hours_in_billing_period = monthly purchase
            if billing_period_start and billing_period_end:
                bp_hours = Decimal(str(int((billing_period_end - billing_period_start).total_seconds() / 3600)))
                projected_monthly = hourly_effective * bp_hours
                monthly_tolerance = tolerance * bp_hours
                if abs(projected_monthly - purchase_total) > monthly_tolerance:
                    findings.append({
                        "tier": "cross_row", "check": "amortization_balance",
                        "severity": "warning", "row": None,
                        "message": (
                            f"CD {cd_id}: hourly EffectiveCost ({hourly_effective}) * {bp_hours} billing hours = "
                            f"{projected_monthly}, but Purchase BilledCost = {purchase_total} "
                            f"(delta: {projected_monthly - purchase_total})"
                        ),
                        "expected": str(purchase_total),
                        "actual": str(projected_monthly),
                        "columns": ["EffectiveCost", "BilledCost"],
                    })
        # Partial upfront has both one-time and recurring; skip amortization check
        # (too complex for a single-file check without knowing the split ratio)

    return findings


def check_cd_quantity_balance(rows, headers, tolerance, csv_name):
    """Per CD + charge period: sum(Used qty) + sum(Unused qty) should be consistent."""
    if not _has_columns(headers, "CommitmentDiscountQuantity", "CommitmentDiscountStatus",
                        "CommitmentDiscountId", "ChargeCategory",
                        "ChargePeriodStart", "ChargePeriodEnd"):
        return []

    findings = []
    # Group by (CD ID, ChargePeriodStart, ChargePeriodEnd)
    periods = {}
    for row in rows:
        cc = (row.get("ChargeCategory") or "").strip()
        if cc != "Usage":
            continue
        cd_id = _normalize_null(row.get("CommitmentDiscountId"))
        if cd_id is None:
            continue
        cp_start = row.get("ChargePeriodStart", "")
        cp_end = row.get("ChargePeriodEnd", "")
        key = (cd_id, cp_start, cp_end)
        status = (row.get("CommitmentDiscountStatus") or "").strip()
        qty = parse_decimal(row.get("CommitmentDiscountQuantity"))
        if qty is None:
            continue
        if key not in periods:
            periods[key] = {"used": Decimal("0"), "unused": Decimal("0"), "total_rows": 0}
        if status == "Used":
            periods[key]["used"] += qty
        elif status == "Unused":
            periods[key]["unused"] += qty
        periods[key]["total_rows"] += 1

    # For each period, check that all periods for the same CD have the same total
    cd_totals = {}
    for (cd_id, cp_start, cp_end), data in periods.items():
        period_total = data["used"] + data["unused"]
        if cd_id not in cd_totals:
            cd_totals[cd_id] = []
        cd_totals[cd_id].append({
            "period": f"{cp_start} to {cp_end}",
            "total": period_total,
            "used": data["used"],
            "unused": data["unused"],
        })

    for cd_id, period_list in cd_totals.items():
        if len(period_list) < 2:
            continue
        first_total = period_list[0]["total"]
        for p in period_list[1:]:
            if abs(p["total"] - first_total) > tolerance:
                findings.append({
                    "tier": "cross_row", "check": "cd_quantity_balance",
                    "severity": "warning", "row": None,
                    "message": (
                        f"CD {cd_id}: inconsistent total CDQuantity across charge periods. "
                        f"Period {period_list[0]['period']} = {first_total}, "
                        f"Period {p['period']} = {p['total']}"
                    ),
                    "expected": str(first_total),
                    "actual": str(p["total"]),
                    "columns": ["CommitmentDiscountQuantity"],
                })

    return findings


# ---------------------------------------------------------------------------
# Tier 4: Semantic checks
# ---------------------------------------------------------------------------

def check_onetime_term_alignment(row, row_num, headers):
    """One-time Purchase: ChargePeriodEnd - ChargePeriodStart >= 364 days."""
    if not _has_columns(headers, "ChargePeriodStart", "ChargePeriodEnd",
                        "ChargeCategory", "ChargeFrequency"):
        return None
    if (row.get("ChargeCategory") or "").strip() != "Purchase":
        return None
    if (row.get("ChargeFrequency") or "").strip() != "One-Time":
        return None

    cp_start = parse_datetime(row.get("ChargePeriodStart"))
    cp_end = parse_datetime(row.get("ChargePeriodEnd"))
    if cp_start is None or cp_end is None:
        return None

    delta = cp_end - cp_start
    if delta.days < 364:
        return {
            "tier": "semantic", "check": "onetime_term_alignment",
            "severity": "error", "row": row_num,
            "message": (
                f"One-Time Purchase ChargePeriod spans {delta.days} days "
                f"({cp_start.date()} to {cp_end.date()}), expected >= 364 days (commitment term)"
            ),
            "expected": ">= 364 days",
            "actual": f"{delta.days} days",
            "columns": ["ChargePeriodStart", "ChargePeriodEnd"],
        }
    return None


def check_recurring_period_alignment(row, row_num, headers):
    """Recurring Purchase: ChargePeriodEnd == BillingPeriodEnd."""
    if not _has_columns(headers, "ChargePeriodEnd", "BillingPeriodEnd",
                        "ChargeCategory", "ChargeFrequency"):
        return None
    if (row.get("ChargeCategory") or "").strip() != "Purchase":
        return None
    if (row.get("ChargeFrequency") or "").strip() != "Recurring":
        return None

    cp_end = _normalize_null(row.get("ChargePeriodEnd"))
    bp_end = _normalize_null(row.get("BillingPeriodEnd"))
    if cp_end is None or bp_end is None:
        return None
    if cp_end != bp_end:
        return {
            "tier": "semantic", "check": "recurring_period_alignment",
            "severity": "warning", "row": row_num,
            "message": f"Recurring Purchase ChargePeriodEnd ({cp_end}) != BillingPeriodEnd ({bp_end})",
            "expected": bp_end,
            "actual": cp_end,
            "columns": ["ChargePeriodEnd", "BillingPeriodEnd"],
        }
    return None


def check_cross_file_columns(file_headers):
    """All CSVs in a directory should share the same column set."""
    if len(file_headers) < 2:
        return []

    findings = []
    # Find majority column set
    header_sets = {name: set(hdrs) for name, hdrs in file_headers.items()}
    all_sets = list(header_sets.values())
    # Use the most common column set as reference
    from collections import Counter
    frozen = [frozenset(s) for s in all_sets]
    most_common = Counter(frozen).most_common(1)[0][0]

    for name, hdr_set in header_sets.items():
        if hdr_set != most_common:
            missing = most_common - hdr_set
            extra = hdr_set - most_common
            parts = []
            if missing:
                parts.append(f"missing: {', '.join(sorted(missing))}")
            if extra:
                parts.append(f"extra: {', '.join(sorted(extra))}")
            findings.append({
                "tier": "semantic", "check": "cross_file_columns",
                "severity": "info", "row": None,
                "message": f"{name} has different columns from majority ({'; '.join(parts)})",
                "expected": f"{len(most_common)} columns",
                "actual": f"{len(hdr_set)} columns",
                "columns": sorted(missing | extra),
            })

    return findings


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def validate_single_csv(csv_path, md_path, tolerance):
    """Run all tier 1-4 checks on a single CSV file."""
    headers, rows = load_csv(csv_path)
    csv_name = csv_path.name
    findings = []

    # Load markdown if available
    md_summary = {"found": False}
    if md_path and md_path.exists():
        md_summary = load_markdown(md_path)

    # Per-row checks
    for i, row in enumerate(rows):
        row_num = i + 2  # 1-indexed, +1 for header row

        # Tier 1
        for check_fn in [check_list_cost_product, check_contracted_cost_product]:
            result = check_fn(row, row_num, headers, tolerance)
            if result:
                result["file"] = csv_name
                findings.append(result)

        # Tier 2
        for check_fn in [check_cd_quantity_not_null, check_sku_price_id_not_null,
                         check_list_unit_price_not_null, check_pricing_category_not_null,
                         check_cd_status_not_null, check_cd_category_not_null]:
            result = check_fn(row, row_num, headers)
            if result:
                result["file"] = csv_name
                findings.append(result)

        # Tier 3 (per-row)
        for check_fn in [check_purchase_effective_cost_zero, check_used_billed_cost_zero]:
            result = check_fn(row, row_num, headers)
            if result:
                result["file"] = csv_name
                findings.append(result)

        # Tier 4 (per-row)
        for check_fn in [check_onetime_term_alignment, check_recurring_period_alignment]:
            result = check_fn(row, row_num, headers)
            if result:
                result["file"] = csv_name
                findings.append(result)

    # Cross-row checks (Tier 3)
    for result in check_amortization_balance(rows, headers, tolerance, csv_name):
        result["file"] = csv_name
        findings.append(result)
    for result in check_cd_quantity_balance(rows, headers, tolerance, csv_name):
        result["file"] = csv_name
        findings.append(result)

    # Markdown cross-reference checks (Tier 1)
    for check_fn in [check_md_billed_cost_total, check_md_effective_cost_total, check_md_row_count]:
        result = check_fn(rows, headers, md_summary, csv_name)
        if result:
            result["file"] = csv_name
            findings.append(result)

    return findings


def validate_directory(dir_path, tolerance):
    """Run all checks on all CSVs in a directory, including cross-file checks."""
    csv_files = sorted(dir_path.glob("*.csv"))
    if not csv_files:
        return []

    findings = []
    file_headers = {}

    for csv_path in csv_files:
        # Look for companion markdown with same stem
        md_candidates = [
            dir_path / f"{csv_path.stem}.md",
            dir_path.parent / f"{csv_path.stem}.md",
        ]
        # Also check in appendix directory structure
        parts = csv_path.parts
        if "data" in parts:
            data_idx = parts.index("data")
            appendix_base = Path(*parts[:data_idx]) / "appendix"
            for subdir in appendix_base.iterdir() if appendix_base.exists() else []:
                if subdir.is_dir():
                    md_candidates.append(subdir / f"{csv_path.stem}.md")

        md_path = None
        for candidate in md_candidates:
            if candidate.exists():
                md_path = candidate
                break

        headers, _ = load_csv(csv_path)
        file_headers[csv_path.name] = headers

        file_findings = validate_single_csv(csv_path, md_path, tolerance)
        findings.extend(file_findings)

    # Cross-file column consistency
    for result in check_cross_file_columns(file_headers):
        findings.append(result)

    return findings


def build_summary(findings):
    """Compute pass/fail counts by tier."""
    tiers = {"arithmetic": 0, "nullability": 0, "cross_row": 0, "semantic": 0}
    for f in findings:
        tier = f.get("tier", "unknown")
        if tier in tiers:
            tiers[tier] += 1
    return {tier: {"failures": count} for tier, count in tiers.items()}


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic gap-check validator for FOCUS CSV example files."
    )
    parser.add_argument("--csv", nargs="+", type=Path, help="CSV file(s) to validate")
    parser.add_argument("--markdown", nargs="+", type=Path,
                        help="Companion markdown file(s) for cross-reference checks")
    parser.add_argument("--directory", type=Path, help="Directory of CSVs to validate")
    parser.add_argument("--tolerance", type=Decimal, default=DEFAULT_TOLERANCE,
                        help=f"Decimal comparison tolerance (default: {DEFAULT_TOLERANCE})")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    args = parser.parse_args()

    if not args.csv and not args.directory:
        parser.error("Provide --csv or --directory")

    all_findings = []

    if args.directory:
        all_findings.extend(validate_directory(args.directory, args.tolerance))
    elif args.csv:
        md_map = {}
        if args.markdown:
            for md_path in args.markdown:
                md_map[md_path.stem] = md_path

        for csv_path in args.csv:
            md_path = md_map.get(csv_path.stem)
            all_findings.extend(validate_single_csv(csv_path, md_path, args.tolerance))

    output = {
        "version": __version__,
        "files_checked": len(args.csv or []) if args.csv else len(list((args.directory or Path()).glob("*.csv"))),
        "total_findings": len(all_findings),
        "findings": all_findings,
        "summary": build_summary(all_findings),
    }

    json.dump(output, sys.stdout, indent=2, default=str)
    print()  # trailing newline


if __name__ == "__main__":
    main()
