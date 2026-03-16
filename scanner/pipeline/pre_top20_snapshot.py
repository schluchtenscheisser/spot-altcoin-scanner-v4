"""Pre-Top20 runtime snapshot writer for inclusion audits."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any, Dict, List


RANKING_STAGE = "post_symbol_dedup_pre_top20_cap"
SORT_KEY_DESCRIPTION = "global_score desc, slippage_bps asc (None last), proxy_liquidity_score desc, symbol asc"


def _sanitize_json_value(value: Any) -> Any:
    if isinstance(value, float):
        return value if math.isfinite(value) else None
    if isinstance(value, dict):
        return {str(key): _sanitize_json_value(inner) for key, inner in value.items()}
    if isinstance(value, list):
        return [_sanitize_json_value(item) for item in value]
    return value


def _extract_candidate_row(row: Dict[str, Any], rank: int) -> Dict[str, Any]:
    payload = {
        "rank": rank,
        "symbol": row.get("symbol"),
        "best_setup_type": row.get("best_setup_type"),
        "setup_subtype": row.get("setup_subtype"),
        "setup_score": row.get("setup_score", row.get("score")),
        "global_score": row.get("global_score", row.get("score")),
        "tradeability_class": row.get("tradeability_class"),
        "risk_acceptable": row.get("risk_acceptable"),
        "entry_ready": row.get("entry_ready"),
        "entry_state": row.get("entry_state"),
        "decision": row.get("decision"),
        "decision_reasons": row.get("decision_reasons"),
        "risk_pct_to_stop": row.get("risk_pct_to_stop"),
        "distance_to_entry_pct": row.get("distance_to_entry_pct"),
    }
    return _sanitize_json_value(payload)


def build_pre_top20_snapshot_payload(
    *,
    run_id: str,
    run_date: str,
    asof_ts_ms: int | None,
    ranked_candidates: List[Dict[str, Any]],
) -> Dict[str, Any]:
    candidates = [_extract_candidate_row(row, idx) for idx, row in enumerate(ranked_candidates, start=1)]
    cutoff_score = candidates[19]["global_score"] if len(candidates) >= 20 else None
    return {
        "meta": {
            "run_id": run_id,
            "run_date": run_date,
            "asof_ts_ms": asof_ts_ms,
            "ranking_stage": RANKING_STAGE,
            "sort_key_description": SORT_KEY_DESCRIPTION,
            "total_candidates": len(candidates),
            "top20_cutoff_index": 20,
            "top20_cutoff_global_score": cutoff_score,
        },
        "candidates": candidates,
    }


def resolve_runtime_dir(config: Dict[str, Any]) -> Path:
    root = config.raw if hasattr(config, "raw") else config
    snapshots_cfg = root.get("snapshots", {}) if isinstance(root, dict) else {}
    return Path(snapshots_cfg.get("runtime_dir", "snapshots/runtime"))


def write_pre_top20_snapshot(*, payload: Dict[str, Any], run_id: str, runtime_dir: Path) -> Path:
    runtime_dir.mkdir(parents=True, exist_ok=True)
    target_path = runtime_dir / f"{run_id}_pre_top20.json"
    tmp_path = target_path.with_suffix(target_path.suffix + ".tmp")
    try:
        tmp_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
        tmp_path.replace(target_path)
    except Exception:
        if tmp_path.exists():
            tmp_path.unlink()
        raise
    return target_path
