# Codex Workflow — Tickets → 1 PR, Canonical Docs First (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_WORKFLOW_CODEX
status: canonical
audience:
  - gpt_codex
  - humans
ticket_inbox: docs/tickets
ticket_in_progress: docs/tickets/_in_progress
ticket_archive: docs/legacy/tickets
canonical_root: docs/canonical
autodocs_read_only:
  - docs/code_map.md
  - docs/GPT_SNAPSHOT.md
one_ticket_one_pr: true
archive_ticket_in_same_pr: true
last_updated_utc: "2026-02-25T23:05:52Z"
```

## 0) Ziel
Diese Arbeitsanweisung beschreibt den verbindlichen Bearbeitungsprozess für GPT-Codex:

- Codex holt genau **ein** Ticket aus `docs/tickets/`
- Codex bearbeitet es vollständig
- Codex erstellt **genau einen PR pro Ticket**
- Codex aktualisiert Canonical Docs nach dem Authority-Prozess
- Codex **archiviert das Ticket im selben PR** (kein zweiter PR nötig)

---

## 1) Authority & Dokument-Hierarchie (verbindlich)
Autoritative Dokumente:
1) `docs/canonical/AUTHORITY.md`
2) `docs/canonical/INDEX.md`
3) `docs/code_map.md` (read-only)
4) `docs/GPT_SNAPSHOT.md` (read-only)

Precedence:
- `docs/canonical/*` > `docs/*` > auto-docs > `docs/legacy/*`

---

## 2) Ticket Lifecycle (Inbox → In-Progress → Archive)

### 2.1 Inbox
- Neue Tickets liegen unter: `docs/tickets/` (Markdown).
- Codex wählt deterministisch das nächste Ticket:
  - sortiere Ticket-Dateinamen lexikographisch (ASCII) aufsteigend
  - nimm die erste Datei, **ausgenommen**:
    - `_TEMPLATE.md`
    - alles unter `docs/tickets/_in_progress/`

### 2.2 In-Progress (Lock, verhindert Doppelbearbeitung)
Sobald Codex ein Ticket auswählt, muss er es **sofort** verschieben nach:
- `docs/tickets/_in_progress/<original_filename>.md`

Zweck:
- Ticket ist aus der Inbox entfernt (andere Runs/Codex-Aufträge picken es nicht versehentlich erneut).

### 2.3 Archive (im selben PR)
Am Ende der Ticketbearbeitung (bevor der PR eröffnet wird) verschiebt Codex das Ticket von `_in_progress` nach:
- `docs/legacy/tickets/<original_filename>.md`

Und fügt oben einen kurzen Header ein (falls noch nicht vorhanden):
```md
> ARCHIVED (ticket): Implemented in PR for this ticket. Canonical truth is under `docs/canonical/`.
```

Canonical rule:
- Das Ticket wird **im selben Branch/PR** archiviert, zusammen mit Code- und Dokuänderungen.

---

## 3) 1 Ticket → 1 PR (verbindlich)
- Pro Ticket genau ein PR.
- Keine Kombination mehrerer Tickets in einem PR.

Branch Naming:
- `ticket/<ticket_slug>`

PR Title:
- `Ticket: <ticket filename> — <short summary>`

PR Body (required):
- Original ticket path (now archived): `docs/legacy/tickets/<filename>.md`
- `Docs impact summary` (siehe Abschnitt 5.4)
- `Verification updated: yes/no` + welche Stellen

---

## 4) Execution Order (Authority Process in PRs)
Wenn das Ticket Logik/Parameter/Schwellenwerte/Scores/Ranking/Outputs/Datenhandling ändert:

1) Canonical Docs zuerst aktualisieren
2) Code ändern
3) Verification/Fixtures aktualisieren (wenn relevant)
4) Sanity checks (Links/Drift)
5) Ticket nach `docs/legacy/tickets/` verschieben (im selben PR)
6) PR erstellen

Wenn Codex glaubt, dass keine Canonical Doku betroffen ist:
- im PR Body begründen: `Docs not required because: ...`

---

## 5) Canonical Docs Update Rules (Kurz)
### 5.1 Determinism Pflicht
- closed-candle-only
- no lookahead
- klare Tie-/NaN-Regeln
- keine „implementation-defined“ Defaults in Canonical

### 5.2 Routing
- Setup/Score: `docs/canonical/SCORING/*.md`
- Ranking: `docs/canonical/SCORING/GLOBAL_RANKING_TOP20.md`
- Liquidity/Slippage/Re-rank: `docs/canonical/LIQUIDITY/*.md`
- Features: `docs/canonical/FEATURES/*.md`
- Outputs: `docs/canonical/OUTPUT_SCHEMA.md` + `docs/canonical/OUTPUTS/*`
- Providers/As-Of: `docs/canonical/DATA_SOURCES.md`
- Mapping: `docs/canonical/MAPPING.md`
- Backtest: `docs/canonical/BACKTEST/*.md`

### 5.3 Verification Pflicht
Wenn Scoring/Threshold/Curve geändert:
- `docs/canonical/VERIFICATION_FOR_AI.md` aktualisieren (expected values/boundaries)

### 5.4 PR “Docs impact summary” (required)
Im PR Body muss stehen:
- `Canonical docs updated:` ...
- `What changed:` ...
- `Verification updated:` yes/no

---

## 6) Ticket Completion Checklist (must satisfy before PR)
- [ ] Ticket wurde nach `_in_progress/` verschoben (Lock)
- [ ] Code implementiert Acceptance Criteria
- [ ] Canonical Docs aktualisiert (wenn fachliche Änderung)
- [ ] `VERIFICATION_FOR_AI.md` aktualisiert (wenn relevant)
- [ ] Ticket nach `docs/legacy/tickets/` verschoben (im selben PR)
- [ ] PR erstellt (1 Ticket → 1 PR)

---

## 7) Operator Command Contract
Du sagst nur:
> „Hole dir das nächste Ticket aus `docs/tickets/` und bearbeite es. Halte dabei die Anweisungen aus `docs/canonical/WORKFLOW_CODEX.md` ein.“

Codex muss dann:
1) Ticket → `_in_progress`
2) bearbeiten (Docs first)
3) Ticket → `docs/legacy/tickets/`
4) PR erstellen
