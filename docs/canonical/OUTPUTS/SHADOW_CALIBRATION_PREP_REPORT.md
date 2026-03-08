# Shadow Calibration Preparation Report (Canonical)

## Machine Header (YAML)
```yaml
id: OUTPUT_SHADOW_CALIBRATION_PREP
status: canonical
output_kind: shadow_calibration_prep_report_json
path_pattern: "artifacts/shadow_calibration/shadow_calibration_prep_*.json"
phase: preparation_only
```

## Purpose
This output is a **preparation artifact** for later shadow calibration work.

Hard constraints:
- It MUST NOT change productive scanner thresholds.
- It MUST NOT enable active calibration.
- It MUST remain an analysis/meta artifact, separate from runtime decision truth.

## Input
- Source file: evaluation dataset JSONL (`eval_*.jsonl`) as defined in `OUTPUTS/EVALUATION_DATASET.md`.
- Required source row types:
  - first row `type="meta"`
  - following `type="candidate_setup"` rows

## Required fields (report)
- `type = "shadow_calibration_prep_report"`
- `report_id` (deterministic id from CLI override or UTC timestamp)
- `generated_at_iso` (UTC)
- `source_run_id`
- `source_dataset_schema_version`
- `summary`
  - `candidate_rows`
  - `evaluable_rows`
  - `not_evaluable_rows`
  - `invalid_rows`
  - `invalid_ratio`
- `setup_type_summary`
- `invalid_examples`
- `calibration_state`
  - `active` MUST be `false`
  - `threshold_adjustment` MUST be `null`

## Data quality handling
- Missing required label fields (`hit10_5d`, `hit20_5d`, `mfe_5d_pct`, `mae_5d_pct`) are invalid and MUST be reported.
- Non-finite numeric values (`NaN`, `+inf`, `-inf`) in preparation inputs MUST be reported explicitly as invalid.
- Not-evaluable rows (e.g. nullable label fields remain `null`) MUST stay separate from invalid rows.

## Determinism
For identical input file and identical CLI arguments:
- `summary`, `setup_type_summary`, and `invalid_examples` MUST be deterministic.
- Ordering of `invalid_examples` MUST be stable.

## Strict / atomic behavior
If strict mode is enabled:
- Any invalid row MUST fail the run.
- The report file MUST NOT be written (no partial writes).
