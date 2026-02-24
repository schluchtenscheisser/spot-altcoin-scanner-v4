# Verification for AI — Golden Fixtures, Invariants, Checklist (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_VERIFICATION_FOR_AI
status: canonical
comparison:
  method: numeric_abs_tolerance
  abs_tolerance: 1e-9
```

## Comparison rule
Compare expected numeric values as floats with absolute tolerance 1e-9. No rounding.

## Fixture A trace (key point)
dist_pct=1.643406808 lies in [0,2):
breakout_distance_score = 30 + 40*(dist_pct/2) = 62.868136160
