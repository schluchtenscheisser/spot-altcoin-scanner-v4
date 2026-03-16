# Counterfactual Chased Threshold Analysis

- Generated: 2026-03-16T09:25:17.142951+00:00
- Current threshold: 3.0%
- Hypothetical thresholds: pullback=8.0%, reversal=12.0%, breakout=5.0%, default=3.0%

## Headline findings

- Total candidates: 140
- Reclassified from reported chased: 66
- Label-only reclassifications in current architecture: 66
- Report vs recomputed entry_state mismatches: 0

## Decision counts

- NO_TRADE: 113
- WAIT: 26
- ENTER: 1

## Entry-state counts

### Reported

- chased: 114
- late: 14
- early: 12

### Recomputed with current threshold

- chased: 114
- late: 14
- early: 12

### Hypothetical

- chased: 48
- late: 80
- early: 12

## Reason-implied floor counts

- NO_TRADE: 113
- WAIT: 24
- UNBLOCKED_BY_REASONS: 3

## Most common hard blockers

- risk_reward_unattractive: 111
- price_past_target_1: 2

## Most common wait-level blockers

- tradeability_marginal: 110
- entry_not_confirmed: 55
- retest_not_reclaimed: 48
- btc_regime_caution: 43
- rebound_not_confirmed: 7

## Setup breakdown

| Setup | Candidates | Reported chased | Reclassified | State mismatches | Reason floor: NO_TRADE | Reason floor: WAIT | Reason floor: UNBLOCKED |
|---|---:|---:|---:|---:|---:|---:|---:|
| pullback | 44 | 30 | 14 | 0 | 32 | 10 | 2 |
| reversal | 96 | 84 | 52 | 0 | 81 | 14 | 1 |

## Per-run breakdown

| Date | Candidates | Reported chased | Reclassified | State mismatches |
|---|---:|---:|---:|---:|
| 2026-03-10 | 20 | 17 | 8 | 0 |
| 2026-03-11 | 20 | 12 | 4 | 0 |
| 2026-03-12 | 20 | 15 | 7 | 0 |
| 2026-03-13 | 20 | 17 | 13 | 0 |
| 2026-03-14 | 20 | 17 | 12 | 0 |
| 2026-03-15 | 20 | 16 | 8 | 0 |
| 2026-03-16 | 20 | 20 | 14 | 0 |

## Reclassified examples

| Date | Symbol | Setup | Decision | Distance % | Reported state | Hypothetical state | Reason-implied floor |
|---|---|---|---|---:|---|---|---|
| 2026-03-10 | MNTUSDT | reversal | NO_TRADE | 5.65 | chased | late | NO_TRADE |
| 2026-03-10 | PLUMEUSDT | pullback | NO_TRADE | 4.54 | chased | late | NO_TRADE |
| 2026-03-10 | AVAXUSDT | reversal | NO_TRADE | 7.54 | chased | late | NO_TRADE |
| 2026-03-10 | HSKUSDT | reversal | NO_TRADE | 7.48 | chased | late | NO_TRADE |
| 2026-03-10 | UNIUSDT | reversal | NO_TRADE | 3.01 | chased | late | NO_TRADE |
| 2026-03-10 | JSTUSDT | reversal | NO_TRADE | 6.94 | chased | late | NO_TRADE |
| 2026-03-10 | SUIUSDT | reversal | NO_TRADE | 4.4 | chased | late | NO_TRADE |
| 2026-03-10 | PIUSDT | pullback | NO_TRADE | 5.1 | chased | late | NO_TRADE |
| 2026-03-11 | BSVUSDT | reversal | NO_TRADE | 7.24 | chased | late | NO_TRADE |
| 2026-03-11 | HSKUSDT | reversal | NO_TRADE | 5.25 | chased | late | NO_TRADE |
| 2026-03-11 | VTHOUSDT | reversal | NO_TRADE | 5.42 | chased | late | NO_TRADE |
| 2026-03-11 | PIUSDT | pullback | NO_TRADE | 5.77 | chased | late | NO_TRADE |
| 2026-03-12 | ICPUSDT | reversal | NO_TRADE | 7.29 | chased | late | NO_TRADE |
| 2026-03-12 | SPKUSDT | reversal | NO_TRADE | 11.88 | chased | late | NO_TRADE |
| 2026-03-12 | GRASSUSDT | pullback | NO_TRADE | 5.41 | chased | late | NO_TRADE |
| 2026-03-12 | NEXOUSDT | reversal | NO_TRADE | 4.12 | chased | late | NO_TRADE |
| 2026-03-12 | HYPEUSDT | pullback | NO_TRADE | 7.4 | chased | late | NO_TRADE |
| 2026-03-12 | FORMUSDT | reversal | NO_TRADE | 11.46 | chased | late | NO_TRADE |
| 2026-03-12 | ETHFIUSDT | reversal | NO_TRADE | 9.31 | chased | late | NO_TRADE |
| 2026-03-13 | STABLEUSDT | pullback | WAIT | 4.48 | chased | late | WAIT |

