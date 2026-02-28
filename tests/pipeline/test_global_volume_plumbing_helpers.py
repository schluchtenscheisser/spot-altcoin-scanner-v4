from scanner.clients.mapping import MappingResult
from scanner.pipeline.__init__ import (
    _compute_mexc_share_24h,
    _compute_turnover_24h,
    _extract_cmc_global_volume_24h,
)


def test_extract_cmc_global_volume_24h_missing_and_present() -> None:
    mapped = MappingResult(
        mexc_symbol="ABCUSDT",
        cmc_data={"quote": {"USD": {"volume_24h": "123.45"}}},
        confidence="high",
        method="symbol_exact_match",
    )
    missing = MappingResult(
        mexc_symbol="ABCUSDT",
        cmc_data={"quote": {"USD": {}}},
        confidence="high",
        method="symbol_exact_match",
    )

    assert _extract_cmc_global_volume_24h(mapped) == 123.45
    assert _extract_cmc_global_volume_24h(missing) is None


def test_turnover_and_mexc_share_handle_zero_and_missing_denominators() -> None:
    assert _compute_turnover_24h(100.0, 10.0) == 10.0
    assert _compute_turnover_24h(100.0, 0) is None
    assert _compute_turnover_24h(None, 10.0) is None

    assert _compute_mexc_share_24h(5.0, 100.0) == 0.05
    assert _compute_mexc_share_24h(5.0, 0) is None
    assert _compute_mexc_share_24h(None, 100.0) is None
