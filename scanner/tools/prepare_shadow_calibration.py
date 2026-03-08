from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REQUIRED_LABEL_FIELDS = ("hit10_5d", "hit20_5d", "mfe_5d_pct", "mae_5d_pct")


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _utc_iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for line_no, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        payload = json.loads(line)
        if not isinstance(payload, dict):
            raise ValueError(f"Invalid JSON object at line {line_no}")
        rows.append(payload)
    if not rows:
        raise ValueError("Evaluation dataset is empty")
    return rows


def _is_finite_or_none(value: Any) -> bool:
    if value is None:
        return True
    if isinstance(value, bool):
        return True
    if isinstance(value, (int, float)):
        return math.isfinite(float(value))
    return False


def _bool_or_none(value: Any) -> bool:
    return value is None or isinstance(value, bool)


def build_shadow_calibration_prep_report(rows: list[dict[str, Any]], *, report_id: str) -> dict[str, Any]:
    meta = rows[0]
    if meta.get("type") != "meta":
        raise ValueError("First JSONL row must be meta")

    candidates = [row for row in rows[1:] if row.get("type") == "candidate_setup"]
    if not candidates:
        raise ValueError("No candidate_setup rows present")

    invalid_rows: list[dict[str, Any]] = []
    for row in candidates:
        missing = [field for field in REQUIRED_LABEL_FIELDS if field not in row]
        if missing:
            invalid_rows.append({"record_id": row.get("record_id"), "error": f"missing_fields:{','.join(missing)}"})
            continue

        if not _bool_or_none(row.get("hit10_5d")) or not _bool_or_none(row.get("hit20_5d")):
            invalid_rows.append({"record_id": row.get("record_id"), "error": "invalid_boolean_label"})
            continue

        non_finite_fields = [
            field for field in ("mfe_5d_pct", "mae_5d_pct", "score") if not _is_finite_or_none(row.get(field))
        ]
        if non_finite_fields:
            invalid_rows.append(
                {"record_id": row.get("record_id"), "error": f"non_finite:{','.join(non_finite_fields)}"}
            )

    evaluable = [row for row in candidates if isinstance(row.get("hit10_5d"), bool) and isinstance(row.get("hit20_5d"), bool)]

    by_setup: dict[str, dict[str, int]] = {}
    for setup in sorted({str(row.get("setup_type")) for row in candidates}):
        rows_for_setup = [row for row in candidates if row.get("setup_type") == setup]
        by_setup[setup] = {
            "rows": len(rows_for_setup),
            "evaluable_rows": sum(
                1
                for row in rows_for_setup
                if isinstance(row.get("hit10_5d"), bool) and isinstance(row.get("hit20_5d"), bool)
            ),
        }

    return {
        "type": "shadow_calibration_prep_report",
        "report_id": report_id,
        "generated_at_iso": _utc_iso(_utc_now()),
        "source_run_id": meta.get("run_id"),
        "source_dataset_schema_version": meta.get("dataset_schema_version"),
        "summary": {
            "candidate_rows": len(candidates),
            "evaluable_rows": len(evaluable),
            "not_evaluable_rows": len(candidates) - len(evaluable),
            "invalid_rows": len(invalid_rows),
            "invalid_ratio": round(len(invalid_rows) / len(candidates), 6),
        },
        "setup_type_summary": by_setup,
        "invalid_examples": sorted(invalid_rows, key=lambda row: (str(row.get("record_id")), str(row.get("error"))))[:20],
        "calibration_state": {
            "active": False,
            "threshold_adjustment": None,
            "notes": "Preparation only. No productive threshold changes are applied.",
        },
    }


def _write_json_atomic(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    tmp_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp_path.replace(path)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Build a shadow-calibration preparation report from evaluation JSONL")
    parser.add_argument("--eval-dataset", required=True, help="Path to eval_*.jsonl")
    parser.add_argument("--output-dir", default="artifacts/shadow_calibration", help="Report output directory")
    parser.add_argument("--report-id", default=None, help="Optional deterministic report id")
    parser.add_argument("--strict", action="store_true", help="Fail if invalid rows are detected; no output is written")
    return parser


def run(args: argparse.Namespace) -> Path:
    rows = _load_jsonl(Path(args.eval_dataset))
    generated_at = _utc_now()
    report_id = args.report_id or generated_at.strftime("%Y-%m-%d_%H%M%SZ")

    report = build_shadow_calibration_prep_report(rows, report_id=report_id)
    if args.strict and int(report["summary"]["invalid_rows"]) > 0:
        raise ValueError("Invalid rows detected in strict mode")

    output_path = Path(args.output_dir) / f"shadow_calibration_prep_{report_id}.json"
    _write_json_atomic(output_path, report)
    return output_path


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        out = run(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print(str(out))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
