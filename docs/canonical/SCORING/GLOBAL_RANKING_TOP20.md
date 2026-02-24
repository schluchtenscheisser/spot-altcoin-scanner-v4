# Global Ranking — Top-N, Dedup, Setup Weights (Canonical)

## Machine Header (YAML)
```yaml
id: SCORE_GLOBAL_RANKING_TOP20
status: canonical
global_top_n_default: 20
dedup:
  per_symbol_max_rows: 1
  prefer_setup_id_order:
    - breakout_retest_1_5d
    - breakout_immediate_1_5d
setup_preference:
  mapping:
    breakout_retest_1_5d: 1
    breakout_immediate_1_5d: 0
  default_for_unknown_setup_id: -1
sorting_after_dedup:
  - key: global_score
    order: desc
  - key: setup_preference
    order: desc
  - key: symbol
    order: asc
global_score_definition:
  method: "max_over_setups"
  setup_weights:
    breakout_trend: 1.0
    pullback: 0.9
    reversal: 0.8
```

## 0) Purpose
This document defines how individual setup scores become a single global ranked list (Top-N), without duplication and with deterministic tie-break rules.

## 1) Inputs
A set of scored setup rows, each containing at minimum:
- `symbol`
- `setup_id`
- `final_score` (0..100)

## 2) Setup weights (canonical defaults)
Setup weights apply to the per-setup `final_score` to produce a comparable global score.

Default weights (reserved for future setups):
- Breakout: 1.0
- Pullback: 0.9
- Reversal: 0.8

If only Breakout Trend 1–5d is active, only weight 1.0 is used.

## 3) Global score definition
For a given symbol:
- `weighted_setup_score = final_score * setup_weight(setup_id)`
- `global_score(symbol) = max(weighted_setup_score over all valid setups for symbol)`
- `best_setup_id = argmax(weighted_setup_score)`

## 4) Setup preference (deterministic)
Define:
- `setup_preference(setup_id)` using the mapping in the Machine Header:
  - `breakout_retest_1_5d -> 1`
  - `breakout_immediate_1_5d -> 0`
  - unknown -> -1

This preference is only used for deterministic tie-breaking.

## 5) Dedup rule (one row per symbol)
Canonical dedup:
1) For each symbol, select the row with the highest `weighted_setup_score`.
2) If multiple rows tie on `weighted_setup_score`, select the one whose `setup_id` appears earliest in:
   - `prefer_setup_id_order` (Machine Header)
3) If still tied, tie-break by `setup_id` lexicographically ascending.
4) If still tied, tie-break by `symbol` ascending.

## 6) Sorting the global list (after dedup)
- Sort by `global_score` descending
- Then by `setup_preference` descending
- Then by `symbol` ascending

## 7) Top-N truncation
- Keep only the first `global_top_n` rows (default 20).

## 8) Interaction with liquidity re-rank
Canonical ordering pipeline:
1) Compute global list (this doc)
2) Apply liquidity re-rank (`docs/canonical/LIQUIDITY/RE_RANK_RULE.md`)
3) Render outputs
