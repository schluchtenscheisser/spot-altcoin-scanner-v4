"""
Breakout Volume Spike Distribution Analysis
============================================
Liest alle Snapshot-Dateien aus snapshots/history/ und extrahiert
spike_combined-Werte aus Breakout-Kandidaten.

Ziel: Empirische Kalibrierung von min_volume_spike (threshold) und
      ideal_volume_spike (100%-Punkt der Score-Kurve).

Aufruf:
    python analyze_volume_spikes.py
    python analyze_volume_spikes.py --snapshots-dir path/to/snapshots/history
    python analyze_volume_spikes.py --min-date 2026-01-01
"""

import argparse
import json
import sys
from pathlib import Path
from collections import defaultdict


def load_breakout_rows(snapshots_dir: Path, min_date: str = None) -> list[dict]:
    """Lädt alle Breakout-Rows aus Snapshot-History."""
    rows = []
    files = sorted(snapshots_dir.glob("????-??-??.json"))

    if not files:
        print(f"ERROR: Keine Snapshot-Dateien in {snapshots_dir}", file=sys.stderr)
        sys.exit(1)

    for path in files:
        date_str = path.stem
        if min_date and date_str < min_date:
            continue

        try:
            with path.open("r", encoding="utf-8") as f:
                snap = json.load(f)
        except Exception as e:
            print(f"WARN: {path} konnte nicht geladen werden: {e}", file=sys.stderr)
            continue

        breakouts = snap.get("scoring", {}).get("breakouts", [])
        for row in breakouts:
            row["_date"] = date_str
            rows.append(row)

    return rows


def percentile(values: list[float], p: float) -> float:
    if not values:
        return float("nan")
    sorted_v = sorted(values)
    idx = (len(sorted_v) - 1) * p / 100
    lo = int(idx)
    hi = min(lo + 1, len(sorted_v) - 1)
    return sorted_v[lo] + (sorted_v[hi] - sorted_v[lo]) * (idx - lo)


def analyze(rows: list[dict]) -> None:
    if not rows:
        print("Keine Breakout-Rows gefunden.")
        return

    spikes = [r["spike_combined"] for r in rows if r.get("spike_combined") is not None]
    spikes_1d = [r["volume_quote_spike_1d"] for r in rows if r.get("volume_quote_spike_1d") is not None]
    spikes_4h = [r["volume_quote_spike_4h"] for r in rows if r.get("volume_quote_spike_4h") is not None]

    dates = sorted(set(r["_date"] for r in rows))
    symbols = set(r.get("symbol", "?") for r in rows)

    print(f"\n{'='*60}")
    print(f"BREAKOUT VOLUME SPIKE DISTRIBUTION")
    print(f"{'='*60}")
    print(f"Zeitraum:    {dates[0]} bis {dates[-1]}  ({len(dates)} Tage)")
    print(f"Total Rows:  {len(rows)}  ({len(symbols)} unique Symbole)")
    print()

    # --- spike_combined Distribution ---
    print("--- spike_combined (0.7×spike_1d + 0.3×spike_4h) ---")
    print(f"  Min:    {min(spikes):.3f}")
    print(f"  P10:    {percentile(spikes, 10):.3f}")
    print(f"  P25:    {percentile(spikes, 25):.3f}")
    print(f"  Median: {percentile(spikes, 50):.3f}")
    print(f"  P75:    {percentile(spikes, 75):.3f}")
    print(f"  P90:    {percentile(spikes, 90):.3f}")
    print(f"  P95:    {percentile(spikes, 95):.3f}")
    print(f"  P99:    {percentile(spikes, 99):.3f}")
    print(f"  Max:    {max(spikes):.3f}")
    print(f"  Mean:   {sum(spikes)/len(spikes):.3f}")
    print()

    # --- Threshold-Analyse ---
    print("--- Anteil Kandidaten ÜBER Threshold (aktuelle Schwellen) ---")
    for threshold in [1.0, 1.2, 1.3, 1.5, 1.7, 2.0, 2.5, 3.0]:
        count = sum(1 for s in spikes if s >= threshold)
        pct = 100 * count / len(spikes)
        marker = "  <-- aktueller threshold" if threshold == 1.5 else \
                 "  <-- aktuelles ideal" if threshold == 2.5 else ""
        print(f"  >= {threshold:.1f}x:  {count:4d} / {len(spikes):4d}  ({pct:5.1f}%){marker}")
    print()

    # --- volume_score=0 Analyse ---
    zero_score = [r for r in rows if r.get("volume_score", 0) == 0.0]
    nonzero_score = [r for r in rows if r.get("volume_score", 0) > 0.0]
    print(f"--- volume_score Verteilung ---")
    print(f"  volume_score = 0:   {len(zero_score):4d} ({100*len(zero_score)/len(rows):.1f}%)")
    print(f"  volume_score > 0:   {len(nonzero_score):4d} ({100*len(nonzero_score)/len(rows):.1f}%)")
    if nonzero_score:
        vs = [r["volume_score"] for r in nonzero_score]
        print(f"  volume_score (>0):  min={min(vs):.1f}  median={percentile(vs,50):.1f}  max={max(vs):.1f}")
    print()

    # --- spike_1d vs spike_4h getrennt ---
    print("--- spike_1d Verteilung ---")
    print(f"  P25={percentile(spikes_1d,25):.3f}  Median={percentile(spikes_1d,50):.3f}  "
          f"P75={percentile(spikes_1d,75):.3f}  P90={percentile(spikes_1d,90):.3f}  "
          f"P95={percentile(spikes_1d,95):.3f}")
    print()
    print("--- spike_4h Verteilung ---")
    print(f"  P25={percentile(spikes_4h,25):.3f}  Median={percentile(spikes_4h,50):.3f}  "
          f"P75={percentile(spikes_4h,75):.3f}  P90={percentile(spikes_4h,90):.3f}  "
          f"P95={percentile(spikes_4h,95):.3f}")
    print()

    # --- Breakout-Qualität: Kandidaten die Gate passieren ---
    gate_pass = [r for r in rows if r.get("execution_gate_pass") is True]
    gate_fail = [r for r in rows if r.get("execution_gate_pass") is False]
    print(f"--- Execution Gate ---")
    print(f"  gate_pass: {len(gate_pass):4d} ({100*len(gate_pass)/len(rows):.1f}%)")
    print(f"  gate_fail: {len(gate_fail):4d} ({100*len(gate_fail)/len(rows):.1f}%)")
    if gate_pass:
        sp = [r["spike_combined"] for r in gate_pass if r.get("spike_combined") is not None]
        print(f"  gate_pass spike_combined: median={percentile(sp,50):.3f}  P75={percentile(sp,75):.3f}  P90={percentile(sp,90):.3f}")
    print()

    # --- Top-20 landing (wenn global_score vorhanden) ---
    with_global = [r for r in rows if r.get("global_score") is not None]
    if with_global:
        print(f"--- global_score vorhanden: {len(with_global)} Rows ---")
        gs = [r["global_score"] for r in with_global]
        print(f"  median={percentile(gs,50):.2f}  P75={percentile(gs,75):.2f}  P90={percentile(gs,90):.2f}  max={max(gs):.2f}")
        print()

    # --- Histogramm spike_combined ---
    print("--- Histogramm spike_combined (Bins á 0.25) ---")
    bins = defaultdict(int)
    for s in spikes:
        bin_key = round(int(s / 0.25) * 0.25, 2)
        bins[bin_key] += 1
    for b in sorted(bins):
        bar = "█" * min(bins[b], 60)
        marker = " <-- threshold" if abs(b - 1.5) < 0.01 else \
                 " <-- ideal" if abs(b - 2.5) < 0.01 else ""
        print(f"  {b:5.2f}x: {bins[b]:4d} {bar}{marker}")
    print()

    # --- Empfehlung ---
    p50 = percentile(spikes, 50)
    p75 = percentile(spikes, 75)
    p90 = percentile(spikes, 90)
    above_1_5 = sum(1 for s in spikes if s >= 1.5) / len(spikes)

    print("--- Kalibrierungs-Hinweise ---")
    print(f"  Nur {100*above_1_5:.1f}% aller Breakout-Kandidaten erreichen spike >= 1.5x")
    print(f"  Median spike: {p50:.3f}x  →  threshold=1.5 liegt über dem Median")
    print(f"  P75:  {p75:.3f}x")
    print(f"  P90:  {p90:.3f}x")
    print()
    print("  Für Ticket C relevant:")
    print(f"    min_volume_spike (threshold=0):  aktuell 1.5x  →  empirisch eher {p50:.1f}x–{p75:.1f}x?")
    print(f"    ideal_volume_spike (score=100):  aktuell 2.5x  →  empirisch eher {p90:.1f}x?")
    print()


def main():
    parser = argparse.ArgumentParser(description="Volume Spike Distribution für Breakout-Kalibrierung")
    parser.add_argument("--snapshots-dir", default="snapshots/history",
                        help="Pfad zum Snapshot-Verzeichnis (default: snapshots/history)")
    parser.add_argument("--min-date", default=None,
                        help="Nur Snapshots ab diesem Datum (YYYY-MM-DD)")
    args = parser.parse_args()

    snapshots_dir = Path(args.snapshots_dir)
    if not snapshots_dir.exists():
        print(f"ERROR: Verzeichnis nicht gefunden: {snapshots_dir}", file=sys.stderr)
        sys.exit(1)

    rows = load_breakout_rows(snapshots_dir, min_date=args.min_date)
    print(f"Geladene Breakout-Rows: {len(rows)}")

    analyze(rows)


if __name__ == "__main__":
    main()
