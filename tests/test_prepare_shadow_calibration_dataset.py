from __future__ import annotations

import json
import math
from pathlib import Path

from scanner.tools import prepare_shadow_calibration_dataset as prep


def _write_eval(path: Path, *, rows: list[dict]) -> None:
    payload = [
        {
            "type": "meta",
            "run_id": "RID",
        },
        *rows,
    ]
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in payload) + "\n", encoding="utf-8")


def _candidate(
    *,
    record_id: str,
    symbol: str,
    setup_rank: int,
    hit10_5d: bool | None,
    hit20_5d: bool | None,
    score: float = 55.5,
    mfe_5d_pct: float | None = 7.0,
) -> dict:
    return {
        "type": "candidate_setup",
        "record_id": record_id,
        "run_id": "RID",
        "t0_date": "2026-02-01",
        "symbol": symbol,
        "setup_type": "breakout",
        "setup_rank": setup_rank,
        "score": score,
        "global_rank": None,
        "hit10_5d": hit10_5d,
        "hit20_5d": hit20_5d,
        "mfe_5d_pct": mfe_5d_pct,
        "mae_5d_pct": -2.0,
    }


def test_shadow_prep_ready_and_deterministic(tmp_path: Path) -> None:
    input_path = tmp_path / "eval.jsonl"
    output_path = tmp_path / "shadow.json"
    _write_eval(
        input_path,
        rows=[
            _candidate(record_id="RID:1", symbol="ZEDUSDT", setup_rank=2, hit10_5d=True, hit20_5d=False),
            _candidate(record_id="RID:2", symbol="ABCUSDT", setup_rank=1, hit10_5d=False, hit20_5d=False),
        ],
    )

    first = prep.prepare_shadow_dataset(input_path=input_path, output_path=output_path, min_labeled_rows=2)
    second = prep.prepare_shadow_dataset(input_path=input_path, output_path=output_path, min_labeled_rows=2)

    assert first == second
    assert first["dataset_status"] == "ready"
    assert [row["symbol"] for row in first["rows"]] == ["ABCUSDT", "ZEDUSDT"]
    assert first["counts"] == {
        "source_candidate_rows": 2,
        "prepared_rows": 2,
        "labeled_rows": 2,
        "not_evaluable_rows": 0,
        "excluded_invalid_rows": 0,
    }


def test_shadow_prep_marks_insufficient_data_without_coercing_labels(tmp_path: Path) -> None:
    input_path = tmp_path / "eval.jsonl"
    output_path = tmp_path / "shadow.json"
    _write_eval(
        input_path,
        rows=[
            _candidate(record_id="RID:1", symbol="AAAUSDT", setup_rank=1, hit10_5d=None, hit20_5d=None),
        ],
    )

    artifact = prep.prepare_shadow_dataset(input_path=input_path, output_path=output_path, min_labeled_rows=1)

    assert artifact["dataset_status"] == "insufficient_labeled_rows"
    assert artifact["counts"]["labeled_rows"] == 0
    assert artifact["counts"]["not_evaluable_rows"] == 1
    assert artifact["rows"][0]["label_status"] == "not_evaluable"
    assert artifact["rows"][0]["hit10_5d"] is None


def test_shadow_prep_excludes_non_finite_rows_explicitly(tmp_path: Path) -> None:
    input_path = tmp_path / "eval.jsonl"
    output_path = tmp_path / "shadow.json"
    _write_eval(
        input_path,
        rows=[
            _candidate(record_id="RID:1", symbol="OKUSDT", setup_rank=1, hit10_5d=True, hit20_5d=True),
            _candidate(
                record_id="RID:2",
                symbol="BADUSDT",
                setup_rank=2,
                hit10_5d=True,
                hit20_5d=False,
                score=math.inf,
            ),
        ],
    )

    artifact = prep.prepare_shadow_dataset(input_path=input_path, output_path=output_path, min_labeled_rows=1)

    assert artifact["counts"]["excluded_invalid_rows"] == 1
    assert artifact["counts"]["prepared_rows"] == 1
    assert [row["symbol"] for row in artifact["rows"]] == ["OKUSDT"]


def test_shadow_prep_invalid_cli_argument_fails() -> None:
    rc = prep.main(["--input", "missing.jsonl", "--output", "out.json", "--min-labeled-rows", "0"])
    assert rc == 1
