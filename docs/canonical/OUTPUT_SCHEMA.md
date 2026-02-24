# Output Schema — JSON / Markdown / Excel (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_OUTPUT_SCHEMA
status: canonical
schema_version: 1
outputs:
  - json
  - markdown
  - excel
limits:
  global_top_n_default: 20
manifest:
  config_hash_required: true
  config_version_optional: true
trade_levels:
  status: canonical_output_only
  levels_timeframe_default_by_setup_id:
    breakout_immediate_1_5d: 4h
    breakout_retest_1_5d: 4h
  atr_timeframe_rule: "atr_pct uses the same timeframe as levels_timeframe"
  rounding:
    mode: none
    note: "No rounding is applied in canonical; emit raw floats."
```

## 1) JSON output
Canonical goal: JSON is the primary machine-readable artifact.

### 1.1 Run manifest (required)
Required:
- `commit_hash`
- `schema_version`
- `asof_ts_ms` (or ISO timestamp)
- `providers_used` (MEXC/CMC, etc.)
- `config_hash`

Optional:
- `config_version`

### 1.2 Candidate row (required, minimal set)
- Identity:
  - `symbol`
  - `setup_id`
- Scores:
  - `base_score`
  - `final_score`
- Liquidity:
  - `proxy_liquidity_score` (0..1, cross-sectional percent-rank of quote_volume_24h_usd)
  - `quote_volume_24h_usd` (raw proxy)
  - `spread_bps` (optional if not fetched)
  - `slippage_bps` (optional if not fetched)
  - `liquidity_insufficient_depth` (bool)
  - `liquidity_grade` (A/B/C/D, if graded)
- Validity:
  - `is_valid_setup`
  - `invalid_reason` (required if invalid)

### 1.3 Ordering and limits
- Global Top list is limited to `global_top_n` (default 20).
- Final ordering must be explainable by `LIQUIDITY/RE_RANK_RULE.md`.

## 2) Trade levels (informational output, deterministic)
Trade levels are informational outputs. They must not change ranking unless explicitly referenced.

### 2.1 Required fields (if present)
- `trade_levels_enabled` (bool)
- `levels_timeframe` in {"1d","4h"} (canonical default depends on setup_id; see Machine Header)
- `entry_level` (price)
- `stop_level` (price)
- `partial_target_level` (price, optional)
- `take_profit_level` (price, optional)
- `risk_R` (price distance; optional)

### 2.2 Canonical formulas (default)
Let:
- `tf = levels_timeframe`
- `entry_level = close_tf_last_closed`
- `atr_pct_tf_last_closed = atr_pct_<tf>_last_closed`
- `atr_abs = (atr_pct_tf_last_closed/100) * close_tf_last_closed`
- `stop_level = entry_level - 1.2 * atr_abs`
- `R = entry_level - stop_level`
- `partial_target_level = entry_level + 1.5 * R` (optional)
- `take_profit_level = entry_level + 3.0 * R` (optional)

Notes:
- If `atr_pct_tf_last_closed` is NaN, levels must be omitted or flagged as unavailable deterministically.
- If `close_tf_last_closed <= 0`, all levels are undefined.

### 2.3 Rounding policy (canonical)
- Canonical: **no rounding**. Emit raw floats.
- If implementation rounds (tick size, decimals), it must be explicitly documented and tested.

## 3) Markdown output
- Must be consistent with JSON (no contradictions).

## 4) Excel output
- A tabular export of the same canonical fields.
- Column order should be stable.

## 5) Schema evolution
- Any breaking change increments `schema_version`.
- Canonical changes must be reflected in docs and tests/fixtures.
