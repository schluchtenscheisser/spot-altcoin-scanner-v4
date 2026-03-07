## Title
[P0] PR-11 Risk-Tests V4.2.1

## Context / Source
- V4.2.1 ist die alleinige Referenz.
- EPIC 5 / PR-11 fordert die explizite Testabsicherung der neuen Risk-/Downside-Berechnung aus PR-09 und der setup-seitigen Invalidation-Anchors aus PR-10.
- Die Decision Layer soll später `risk_acceptable` als harten Input konsumieren; deshalb muss die Risk-Stufe bereits jetzt deterministisch und regressionssicher getestet sein.

## Goal
Ein belastbares Testnetz für die Phase-1-Risk-Berechnung bereitstellen, das mindestens absichert:
- korrekte ATR-basierte Stop-Berechnung
- korrekte Min-/Max-Stop-Distanzlogik
- korrekte RR-Berechnung
- korrekte Ableitung von `risk_acceptable`
- explizites Verhalten bei fehlender ATR / fehlenden Pflichtdaten
- korrektes Durchreichen optionaler setup-seitiger Invalidation-Anchors

## Scope
- neue oder angepasste Tests unter `tests/`
- wahrscheinlich relevant:
  - `tests/test_t81_indicator_ema_atr.py`
  - neue dedizierte Risk-Tests, z. B. `tests/test_v421_risk_calculation.py`
  - ggf. kleine Fixtures/Helfer für Risk-Inputs

## Out of Scope
- Keine neue Runtime-Logik in `scanner/pipeline/risk.py`
- Keine Änderung der Risk-Regeln selbst
- Keine Änderung der Decision Layer
- Keine BTC-Regime-Logik
- Keine Output-Renderer-Änderung
- Keine Änderung der Tradeability-Logik
- Keine Änderung der Setup-Scorer jenseits testseitiger Nutzung

## Canonical References (important)
- `docs/canonical/AUTHORITY.md`
- `docs/canonical/RISK_MODEL.md`
- `docs/canonical/PIPELINE.md`
- `docs/canonical/OUTPUT_SCHEMA.md`
- `docs/tickets/_TEMPLATE.md`
- `docs/tickets/_TICKET_PREFLIGHT_CHECKLIST.md`

## Proposed change (high-level)
Before:
- Die neue ATR-basierte Risk-Stufe und ihre Edge-Cases sind nicht vollständig regressionssicher abgesichert.
- Es fehlt ein explizites Testbündel für Min-/Max-Distanz, RR, `risk_acceptable` und insufficient-data-Pfade.

After:
- Es existieren deterministische Tests für:
  - verschiedene ATR-Werte und korrekte Stop-Berechnung
  - Min-Stop-Distanz 4%
  - Max-Stop-Distanz 12%
  - korrekte RR-Berechnung
  - `risk_acceptable = true` bei RR ≥ 1.3
  - `risk_acceptable = false` bei RR < 1.3
  - fehlende ATR / fehlende Pflichtdaten => expliziter insufficient-data-Pfad
  - setup-seitige Invalidation-Anchors werden korrekt mitgeführt, wenn vorhanden

Edge cases:
- sehr niedrige ATR => Stop würde unter Minimum liegen
- sehr hohe ATR => Stop würde über Maximum liegen
- TP10/TP20 fehlen
- Entry fehlt
- ATR fehlt
- Anchor vorhanden
- Anchor fehlt
- Risk-Felder berechenbar vs nicht berechenbar sauber getrennt

Backward compatibility impact:
- Keine fachliche Verhaltensänderung beabsichtigt; Ticket erhöht nur die Testabdeckung.
- Bestehende Tests dürfen angepasst werden, wenn sie alte implizite Risk-Annahmen fest verdrahten.

## Codex Implementation Guardrails (No-Guesswork, Pflicht bei Code-Tickets)
- **Canonical first:** Testwerte und Schwellen müssen exakt die Phase-1-Parameter aus V4.2.1/Canonical widerspiegeln.
- **ATR-Stop bleibt Primärlogik:** Tests dürfen nicht versehentlich setup-basierte Anchors als operative Stop-Primärlogik voraussetzen.
- **Missing vs invalid trennen:** Fehlende ATR/Entry/TP-Daten ≠ negatives Risk, sondern expliziter insufficient-data-Pfad.
- **Keine bool()-Koerzierung:** `risk_acceptable` explizit prüfen; null/fehlende Werte nicht indirekt über truthiness auswerten.
- **Determinismus:** Tests müssen ohne externe Datenquellen/API laufen.
- **Anchors nur als Kontext prüfen:** Wenn `invalidation_anchor_*` vorhanden ist, korrekt durchgereicht; keine operative Stop-Ableitung aus dem Anchor in diesem Ticket.
- **Keine Decision-Semantik hineinziehen:** Dieses Ticket testet Risk, nicht `ENTER/WAIT/NO_TRADE`.

## Implementation Notes (optional but useful)
- Wenn bestehende ATR-Tests nur Indikatorberechnung abdecken, lege eine neue dedizierte Risk-Testdatei an, statt semantisch unpassende Tests zu überladen.
- Teste RR idealerweise mit einfach nachvollziehbaren Zahlen, damit Erwartungswerte im Review leicht überprüfbar sind.
- Falls PR-09 einen expliziten Status / Reason für insufficient risk data eingeführt hat, teste diesen präzise und vollständig.

## Acceptance Criteria (deterministic)
1) Es gibt Tests für korrekte ATR-basierte Stop-Berechnung bei mehreren ATR-Ausprägungen.

2) Es gibt Tests für die Min-Stop-Distanzlogik von 4%.

3) Es gibt Tests für die Max-Stop-Distanzlogik von 12%.

4) Es gibt Tests für korrekte RR-Berechnung zu `tp10` und `tp20`.

5) Es gibt Tests, die explizit prüfen:
   - `risk_acceptable = true` bei RR ≥ 1.3
   - `risk_acceptable = false` bei RR < 1.3

6) Es gibt Tests für fehlende ATR-Daten, die den expliziten insufficient-data-Pfad absichern.

7) Es gibt Tests für fehlende Entry- oder TP-Daten, die den expliziten insufficient-data-Pfad absichern.

8) Es gibt Tests, die setup-seitige `invalidation_anchor_*`-Felder korrekt durchgereicht/erhalten sehen, wenn vorhanden.

9) Alle Tests laufen deterministisch und ohne externe API-/Netzwerkzugriffe.

## Default-/Edgecase-Abdeckung (Pflicht bei Code-Tickets)
- **Config Defaults (Missing key → Default):** ✅ (Test: zentrale Risk-Defaults greifen)
- **Config Invalid Value Handling:** ✅ (Test: ungültige Risk-/ATR-Parameter führen zu klarem Fehler, sofern Runtime-Validierung vorhanden)
- **Nullability / kein bool()-Coercion:** ✅ (fehlende Risk-Daten explizit prüfen, nicht indirekt)
- **Not-evaluated vs failed getrennt:** ✅ (insufficient risk data ≠ unattraktives Risk)
- **Strict/Preflight Atomizität (0 Partial Writes):** ✅ (N/A — kein Writer-/CLI-Ticket)
- **ID/Dateiname Namespace-Kollisionen (falls relevant):** ✅ (N/A)
- **Deterministische Sortierung / Tie-breaker:** ✅ (N/A; Berechnung selbst deterministisch)

## Tests (required if logic changes)
- Unit:
  - ATR-Stop normal
  - Min-Floor greift
  - Max-Cap greift
  - RR zu TP10 korrekt
  - RR zu TP20 korrekt
  - `risk_acceptable` true/false korrekt
  - fehlende ATR => insufficient-data
  - fehlende Entry-/TP-Daten => insufficient-data
  - Anchor-Felder vorhanden / nicht vorhanden werden korrekt mitgetragen

- Integration:
  - mehrere Kandidaten mit unterschiedlichen ATR-/TP-Konstellationen werden deterministisch verarbeitet
  - keine externen IOs
  - falls PR-09 Risk-Felder an Kandidaten anhängt: Felder nach der Stufe vorhanden

- Golden fixture / verification:
  - Nur anpassen, wenn bestehende Snapshot-/Golden-Tests implizit alte Risk-Annahmen fest fixieren
  - Keine Autodocs manuell editieren

## Constraints / Invariants (must not change)
- [ ] ATR-basierter Stop bleibt Phase-1-Primärlogik
- [ ] Min 4% / Max 12% bleiben als Testannahmen gemäß V4.2.1 abgesichert
- [ ] `risk_acceptable` hängt an RR-Regel, nicht an truthiness
- [ ] setup-seitige Anchors bleiben Kontext, nicht operative Stop-Primärquelle
- [ ] keine Decision-/BTC-/Output-Logik in dieses Ticket hineinziehen
- [ ] Tests bleiben deterministisch und offline

## Definition of Done (Codex must satisfy)
- [ ] Risk-Tests gemäß Acceptance Criteria ergänzt/angepasst
- [ ] insufficient-data vs unattractive-risk explizit abgesichert
- [ ] RR-/Stop-Logik regressionssicher getestet
- [ ] Keine Scope-Überschreitung in Decision/BTC/Output
- [ ] PR erstellt: genau 1 Ticket → 1 PR
- [ ] Ticket nach PR-Erstellung gemäß Workflow verschoben

## Metadata (optional)
```yaml
created_utc: "2026-03-07T00:00:00Z"
priority: P0
type: test
owner: codex
related_issues: []
```
