from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

SHADOW_PREP_SCHEMA_VERSION = "1.0"


class InvalidRowError(ValueError):
    pass


def _read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError("JSONL rows must be JSON objects")
        rows.append(payload)
    if not rows:
        raise ValueError("Input dataset is empty")
    return rows


def _as_finite_or_none(value: Any, field_name: str) -> float | None:
    if value is None:
        return None
    numeric = float(value)
    if not math.isfinite(numeric):
        raise InvalidRowError(f"{field_name} must be finite when present")
    return numeric


def _as_nullable_bool(value: Any, field_name: str) -> bool | None:
    if value is None:
        return None
    if isinstance(value, bool):
        return value
    raise InvalidRowError(f"{field_name} must be bool|null")


def _prepare_candidate_row(row: dict[str, Any]) -> dict[str, Any]:
    required = ["record_id", "run_id", "t0_date", "symbol", "setup_type", "setup_rank", "score"]
    for key in required:
        if key not in row or row.get(key) is None:
            raise InvalidRowError(f"Missing non-nullable candidate field: {key}")

    score = _as_finite_or_none(row.get("score"), "score")
    if score is None:
        raise InvalidRowError("score must be finite")

    hit10 = _as_nullable_bool(row.get("hit10_5d"), "hit10_5d")
    hit20 = _as_nullable_bool(row.get("hit20_5d"), "hit20_5d")

    prepared = {
        "record_id": str(row["record_id"]),
        "run_id": str(row["run_id"]),
        "t0_date": str(row["t0_date"]),
        "symbol": str(row["symbol"]),
        "setup_type": str(row["setup_type"]),
        "setup_rank": int(row["setup_rank"]),
        "score": score,
        "global_rank": int(row["global_rank"]) if row.get("global_rank") is not None else None,
        "hit10_5d": hit10,
        "hit20_5d": hit20,
        "mfe_5d_pct": _as_finite_or_none(row.get("mfe_5d_pct"), "mfe_5d_pct"),
        "mae_5d_pct": _as_finite_or_none(row.get("mae_5d_pct"), "mae_5d_pct"),
        "label_status": "labeled" if hit10 is not None and hit20 is not None else "not_evaluable",
    }
    return prepared


def prepare_shadow_dataset(*, input_path: Path, output_path: Path, min_labeled_rows: int) -> dict[str, Any]:
    if min_labeled_rows < 1:
        raise ValueError("min_labeled_rows must be >= 1")

    rows = _read_jsonl(input_path)
    meta = rows[0]
    if meta.get("type") != "meta":
        raise ValueError("First JSONL row must be meta")

    prepared_rows: list[dict[str, Any]] = []
    excluded_invalid = 0

    for row in rows[1:]:
        if row.get("type") != "candidate_setup":
            continue
        try:
            prepared_rows.append(_prepare_candidate_row(row))
        except InvalidRowError:
            excluded_invalid += 1

    prepared_rows.sort(
        key=lambda r: (r["t0_date"], r["setup_type"], r["setup_rank"], r["symbol"], r["record_id"])
    )

    labeled_rows = [r for r in prepared_rows if r["label_status"] == "labeled"]
    dataset_status = "ready" if len(labeled_rows) >= min_labeled_rows else "insufficient_labeled_rows"

    artifact = {
        "type": "shadow_calibration_prep",
        "shadow_prep_schema_version": SHADOW_PREP_SCHEMA_VERSION,
        "source_eval_path": str(input_path),
        "source_run_id": meta.get("run_id"),
        "min_labeled_rows": min_labeled_rows,
        "dataset_status": dataset_status,
        "counts": {
            "source_candidate_rows": sum(1 for row in rows[1:] if row.get("type") == "candidate_setup"),
            "prepared_rows": len(prepared_rows),
            "labeled_rows": len(labeled_rows),
            "not_evaluable_rows": len(prepared_rows) - len(labeled_rows),
            "excluded_invalid_rows": excluded_invalid,
        },
        "rows": prepared_rows,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(artifact, ensure_ascii=False, sort_keys=True) + "\n", encoding="utf-8")
    return artifact


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Prepare shadow-calibration input artifact from evaluation dataset JSONL")
    parser.add_argument("--input", required=True, help="Path to eval_*.jsonl")
    parser.add_argument("--output", required=True, help="Path to output JSON")
    parser.add_argument("--min-labeled-rows", type=int, default=30, help="Minimum labeled rows for ready status")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        artifact = prepare_shadow_dataset(
            input_path=Path(args.input),
            output_path=Path(args.output),
            min_labeled_rows=int(args.min_labeled_rows),
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(json.dumps({"output": str(args.output), "dataset_status": artifact["dataset_status"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
