# Liquidity — Orderbook Top-K Policy & Budget (Canonical)

## Machine Header (YAML)
```yaml
id: LIQ_ORDERBOOK_TOPK_POLICY
status: canonical
top_k_default: 200
fetch_policy:
  pre_rank_by: "proxy_liquidity_score"
  fetch_only_topk: true
determinism:
  stable_symbol_order: true
  tie_breaker_for_fetch: "symbol_asc"
symbol_definition: "full exchange trading pair string (e.g., ETHUSDT)"
missing_orderbook: "treated_as_worst_for_rerank"
```

## 1) Ziel
Orderbook-Fetch ist teuer. Canonical Policy:
1) Proxy-Liquidity vorberechnen (deterministisch)
2) Nur für Top-Kandidaten Orderbooks laden
3) Slippage/Grade berechnen
4) Kandidaten re-ranken (`RE_RANK_RULE.md`)

## 2) Top-K Definition
- Es werden nur die **Top-K** Levels je Seite (bids/asks) berücksichtigt.
- Default: `K = 200`.

## 3) Pre-Rank (Proxy)
- Pre-rank uses `proxy_liquidity_score` (0..1) computed from cross-sectional percent-rank of `quote_volume_24h_usd`.
- This stage must not change the percent-rank population definition.

## 4) Fetch Policy (deterministic)
- Fetch orderbooks for candidates in descending proxy rank order.
- Ties are broken by `symbol` ascending, where `symbol` is the full exchange pair string (e.g., `ETHUSDT`).

## 5) Failure handling
- If orderbook missing: mark slippage as missing and treat as worst in re-rank.
