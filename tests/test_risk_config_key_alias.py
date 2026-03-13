import math

import pytest

from scanner.config import ScannerConfig, resolve_risk_min_rr_to_target_1


def test_resolve_uses_canonical_key_when_present() -> None:
    assert resolve_risk_min_rr_to_target_1({"min_rr_to_target_1": 1.7}) == pytest.approx(1.7)


def test_resolve_uses_legacy_alias_when_canonical_missing() -> None:
    assert resolve_risk_min_rr_to_target_1({"min_rr_to_tp10": 1.6}) == pytest.approx(1.6)


def test_resolve_prefers_canonical_when_both_present() -> None:
    assert resolve_risk_min_rr_to_target_1({"min_rr_to_target_1": 1.8, "min_rr_to_tp10": 1.1}) == pytest.approx(1.8)


def test_resolve_raises_on_invalid_canonical_even_if_legacy_valid() -> None:
    with pytest.raises(ValueError, match="risk.min_rr_to_target_1"):
        resolve_risk_min_rr_to_target_1({"min_rr_to_target_1": "bad", "min_rr_to_tp10": 1.1})


@pytest.mark.parametrize("bad", [math.nan, math.inf, -math.inf])
def test_resolve_rejects_non_finite_for_both_keys(bad: float) -> None:
    with pytest.raises(ValueError, match="risk.min_rr_to_target_1"):
        resolve_risk_min_rr_to_target_1({"min_rr_to_target_1": bad})
    with pytest.raises(ValueError, match="risk.min_rr_to_tp10"):
        resolve_risk_min_rr_to_target_1({"min_rr_to_tp10": bad})


def test_config_accessor_defaults_when_both_keys_missing() -> None:
    cfg = ScannerConfig(raw={})
    assert cfg.risk_min_rr_to_target_1 == pytest.approx(1.3)
