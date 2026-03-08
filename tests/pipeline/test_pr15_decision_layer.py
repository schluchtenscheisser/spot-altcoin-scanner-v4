from __future__ import annotations

import pytest

from scanner.pipeline.decision import apply_decision_layer


def _cfg(**overrides):
    base = {
        "decision": {
            "min_score_for_enter": 65,
            "min_score_for_wait": 40,
            "require_tradeability_for_enter": True,
            "require_risk_acceptable_for_enter": True,
        },
        "btc_regime": {
            "risk_off_enter_boost": 15,
        },
    }
    for section, values in overrides.items():
        base.setdefault(section, {}).update(values)
    return base


def test_enter_for_direct_ok_when_all_requirements_are_met():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "DIRECT_OK", "entry_ready": True, "risk_acceptable": True, "setup_score": 70}]
    out = apply_decision_layer(rows, _cfg())
    assert out[0]["decision"] == "ENTER"
    assert out[0]["decision_reasons"] == []


def test_enter_for_tranche_ok_when_all_requirements_are_met():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "TRANCHE_OK", "entry_ready": True, "risk_acceptable": True, "setup_score": 66}]
    out = apply_decision_layer(rows, _cfg())
    assert out[0]["decision"] == "ENTER"


def test_wait_when_entry_not_ready_but_quality_is_sufficient():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "DIRECT_OK", "entry_ready": False, "entry_readiness_reasons": ["breakout_not_confirmed"], "risk_acceptable": True, "setup_score": 55}]
    out = apply_decision_layer(rows, _cfg())
    assert out[0]["decision"] == "WAIT"
    assert out[0]["decision_reasons"] == ["entry_not_confirmed", "breakout_not_confirmed"]


def test_wait_for_marginal_tradeability():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "MARGINAL", "entry_ready": True, "risk_acceptable": True, "setup_score": 75}]
    out = apply_decision_layer(rows, _cfg())
    assert out[0]["decision"] == "WAIT"
    assert "tradeability_marginal" in out[0]["decision_reasons"]


def test_wait_when_btc_regime_boost_prevents_enter():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "DIRECT_OK", "entry_ready": True, "risk_acceptable": True, "setup_score": 70}]
    out = apply_decision_layer(rows, _cfg(), btc_regime={"state": "RISK_OFF"})
    assert out[0]["decision"] == "WAIT"
    assert out[0]["decision_reasons"] == ["btc_regime_caution"]


def test_no_trade_for_rejected_risk():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "DIRECT_OK", "entry_ready": True, "risk_acceptable": False, "setup_score": 90}]
    out = apply_decision_layer(rows, _cfg())
    assert out[0]["decision"] == "NO_TRADE"
    assert "risk_reward_unattractive" in out[0]["decision_reasons"]


def test_no_trade_below_minimum_wait_score():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "DIRECT_OK", "entry_ready": False, "risk_acceptable": True, "setup_score": 30}]
    out = apply_decision_layer(rows, _cfg())
    assert out[0]["decision"] == "NO_TRADE"
    assert "insufficient_edge" in out[0]["decision_reasons"]


def test_no_trade_when_hard_risk_flag_is_present():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "DIRECT_OK", "entry_ready": True, "risk_acceptable": True, "risk_flags": ["stop_distance_too_wide"], "setup_score": 90}]
    out = apply_decision_layer(rows, _cfg())
    assert out[0]["decision"] == "NO_TRADE"
    assert out[0]["decision_reasons"] == ["risk_flag_blocked", "stop_distance_too_wide"]


def test_unknown_and_fail_never_become_enter_or_wait():
    rows = [
        {"symbol": "AAAUSDT", "tradeability_class": "UNKNOWN", "setup_score": 99, "entry_ready": True, "risk_acceptable": True},
        {"symbol": "BBBUSDT", "tradeability_class": "FAIL", "setup_score": 99, "entry_ready": True, "risk_acceptable": True},
    ]
    out = apply_decision_layer(rows, _cfg())
    assert {row["symbol"]: row["decision"] for row in out} == {"AAAUSDT": "NO_TRADE", "BBBUSDT": "NO_TRADE"}


def test_nullable_risk_acceptable_is_not_coerced_to_bool():
    rows = [{"symbol": "AAAUSDT", "tradeability_class": "DIRECT_OK", "entry_ready": True, "risk_acceptable": None, "setup_score": 90}]
    out = apply_decision_layer(rows, _cfg())
    assert out[0]["decision"] == "WAIT"
    assert out[0]["decision_reasons"] == ["risk_data_insufficient"]


def test_decision_output_is_deterministic_for_identical_inputs():
    rows = [
        {"symbol": "AAAUSDT", "tradeability_class": "DIRECT_OK", "entry_ready": False, "entry_readiness_reasons": ["retest_not_reclaimed"], "risk_acceptable": True, "setup_score": 60},
        {"symbol": "BBBUSDT", "tradeability_class": "MARGINAL", "entry_ready": True, "risk_acceptable": None, "setup_score": 62},
    ]
    out1 = apply_decision_layer(rows, _cfg(), btc_regime={"state": "RISK_OFF"})
    out2 = apply_decision_layer(rows, _cfg(), btc_regime={"state": "RISK_OFF"})
    assert out1 == out2


def test_invalid_decision_config_is_rejected():
    with pytest.raises(ValueError):
        apply_decision_layer([], {"decision": {"min_score_for_enter": 30, "min_score_for_wait": 40}})
