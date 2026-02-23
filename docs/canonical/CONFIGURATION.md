# Configuration — Keys, Defaults, Limits (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_CONFIG
status: canonical
intent: "single machine-readable source for defaults/limits and their meanings"
```

## 0) Canonical principle
This document defines canonical defaults, limits, and parameter meanings.
If the implementation deviates, either:
- the code is updated to match canonical, or
- canonical is updated explicitly (AUTHORITY process).

## 1) Machine Defaults (YAML)
```yaml
limits:
  universe:
    market_cap_usd_default: {min: 100_000_000, max: 10_000_000_000}
  outputs:
    global_top_n_default: 20

liquidity:
  orderbook_top_k_default: 200
  slippage_notional_usd_default: 20_000

history_minimums_default:
  breakout: { "1d": 30, "4h": 50 }
  pullback: { "1d": 60, "4h": 80 }
  reversal: { "1d": 120, "4h": 80 }

features:
  ema_periods_default: [20, 50]
  atr_period_default: 14
  volume_sma_periods_default: { "1d": 20, "4h": 20 }
  bb:
    period_default: 20
    stddev_default: 2.0
    rank_lookback_4h_default: 120
  atr_pct_rank_lookback_1d_default: 120

percent_rank:
  population_definition: "eligible universe after hard gates with non-NaN feature value"
  tie_handling: "average_rank"
  formula: "(count_less + 0.5*count_equal) / N"

setup_breakout_trend_1_5d:
  liquidity_gates_usd:
    normal_quote_volume_24h_min: 10_000_000
    btc_risk_off_quote_volume_24h_min: 15_000_000
  gates_1d:
    atr_pct_rank_120_max: 0.80
    overextension_dist_ema20_hard_lt: 28.0
    overextension_dist_ema20_mult_start: 12
    overextension_dist_ema20_mult_strong: 20
  trigger_4h:
    window_bars: 6
  retest_4h:
    tolerance_pct: 1.0
    window_bars: 12
  weights:
    breakout_distance: 0.35
    volume: 0.35
    trend: 0.15
    bb_score: 0.15
  curves:
    breakout_distance:
      floor: -5.0
      min_breakout: 2.0
      ideal_breakout: 5.0
      max_breakout: 20.0
    volume_score:
      min_spike: 1.5
      full_spike: 2.5
    bb_score:
      full_rank_le: 0.20
      linear_to_rank_le: 0.60
      linear_floor_at: 40
  multipliers:
    anti_chase:
      start_r7: 30
      full_r7: 60
      min_mult: 0.75
    btc_regime:
      risk_off_multiplier: 0.85
      rs_override:
        r7_diff_ge: 7.5
        r3_diff_ge: 3.5
```

## 2) Units & conventions
- Percent ranks are in `[0..1]`
- Scores are in `[0..100]`
- `*_pct` is percent (e.g., 7.5 means 7.5%)
- `*_bps` is basis points (1% = 100 bps)

## 3) Config keys in code
Implementation may use different key names. Canonical mapping should be documented once confirmed:
- TODO: map canonical keys to `config/config.yml` keys and/or CLI flags.

## 4) Change control
Any default/limit change that affects outputs requires:
- updating this document
- updating golden fixtures (if impacted)
- verifying deterministic invariants
