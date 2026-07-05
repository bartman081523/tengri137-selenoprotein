#!/usr/bin/env python3
"""
phase2_validate_tokens.py — V6 Phase 2: Token-Validation (DevMind).

V6 PIVOT: Validiert die Token-Stream-Qualität.
1. Coverage: Was % der Inken-Pixel sind durch Token-Match erklärt?
2. Glyph-Verteilung: Sind alle 25 Referenz-Glyphen im Stream vertreten?
3. Per-Page-Statistik: Welche Pages haben viele/wenige Tokens?
4. Confidence-Analyse: Anteil conf >= 0.95, 0.85, 0.80

Output: bbox/token_validation_20260706_V6/validation.json
"""
import argparse
import json
from collections import Counter
from pathlib import Path

import numpy as np
from PIL import Image


def compute_coverage(page_id: str, pages_png_dir: Path, tokens: list, padding: int = 2) -> float:
    """Wie viel % der Inken-Pixel sind durch Token-Bboxen abgedeckt?"""
    page_num = int(page_id[1:])
    png_path = pages_png_dir / f"page-{page_num:02d}.png"
    if not png_path.exists():
        return 0.0
    arr = np.array(Image.open(png_path).convert("L"))
    ink = arr < 200
    if ink.sum() == 0:
        return 0.0
    # Maske der Token-Bereiche
    covered = np.zeros_like(ink)
    for t in tokens:
        x, y, w, h = t["x"], t["y"], t["w"], t["h"]
        x0 = max(0, x - padding)
        y0 = max(0, y - padding)
        x1 = min(arr.shape[1], x + w + padding)
        y1 = min(arr.shape[0], y + h + padding)
        covered[y0:y1, x0:x1] = True
    # Coverage: Pixel die sowohl Tinte als auch Token-coved sind
    covered_ink = (ink & covered).sum()
    total_ink = ink.sum()
    return covered_ink / total_ink if total_ink > 0 else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True)
    ap.add_argument("--pages-png", type=Path, required=True)
    ap.add_argument("--glyphs-final", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    glyphs_final = json.loads(args.glyphs_final.read_text())["glyphs"]
    expected_glyphs = {g["glyph_id"] for g in glyphs_final}
    print(f"Expected glyphs: {len(expected_glyphs)}")

    per_page = {}
    all_tokens = []
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        tokens = d["tokens"]
        per_page[pid] = {
            "n_tokens": len(tokens),
            "n_unique": len(set(t["glyph_id"] for t in tokens)),
            "mean_conf": float(np.mean([t["conf"] for t in tokens])) if tokens else 0.0,
            "coverage_ink": round(compute_coverage(pid, args.pages_png, tokens), 4),
        }
        all_tokens.extend(tokens)

    # Globale Statistik
    counts = Counter(t["glyph_id"] for t in all_tokens)
    confs = [t["conf"] for t in all_tokens]
    found_glyphs = set(counts.keys())

    missing = expected_glyphs - found_glyphs
    extra = found_glyphs - expected_glyphs

    # Confidence-Buckets
    conf_buckets = {
        ">=0.95": sum(1 for c in confs if c >= 0.95),
        "0.90-0.95": sum(1 for c in confs if 0.90 <= c < 0.95),
        "0.85-0.90": sum(1 for c in confs if 0.85 <= c < 0.90),
        "<0.85": sum(1 for c in confs if c < 0.85),
    }

    # Per-Page-Report
    print(f"\n=== Per-Page Validation ===")
    print(f"{'Page':<5} {'Tokens':<8} {'Unique':<8} {'Conf':<7} {'Coverage':<10}")
    for pid in sorted(per_page.keys()):
        s = per_page[pid]
        print(f"  {pid} {s['n_tokens']:<8} {s['n_unique']:<8} {s['mean_conf']:.3f}  {s['coverage_ink']:.2%}")

    # Aggregat
    n_total = len(all_tokens)
    result = {
        "metadata": {
            "n_expected_glyphs": len(expected_glyphs),
            "n_pages": len(per_page),
            "n_tokens_total": n_total,
        },
        "glyph_coverage": {
            "found": sorted(found_glyphs),
            "missing": sorted(missing),
            "extra": sorted(extra),
            "n_found": len(found_glyphs),
            "n_missing": len(missing),
        },
        "confidence_buckets": conf_buckets,
        "per_page": per_page,
        "global": {
            "n_tokens": n_total,
            "n_unique": len(found_glyphs),
            "mean_conf": float(np.mean(confs)) if confs else 0.0,
            "median_conf": float(np.median(confs)) if confs else 0.0,
            "min_conf": float(min(confs)) if confs else 0.0,
            "max_conf": float(max(confs)) if confs else 0.0,
        },
        "interpretation": (
            f"Von {len(expected_glyphs)} erwarteten Glyphen wurden {len(found_glyphs)} gefunden. "
            f"Fehlend: {len(missing)}. "
            f"Coverage: {np.mean([s['coverage_ink'] for s in per_page.values()]):.2%} (Ziel: > 60%). "
            f"High-Confidence (>= 0.95): {conf_buckets['>=0.95']} ({conf_buckets['>=0.95']/n_total*100:.1f}%)."
        )
    }
    out_path = args.out / "validation.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    # Print
    print(f"\n=== Global Statistics ===")
    print(f"  Total tokens: {n_total}")
    print(f"  Unique glyphs: {len(found_glyphs)}/{len(expected_glyphs)} (missing: {len(missing)})")
    print(f"  Mean confidence: {result['global']['mean_conf']:.3f}")
    print(f"  Confidence >= 0.95: {conf_buckets['>=0.95']} ({conf_buckets['>=0.95']/n_total*100:.1f}%)")
    print(f"  Average coverage: {np.mean([s['coverage_ink'] for s in per_page.values()]):.2%}")
    print(f"\nMissing glyphs: {sorted(missing)}")
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
