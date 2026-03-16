# Chased Entry Analysis

- Generated: 2026-03-16T08:52:16Z
- Runs analyzed: 7
- Total candidates: 140
- Source files: 2026-03-10.json, 2026-03-11.json, 2026-03-12.json, 2026-03-13.json, 2026-03-14.json, 2026-03-15.json, 2026-03-16.json

## Setup join diagnostics

- Candidates with setup already present: 0
- Candidates joined via unique symbol match: 91
- Candidates joined via multi-match heuristic: 14
- Candidates unresolved after join: 35
- Unresolved symbols: 1INCHUSDT, ADAUSDT, ALGOUSDT, ATHUSDT, BANANAS31USDT, BBUSDT, BERAUSDT, BNBUSDT, DEEPUSDT, ETHFIUSDT, FLOWUSDT, FORMUSDT, JSTUSDT, KERNELUSDT, LINKUSDT, LUNCUSDT, MELANIAUSDT, MOODENGUSDT, PENGUUSDT, PIUSDT, PIXELUSDT, POPCATUSDT, RIVERUSDT, SUIUSDT, TIAUSDT

## Overall entry-state counts

- chased: 114
- late: 14
- early: 12

## Overall decision counts

- NO_TRADE: 113
- WAIT: 26
- ENTER: 1

## Overall distance buckets (all)

| Bucket | Count |
|---|---:|
| 0-3% | 14 |
| 3-7% | 39 |
| 7-15% | 46 |
| >15% | 29 |
| unknown | 12 |

## Overall distance buckets (chased only)

| Bucket | Count |
|---|---:|
| 0-3% | 0 |
| 3-7% | 39 |
| 7-15% | 46 |
| >15% | 29 |

## Per-run chased summary

| Date | Candidates | Chased | Chased % | Median chased distance % | P75 chased distance % | Pullback | Reversal | Breakout | Other | 0-3% | 3-7% | 7-15% | >15% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-03-10 | 20 | 17 | 85.00 | 8.50 | 17.34 | 4 | 10 | 0 | 6 | 0 | 6 | 4 | 7 |
| 2026-03-11 | 20 | 12 | 60.00 | 12.20 | 26.65 | 9 | 10 | 0 | 1 | 0 | 3 | 4 | 5 |
| 2026-03-12 | 20 | 15 | 75.00 | 11.88 | 14.89 | 6 | 10 | 0 | 4 | 0 | 2 | 9 | 4 |
| 2026-03-13 | 20 | 17 | 85.00 | 6.36 | 11.07 | 1 | 10 | 0 | 9 | 0 | 9 | 5 | 3 |
| 2026-03-14 | 20 | 17 | 85.00 | 9.17 | 13.90 | 5 | 10 | 1 | 4 | 0 | 6 | 7 | 4 |
| 2026-03-15 | 20 | 16 | 80.00 | 10.24 | 14.39 | 8 | 9 | 0 | 3 | 0 | 5 | 8 | 3 |
| 2026-03-16 | 20 | 20 | 100.00 | 7.90 | 13.65 | 2 | 10 | 0 | 8 | 0 | 8 | 9 | 3 |

## Setup breakdown

| Setup | Bucket | Candidates | Chased | Chased % | Median distance % | P75 distance % | 0-3% | 3-7% | 7-15% | >15% |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|  | other | 35 | 33 | 94.29 | 6.94 | 10.99 | 0 | 16 | 12 | 5 |
| breakout_retest_1_5d | breakout | 1 | 1 | 100.00 | 4.28 | 4.28 | 0 | 1 | 0 | 0 |
| pullback | pullback | 35 | 22 | 62.86 | 5.41 | 13.95 | 0 | 7 | 7 | 8 |
| reversal | reversal | 69 | 58 | 84.06 | 8.36 | 14.10 | 0 | 15 | 27 | 16 |

## Most common decision reasons

- entry_chased: 114
- risk_reward_unattractive: 111
- tradeability_marginal: 110
- entry_not_confirmed: 55
- retest_not_reclaimed: 48
- btc_regime_caution: 43
- entry_late: 14
- entry_too_early: 12
- rebound_not_confirmed: 7
- price_past_target_1: 2

## Sample chased candidates (overall)

| Date | Symbol | Decision | Setup | Distance % | Reasons |
|---|---|---|---|---:|---|
| 2026-03-10 | FLOWUSDT | NO_TRADE | reversal | 67.49 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | PIXELUSDT | NO_TRADE |  | 56.06 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | ARIAUSDT | NO_TRADE | pullback | 37.31 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | KERNELUSDT | NO_TRADE |  | 19.30 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-10 | BABYUSDT | NO_TRADE | reversal | 17.34 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-10 | ZROUSDT | NO_TRADE | reversal | 16.14 | risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | ETHFIUSDT | NO_TRADE |  | 15.03 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | HUMAUSDT | NO_TRADE | reversal | 12.46 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | GRASSUSDT | NO_TRADE | pullback | 8.50 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-10 | AVAXUSDT | NO_TRADE | reversal | 7.54 | risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | HSKUSDT | NO_TRADE | reversal | 7.48 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | JSTUSDT | NO_TRADE |  | 6.94 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | MNTUSDT | NO_TRADE | reversal | 5.65 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | PIUSDT | NO_TRADE | pullback | 5.10 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-10 | PLUMEUSDT | NO_TRADE | reversal | 4.54 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | SUIUSDT | NO_TRADE |  | 4.40 | risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | UNIUSDT | NO_TRADE |  | 3.01 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-11 | PIXELUSDT | NO_TRADE | pullback | 56.76 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-11 | FLOWUSDT | NO_TRADE | reversal | 46.52 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-11 | HUMAUSDT | NO_TRADE | reversal | 27.08 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |

## Pullback only

- Candidates: 35

### Entry-state counts

- chased: 22
- late: 5
- early: 8

### Decision counts

- NO_TRADE: 25
- WAIT: 10

### Distance buckets (all)

| Bucket | Count |
|---|---:|
| 0-3% | 5 |
| 3-7% | 7 |
| 7-15% | 7 |
| >15% | 8 |
| unknown | 8 |

### Distance buckets (chased only)

| Bucket | Count |
|---|---:|
| 0-3% | 0 |
| 3-7% | 7 |
| 7-15% | 7 |
| >15% | 8 |

### Per-run summary

| Date | Candidates | Chased | Chased % | Median chased distance % | P75 chased distance % | 0-3% | 3-7% | 7-15% | >15% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-03-10 | 4 | 3 | 75.00 | 8.50 | 22.91 | 0 | 1 | 1 | 1 |
| 2026-03-11 | 9 | 3 | 33.33 | 26.51 | 41.63 | 0 | 0 | 1 | 2 |
| 2026-03-12 | 6 | 4 | 66.67 | 9.90 | 12.70 | 0 | 1 | 3 | 0 |
| 2026-03-13 | 1 | 1 | 100.00 | 4.48 | 4.48 | 0 | 1 | 0 | 0 |
| 2026-03-14 | 5 | 4 | 80.00 | 18.33 | 20.88 | 0 | 1 | 0 | 3 |
| 2026-03-15 | 8 | 5 | 62.50 | 13.53 | 15.01 | 0 | 2 | 1 | 2 |
| 2026-03-16 | 2 | 2 | 100.00 | 9.65 | 12.00 | 0 | 1 | 1 | 0 |

### Most common decision reasons

- tradeability_marginal: 30
- risk_reward_unattractive: 25
- entry_chased: 22
- btc_regime_caution: 13
- entry_too_early: 8
- entry_not_confirmed: 6
- rebound_not_confirmed: 6
- entry_late: 5

### Sample chased candidates

| Date | Symbol | Decision | Setup | Distance % | Reasons |
|---|---|---|---|---:|---|
| 2026-03-10 | ARIAUSDT | NO_TRADE | pullback | 37.31 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | GRASSUSDT | NO_TRADE | pullback | 8.50 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-10 | PIUSDT | NO_TRADE | pullback | 5.10 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-11 | PIXELUSDT | NO_TRADE | pullback | 56.76 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-11 | ARIAUSDT | NO_TRADE | pullback | 26.51 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-11 | GRASSUSDT | NO_TRADE | pullback | 8.60 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-12 | PIUSDT | NO_TRADE | pullback | 13.56 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-12 | QUBICUSDT | NO_TRADE | pullback | 12.41 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-12 | HYPEUSDT | NO_TRADE | pullback | 7.40 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-12 | GRASSUSDT | NO_TRADE | pullback | 5.41 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |

## Reversal only

- Candidates: 69

### Entry-state counts

- chased: 58
- late: 7
- early: 4

### Decision counts

- NO_TRADE: 59
- WAIT: 10

### Distance buckets (all)

| Bucket | Count |
|---|---:|
| 0-3% | 7 |
| 3-7% | 15 |
| 7-15% | 27 |
| >15% | 16 |
| unknown | 4 |

### Distance buckets (chased only)

| Bucket | Count |
|---|---:|
| 0-3% | 0 |
| 3-7% | 15 |
| 7-15% | 27 |
| >15% | 16 |

### Per-run summary

| Date | Candidates | Chased | Chased % | Median chased distance % | P75 chased distance % | 0-3% | 3-7% | 7-15% | >15% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-03-10 | 10 | 8 | 80.00 | 10.00 | 16.44 | 0 | 2 | 3 | 3 |
| 2026-03-11 | 10 | 8 | 80.00 | 12.20 | 24.77 | 0 | 2 | 3 | 3 |
| 2026-03-12 | 10 | 8 | 80.00 | 12.83 | 16.02 | 0 | 1 | 4 | 3 |
| 2026-03-13 | 10 | 8 | 80.00 | 11.65 | 19.68 | 0 | 2 | 3 | 3 |
| 2026-03-14 | 10 | 8 | 80.00 | 6.47 | 9.18 | 0 | 4 | 4 | 0 |
| 2026-03-15 | 9 | 8 | 88.89 | 10.24 | 14.15 | 0 | 1 | 6 | 1 |
| 2026-03-16 | 10 | 10 | 100.00 | 11.51 | 14.69 | 0 | 3 | 4 | 3 |

### Most common decision reasons

- entry_chased: 58
- risk_reward_unattractive: 57
- tradeability_marginal: 52
- entry_not_confirmed: 30
- retest_not_reclaimed: 30
- btc_regime_caution: 20
- entry_late: 7
- entry_too_early: 4
- price_past_target_1: 2

### Sample chased candidates

| Date | Symbol | Decision | Setup | Distance % | Reasons |
|---|---|---|---|---:|---|
| 2026-03-10 | FLOWUSDT | NO_TRADE | reversal | 67.49 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | BABYUSDT | NO_TRADE | reversal | 17.34 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-10 | ZROUSDT | NO_TRADE | reversal | 16.14 | risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | HUMAUSDT | NO_TRADE | reversal | 12.46 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | AVAXUSDT | NO_TRADE | reversal | 7.54 | risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | HSKUSDT | NO_TRADE | reversal | 7.48 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | MNTUSDT | NO_TRADE | reversal | 5.65 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | PLUMEUSDT | NO_TRADE | reversal | 4.54 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-11 | FLOWUSDT | NO_TRADE | reversal | 46.52 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-11 | HUMAUSDT | NO_TRADE | reversal | 27.08 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |

## Breakout only

- Candidates: 1

### Entry-state counts

- chased: 1

### Decision counts

- NO_TRADE: 1

### Distance buckets (all)

| Bucket | Count |
|---|---:|
| 0-3% | 0 |
| 3-7% | 1 |
| 7-15% | 0 |
| >15% | 0 |

### Distance buckets (chased only)

| Bucket | Count |
|---|---:|
| 0-3% | 0 |
| 3-7% | 1 |
| 7-15% | 0 |
| >15% | 0 |

### Per-run summary

| Date | Candidates | Chased | Chased % | Median chased distance % | P75 chased distance % | 0-3% | 3-7% | 7-15% | >15% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-03-14 | 1 | 1 | 100.00 | 4.28 | 4.28 | 0 | 1 | 0 | 0 |

### Most common decision reasons

- tradeability_marginal: 1
- risk_reward_unattractive: 1
- entry_chased: 1

### Sample chased candidates

| Date | Symbol | Decision | Setup | Distance % | Reasons |
|---|---|---|---|---:|---|
| 2026-03-14 | JSTUSDT | NO_TRADE | breakout_retest_1_5d | 4.28 | tradeability_marginal, risk_reward_unattractive, entry_chased |

## Other only

- Candidates: 35

### Entry-state counts

- chased: 33
- late: 2

### Decision counts

- NO_TRADE: 28
- WAIT: 6
- ENTER: 1

### Distance buckets (all)

| Bucket | Count |
|---|---:|
| 0-3% | 2 |
| 3-7% | 16 |
| 7-15% | 12 |
| >15% | 5 |

### Distance buckets (chased only)

| Bucket | Count |
|---|---:|
| 0-3% | 0 |
| 3-7% | 16 |
| 7-15% | 12 |
| >15% | 5 |

### Per-run summary

| Date | Candidates | Chased | Chased % | Median chased distance % | P75 chased distance % | 0-3% | 3-7% | 7-15% | >15% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 2026-03-10 | 6 | 6 | 100.00 | 10.99 | 18.23 | 0 | 3 | 0 | 3 |
| 2026-03-11 | 1 | 1 | 100.00 | 5.77 | 5.77 | 0 | 1 | 0 | 0 |
| 2026-03-12 | 4 | 3 | 75.00 | 11.46 | 18.45 | 0 | 0 | 2 | 1 |
| 2026-03-13 | 9 | 8 | 88.89 | 5.78 | 6.59 | 0 | 6 | 2 | 0 |
| 2026-03-14 | 4 | 4 | 100.00 | 11.55 | 15.39 | 0 | 0 | 3 | 1 |
| 2026-03-15 | 3 | 3 | 100.00 | 5.59 | 10.08 | 0 | 2 | 1 | 0 |
| 2026-03-16 | 8 | 8 | 100.00 | 7.01 | 8.73 | 0 | 4 | 4 | 0 |

### Most common decision reasons

- entry_chased: 33
- risk_reward_unattractive: 28
- tradeability_marginal: 27
- entry_not_confirmed: 19
- retest_not_reclaimed: 18
- btc_regime_caution: 10
- entry_late: 2
- rebound_not_confirmed: 1

### Sample chased candidates

| Date | Symbol | Decision | Setup | Distance % | Reasons |
|---|---|---|---|---:|---|
| 2026-03-10 | PIXELUSDT | NO_TRADE |  | 56.06 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | KERNELUSDT | NO_TRADE |  | 19.30 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-10 | ETHFIUSDT | NO_TRADE |  | 15.03 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | JSTUSDT | NO_TRADE |  | 6.94 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_chased |
| 2026-03-10 | SUIUSDT | NO_TRADE |  | 4.40 | risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-10 | UNIUSDT | NO_TRADE |  | 3.01 | tradeability_marginal, risk_reward_unattractive, btc_regime_caution, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-11 | PIUSDT | NO_TRADE |  | 5.77 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, rebound_not_confirmed, entry_chased |
| 2026-03-12 | FLOWUSDT | NO_TRADE |  | 25.43 | tradeability_marginal, risk_reward_unattractive, entry_not_confirmed, retest_not_reclaimed, entry_chased |
| 2026-03-12 | FORMUSDT | NO_TRADE |  | 11.46 | tradeability_marginal, risk_reward_unattractive, entry_chased |
| 2026-03-12 | ETHFIUSDT | NO_TRADE |  | 9.31 | tradeability_marginal, risk_reward_unattractive, entry_chased |

