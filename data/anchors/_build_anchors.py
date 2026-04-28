"""One-shot anchor builder.

Reads the raw fetched files in this directory and writes per-question anchor
JSON files. Run from data/anchors/. Idempotent — safe to re-run.
"""

from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent


def write_json(name: str, payload: dict) -> None:
    out = HERE / name
    with out.open("w", encoding="utf-8") as fh:
        json.dump(payload, fh, indent=2, ensure_ascii=False)
    size = out.stat().st_size
    print(f"  wrote {name}  ({size:,} bytes)")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


# ---- q_001: supplier dedupe (USAspending recipient name variants) -----------

def build_q001() -> None:
    lockheed = json.loads((HERE / "lockheed_autocomplete.json").read_text())["results"]
    gd = json.loads((HERE / "general_dynamics_autocomplete.json").read_text())["results"]

    # Pick the two best dedupe candidate pairs to anchor the question.
    pairs = [
        {
            "pair_id": "lockheed_corp",
            "candidate_a": next(r for r in lockheed if r["recipient_name"] == "LOCKHEED MARTIN CORPORATION"),
            "candidate_b": next(r for r in lockheed if r["recipient_name"] == "LOCKHEED MARTIN CORP"),
            "pattern": "abbreviation variant (CORPORATION vs CORP)",
            "likely_same_entity": True,
        },
        {
            "pair_id": "lockheed_services",
            "candidate_a": next(r for r in lockheed if r["recipient_name"] == "LOCKHEED MARTIN SERVICES, INC."),
            "candidate_b": next(r for r in lockheed if r["recipient_name"] == "LOCKHEED MARTIN SERVICES INC"),
            "pattern": "punctuation/comma variant",
            "likely_same_entity": True,
        },
        {
            "pair_id": "lockheed_services_llc_vs_inc",
            "candidate_a": next(r for r in lockheed if r["recipient_name"] == "LOCKHEED MARTIN SERVICES, LLC"),
            "candidate_b": next(r for r in lockheed if r["recipient_name"] == "LOCKHEED MARTIN SERVICES, INC."),
            "pattern": "different legal entity type (LLC vs INC) — likely DIFFERENT legal entities, NOT a dedupe",
            "likely_same_entity": False,
        },
        {
            "pair_id": "gd_land_systems",
            "candidate_a": next(r for r in gd if r["recipient_name"] == "GENERAL DYNAMICS LAND SYSTEMS INC."),
            "candidate_b": next(r for r in gd if r["recipient_name"] == "GENERAL DYNAMICS LAND SYSTEMS"),
            "pattern": "missing entity suffix (truncation/abbreviation)",
            "likely_same_entity": True,
        },
    ]

    payload = {
        "anchor_for": "q_001 — supplier_data dedupe",
        "source": "USAspending.gov autocomplete API (api.usaspending.gov/api/v2/autocomplete/recipient/)",
        "fetched_at": now_iso(),
        "note": (
            "Real federal-contractor names exhibiting the variant patterns AP supplier "
            "master teams encounter daily. UEI/DUNS are null in the autocomplete payload; "
            "for production use, hit the recipient_overview endpoint to pull canonical UEIs "
            "per pair to confirm whether they are the same legal entity."
        ),
        "all_lockheed_variants": [r["recipient_name"] for r in lockheed],
        "all_general_dynamics_variants": [r["recipient_name"] for r in gd],
        "annotated_pairs": pairs,
    }
    write_json("anchor_q001_supplier_dedupe.json", payload)


# ---- q_004: duplicate invoice detection (Chicago Payments) ------------------

def build_q004() -> None:
    raw = json.loads((HERE / "chicago_payments_raw.json").read_text())

    # Normalize and find near-duplicates: same vendor + same amount + same contract.
    # The Chicago dataset's `check_date` is year-only at this granularity, so we
    # look for clusters of identical (vendor, amount, contract) — strong signal
    # of repeated payments worth surfacing as candidate duplicates.
    by_key: dict[tuple, list] = defaultdict(list)
    for row in raw:
        key = (row.get("vendor_name"), row.get("amount"), row.get("contract_number"))
        by_key[key].append(row)

    # A "duplicate cluster" = 2+ payments with identical key.
    clusters = [
        {
            "vendor_name": k[0],
            "amount": k[1],
            "contract_number": k[2],
            "occurrences": len(v),
            "rows": v,
        }
        for k, v in by_key.items()
        if len(v) >= 2 and k[0] and k[1]
    ]
    clusters.sort(key=lambda c: c["occurrences"], reverse=True)

    # Also surface near-amount duplicates (same vendor, amounts within $1).
    by_vendor: dict[str, list] = defaultdict(list)
    for row in raw:
        if row.get("vendor_name") and row.get("amount"):
            by_vendor[row["vendor_name"]].append(row)

    near_amount: list[dict] = []
    for vendor, rows in by_vendor.items():
        amounts = sorted({float(r["amount"]) for r in rows})
        for i in range(len(amounts) - 1):
            a, b = amounts[i], amounts[i + 1]
            if 0 < (b - a) <= 1.0 and a > 100:  # $1 difference, non-trivial amount
                near_amount.append({
                    "vendor_name": vendor,
                    "amount_a": a,
                    "amount_b": b,
                    "delta": round(b - a, 2),
                })

    payload = {
        "anchor_for": "q_004 — invoice_processing duplicate detection",
        "source": "data.cityofchicago.org Payments dataset (resource s4vu-giwb)",
        "fetched_at": now_iso(),
        "rows_in_sample": len(raw),
        "exact_duplicate_cluster_count": len(clusters),
        "near_amount_pair_count": len(near_amount),
        "note": (
            "Exact-cluster = same vendor + same amount + same contract appearing 2+ times in "
            "the sample. These are not necessarily improper payments — they may be legitimate "
            "milestone billings on a multi-payment contract — but they are exactly the rows a "
            "duplicate-detection rule would flag for review. Use the top cluster to anchor the "
            "scenario in q_004 (replace the synthesized 'NB-2024-1142' invoice numbers with "
            "real values)."
        ),
        "top_exact_duplicate_clusters": clusters[:10],
        "near_amount_pairs_sample": near_amount[:10],
    }
    write_json("anchor_q004_duplicate_detection.json", payload)


# ---- q_009: sanctions screening (OFAC SDN sample) ---------------------------

def build_q009() -> None:
    # OFAC SDN.csv columns:
    # ent_num, SDN_Name, SDN_Type, Program, Title, Call_Sign, Vess_type,
    # Tonnage, GRT, Vess_flag, Vess_owner, Remarks
    columns = [
        "ent_num", "sdn_name", "sdn_type", "program", "title",
        "call_sign", "vess_type", "tonnage", "grt", "vess_flag",
        "vess_owner", "remarks",
    ]

    rows: list[dict] = []
    with (HERE / "ofac_sdn.csv").open("r", encoding="latin-1") as fh:
        reader = csv.reader(fh)
        for raw in reader:
            row = {columns[i]: (raw[i] if i < len(raw) else "") for i in range(len(columns))}
            # OFAC null marker is "-0- " (note trailing space). Normalize to "".
            row = {k: ("" if v.strip() == "-0-" else v.strip()) for k, v in row.items()}
            # Entities are the implicit type when sdn_type is empty.
            if not row["sdn_type"]:
                row["sdn_type"] = "entity"
            rows.append(row)

    # Stratified sample across high-volume programs and entity types. q_009's
    # scenario should face a real screening hit, so weight toward entities and
    # the programs most relevant to procurement (Russia, Iran, sanctions evasion).
    programs_seen = Counter(r["program"] for r in rows)

    def pick(filter_fn, n):
        return [r for r in rows if filter_fn(r)][:n]

    sample = []
    sample.extend(pick(lambda r: r["sdn_type"] == "entity" and "RUSSIA" in r["program"].upper(), 5))
    sample.extend(pick(lambda r: r["sdn_type"] == "individual" and "RUSSIA" in r["program"].upper(), 3))
    sample.extend(pick(lambda r: r["sdn_type"] == "entity" and "IRAN" in r["program"].upper(), 3))
    sample.extend(pick(lambda r: r["sdn_type"] == "entity" and "CYBER" in r["program"].upper(), 2))
    sample.extend(pick(lambda r: r["sdn_type"] == "vessel", 2))
    # Dedupe by ent_num
    seen = set()
    deduped = []
    for r in sample:
        if r["ent_num"] not in seen:
            seen.add(r["ent_num"])
            deduped.append(r)

    payload = {
        "anchor_for": "q_009 — supplier_data sanctions screening",
        "source": "OFAC SDN list (treasury.gov/ofac/downloads/sdn.csv)",
        "fetched_at": now_iso(),
        "total_records_in_sdn": len(rows),
        "program_distribution_top10": programs_seen.most_common(10),
        "stratified_sample": deduped,
        "note": (
            "Real SDN-listed entities/individuals/vessels across high-volume programs. "
            "Use one Russia-program entity to make q_009's hypothetical 'Pacific Trade "
            "Solutions LLC / Ivan Petrov' scenario concrete — replace the made-up name "
            "with a real entity if you want the model to face an actual screening hit, "
            "OR keep the made-up scenario and use this list as the rubric anchor for "
            "'what should the sanctions screen check against.'"
        ),
    }
    write_json("anchor_q009_sanctions_screening.json", payload)


def main() -> None:
    print("building anchor files...")
    build_q001()
    build_q004()
    build_q009()
    print("done.")


if __name__ == "__main__":
    main()
