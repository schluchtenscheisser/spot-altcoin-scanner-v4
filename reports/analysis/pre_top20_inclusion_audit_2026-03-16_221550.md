# Pre-Top20 Inclusion Audit

- Generated at UTC: `2026-03-16T22:15:50Z`
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
_No larger upstream candidate array found._

## Missing-snapshot guidance
- `status`: missing_upstream_candidate_array
- `message`: No larger pre-Top20 candidate array was found in snapshots/runtime, snapshots/history, snapshots/raw, or other repo JSONs after excluding tests/fixtures and requiring global-ranking-capable score fields.
- `search_order_used`: ['snapshots/runtime', 'snapshots/history', 'snapshots/raw', 'other']
- `run_id_target`: 2026-03-16_1773675009352
- `run_dates_target`: ['2026-03-16']
- `run_tokens_target`: ['1773675009352']
- `required_minimum_fields_per_row`: ['symbol', 'setup_id', 'best_setup_type or setup_type', 'at least one of: global_score / weighted_score / final_score / setup_score']
- `preferred_additional_fields`: ['tradeability_class', 'risk_acceptable', 'entry_ready', 'entry_state', 'decision', 'decision_reasons']
- `preferred_snapshot_semantics`: ['same run_id / asof context as published run JSON', 'one row per setup candidate before final symbol dedup OR after symbol dedup but before top20 cap', 'stable score fields from the ranking stage']
- `next_best_place_to_snapshot`: ['snapshots/runtime', 'snapshots/history']

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
