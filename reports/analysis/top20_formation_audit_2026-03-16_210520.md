# Top20 Formation Audit

- Generated at UTC: `2026-03-16T21:05:20Z`
- Runs analyzed: `5`

## Aggregate summary

- `runs_analyzed`: 5
- `total_top20_slots`: 100
- `decision_counts`: {'ENTER': 1, 'NO_TRADE': 67, 'WAIT': 32}
- `setup_type_counts`: {'pullback': 30, 'reversal': 70}
- `tradeability_class_counts`: {'DIRECT_OK': 23, 'MARGINAL': 77}
- `entry_state_counts`: {'chased': 85, 'early': 7, 'late': 8}
- `risk_acceptable_true_total`: 36
- `entry_eligible_tradeability_total`: 23
- `risk_ok_and_entry_eligible_total`: 14
- `marginal_share_pct`: 77.0
- `risk_ok_share_pct`: 36.0
- `entry_eligible_share_pct`: 23.0
- `risk_ok_entry_eligible_share_pct`: 14.0
- `ordering_violations_total`: 0
- `runs_with_optional_upstream_data`: 0

## Run `2026-03-16_1773675009352`

- Timestamp UTC: `2026-03-16T15:30:09Z`
- Schema: `6.3.0`
- Source file: `reports/2026-03-16.json`

### Visible Top20 signals
- `top20_size`: 20
- `decision_counts`: {'NO_TRADE': 7, 'WAIT': 13}
- `setup_type_counts`: {'pullback': 4, 'reversal': 16}
- `tradeability_class_counts`: {'DIRECT_OK': 7, 'MARGINAL': 13}
- `entry_state_counts`: {'chased': 20}
- `risk_acceptable_true`: 14
- `entry_eligible_tradeability`: 7
- `risk_ok_and_entry_eligible`: 6
- `global_score_all`: {'count': 20, 'min': 56.584, 'median': 59.868, 'max': 75.904, 'mean': 62.82}
- `setup_score_all`: {'count': 20, 'min': 64.8, 'median': 74.1, 'max': 94.88, 'mean': 76.875}
- `global_score_by_setup_type`: {'pullback': {'count': 4, 'min': 58.32, 'median': 59.04, 'max': 61.2, 'mean': 59.4}, 'reversal': {'count': 16, 'min': 56.584, 'median': 60.496, 'max': 75.904, 'mean': 63.675}}
- `setup_concentration`: {'top_share_pct': 80.0, 'effective_unique_setups': 1.4706}
- `marginal_share_pct`: 65.0
- `risk_ok_share_pct`: 70.0
- `entry_eligible_share_pct`: 35.0
- `risk_ok_entry_eligible_share_pct`: 30.0

### Ordering violations
- none

### Optional upstream arrays found
- none

### Upstream inclusion audit
_No larger upstream candidate array found in this run JSON. Full inclusion audit not possible from this artifact alone._

### Published Top20 rows
| rank | symbol | decision | setup | tradeability | risk_ok | entry_ready | entry_state | global_score | reasons |
|---:|---|---|---|---|---:|---:|---|---:|---|
| 1 | CAKEUSDT | WAIT | reversal | DIRECT_OK | True | True | chased | 75.904 | effective_rr_insufficient, entry_chased |
| 2 | NEOUSDT | WAIT | reversal | MARGINAL | True | True | chased | 75.288 | tradeability_marginal, entry_chased |
| 3 | BBUSDT | WAIT | reversal | MARGINAL | True | False | chased | 67.592 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 4 | SUSDT | WAIT | reversal | MARGINAL | True | False | chased | 65.488 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 5 | EIGENUSDT | WAIT | reversal | DIRECT_OK | True | False | chased | 65.472 | entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 6 | BONKUSDT | WAIT | reversal | MARGINAL | True | False | chased | 61.016 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 7 | ETCUSDT | WAIT | reversal | DIRECT_OK | True | False | chased | 59.976 | entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 8 | KASUSDT | WAIT | reversal | MARGINAL | True | False | chased | 59.392 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 9 | ZENUSDT | WAIT | reversal | MARGINAL | True | False | chased | 59.168 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 10 | QUBICUSDT | WAIT | pullback | MARGINAL | True | True | chased | 58.32 | tradeability_marginal, entry_chased |
| 11 | TAOUSDT | WAIT | pullback | DIRECT_OK | True | True | chased | 58.32 | entry_chased |
| 12 | FARTCOINUSDT | WAIT | reversal | MARGINAL | True | False | chased | 58.032 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 13 | ORDIUSDT | WAIT | reversal | DIRECT_OK | True | False | chased | 57.648 | entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 14 | CFXUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 72.688 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 15 | FETUSDT | NO_TRADE | reversal | DIRECT_OK | True | True | chased | 68.992 | price_past_target_1, entry_chased |
| 16 | RIVERUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 61.2 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 17 | AVAXUSDT | NO_TRADE | pullback | DIRECT_OK | False | False | chased | 59.76 | risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, rebound_not_confirmed, entry_chased |
| 18 | BERAUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 58.488 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 19 | PENGUUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 57.072 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 20 | MOODENGUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 56.584 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |

## Run `2026-03-15_1773553334743`

- Timestamp UTC: `2026-03-15T05:42:14Z`
- Schema: `6.3.0`
- Source file: `reports/2026-03-15.json`

### Visible Top20 signals
- `top20_size`: 20
- `decision_counts`: {'NO_TRADE': 13, 'WAIT': 7}
- `setup_type_counts`: {'pullback': 12, 'reversal': 8}
- `tradeability_class_counts`: {'DIRECT_OK': 4, 'MARGINAL': 16}
- `entry_state_counts`: {'chased': 16, 'early': 3, 'late': 1}
- `risk_acceptable_true`: 9
- `entry_eligible_tradeability`: 4
- `risk_ok_and_entry_eligible`: 4
- `global_score_all`: {'count': 20, 'min': 54.0, 'median': 60.373, 'max': 74.416, 'mean': 60.72325}
- `setup_score_all`: {'count': 20, 'min': 60.0, 'median': 68.52, 'max': 93.02, 'mean': 70.9575}
- `global_score_by_setup_type`: {'pullback': {'count': 12, 'min': 54.0, 'median': 59.121, 'max': 68.4, 'mean': 59.35875}, 'reversal': {'count': 8, 'min': 55.232, 'median': 61.852, 'max': 74.416, 'mean': 62.77}}
- `setup_concentration`: {'top_share_pct': 60.0, 'effective_unique_setups': 1.9231}
- `marginal_share_pct`: 80.0
- `risk_ok_share_pct`: 45.0
- `entry_eligible_share_pct`: 20.0
- `risk_ok_entry_eligible_share_pct`: 20.0

### Ordering violations
- none

### Optional upstream arrays found
- none

### Upstream inclusion audit
_No larger upstream candidate array found in this run JSON. Full inclusion audit not possible from this artifact alone._

### Published Top20 rows
| rank | symbol | decision | setup | tradeability | risk_ok | entry_ready | entry_state | global_score | reasons |
|---:|---|---|---|---|---:|---:|---|---:|---|
| 1 | CUSDT | WAIT | pullback | MARGINAL | True | True | chased | 61.2 | tradeability_marginal, btc_regime_caution, entry_chased |
| 2 | RENDERUSDT | WAIT | pullback | DIRECT_OK | True | True | chased | 61.2 | btc_regime_caution, entry_chased |
| 3 | TAOUSDT | WAIT | pullback | DIRECT_OK | True | True | chased | 61.2 | btc_regime_caution, entry_chased |
| 4 | SUSDT | WAIT | reversal | MARGINAL | True | False | chased | 60.824 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 5 | DEXEUSDT | WAIT | pullback | MARGINAL | True | True | chased | 58.32 | tradeability_marginal, entry_chased |
| 6 | BANANAS31USDT | WAIT | pullback | MARGINAL | True | True | chased | 54.0 | tradeability_marginal, entry_chased |
| 7 | RIVERUSDT | WAIT | pullback | MARGINAL | True | True | chased | 54.0 | tradeability_marginal, entry_chased |
| 8 | SPKUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 74.416 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 9 | FETUSDT | NO_TRADE | pullback | DIRECT_OK | True | True | chased | 68.4 | price_past_target_1, entry_chased |
| 10 | MNTUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 68.272 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 11 | RSRUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 65.504 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 12 | PIUSDT | NO_TRADE | pullback | MARGINAL | False | False | early | 64.8 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, rebound_not_confirmed, entry_too_early |
| 13 | BSVUSDT | NO_TRADE | reversal | MARGINAL | False | False | late | 62.88 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_late |
| 14 | BDXUSDT | NO_TRADE | pullback | MARGINAL | False | False | early | 59.922 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, rebound_not_confirmed, entry_too_early |
| 15 | BERAUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 59.032 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 16 | ALLOUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 58.32 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 17 | STABLEUSDT | NO_TRADE | pullback | MARGINAL | False | False | early | 56.943 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, rebound_not_confirmed, entry_too_early |
| 18 | TRUMPUSDT | NO_TRADE | reversal | DIRECT_OK | True | True | chased | 56.0 | price_past_target_1, entry_chased |
| 19 | LAUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 55.232 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 20 | PIXELUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 54.0 | tradeability_marginal, risk_reward_unattractive, entry_chased |

## Run `2026-03-14_1773483267911`

- Timestamp UTC: `2026-03-14T10:14:27Z`
- Schema: `6.3.0`
- Source file: `reports/2026-03-14.json`

### Visible Top20 signals
- `top20_size`: 20
- `decision_counts`: {'ENTER': 1, 'NO_TRADE': 12, 'WAIT': 7}
- `setup_type_counts`: {'pullback': 6, 'reversal': 14}
- `tradeability_class_counts`: {'DIRECT_OK': 4, 'MARGINAL': 16}
- `entry_state_counts`: {'chased': 17, 'early': 3}
- `risk_acceptable_true`: 8
- `entry_eligible_tradeability`: 4
- `risk_ok_and_entry_eligible`: 3
- `global_score_all`: {'count': 20, 'min': 55.44, 'median': 61.692, 'max': 73.688, 'mean': 62.1976}
- `setup_score_all`: {'count': 20, 'min': 61.6, 'median': 76.58, 'max': 92.11, 'mean': 75.297}
- `global_score_by_setup_type`: {'pullback': {'count': 6, 'min': 55.44, 'median': 59.76, 'max': 61.2, 'mean': 58.8}, 'reversal': {'count': 14, 'min': 56.0, 'median': 63.744, 'max': 73.688, 'mean': 63.653714}}
- `setup_concentration`: {'top_share_pct': 70.0, 'effective_unique_setups': 1.7241}
- `marginal_share_pct`: 80.0
- `risk_ok_share_pct`: 40.0
- `entry_eligible_share_pct`: 20.0
- `risk_ok_entry_eligible_share_pct`: 15.0

### Ordering violations
- none

### Optional upstream arrays found
- none

### Upstream inclusion audit
_No larger upstream candidate array found in this run JSON. Full inclusion audit not possible from this artifact alone._

### Published Top20 rows
| rank | symbol | decision | setup | tradeability | risk_ok | entry_ready | entry_state | global_score | reasons |
|---:|---|---|---|---|---:|---:|---|---:|---|
| 1 | TRUMPUSDT | ENTER | reversal | DIRECT_OK | True | True | chased | 56.0 | entry_chased |
| 2 | GRTUSDT | WAIT | reversal | MARGINAL | True | False | early | 63.968 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_too_early |
| 3 | TURBOUSDT | WAIT | reversal | MARGINAL | True | False | chased | 62.392 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 4 | ALGOUSDT | WAIT | reversal | DIRECT_OK | True | False | chased | 62.184 | entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 5 | RIVERUSDT | WAIT | pullback | MARGINAL | True | True | chased | 61.2 | tradeability_marginal, btc_regime_caution, entry_chased |
| 6 | MELANIAUSDT | WAIT | reversal | MARGINAL | True | True | chased | 60.344 | tradeability_marginal, entry_chased |
| 7 | TAOUSDT | WAIT | pullback | DIRECT_OK | True | True | chased | 58.32 | entry_chased |
| 8 | BANANAS31USDT | WAIT | pullback | MARGINAL | True | True | chased | 55.44 | tradeability_marginal, entry_chased |
| 9 | FETUSDT | NO_TRADE | reversal | DIRECT_OK | False | True | chased | 73.688 | risk_reward_unattractive, entry_chased |
| 10 | CFXUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 67.736 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 11 | RSRUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 66.512 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 12 | MEWUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 66.488 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 13 | MOODENGUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 66.088 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 14 | BBUSDT | NO_TRADE | reversal | MARGINAL | False | False | early | 65.936 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_too_early |
| 15 | HUMAUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 63.52 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 16 | NAORISUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 61.2 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 17 | RESOLVUSDT | NO_TRADE | pullback | MARGINAL | False | False | early | 61.2 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, rebound_not_confirmed, entry_too_early |
| 18 | DEEPUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 59.448 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 19 | BERAUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 56.848 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 20 | JSTUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 55.44 | tradeability_marginal, risk_reward_unattractive, entry_chased |

## Run `2026-03-13_1773431126642`

- Timestamp UTC: `2026-03-13T19:45:26Z`
- Schema: `6.3.0`
- Source file: `reports/2026-03-13.json`

### Visible Top20 signals
- `top20_size`: 20
- `decision_counts`: {'NO_TRADE': 15, 'WAIT': 5}
- `setup_type_counts`: {'pullback': 1, 'reversal': 19}
- `tradeability_class_counts`: {'DIRECT_OK': 6, 'MARGINAL': 14}
- `entry_state_counts`: {'chased': 17, 'late': 3}
- `risk_acceptable_true`: 5
- `entry_eligible_tradeability`: 6
- `risk_ok_and_entry_eligible`: 1
- `global_score_all`: {'count': 20, 'min': 69.08, 'median': 72.515, 'max': 92.86, 'mean': 76.5185}
- `setup_score_all`: {'count': 20, 'min': 69.08, 'median': 72.515, 'max': 92.86, 'mean': 76.5185}
- `global_score_by_setup_type`: {'pullback': {'count': 1, 'min': 71.58, 'median': 71.58, 'max': 71.58, 'mean': 71.58}, 'reversal': {'count': 19, 'min': 69.08, 'median': 72.67, 'max': 92.86, 'mean': 76.778421}}
- `setup_concentration`: {'top_share_pct': 95.0, 'effective_unique_setups': 1.105}
- `marginal_share_pct`: 70.0
- `risk_ok_share_pct`: 25.0
- `entry_eligible_share_pct`: 30.0
- `risk_ok_entry_eligible_share_pct`: 5.0

### Ordering violations
- none

### Optional upstream arrays found
- none

### Upstream inclusion audit
_No larger upstream candidate array found in this run JSON. Full inclusion audit not possible from this artifact alone._

### Published Top20 rows
| rank | symbol | decision | setup | tradeability | risk_ok | entry_ready | entry_state | global_score | reasons |
|---:|---|---|---|---|---:|---:|---|---:|---|
| 1 | TURBOUSDT | WAIT | reversal | MARGINAL | True | True | chased | 89.99 | tradeability_marginal, entry_chased |
| 2 | GRTUSDT | WAIT | reversal | MARGINAL | True | False | late | 72.67 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_late |
| 3 | STABLEUSDT | WAIT | pullback | MARGINAL | True | True | chased | 71.58 | tradeability_marginal, entry_chased |
| 4 | ALGOUSDT | WAIT | reversal | MARGINAL | True | False | chased | 70.99 | tradeability_marginal, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 5 | BNBUSDT | WAIT | reversal | DIRECT_OK | True | False | chased | 70.22 | entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 6 | TAOUSDT | NO_TRADE | reversal | DIRECT_OK | False | True | chased | 92.86 | risk_reward_unattractive, entry_chased |
| 7 | SATSUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 92.54 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 8 | RENDERUSDT | NO_TRADE | reversal | DIRECT_OK | False | True | chased | 92.2 | risk_reward_unattractive, entry_chased |
| 9 | ASTERUSDT | NO_TRADE | reversal | DIRECT_OK | False | True | late | 81.29 | risk_reward_unattractive, entry_late |
| 10 | AVAXUSDT | NO_TRADE | reversal | DIRECT_OK | False | False | chased | 79.61 | risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 11 | DEEPUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 78.37 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 12 | VIRTUALUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 74.19 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 13 | OKBUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 73.54 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 14 | BBUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 72.36 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 15 | LUNCUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 70.48 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 16 | POPCATUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 70.45 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 17 | MOODENGUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 69.41 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 18 | TIAUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 69.41 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 19 | PENGUUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 69.13 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 20 | LINKUSDT | NO_TRADE | reversal | DIRECT_OK | False | False | late | 69.08 | risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_late |

## Run `2026-03-12_1773335486896`

- Timestamp UTC: `2026-03-12T17:11:26Z`
- Schema: `5.7.0`
- Source file: `reports/2026-03-12.json`

### Visible Top20 signals
- `top20_size`: 20
- `decision_counts`: {'NO_TRADE': 20}
- `setup_type_counts`: {'pullback': 7, 'reversal': 13}
- `tradeability_class_counts`: {'DIRECT_OK': 2, 'MARGINAL': 18}
- `entry_state_counts`: {'chased': 15, 'early': 1, 'late': 4}
- `risk_acceptable_true`: 0
- `entry_eligible_tradeability`: 2
- `risk_ok_and_entry_eligible`: 0
- `global_score_all`: {'count': 20, 'min': 60.15, 'median': 66.435, 'max': 93.78, 'mean': 70.181}
- `setup_score_all`: {'count': 20, 'min': 60.15, 'median': 66.435, 'max': 93.78, 'mean': 70.181}
- `global_score_by_setup_type`: {'pullback': {'count': 7, 'min': 62.4, 'median': 64.8, 'max': 75.19, 'mean': 66.654286}, 'reversal': {'count': 13, 'min': 60.15, 'median': 66.62, 'max': 93.78, 'mean': 72.08}}
- `setup_concentration`: {'top_share_pct': 65.0, 'effective_unique_setups': 1.8349}
- `marginal_share_pct`: 90.0
- `risk_ok_share_pct`: 0.0
- `entry_eligible_share_pct`: 10.0
- `risk_ok_entry_eligible_share_pct`: 0.0

### Ordering violations
- none

### Optional upstream arrays found
- none

### Upstream inclusion audit
_No larger upstream candidate array found in this run JSON. Full inclusion audit not possible from this artifact alone._

### Published Top20 rows
| rank | symbol | decision | setup | tradeability | risk_ok | entry_ready | entry_state | global_score | reasons |
|---:|---|---|---|---|---:|---:|---|---:|---|
| 1 | ICPUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 93.78 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2 | DEEPUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 93.04 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 3 | ILVUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 82.68 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 4 | SPKUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 79.22 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 5 | COMPUSDT | NO_TRADE | reversal | MARGINAL | False | False | late | 78.17 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_late |
| 6 | RENDERUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 75.19 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 7 | PENDLEUSDT | NO_TRADE | reversal | MARGINAL | False | False | early | 68.46 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_too_early |
| 8 | GRASSUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 68.0 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 9 | QUBICUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 68.0 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 10 | NEXOUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 66.62 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 11 | BABYUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 66.25 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 12 | HYPEUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 64.8 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 13 | PIUSDT | NO_TRADE | pullback | MARGINAL | False | True | chased | 64.8 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 14 | TAOUSDT | NO_TRADE | reversal | DIRECT_OK | False | True | chased | 64.38 | risk_reward_unattractive, entry_chased |
| 15 | BDXUSDT | NO_TRADE | pullback | MARGINAL | False | True | late | 63.39 | tradeability_marginal, risk_reward_unattractive, entry_late |
| 16 | STABLEUSDT | NO_TRADE | pullback | MARGINAL | False | True | late | 62.4 | tradeability_marginal, risk_reward_unattractive, entry_late |
| 17 | TRXUSDT | NO_TRADE | reversal | DIRECT_OK | False | True | late | 62.02 | risk_reward_unattractive, entry_late |
| 18 | FORMUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 61.25 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 19 | FLOWUSDT | NO_TRADE | reversal | MARGINAL | False | False | chased | 61.02 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 20 | ETHFIUSDT | NO_TRADE | reversal | MARGINAL | False | True | chased | 60.15 | tradeability_marginal, risk_reward_unattractive, entry_chased |
