# Risk/Reward Diagnosis

- Generated: 2026-03-16T12:32:22Z
- Source: trade_candidates (40 candidates)
- Current config: min_stop=4.0%, max_stop=12.0%, min_rr_t2=1.3

## Headline

- risk_acceptable=true: **16** (40.0%)
- risk_acceptable=false: **24** (60.0%)
- risk_acceptable=null: 0

## Why risk_acceptable=false

| Failure Mode | Count | Meaning |
|---|---:|---|
| STOP_TOO_WIDE | 20 | risk_pct_to_stop > 12.0% — stop too far from entry |
| PASS | 16 | risk_acceptable=true |
| STOP_TOO_TIGHT | 4 | risk_pct_to_stop < 4.0% — stop too close to entry |

## Setup Type Breakdown

### Reversal (26 candidates)

- risk_acceptable: true=7, false=19, null=0

**Stop source:**

- invalidation: 26

**risk_pct_to_stop distribution:** min=8.21% | P25=14.1% | median=17.56% | P75=22.43% | max=43.85%

**rr_to_target_2 distribution:** min=2.0 | median=2.0 | max=2.0

**Failure modes:**

| Mode | Count |
|---|---:|
| STOP_TOO_WIDE | 19 |
| PASS | 7 |

**Counterfactual — max_stop_distance=25.0%:**
- Would pass: 22 (current: 7, delta: **+15**)

**Counterfactual — ATR-fallback stop instead of base_low:**
- Viable ATR stops: 0
- Would pass risk_acceptable: 0

### Pullback (14 candidates)

- risk_acceptable: true=9, false=5, null=0

**Stop source:**

- invalidation: 14

**risk_pct_to_stop distribution:** min=0.31% | P25=3.04% | median=7.67% | P75=9.13% | max=17.37%

**rr_to_target_2 distribution:** min=2.0 | median=2.0 | max=2.0

**Failure modes:**

| Mode | Count |
|---|---:|
| PASS | 9 |
| STOP_TOO_TIGHT | 4 |
| STOP_TOO_WIDE | 1 |

**Counterfactual — max_stop_distance=12.0%:**
- Would pass: 8 (current: 9, delta: **+-1**)

## Full Scored Universe (all setups, not just Top 20)

### Reversal (46 scored)

- risk_acceptable: true=13, false=33
- risk_pct_to_stop: median=17.56% | P75=22.43% | P90=29.47% | max=43.85%
- Stop sources: {'invalidation': 46}
- Failure modes: {'STOP_TOO_WIDE': 33, 'PASS': 13}

### Pullback (34 scored)

- risk_acceptable: true=20, false=14
- risk_pct_to_stop: median=5.58% | P75=7.89% | P90=11.09% | max=17.37%
- Stop sources: {'invalidation': 34}
- Failure modes: {'PASS': 20, 'STOP_TOO_TIGHT': 13, 'STOP_TOO_WIDE': 1}

### Breakout (18 scored)

- risk_acceptable: true=14, false=4
- risk_pct_to_stop: median=9.38% | P75=9.71% | P90=11.31% | max=11.33%
- Stop sources: {'invalidation': 18}
- Failure modes: {'PASS': 14, 'STOP_TOO_TIGHT': 4}

## Per-Run Timeline

| Date | Candidates | RA=true | RA=false | RA=null | Stop Wide | Stop Tight | RR Low |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2026-03-15 | 20 | 9 | 11 | 0 | 7 | 4 | 0 |
| 2026-03-16 | 20 | 7 | 13 | 0 | 13 | 0 | 0 |

## Worst Reversal Risk Profiles (widest stops)

| Date | Symbol | Stop Source | Stop % | RR2 | Entry | Stop | Invalidation | ATR | CF ATR Pass? |
|---|---|---|---:|---:|---:|---:|---:|---:|---|
| 2026-03-16 | BERAUSDT | invalidation | 43.85% | 2.0 | 0.595694 | 0.3345 | None | None | n/a (%) |
| 2026-03-15 | BERAUSDT | invalidation | 43.11% | 2.0 | 0.587957 | 0.3345 | None | None | n/a (%) |
| 2026-03-15 | LAUSDT | invalidation | 32.74% | 2.0 | 0.2284 | 0.15362 | None | None | n/a (%) |
| 2026-03-16 | UNIUSDT | invalidation | 26.19% | 2.0 | 3.858685 | 2.848 | None | None | n/a (%) |
| 2026-03-15 | BSVUSDT | invalidation | 24.17% | 2.0 | 15.007463 | 11.38 | None | None | n/a (%) |
| 2026-03-15 | MNTUSDT | invalidation | 23.87% | 2.0 | 0.687484 | 0.5234 | None | None | n/a (%) |
| 2026-03-16 | CFXUSDT | invalidation | 23.03% | 2.0 | 0.052372 | 0.04031 | None | None | n/a (%) |
| 2026-03-16 | LINKUSDT | invalidation | 20.61% | 2.0 | 9.018915 | 7.16 | None | None | n/a (%) |
| 2026-03-16 | ATHUSDT | invalidation | 20.48% | 2.0 | 0.006047 | 0.004808 | None | None | n/a (%) |
| 2026-03-16 | AVAXUSDT | invalidation | 19.81% | 2.0 | 9.415545 | 7.55 | None | None | n/a (%) |
| 2026-03-15 | SPKUSDT | invalidation | 19.16% | 2.0 | 0.021314 | 0.01723 | None | None | n/a (%) |
| 2026-03-16 | FETUSDT | invalidation | 18.72% | 2.0 | 0.164743 | 0.1339 | None | None | n/a (%) |
| 2026-03-16 | QNTUSDT | invalidation | 17.58% | 2.0 | 65.006378 | 53.58 | None | None | n/a (%) |
| 2026-03-16 | ADAUSDT | invalidation | 17.55% | 2.0 | 0.267799 | 0.2208 | None | None | n/a (%) |
| 2026-03-15 | RSRUSDT | invalidation | 17.09% | 2.0 | 0.001617 | 0.001341 | None | None | n/a (%) |
| 2026-03-16 | XVSUSDT | invalidation | 17.05% | 2.0 | 3.014494 | 2.5006 | None | None | n/a (%) |
| 2026-03-16 | 1INCHUSDT | invalidation | 16.55% | 2.0 | 0.095869 | 0.08 | None | None | n/a (%) |
| 2026-03-16 | QTUMUSDT | invalidation | 15.5% | 2.0 | 0.911257 | 0.77 | None | None | n/a (%) |
| 2026-03-16 | CAKEUSDT | invalidation | 15.14% | 2.0 | 1.377584 | 1.169 | None | None | n/a (%) |
