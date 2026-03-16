#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import statistics
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Iterable


DISTANCE_BUCKETS: list[tuple[str, float | None, float | None]] = [
    ("0-3%", 0.0, 3.0),
    ("3-7%", 3.0, 7.0),
    ("7-15%", 7.0, 15.0),
    (">15%", 15.0, None),
]


@dataclass
class CandidateRow:
    report_date: str
    symbol: str
    decision: str | None
    setup_id: str | None
    entry_state: str | None
    distance_to_entry_pct: float | None
    current_price: float | None
    planned_entry_price: float | None
    decision_reasons: list[str]
    source_path: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze chased-entry behavior across recent Spot Altcoin Scanner reports."
    )
    parser.add_argument(
        "--reports-dir",
        default="reports",
        help="Directory containing YYYY-MM-DD.json report files (default: reports)",
    )
    parser.add_argument(
        "--output-dir",
        default="reports/analysis",
        help="Directory for generated analysis artifacts (default: reports/analysis)",
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=7,
        help="Number of most recent daily report JSON files to analyze (default: 7)",
    )
    parser.add_argument(
        "--start-date",
        default=None,
        help="Optional lower bound date in YYYY-MM-DD",
    )
    parser.add_argument(
        "--end-date",
        default=None,
        help="Optional upper bound date in YYYY-MM-DD",
    )
    return parser.parse_args()


def is_daily_report_json(path: Path) -> bool:
    if path.suffix.lower() != ".json":
        return False
    name = path.name
    if "_" in name:
        return False
    try:
        datetime.strptime(path.stem, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def parse_report_date(path: Path) -> str:
    return path.stem


def parse_iso_date(value: str | None) -> datetime | None:
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d")


def coerce_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def coerce_list_of_str(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(v) for v in value]
    if isinstance(value, str):
        return [part.strip() for part in value.split(",") if part.strip()]
    return [str(value)]


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def iter_dict_nodes(obj: Any, path: str = "$") -> Iterable[tuple[dict[str, Any], str]]:
    if isinstance(obj, dict):
        yield obj, path
        for key, value in obj.items():
            yield from iter_dict_nodes(value, f"{path}.{key}")
    elif isinstance(obj, list):
        for idx, value in enumerate(obj):
            yield from iter_dict_nodes(value, f"{path}[{idx}]")


def looks_like_candidate(node: dict[str, Any]) -> bool:
    return "symbol" in node and "decision" in node and "entry_state" in node


def first_non_null_float(node: dict[str, Any], keys: list[str]) -> float | None:
    for key in keys:
        value = coerce_float(node.get(key))
        if value is not None:
            return value
    return None


def normalize_setup_bucket(setup_id: str | None) -> str:
    if not setup_id:
        return "other"
    s = setup_id.lower()
    if "pullback" in s:
        return "pullback"
    if "reversal" in s:
        return "reversal"
    if "breakout" in s:
        return "breakout"
    return "other"


def extract_candidates(report_data: Any, report_date: str) -> list[CandidateRow]:
    rows: list[CandidateRow] = []

    for node, source_path in iter_dict_nodes(report_data):
        if not looks_like_candidate(node):
            continue

        symbol = str(node.get("symbol") or "").strip()
        if not symbol:
            continue

        decision = str(node.get("decision")) if node.get("decision") is not None else None
        setup_id = (
            str(node.get("setup_id"))
            if node.get("setup_id") is not None
            else str(node.get("setup_type")) if node.get("setup_type") is not None else None
        )
        entry_state = (
            str(node.get("entry_state")) if node.get("entry_state") is not None else None
        )

        planned_entry_price = first_non_null_float(
            node,
            ["entry_price", "entry", "planned_entry_price", "entry_trigger", "trigger_price"],
        )
        current_price = first_non_null_float(
            node,
            ["current_price", "price", "market_price", "last_price", "close"],
        )
        distance_to_entry_pct = first_non_null_float(
            node,
            ["distance_to_entry_pct", "entry_distance_pct", "distance_from_entry_pct"],
        )

        rows.append(
            CandidateRow(
                report_date=report_date,
                symbol=symbol,
                decision=decision,
                setup_id=setup_id,
                entry_state=entry_state,
                distance_to_entry_pct=distance_to_entry_pct,
                current_price=current_price,
                planned_entry_price=planned_entry_price,
                decision_reasons=coerce_list_of_str(node.get("decision_reasons")),
                source_path=source_path,
            )
        )

    return deduplicate_rows(rows)


def dedup_key(row: CandidateRow) -> tuple[Any, ...]:
    distance = None if row.distance_to_entry_pct is None else round(row.distance_to_entry_pct, 6)
    planned = None if row.planned_entry_price is None else round(row.planned_entry_price, 12)
    current = None if row.current_price is None else round(row.current_price, 12)

    return (
        row.report_date,
        row.symbol,
        row.decision,
        row.entry_state,
        row.setup_id or "",
        distance,
        planned,
        current,
    )


def row_quality_score(row: CandidateRow) -> tuple[int, int, int, int, int]:
    has_setup = 1 if row.setup_id else 0
    has_planned = 1 if row.planned_entry_price is not None else 0
    has_current = 1 if row.current_price is not None else 0
    reason_count = len(row.decision_reasons)
    from_trade_candidates = 1 if ".trade_candidates[" in row.source_path else 0

    return (
        has_setup,
        has_planned,
        has_current,
        reason_count,
        from_trade_candidates,
    )


def deduplicate_rows(rows: list[CandidateRow]) -> list[CandidateRow]:
    chosen: dict[tuple[Any, ...], CandidateRow] = {}

    for row in rows:
        key = dedup_key(row)
        existing = chosen.get(key)
        if existing is None:
            chosen[key] = row
            continue

        if row_quality_score(row) > row_quality_score(existing):
            chosen[key] = row

    return list(chosen.values())


def select_report_files(
    reports_dir: Path,
    runs: int,
    start_date: str | None,
    end_date: str | None,
) -> list[Path]:
    files = sorted(
        [p for p in reports_dir.iterdir() if p.is_file() and is_daily_report_json(p)],
        key=lambda p: p.name,
    )

    start_dt = parse_iso_date(start_date)
    end_dt = parse_iso_date(end_date)

    filtered: list[Path] = []
    for path in files:
        report_dt = parse_iso_date(parse_report_date(path))
        if report_dt is None:
            continue
        if start_dt and report_dt < start_dt:
            continue
        if end_dt and report_dt > end_dt:
            continue
        filtered.append(path)

    return filtered[-runs:]


def median_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    return float(statistics.median(values))


def p75_or_none(values: list[float]) -> float | None:
    if not values:
        return None
    if len(values) == 1:
        return float(values[0])
    return float(statistics.quantiles(values, n=4, method="inclusive")[2])


def safe_pct(numerator: int, denominator: int) -> float | None:
    if denominator == 0:
        return None
    return (numerator / denominator) * 100.0


def classify_distance_bucket(distance: float | None) -> str:
    if distance is None:
        return "unknown"
    for label, lower, upper in DISTANCE_BUCKETS:
        if lower is not None and distance < lower:
            continue
        if upper is None and distance >= lower:
            return label
        if lower is not None and upper is not None and lower <= distance < upper:
            return label
    return "unknown"


def bucket_counter(rows: list[CandidateRow], chased_only: bool = False) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        if chased_only and row.entry_state != "chased":
            continue
        counter[classify_distance_bucket(row.distance_to_entry_pct)] += 1
    ordered = {label: counter.get(label, 0) for label, _, _ in DISTANCE_BUCKETS}
    if counter.get("unknown", 0):
        ordered["unknown"] = counter["unknown"]
    return ordered


def summarize_subset(rows: list[CandidateRow], label: str) -> dict[str, Any]:
    rows_by_date: dict[str, list[CandidateRow]] = defaultdict(list)
    for row in rows:
        rows_by_date[row.report_date].append(row)

    decision_counter: Counter[str] = Counter()
    entry_state_counter: Counter[str] = Counter()
    reason_counter: Counter[str] = Counter()

    for row in rows:
        decision_counter[row.decision or "null"] += 1
        entry_state_counter[row.entry_state or "null"] += 1
        for reason in row.decision_reasons:
            reason_counter[reason] += 1

    per_run: list[dict[str, Any]] = []
    for report_date in sorted(rows_by_date):
        day_rows = rows_by_date[report_date]
        chased_rows = [r for r in day_rows if r.entry_state == "chased"]
        distances = [r.distance_to_entry_pct for r in chased_rows if r.distance_to_entry_pct is not None]
        per_run.append(
            {
                "report_date": report_date,
                "candidate_count": len(day_rows),
                "decision_counts": dict(Counter((r.decision or "null") for r in day_rows)),
                "entry_state_counts": dict(Counter((r.entry_state or "null") for r in day_rows)),
                "chased_count": len(chased_rows),
                "chased_pct": safe_pct(len(chased_rows), len(day_rows)),
                "median_chased_distance_to_entry_pct": median_or_none(distances),
                "p75_chased_distance_to_entry_pct": p75_or_none(distances),
                "distance_buckets_all": bucket_counter(day_rows, chased_only=False),
                "distance_buckets_chased": bucket_counter(day_rows, chased_only=True),
            }
        )

    chased_examples = sorted(
        [r for r in rows if r.entry_state == "chased"],
        key=lambda r: (r.report_date, -(r.distance_to_entry_pct or -1.0), r.symbol, r.setup_id or ""),
    )[:20]

    return {
        "label": label,
        "candidate_count": len(rows),
        "decision_counts": dict(decision_counter),
        "entry_state_counts": dict(entry_state_counter),
        "reason_counts": dict(reason_counter.most_common()),
        "distance_buckets_all": bucket_counter(rows, chased_only=False),
        "distance_buckets_chased": bucket_counter(rows, chased_only=True),
        "per_run": per_run,
        "sample_chased_candidates": [asdict(r) for r in chased_examples],
    }


def build_summary(rows: list[CandidateRow]) -> dict[str, Any]:
    rows_by_date: dict[str, list[CandidateRow]] = defaultdict(list)
    for row in rows:
        rows_by_date[row.report_date].append(row)

    setup_counts: dict[str, Counter[str]] = defaultdict(Counter)
    setup_distances: dict[str, list[float]] = defaultdict(list)
    reason_counter: Counter[str] = Counter()
    decision_counter: Counter[str] = Counter()
    entry_state_counter: Counter[str] = Counter()
    bucket_rows: dict[str, list[CandidateRow]] = defaultdict(list)

    for row in rows:
        decision_counter[row.decision or "null"] += 1
        entry_state_counter[row.entry_state or "null"] += 1
        setup_key = row.setup_id or ""
        setup_counts[setup_key][row.entry_state or "null"] += 1
        if row.distance_to_entry_pct is not None:
            setup_distances[setup_key].append(row.distance_to_entry_pct)
        for reason in row.decision_reasons:
            reason_counter[reason] += 1
        bucket_rows[normalize_setup_bucket(row.setup_id)].append(row)

    per_run: list[dict[str, Any]] = []
    for report_date in sorted(rows_by_date):
        day_rows = rows_by_date[report_date]
        chased_rows = [r for r in day_rows if r.entry_state == "chased"]
        distances = [r.distance_to_entry_pct for r in chased_rows if r.distance_to_entry_pct is not None]
        bucket_counts = Counter(normalize_setup_bucket(r.setup_id) for r in day_rows)
        chased_bucket_counts = Counter(normalize_setup_bucket(r.setup_id) for r in chased_rows)

        per_run.append(
            {
                "report_date": report_date,
                "candidate_count": len(day_rows),
                "decision_counts": dict(Counter((r.decision or "null") for r in day_rows)),
                "entry_state_counts": dict(Counter((r.entry_state or "null") for r in day_rows)),
                "setup_bucket_counts": dict(bucket_counts),
                "chased_bucket_counts": dict(chased_bucket_counts),
                "chased_count": len(chased_rows),
                "chased_pct": safe_pct(len(chased_rows), len(day_rows)),
                "median_chased_distance_to_entry_pct": median_or_none(distances),
                "p75_chased_distance_to_entry_pct": p75_or_none(distances),
                "distance_buckets_all": bucket_counter(day_rows, chased_only=False),
                "distance_buckets_chased": bucket_counter(day_rows, chased_only=True),
            }
        )

    setup_breakdown: list[dict[str, Any]] = []
    for setup_id in sorted(setup_counts):
        counter = setup_counts[setup_id]
        total = sum(counter.values())
        chased_count = counter.get("chased", 0)
        setup_rows = [r for r in rows if (r.setup_id or "") == setup_id]
        setup_breakdown.append(
            {
                "setup_id": setup_id,
                "setup_bucket": normalize_setup_bucket(setup_id or None),
                "candidate_count": total,
                "entry_state_counts": dict(counter),
                "chased_count": chased_count,
                "chased_pct": safe_pct(chased_count, total),
                "median_distance_to_entry_pct": median_or_none(setup_distances[setup_id]),
                "p75_distance_to_entry_pct": p75_or_none(setup_distances[setup_id]),
                "distance_buckets_all": bucket_counter(setup_rows, chased_only=False),
                "distance_buckets_chased": bucket_counter(setup_rows, chased_only=True),
            }
        )

    top_chased_examples = sorted(
        [r for r in rows if r.entry_state == "chased"],
        key=lambda r: (r.report_date, -(r.distance_to_entry_pct or -1.0), r.symbol, r.setup_id or ""),
    )[:50]

    setup_bucket_summaries = {
        bucket: summarize_subset(bucket_rows.get(bucket, []), bucket)
        for bucket in ["pullback", "reversal", "breakout", "other"]
    }

    return {
        "generated_at_utc": datetime.utcnow().isoformat(timespec="seconds") + "Z",
        "runs_analyzed": len(rows_by_date),
        "total_candidates": len(rows),
        "decision_counts": dict(decision_counter),
        "entry_state_counts": dict(entry_state_counter),
        "reason_counts": dict(reason_counter.most_common()),
        "distance_buckets_all": bucket_counter(rows, chased_only=False),
        "distance_buckets_chased": bucket_counter(rows, chased_only=True),
        "per_run": per_run,
        "setup_breakdown": setup_breakdown,
        "setup_bucket_summaries": setup_bucket_summaries,
        "top_chased_examples": [asdict(r) for r in top_chased_examples],
    }


def format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.2f}"


def render_distance_bucket_table(title: str, bucket_counts: dict[str, int]) -> list[str]:
    lines: list[str] = []
    lines.append(title)
    lines.append("")
    lines.append("| Bucket | Count |")
    lines.append("|---|---:|")
    for label, _, _ in DISTANCE_BUCKETS:
        lines.append(f"| {label} | {bucket_counts.get(label, 0)} |")
    if "unknown" in bucket_counts:
        lines.append(f"| unknown | {bucket_counts.get('unknown', 0)} |")
    lines.append("")
    return lines


def render_subset_markdown(subset: dict[str, Any]) -> list[str]:
    lines: list[str] = []
    label = subset["label"]

    lines.append(f"## {label.title()} only")
    lines.append("")
    lines.append(f"- Candidates: {subset['candidate_count']}")
    lines.append("")

    lines.append("### Entry-state counts")
    lines.append("")
    for key, value in subset["entry_state_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")

    lines.append("### Decision counts")
    lines.append("")
    for key, value in subset["decision_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")

    lines.extend(render_distance_bucket_table("### Distance buckets (all)", subset["distance_buckets_all"]))
    lines.extend(render_distance_bucket_table("### Distance buckets (chased only)", subset["distance_buckets_chased"]))

    lines.append("### Per-run summary")
    lines.append("")
    lines.append("| Date | Candidates | Chased | Chased % | Median chased distance % | P75 chased distance % | 0-3% | 3-7% | 7-15% | >15% |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in subset["per_run"]:
        buckets = row["distance_buckets_chased"]
        lines.append(
            "| {report_date} | {candidate_count} | {chased_count} | {chased_pct} | {median} | {p75} | {b0} | {b1} | {b2} | {b3} |".format(
                report_date=row["report_date"],
                candidate_count=row["candidate_count"],
                chased_count=row["chased_count"],
                chased_pct=format_float(row["chased_pct"]),
                median=format_float(row["median_chased_distance_to_entry_pct"]),
                p75=format_float(row["p75_chased_distance_to_entry_pct"]),
                b0=buckets.get("0-3%", 0),
                b1=buckets.get("3-7%", 0),
                b2=buckets.get("7-15%", 0),
                b3=buckets.get(">15%", 0),
            )
        )
    lines.append("")

    lines.append("### Most common decision reasons")
    lines.append("")
    for reason, count in list(subset["reason_counts"].items())[:10]:
        lines.append(f"- {reason}: {count}")
    lines.append("")

    lines.append("### Sample chased candidates")
    lines.append("")
    lines.append("| Date | Symbol | Decision | Setup | Distance % | Reasons |")
    lines.append("|---|---|---|---|---:|---|")
    for row in subset["sample_chased_candidates"][:10]:
        lines.append(
            "| {report_date} | {symbol} | {decision} | {setup_id} | {distance} | {reasons} |".format(
                report_date=row["report_date"],
                symbol=row["symbol"],
                decision=row["decision"] or "",
                setup_id=row["setup_id"] or "",
                distance=format_float(row["distance_to_entry_pct"]),
                reasons=", ".join(row["decision_reasons"]),
            )
        )
    lines.append("")
    return lines


def render_markdown(summary: dict[str, Any], source_files: list[Path]) -> str:
    lines: list[str] = []
    lines.append("# Chased Entry Analysis")
    lines.append("")
    lines.append(f"- Generated: {summary['generated_at_utc']}")
    lines.append(f"- Runs analyzed: {summary['runs_analyzed']}")
    lines.append(f"- Total candidates: {summary['total_candidates']}")
    lines.append(f"- Source files: {', '.join(p.name for p in source_files)}")
    lines.append("")

    lines.append("## Overall entry-state counts")
    lines.append("")
    for key, value in summary["entry_state_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")

    lines.append("## Overall decision counts")
    lines.append("")
    for key, value in summary["decision_counts"].items():
        lines.append(f"- {key}: {value}")
    lines.append("")

    lines.extend(render_distance_bucket_table("## Overall distance buckets (all)", summary["distance_buckets_all"]))
    lines.extend(render_distance_bucket_table("## Overall distance buckets (chased only)", summary["distance_buckets_chased"]))

    lines.append("## Per-run chased summary")
    lines.append("")
    lines.append("| Date | Candidates | Chased | Chased % | Median chased distance % | P75 chased distance % | Pullback | Reversal | Breakout | Other | 0-3% | 3-7% | 7-15% | >15% |")
    lines.append("|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in summary["per_run"]:
        bucket_counts = row.get("setup_bucket_counts", {})
        distance_buckets = row.get("distance_buckets_chased", {})
        lines.append(
            "| {report_date} | {candidate_count} | {chased_count} | {chased_pct} | {median} | {p75} | {pullback} | {reversal} | {breakout} | {other} | {b0} | {b1} | {b2} | {b3} |".format(
                report_date=row["report_date"],
                candidate_count=row["candidate_count"],
                chased_count=row["chased_count"],
                chased_pct=format_float(row["chased_pct"]),
                median=format_float(row["median_chased_distance_to_entry_pct"]),
                p75=format_float(row["p75_chased_distance_to_entry_pct"]),
                pullback=bucket_counts.get("pullback", 0),
                reversal=bucket_counts.get("reversal", 0),
                breakout=bucket_counts.get("breakout", 0),
                other=bucket_counts.get("other", 0),
                b0=distance_buckets.get("0-3%", 0),
                b1=distance_buckets.get("3-7%", 0),
                b2=distance_buckets.get("7-15%", 0),
                b3=distance_buckets.get(">15%", 0),
            )
        )
    lines.append("")

    lines.append("## Setup breakdown")
    lines.append("")
    lines.append("| Setup | Bucket | Candidates | Chased | Chased % | Median distance % | P75 distance % | 0-3% | 3-7% | 7-15% | >15% |")
    lines.append("|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|")
    for row in summary["setup_breakdown"]:
        dist = row["distance_buckets_chased"]
        lines.append(
            "| {setup_id} | {setup_bucket} | {candidate_count} | {chased_count} | {chased_pct} | {median} | {p75} | {b0} | {b1} | {b2} | {b3} |".format(
                setup_id=row["setup_id"],
                setup_bucket=row["setup_bucket"],
                candidate_count=row["candidate_count"],
                chased_count=row["chased_count"],
                chased_pct=format_float(row["chased_pct"]),
                median=format_float(row["median_distance_to_entry_pct"]),
                p75=format_float(row["p75_distance_to_entry_pct"]),
                b0=dist.get("0-3%", 0),
                b1=dist.get("3-7%", 0),
                b2=dist.get("7-15%", 0),
                b3=dist.get(">15%", 0),
            )
        )
    lines.append("")

    lines.append("## Most common decision reasons")
    lines.append("")
    for reason, count in list(summary["reason_counts"].items())[:15]:
        lines.append(f"- {reason}: {count}")
    lines.append("")

    lines.append("## Sample chased candidates (overall)")
    lines.append("")
    lines.append("| Date | Symbol | Decision | Setup | Distance % | Reasons |")
    lines.append("|---|---|---|---|---:|---|")
    for row in summary["top_chased_examples"][:20]:
        lines.append(
            "| {report_date} | {symbol} | {decision} | {setup_id} | {distance} | {reasons} |".format(
                report_date=row["report_date"],
                symbol=row["symbol"],
                decision=row["decision"] or "",
                setup_id=row["setup_id"] or "",
                distance=format_float(row["distance_to_entry_pct"]),
                reasons=", ".join(row["decision_reasons"]),
            )
        )
    lines.append("")

    for bucket in ["pullback", "reversal", "breakout", "other"]:
        lines.extend(render_subset_markdown(summary["setup_bucket_summaries"][bucket]))

    return "\n".join(lines)


def main() -> int:
    args = parse_args()

    reports_dir = Path(args.reports_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    report_files = select_report_files(
        reports_dir=reports_dir,
        runs=args.runs,
        start_date=args.start_date,
        end_date=args.end_date,
    )
    if not report_files:
        raise SystemExit("No matching daily report JSON files found.")

    all_rows: list[CandidateRow] = []
    for report_file in report_files:
        report_data = load_json(report_file)
        report_date = parse_report_date(report_file)
        all_rows.extend(extract_candidates(report_data, report_date))

    if not all_rows:
        raise SystemExit("No candidate rows found in selected reports.")

    summary = build_summary(all_rows)

    latest_date = parse_report_date(report_files[-1])
    stem = f"chased_entry_analysis_{latest_date}"

    json_path = output_dir / f"{stem}.json"
    md_path = output_dir / f"{stem}.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    with md_path.open("w", encoding="utf-8") as f:
        f.write(render_markdown(summary, report_files) + "\n")

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
