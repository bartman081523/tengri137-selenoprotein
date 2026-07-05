#!/usr/bin/env python3
"""
phase1f_pixel_similarity.py — V6 Phase 1f: Pixel-basierte Duplikat-Detection.

Da der Triplet-Loss-Ansatz versagt hat (Embeddings diskriminieren nicht zwischen
echten Glyphen und Random-Noise), nutzen wir direkten Pixel-Vergleich:

1. Lade alle 25 V6-Templates
2. Normalisiere auf 32×32 mit weißem Padding
3. Berechne paarweise Cosine-Similarity
4. Finde Duplikate (sim > 0.85)

Zusätzlich: SSIM (Structural Similarity) — robuster gegen kleine Verschiebungen.

Output: models/symbols_20260706_V6/pixel_similarity_report.json
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image


def load_normalized(p, size=32):
    """Lade PNG, zentriere auf size×size mit weißem Padding, normalisiere."""
    img = Image.open(p).convert("L")
    w, h = img.size
    side = max(w, h)
    sq = Image.new("L", (side, side), 255)
    sq.paste(img, ((side - w) // 2, (side - h) // 2))
    sq = sq.resize((size, size), Image.BILINEAR)
    a = np.array(sq, dtype=np.float32) / 255.0
    return a


def pixel_cosine(a, b):
    """Cosine-Similarity auf flachen Pixel-Vektoren."""
    a_f = a.flatten() - a.mean()
    b_f = b.flatten() - b.mean()
    na, nb = np.linalg.norm(a_f), np.linalg.norm(b_f)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a_f, b_f) / (na * nb))


def structural_similarity(a, b):
    """Vereinfachte SSIM."""
    c1 = (0.01) ** 2
    c2 = (0.03) ** 2
    mu_a, mu_b = a.mean(), b.mean()
    sig_a2 = a.var()
    sig_b2 = b.var()
    sig_ab = ((a - mu_a) * (b - mu_b)).mean()
    num = (2 * mu_a * mu_b + c1) * (2 * sig_ab + c2)
    den = (mu_a**2 + mu_b**2 + c1) * (sig_a2 + sig_b2 + c2)
    return float(num / den)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--refs", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--threshold", type=float, default=0.85)
    args = ap.parse_args()

    files = sorted(args.refs.glob("G*.png"))
    print(f"Lade {len(files)} Templates...")

    imgs = {}
    for p in files:
        imgs[p.stem] = load_normalized(p)

    n = len(imgs)
    names = sorted(imgs.keys())

    # Cosine-Similarity
    print(f"\n=== Pixel-Cosine-Similarity (Schwelle {args.threshold}) ===")
    duplicates = []
    matrix = {}
    for i, n1 in enumerate(names):
        for j, n2 in enumerate(names):
            if i < j:
                sim = pixel_cosine(imgs[n1], imgs[n2])
                matrix[f"{n1}__{n2}"] = round(sim, 4)
                if sim > args.threshold:
                    duplicates.append({
                        "glyph_a": n1, "glyph_b": n2,
                        "cosine_sim": round(sim, 4)
                    })
                    print(f"  {n1} <-> {n2}: {sim:.4f}  ← DUPLIKAT")

    # SSIM
    print(f"\n=== Structural-Similarity SSIM (Schwelle {args.threshold}) ===")
    ssim_dups = []
    ssim_matrix = {}
    for i, n1 in enumerate(names):
        for j, n2 in enumerate(names):
            if i < j:
                ssim = structural_similarity(imgs[n1], imgs[n2])
                ssim_matrix[f"{n1}__{n2}"] = round(ssim, 4)
                if ssim > args.threshold:
                    ssim_dups.append({
                        "glyph_a": n1, "glyph_b": n2,
                        "ssim": round(ssim, 4)
                    })

    # Schnittmenge
    cosine_set = {(d["glyph_a"], d["glyph_b"]) for d in duplicates}
    ssim_set = {(d["glyph_a"], d["glyph_b"]) for d in ssim_dups}
    confirmed = cosine_set & ssim_set
    print(f"\nBestätigt durch BEIDE Methoden: {len(confirmed)} Paare")
    for a, b in sorted(confirmed):
        print(f"  {a} <-> {b}")

    # Gruppierung: Connected Components auf Duplikat-Graph
    print(f"\n=== Duplikat-Gruppen ===")
    parent = {n: n for n in names}
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
    for (a, b) in cosine_set:
        union(a, b)

    groups = {}
    for n in names:
        root = find(n)
        groups.setdefault(root, []).append(n)

    print(f"Anzahl Gruppen: {len(groups)}")
    for root, members in sorted(groups.items(), key=lambda x: -len(x[1])):
        if len(members) > 1:
            print(f"  {len(members)} Glyphen zusammen: {sorted(members)}")

    # Output
    output = {
        "metadata": {
            "n_templates": n,
            "threshold": args.threshold,
            "methods": ["pixel_cosine", "ssim"],
        },
        "cosine_duplicates": duplicates,
        "ssim_duplicates": ssim_dups,
        "confirmed_duplicates": [
            {"glyph_a": a, "glyph_b": b} for (a, b) in sorted(confirmed)
        ],
        "duplicate_groups": [
            {"root": root, "members": sorted(members)}
            for root, members in groups.items() if len(members) > 1
        ],
        "n_estimated_unique": len([g for g in groups.values() if len(g) == 1]) +
                              sum(1 for g in groups.values() if len(g) > 1),
        "interpretation": (
            f"Mit Cosine>={args.threshold}: {len(duplicates)} Duplikat-Paare. "
            f"Mit SSIM>={args.threshold}: {len(ssim_dups)} Paare. "
            f"Bestätigt durch beide Methoden: {len(confirmed)} Paare. "
            f"Schätzung der unique Glyphen: {len(groups)} Gruppen."
        )
    }
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWrote {args.out}")
    print(f"Unique-Glyph-Schätzung: {len(groups)} (von {n} Templates)")


if __name__ == "__main__":
    main()
