# Post-Risk-Unlock Blocker Audit

- Generated at UTC: `2026-03-16T20:50:41Z`
- Runs analyzed: `5`

## Aggregate summary

### Waterfall sums
- `risk_acceptable_true`: 36
- `risk_acceptable_true_direct_ok`: 14
- `risk_acceptable_true_entry_eligible_tradeability`: 14
- `risk_acceptable_true_fail`: 0
- `risk_acceptable_true_marginal`: 22
- `risk_acceptable_true_tranche_ok`: 0
- `risk_acceptable_true_unknown`: 0
- `risk_ok_plus_entry_eligible_plus_entry_ready`: 9
- `risk_ok_plus_entry_eligible_plus_entry_ready_non_enter`: 8
- `timing_only_after_risk_tradeability_readiness`: 2
- `top_candidates`: 100

### Aggregate blocker buckets

#### All risk_ok non-ENTER
- `timing`: 35
- `tradeability`: 22
- `confirmation`: 16
- `btc_regime`: 4
- `late_entry_guard`: 4

#### risk_ok + entry-eligible non-ENTER
- `timing`: 13
- `confirmation`: 5
- `late_entry_guard`: 4
- `btc_regime`: 2

#### risk_ok + entry-eligible + entry_ready non-ENTER
- `timing`: 8
- `late_entry_guard`: 4
- `btc_regime`: 2

### Aggregate blocker reasons

#### All risk_ok non-ENTER
- `entry_chased`: 33
- `tradeability_marginal`: 22
- `entry_not_confirmed`: 16
- `retest_not_reclaimed`: 16
- `btc_regime_caution`: 4
- `price_past_target_1`: 3
- `effective_rr_insufficient`: 1
- `entry_late`: 1
- `entry_too_early`: 1

#### risk_ok + entry-eligible non-ENTER
- `entry_chased`: 13
- `entry_not_confirmed`: 5
- `retest_not_reclaimed`: 5
- `price_past_target_1`: 3
- `btc_regime_caution`: 2
- `effective_rr_insufficient`: 1

#### risk_ok + entry-eligible + entry_ready non-ENTER
- `entry_chased`: 8
- `price_past_target_1`: 3
- `btc_regime_caution`: 2
- `effective_rr_insufficient`: 1

## Run `2026-03-16_1773675009352`

- Timestamp UTC: `2026-03-16T15:30:09Z`
- Schema: `6.3.0`
- Source file: `reports/2026-03-16.json`

### Waterfall
- `top_candidates`: 20
- `risk_acceptable_true`: 14
- `risk_acceptable_true_direct_ok`: 6
- `risk_acceptable_true_tranche_ok`: 0
- `risk_acceptable_true_entry_eligible_tradeability`: 6
- `risk_acceptable_true_marginal`: 8
- `risk_acceptable_true_fail`: 0
- `risk_acceptable_true_unknown`: 0
- `risk_ok_plus_entry_eligible_plus_entry_ready`: 3
- `risk_ok_plus_entry_eligible_plus_entry_ready_non_enter`: 3
- `timing_only_after_risk_tradeability_readiness`: 1

### Distributions

#### decision
- `NO_TRADE`: 7
- `WAIT`: 13

#### tradeability_class
- `DIRECT_OK`: 7
- `MARGINAL`: 13

#### entry_ready
- `False`: 12
- `True`: 8

#### entry_state
- `chased`: 20

#### best_setup_type
- `pullback`: 4
- `reversal`: 16

### Post-risk blocker buckets

#### all_risk_ok_non_enter_bucket_counts
- `timing`: 14
- `confirmation`: 9
- `tradeability`: 8
- `late_entry_guard`: 2

#### risk_ok_entry_eligible_non_enter_bucket_counts
- `timing`: 6
- `confirmation`: 3
- `late_entry_guard`: 2

#### risk_ok_entry_eligible_entry_ready_non_enter_bucket_counts
- `timing`: 3
- `late_entry_guard`: 2

### Post-risk blocker reasons

#### all_risk_ok_non_enter_reason_counts
- `entry_chased`: 14
- `entry_not_confirmed`: 9
- `retest_not_reclaimed`: 9
- `tradeability_marginal`: 8
- `effective_rr_insufficient`: 1
- `price_past_target_1`: 1

#### risk_ok_entry_eligible_non_enter_reason_counts
- `entry_chased`: 6
- `entry_not_confirmed`: 3
- `retest_not_reclaimed`: 3
- `effective_rr_insufficient`: 1
- `price_past_target_1`: 1

#### risk_ok_entry_eligible_entry_ready_non_enter_reason_counts
- `entry_chased`: 3
- `effective_rr_insufficient`: 1
- `price_past_target_1`: 1

### Timing-only rows
| symbol | decision | setup | tradeability | entry_ready | entry_state | reasons |
|---|---|---|---|---:|---|---|
| TAOUSDT | WAIT | pullback | DIRECT_OK | True | chased | entry_chased |

### Clean-but-not-ENTER rows
| symbol | decision | setup | tradeability | entry_ready | entry_state | reasons |
|---|---|---|---|---:|---|---|
| CAKEUSDT | WAIT | reversal | DIRECT_OK | True | chased | effective_rr_insufficient, entry_chased |
| TAOUSDT | WAIT | pullback | DIRECT_OK | True | chased | entry_chased |
| FETUSDT | NO_TRADE | reversal | DIRECT_OK | True | chased | price_past_target_1, entry_chased |

## Run `2026-03-15_1773553334743`

- Timestamp UTC: `2026-03-15T05:42:14Z`
- Schema: `6.3.0`
- Source file: `reports/2026-03-15.json`

### Waterfall
- `top_candidates`: 20
- `risk_acceptable_true`: 9
- `risk_acceptable_true_direct_ok`: 4
- `risk_acceptable_true_tranche_ok`: 0
- `risk_acceptable_true_entry_eligible_tradeability`: 4
- `risk_acceptable_true_marginal`: 5
- `risk_acceptable_true_fail`: 0
- `risk_acceptable_true_unknown`: 0
- `risk_ok_plus_entry_eligible_plus_entry_ready`: 4
- `risk_ok_plus_entry_eligible_plus_entry_ready_non_enter`: 4
- `timing_only_after_risk_tradeability_readiness`: 0

### Distributions

#### decision
- `NO_TRADE`: 13
- `WAIT`: 7

#### tradeability_class
- `DIRECT_OK`: 4
- `MARGINAL`: 16

#### entry_ready
- `False`: 7
- `True`: 13

#### entry_state
- `chased`: 16
- `early`: 3
- `late`: 1

#### best_setup_type
- `pullback`: 12
- `reversal`: 8

### Post-risk blocker buckets

#### all_risk_ok_non_enter_bucket_counts
- `timing`: 9
- `tradeability`: 5
- `btc_regime`: 3
- `late_entry_guard`: 2
- `confirmation`: 1

#### risk_ok_entry_eligible_non_enter_bucket_counts
- `timing`: 4
- `btc_regime`: 2
- `late_entry_guard`: 2

#### risk_ok_entry_eligible_entry_ready_non_enter_bucket_counts
- `timing`: 4
- `btc_regime`: 2
- `late_entry_guard`: 2

### Post-risk blocker reasons

#### all_risk_ok_non_enter_reason_counts
- `entry_chased`: 9
- `tradeability_marginal`: 5
- `btc_regime_caution`: 3
- `price_past_target_1`: 2
- `entry_not_confirmed`: 1
- `retest_not_reclaimed`: 1

#### risk_ok_entry_eligible_non_enter_reason_counts
- `entry_chased`: 4
- `btc_regime_caution`: 2
- `price_past_target_1`: 2

#### risk_ok_entry_eligible_entry_ready_non_enter_reason_counts
- `entry_chased`: 4
- `btc_regime_caution`: 2
- `price_past_target_1`: 2

### Timing-only rows
_none_

### Clean-but-not-ENTER rows
| symbol | decision | setup | tradeability | entry_ready | entry_state | reasons |
|---|---|---|---|---:|---|---|
| RENDERUSDT | WAIT | pullback | DIRECT_OK | True | chased | btc_regime_caution, entry_chased |
| TAOUSDT | WAIT | pullback | DIRECT_OK | True | chased | btc_regime_caution, entry_chased |
| FETUSDT | NO_TRADE | pullback | DIRECT_OK | True | chased | price_past_target_1, entry_chased |
| TRUMPUSDT | NO_TRADE | reversal | DIRECT_OK | True | chased | price_past_target_1, entry_chased |

## Run `2026-03-14_1773483267911`

- Timestamp UTC: `2026-03-14T10:14:27Z`
- Schema: `6.3.0`
- Source file: `reports/2026-03-14.json`

### Waterfall
- `top_candidates`: 20
- `risk_acceptable_true`: 8
- `risk_acceptable_true_direct_ok`: 3
- `risk_acceptable_true_tranche_ok`: 0
- `risk_acceptable_true_entry_eligible_tradeability`: 3
- `risk_acceptable_true_marginal`: 5
- `risk_acceptable_true_fail`: 0
- `risk_acceptable_true_unknown`: 0
- `risk_ok_plus_entry_eligible_plus_entry_ready`: 2
- `risk_ok_plus_entry_eligible_plus_entry_ready_non_enter`: 1
- `timing_only_after_risk_tradeability_readiness`: 1

### Distributions

#### decision
- `ENTER`: 1
- `NO_TRADE`: 12
- `WAIT`: 7

#### tradeability_class
- `DIRECT_OK`: 4
- `MARGINAL`: 16

#### entry_ready
- `False`: 8
- `True`: 12

#### entry_state
- `chased`: 17
- `early`: 3

#### best_setup_type
- `pullback`: 6
- `reversal`: 14

### Post-risk blocker buckets

#### all_risk_ok_non_enter_bucket_counts
- `timing`: 7
- `tradeability`: 5
- `confirmation`: 3
- `btc_regime`: 1

#### risk_ok_entry_eligible_non_enter_bucket_counts
- `timing`: 2
- `confirmation`: 1

#### risk_ok_entry_eligible_entry_ready_non_enter_bucket_counts
- `timing`: 1

### Post-risk blocker reasons

#### all_risk_ok_non_enter_reason_counts
- `entry_chased`: 6
- `tradeability_marginal`: 5
- `entry_not_confirmed`: 3
- `retest_not_reclaimed`: 3
- `btc_regime_caution`: 1
- `entry_too_early`: 1

#### risk_ok_entry_eligible_non_enter_reason_counts
- `entry_chased`: 2
- `entry_not_confirmed`: 1
- `retest_not_reclaimed`: 1

#### risk_ok_entry_eligible_entry_ready_non_enter_reason_counts
- `entry_chased`: 1

### Timing-only rows
| symbol | decision | setup | tradeability | entry_ready | entry_state | reasons |
|---|---|---|---|---:|---|---|
| TAOUSDT | WAIT | pullback | DIRECT_OK | True | chased | entry_chased |

### Clean-but-not-ENTER rows
| symbol | decision | setup | tradeability | entry_ready | entry_state | reasons |
|---|---|---|---|---:|---|---|
| TAOUSDT | WAIT | pullback | DIRECT_OK | True | chased | entry_chased |

## Run `2026-03-13_1773431126642`

- Timestamp UTC: `2026-03-13T19:45:26Z`
- Schema: `6.3.0`
- Source file: `reports/2026-03-13.json`

### Waterfall
- `top_candidates`: 20
- `risk_acceptable_true`: 5
- `risk_acceptable_true_direct_ok`: 1
- `risk_acceptable_true_tranche_ok`: 0
- `risk_acceptable_true_entry_eligible_tradeability`: 1
- `risk_acceptable_true_marginal`: 4
- `risk_acceptable_true_fail`: 0
- `risk_acceptable_true_unknown`: 0
- `risk_ok_plus_entry_eligible_plus_entry_ready`: 0
- `risk_ok_plus_entry_eligible_plus_entry_ready_non_enter`: 0
- `timing_only_after_risk_tradeability_readiness`: 0

### Distributions

#### decision
- `NO_TRADE`: 15
- `WAIT`: 5

#### tradeability_class
- `DIRECT_OK`: 6
- `MARGINAL`: 14

#### entry_ready
- `False`: 10
- `True`: 10

#### entry_state
- `chased`: 17
- `late`: 3

#### best_setup_type
- `pullback`: 1
- `reversal`: 19

### Post-risk blocker buckets

#### all_risk_ok_non_enter_bucket_counts
- `timing`: 5
- `tradeability`: 4
- `confirmation`: 3

#### risk_ok_entry_eligible_non_enter_bucket_counts
- `confirmation`: 1
- `timing`: 1

#### risk_ok_entry_eligible_entry_ready_non_enter_bucket_counts
- none

### Post-risk blocker reasons

#### all_risk_ok_non_enter_reason_counts
- `entry_chased`: 4
- `tradeability_marginal`: 4
- `entry_not_confirmed`: 3
- `retest_not_reclaimed`: 3
- `entry_late`: 1

#### risk_ok_entry_eligible_non_enter_reason_counts
- `entry_chased`: 1
- `entry_not_confirmed`: 1
- `retest_not_reclaimed`: 1

#### risk_ok_entry_eligible_entry_ready_non_enter_reason_counts
- none

### Timing-only rows
_none_

### Clean-but-not-ENTER rows
_none_

## Run `2026-03-12_1773335486896`

- Timestamp UTC: `2026-03-12T17:11:26Z`
- Schema: `5.7.0`
- Source file: `reports/2026-03-12.json`

### Waterfall
- `top_candidates`: 20
- `risk_acceptable_true`: 0
- `risk_acceptable_true_direct_ok`: 0
- `risk_acceptable_true_tranche_ok`: 0
- `risk_acceptable_true_entry_eligible_tradeability`: 0
- `risk_acceptable_true_marginal`: 0
- `risk_acceptable_true_fail`: 0
- `risk_acceptable_true_unknown`: 0
- `risk_ok_plus_entry_eligible_plus_entry_ready`: 0
- `risk_ok_plus_entry_eligible_plus_entry_ready_non_enter`: 0
- `timing_only_after_risk_tradeability_readiness`: 0

### Distributions

#### decision
- `NO_TRADE`: 20

#### tradeability_class
- `DIRECT_OK`: 2
- `MARGINAL`: 18

#### entry_ready
- `False`: 4
- `True`: 16

#### entry_state
- `chased`: 15
- `early`: 1
- `late`: 4

#### best_setup_type
- `pullback`: 7
- `reversal`: 13

### Post-risk blocker buckets

#### all_risk_ok_non_enter_bucket_counts
- none

#### risk_ok_entry_eligible_non_enter_bucket_counts
- none

#### risk_ok_entry_eligible_entry_ready_non_enter_bucket_counts
- none

### Post-risk blocker reasons

#### all_risk_ok_non_enter_reason_counts
- none

#### risk_ok_entry_eligible_non_enter_reason_counts
- none

#### risk_ok_entry_eligible_entry_ready_non_enter_reason_counts
- none

### Timing-only rows
_none_

### Clean-but-not-ENTER rows
_none_
