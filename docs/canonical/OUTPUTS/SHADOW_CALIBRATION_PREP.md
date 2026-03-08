# Shadow Calibration Prep Artifact — JSON Contract (Canonical)

## Machine Header (YAML)
```yaml
id: OUTPUT_SHADOW_CALIBRATION_PREP
status: canonical
output_kind: shadow_calibration_prep_json
path_pattern: "artifacts/evaluation/shadow_calibration_prep_*.json"
related_inputs:
  - docs/canonical/OUTPUTS/EVALUATION_DATASET.md
```

## Purpose
This artifact prepares calibration-ready rows from the evaluation dataset without changing live thresholds or decision logic.

Hard rules:
- This artifact is analysis-only.
- It MUST NOT mutate or override live decision thresholds.
- Missing labels (`null`) stay non-evaluable (`not_evaluable`) and MUST NOT be coerced to `false`.

## Input
- Source: evaluation dataset JSONL from `EVALUATION_DATASET.md`.
- First line must be `meta`; subsequent `candidate_setup` rows are processed.

## Output fields
Top-level JSON object fields:
- `type`: constant `shadow_calibration_prep`
- `shadow_prep_schema_version`: schema version string
- `source_eval_path`: input path
- `source_run_id`: copied from meta row
- `min_labeled_rows`: integer threshold for readiness
- `dataset_status`: `ready | insufficient_labeled_rows`
- `counts`: deterministic counters
- `rows`: prepared candidate rows

Prepared row fields:
- identity: `record_id`, `run_id`, `t0_date`, `symbol`, `setup_type`, `setup_rank`
- calibration inputs: `score`, `global_rank`, `hit10_5d`, `hit20_5d`, `mfe_5d_pct`, `mae_5d_pct`
- `label_status`: `labeled | not_evaluable`

## Determinism and edge-case rules
- Sort rows by `(t0_date, setup_type, setup_rank, symbol, record_id)`.
- Non-finite numerics (`NaN`, `inf`, `-inf`) in numeric fields are invalid and excluded with `counts.excluded_invalid_rows` incremented.
- Missing/nullable labels are not invalid rows; they remain in output with `label_status=not_evaluable`.
- `dataset_status=ready` only when `counts.labeled_rows >= min_labeled_rows`.

## Live invariants
- No live scanner output schema fields are changed by this artifact.
- No decision threshold (`min_score_for_enter`, `min_rr_to_tp10`, etc.) is changed by this artifact.
