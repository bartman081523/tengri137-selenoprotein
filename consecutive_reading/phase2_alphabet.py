#!/usr/bin/env python3
"""
phase2_alphabet.py — Glyph-Alphabet-Isolation (DevMind + Crypto-Constraint).

V5 PIVOT: Constraint-Clustering mit vorhergesagter K aus Phase 1.
NICHT Tesseract, NICHT Schmeh. Multi-Resolution-Embeddings (16/32/64 px)
+ Agglomeratives Clustering mit Ziel-K aus Cryptanalysis-Hypothese.

Input:  bbox/substrat_20260705_V5/p{NN}.json  (Phase 0)
        bbox/cryptanalysis_20260705_V5/crypto_report.json  (Phase 1)
        models/symbols_20260704_V2/model.pt  (V2-Warm-Start)
        bbox/components_20260704_V4/p{NN}/p{NN}_glyphs/g*.png  (V4-Crops)
Output: bbox/alphabet_20260705_V5/alphabet.json
        {
          "predicted_K": [25, 35],
          "actual_K": 30,
          "glyphs": [
            {"glyph_id": 1, "label": "diamond_with_dot",
             "medoid_path": "g0001.png",
             "n_occurrences": 87,
             "pages": ["p01", "p05", ...]}
          ]
        }
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
import torch
from PIL import Image
from scipy.cluster.hierarchy import fcluster, linkage
from scipy.spatial.distance import pdist

sys.path.insert(0, str(Path("/run/media/julian/ML4/tengri137/consecutive_reading/models/symbols_20260704_V2")))
from inference import EmbeddingNet, preprocess  # V2-Architektur wiederverwendet


def silhouette_score_numpy(D: np.ndarray, labels: np.ndarray) -> float:
    """Silhouette-Score ohne sklearn. D ist Precomputed-Distance-Matrix."""
    n = len(labels)
    if n < 2:
        return -1.0
    unique_labels = np.unique(labels)
    if len(unique_labels) < 2:
        return -1.0

    silhouettes = np.zeros(n)
    for i in range(n):
        same_cluster = np.where(labels == labels[i])[0]
        other_clusters = [np.where(labels == c)[0] for c in unique_labels if c != labels[i]]
        if len(same_cluster) > 1:
            a_i = np.mean([D[i, j] for j in same_cluster if j != i])
        else:
            a_i = 0.0
        b_i = min(np.mean([D[i, j] for j in c]) for c in other_clusters)
        denom = max(a_i, b_i)
        silhouettes[i] = (b_i - a_i) / denom if denom > 0 else 0.0
    return float(silhouettes.mean())


def multi_res_embed(crop_path: Path, model: EmbeddingNet, sizes=(16, 32, 64)) -> np.ndarray:
    """192-dim Embedding = Konkatenation aus 16+32+64 px."""
    embs = []
    for size in sizes:
        x = preprocess(crop_path, size=size).unsqueeze(0)
        with torch.no_grad():
            e = model(x).numpy().flatten()
        embs.append(e)
    return np.concatenate(embs)


def multi_modal_distance(embs, sizes, aspects, weights=(0.2, 0.5, 0.3)):
    """V4-erbt: Cosine + Size + Aspect (V2-EmbeddingNet liefert enge Cosine)."""
    w_emb, w_size, w_aspect = weights
    sim = embs @ embs.T
    emb_dist = np.clip(1.0 - sim, 0.0, 2.0).astype(np.float32)

    n = len(sizes)
    size_dist = np.zeros((n, n), dtype=np.float32)
    aspect_dist = np.zeros((n, n), dtype=np.float32)
    for i in range(n):
        for j in range(n):
            size_dist[i, j] = abs(np.log(sizes[i] / max(sizes[j], 1))) / 3.0
            aspect_dist[i, j] = abs(np.log(aspects[i] / max(aspects[j], 0.01))) / 1.5
    size_dist = np.clip(size_dist, 0, 2.0)
    aspect_dist = np.clip(aspect_dist, 0, 2.0)

    return (w_emb * emb_dist + w_size * size_dist + w_aspect * aspect_dist).astype(np.float32)


def cluster_with_constraint(embs, sizes, aspects, k_min, k_max):
    """Agglomeratives Clustering, suche bestes K im Bereich [k_min, k_max]."""
    D = multi_modal_distance(embs, sizes, aspects)
    # Linkage auf der Distanz-Matrix
    condensed = pdist(D, metric="euclidean")
    Z = linkage(condensed, method="average")

    best_k = None
    best_silhouette = -1.0
    best_labels = None

    for k in range(k_min, k_max + 1):
        if k >= len(embs):
            break
        labels = fcluster(Z, t=k, criterion="maxclust")
        # Silhouette benötigt mindestens 2 Cluster
        if len(set(labels)) < 2:
            continue
        sil = silhouette_score_numpy(D, labels)
        if sil > best_silhouette:
            best_silhouette = sil
            best_k = k
            best_labels = labels

    return best_k, best_silhouette, best_labels


def medoid_for_cluster(embs, indices):
    """Finde den Index im Cluster, der die geringste mittlere Distanz hat."""
    if len(indices) == 1:
        return indices[0]
    cluster_embs = embs[indices]
    D = 1.0 - (cluster_embs @ cluster_embs.T)
    np.fill_diagonal(D, 0)
    mean_dist = D.mean(axis=1)
    return indices[int(np.argmin(mean_dist))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--components", type=Path, required=True,
                    help="bbox/substrat_20260705_V5/  (Phase 0)")
    ap.add_argument("--crypto-report", type=Path, required=True,
                    help="bbox/cryptanalysis_20260705_V5/crypto_report.json")
    ap.add_argument("--crops", type=Path, required=True,
                    help="bbox/components_20260704_V4/  (V4-Crops als Embedding-Input)")
    ap.add_argument("--model", type=Path, required=True,
                    help="models/symbols_20260704_V2/model.pt")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/alphabet_20260705_V5/")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Crypto-Hypothese laden
    crypto = json.loads(args.crypto_report.read_text())
    k_min, k_max = crypto["hypothesis"]["predicted_alphabet_size"]
    print(f"[Phase 2] Crypto-Constraint: K ∈ [{k_min}, {k_max}]")

    # V2-EmbeddingNet laden
    model = EmbeddingNet(emb_dim=64)
    model.load_state_dict(torch.load(args.model, map_location="cpu", weights_only=True))
    model.eval()
    print(f"[Phase 2] V2-EmbeddingNet geladen: {sum(p.numel() for p in model.parameters())} Parameter")

    # V4-Crops sammeln
    crop_paths = sorted(args.crops.glob("p*/p*_glyphs/g*.png"))
    print(f"[Phase 2] {len(crop_paths)} Crops gefunden")

    if len(crop_paths) < k_min:
        print(f"FEHLER: Zu wenig Crops ({len(crop_paths)} < {k_min})", file=sys.stderr)
        sys.exit(1)

    # Embeddings berechnen
    embs_list = []
    sizes = []
    aspects = []
    valid_paths = []
    for crop in crop_paths:
        try:
            e = multi_res_embed(crop, model)
        except Exception as ex:
            print(f"  WARNUNG: {crop} failed: {ex}", file=sys.stderr)
            continue
        embs_list.append(e)
        # Größe + Aspect aus dem Crop
        img = Image.open(crop).convert("L")
        w, h = img.size
        size_px = w * h
        sizes.append(size_px)
        aspects.append(w / max(h, 1))
        valid_paths.append(crop)

    embs = np.stack(embs_list)
    sizes = np.array(sizes, dtype=np.float32)
    aspects = np.array(aspects, dtype=np.float32)
    print(f"[Phase 2] {len(embs)} gültige Embeddings (192-dim)")

    # Clustering mit Constraint
    print(f"[Phase 2] Clustere mit K ∈ [{k_min}, {k_max}]…")
    best_k, best_sil, labels = cluster_with_constraint(embs, sizes, aspects, k_min, k_max)
    print(f"[Phase 2] Bestes K = {best_k} (Silhouette = {best_sil:.4f})")

    # Cluster analysieren
    cluster_indices = defaultdict(list)
    for idx, lab in enumerate(labels):
        cluster_indices[int(lab)].append(idx)

    glyphs = []
    for cid, indices in sorted(cluster_indices.items()):
        medoid_idx = medoid_for_cluster(embs, indices)
        pages = sorted(set(valid_paths[i].parent.parent.parent.name for i in indices))
        glyphs.append({
            "glyph_id": cid,
            "label": f"cluster_{cid:02d}",
            "medoid_path": str(valid_paths[medoid_idx]),
            "n_occurrences": len(indices),
            "pages": pages,
        })

    output = {
        "predicted_K_range": [k_min, k_max],
        "actual_K": best_k,
        "silhouette": round(best_sil, 4),
        "n_crops_input": len(crop_paths),
        "n_crops_valid": len(embs),
        "hypothesis_label": crypto["hypothesis"]["label"],
        "glyphs": glyphs,
    }
    out_path = args.out / "alphabet.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\n[Phase 2] Alphabet geschrieben: {out_path}")
    print(f"[Phase 2] K = {best_k} Cluster aus {len(embs)} Crops")
    print(f"[Phase 2] Cluster-Verteilung: {sorted([g['n_occurrences'] for g in glyphs], reverse=True)[:10]}…")


if __name__ == "__main__":
    main()
