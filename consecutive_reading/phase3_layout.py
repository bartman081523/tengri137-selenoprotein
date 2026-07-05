#!/usr/bin/env python3
"""
phase3_layout.py — Multi-Layout-Analyse (DevMind).

V5 PIVOT: V4 hat alle Pages gleich behandelt (Y-Zeilen-Clustering).
V5 erkennt pro Page den Layout-Typ und wendet die passende Region-Detection an.

Layout-Typen (aus Gemini-Korrektur 2026-07-05):
  - fliesstext: Y-Zeilen-Clustering auf Glyph-Centroids
  - magic_cube: 3x3-Raster aus Glyphen (p05, p06)
  - formel_2d: 2D-Layout mit Brüchen/Exponenten (p17-p19)
  - chemie_struktur: Hexagonale Ringe + Bindungslinien (p23)
  - silhouette: 1 großer Tintenklecks + Glyphen drumherum (p18, p22)
  - unbekannt: nicht klassifizierbar

Heuristik pro Page:
  - Anzahl Komponenten > 800 UND > 90% micro → wahrscheinlich Burumut/Magic-Cube
  - Y-Verteilung: Standardabweichung niedrig → gleichmäßige Zeilen
  - Mehrere Komponenten pro Y-Band: eher Glyphen-Cluster als Magic-Cube
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np


def classify_page_layout(components: list, image_size: list, page_id: str = "") -> dict:
    """Klassifiziere das Layout einer einzelnen Page.

    Wenn page_id in der Gemini-Override-Liste ist, verwende diese (autoritative Quelle).
    Sonst verwende die automatische Heuristik.
    """
    # Gemini-Korrektur 2026-07-05: autoritative Page-Typen
    GEMINI_OVERRIDES = {
        "p05": "magic_cube",        # 3D-Würfel mit Ziffern
        "p06": "magic_cube",        # 3D-Würfel mit Ziffern
        "p18": "silhouette_formel", # Tintenklecks + mathematische Formeln
        "p22": "silhouette_formel", # Silhouette + Formeln
        "p23": "chemie_struktur",   # Cytosin/Thymin
        # p17-p21: Burumut-Block (einzelne lateinische Großbuchstaben in einer Reihe)
        "p17": "burumut_block",
        "p19": "burumut_block",
        "p20": "burumut_block",
        "p21": "burumut_block",
    }

    if page_id in GEMINI_OVERRIDES:
        return {
            "layout_type": GEMINI_OVERRIDES[page_id],
            "confidence": 0.95,  # hoch, da autoritative Gemini-Korrektur
            "scores": {GEMINI_OVERRIDES[page_id]: 3.0},
            "n_components": len(components),
            "n_micro": sum(1 for c in components if c["size_px"] < 100),
            "n_meso": sum(1 for c in components if 100 <= c["size_px"] < 2000),
            "n_macro": sum(1 for c in components if c["size_px"] >= 2000),
            "micro_ratio": round(sum(1 for c in components if c["size_px"] < 100) / max(len(components), 1), 3),
            "reasons": [f"Gemini-Override 2026-07-05 für {page_id}"],
        }

    if not components:
        return {"layout_type": "unbekannt", "confidence": 0.0, "reasons": ["keine Komponenten"]}

    n = len(components)
    sizes = np.array([c["size_px"] for c in components])
    n_micro = int(np.sum(sizes < 100))
    n_meso = int(np.sum((sizes >= 100) & (sizes < 2000)))
    n_macro = int(np.sum(sizes >= 2000))
    micro_ratio = n_micro / n

    # Y-Verteilung
    ys = np.array([c["centroid"][1] for c in components])
    y_std = float(np.std(ys))
    y_range = float(np.max(ys) - np.min(ys))

    # Komponenten pro Y-Band (50-px-Bänder)
    band_size = 50
    bands = defaultdict(int)
    for y in ys:
        band_idx = int(y // band_size)
        bands[band_idx] += 1
    band_counts = list(bands.values())
    max_band = max(band_counts) if band_counts else 0
    n_bands_with_many = sum(1 for c in band_counts if c >= 9)

    # X-Verteilung (zur Magic-Cube-Erkennung)
    xs = np.array([c["centroid"][0] for c in components])
    x_band_size = 50
    x_bands = defaultdict(int)
    for x in xs:
        x_band_idx = int(x // x_band_size)
        x_bands[x_band_idx] += 1
    x_band_counts = list(x_bands.values())

    reasons = []
    scores = defaultdict(float)

    # Heuristik 1: Viele Mikro-Komponenten UND 3x3 X+Y Raster → echter Magic-Cube
    #   X-Bänder mit ≥ 3 Komponenten UND Y-Bänder mit ≥ 3 Komponenten
    x_bands_with_many = sum(1 for c in x_band_counts if c >= 3)
    has_3x3 = x_bands_with_many >= 3 and n_bands_with_many >= 3
    if has_3x3 and micro_ratio > 0.5:
        scores["magic_cube"] = 3.0
        reasons.append(f"3x3-Raster: {x_bands_with_many} X-Bänder, {n_bands_with_many} Y-Bänder mit ≥3 Komp.")
    elif micro_ratio > 0.9 and n > 500:
        scores["magic_cube_or_burumut"] = 1.5
        reasons.append(f"{micro_ratio:.1%} micro (Schwelle 90%), aber kein 3x3-Raster")

    # Heuristik 2: Silhouette-Charakteristik: 1 großer Macro + viel micro drumherum
    if n_macro == 1 and n_micro > 100 and not has_3x3:
        scores["silhouette"] = 2.5
        reasons.append(f"1 Macro + {n_micro} micro → Silhouette")

    # Heuristik 3: p17-p22 Burumut-Block (viele isolierte Mikro-Punkte, aber KEIN 3x3-Raster)
    #   Magic-Cube hat gleichmäßige Verteilung; Burumut ist eine isolierte Sequenz
    if micro_ratio > 0.95 and not has_3x3 and n_micro > 500:
        scores["burumut_block"] = 2.5
        reasons.append(f"{micro_ratio:.1%} micro ohne 3x3 → Burumut-Sequenz")

    # Heuristik 4: p17-p19 Formel (mathematische Brüche mit meso-Komp.)
    if n_meso > n_micro * 0.5 and y_std > 200 and not has_3x3:
        scores["formel_2d"] = 1.5
        reasons.append(f"{n_meso} meso, Y-Stddev {y_std:.0f} → Formel")

    # Heuristik 5: p23 Chemie — moderate Mikro + moderate Meso + ungleichmäßige X-Verteilung
    #   Hexagonale Ringe + Bindungslinien erzeugen ein charakteristisches Muster
    if (n_micro > 500 and n_meso > 100 and n_meso < 300
            and not has_3x3 and n_micro / n_meso > 2):
        scores["chemie_struktur"] = 3.0
        scores["magic_cube"] = scores.get("magic_cube", 0) + 0.3
        reasons.append(f"{n_micro} micro + {n_meso} meso, micro/meso={n_micro/n_meso:.1f} → Chemie (Cytosin/Thymin)")

    # Heuristik 6: p09 hat viele Komponenten → Magic-Cube oder Magic-Cube-Variante?
    #   Magic-Cube ist spezifisch: 3x3-Raster + 9 Bänder
    if n > 800 and not has_3x3 and micro_ratio < 0.5:
        scores["formel_2d"] = scores.get("formel_2d", 0) + 1.0
        reasons.append(f"{n} Komp., <50% micro, kein 3x3 → komplexer Fließtext")

    # Default
    if not scores:
        scores["fliesstext"] = 1.0
        reasons.append("Keine Magic-Cube/Silhouette-Indikatoren → Fließtext-Default")

    # Bester Layout-Typ
    best_layout = max(scores, key=scores.get)
    best_score = scores[best_layout]
    confidence = min(best_score / 3.0, 1.0)

    return {
        "layout_type": best_layout,
        "confidence": round(confidence, 3),
        "scores": dict(scores),
        "n_components": n,
        "n_micro": n_micro,
        "n_meso": n_meso,
        "n_macro": n_macro,
        "micro_ratio": round(micro_ratio, 3),
        "y_std": round(y_std, 1),
        "n_bands_with_many": n_bands_with_many,
        "reasons": reasons,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--substrat", type=Path, required=True,
                    help="bbox/substrat_20260705_V5/")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/layout_20260705_V5/")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    layout_summary = {}
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        sub_path = args.substrat / f"{page_id}.json"
        if not sub_path.exists():
            print(f"  {page_id}: SKIP (kein Substrat)", file=sys.stderr)
            continue
        data = json.loads(sub_path.read_text())
        components = data.get("components", [])
        image_size = data.get("image_size", [1125, 1625])

        result = classify_page_layout(components, image_size, page_id=page_id)
        layout_summary[page_id] = result

        out_path = args.out / f"{page_id}.json"
        out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(f"  {page_id}: {result['layout_type']:<20} "
              f"(conf={result['confidence']:.2f}, n={result['n_components']}, "
              f"micro={result['n_micro']})")

    # Summary
    type_counts = Counter(v["layout_type"] for v in layout_summary.values())
    print(f"\nLayout-Verteilung:")
    for lt, n in sorted(type_counts.items(), key=lambda x: -x[1]):
        print(f"  {lt:<20}: {n} pages")

    (args.out / "layout_summary.json").write_text(
        json.dumps(layout_summary, indent=2, ensure_ascii=False))
    print(f"\n[Phase 3] {len(layout_summary)} Pages klassifiziert")


if __name__ == "__main__":
    main()
