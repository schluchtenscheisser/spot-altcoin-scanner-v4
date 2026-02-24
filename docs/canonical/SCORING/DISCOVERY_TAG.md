# Discovery Tag — “New coin” identification (Canonical)

## Machine Header (YAML)
```yaml
id: SCORE_DISCOVERY_TAG
status: canonical
default_max_age_days: 180
timestamps_unit: ms
discovery_source_allowed:
  - cmc_date_added
  - first_seen_ts
  - null
```

## Age computation (ms)
- `age_days = floor((asof_ts_ms - source_ts_ms) / 86_400_000)`

## Output
- `discovery_source` is `null` if neither source exists.
