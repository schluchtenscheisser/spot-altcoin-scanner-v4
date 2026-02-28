from scanner.config import ScannerConfig, validate_config
from scanner.pipeline import _build_scoring_volume_maps
from scanner.pipeline.scoring.reversal import score_reversals


def _reversal_features():
    return {
        "XUSDT": {
            "1d": {
                "drawdown_from_ath": -60.0,
                "base_detected": True,
                "base_score": 80.0,
                "reclaim_ema50": True,
                "dist_ema50_pct": 1.0,
                "volume_spike": 1.7,
            },
            "4h": {"volume_spike": 1.6},
            "meta": {"last_closed_idx": {"1d": 200, "4h": 200}},
            "quote_volume_24h": 2_000_000.0,
        }
    }


def test_scoring_volume_source_defaults_to_mexc_when_missing() -> None:
    cfg = ScannerConfig(raw={})
    assert cfg.scoring_volume_source == "mexc"


def test_scoring_volume_source_invalid_value_fails_validation() -> None:
    cfg = ScannerConfig(
        raw={
            "general": {"run_mode": "offline"},
            "universe_filters": {"market_cap": {"min_usd": 1, "max_usd": 2}},
            "scoring": {"volume_source": "invalid"},
        }
    )
    errors = validate_config(cfg)
    assert any("scoring.volume_source" in err for err in errors)


def test_build_scoring_volume_map_uses_global_and_falls_back_to_mexc() -> None:
    shortlist = [
        {"symbol": "AUSDT", "quote_volume_24h": 100.0, "global_volume_24h_usd": 500.0},
        {"symbol": "BUSDT", "quote_volume_24h": 200.0, "global_volume_24h_usd": None},
    ]

    volume_map, source_map = _build_scoring_volume_maps(shortlist, {"scoring": {"volume_source": "global_fallback_mexc"}})

    assert volume_map == {"AUSDT": 500.0, "BUSDT": 200.0}
    assert source_map == {"AUSDT": "global", "BUSDT": "mexc"}


def test_reversal_scoring_reports_volume_source_used() -> None:
    features = _reversal_features()
    volumes = {"XUSDT": 2_000_000.0}

    rows = score_reversals(features, volumes, {}, volume_source_map={"XUSDT": "global"})

    assert rows[0]["volume_source_used"] == "global"
    assert rows[0]["reasons"][0] == "Volume source used: global"
