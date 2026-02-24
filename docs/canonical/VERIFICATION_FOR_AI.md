# Verification for AI — Golden Fixtures, Invariants, Checklist (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_VERIFICATION_FOR_AI
status: canonical
invariants:
  - closed_candle_only
  - no_lookahead
  - deterministic_outputs
  - score_range_0_100
  - percent_rank_population_universe_not_shortlist
golden_fixtures:
  - id: FIX_A_MORPHOUSDT_2026_02_21
    type: market_snapshot
negative_fixtures:
  - id: FIX_B_BTC_RISK_OFF_NO_RS_OVERRIDE
  - id: FIX_C_OVEREXTENSION_HARD_GATE
deterministic_tables:
  - id: TABLE_ANTI_CHASE_MULT
  - id: TABLE_OVEREXTENSION_MULT
  - id: TABLE_BB_SCORE
  - id: TABLE_ATR_GATE
rounding_policy:
  component_scores: "no rounding"
  reported_decimals_optional: 9
```

## 1) Invariants (must always hold)

### 1.1 Closed-candle only
- All computations use only candles with `closeTime <= asof_ts_ms`.

### 1.2 No lookahead
- No feature/gate/score may depend on future candles (index > last closed).

### 1.3 Determinism
- Same inputs + same config => same outputs.
- No stochastic components.

### 1.4 Score ranges
- All component scores and final scores are clamped to `0..100`.

### 1.5 percent_rank population (cross-sectional)
- `percent_rank` population is the *eligible universe after hard gates* (not the shortlist).
- Tie handling is `average_rank` with:
  - `rank = (count_less + 0.5*count_equal) / N` in `[0..1]`
- Equality is exact IEEE-754 float equality (no rounding).

---

## 2) Golden Fixture Set A — MORPHOUSDT Snapshot (2026-02-21)

### 2.1 Snapshot time & last closed candles
- Snapshot time: 2026-02-21 05:10:00 UTC
- 1D last closed: close_time = 2026-02-21 00:00 UTC
- 4H last closed: close_time = 2026-02-21 04:00 UTC

### 2.2 Market/CMC snapshot inputs (MORPHOUSDT)
- quote_volume_24h_usd = 55,339,590
- market_cap_usd = 591,203,400
- price_usd = 1.556758

### 2.3 1D OHLCV-derived values (last closed @ 2026-02-21 00:00 UTC)
- close_1d = 1.5769
- ema20_1d = 1.306868269
- ema50_1d = 1.281034261
- dist_ema20_pct_1d = 20.662505719
- dist_ema50_pct_1d = 23.095849054
- atr_pct_1d = 7.903712459
- atr_pct_rank_120_1d = 0.627358491
- r_7_1d = 33.015605230
- r_3_1d = 4.568965517

### 2.4 Breakout level (1D structure)
- high_20d_1d = 1.5334
  - definition: max high over bars [t1d-20 .. t1d-1] (exclude current 1D bar)

### 2.5 4H OHLCV-derived values (last closed @ 2026-02-21 04:00 UTC)
- close_4h_last_closed = 1.5586
- ema20_4h_last_closed = 1.472211725
- ema50_4h_last_closed = 1.390535901
- bb_width_pct_4h_last_closed = 17.072137112
- bb_width_rank_120_4h = 0.595833333

### 2.6 Volume spikes (SMA20, exclude current)
- volume_quote_spike_1d = 2.645454792
- volume_quote_spike_4h = 1.910802512
- spike_combined = 2.425059108
  - definition: 0.7*spike_1d + 0.3*spike_4h

### 2.7 Distance for scoring (4H close vs level)
- dist_pct = ((close_4h_last_closed / high_20d_1d) - 1) * 100
- dist_pct = 1.643406808

---

## 3) Expected multipliers & component scores (Fixture A)

### 3.1 Overextension multiplier (d = 20.662505719)
Expected:
- overextension_multiplier = 0.837578018

### 3.2 Anti-chase multiplier (r7 = 33.015605230)
Expected:
- anti_chase_multiplier = 0.974869956

### 3.3 BB score (rank r = 0.595833333)
Expected:
- bb_score = 40.625000000

### 3.4 Volume score (spike_combined = 2.425059108)
Expected:
- volume_score = 92.505910842

### 3.5 Breakout distance score (dist_pct = 1.643406808)
Curve params:
- floor=-5, min=2, ideal=5, max=20

Expected:
- breakout_distance_score = 62.868136160

Notes:
- No rounding is applied to component scores by default; values above are provided with 9 decimals.

### 3.6 Gates for Fixture A (must pass)
- trend_gate_1d: True
- atr_chaos_gate_1d: True
- overextension_hard_gate_1d: True
- momentum_gate_1d: True

---

## 4) Negative Fixture Set B — BTC Risk-Off without RS override => Excluded

Arrange (synthetic):
- btc_risk_on = false
- quote_volume_24h_usd (alt) = 20,000,000
- alt_r7_1d - btc_r7_1d = 7.49
- alt_r3_1d - btc_r3_1d = 3.49

Assert:
- RS override == false
- setup invalid (excluded)
- btc_multiplier must not be applied (candidate excluded).

---

## 5) Negative Fixture Set C — Overextension hard gate boundary => Excluded

Arrange:
- dist_ema20_pct_1d = 28.0

Assert:
- setup invalid because hard gate is strict: `dist_ema20_pct_1d < 28.0`.

---

## 6) Deterministic unit tables (no market data required)

### 6.1 TABLE_ANTI_CHASE_MULT (start=30, full=60, min=0.75)

| r_7_1d | expected multiplier |
|---:|---:|
| 29.9 | 1.000000000 |
| 30.0 | 1.000000000 |
| 45.0 | 0.875000000 |
| 60.0 | 0.750000000 |
| 60.1 | 0.750000000 |

### 6.2 TABLE_OVEREXTENSION_MULT (start=12 -> 1.0; strong=20 -> 0.85; hard gate at 28)

| dist_ema20_pct_1d | expected |
|---:|---|
| 11.9 | 1.000000 |
| 12.0 | 1.000000 |
| 16.0 | 0.925000 |
| 20.0 | 0.850000 |
| 27.9 | 0.701875 |
| 28.0 | EXCLUDED |

### 6.3 TABLE_BB_SCORE (rank r)

| bb_width_rank_120_4h | expected bb_score |
|---:|---:|
| 0.20 | 100.0 |
| 0.40 | 70.0 |
| 0.60 | 40.0 |
| 0.61 | 0.0 |

### 6.4 TABLE_ATR_GATE (max_rank = 0.80)

| atr_pct_rank_120_1d | expected |
|---:|---|
| 0.80 | PASS |
| 0.81 | EXCLUDED |

---

## 7) AI Review Checklist (questions to answer)
- Do the fixture inputs reproduce the expected derived values exactly (within float tolerance)?
- Are all hard gates applied exactly as specified (including strict inequalities)?
- Is cross-sectional `percent_rank` tie-handling average-rank with IEEE-754 equality?
- Are rolling ranks (ATR rank, BB rank) using `rolling_percent_rank` (time-series), not cross-sectional population?
- Is ordering deterministic (global ranking + liquidity re-rank)?
