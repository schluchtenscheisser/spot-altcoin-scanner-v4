# AUTHORITY — Dokument-Hierarchie & Quelle der Wahrheit (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_AUTHORITY
status: canonical
canonical_root: docs/canonical
autodocs_read_only:
  - docs/code_map.md
  - docs/GPT_SNAPSHOT.md
precedence_order:
  - docs/canonical/*
  - docs/*
  - docs/code_map.md
  - docs/GPT_SNAPSHOT.md
  - docs/legacy/*
change_process:
  - update_canonical_docs_first
  - update_tests_and_fixtures
  - regenerate_autodocs_via_ci
```

## Ziel
Diese Datei verhindert widersprüchliche “Wahrheiten” in der Doku. Für KI-Modelle gilt: **Canonical ist deterministisch und vollständig definiert.** Wenn etwas nicht definiert ist, ist es **nicht erlaubt** (kein Interpretationsspielraum).

## Canonical Suite (Soll-Zustand)
Alle Dokumente unter `docs/canonical/` sind die **Single Source of Truth** für:
- Definitionen (Formeln, Parameter, Limits, Tie-Handling, Closed-Candle Policy)
- Setup-Regeln (Gates, Validität, Score-Logik)
- Output-Schema & Limits
- Liquidity/Slippage Regeln
- Backtest-/Evaluation-Definitionen (Analytics-only)

## Operative Doku (Ist-Zustand, unterstützend)
Dokumente unter `docs/` (außer Auto-Doks) sind unterstützend (z.B. Lauf-/Dev-Infos). Bei Widerspruch gilt Canonical.

## Auto-Dokumente (Ist-Zustand, auto-updated, read-only)
Diese Dateien werden per GitHub Actions aktualisiert und dürfen **nicht manuell editiert** werden:
- `docs/code_map.md` (Code-Struktur/Module/Pfade)
- `docs/GPT_SNAPSHOT.md` (aktueller Lauf-/Betriebszustand)

Auto-Dokumente sind **Status/Referenz**, aber **nicht** Requirements-Quelle.

## Legacy Doku (nur Kontext)
Alles unter `docs/legacy/` ist historischer Kontext (Tickets, alte Specs, Notizen). Bei Widerspruch gilt Canonical.

## Precedence (bei Widerspruch)
1) `docs/canonical/*`  
2) `docs/*` (nicht auto-generated)  
3) `docs/code_map.md`, `docs/GPT_SNAPSHOT.md` (Status/Referenz)  
4) `docs/legacy/*` (Kontext)

## Änderungsprozess (drift-frei)
Regel: Änderungen laufen **immer** über Canonical, dann Tests/Fixtures, dann Auto-Doks.
- Fachliche Änderung → zuerst Canonical Spez anpassen
- Dann Tests/Golden Fixtures aktualisieren (Determinismus & Invariants)
- Dann Code/CI laufen lassen, Auto-Doks werden aktualisiert

## Verbotene Praktiken
- “Stille” Logikänderungen ohne Canonical Update
- Fuzzy/heuristische Interpretation in der Doku (“ungefähr”, “meistens”)
- Nicht-deterministische Regeln ohne explizite Determinismus-Sektion
