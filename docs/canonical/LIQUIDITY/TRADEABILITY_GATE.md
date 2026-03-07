# Tradeability Gate — Classes, Reasons, Decision Eligibility (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_TRADEABILITY_GATE
status: canonical
tradeability_classes:
  - DIRECT_OK
  - TRANCHE_OK
  - MARGINAL
  - FAIL
  - UNKNOWN
unknown_reason_family:
  - tradeability_unknown
  - orderbook_data_missing
  - orderbook_data_stale
  - orderbook_not_in_budget
```

## Class semantics
- `DIRECT_OK`: Entry-size feasible under direct execution constraints.
- `TRANCHE_OK`: Entry feasible only via tranche execution constraints.
- `MARGINAL`: Fully evaluated but below Phase-1 entry execution quality threshold.
- `FAIL`: Fully evaluated and hard-failed tradeability checks.
- `UNKNOWN`: Not evaluable / not evaluated; no deterministic execution quality assessment available.

## Classification criteria (Phase 1 V4.2.1)
- Inputs (runtime-configurable with canonical defaults):
  - `notional_total_usdt` (default `20_000`)
  - `notional_chunk_usdt` (default `5_000`)
  - `max_tranches` (default `4`)
  - `max_spread_pct` (default `0.15`)
  - `min_depth_1pct_usd` (default `200_000`)
  - class thresholds: `direct_ok_max_slippage_bps=50`, `tranche_ok_max_slippage_bps=100`, `marginal_max_slippage_bps=150`
- `DIRECT_OK` iff all hold: spread gate pass, depth gate pass, and `slippage_bps_20k <= direct_ok_max_slippage_bps`.
- `TRANCHE_OK` iff not `DIRECT_OK` and all hold: spread/depth gates pass, `slippage_bps_5k <= tranche_ok_max_slippage_bps`, and `notional_chunk_usdt * max_tranches >= notional_total_usdt`.
- `MARGINAL` iff fully evaluated and neither `DIRECT_OK` nor `TRANCHE_OK`, but still within marginal execution quality envelope.
- `FAIL` iff fully evaluated and hard-fails tradeability quality envelope.
- `UNKNOWN` iff required orderbook evidence is absent/not usable (`missing`, `stale`, or `not_in_budget`).

## Required invariants
- `MARGINAL` is **not ENTER-fähig**.
- `UNKNOWN` is **not WAIT-fähig**.
- `UNKNOWN` is **not FAIL**.
- `UNKNOWN` candidates stop before `DECISION_LAYER`.

## UNKNOWN reason-paths (distinct, non-collapsed)
- `tradeability_unknown`: generic fallback when unknown state is explicit but no narrower reason applies.
- `orderbook_data_missing`: required orderbook snapshot unavailable.
- `orderbook_data_stale`: snapshot exists but violates freshness threshold.
- `orderbook_not_in_budget`: skipped because symbol is outside configured orderbook budget (`orderbook_top_k`).

These reasons MUST remain distinguishable in outputs and diagnostics.

## Decision eligibility mapping
- Eligible for `ENTER`: `DIRECT_OK` or `TRANCHE_OK` only, plus other decision prerequisites.
- Eligible for `WAIT`: fully evaluated non-enter state only (`MARGINAL` or context-dependent holdback); never `UNKNOWN`.
- Forced `NO_TRADE`: `FAIL`.

## Determinism
- Tradeability class assignment order and tie-breaking must be deterministic.
- Null/missing fields must not be bool-coerced into a pass/fail class.
