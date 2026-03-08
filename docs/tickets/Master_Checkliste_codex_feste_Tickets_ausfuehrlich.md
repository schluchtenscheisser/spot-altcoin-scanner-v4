# Master-Checkliste für codex-feste Tickets (ausführliche Version)

**Zweck:**  
Diese Checkliste ist die **eine verbindliche Master-Checkliste** für die Erstellung und Prüfung von Tickets, die von Codex umgesetzt werden sollen.  
Sie ersetzt die Trennung zwischen allgemeiner Preflight-Checkliste und separater Zusatz-Checkliste für numerische/config-lastige Tickets.

**Ziel:**  
Tickets so präzise formulieren, dass Codex **keine semantischen Annahmen treffen** muss und spätere Review-Kommentare auf ein Minimum reduziert werden.

**Anwendungsbereich:**  
Für **jedes** Ticket verpflichtend.  
Besonders strikt anwenden bei Tickets mit:
- Config-Logik
- numerischen Berechnungen
- Nullable-/Tri-State-Feldern
- Pipeline-Gates / Stop-Pfaden
- Budget-/Ranking-/Sorting-Logik
- Risk-/Tradeability-/Decision-Semantik

---

## 1. Kanonische Autorität / Scope

### Prüffragen
- [ ] Sind die **autoritativen Canonical-Dokumente** im Ticket explizit genannt?
- [ ] Ist explizit festgelegt, dass bei Konflikten **Canonical vor Legacy, Autodocs und bestehendem Code** gilt?
- [ ] Ist der Scope so geschnitten, dass **1 Ticket = 1 PR** realistisch bleibt?
- [ ] Sind **Nicht-Ziele / Out of Scope** konkret genug, um Scope-Drift zu verhindern?
- [ ] Ist ausgeschlossen, dass das Ticket implizit spätere Epics oder Nachbar-PRs vorwegnimmt?

### Pflichtsatz im Ticket
> Wenn Canonical und bestehender Code widersprechen, gewinnt Canonical. Bei zusätzlichem Klärungsbedarf Ticket ergänzen statt interpretieren.

---

## 2. Begriffs- und Statusschärfe

Für jeden neuen oder geänderten Status, Enum-Wert oder Reason Key:

### Prüffragen
- [ ] Ist die erlaubte Wertemenge **vollständig und explizit** ausgeschrieben?
- [ ] Ist jeder Wert **positiv definiert**, nicht nur indirekt über Ausschluss?
- [ ] Ist klar, welche Werte **weiterlaufen**, welche **stoppen** und welche nur **Kontext** sind?
- [ ] Ist explizit beschrieben, was der jeweilige Wert **nicht** bedeutet?
- [ ] Sind Reason Keys maschinenlesbar, stabil und eindeutig?

### Pflichtfragen für typische Status
- [ ] Ist `UNKNOWN` klar von `FAIL` getrennt?
- [ ] Ist `NOT_EVALUATED` klar von `NEGATIVE_EVALUATION` getrennt?
- [ ] Ist `WAIT` klar von „nicht entscheidbar“ getrennt?
- [ ] Ist `MARGINAL` klar von `UNKNOWN` und `FAIL` getrennt?
- [ ] Ist `null` semantisch beschrieben?

### Pflichtsatz im Ticket
Für jeden kritischen Status mindestens ein Satz der Form:
- `UNKNOWN` bedeutet ...
- `FAIL` bedeutet ...
- `MARGINAL` bedeutet ...
- `WAIT` bedeutet ...
- `null` bedeutet ...

---

## 3. Config-Semantik: Missing vs Default vs Invalid

Das ist eine der häufigsten Fehlerquellen.

Für **jeden** neuen oder genutzten Config-Block muss explizit beantwortet sein:

### Prüffragen
- [ ] Welche Keys sind **optional**?
- [ ] Welche Keys sind **required**?
- [ ] Was passiert bei **fehlendem Key**?
- [ ] Was passiert bei **ungültigem Wert**?
- [ ] Was passiert bei **partiellem Nested-Override**?
- [ ] Gibt es verbotene stille Fallbacks?

### Pflichtentscheidungen pro Config-Block
- [ ] Missing key → **Default** oder **Fehler**?
- [ ] Partielles Dict-Override → **Merge mit Defaults** oder **vollständiger Replace**?
- [ ] Ungültiger Typ/Wert → klarer Fehler oder normalisierte Korrektur?
- [ ] Werden zentrale Defaults benutzt oder ad-hoc Raw-Dict-Fallbacks?

### Pflichtsatz im Ticket
Für jeden verschachtelten Config-Block muss mindestens einer dieser Sätze explizit enthalten sein:

**Variante A — Merge**
> Partielle Overrides in `<config_block>` werden feldweise mit zentralen Defaults gemergt; fehlende Unterkeys gelten nicht als invalid.

**Variante B — Replace**
> Overrides in `<config_block>` ersetzen den Block vollständig; fehlende Unterkeys sind nach dem Override invalid.

**Wichtig:**  
Ohne diese Festlegung ist das Ticket **nicht freigabefähig**.

---

## 4. Numerische Robustheit: `NaN`, `inf`, `-inf`, leere numerische Inputs

Diese Sektion ist Pflicht für Tickets mit:
- ATR / EMA / OHLCV / Risiko
- Slippage / Spread / Depth
- Prozenten / Scores / Thresholds
- pandas / numpy / float-Konvertierung
- sonstiger numerischer Transformationslogik

### Prüffragen
- [ ] Was passiert bei `None`?
- [ ] Was passiert bei `NaN`?
- [ ] Was passiert bei `inf` / `-inf`?
- [ ] Was passiert bei leerer Payload / leerer Serie / leerem Orderbook?
- [ ] Was passiert bei Division durch 0 oder quasi-0?
- [ ] Welche Eingaben gelten als „fehlend“?
- [ ] Welche Eingaben gelten als „ungültig“?
- [ ] Welche Eingaben gelten als „fachlich negativ“?

### Pflichtsatz im Ticket
> Nicht-finite numerische Werte (`NaN`, `inf`, `-inf`) gelten als ungültige bzw. nicht auswertbare Inputs und dürfen nicht in numerisch aussehende Outputs durchgereicht werden.

Wenn das **nicht** gelten soll, muss die Alternativregel explizit und testbar beschrieben sein.

---

## 5. Nullability / Tri-State / Bool-Fallen

Für jedes bool-artige Feld oder Entscheidungsergebnis:

### Prüffragen
- [ ] Ist klar, ob das Feld wirklich **binär bool** ist?
- [ ] Oder ist es fachlich **tri-state** (`true` / `false` / `null`)?
- [ ] Ist `null` semantisch beschrieben?
- [ ] Ist ausgeschlossen, dass `bool(x)` auf semantisch nullable Felder angewendet wird?
- [ ] Bedeutet `false` wirklich „negativ bewertet“?
- [ ] Bedeutet `null` „nicht evaluierbar“?
- [ ] Darf ein nicht berechenbarer Wert zu `false` kollabieren?
- [ ] Müssen abhängige Felder ebenfalls `null` bleiben, wenn Input fehlt?

### Pflichtsatz im Ticket
Für jedes potentiell tri-state Feld:
> `<feld>` ist nullable. `null` bedeutet „nicht belastbar evaluierbar“ und darf nicht implizit zu `false` koerziert werden.

### Typische Beispiele
- `risk_acceptable`
- `rr_to_tp10`
- `tradeable_via_tranches`
- `slippage_bps_20k`

---

## 6. Not-evaluated vs negative evaluation

Diese Trennung muss bei allen Gating-, Risk-, Tradeability- und Decision-Tickets explizit sein.

### Prüffragen
- [ ] Wann ist ein Kandidat **nicht evaluiert**?
- [ ] Wann ist ein Kandidat **evaluiert und negativ**?
- [ ] Wann ist ein Kandidat **evaluiert, aber grenzwertig**?
- [ ] Welcher Status / welches Feld repräsentiert diese Fälle?

### Pflichtsatz im Ticket
> Nicht evaluierbar / nicht bewertet und fachlich negativ bewertet sind getrennte Zustände und müssen im Code getrennt erhalten bleiben.

---

## 7. Determinismus / Reihenfolge / Tie-Breaker

Für jede Selektion, Sortierung, Budget-Grenze, Top-K-Logik oder Score-Reihenfolge:

### Prüffragen
- [ ] Ist die Sortierlogik vollständig spezifiziert?
- [ ] Ist ein Tie-Breaker explizit benannt?
- [ ] Ist beschrieben, welche Eingaben zur Reihenfolge beitragen und welche nicht?
- [ ] Ist ausgeschlossen, dass Dict-/Set-Iteration implizit die Reihenfolge bestimmt?
- [ ] Ist bei identischem Input + identischer Config die Ausgabe identisch?

### Pflichtsatz im Ticket
> Bei identischem Input und identischer Config sind Auswahl, Reihenfolge, Status und Gründe identisch.

Wenn Sortierung relevant ist:
> Bei Score-Gleichstand greift der explizite Tie-Breaker `<x>`.

---

## 8. Pipeline-Grenzen / Stopp-Pfade

Für jedes Ticket, das eine Pipeline-Stufe verändert:

### Prüffragen
- [ ] Ist die genaue Position in der Pipeline benannt?
- [ ] Ist klar, was **weiterläuft** und was **stoppt**?
- [ ] Ist klar, welche teuren Folgeschritte **nicht** mehr ausgelöst werden dürfen?
- [ ] Sind interne Stop-Reasons klar benannt?
- [ ] Erreichen gestoppte Kandidaten noch OHLCV / Features / Scoring / Risk / Decision?
- [ ] Werden API-/Runtime-Kosten durch den Stop-Pfad wirklich vermieden?
- [ ] Sind gestoppte Kandidaten still verworfen oder explizit begründet?

### Pflichtsatz im Ticket
> `<status/klasse>` stoppt vor `<nachfolgende_stufe>` und darf keine weiteren Kosten in `<nachfolgende_stufe>` auslösen.

---

## 9. Test-Schärfe: Kategorien reichen nicht, konkrete Fälle sind Pflicht

Jede relevante Preflight-Kategorie muss im Ticket mindestens einen **konkreten Testfall** haben.

### Nicht ausreichend
- „Config Defaults testen“
- „Nullability testen“
- „Determinismus testen“

### Erforderlich
- [ ] konkreter Missing-Key-Test
- [ ] konkreter Invalid-Value-Test
- [ ] konkreter `NaN`-/`inf`-Test, falls numerisch relevant
- [ ] konkreter `null`-bleibt-`null`-Test
- [ ] konkreter not-evaluated-vs-failed-Test
- [ ] konkreter deterministischer Reproduktions-Test
- [ ] konkreter Stop-/Weiterlauf-Test bei Pipeline-Tickets

### Pflichtsatz im Ticket
> Jede Preflight-Pflichtkategorie ist durch mindestens einen explizit ausgeschriebenen Testfall abgesichert.

---

## 10. Repo-Realität / vorhandene Implementierung

### Prüffragen
- [ ] Ist das Ticket gegen die echte Repo-Struktur geschrieben?
- [ ] Sind vorhandene Module/Tests benannt, die wiederverwendet oder angepasst werden sollen?
- [ ] Ist klar, wo bestehende Logik weiterverwendet werden darf und wo nicht?
- [ ] Wird vermieden, neue Parallel-Logik einzuführen, wenn bestehende Helfer genügen?

### Pflichtsatz im Ticket
> Vorhandene Repo-Pfade/Helfer dürfen wiederverwendet werden, solange sie Canonical nicht widersprechen; keine zweite Wahrheit einführen.

---

## 11. Verbotsliste für stille Interpretationen

Ein Ticket ist **nicht ausreichend präzise**, wenn eine der folgenden Fragen offen bleibt:

- [ ] Merge oder Replace bei verschachtelter Config?
- [ ] `NaN` / `inf`-Verhalten?
- [ ] `null` vs `false`?
- [ ] not-evaluated vs failed?
- [ ] expliziter Tie-Breaker?
- [ ] gestoppt vs weitergereicht?
- [ ] Default bei Missing Key?
- [ ] klarer Fehler bei Invalid Value?
- [ ] fehlend vs stale vs ungültig?
- [ ] erlaubte Enum-Werte vollständig?

Wenn eine dieser Fragen offen ist, muss das Ticket ergänzt werden.

---

## 12. Pflichtsektion für numerische / Config-lastige Tickets

Diese Sektion muss **wörtlich oder inhaltlich gleichwertig** in jedes Ticket aufgenommen werden, das Konfigurations- oder numerische Logik enthält:

### Pflichtblock
- [ ] Partielle Nested-Overrides: **merge oder replace explizit festlegen**
- [ ] Nicht-finite Werte (`NaN`, `inf`, `-inf`) explizit behandeln
- [ ] Nullable Ergebnisse explizit als nullable markieren
- [ ] Nicht auswertbar ≠ negativ bewertet
- [ ] Fehlender Key ≠ ungültiger Key
- [ ] Konkrete Tests für genau diese Fälle ausschreiben

---

## 13. Freigabe-Gate vor Ticket-Abgabe

Ein Ticket darf erst als **codex-fest** gelten, wenn alle folgenden Fragen mit **Ja** beantwortet sind:

- [ ] Könnte Codex das Ticket umsetzen, ohne bei Missing-vs-Invalid raten zu müssen?
- [ ] Könnte Codex das Ticket umsetzen, ohne bei `null` vs `false` raten zu müssen?
- [ ] Könnte Codex das Ticket umsetzen, ohne bei `NaN`/`inf` raten zu müssen?
- [ ] Könnte Codex das Ticket umsetzen, ohne Merge-vs-Replace bei Config erraten zu müssen?
- [ ] Könnte Codex das Ticket umsetzen, ohne not-evaluated-vs-failed zu verwischen?
- [ ] Könnte Codex die Tests schreiben, ohne zusätzliche Semantik zu erfinden?
- [ ] Könnte Codex die PR umsetzen, ohne benachbarte Epics mitzuziehen?

Wenn eine Antwort **Nein** ist, ist das Ticket noch nicht scharf genug.

---

## 14. Wiederverwendbare Standardsätze für Tickets

Diese Sätze können fast wörtlich wiederverwendet werden:

### Config
> Partielle Overrides in `<block>` werden feldweise mit zentralen Defaults gemergt; fehlende Unterkeys gelten nicht als invalid. Ungültige Werte erzeugen einen klaren Fehler.

### Numerik
> Nicht-finite numerische Werte (`NaN`, `inf`, `-inf`) gelten als nicht auswertbar und dürfen nicht in numerisch aussehenden Outputs verbleiben.

### Nullability
> `<feld>` ist nullable. `null` bedeutet „nicht belastbar evaluierbar“ und darf nicht implizit zu `false` koerziert werden.

### Status-Trennung
> Nicht evaluierbar / nicht bewertet und fachlich negativ bewertet sind getrennte Zustände und bleiben im Code getrennt erhalten.

### Determinismus
> Bei identischem Input und identischer Config sind Auswahl, Reihenfolge, Status und Gründe identisch.

### Pipeline-Stop
> `<status/klasse>` stoppt vor `<stufe>` und darf keine weiteren Kosten in `<stufe>` auslösen.

---

## 15. Schnellprüfung vor Freigabe

Diese Kurzprüfung muss vor Ticket-Abgabe einmal bewusst beantwortet werden:

### Config
- [ ] Missing key → Default oder Fehler?
- [ ] Invalid value → klarer Fehler?
- [ ] Nested override → merge oder replace?

### Numerik
- [ ] `None` behandelt?
- [ ] `NaN` behandelt?
- [ ] `inf` / `-inf` behandelt?
- [ ] Division durch 0 / quasi-0 behandelt?

### Nullable Felder
- [ ] Ist das Feld wirklich bool oder tri-state?
- [ ] Ist `null` semantisch beschrieben?
- [ ] Bleibt `null` erhalten oder kollabiert fälschlich zu `false`?

### Statuslogik
- [ ] not evaluated ≠ failed?
- [ ] unknown ≠ fail?
- [ ] missing data ≠ negative evaluation?

### Tests
- [ ] ein Missing-Key-Test
- [ ] ein Invalid-Value-Test
- [ ] ein `NaN`-/`inf`-Test
- [ ] ein `null`-bleibt-`null`-Test
- [ ] ein deterministischer Reproduktions-Test

---

## 16. Empfehlung zur Anwendung

**Verbindlicher Standard:**  
Diese Master-Checkliste für jedes Ticket verwenden.

**Besonders strikt anwenden bei:**
- Config-Tickets
- Risk-Tickets
- Tradeability-Tickets
- numerischen Berechnungen
- Pipeline-Gates
- Budget-/Ranking-/Top-K-Logik

**Praktischer Workflow:**
1. Ticket entwerfen  
2. gegen diese Checkliste prüfen  
3. Pflichtsätze ergänzen  
4. konkrete Testfälle ergänzen  
5. erst dann Ticket ausgeben

So werden genau die Lücken reduziert, die später oft zu Codex-Review-Kommentaren führen.
