import pytest

from scanner.pipeline.output import ReportGenerator


def _row(symbol: str, **kwargs):
    row = {
        "symbol": symbol,
        "coin_name": symbol.replace("USDT", ""),
        "decision": "WAIT",
        "decision_reasons": ["entry_not_confirmed"],
        "global_score": 70.0,
    }
    row.update(kwargs)
    return row


def test_markdown_uses_trade_candidates_not_setup_lists() -> None:
    generator = ReportGenerator({"output": {"top_n_per_setup": 5}})

    reversals = [{"symbol": "LEGACYUSDT", "coin_name": "Legacy", "score": 90.0}]
    global_top20 = [_row("AAAUSDT", decision="ENTER", global_score=80.0)]

    md = generator.generate_markdown_report(reversals, [], [], global_top20, "2026-03-08")

    assert "AAAUSDT" in md
    assert "LEGACYUSDT" not in md


def test_markdown_wait_reasons_are_rendered_without_shortening() -> None:
    generator = ReportGenerator({"output": {"top_n_per_setup": 5}})

    global_top20 = [
        _row(
            "AAAUSDT",
            decision_reasons=["entry_not_confirmed", "btc_regime_caution", "spread_too_wide"],
        )
    ]
    md = generator.generate_markdown_report([], [], [], global_top20, "2026-03-08")

    assert "decision_reasons: entry_not_confirmed, btc_regime_caution, spread_too_wide" in md


def test_markdown_raises_clear_error_for_invalid_trade_candidates_schema(monkeypatch) -> None:
    generator = ReportGenerator({"output": {"top_n_per_setup": 5}})

    def _invalid_report(*args, **kwargs):
        return {
            "trade_candidates": [{"rank": 1, "symbol": "AAAUSDT", "decision": "WAIT", "decision_reasons": "bad"}],
            "run_manifest": {},
            "btc_regime": {},
        }

    monkeypatch.setattr(generator, "generate_json_report", _invalid_report)

    with pytest.raises(ValueError, match="decision_reasons"):
        generator.generate_markdown_report([], [], [], [_row("AAAUSDT")], "2026-03-08")


def test_markdown_output_is_deterministic_for_identical_input() -> None:
    generator = ReportGenerator({"output": {"top_n_per_setup": 5}})

    global_top20 = [
        _row("BBBUSDT", decision="WAIT", global_score=70.0),
        _row("AAAUSDT", decision="ENTER", global_score=80.0),
        _row("CCCUSDT", decision="NO_TRADE", global_score=90.0),
    ]

    first = generator.generate_markdown_report([], [], [], global_top20, "2026-03-08")
    second = generator.generate_markdown_report([], [], [], global_top20, "2026-03-08")

    assert first == second
    assert first.index("AAAUSDT") < first.index("BBBUSDT")
