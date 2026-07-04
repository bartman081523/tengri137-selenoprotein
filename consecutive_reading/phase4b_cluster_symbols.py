#!/usr/bin/env python3
"""
Phase 4b — Agglomeratives Clustering + Symbol-Index (User: Auto-Silhouette).

Liest:
  - bbox/embeddings_<TS>/crop_embeddings.npz
  - bbox/vision_qa_<TS>/p{NN}/p{NN}_glyphs/g*.json (Vision-Beschreibungen)
  - bbox/vision_qa_<TS>/p{NN}/p{NN}_page.json (Vision-Region-Info)

Schreibt:
  - bbox/symbols_global_<TS>/symbols_index.json
  - bbox/symbols_global_<TS>/p{NN}_symbols.json (pro Seite, alle Symbole)
  - bbox/symbols_global_<TS>/clusters.json (Debug-Output)
  - bbox/symbols_global_<TS>/clustering_stats.json
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import pdist, squareform

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def load_embeddings(emb_path: Path):
    """Lade Embeddings + Metadaten."""
    d = np.load(emb_path, allow_pickle=True)
    embs = d["embeddings_normalized"].astype(np.float32)  # L2-normalisiert
    return {
        "embeddings": embs,
        "raw_embeddings": d["embeddings"].astype(np.float32),
        "paths": d["paths"],
        "page_id": d["page_id"],
        "crop_index": d["crop_index"],
        "kind": d["kind"],
        "bbox": d["bbox"],  # placeholder
        "area_px": d["area_px"],
        "ink_ratio": d["ink_ratio"],
        "aspect_ratio": d["aspect_ratio"],
    }


def load_vision_data(vision_dir: Path):
    """Lade alle Vision-glyph-Beschreibungen + page-Outputs."""
    vision = {}
    for page_dir in sorted(vision_dir.glob("p*")):
        if not page_dir.is_dir():
            continue
        page_id = page_dir.name
        # Lade Vision-glyphs
        for gfile in (page_dir / f"{page_id}_glyphs").glob("g*.json"):
            try:
                d = json.loads(gfile.read_text())
            except json.JSONDecodeError:
                continue
            if "error" in d and "crop_path" not in d:
                continue
            # Extrahiere crop_filename (nur p{NN}_blank_NNN oder p{NN}_color_NNN)
            crop_path = d.get("crop_path", "")
            m = re.search(r"p\d{2}_(?:blank|color)_\d+\.png", crop_path)
            if not m:
                continue
            key = m.group(0)
            vision[key] = {
                "page": page_id,
                "kind": d.get("kind"),
                "description": d.get("description"),
                "unicode_codepoint": d.get("unicode_codepoint"),
                "confidence": d.get("confidence"),
                "position": d.get("position"),
                "crop_bbox": d.get("crop_bbox"),
            }
    return vision


def multi_modal_distance(embs: np.ndarray, areas: np.ndarray,
                         aspects: np.ndarray, weights=(0.7, 0.15, 0.15)):
    """Kombinierte Distanz-Matrix:
       - 0.7 * cosine_distance(embeddings)
       - 0.15 * size_distance (1 - |log(area_ratio)|, geclippt)
       - 0.15 * aspect_distance (1 - |log(aspect_ratio)|, geclippt)
    """
    w_emb, w_size, w_aspect = weights
    # Cosine: 1 - sim, da embs L2-normalized
    sim = embs @ embs.T
    emb_dist = np.clip(1.0 - sim, 0.0, 2.0).astype(np.float32)

    # Size: |log(area_a / area_b)|
    log_areas = np.log(np.maximum(areas, 1.0))
    size_diff = np.abs(log_areas[:, None] - log_areas[None, :])
    size_dist = np.clip(size_diff / 3.0, 0.0, 1.0).astype(np.float32)  # normalize

    # Aspect: |log(aspect_a / aspect_b)|
    log_aspects = np.log(np.maximum(aspects, 0.01))
    aspect_diff = np.abs(log_aspects[:, None] - log_aspects[None, :])
    aspect_dist = np.clip(aspect_diff / 1.5, 0.0, 1.0).astype(np.float32)

    combined = (w_emb * emb_dist
                + w_size * size_dist
                + w_aspect * aspect_dist).astype(np.float32)
    return combined


def silhouette_score_subsample(D: np.ndarray, labels: np.ndarray,
                              n_sample: int = 200, rng=None) -> float:
    """Silhouette-Score auf Subsample (numpy-only, kein sklearn)."""
    if rng is None:
        rng = np.random.default_rng(42)
    n = D.shape[0]
    if n > n_sample:
        idx = rng.choice(n, size=n_sample, replace=False)
        D_sub = D[np.ix_(idx, idx)]
        labels_sub = labels[idx]
    else:
        D_sub = D
        labels_sub = labels
    unique = np.unique(labels_sub)
    if len(unique) < 2:
        return 0.0
    sil = []
    for i in range(D_sub.shape[0]):
        same = labels_sub == labels_sub[i]
        if same.sum() == 1:
            continue
        a = D_sub[i, same].mean() if same.sum() > 1 else 0.0
        # b: mittlere Distanz zur nächsten anderen Klasse
        b = np.inf
        for u in unique:
            if u == labels_sub[i]:
                continue
            mask = labels_sub == u
            if mask.sum() == 0:
                continue
            d = D_sub[i, mask].mean()
            if d < b:
                b = d
        if b == np.inf or a == 0 and b == 0:
            continue
        s = (b - a) / max(a, b)
        sil.append(s)
    return float(np.mean(sil)) if sil else 0.0


def find_best_threshold(D: np.ndarray, thresholds=(0.05, 0.10, 0.15, 0.20,
                                                   0.25, 0.30, 0.40, 0.50)):
    """Auto-Silhouette: teste verschiedene Thresholds, wähle besten."""
    condensed = squareform(D, checks=False)
    Z = linkage(condensed, method="average")
    best_t, best_s, best_labels = 0.30, -1.0, None
    results = []
    for t in thresholds:
        labels = fcluster(Z, t=t, criterion="distance")
        n_clusters = len(set(labels))
        if n_clusters < 2 or n_clusters > len(labels) - 1:
            results.append({"t": t, "n_clusters": n_clusters, "silhouette": -1.0})
            continue
        s = silhouette_score_subsample(D, labels)
        results.append({"t": t, "n_clusters": n_clusters, "silhouette": s})
        if s > best_s:
            best_s = s
            best_t = t
            best_labels = labels
    if best_s < 0.3:
        # Fallback auf t=0.30
        best_t = 0.30
        best_labels = fcluster(Z, t=best_t, criterion="distance")
    return best_t, best_s, best_labels, results


def assign_cluster_label(members: list, vision: dict) -> dict:
    """5-stufige Priorität für Cluster-Label."""
    # Sammle alle Vision-Beschreibungen in diesem Cluster
    kinds = []
    descriptions = []
    confidences = []
    unicodes = []
    for m in members:
        key = Path(m["path"]).name
        v = vision.get(key)
        if v and v.get("kind"):
            kinds.append((v["kind"], v.get("confidence", 0.0)))
            if v.get("description"):
                descriptions.append(v["description"])
            if v.get("confidence"):
                confidences.append(v["confidence"])
            if v.get("unicode_codepoint"):
                unicodes.append(v["unicode_codepoint"])

    if not kinds:
        return {
            "kind": "unknown", "label_source": "unknown",
            "description": "", "unicode_codepoint": "",
            "vision_confidence": 0.0,
        }

    # P0: Vision-Crop mit höchster Confidence
    best = max(kinds, key=lambda x: x[1])
    # P2: Mehrheits-Vote
    counter = Counter(k[0] for k in kinds)
    majority_kind, majority_count = counter.most_common(1)[0]

    # Source: "vision_glyph" wenn mind. 1 Vision-Crop mit conf >= 0.7
    has_high_conf = any(c >= 0.7 for c in confidences)
    if has_high_conf:
        source = "vision_glyph"
        chosen = best[0]
    elif majority_count > 1:
        source = "consensus"
        chosen = majority_kind
    else:
        source = "vision_glyph"
        chosen = best[0]

    # Description: längste (most detailed)
    description = max(descriptions, key=len) if descriptions else ""

    # Unicode: häufigstes (nicht-leer)
    unicode = ""
    if unicodes:
        unicode = Counter(unicodes).most_common(1)[0][0]

    return {
        "kind": chosen,
        "label_source": source,
        "description": description,
        "unicode_codepoint": unicode,
        "vision_confidence": float(np.mean(confidences)) if confidences else 0.0,
    }


def medoid(embs: np.ndarray, indices: list) -> int:
    """Element mit minimaler durchschnittlicher Distanz zu allen anderen."""
    sub = embs[indices]
    D = squareform(pdist(sub, metric="cosine"), checks=False)
    mean_d = D.mean(axis=1)
    return indices[int(np.argmin(mean_d))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--embeddings", type=Path, required=True,
                    help="bbox/embeddings_<TS>/crop_embeddings.npz")
    ap.add_argument("--vision", type=Path, required=True,
                    help="bbox/vision_qa_<TS>/")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Lade Embeddings
    data = load_embeddings(args.embeddings)
    embs = data["embeddings"]
    paths = data["paths"]
    n = len(paths)
    print(f"Loaded {n} embeddings (dim={embs.shape[1]})")

    # Lade Vision-Daten
    vision = load_vision_data(args.vision)
    print(f"Loaded {len(vision)} vision-glyph descriptions")

    # Berechne Distanz-Matrix
    D = multi_modal_distance(embs, data["area_px"], data["aspect_ratio"])
    print(f"Distance matrix: {D.shape}, mean={D.mean():.3f}, max={D.max():.3f}")

    # Auto-Silhouette: finde besten Threshold
    print("Auto-silhouette search...")
    best_t, best_s, labels, threshold_results = find_best_threshold(D)
    print(f"Best threshold: t={best_t}, silhouette={best_s:.3f}")
    n_clusters = len(set(labels))
    print(f"Found {n_clusters} clusters")

    # Cluster-Stats
    cluster_sizes = Counter(labels)
    singletons = sum(1 for c in cluster_sizes.values() if c == 1)
    multi = n_clusters - singletons
    print(f"  Singletons: {singletons}, Multi-member: {multi}")

    # Sammle cluster members
    cluster_members = defaultdict(list)
    for i, lab in enumerate(labels):
        cluster_members[lab].append(i)

    # Label-Assignment + Medoid pro Cluster
    clusters = []
    for cid, members_idx in sorted(cluster_members.items()):
        members = []
        for i in members_idx:
            members.append({
                "path": str(paths[i]),
                "crop_path": str(paths[i]),
                "page": str(data["page_id"][i]),
                "crop_index": int(data["crop_index"][i]),
                "bbox": data["bbox"][i].tolist(),  # placeholder
                "area_px": float(data["area_px"][i]),
                "ink_ratio": float(data["ink_ratio"][i]),
                "aspect_ratio": float(data["aspect_ratio"][i]),
            })
        # Medoid (Index in members_idx, nicht in members)
        medoid_idx = medoid(embs, members_idx)
        # Mappe auf Position in members
        medoid_pos = members_idx.index(medoid_idx)
        members[medoid_pos]["is_medoid"] = True
        # Intra-cluster distance
        sub = embs[members_idx]
        if len(members_idx) > 1:
            D_sub = pdist(sub, metric="cosine")
            intra_mean = float(D_sub.mean())
            intra_max = float(D_sub.max())
        else:
            intra_mean = 0.0
            intra_max = 0.0
        # Label
        label = assign_cluster_label(members, vision)
        # Cluster-ID
        kind_safe = re.sub(r"[^A-Z0-9_]", "_", label["kind"].upper())[:20] or "UNKNOWN"
        cluster_id = f"GEOM_{kind_safe}_{cid:04d}"
        # Representative crop
        rep = members[medoid_pos]
        cluster_obj = {
            "cluster_id": cluster_id,
            "kind": label["kind"],
            "label_source": label["label_source"],
            "description": label["description"],
            "unicode_codepoint": label["unicode_codepoint"],
            "size": len(members_idx),
            "is_singleton": len(members_idx) == 1,
            "intra_cluster_distance_mean": intra_mean,
            "intra_cluster_distance_max": intra_max,
            "members": members,
            "representative_crop": {
                "crop_path": rep["path"],
                "page": rep["page"],
                "bbox": rep["bbox"],
            },
            "confidence": (0.6 * label["vision_confidence"]
                           + 0.4 * (1.0 - intra_mean)
                           if len(members_idx) > 1
                           else 0.1),
        }
        clusters.append(cluster_obj)

    # Sort by size desc (largest first), then by first page
    def sort_key(c):
        rep_page = c["representative_crop"]["page"]
        rep_bbox = c["representative_crop"]["bbox"]
        return (-c["size"], rep_page, rep_bbox[1] if len(rep_bbox) > 1 else 0,
                rep_bbox[0] if len(rep_bbox) > 0 else 0)
    clusters.sort(key=sort_key)

    # Symbol-Index in Lesereihenfolge: alle Cluster sortiert nach (first_seen_page, top, left)
    # Rep-Position aus Member-Sicht: nimm das Member, das im Fließtext am frühesten vorkommt
    def reading_order(c):
        # Sortiere Members des Clusters nach (page, top, left) und nimm den ersten
        sorted_members = sorted(c["members"],
                                key=lambda m: (m["page"],
                                               m["bbox"][1] if len(m["bbox"]) > 1 else 0,
                                               m["bbox"][0] if len(m["bbox"]) > 0 else 0))
        first = sorted_members[0]
        return (first["page"],
                first["bbox"][1] if len(first["bbox"]) > 1 else 0,
                first["bbox"][0] if len(first["bbox"]) > 0 else 0)

    # Erst reading-order sort, dann symbol_id zuweisen
    clusters_ro = sorted(clusters, key=reading_order)

    # Schreibe symbol_index
    symbols_index = []
    for sym_id, c in enumerate(clusters_ro, start=1):
        # Sammle Occurrences aus Members
        occurrences = []
        for m in c["members"]:
            occ = {
                "page": m["page"],
                "bbox": m["bbox"],
                "crop_path": m["path"],
                "ink_ratio": m["ink_ratio"],
            }
            if c["size"] > 0:
                key = Path(m["path"]).name
                v = vision.get(key)
                if v and v.get("confidence") is not None:
                    occ["vision_confidence"] = v["confidence"]
            occurrences.append(occ)
        # First position (top, left) des ersten Members
        first = sorted(c["members"],
                       key=lambda m: (m["page"],
                                      m["bbox"][1] if len(m["bbox"]) > 1 else 0,
                                      m["bbox"][0] if len(m["bbox"]) > 0 else 0))[0]
        geometry_id = c["cluster_id"]
        symbol = {
            "symbol_id": sym_id,
            "cluster_id": c["cluster_id"],
            "geometry_id": geometry_id,
            "first_seen_page": first["page"],
            "first_seen_position": first["bbox"],
            "kind": c["kind"],
            "label_source": c["label_source"],
            "description": c["description"],
            "unicode_codepoint": c["unicode_codepoint"],
            "representative_crop_path": c["representative_crop"]["crop_path"],
            "geometry": {
                "aspect_ratio": float(np.mean([m["aspect_ratio"] for m in c["members"]])),
                "mean_area_px": float(np.mean([m["area_px"] for m in c["members"]])),
                "mean_ink_ratio": float(np.mean([m["ink_ratio"] for m in c["members"]])),
                "bounding_box_normalized": [0, 0, 1, 1],
                "fingerprint_hash": "",
                "centroid": [0, 0],
            },
            "occurrences": occurrences,
            "cluster_size": c["size"],
            "cluster_density": c["intra_cluster_distance_mean"],
            "confidence": c["confidence"],
            "is_singleton": c["is_singleton"],
        }
        symbols_index.append(symbol)

    # Schreibe Top-Level Symbols Index
    out_index = {
        "schema_version": "2.0",
        "generated_at": "2026-07-04T00:00:00Z",
        "ordering_rule": (
            "Reihenfolge des ersten Auftretens im Fließtext; "
            "Seite 1 oben-links (0,0) nach unten-rechts lesend."
        ),
        "clustering_method": "agglomerative_average_auto_silhouette",
        "clustering_threshold": float(best_t),
        "silhouette_score": float(best_s),
        "n_clusters": n_clusters,
        "n_singletons": singletons,
        "n_multi_member": multi,
        "total_symbols": len(symbols_index),
        "distance_weights": {"embedding": 0.7, "size": 0.15, "aspect": 0.15},
        "symbols": symbols_index,
    }
    (args.out / "symbols_index.json").write_text(
        json.dumps(out_index, indent=2, ensure_ascii=False))
    print(f"Wrote symbols_index.json with {len(symbols_index)} symbols")

    # Schreibe pro-Seite Symbole
    page_to_symbols = defaultdict(list)
    for sym in symbols_index:
        for occ in sym["occurrences"]:
            page_to_symbols[occ["page"]].append({
                "symbol_id": sym["symbol_id"],
                "cluster_id": sym["cluster_id"],
                "page": occ["page"],
                "bbox": occ["bbox"],
                "kind": sym["kind"],
                "first_appearance": (occ["page"] == sym["first_seen_page"]
                                      and occ["bbox"] == sym["first_seen_position"]),
                "vision_description": sym["description"],
                "unicode_codepoint": sym["unicode_codepoint"],
                "vision_confidence": occ.get("vision_confidence", 0.0),
                "crop_path": occ.get("crop_path"),
            })
    for p in range(1, 24):
        page_id = f"p{p:02d}"
        syms = page_to_symbols.get(page_id, [])
        # Sortiere nach (top, left)
        syms.sort(key=lambda s: (s["bbox"][1] if len(s["bbox"]) > 1 else 0,
                                 s["bbox"][0] if len(s["bbox"]) > 0 else 0))
        (args.out / f"{page_id}_symbols.json").write_text(
            json.dumps(syms, indent=2, ensure_ascii=False))
    print(f"Wrote 23 per-page symbol files")

    # Debug: clusters.json
    (args.out / "clusters.json").write_text(
        json.dumps({"clusters": clusters,
                    "clustering_stats": {
                        "best_threshold": best_t,
                        "silhouette": best_s,
                        "threshold_results": threshold_results,
                        "n_clusters": n_clusters,
                        "n_singletons": singletons,
                        "n_multi_member": multi,
                    }},
                   indent=2, ensure_ascii=False))
    print(f"Wrote clusters.json (debug)")


if __name__ == "__main__":
    main()
