# Title
[P3] Persist pre-Top20 ranked candidate snapshot for inclusion audit observability

## Context / Source (optional)
The `pre_top20_inclusion_audit` analysis script (run 2026-03-16) identified that the published run JSON does not contain the full set of scored and ranked candidates before the Top20 cap is applied:

- `trade_candidates`: 20 rows (post-dedup, post-ranking-cap)
- `setups.reversals` / `setups.pullbacks`: truncated to ~10 per type
- `setups.breakouts`: all 5 (only because sample is small)

The pipeline scores ~191 unique symbols at runtime (186 reversal + 191 pullback + 5 breakout, minus duplicates after symbol-level dedup), but only the final 20 are persisted. This prevents audit scripts from answering:

- Are there DIRECT_OK candidates with competitive scores at rank 21–40?
- Is the 65% MARGINAL share in the Top20 a universe property or a selection artifact?
- What is the score gap between rank 20 and rank 21?

This is a pure observability change. No scoring, ranking, decision, or pipeline behavior is modified.

> If the current authoritative reference, Canonical, and existing code conflict, the authoritative specification takes precedence. If additional clarification is needed, amend this ticket or ask the user rather than interpret.

## Goal
After this change:

1. Each pipeline run persists a snapshot of **all** globally-ranked candidates (post symbol-level dedup, pre Top20 cap) to a deterministic file path.
2. The snapshot contains the fields required for inclusion audit: symbol, setup identification, scores, tradeability, risk, entry readiness, and decision metadata.
3. Existing pipeline behavior, output schema, and performance budget remain unchanged.
4. The `pre_top20_inclusion_audit` script can consume this snapshot to perform full rank-comparison analysis.

## Scope
Allowlist of files/modules that may need changes:

- `scanner/pipeline/ranking/` (or wherever the global ranking + Top20 cap happens)
- `scanner/report_writer.py` (or equivalent output module)
- `scripts/pre_top20_inclusion_audit.py` (optional: add snapshot consumption path)

## Out of Scope
- Any change to scoring, ranking, decision, or risk logic
- Any change to the published `trade_candidates` array or its schema
- Any change to the existing `setups.*` arrays in the run JSON
- Any change to config semantics or config validation
- Any Top20 selection criteria change (e.g. tradeability weighting)
- Any new pipeline stage or gate

## Canonical References (important)
- `docs/canonical/CONFIGURATION.md` (no changes expected, but verify snapshot path config if added)
- `docs/canonical/VERIFICATION_FOR_AI.md` (no changes expected — no scoring/threshold change)

## Proposed change (high-level)

- Before:
  - The global ranking stage computes a ranked list of all scored candidates (after symbol-level dedup), then caps to Top20 and writes only those 20 to `trade_candidates`.
  - The full ranked list is discarded after the Top20 cap.

- After:
  - Immediately before (or immediately after) the Top20 cap, the full ranked candidate list is serialized to `snapshots/runtime/<run_id>_pre_top20.json`.
  - The snapshot contains one row per candidate (post symbol-level dedup) with the fields listed in Acceptance Criteria.
  - The snapshot file is written atomically (write to temp, rename) to avoid partial writes.
  - The existing `trade_candidates` array and all other outputs remain identical.

- Edge cases:
  - If the ranked candidate list is empty (0 scored symbols): write a valid JSON file with an empty `candidates` array and populated `meta` block.
  - If the ranked candidate list has ≤ 20 entries: write the snapshot normally; all candidates will also appear in `trade_candidates`.
  - If `snapshots/runtime/` does not exist: create it (mkdir -p equivalent).
  - Filename collision (same `run_id`): overwrite deterministically. Since `run_id` includes a millisecond timestamp, collisions are only possible on re-runs of the exact same input, where overwrite is correct behavior.

- Backward compatibility impact:
  - None. A new file is added; no existing file or output changes.

## Codex Implementation Guardrails (No-Guesswork, Pflicht bei Code-Tickets)

- **Config/Defaults:** No config values are read or validated by this ticket. If a config key for the snapshot output path is introduced, it must be optional with a hardcoded default of `snapshots/runtime/`. Missing key = use default.
- **Nullability:** Snapshot rows must preserve the exact nullability of their source fields. If `risk_acceptable` is `null` in the ranking stage, it must remain `null` in the snapshot — no implicit `bool(...)` coercion.
- **Strict/Preflight:** Snapshot write must be atomic: write to a temp file, then rename. If write fails, no partial file remains.
- **Not-evaluated vs failed:** Not applicable — this ticket does not introduce evaluation logic.
- **Determinism:** At identical input and identical config, the snapshot content (field values, row order, row count) must be identical. Row order must match the global ranking order used for Top20 selection.

> Existing repo paths and helpers may be reused as long as they do not contradict Canonical; no second source of truth is introduced.

## Implementation Notes (optional but useful)

- **Pipeline position:** The snapshot is written at the global ranking stage, after symbol-level dedup and score computation, before (or at) the Top20 cap. No additional API calls, OHLCV fetches, or scoring computations are triggered.
- **Determinism:** Row order in the snapshot must be identical to the ranking order that determines the Top20 cutoff. If the ranking uses `global_score` descending with a tie-breaker, the snapshot must use the same sort.
- **Performance:** Serializing ~191 rows to JSON is negligible relative to the ~117s pipeline runtime. No budget impact.
- **Schema:** The snapshot is a new artifact with its own implicit schema. It does not modify the existing run JSON schema.

> At identical input and identical config, the snapshot content is identical.
> At score ties, the same tie-breaker as the existing global ranking is used.

## Acceptance Criteria (deterministic)

1) After each pipeline run, a file `snapshots/runtime/<run_id>_pre_top20.json` exists.

2) The file contains valid JSON with structure:
   ```json
   {
     "meta": {
       "run_id": "<run_id>",
       "timestamp_utc": "<ISO timestamp>",
       "canonical_schema_version": "<version>",
       "total_candidates": <int>,
       "top20_cutoff_index": <int>,
       "top20_cutoff_global_score": <float or null>
     },
     "candidates": [ ... ]
   }
   ```

3) `candidates` contains one row per globally-ranked candidate (post symbol-level dedup, pre Top20 cap), ordered by the same sort key used for Top20 selection.

4) Each candidate row contains at minimum:
   - `rank` (int, 1-based, matching position in global ranking)
   - `symbol` (str)
   - `best_setup_type` (str)
   - `setup_subtype` (str or null)
   - `setup_score` (float or null)
   - `global_score` (float or null)
   - `tradeability_class` (str or null)
   - `risk_acceptable` (bool or null)
   - `entry_ready` (bool or null)
   - `entry_state` (str or null)
   - `decision` (str — as it would be computed, or null if decision layer has not run yet at this stage)
   - `decision_reasons` (list of str, or null)
   - `risk_pct_to_stop` (float or null)
   - `distance_to_entry_pct` (float or null)

5) The first 20 rows in `candidates` (rank 1–20) correspond exactly to the symbols in `trade_candidates` in the published run JSON, in the same order.

6) `meta.total_candidates` equals `len(candidates)`.

7) `meta.top20_cutoff_global_score` equals `candidates[19].global_score` if `len(candidates) >= 20`, else `null`.

8) Nullable fields in candidate rows preserve source nullability: if a field is `null` in the ranking stage, it remains `null` in the snapshot. No implicit coercion to `false`, `0`, or empty string.

9) If `candidates` is empty (0 scored symbols), the file is still written with `"candidates": []` and `meta.total_candidates = 0`.

10) The snapshot file is written atomically (temp file + rename). If write fails, no partial file remains on disk.

11) Existing pipeline outputs (`trade_candidates`, `setups.*`, run manifest, MD report) remain byte-identical with and without this change.

> Non-finite numeric values (`NaN`, `inf`, `-inf`) are treated as non-evaluable inputs and must not appear as numeric-looking values in snapshot outputs. If a source field is non-finite, serialize as `null`.

## Default-/Edgecase-Abdeckung (Pflicht bei Code-Tickets)

- **Config Defaults (Missing key → Default):** ✅ (N/A — ticket reads no config. If an optional snapshot path config key is introduced: missing key → hardcoded default `snapshots/runtime/`)
- **Config Invalid Value Handling:** ✅ (N/A — ticket introduces no config validation)
- **Nullability / kein bool()-Coercion:** ✅ (AC: #8 ; Test: snapshot row with `risk_acceptable=null` preserves `null`)
- **Not-evaluated vs failed getrennt:** ✅ (N/A — ticket introduces no evaluation logic)
- **Strict/Preflight Atomizität (0 Partial Writes):** ✅ (AC: #10 ; Test: simulated write failure leaves no partial file)
- **ID/Dateiname Namespace-Kollisionen (falls relevant):** ✅ (AC: #1, edge case in Proposed Change; `run_id` includes ms timestamp; same `run_id` → deterministic overwrite)
- **Deterministische Sortierung/Tie-breaker:** ✅ (AC: #3, #5 ; Test: snapshot row order matches Top20 selection order; tie-breaker is the same as existing global ranking)

## Tests (required if logic changes)

- Unit:
  - Snapshot with >20 candidates: first 20 symbols match `trade_candidates` symbols in order (AC #5)
  - Snapshot with ≤20 candidates: all candidates present, `top20_cutoff_global_score` is `null` if <20 (AC #7)
  - Snapshot with 0 candidates: valid JSON, empty `candidates` array (AC #9)
  - Nullable field preservation: row with `risk_acceptable=null` in ranking → `null` in snapshot (AC #8)
  - Non-finite value: row with `global_score=NaN` in ranking → `null` in snapshot
  - Atomic write: simulated write failure (e.g. read-only dir) → no partial `.json` file on disk (AC #10)
  - Determinism: same input twice → byte-identical snapshot output
- Integration:
  - Full pipeline run produces snapshot file at expected path with expected row count
- Golden fixture / verification:
  - Not required — no scoring/threshold/curve change

> Every preflight obligation category is covered by at least one explicitly specified test case.

## Constraints / Invariants (must not change)

- [x] Closed-candle-only behavior must not change
- [x] No-lookahead behavior must not change
- [x] Existing deterministic ordering / tie-break behavior for Top20 selection must not change
- [x] Existing `trade_candidates` output must remain byte-identical
- [x] No additional API calls or OHLCV fetches introduced
- [x] Pipeline runtime budget: snapshot serialization adds negligible overhead (<1s for ~200 rows)
- [x] This remains exactly **1 ticket → 1 PR**

---

## Definition of Done (Codex must satisfy)
(Reference: `docs/canonical/WORKFLOW_CODEX.md`)

- [ ] Implemented code changes per Acceptance Criteria
- [ ] Updated canonical docs under `docs/canonical/` (if snapshot path or schema documented)
- [ ] Updated `docs/canonical/VERIFICATION_FOR_AI.md` — not required (no scoring/threshold/curve change)
- [ ] PR created: exactly **1 ticket → 1 PR**
- [ ] Ticket moved to `docs/legacy/tickets/` after PR is created

---

## Metadata (optional)
```yaml
created_utc: "2026-03-16T00:00:00Z"
priority: P3
type: feature
owner: codex
related_issues: []
```
