# Mapping Layer — Exchange Symbols ↔ Market-Cap Assets (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_MAPPING_LAYER
status: canonical
purpose:
  - link_exchange_symbols_to_market_cap_assets
  - prevent_silent_mismatches_in_filters_and_scoring
determinism:
  required: true
  no_fuzzy_matching: true
inputs:
  - exchange_symbols: "MEXC spot symbols (base/quote)"
  - market_cap_assets: "CMC assets (id, symbol, slug, name, market_cap_usd)"
manual_controls:
  - denylist: "config/denylist.yaml"
  - mapping_overrides: "config/mapping_overrides.json"
outputs:
  - mapping_table: "reports/mapping_table.csv (or json)"
  - collisions_report: "reports/mapping_collisions.csv"
  - unmapped_report: "reports/mapping_unmapped.csv"
```

## 0) Ziel
Die Mapping-Layer verbindet **Exchange-Symbole** (MEXC) mit **Market-Cap-Assets** (CMC oder äquivalente Quelle).  
Sie ist kritisch, weil:

- Market-Cap Filter *und* Discovery-Tag hängen an CMC-Assets
- Scoring/Backtests hängen an OHLCV des Exchange-Symbols
- Ein falsches Mapping erzeugt deterministische, aber **fachlich falsche** Signale

Canonical Ziel: **Keine stillen Annahmen.** Alle Unsicherheiten müssen explizit als Collision/Unmapped/Override sichtbar sein.

---

## 1) Begriffe & Entitäten

### 1.1 Exchange Symbol (MEXC)
Beispiel:
- `symbol`: `HUSDT`
- `base_asset`: `H`
- `quote_asset`: `USDT`

Canonical Fokus:
- Spot
- Quote-Asset: `USDT` (siehe `SCOPE.md`)

### 1.2 Market-Cap Asset (CMC)
Minimalfelder:
- `cmc_id`
- `symbol`
- `slug`
- `name`
- `market_cap_usd`
- optional: `date_added`

---

## 2) Mapping Output Schema (pro Exchange Symbol)

Für jedes Exchange Symbol `S` wird ein Mapping-Record erzeugt:

- `exchange_symbol`
- `base_asset`
- `quote_asset`
- `mapped` (bool)
- `cmc_id` (nullable)
- `cmc_symbol` (nullable)
- `mapping_method` (enum, siehe unten)
- `confidence` (enum: high/medium/low/none)
- `collision` (bool)
- `notes` (string, optional)

### 2.1 Confidence Semantik
- `high`: deterministisch, kollisionsfrei, ohne Override
- `medium`: deterministisch **mit** Override (Override ist die Wahrheit)
- `low`: deterministisch, aber potenziell riskant (z.B. mehrere plausible Kandidaten, aber Regel entscheidet)
- `none`: kein Mapping

Canonical Regel:
- Wenn `require_high_confidence=true` (falls implementiert), dürfen nur `high`/`medium` weiterverarbeitet werden.  
- Standard: `medium` ist erlaubt, weil Override explizit ist.

---

## 3) Mapping Methoden (deterministisch)

### 3.1 M0 — Manual Override (höchste Priorität)
Wenn `mapping_overrides.json` einen Eintrag für `base_asset` oder `exchange_symbol` enthält, gilt dieser:
- `mapping_method = manual_override`
- `confidence = medium`
- Collision wird damit **aufgelöst**, aber weiterhin im Report sichtbar gemacht.

Canonical: Overrides sind version-controlled und müssen eine Notiz tragen (Warum).

### 3.2 M1 — Exact Symbol Match (1:1)
Wenn genau **ein** CMC Asset mit `cmc_symbol == base_asset` existiert:
- `mapping_method = exact_symbol_match`
- `confidence = high`

### 3.3 M2 — Normalized Symbol Match (deterministisch, aber strikt)
Normalization (canonical):
- upper-case
- whitespace strip
- no punctuation transforms (keine fuzzy steps)
- keine string similarity

Wenn genau **ein** CMC Asset mit `normalize(cmc_symbol) == normalize(base_asset)` existiert:
- `mapping_method = normalized_symbol_match`
- `confidence = high`

### 3.4 M3 — Unmapped (none)
Wenn kein eindeutiger Match existiert:
- `mapped = false`
- `confidence = none`
- `mapping_method = none`

> Canonical: **Kein** fuzzy matching (Levenshtein, slug-guessing, name contains) in Phase 1.  
> Wenn du später fuzzy möchtest, muss es explizit als neue Methode M4+ definiert werden, inkl. Tests/Reports.

---

## 4) Collisions (Mehrdeutigkeit)

### 4.1 Collision Definition
Eine Collision liegt vor, wenn:
- Mehr als ein CMC Asset das gleiche `cmc_symbol` hat, das zum `base_asset` passt

Beispiel:
- base_asset `MPLX` passt zu mehreren CMC Einträgen → collision.

### 4.2 Collision Handling (canonical)
- Collision wird **immer** im `collisions_report` protokolliert.
- Ohne Override:
  - `mapped=false`, `confidence=low/none` (canonical Default: **none**, weil nicht eindeutig)
- Mit Override:
  - `mapped=true`, `confidence=medium`, `mapping_method=manual_override`

Canonical Ziel: Collisions sind nie “silent resolved”.

---

## 5) Unmapped Assets
Wenn `mapped=false`:
- Asset wird aus allen Stage-Outputs entfernt, die Market-Cap benötigen (Universe filter).
- Optional: kann als “unmapped watchlist” erscheinen (ohne Scoring), wenn du das willst — muss dann in `PIPELINE.md`/`OUTPUT_SCHEMA.md` explizit beschrieben sein.

---

## 6) Integration in Pipeline (Reihenfolge)

Canonical Reihenfolge (siehe `PIPELINE.md`):
1) Universe fetch (MEXC symbols)
2) Mapping (dieses Dokument)
3) Hard gates (Market-Cap, Liquidity, Risk Flags, Minimum History)
4) erst danach: `percent_rank` Population bilden und Feature/Scoring durchführen

Wichtig:
- Market-Cap Filter ist ohne Mapping nicht möglich.
- Daher sind unmapped Symbole typischerweise nicht eligible.

---

## 7) Reports (Pflicht-Artefakte)

### 7.1 mapping_table
Alle Exchange Symbols + Mapping-Record.

### 7.2 collisions_report
Nur Collisions, inkl. Kandidatenliste:
- `exchange_symbol`, `base_asset`
- Liste möglicher CMC Kandidaten (id/symbol/slug/name)
- Hinweis ob Override existiert

### 7.3 unmapped_report
Alle Symbole ohne Mapping (inkl. Grund).

Canonical: Diese Reports sind deterministisch und gehören in die Run-Artefakte.

---

## 8) Determinismus & Stabilität

### 8.1 Stable ordering
Wenn Listen iteriert werden:
- Sortiere deterministisch (z.B. `exchange_symbol` asc, `cmc_id` asc).

### 8.2 No hidden state
- Mapping darf nicht von “zufälliger” API-Reihenfolge abhängen.
- Alles muss durch Sortierung/Regeln stabilisiert werden.

### 8.3 Versioning
Wenn du Mapping-Logik änderst:
- Canonical Doku aktualisieren
- Tests/Fixtures (mindestens Collision & Unmapped) ergänzen
- Optional: Schema-Version bump in `OUTPUT_SCHEMA.md` wenn Felder sich ändern

---

## 9) Security / Safety Notes
- Keine API Keys in Reports oder Doku.
- Overrides enthalten keine Secrets.

---

## 10) Open Points (für spätere Iteration)
- Exakte Pfade der Reports (abhängig vom aktuellen Repo-Layout)
- Ob Market-Cap Provider ausschließlich CMC ist oder auch alternative Providers existieren
- Ob `require_high_confidence` als Config existiert (v1 hatte so etwas; canonical kann es aufnehmen, wenn im Code vorhanden)
