# PR9 — Backtest: Do not drop Breakout Trend 1–5D rows when 4H simulation returns None

## Short explanation
In `scanner/pipeline/backtest_runner.py`, when `_simulate_breakout_4h_trade(...)` returns `None`, the code path uses `continue`, causing the row to be omitted entirely. Since Breakout Trend 1–5D rows do not always include full trade-level payloads, this leads to missing rows in backtest outputs, understating counts/trigger stats and biasing experiments.

Fix: always record the row in backtest outputs even if trade simulation cannot produce a trade object; store an explicit “no_trade_reason” / status instead of dropping.

## Scope
- Backtest output should preserve the existence of each scored setup row.
- If no trade can be simulated, record it with status fields.
- Add tests ensuring rows are not dropped.

## Files to change
- `scanner/pipeline/backtest_runner.py`
- `tests/`

---

## Required code changes (exact)

### 1) Replace `continue` on None simulation with explicit record
Wherever the code does:
- `trade = _simulate_breakout_4h_trade(...)`
- `if trade is None: continue`

Replace with:
- If `trade is None`:
  - Append a result entry for that row with:
    - `trade_status = "NO_TRADE"`
    - `no_trade_reason = "<reason>"` (string; choose one of the fixed enums below)
  - The row must still contribute to “triggered candidates” counts.

Define fixed `no_trade_reason` values (enum-like strings):
- `MISSING_NEXT_4H_OPEN`
- `RETEST_NOT_FILLED`
- `INSUFFICIENT_4H_HISTORY`
- `MISSING_REQUIRED_FEATURES`
(Choose the best match; do not invent new values beyond this list.)

### 2) Keep existing trade objects unchanged when simulation succeeds
If `trade` is not None -> record as before.

### 3) Ensure summary metrics separate signals vs executed trades
If the backtest summary currently uses “rows” as “trades”, update it so:
- “signals” count = number of setup rows considered
- “trades” count = number of rows with `trade_status == "TRADE"` (or existing success condition)

---

## Tests (tests-first)

### A) None trade does not remove row
Create a test where `_simulate_breakout_4h_trade` returns None (e.g. missing next 4H candle open).
Assert:
- Output contains an entry for the row with `trade_status == "NO_TRADE"`.
- It is not dropped from arrays/tables.

### B) Summary counts do not undercount signals
Assert:
- signals >= trades
- signals equals number of setup rows fed into backtest.

---

## Acceptance criteria
- No setup rows disappear from backtest outputs due to simulation returning None.
- Outputs include explicit `trade_status` and `no_trade_reason` for NO_TRADE cases.
- Tests pass.
- `python -m pytest -q` passes.

## Close-out / Archive step (mandatory)
After merge:
1) Move this ticket file to `docs/legacy/v2/tickets/` (same filename).
2) Update `docs/v2/Zwischenstand und Ticket-Status (Canonical v2).md`.
