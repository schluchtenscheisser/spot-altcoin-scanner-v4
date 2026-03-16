# Risk/Reward Diagnosis (v2 — Sensitivity Ladder)

- Generated: 2026-03-16T14:00:30Z
- Candidates: 40
- Config: min_stop=4.0%, max_stop=12.0%, min_rr_t2=1.3

## Headline

- risk_acceptable=true: **16** (40.0%)
- risk_acceptable=false: **24** (60.0%)

## Failure Modes

| Mode | Count |
|---|---:|
| STOP_TOO_WIDE | 20 |
| PASS | 16 |
| STOP_TOO_TIGHT | 4 |

## Reversal (26)

- Pass/Fail/Null: 7/19/0
- Stop sources: {'invalidation': 26}
- Stop distance: min=8.21% | P25=14.1% | median=17.56% | P75=22.43% | P90=29.47% | max=43.85%
- Failure modes: {'STOP_TOO_WIDE': 19, 'PASS': 7}

### ATR-Fallback Counterfactual

- Viable: 0, Would pass: 0

## Pullback (14)

- Pass/Fail/Null: 9/5/0
- Stop sources: {'invalidation': 14}
- Stop distance: min=0.31% | P25=3.04% | median=7.67% | P75=9.13% | P90=12.54% | max=17.37%
- Failure modes: {'PASS': 9, 'STOP_TOO_TIGHT': 4, 'STOP_TOO_WIDE': 1}

## Reversal Sensitivity Ladder

| Threshold | Would Pass | +vs Current | +vs Prev Step | New Symbols |
|---:|---:|---:|---:|---|
| **12.0% (current)** | **7** | — | — | — |
| 15.0% | 7 | +0 | +0 |  |
| 18.0% | 14 | +7 | +7 | 1INCHUSDT, ADAUSDT, CAKEUSDT, QNTUSDT, QTUMUSDT, RSRUSDT, XVSUSDT |
| 20.0% | 17 | +10 | +3 | 1INCHUSDT, ADAUSDT, AVAXUSDT, CAKEUSDT, FETUSDT, QNTUSDT, QTUMUSDT, RSRUSDT, SPKUSDT, XVSUSDT |
| 22.0% | 19 | +12 | +2 | 1INCHUSDT, ADAUSDT, ATHUSDT, AVAXUSDT, CAKEUSDT, FETUSDT, LINKUSDT, QNTUSDT, QTUMUSDT, RSRUSDT (+2) |
| 25.0% | 22 | +15 | +3 | 1INCHUSDT, ADAUSDT, ATHUSDT, AVAXUSDT, BSVUSDT, CAKEUSDT, CFXUSDT, FETUSDT, LINKUSDT, MNTUSDT (+5) |
| 30.0% | 23 | +16 | +1 | 1INCHUSDT, ADAUSDT, ATHUSDT, AVAXUSDT, BSVUSDT, CAKEUSDT, CFXUSDT, FETUSDT, LINKUSDT, MNTUSDT (+6) |

## Per-Run Timeline

| Date | Candidates | RA=true | RA=false | Stop Wide | Stop Tight |
|---|---:|---:|---:|---:|---:|
| 2026-03-15 | 20 | 9 | 11 | 7 | 4 |
| 2026-03-16 | 20 | 7 | 13 | 13 | 0 |

## Full Scored Universe

**Reversal** (46): pass=13, fail=33 | median=17.56%, P90=29.47%, max=43.85%

**Pullback** (34): pass=20, fail=14 | median=5.58%, P90=11.09%, max=17.37%

**Breakout** (18): pass=14, fail=4 | median=9.38%, P90=11.31%, max=11.33%

## Worst Reversal Stop Profiles

| Date | Symbol | Stop % | Entry | Stop | Invalidation | ATR | ATR CF |
|---|---|---:|---:|---:|---:|---:|---|
| 2026-03-16 | BERAUSDT | 43.85% | 0.595694 | 0.3345 | None | None | n/a |
| 2026-03-15 | BERAUSDT | 43.11% | 0.587957 | 0.3345 | None | None | n/a |
| 2026-03-15 | LAUSDT | 32.74% | 0.2284 | 0.15362 | None | None | n/a |
| 2026-03-16 | UNIUSDT | 26.19% | 3.858685 | 2.848 | None | None | n/a |
| 2026-03-15 | BSVUSDT | 24.17% | 15.007463 | 11.38 | None | None | n/a |
| 2026-03-15 | MNTUSDT | 23.87% | 0.687484 | 0.5234 | None | None | n/a |
| 2026-03-16 | CFXUSDT | 23.03% | 0.052372 | 0.04031 | None | None | n/a |
| 2026-03-16 | LINKUSDT | 20.61% | 9.018915 | 7.16 | None | None | n/a |
| 2026-03-16 | ATHUSDT | 20.48% | 0.006047 | 0.004808 | None | None | n/a |
| 2026-03-16 | AVAXUSDT | 19.81% | 9.415545 | 7.55 | None | None | n/a |
| 2026-03-15 | SPKUSDT | 19.16% | 0.021314 | 0.01723 | None | None | n/a |
| 2026-03-16 | FETUSDT | 18.72% | 0.164743 | 0.1339 | None | None | n/a |
| 2026-03-16 | QNTUSDT | 17.58% | 65.006378 | 53.58 | None | None | n/a |
| 2026-03-16 | ADAUSDT | 17.55% | 0.267799 | 0.2208 | None | None | n/a |
| 2026-03-15 | RSRUSDT | 17.09% | 0.001617 | 0.001341 | None | None | n/a |
| 2026-03-16 | XVSUSDT | 17.05% | 3.014494 | 2.5006 | None | None | n/a |
| 2026-03-16 | 1INCHUSDT | 16.55% | 0.095869 | 0.08 | None | None | n/a |
| 2026-03-16 | QTUMUSDT | 15.5% | 0.911257 | 0.77 | None | None | n/a |
| 2026-03-16 | CAKEUSDT | 15.14% | 1.377584 | 1.169 | None | None | n/a |
