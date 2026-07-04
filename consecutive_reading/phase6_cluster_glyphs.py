#!/usr/bin/env python3
"""
Phase 6 v4 — 3-Level Glyph-Clustering.

Input:
  - bbox/embeddings_20260704_V4/crop_embeddings.npz  (Phase 5: 192-dim)
  - bbox/vision_qa_20260704_V4/p{NN}/p{NN}_line_*.json  (Phase 3: vision)

Output:
  - bbox/symbols_global_20260704_V4/level_{coarse,medium,fine}/symbols_index.json
  - bbox/symbols_global_20260704_V4/level_{coarse,medium,fine}/clusters.json
  - bbox/symbols_global_20260704_V4/cluster_hierarchy.json
  - bbox/symbols_global_20260704_V4/level_medium/p{NN}_glyphs.json

Algorithmus:
1. Multi-Modal-Distanz (V2-erbt):
   - 0.7 × Cosine-Distanz (192-dim)
   - 0.15 × Size-Distanz
   - 0.15 × Aspect-Distanz
2. Auto-Silhouette (V2-erbt)
3. Agglomeratives Clustering (3 Levels mit verschiedenen Thresholds):
   - Coarse: t=0.40 (5-10 Cluster)
   - Medium: t=0.20 (15-30 Cluster) — Standard-Level
   - Fine:   t=0.10 (50-100 Cluster)
4. Vision-Label pro Cluster (V2-Logik)
5. Cross-Level-Hierarchie
6. Singletons bekommen kind: "singleton"
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


def multi_modal_distance(embs, areas, aspects, weights=(0.2, 0.5, 0.3)):
    """Kombinierte Distanz-Matrix.

    V4-Gewichtung: V2-EmbeddingNet (V4-Warm-Start) liefert extrem enge Cosine-Distanzen
    (alle Glyphen ~identisch im Winkel), daher Size+Aspect stärker gewichten:
    - 0.2 × Cosine-Distanz (192-dim)
    - 0.5 × Size-Distanz (log-Area)
    - 0.3 × Aspect-Distanz (log-Ratio)
    """
    w_emb, w_size, w_aspect = weights
    sim = embs @ embs.T
    emb_dist = np.clip(1.0 - sim, 0.0, 2.0).astype(np.float32)
    log_areas = np.log(np.maximum(areas, 1.0))
    size_diff = np.abs(log_areas[:, None] - log_areas[None, :])
    size_dist = np.clip(size_diff / 3.0, 0.0, 1.0).astype(np.float32)
    log_aspects = np.log(np.maximum(aspects, 0.01))
    aspect_diff = np.abs(log_aspects[:, None] - log_aspects[None, :])
    aspect_dist = np.clip(aspect_diff / 1.5, 0.0, 1.0).astype(np.float32)
    combined = (w_emb * emb_dist + w_size * size_dist + w_aspect * aspect_dist).astype(np.float32)
    return combined


def silhouette_score_subsample(D, labels, n_sample=200, rng=None):
    """Silhouette-Score auf Subsample (numpy-only)."""
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


def find_best_threshold(D, level="medium"):
    """Auto-Silhouette: teste Thresholds passend zum Level.

    V4-Schwellen: Da Multi-Modal-Distanz (V4-Gewichtung 0.2/0.5/0.3) höhere Werte
    liefert (mean=0.5), brauchen wir höhere Schwellen als V2.
    """
    if level == "coarse":
        thresholds = (0.45, 0.50, 0.55, 0.60, 0.65)
    elif level == "medium":
        thresholds = (0.25, 0.30, 0.35, 0.40, 0.45)
    else:  # fine
        thresholds = (0.10, 0.15, 0.18, 0.20, 0.25)
    condensed = squareform(D, checks=False)
    Z = linkage(condensed, method="average")
    best_t, best_s, best_labels = thresholds[0], -1.0, None
    for t in thresholds:
        labels = fcluster(Z, t=t, criterion="distance")
        n_clusters = len(set(labels))
        if n_clusters < 2 or n_clusters > len(labels) - 1:
            continue
        s = silhouette_score_subsample(D, labels)
        if s > best_s:
            best_s = s
            best_t = t
            best_labels = labels
    if best_labels is None:
        best_t = thresholds[0]
        best_labels = fcluster(Z, t=best_t, criterion="distance")
    return best_t, best_s, best_labels


def medoid(embs, indices):
    sub = embs[indices]
    D = squareform(pdist(sub, metric="cosine"), checks=False)
    mean_d = D.mean(axis=1)
    return indices[int(np.argmin(mean_d))]


def build_cluster(vision_data, embs, labels, areas, aspects, glyph_index, page_id_arr,
                  bbox_arr, size_px_arr, fill_ratio_arr, n_components_arr,
                  type_hint_arr, level="medium"):
    """Baut Cluster-Objekte aus Labels."""
    cluster_members = defaultdict(list)
    for i, lab in enumerate(labels):
        cluster_members[int(lab)].append(i)
    clusters = []
    for cid, members_idx in sorted(cluster_members.items()):
        members = []
        kinds = []
        for i in members_idx:
            gid = int(glyph_index[i])
            v = vision_data.get(gid, {})
            if v.get("kind"):
                kinds.append((v["kind"], v.get("confidence", 0.0)))
            members.append({
                "glyph_index": gid,
                "page": str(page_id_arr[i]),
                "bbox": bbox_arr[i].tolist(),
                "size_px": int(size_px_arr[i]),
                "fill_ratio": float(fill_ratio_arr[i]),
                "n_components": int(n_components_arr[i]),
                "type_hint": str(type_hint_arr[i]),
                "vision_kind": v.get("kind"),
                "vision_description": v.get("description", ""),
                "vision_confidence": v.get("confidence", 0.0),
            })
        # Medoid
        medoid_idx = medoid(embs, members_idx)
        medoid_pos = members_idx.index(medoid_idx)
        # Intra-cluster
        sub = embs[members_idx]
        if len(members_idx) > 1:
            D_sub = pdist(sub, metric="cosine")
            intra_mean = float(D_sub.mean())
            intra_max = float(D_sub.max())
        else:
            intra_mean = 0.0
            intra_max = 0.0
        # Label
        if kinds:
            best = max(kinds, key=lambda x: x[1])
            counter = Counter(k[0] for k in kinds)
            majority_kind, majority_count = counter.most_common(1)[0]
            has_high_conf = any(c >= 0.7 for _, c in kinds)
            if has_high_conf or majority_count > 1:
                chosen = best[0] if has_high_conf else majority_kind
            else:
                chosen = best[0]
        else:
            chosen = "singleton" if len(members_idx) == 1 else "unknown"
        # Cluster-ID
        kind_safe = re.sub(r"[^A-Z0-9_]", "_", chosen.upper())[:20] or "UNKNOWN"
        cluster_id = f"GEOM_{level.upper()}_{kind_safe}_{cid:04d}"
        cluster_obj = {
            "cluster_id": cluster_id,
            "kind": chosen,
            "label_source": "vision_line" if kinds else "no_vision",
            "size": len(members_idx),
            "is_singleton": len(members_idx) == 1,
            "intra_cluster_distance_mean": intra_mean,
            "intra_cluster_distance_max": intra_max,
            "members": members,
            "representative_glyph_index": int(glyph_index[medoid_idx]),
        }
        clusters.append(cluster_obj)
    return clusters


def load_vision_data(vision_dir: Path) -> dict:
    """Lade Vision-Daten aus Phase 3 line-level outputs.
    Returns: {glyph_index: {kind, description, confidence, ...}}"""
    vision = {}
    if not vision_dir or not vision_dir.exists():
        return vision
    for page_dir in sorted(vision_dir.glob("p*")):
        if not page_dir.is_dir():
            continue
        page_id = page_dir.name
        # Pattern: p01_line01.json (zweistellig) ODER p01_line_01.json
        for lf in sorted(list(page_dir.glob(f"{page_id}_line*.json"))):
            # Skip p01_page.json
            if "_page" in lf.name:
                continue
            try:
                d = json.loads(lf.read_text())
            except json.JSONDecodeError:
                continue
            for m in d.get("matched_glyphs", []):
                vg = m.get("vision_glyph", {})
                gi = m.get("matched_glyph_index")
                if gi is not None and vg:
                    vision[int(gi)] = {
                        "kind": vg.get("visual_kind", ""),
                        "description": vg.get("description", ""),
                        "confidence": vg.get("confidence", 0.0),
                        "unicode_codepoint": vg.get("unicode_codepoint_candidate", ""),
                    }
    return vision


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--embeddings", type=Path, required=True,
                    help="bbox/embeddings_<TS>/crop_embeddings.npz")
    ap.add_argument("--vision", type=Path, default=None,
                    help="bbox/vision_qa_<TS>/")
    ap.add_argument("--out-dir", type=Path, required=True,
                    help="bbox/symbols_global_<TS>/")
    args = ap.parse_args()

    out_dir = args.out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    for level in ("coarse", "medium", "fine"):
        (out_dir / f"level_{level}").mkdir(parents=True, exist_ok=True)

    # Load embeddings
    data = np.load(args.embeddings, allow_pickle=True)
    embs = data["embeddings"].astype(np.float32)
    glyph_index = data["glyph_index"]
    page_id_arr = data["page_id"]
    bbox_arr = data["bbox"]
    size_px_arr = data["size_px"]
    fill_ratio_arr = data["fill_ratio"]
    n_components_arr = data["n_components"]
    type_hint_arr = data["type_hint"]
    n = len(glyph_index)
    print(f"Loaded {n} embeddings, dim={embs.shape[1]}")

    # Areas + Aspects
    # bbox_arr ist Liste von [x0, y0, w, h]
    areas = np.array([b[2] * b[3] for b in bbox_arr], dtype=np.float32)
    aspects = np.array([b[2] / max(1, b[3]) for b in bbox_arr], dtype=np.float32)

    # Vision data
    vision_data = load_vision_data(args.vision)
    print(f"Loaded {len(vision_data)} vision-glyph entries")

    # Distance matrix
    D = multi_modal_distance(embs, areas, aspects)
    print(f"Distance matrix: {D.shape}, mean={D.mean():.3f}, max={D.max():.3f}")

    # 3-Level Clustering
    hierarchy = {}
    all_clusters = {}
    for level in ("coarse", "medium", "fine"):
        print(f"\n=== {level.upper()} Level ===")
        best_t, best_s, labels = find_best_threshold(D, level=level)
        n_clusters = len(set(labels))
        singletons = sum(1 for lab in set(labels) if (labels == lab).sum() == 1)
        multi = n_clusters - singletons
        print(f"  t={best_t}, silhouette={best_s:.3f}, n_clusters={n_clusters}, "
              f"singletons={singletons}, multi={multi}")
        clusters = build_cluster(
            vision_data, embs, labels, areas, aspects,
            glyph_index, page_id_arr, bbox_arr, size_px_arr, fill_ratio_arr,
            n_components_arr, type_hint_arr, level=level,
        )
        # Sort by size desc
        clusters.sort(key=lambda c: (-c["size"], c["representative_glyph_index"]))
        # Write clusters.json
        (out_dir / f"level_{level}" / "clusters.json").write_text(
            json.dumps({"clusters": clusters,
                        "clustering_stats": {
                            "level": level,
                            "best_threshold": best_t,
                            "silhouette": best_s,
                            "n_clusters": n_clusters,
                            "n_singletons": singletons,
                            "n_multi_member": multi,
                        }}, indent=2, ensure_ascii=False))
        # Build symbols_index.json
        symbols_index = []
        for sym_id, c in enumerate(clusters, start=1):
            # Sort members by reading order
            sorted_members = sorted(c["members"],
                                    key=lambda m: (m["page"],
                                                   m["bbox"][1] if len(m["bbox"]) > 1 else 0,
                                                   m["bbox"][0] if len(m["bbox"]) > 0 else 0))
            first = sorted_members[0]
            sym = {
                "symbol_id": sym_id,
                "cluster_id": c["cluster_id"],
                "kind": c["kind"],
                "label_source": c["label_source"],
                "size": c["size"],
                "is_singleton": c["is_singleton"],
                "intra_cluster_distance_mean": c["intra_cluster_distance_mean"],
                "first_seen_page": first["page"],
                "first_seen_glyph_index": first["glyph_index"],
                "first_seen_bbox": first["bbox"],
                "representative_glyph_index": c["representative_glyph_index"],
                "members": c["members"],
                "level": level,
            }
            symbols_index.append(sym)
        (out_dir / f"level_{level}" / "symbols_index.json").write_text(
            json.dumps({
                "schema_version": "4.0",
                "level": level,
                "clustering_threshold": best_t,
                "silhouette_score": best_s,
                "n_clusters": n_clusters,
                "n_singletons": singletons,
                "n_multi_member": multi,
                "total_glyphs": n,
                "symbols": symbols_index,
            }, indent=2, ensure_ascii=False))
        all_clusters[level] = {c["cluster_id"]: c for c in clusters}
        print(f"  Wrote level_{level}/symbols_index.json ({len(symbols_index)} symbols)")

    # Cross-Level-Hierarchie: finde parent_cluster für jedes Medium-Cluster
    # (Coarse cluster whose members overlap most with this Medium cluster)
    print("\n=== Building cluster hierarchy ===")
    coarse_to_members = defaultdict(set)
    for cid, c in all_clusters["coarse"].items():
        for m in c["members"]:
            coarse_to_members[cid].add(m["glyph_index"])
    medium_parents = {}
    for m_cid, m_cluster in all_clusters["medium"].items():
        m_members = {m["glyph_index"] for m in m_cluster["members"]}
        best_parent = None
        best_overlap = 0
        for c_cid, c_members in coarse_to_members.items():
            overlap = len(m_members & c_members)
            if overlap > best_overlap:
                best_overlap = overlap
                best_parent = c_cid
        medium_parents[m_cid] = {
            "parent_cluster_id": best_parent,
            "overlap_count": best_overlap,
            "overlap_ratio": best_overlap / max(1, len(m_members)),
        }
    fine_parents = {}
    for f_cid, f_cluster in all_clusters["fine"].items():
        f_members = {m["glyph_index"] for m in f_cluster["members"]}
        best_parent = None
        best_overlap = 0
        for m_cid, m_cluster in all_clusters["medium"].items():
            m_members = {m["glyph_index"] for m in m_cluster["members"]}
            overlap = len(f_members & m_members)
            if overlap > best_overlap:
                best_overlap = overlap
                best_parent = m_cid
        fine_parents[f_cid] = {
            "parent_cluster_id": best_parent,
            "overlap_count": best_overlap,
            "overlap_ratio": best_overlap / max(1, len(f_members)),
        }
    hierarchy = {
        "medium_parents": medium_parents,
        "fine_parents": fine_parents,
    }
    (out_dir / "cluster_hierarchy.json").write_text(
        json.dumps(hierarchy, indent=2, ensure_ascii=False))
    print("Wrote cluster_hierarchy.json")

    # Pro-Seite Glyph-Liste (Medium Level) - für Phase 4 lookup
    page_to_glyphs = defaultdict(list)
    for c in all_clusters["medium"].values():
        for m in c["members"]:
            page_to_glyphs[m["page"]].append({
                "glyph_index": m["glyph_index"],
                "cluster_id": c["cluster_id"],
                "kind": c["kind"],
                "first_appearance": m["glyph_index"] == c["representative_glyph_index"],
                "page": m["page"],
                "bbox": m["bbox"],
            })
    for p in range(1, 24):
        page_id = f"p{p:02d}"
        gs = page_to_glyphs.get(page_id, [])
        gs.sort(key=lambda g: (g["bbox"][1] if len(g["bbox"]) > 1 else 0,
                               g["bbox"][0] if len(g["bbox"]) > 0 else 0))
        (out_dir / "level_medium" / f"{page_id}_glyphs.json").write_text(
            json.dumps(gs, indent=2, ensure_ascii=False))
    print("Wrote 23 per-page glyph files (level_medium)")


if __name__ == "__main__":
    main()
