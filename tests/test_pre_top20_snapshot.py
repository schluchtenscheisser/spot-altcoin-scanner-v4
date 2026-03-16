import json
from pathlib import Path

import pytest

from scanner.pipeline.global_ranking import compute_global_ranked_candidates, compute_global_top20
from scanner.pipeline.pre_top20_snapshot import (
    RANKING_STAGE,
    SORT_KEY_DESCRIPTION,
    build_pre_top20_snapshot_payload,
    write_pre_top20_snapshot,
)


def test_pre_top20_payload_meta_and_cutoff_for_less_than_20() -> None:
    payload = build_pre_top20_snapshot_payload(
        run_id="2026-03-16_123",
        run_date="2026-03-16",
        asof_ts_ms=123,
        ranked_candidates=[{"symbol": "AAAUSDT", "global_score": 1.0, "best_setup_type": "breakout"}],
    )

    assert payload["meta"]["ranking_stage"] == RANKING_STAGE
    assert payload["meta"]["sort_key_description"] == SORT_KEY_DESCRIPTION
    assert payload["meta"]["total_candidates"] == 1
    assert payload["meta"]["top20_cutoff_global_score"] is None
    assert payload["candidates"][0]["rank"] == 1


def test_pre_top20_payload_empty_candidates() -> None:
    payload = build_pre_top20_snapshot_payload(
        run_id="run",
        run_date="2026-03-16",
        asof_ts_ms=1,
        ranked_candidates=[],
    )

    assert payload["meta"]["total_candidates"] == 0
    assert payload["meta"]["top20_cutoff_global_score"] is None
    assert payload["candidates"] == []


def test_pre_top20_payload_nonfinite_numeric_serialized_as_null() -> None:
    payload = build_pre_top20_snapshot_payload(
        run_id="run",
        run_date="2026-03-16",
        asof_ts_ms=1,
        ranked_candidates=[
            {
                "symbol": "AAAUSDT",
                "best_setup_type": "breakout",
                "global_score": float("nan"),
                "setup_score": float("inf"),
                "risk_pct_to_stop": float("-inf"),
                "distance_to_entry_pct": 1.2,
            }
        ],
    )
    row = payload["candidates"][0]
    assert row["global_score"] is None
    assert row["setup_score"] is None
    assert row["risk_pct_to_stop"] is None
    assert row["distance_to_entry_pct"] == 1.2


def test_pre_top20_payload_preserves_nullable_fields() -> None:
    payload = build_pre_top20_snapshot_payload(
        run_id="run",
        run_date="2026-03-16",
        asof_ts_ms=1,
        ranked_candidates=[
            {
                "symbol": "AAAUSDT",
                "best_setup_type": "reversal",
                "risk_acceptable": None,
                "decision": None,
                "decision_reasons": None,
            }
        ],
    )
    row = payload["candidates"][0]
    assert row["risk_acceptable"] is None
    assert row["decision"] is None
    assert row["decision_reasons"] is None


def test_pre_top20_snapshot_overwrite_is_deterministic(tmp_path: Path) -> None:
    payload = build_pre_top20_snapshot_payload(
        run_id="run",
        run_date="2026-03-16",
        asof_ts_ms=1,
        ranked_candidates=[{"symbol": "AAAUSDT", "global_score": 5.0, "best_setup_type": "breakout"}],
    )

    path = write_pre_top20_snapshot(payload=payload, run_id="run", runtime_dir=tmp_path)
    first = path.read_bytes()
    write_pre_top20_snapshot(payload=payload, run_id="run", runtime_dir=tmp_path)
    second = path.read_bytes()

    assert first == second


def test_pre_top20_snapshot_atomic_write_failure_leaves_no_partial(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    payload = build_pre_top20_snapshot_payload(
        run_id="run",
        run_date="2026-03-16",
        asof_ts_ms=1,
        ranked_candidates=[{"symbol": "AAAUSDT", "global_score": 5.0, "best_setup_type": "breakout"}],
    )

    original = Path.write_text

    def fail_once(self: Path, *args, **kwargs):
        raise OSError("disk full")

    monkeypatch.setattr(Path, "write_text", fail_once)
    with pytest.raises(OSError):
        write_pre_top20_snapshot(payload=payload, run_id="run", runtime_dir=tmp_path)

    assert not (tmp_path / "run_pre_top20.json").exists()
    assert not (tmp_path / "run_pre_top20.json.tmp").exists()
    monkeypatch.setattr(Path, "write_text", original)


def test_first_20_pre_top20_candidates_match_global_top20_symbols() -> None:
    rows = [{"symbol": f"S{i:03d}USDT", "score": 100.0 - i, "final_score": 100.0 - i, "setup_id": "breakout_immediate_1_5d"} for i in range(30)]
    ranked = compute_global_ranked_candidates([], rows, [], {})
    top20 = compute_global_top20([], rows, [], {})

    payload = build_pre_top20_snapshot_payload(
        run_id="run",
        run_date="2026-03-16",
        asof_ts_ms=1,
        ranked_candidates=ranked,
    )

    assert [row["symbol"] for row in payload["candidates"][:20]] == [row["symbol"] for row in top20]
    assert payload["meta"]["top20_cutoff_global_score"] == payload["candidates"][19]["global_score"]


def test_pre_top20_snapshot_written_json_loads(tmp_path: Path) -> None:
    payload = build_pre_top20_snapshot_payload(
        run_id="run",
        run_date="2026-03-16",
        asof_ts_ms=1,
        ranked_candidates=[{"symbol": "AAAUSDT", "global_score": 5.0, "best_setup_type": "breakout"}],
    )
    path = write_pre_top20_snapshot(payload=payload, run_id="run", runtime_dir=tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["meta"]["run_id"] == "run"
