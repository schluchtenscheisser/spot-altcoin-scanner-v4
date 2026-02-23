# Scope — What the Spot Altcoin Scanner Does (and does not) (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_SCOPE
status: canonical
tool_name: spot-altcoin-scanner
market_focus:
  exchange: MEXC
  market: spot
  quote_asset: USDT
segment_focus_default:
  market_cap_usd: {min: 100_000_000, max: 10_000_000_000}
non_goals:
  - automated_execution
  - financial_advice
  - ML_prediction
  - sentiment_or_news_dependency
determinism_contract:
  closed_candle_only: true
  no_lookahead: true
  no_randomness: true
```

## What it does
- Deterministic scanner that identifies and ranks short-term spot-altcoin trading setups.
- Produces structured outputs (JSON/Markdown/Excel) containing:
  - setup_id
  - component scores and final score
  - gating/flag diagnostics
  - liquidity diagnostics (slippage/spread/grade) for top candidates
  - reproducibility manifest (commit/config/as-of)

## What it does not do
- No automated trading/execution (not a bot).
- No predictive ML model.
- No guarantees of profitability.
- No implicit use of sentiment/news/on-chain data unless explicitly specified in canonical docs.

## Current canonical setups
- Breakout Trend 1–5d (Immediate + Retest): `SCORING/SCORE_BREAKOUT_TREND_1_5D.md`

## Determinism contract (high-level)
- Closed-candle-only: never use an in-progress candle for computations.
- No-lookahead: never use future candles.
- Identical inputs + identical config => identical outputs.
