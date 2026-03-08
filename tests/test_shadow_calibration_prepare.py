from __future__ import annotations

import json
from pathlib import Path

from scanner.tools import prepare_shadow_calibration as prep


def _write_eval_jsonl(path: Path, candidate_rows: list[dict]) -> Path:
    rows = [
        {
            "type": "meta",
            "run_id": "RID",
            "dataset_schema_version": "1.3",
        },
        *candidate_rows,
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    return path


def test_prepare_report_is_deterministic_and_keeps_calibration_inactive(tmp_path: Path, monkeypatch) -> None:
    dataset = _write_eval_jsonl(
        tmp_path / "eval.jsonl",
        [
            {
                "type": "candidate_setup",
                "record_id": "RID:2026-02-01:A:breakout:s1",
                "setup_type": "breakout",
                "score": 70.0,
                "hit10_5d": True,
                "hit20_5d": False,
                "mfe_5d_pct": 11.0,
                "mae_5d_pct": -3.0,
            },
            {
                "type": "candidate_setup",
                "record_id": "RID:2026-02-01:B:pullback:s2",
                "setup_type": "pullback",
                "score": 40.0,
                "hit10_5d": None,
                "hit20_5d": None,
                "mfe_5d_pct": None,
                "mae_5d_pct": None,
            },
        ],
    )

    monkeypatch.setattr(prep, "_utc_now", lambda: prep.datetime(2026, 3, 8, 1, 2, 3, tzinfo=prep.timezone.utc))
    first = prep.run(prep.build_parser().parse_args(["--eval-dataset", str(dataset), "--output-dir", str(tmp_path), "--report-id", "R1"]))
    second = prep.run(prep.build_parser().parse_args(["--eval-dataset", str(dataset), "--output-dir", str(tmp_path), "--report-id", "R1"]))

    first_payload = json.loads(first.read_text(encoding="utf-8"))
    second_payload = json.loads(second.read_text(encoding="utf-8"))
    assert first_payload == second_payload
    assert first_payload["summary"] == {
        "candidate_rows": 2,
        "evaluable_rows": 1,
        "not_evaluable_rows": 1,
        "invalid_rows": 0,
        "invalid_ratio": 0.0,
    }
    assert first_payload["calibration_state"]["active"] is False
    assert first_payload["calibration_state"]["threshold_adjustment"] is None


def test_prepare_report_flags_non_finite_values_explicitly(tmp_path: Path) -> None:
    dataset = _write_eval_jsonl(
        tmp_path / "eval.jsonl",
        [
            {
                "type": "candidate_setup",
                "record_id": "RID:2026-02-01:X:reversal:s1",
                "setup_type": "reversal",
                "score": float("inf"),
                "hit10_5d": True,
                "hit20_5d": True,
                "mfe_5d_pct": 22.0,
                "mae_5d_pct": -4.0,
            }
        ],
    )

    out = prep.run(prep.build_parser().parse_args(["--eval-dataset", str(dataset), "--output-dir", str(tmp_path), "--report-id", "R2"]))
    payload = json.loads(out.read_text(encoding="utf-8"))

    assert payload["summary"]["invalid_rows"] == 1
    assert payload["invalid_examples"][0]["error"] == "non_finite:score"


def test_prepare_strict_mode_has_no_partial_write_on_invalid_rows(tmp_path: Path) -> None:
    dataset = _write_eval_jsonl(
        tmp_path / "eval.jsonl",
        [
            {
                "type": "candidate_setup",
                "record_id": "RID:2026-02-01:X:reversal:s1",
                "setup_type": "reversal",
                "score": 50.0,
                "hit10_5d": "yes",
                "hit20_5d": False,
                "mfe_5d_pct": 1.0,
                "mae_5d_pct": -1.0,
            }
        ],
    )

    report_path = tmp_path / "shadow_calibration_prep_R3.json"
    rc = prep.main([
        "--eval-dataset",
        str(dataset),
        "--output-dir",
        str(tmp_path),
        "--report-id",
        "R3",
        "--strict",
    ])

    assert rc == 1
    assert not report_path.exists()


def test_prepare_requires_candidate_rows(tmp_path: Path) -> None:
    dataset = _write_eval_jsonl(tmp_path / "eval.jsonl", [])

    rc = prep.main([
        "--eval-dataset",
        str(dataset),
        "--output-dir",
        str(tmp_path),
    ])

    assert rc == 1
