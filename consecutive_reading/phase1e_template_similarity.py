#!/usr/bin/env python3
"""
phase1e_template_similarity.py — V6 Phase 1e: Cosine-Similarity-Matrix der 25 Templates.

Nach dem Training: Embed alle 25 V6-Templates, berechne paarweise Cosine-Similarity,
identifiziere Duplikate (Ähnlichkeit > 0.85).

Output: models/symbols_20260706_V6/similarity_matrix.json
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
import torch
from PIL import Image

sys.path.insert(0, "models/symbols_20260704_V2")
from inference import EmbeddingNet, preprocess


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", type=Path, required=True,
                    help="models/symbols_20260706_V6/")
    ap.add_argument("--refs", type=Path, required=True,
                    help="bbox/glyph_refs_20260706_V6/refs/")
    ap.add_argument("--out", type=Path, required=True,
                    help="models/symbols_20260706_V6/similarity_report.json")
    args = ap.parse_args()

    device = torch.device("cpu")
    model = EmbeddingNet(emb_dim=64)
    model.load_state_dict(torch.load(args.model_dir / "model.pt",
                                     map_location="cpu", weights_only=True))
    model.eval()

    # Embed alle Templates
    glyph_files = sorted(args.refs.glob("G*.png"))
    print(f"Embedding {len(glyph_files)} templates...")

    glyphs = []
    embs = []
    for p in glyph_files:
        gid = p.stem
        x = preprocess(p).unsqueeze(0)
        with torch.no_grad():
            e = model(x).numpy()[0]
        # Explizit L2-normalisieren
        e = e / max(np.linalg.norm(e), 1e-8)
        glyphs.append(gid)
        embs.append(e)

    embs = np.array(embs)
    n = len(glyphs)

    # Cosine-Similarity (jetzt korrekt -1 bis 1)
    sim = embs @ embs.T

    # Duplikate finden (similarity > 0.85, off-diagonal)
    threshold = 0.85
    print(f"\n=== Cosine-Similarity (Schwelle {threshold}) ===")
    print(f"{'G1':<5} {'G2':<5} {'Sim':<8}")
    duplicates = []
    for i in range(n):
        for j in range(i + 1, n):
            if sim[i, j] > threshold:
                duplicates.append({
                    "glyph_a": glyphs[i],
                    "glyph_b": glyphs[j],
                    "cosine_sim": round(float(sim[i, j]), 4),
                })
                print(f"  {glyphs[i]:<5} {glyphs[j]:<5} {sim[i, j]:.4f}  ← DUPLIKAT")

    # Top-3 ähnlichste für jedes Glyph
    print(f"\n=== Top-3 nächste Nachbarn pro Glyph ===")
    print(f"{'Glyph':<5} {'#1':<5} {'#2':<5} {'#3':<5}")
    nearest = {}
    for i in range(n):
        # Top-3 höchste (außer sich selbst)
        sims = sim[i].copy()
        sims[i] = -1
        top3 = np.argsort(-sims)[:3]
        top3_pairs = [(glyphs[j], round(float(sims[j]), 3)) for j in top3]
        nearest[glyphs[i]] = top3_pairs
        print(f"  {glyphs[i]:<5} {top3_pairs[0][0]}({top3_pairs[0][1]:.3f})  "
              f"{top3_pairs[1][0]}({top3_pairs[1][1]:.3f})  "
              f"{top3_pairs[2][0]}({top3_pairs[2][1]:.3f})")

    # Volle Similarity-Matrix speichern
    sim_dict = {}
    for i in range(n):
        for j in range(n):
            sim_dict[f"{glyphs[i]}__{glyphs[j]}"] = round(float(sim[i, j]), 4)

    output = {
        "metadata": {
            "n_templates": n,
            "model": "EmbeddingNet(64) trained on 1248 V6 token crops (30 epochs)",
            "duplicate_threshold": threshold,
        },
        "duplicates": duplicates,
        "n_duplicate_pairs": len(duplicates),
        "nearest_neighbors": nearest,
        "similarity_matrix": sim_dict,
        "interpretation": (
            f"Mit Schwelle {threshold}: {len(duplicates)} Glyphen-Paare sind 'Duplikate' "
            f"(Cosine-Similarity > {threshold}). "
            "Das war der Haupt-Verdacht (15 Duplikate in Gemini-Inspektion). "
            "Wenn 0 Paare gefunden: alle 25 Templates sind visuell distinkt. "
            "Wenn viele Paare: das Alphabet ist kleiner als 25 Zeichen."
        )
    }
    args.out.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWrote {args.out}")


if __name__ == "__main__":
    main()
