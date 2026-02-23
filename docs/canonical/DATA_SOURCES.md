# Data Sources — Providers, Felder, As-Of & Closed-Candle Policy (Canonical)

## Machine Header (YAML)
```yaml
id: CANON_DATA_SOURCES
status: canonical
policy:
  free_first: true
  paid_optional_phase1: true
providers:
  - name: MEXC
    purpose:
      - universe_symbols
      - tickers_24h_quote_volume
      - ohlcv_1d
      - ohlcv_4h
      - orderbook_depth_topk
  - name: CoinMarketCap
    purpose:
      - market_cap_universe
      - metadata_date_added
      - asset_validation
asof_policy:
  closed_candle_only: true
  rule: "use only candles with closeTime <= asof_ts_ms"
  asof_fallback: "if asof_ts_ms is None: use last available closed candle"
```

## 1) Free-first / Paid-optional
**Grundsatz:** Paid-Quellen dürfen Phase-1 nicht blockieren.  
**CMC (CoinMarketCap)** ist im Betrieb optional/konfigurationsabhängig, darf aber (je nach `run_mode`) erforderlich sein.

**Canonical Regel (aus v2):**
- CMC wird für Market-Cap Universe und Meta (z.B. `date_added`) genutzt.
- `run_mode=standard` kann einen CMC API Key erfordern (abhängig von Implementierung/Config).

> Wenn `run_mode` oder “CMC Pflicht/optional” im Code abweicht, ist **Canonical** anzupassen (AUTHORITY-Regel).

## 2) MEXC (primär)
MEXC liefert:
- Universe: verfügbare Spot-Paare (Quote-Asset Fokus: USDT)
- 24h Ticker: Quote-Volumen (Proxy-Liquidity)
- OHLCV/Klines: 1D und 4H
- Orderbook/Depth: für Slippage/Liquidity Grade (Top-K)

### 2.1 Canonical Felder (konzeptuell)
Für KIs zählt die interne, canonical Benennung (nicht zwingend Provider-Rohfelder):
- `quote_volume_24h` (Proxy-Liquidity; Einheit: Quote-Asset, typ. USDT)
- `ohlcv_1d` / `ohlcv_4h` Candle-Arrays mit mindestens:
  - `open, high, low, close, volume, quote_volume, closeTime`

### 2.2 Rate-Limit Strategie (canonical)
- Erst “cheap” Proxy-Priorisierung
- Orderbook-Fetch nur für Top-K Kandidaten (siehe `docs/canonical/LIQUIDITY/ORDERBOOK_TOPK_POLICY.md`)

## 3) CoinMarketCap (CMC)
CMC liefert:
- Market Cap in USD (Universe-Filter, Segment MidCaps)
- Meta wie `date_added` (Discovery Tag)
- Asset-Validierung (Mapping/ID)

**Canonical Segment-Fokus (aus v2):**
- Market Cap Universe: **100M bis 10B USD** (für Breakout Trend 1–5d)

> Sobald `CONFIGURATION.md` finalisiert ist, wird dort der “Single Default” fixiert und hier referenziert.

## 4) Symbol-Mapping (kritisch)
MEXC-Symbole müssen deterministisch auf CMC-Assets gemappt werden.
- Mapping muss Overrides/Collision-Handling unterstützen
- Keine “magischen” Heuristiken ohne Logging/Report

(Details später in `docs/canonical/PIPELINE.md` und ggf. `docs/canonical/MAPPING.md`.)

## 5) As-Of & Closed-Candle Policy (Canonical, deterministisch)

### 5.1 Definitionen
- `asof_ts_ms`: Zeitpunkt, der die maximal verwendbaren Candles begrenzt.
- `closeTime`: Candle-Endzeitpunkt (Providerfeld).
- `last_closed_candle`: Candle mit `closeTime <= asof_ts_ms`, maximaler closeTime-Wert.

### 5.2 Regel
**Alle Berechnungen verwenden ausschließlich abgeschlossene Candles.**  
Zulässige Candles erfüllen:

- `closeTime_i <= asof_ts_ms`

Wenn `asof_ts_ms` **None** ist:
- Verwende die **letzte verfügbare abgeschlossene** Candle.

### 5.3 Konsequenzen
- Kein Lookahead
- Keine Nutzung “aktueller” (noch nicht abgeschlossener) Candles in Features/Gates/Scores
- Determinismus: identische Inputs + identische Config → identischer Output

## 6) Discovery Tag ohne Paid-Zwang (Canonical)
- Primär: CMC `date_added` (wenn verfügbar)
- Fallback: `first_seen_ts` aus historischer Datenbasis (z.B. älteste 1D Candle im Cache/Fetch), deterministisch definiert

## 7) Reproduzierbarkeit & Manifest
Reports sollen ein Manifest enthalten (konzeptionell):
- Commit hash
- Config hash / Version
- Schema-Version
- As-Of
- verwendete Provider (und ggf. Cache-Freshness)

(Details in `docs/canonical/OUTPUT_SCHEMA.md`.)
