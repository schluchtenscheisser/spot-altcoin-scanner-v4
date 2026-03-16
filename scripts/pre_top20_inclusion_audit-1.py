#!/usr/bin/env python3
"""
Pre-Top20 inclusion audit for Spot Altcoin Scanner.

Purpose
-------
Audit the upstream candidate pool BEFORE final Top20 publication to answer:

- Are the published Top20 symbols actually the best-scoring deduplicated symbols?
- Are more executable candidates being displaced below the cut line?
- Is setup-type concentration already present before Top20, or introduced by the cap?
- Is the issue a ranking/inclusion problem, or a market-wide weakness?

This script is analysis-only. It does NOT modify pipeline behavior.

Inputs
------
Best effort auto-discovery, plus optional explicit paths:
- --run-json PATH        canonical run JSON with trade_candidates
- --upstream-json PATH   snapshot or analysis JSON containing a larger candidate array

Snapshot-aware discovery order
------------------------------
1) snapshots/runtime
2) snapshots/history
3) snapshots/raw
4) remaining repo JSONs

Outputs
-------
Writes both:
- reports/analysis/pre_top20_inclusion_audit_<date>.json
- reports/analysis/pre_top20_inclusion_audit_<date>.md
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple


UNKNOWN = "UNKNOWN"
ENTRY_ELIGIBLE_TRADEABILITY = {"DIRECT_OK", "TRANCHE_OK"}
IGNORED_DIR_PARTS = {".git", ".venv", "venv", "__pycache__"}
SNAPSHOT_PRIORITY = [
    "snapshots/runtime",
    "snapshots/history",
    "snapshots/raw",
    "other",
]


@dataclass(frozen=True)
class RunRecord:
    path: Path
    run_id: str
    timestamp_utc: str
    canonical_schema_version: Optional[str]
    raw_data: Dict[str, Any]
    trade_candidates: List[Dict[str, Any]]


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def analysis_dir() -> Path:
    out = repo_root() / "reports" / "analysis"
    out.mkdir(parents=True, exist_ok=True)
    return out


def utc_now_slug() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d_%H%M%S")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def safe_load_json(path: Path) -> Optional[Any]:
    try:
        with path.open("r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def normalize_str(value: Any, default: str = UNKNOWN) -> str:
    if value in (None, ""):
        return default
    return str(value)


def normalize_list_str(value: Any) -> List[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(x) for x in value if x is not None]
    if isinstance(value, str):
        return [value]
    return [str(value)]


def is_finite_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and math.isfinite(value)


def score_of(row: Dict[str, Any], key: str) -> Optional[float]:
    value = row.get(key)
    return float(value) if is_finite_number(value) else None


def bool_true(value: Any) -> bool:
    return value is True


def symbol_of(row: Dict[str, Any]) -> str:
    return normalize_str(row.get("symbol"), "UNKNOWN_SYMBOL")


def setup_id_of(row: Dict[str, Any]) -> str:
    return normalize_str(row.get("setup_id"))


def setup_type_of(row: Dict[str, Any]) -> str:
    return normalize_str(
        row.get("best_setup_type") or row.get("setup_type") or row.get("category")
    )


def decision_of(row: Dict[str, Any]) -> str:
    return normalize_str(row.get("decision"))


def tradeability_of(row: Dict[str, Any]) -> str:
    return normalize_str(row.get("tradeability_class"))


def entry_state_of(row: Dict[str, Any]) -> str:
    return normalize_str(row.get("entry_state"))


def reasons_of(row: Dict[str, Any]) -> List[str]:
    return normalize_list_str(row.get("decision_reasons"))


def entry_eligible(row: Dict[str, Any]) -> bool:
    return tradeability_of(row) in ENTRY_ELIGIBLE_TRADEABILITY


def looks_like_run_json(data: Any) -> bool:
    return (
        isinstance(data, dict)
        and isinstance(data.get("trade_candidates"), list)
        and isinstance(data.get("run_manifest"), dict)
    )


def parse_run_json(path: Path) -> Optional[RunRecord]:
    data = safe_load_json(path)
    if not looks_like_run_json(data):
        return None

    run_manifest = data.get("run_manifest", {})
    return RunRecord(
        path=path,
        run_id=normalize_str(run_manifest.get("run_id"), path.stem),
        timestamp_utc=normalize_str(run_manifest.get("timestamp_utc"), ""),
        canonical_schema_version=run_manifest.get("canonical_schema_version"),
        raw_data=data,
        trade_candidates=data.get("trade_candidates", []),
    )


def discover_run_files(root: Path) -> List[Path]:
    paths: List[Path] = []
    for path in root.rglob("*.json"):
        if any(part in IGNORED_DIR_PARTS for part in path.parts):
            continue
        name = path.name.lower()
        path_str = str(path).lower().replace("\\", "/")
        if "/reports/analysis/" in path_str:
            continue
        if name.endswith(".manifest.json"):
            continue
        if "counterfactual" in name or "diagnose_rr" in name or "chased_entry_analysis" in name:
            continue
        if "post_risk_unlock_audit" in name or "top20_formation_audit" in name or "pre_top20_inclusion_audit" in name:
            continue
        data = safe_load_json(path)
        if looks_like_run_json(data):
            paths.append(path)
    return sorted(paths)


def sort_runs_desc(runs: List[RunRecord]) -> List[RunRecord]:
    return sorted(runs, key=lambda r: (r.timestamp_utc or "", r.run_id or ""), reverse=True)


def classify_source_bucket(path: Path, root: Path) -> str:
    rel = str(path.resolve().relative_to(root.resolve())).replace("\\", "/").lower()
    if rel.startswith("snapshots/runtime/"):
        return "snapshots/runtime"
    if rel.startswith("snapshots/history/"):
        return "snapshots/history"
    if rel.startswith("snapshots/raw/"):
        return "snapshots/raw"
    return "other"


def source_bucket_rank(bucket: str) -> int:
    try:
        return SNAPSHOT_PRIORITY.index(bucket)
    except ValueError:
        return len(SNAPSHOT_PRIORITY)


def detect_candidate_arrays(payload: Any, min_len: int = 21) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []

    def inspect_container(container: Any, path: str) -> None:
        if isinstance(container, dict):
            for k, v in container.items():
                inspect_container(v, f"{path}.{k}" if path else k)
            return

        if not isinstance(container, list):
            return
        if len(container) < min_len:
            return
        if not container or not isinstance(container[0], dict):
            return

        keys = set()
        sample = container[:3]
        for row in sample:
            if isinstance(row, dict):
                keys.update(row.keys())

        score_keys = {"symbol", "global_score", "weighted_score", "final_score", "setup_score", "setup_id"}
        if len(keys & score_keys) < 2:
            return

        findings.append(
            {
                "path": path or "$",
                "length": len(container),
                "sample_keys": sorted(list(keys))[:25],
                "rows": container,
            }
        )

    inspect_container(payload, "")
    findings.sort(key=lambda x: (-x["length"], x["path"]))
    return findings


def choose_best_candidate_array(findings: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not findings:
        return None

    scored: List[Tuple[int, int, str, Dict[str, Any]]] = []
    for item in findings:
        keys = set(item["sample_keys"])
        quality = 0
        for key in ("symbol", "global_score", "weighted_score", "final_score", "setup_score", "setup_id"):
            if key in keys:
                quality += 1
        scored.append((quality, item["length"], item["path"], item))

    scored.sort(key=lambda x: (-x[0], -x[1], x[2]))
    return scored[0][3]


def preferred_score_proxy(row: Dict[str, Any]) -> Optional[float]:
    for key in ("global_score", "weighted_score", "final_score", "setup_score"):
        value = score_of(row, key)
        if value is not None:
            return value
    return None


def dedup_best_symbol_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    best: Dict[str, Dict[str, Any]] = {}
    for row in rows:
        symbol = symbol_of(row)
        proxy = preferred_score_proxy(row)
        if proxy is None:
            continue

        prev = best.get(symbol)
        if prev is None:
            best[symbol] = row
            continue

        prev_proxy = preferred_score_proxy(prev)
        if prev_proxy is None or proxy > prev_proxy:
            best[symbol] = row
        elif proxy == prev_proxy and setup_id_of(row) < setup_id_of(prev):
            best[symbol] = row

    deduped = list(best.values())
    deduped.sort(
        key=lambda row: (
            -(preferred_score_proxy(row) if preferred_score_proxy(row) is not None else -1e18),
            setup_id_of(row),
            symbol_of(row),
        )
    )
    return deduped


def summarize_distribution(rows: Iterable[Dict[str, Any]], field_name: str) -> Dict[str, int]:
    counter: Counter[str] = Counter()
    for row in rows:
        if field_name == "setup_type":
            counter.update([setup_type_of(row)])
        elif field_name == "tradeability":
            counter.update([tradeability_of(row)])
        elif field_name == "decision":
            counter.update([decision_of(row)])
        elif field_name == "entry_state":
            counter.update([entry_state_of(row)])
    return dict(sorted(counter.items(), key=lambda kv: (-kv[1], kv[0])))


def summarize_numeric(rows: Iterable[Dict[str, Any]], key: str) -> Dict[str, Optional[float]]:
    values = [score_of(r, key) for r in rows]
    clean = [v for v in values if v is not None]
    if not clean:
        return {"count": 0, "min": None, "median": None, "max": None, "mean": None}
    clean.sort()
    n = len(clean)
    median = clean[n // 2] if n % 2 == 1 else (clean[n // 2 - 1] + clean[n // 2]) / 2.0
    mean = sum(clean) / n
    return {
        "count": n,
        "min": round(clean[0], 6),
        "median": round(median, 6),
        "max": round(clean[-1], 6),
        "mean": round(mean, 6),
    }


def row_brief(row: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "symbol": symbol_of(row),
        "setup_id": setup_id_of(row),
        "best_setup_type": setup_type_of(row),
        "decision": decision_of(row),
        "tradeability_class": tradeability_of(row),
        "risk_acceptable": row.get("risk_acceptable"),
        "entry_ready": row.get("entry_ready"),
        "entry_state": entry_state_of(row),
        "global_score": row.get("global_score"),
        "weighted_score": row.get("weighted_score"),
        "final_score": row.get("final_score"),
        "setup_score": row.get("setup_score"),
        "decision_reasons": reasons_of(row),
    }


def compare_published_vs_reconstructed(
    published_rows: List[Dict[str, Any]],
    upstream_rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    deduped = dedup_best_symbol_rows(upstream_rows)
    reconstructed_top20 = deduped[:20]

    published_symbols_ordered = [symbol_of(r) for r in published_rows]
    reconstructed_symbols_ordered = [symbol_of(r) for r in reconstructed_top20]

    published_set = set(published_symbols_ordered)
    reconstructed_set = set(reconstructed_symbols_ordered)

    cutoff_score = preferred_score_proxy(deduped[19]) if len(deduped) >= 20 else None
    near_misses = []
    for row in deduped[20:40]:
        proxy = preferred_score_proxy(row)
        near_misses.append(
            {
                **row_brief(row),
                "score_proxy": proxy,
                "gap_to_cutoff": round(cutoff_score - proxy, 6) if cutoff_score is not None and proxy is not None else None,
                "entry_eligible_tradeability": entry_eligible(row),
            }
        )

    overlap_count = len(published_set & reconstructed_set)
    jaccard = round(overlap_count / len(published_set | reconstructed_set), 4) if (published_set | reconstructed_set) else None

    return {
        "upstream_rows_total": len(upstream_rows),
        "dedup_symbols_total": len(deduped),
        "published_top20_symbols_ordered": published_symbols_ordered,
        "reconstructed_top20_symbols_ordered": reconstructed_symbols_ordered,
        "overlap_count": overlap_count,
        "jaccard_overlap": jaccard,
        "published_not_in_reconstructed_top20": sorted(list(published_set - reconstructed_set)),
        "reconstructed_not_in_published_top20": sorted(list(reconstructed_set - published_set)),
        "cutoff_score_proxy": cutoff_score,
        "published_top20_score_proxy_summary": summarize_numeric(published_rows, "global_score"),
        "reconstructed_top20_score_proxy_summary": {
            "global_score": summarize_numeric(reconstructed_top20, "global_score"),
            "weighted_score": summarize_numeric(reconstructed_top20, "weighted_score"),
            "final_score": summarize_numeric(reconstructed_top20, "final_score"),
            "setup_score": summarize_numeric(reconstructed_top20, "setup_score"),
        },
        "setup_type_distribution": {
            "published_top20": summarize_distribution(published_rows, "setup_type"),
            "reconstructed_top20": summarize_distribution(reconstructed_top20, "setup_type"),
            "dedup_universe": summarize_distribution(deduped, "setup_type"),
        },
        "tradeability_distribution": {
            "published_top20": summarize_distribution(published_rows, "tradeability"),
            "reconstructed_top20": summarize_distribution(reconstructed_top20, "tradeability"),
            "near_misses_21_40": summarize_distribution(near_misses, "tradeability"),
        },
        "risk_ok_counts": {
            "published_top20": sum(1 for r in published_rows if bool_true(r.get("risk_acceptable"))),
            "reconstructed_top20": sum(1 for r in reconstructed_top20 if bool_true(r.get("risk_acceptable"))),
            "near_misses_21_40": sum(1 for r in near_misses if bool_true(r.get("risk_acceptable"))),
        },
        "entry_eligible_counts": {
            "published_top20": sum(1 for r in published_rows if entry_eligible(r)),
            "reconstructed_top20": sum(1 for r in reconstructed_top20 if entry_eligible(r)),
            "near_misses_21_40": sum(1 for r in near_misses if entry_eligible(r)),
        },
        "near_misses_21_40": near_misses,
        "reconstructed_top20_rows": [row_brief(r) for r in reconstructed_top20],
    }


def iter_json_files_in_dir(base_dir: Path) -> Iterable[Path]:
    if not base_dir.exists() or not base_dir.is_dir():
        return []
    return sorted(base_dir.rglob("*.json"))


def eligible_json_path(path: Path) -> bool:
    if any(part in IGNORED_DIR_PARTS for part in path.parts):
        return False
    name = path.name.lower()
    path_str = str(path).lower().replace("\\", "/")
    if "/reports/analysis/" in path_str:
        return False
    if name.endswith(".manifest.json"):
        return False
    if "counterfactual" in name or "diagnose_rr" in name or "chased_entry_analysis" in name:
        return False
    if "post_risk_unlock_audit" in name or "top20_formation_audit" in name or "pre_top20_inclusion_audit" in name:
        return False
    return True


def discover_upstream_json_candidates(root: Path, exclude_paths: List[Path], min_len: int) -> List[Dict[str, Any]]:
    findings: List[Dict[str, Any]] = []
    exclude_set = {p.resolve() for p in exclude_paths}

    searched_paths: List[Tuple[str, List[Path]]] = [
        ("snapshots/runtime", [p for p in iter_json_files_in_dir(root / "snapshots" / "runtime")]),
        ("snapshots/history", [p for p in iter_json_files_in_dir(root / "snapshots" / "history")]),
        ("snapshots/raw", [p for p in iter_json_files_in_dir(root / "snapshots" / "raw")]),
    ]

    already_seen = set()
    for bucket, paths in searched_paths:
        for path in paths:
            if not eligible_json_path(path):
                continue
            if path.resolve() in exclude_set:
                continue
            already_seen.add(path.resolve())

            data = safe_load_json(path)
            if data is None:
                continue
            arrays = detect_candidate_arrays(data, min_len=min_len)
            best = choose_best_candidate_array(arrays)
            if best is None:
                continue

            findings.append(
                {
                    "path": path,
                    "source_bucket": bucket,
                    "array_path": best["path"],
                    "array_length": best["length"],
                    "sample_keys": best["sample_keys"],
                    "rows": best["rows"],
                }
            )

    for path in root.rglob("*.json"):
        if path.resolve() in already_seen:
            continue
        if path.resolve() in exclude_set:
            continue
        if not eligible_json_path(path):
            continue

        data = safe_load_json(path)
        if data is None:
            continue
        arrays = detect_candidate_arrays(data, min_len=min_len)
        best = choose_best_candidate_array(arrays)
        if best is None:
            continue

        findings.append(
            {
                "path": path,
                "source_bucket": classify_source_bucket(path, root),
                "array_path": best["path"],
                "array_length": best["length"],
                "sample_keys": best["sample_keys"],
                "rows": best["rows"],
            }
        )

    findings.sort(
        key=lambda x: (
            source_bucket_rank(x["source_bucket"]),
            -x["array_length"],
            str(x["path"]),
        )
    )
    return findings


def resolve_inputs(args: argparse.Namespace) -> Tuple[RunRecord, Optional[Dict[str, Any]]]:
    root = repo_root()

    if args.run_json:
        run = parse_run_json(Path(args.run_json))
        if run is None:
            raise SystemExit(f"--run-json is not a canonical run JSON: {args.run_json}")
    else:
        runs = [parse_run_json(p) for p in discover_run_files(root)]
        runs = [r for r in runs if r is not None]
        runs = sort_runs_desc(runs)
        if not runs:
            raise SystemExit("No canonical run JSON files with trade_candidates were found.")
        run = runs[0]

    upstream_candidate = None

    if args.upstream_json:
        path = Path(args.upstream_json)
        data = safe_load_json(path)
        if data is None:
            raise SystemExit(f"Could not load --upstream-json: {args.upstream_json}")
        arrays = detect_candidate_arrays(data, min_len=max(21, len(run.trade_candidates) + 1))
        best = choose_best_candidate_array(arrays)
        if best is None:
            raise SystemExit(f"No suitable larger candidate array found in {args.upstream_json}")
        upstream_candidate = {
            "source_file": str(path),
            "source_bucket": classify_source_bucket(path, root),
            "array_path": best["path"],
            "array_length": best["length"],
            "sample_keys": best["sample_keys"],
            "rows": best["rows"],
        }
    else:
        nearby = discover_upstream_json_candidates(
            root=root,
            exclude_paths=[run.path],
            min_len=max(21, len(run.trade_candidates) + 1),
        )
        if nearby:
            best = nearby[0]
            upstream_candidate = {
                "source_file": str(best["path"]),
                "source_bucket": best["source_bucket"],
                "array_path": best["array_path"],
                "array_length": best["array_length"],
                "sample_keys": best["sample_keys"],
                "rows": best["rows"],
            }

    return run, upstream_candidate


def build_missing_snapshot_guidance() -> Dict[str, Any]:
    return {
        "status": "missing_upstream_candidate_array",
        "message": (
            "No larger pre-Top20 candidate array was found in snapshots/runtime, snapshots/history, snapshots/raw, "
            "or other repo JSONs. A full inclusion audit requires a snapshot JSON with a list of candidate rows "
            "BEFORE final Top20 cap."
        ),
        "search_order_used": SNAPSHOT_PRIORITY,
        "required_minimum_fields_per_row": [
            "symbol",
            "setup_id",
            "best_setup_type or setup_type",
            "global_score",
        ],
        "preferred_additional_fields": [
            "weighted_score",
            "final_score",
            "setup_score",
            "tradeability_class",
            "risk_acceptable",
            "entry_ready",
            "entry_state",
            "decision",
            "decision_reasons",
        ],
        "preferred_snapshot_semantics": [
            "one row per setup candidate before final symbol dedup OR after symbol dedup but before top20 cap",
            "same run_id/asof as the published run JSON",
            "stable score fields from the ranking stage",
        ],
        "next_best_place_to_snapshot": [
            "snapshots/runtime",
            "snapshots/history",
        ],
    }


def render_md_counter(counter: Dict[str, Any]) -> str:
    if not counter:
        return "- none"
    return "\n".join(f"- `{k}`: {v}" for k, v in counter.items())


def render_md_rows(rows: List[Dict[str, Any]], limit: int = 20) -> str:
    if not rows:
        return "_none_"
    show = rows[:limit]
    header = (
        "| symbol | setup_id | setup | decision | tradeability | risk_ok | entry_ready | entry_state | global_score | reasons |\n"
        "|---|---|---|---|---|---:|---:|---|---:|---|"
    )
    lines = [header]
    for row in show:
        lines.append(
            "| {symbol} | {setup_id} | {best_setup_type} | {decision} | {tradeability_class} | {risk_acceptable} | {entry_ready} | {entry_state} | {global_score} | {reasons} |".format(
                symbol=row.get("symbol"),
                setup_id=row.get("setup_id"),
                best_setup_type=row.get("best_setup_type"),
                decision=row.get("decision"),
                tradeability_class=row.get("tradeability_class"),
                risk_acceptable=row.get("risk_acceptable"),
                entry_ready=row.get("entry_ready"),
                entry_state=row.get("entry_state"),
                global_score=row.get("global_score"),
                reasons=", ".join(row.get("decision_reasons", [])),
            )
        )
    return "\n".join(lines)


def render_markdown(payload: Dict[str, Any]) -> str:
    lines: List[str] = []
    lines.append("# Pre-Top20 Inclusion Audit")
    lines.append("")
    lines.append(f"- Generated at UTC: `{payload['generated_at_utc']}`")
    lines.append(f"- Run ID: `{payload['run']['run_id']}`")
    lines.append(f"- Run file: `{payload['run']['source_file']}`")
    lines.append("")

    lines.append("## Published Top20")
    lines.append(render_md_counter(payload["published_top20_summary"]))
    lines.append("")

    if payload["upstream_candidate_source"] is None:
        lines.append("## Upstream candidate source")
        lines.append("_No larger upstream candidate array found._")
        lines.append("")
        lines.append("## Missing-snapshot guidance")
        lines.append(render_md_counter(payload["missing_snapshot_guidance"]))
        lines.append("")
        lines.append("## Published Top20 rows")
        lines.append(render_md_rows(payload["published_top20_rows"]))
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    lines.append("## Upstream candidate source")
    lines.append(render_md_counter(payload["upstream_candidate_source"]))
    lines.append("")
    lines.append("## Inclusion comparison")
    lines.append(render_md_counter(payload["comparison_summary"]))
    lines.append("")
    lines.append("## Published vs reconstructed setup distributions")
    lines.append(render_md_counter(payload["comparison"]["setup_type_distribution"]))
    lines.append("")
    lines.append("## Published vs reconstructed tradeability distributions")
    lines.append(render_md_counter(payload["comparison"]["tradeability_distribution"]))
    lines.append("")
    lines.append("## Near misses 21-40")
    lines.append(render_md_rows(payload["comparison"]["near_misses_21_40"], limit=20))
    lines.append("")
    lines.append("## Reconstructed Top20")
    lines.append(render_md_rows(payload["comparison"]["reconstructed_top20_rows"], limit=20))
    lines.append("")
    lines.append("## Published Top20 rows")
    lines.append(render_md_rows(payload["published_top20_rows"], limit=20))
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-Top20 inclusion audit")
    parser.add_argument("--run-json", type=str, default=None, help="Explicit canonical run JSON path")
    parser.add_argument("--upstream-json", type=str, default=None, help="Explicit upstream snapshot/JSON path")
    args = parser.parse_args()

    run, upstream = resolve_inputs(args)

    published_rows = list(run.trade_candidates)
    published_summary = {
        "top20_size": len(published_rows),
        "decision_distribution": summarize_distribution(published_rows, "decision"),
        "setup_type_distribution": summarize_distribution(published_rows, "setup_type"),
        "tradeability_distribution": summarize_distribution(published_rows, "tradeability"),
        "entry_state_distribution": summarize_distribution(published_rows, "entry_state"),
        "risk_ok_count": sum(1 for r in published_rows if bool_true(r.get("risk_acceptable"))),
        "entry_eligible_count": sum(1 for r in published_rows if entry_eligible(r)),
        "global_score_summary": summarize_numeric(published_rows, "global_score"),
    }

    payload: Dict[str, Any] = {
        "analysis_name": "pre_top20_inclusion_audit",
        "generated_at_utc": utc_now_iso(),
        "run": {
            "run_id": run.run_id,
            "timestamp_utc": run.timestamp_utc,
            "canonical_schema_version": run.canonical_schema_version,
            "source_file": str(run.path.relative_to(repo_root())),
        },
        "published_top20_summary": published_summary,
        "published_top20_rows": [row_brief(r) for r in published_rows],
        "upstream_candidate_source": None,
        "comparison_summary": None,
        "comparison": None,
        "missing_snapshot_guidance": None,
    }

    if upstream is None:
        payload["missing_snapshot_guidance"] = build_missing_snapshot_guidance()
    else:
        payload["upstream_candidate_source"] = {
            "source_file": upstream["source_file"],
            "source_bucket": upstream["source_bucket"],
            "search_priority_order": SNAPSHOT_PRIORITY,
            "array_path": upstream["array_path"],
            "array_length": upstream["array_length"],
            "sample_keys": upstream["sample_keys"],
        }
        comparison = compare_published_vs_reconstructed(
            published_rows=published_rows,
            upstream_rows=upstream["rows"],
        )
        payload["comparison"] = comparison
        payload["comparison_summary"] = {
            "upstream_rows_total": comparison["upstream_rows_total"],
            "dedup_symbols_total": comparison["dedup_symbols_total"],
            "overlap_count": comparison["overlap_count"],
            "jaccard_overlap": comparison["jaccard_overlap"],
            "published_not_in_reconstructed_top20_count": len(comparison["published_not_in_reconstructed_top20"]),
            "reconstructed_not_in_published_top20_count": len(comparison["reconstructed_not_in_published_top20"]),
            "published_not_in_reconstructed_top20": comparison["published_not_in_reconstructed_top20"],
            "reconstructed_not_in_published_top20": comparison["reconstructed_not_in_published_top20"],
            "cutoff_score_proxy": comparison["cutoff_score_proxy"],
            "published_risk_ok_count": comparison["risk_ok_counts"]["published_top20"],
            "reconstructed_risk_ok_count": comparison["risk_ok_counts"]["reconstructed_top20"],
            "near_misses_risk_ok_count": comparison["risk_ok_counts"]["near_misses_21_40"],
            "published_entry_eligible_count": comparison["entry_eligible_counts"]["published_top20"],
            "reconstructed_entry_eligible_count": comparison["entry_eligible_counts"]["reconstructed_top20"],
            "near_misses_entry_eligible_count": comparison["entry_eligible_counts"]["near_misses_21_40"],
        }

    slug = utc_now_slug()
    out_dir = analysis_dir()
    json_path = out_dir / f"pre_top20_inclusion_audit_{slug}.json"
    md_path = out_dir / f"pre_top20_inclusion_audit_{slug}.md"

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    with md_path.open("w", encoding="utf-8") as f:
        f.write(render_markdown(payload))

    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
