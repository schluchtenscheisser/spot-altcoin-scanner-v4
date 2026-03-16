# Pre-Top20 Inclusion Audit

- Generated at UTC: `2026-03-16T22:04:30Z`
- Run ID: `2026-03-16_1773675009352`
- Run file: `reports/2026-03-16.json`

## Published Top20
- `top20_size`: 20
- `decision_distribution`: {'WAIT': 13, 'NO_TRADE': 7}
- `setup_type_distribution`: {'reversal': 16, 'pullback': 4}
- `tradeability_distribution`: {'MARGINAL': 13, 'DIRECT_OK': 7}
- `entry_state_distribution`: {'chased': 20}
- `risk_ok_count`: 14
- `entry_eligible_count`: 7
- `global_score_summary`: {'count': 20, 'min': 56.584, 'median': 59.868, 'max': 75.904, 'mean': 62.82}

## Upstream candidate source
- `source_file`: /home/runner/work/spot-altcoin-scanner/spot-altcoin-scanner/tests/fixtures/snapshots/history/2026-02-01.json
- `source_bucket`: other
- `search_priority_order`: ['snapshots/runtime', 'snapshots/history', 'snapshots/raw', 'other']
- `array_path`: scoring.breakouts
- `array_length`: 21
- `sample_keys`: ['score', 'setup_id', 'symbol', 'trade_levels']

## Inclusion comparison
- `upstream_rows_total`: 21
- `dedup_symbols_total`: 0
- `overlap_count`: 0
- `jaccard_overlap`: 0.0
- `published_not_in_reconstructed_top20_count`: 20
- `reconstructed_not_in_published_top20_count`: 0
- `published_not_in_reconstructed_top20`: ['AVAXUSDT', 'BBUSDT', 'BERAUSDT', 'BONKUSDT', 'CAKEUSDT', 'CFXUSDT', 'EIGENUSDT', 'ETCUSDT', 'FARTCOINUSDT', 'FETUSDT', 'KASUSDT', 'MOODENGUSDT', 'NEOUSDT', 'ORDIUSDT', 'PENGUUSDT', 'QUBICUSDT', 'RIVERUSDT', 'SUSDT', 'TAOUSDT', 'ZENUSDT']
- `reconstructed_not_in_published_top20`: []
- `cutoff_score_proxy`: None
- `published_risk_ok_count`: 14
- `reconstructed_risk_ok_count`: 0
- `near_misses_risk_ok_count`: 0
- `published_entry_eligible_count`: 7
- `reconstructed_entry_eligible_count`: 0
- `near_misses_entry_eligible_count`: 0

## Published vs reconstructed setup distributions
- `published_top20`: {'reversal': 16, 'pullback': 4}
- `reconstructed_top20`: {}
- `dedup_universe`: {}

## Published vs reconstructed tradeability distributions
- `published_top20`: {'MARGINAL': 13, 'DIRECT_OK': 7}
- `reconstructed_top20`: {}
- `near_misses_21_40`: {}

## Near misses 21-40
_none_

## Reconstructed Top20
_none_

## Published Top20 rows
| symbol | setup_id | setup | decision | tradeability | risk_ok | entry_ready | entry_state | global_score | reasons |
|---|---|---|---|---|---:|---:|---|---:|---|
| CAKEUSDT | UNKNOWN | reversal | WAIT | DIRECT_OK | True | True | chased | 75.904 | effective_rr_insufficient, entry_chased |
| NEOUSDT | UNKNOWN | reversal | WAIT | MARGINAL | True | True | chased | 75.288 | tradeability_marginal, entry_chased |
| BBUSDT | UNKNOWN | reversal | WAIT | MARGINAL | True | False | chased | 67.592 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| SUSDT | UNKNOWN | reversal | WAIT | MARGINAL | True | False | chased | 65.488 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| EIGENUSDT | UNKNOWN | reversal | WAIT | DIRECT_OK | True | False | chased | 65.472 | entry_not_confirmed, retest_not_reclaimed, entry_chased |
| BONKUSDT | UNKNOWN | reversal | WAIT | MARGINAL | True | False | chased | 61.016 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| ETCUSDT | UNKNOWN | reversal | WAIT | DIRECT_OK | True | False | chased | 59.976 | entry_not_confirmed, retest_not_reclaimed, entry_chased |
| KASUSDT | UNKNOWN | reversal | WAIT | MARGINAL | True | False | chased | 59.392 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| ZENUSDT | UNKNOWN | reversal | WAIT | MARGINAL | True | False | chased | 59.168 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| QUBICUSDT | UNKNOWN | pullback | WAIT | MARGINAL | True | True | chased | 58.32 | tradeability_marginal, entry_chased |
| TAOUSDT | UNKNOWN | pullback | WAIT | DIRECT_OK | True | True | chased | 58.32 | entry_chased |
| FARTCOINUSDT | UNKNOWN | reversal | WAIT | MARGINAL | True | False | chased | 58.032 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| ORDIUSDT | UNKNOWN | reversal | WAIT | DIRECT_OK | True | False | chased | 57.648 | entry_not_confirmed, retest_not_reclaimed, entry_chased |
| CFXUSDT | UNKNOWN | reversal | NO_TRADE | MARGINAL | False | True | chased | 72.688 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| FETUSDT | UNKNOWN | reversal | NO_TRADE | DIRECT_OK | True | True | chased | 68.992 | price_past_target_1, entry_chased |
| RIVERUSDT | UNKNOWN | pullback | NO_TRADE | MARGINAL | False | True | chased | 61.2 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| AVAXUSDT | UNKNOWN | pullback | NO_TRADE | DIRECT_OK | False | False | chased | 59.76 | risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, rebound_not_confirmed, entry_chased |
| BERAUSDT | UNKNOWN | reversal | NO_TRADE | MARGINAL | False | True | chased | 58.488 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| PENGUUSDT | UNKNOWN | reversal | NO_TRADE | MARGINAL | False | False | chased | 57.072 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| MOODENGUSDT | UNKNOWN | reversal | NO_TRADE | MARGINAL | False | False | chased | 56.584 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
