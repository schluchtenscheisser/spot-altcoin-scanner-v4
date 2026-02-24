# Discovery Tag — “New coin” identification (Canonical)

## Machine Header (YAML)
```yaml
id: SCORE_DISCOVERY_TAG
status: canonical
default_max_age_days: 180
primary_source: "cmc_date_added"
fallback_source: "first_seen_ts"
outputs:
  discovery_source_enum:
    - cmc_date_added
    - first_seen_ts
    - none
timestamps:
  unit: ms
```

## 0) Purpose
Discovery is an informational tag indicating whether an asset is “new” within a defined age window. It must be deterministic.

## 1) Inputs
Primary (preferred):
- `cmc_date_added_ts_ms` (UTC, milliseconds), derived from CMC `date_added`.

Fallback:
- `first_seen_ts_ms` (UTC, milliseconds), earliest available 1D OHLCV candle closeTime for the symbol.

## 2) Age computation (milliseconds)
Let:
- `asof_ts_ms` = run as-of timestamp in ms (UTC)
- `source_ts_ms` = `cmc_date_added_ts_ms` if present else `first_seen_ts_ms`

Compute:
- `age_days = floor((asof_ts_ms - source_ts_ms) / 86_400_000)`

If `asof_ts_ms < source_ts_ms`:
- clamp `age_days = 0` (deterministic).

## 3) Discovery decision
Let `max_age_days = 180` (default).
- `discovery = (age_days <= max_age_days)`

## 4) Output fields
Per symbol:
- `discovery` (bool)
- `age_days` (int)
- `discovery_source` in {"cmc_date_added", "first_seen_ts", "none"}

Rules:
- If CMC date_added present: `discovery_source="cmc_date_added"`
- Else if first_seen present: `discovery_source="first_seen_ts"`
- Else: `discovery=false`, `age_days=null`, `discovery_source="none"`

## 5) Determinism constraints
- All timestamps use ms.
- Fallback `first_seen_ts_ms` must be derived from OHLCV data itself (earliest closeTime), not API ordering.

## 6) Notes
Discovery must not influence scoring unless explicitly referenced.
