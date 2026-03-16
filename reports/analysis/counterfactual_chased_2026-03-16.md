# Counterfactual Chased Threshold Analysis

- Generated: 2026-03-16T12:00:25Z
- Total candidates: 140
- Reported chased: 114
- Reclassified from reported chased: 66
- Label-only reclassifications: 66
- Report vs recomputed entry_state mismatches: 0

## Thresholds used

- pullback: 8.00%
- reversal: 12.00%
- breakout: 5.00%
- other: 3.00%

## Non-timing blocker counts

- risk_reward_unattractive: 111
- tradeability_marginal: 110
- entry_not_confirmed: 55
- retest_not_reclaimed: 48
- btc_regime_caution: 43
- rebound_not_confirmed: 7
- price_past_target_1: 2

## Setup breakdown

| Setup | Candidates | Reported chased | Reclassified | Threshold |
|---|---:|---:|---:|---:|
| pullback | 44 | 30 | 14 | 8.00% |
| reversal | 96 | 84 | 52 | 12.00% |

## Focus Symbol: TAOUSDT

- Rows: 5
- Reported chased: 4
- Reclassified: 1
- By setup bucket: {"pullback": 3, "reversal": 2}
- Reason-implied floors: {"NO_TRADE": 3, "UNBLOCKED_BY_REASONS": 1, "WAIT": 1}

| Date | Setup | Decision | Dist % | Reported | Hypothetical | RR2 | Stop | Entry ready | Tradeability | BTC regime | Floor | Non-timing reasons |
|---|---|---|---:|---|---|---:|---:|---|---|---|---|---|
| 2026-03-11 | pullback | NO_TRADE | 2.19 | late | late |  | 180.1994 | true | DIRECT_OK | RISK_OFF | NO_TRADE | risk_reward_unattractive, btc_regime_caution |
| 2026-03-12 | reversal | NO_TRADE | 16.07 | chased | chased |  | 153.3617 | true | DIRECT_OK | RISK_OFF | NO_TRADE | risk_reward_unattractive |
| 2026-03-13 | reversal | NO_TRADE | 21.70 | chased | chased | 2.00 | 143.0000 | true | DIRECT_OK | RISK_OFF | NO_TRADE | risk_reward_unattractive |
| 2026-03-14 | pullback | WAIT | 6.92 | chased | late | 2.00 | 205.4515 | true | DIRECT_OK | RISK_OFF | UNBLOCKED_BY_REASONS |  |
| 2026-03-15 | pullback | WAIT | 15.01 | chased | chased | 2.00 | 212.8481 | true | DIRECT_OK | RISK_OFF | WAIT | btc_regime_caution |

