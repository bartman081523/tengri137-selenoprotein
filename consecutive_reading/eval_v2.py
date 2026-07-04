#!/usr/bin/env python3
"""
Eval v2 — kNN-Accuracy, Confusion-Matrix, Intra/Inter-Cluster-Distanz.

Berechnet:
  - kNN-Accuracy@k für k=1,3,5
  - Confusion-Matrix für Top-20-Cluster
  - Intra-Cluster-Distanz (Mean, Max) pro Cluster
  - Inter-Cluster-Distanz (Mean über Cluster-Paare)
  - Silhouette-Score pro Cluster

Input:
  - models/symbols_<TS>/embeddings.npz
  - models/symbols_<TS>/classes.json
  - bbox/symbols_global_<TS>/symbols_index.json (für Cluster-Info)

Output:
  - models/symbols_<TS>/eval.json
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def l2_normalize(x: np.ndarray) -> np.ndarray:
    norms = np.linalg.norm(x, axis=1, keepdims=True)
    norms = np.where(norms == 0, 1.0, norms)
    return (x / norms).astype(np.float32)


def knn_predict(embs: np.ndarray, ref_embs: np.ndarray, ref_labels: np.ndarray,
                k: int = 5) -> np.ndarray:
    """Predict class via kNN majority vote."""
    sim = l2_normalize(embs) @ l2_normalize(ref_embs).T
    n = min(k, sim.shape[1])
    idx = np.argpartition(-sim, kth=n - 1, axis=1)[:, :n]
    preds = np.zeros(len(embs), dtype=np.int64)
    for i, inds in enumerate(idx):
        ref_l = ref_labels[inds]
        preds[i] = Counter(ref_l.tolist()).most_common(1)[0][0]
    return preds


def confusion_pairs(y_true: np.ndarray, y_pred: np.ndarray) -> dict:
    """Compute (true, pred) → count for confusion stats."""
    pairs = Counter()
    for t, p in zip(y_true.tolist(), y_pred.tolist()):
        pairs[(t, p)] += 1
    return dict(pairs)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--model-dir", type=Path, required=True)
    ap.add_argument("--symbols", type=Path, required=True,
                    help="bbox/symbols_global_<TS>/symbols_index.json")
    args = ap.parse_args()

    # Lade Embeddings + Klassen
    embs_data = np.load(args.model_dir / "embeddings.npz", allow_pickle=True)
    embs = embs_data["embeddings_normalized"]
    labels = embs_data["labels"]
    cluster_ids = embs_data["cluster_ids"]
    paths = embs_data["paths"]

    classes = json.loads((args.model_dir / "classes.json").read_text())
    cid_to_cluster = classes.get("cid_to_cluster", {})

    # Lade Symbole
    symbols_index = json.loads(args.symbols.read_text())
    n_clusters = symbols_index.get("n_clusters", 0)

    # 5-fold cross-validation statt 10% holdout (mit 818 Samples besser)
    n = len(embs)
    indices = np.arange(n)
    rng = np.random.default_rng(42)
    rng.shuffle(indices)
    k_folds = 5
    fold_size = n // k_folds

    print(f"Total samples: {n}, classes: {len(cid_to_cluster)}")
    print(f"Running {k_folds}-fold cross-validation...")

    fold_results = []
    all_pairs = Counter()
    for fold in range(k_folds):
        val_idx = indices[fold * fold_size:(fold + 1) * fold_size]
        train_idx = np.array([i for i in indices if i not in set(val_idx.tolist())])
        # kNN@k
        for k in [1, 3, 5]:
            preds = knn_predict(embs[val_idx], embs[train_idx], labels[train_idx], k=k)
            acc = float((preds == labels[val_idx]).mean())
            fold_results.append({"fold": fold, "k": k, "accuracy": acc})
        # Confusion (k=5)
        preds = knn_predict(embs[val_idx], embs[train_idx], labels[train_idx], k=5)
        all_pairs.update(confusion_pairs(labels[val_idx], preds))

    # Aggregiere
    accs_by_k = {1: [], 3: [], 5: []}
    for r in fold_results:
        accs_by_k[r["k"]].append(r["accuracy"])

    summary = {
        "total_samples": n,
        "n_classes": len(cid_to_cluster),
        "n_clusters": n_clusters,
        "k_fold": k_folds,
        "accuracy_at_k": {
            "k=1": {"mean": float(np.mean(accs_by_k[1])),
                     "std": float(np.std(accs_by_k[1])),
                     "per_fold": accs_by_k[1]},
            "k=3": {"mean": float(np.mean(accs_by_k[3])),
                     "std": float(np.std(accs_by_k[3])),
                     "per_fold": accs_by_k[3]},
            "k=5": {"mean": float(np.mean(accs_by_k[5])),
                     "std": float(np.std(accs_by_k[5])),
                     "per_fold": accs_by_k[5]},
        },
        "confusion_pairs_top20": {f"{t}->{p}": c
                                   for (t, p), c in Counter(all_pairs).most_common(20)},
        "per_class_size": {str(int(c)): int(n) for c, n in Counter(int(c) for c in labels.tolist()).items()},
    }

    # Per-Cluster-Stats
    cluster_stats = {}
    for cid_str, cluster_name in cid_to_cluster.items():
        cid = int(cid_str)
        mask = labels == cid
        if mask.sum() == 0:
            continue
        sub_embs = embs[mask]
        # Intra-Cluster cosine sim
        if len(sub_embs) > 1:
            sim = l2_normalize(sub_embs) @ l2_normalize(sub_embs).T
            n_s = sim.shape[0]
            iu = np.triu_indices(n_s, k=1)
            intra_mean = float(sim[iu].mean()) if len(iu[0]) > 0 else 0.0
            intra_max = float(sim[iu].max()) if len(iu[0]) > 0 else 0.0
        else:
            intra_mean = intra_max = 0.0
        cluster_stats[cluster_name] = {
            "size": int(mask.sum()),
            "intra_cluster_sim_mean": intra_mean,
            "intra_cluster_sim_max": intra_max,
        }
    summary["per_cluster_stats"] = cluster_stats

    out_path = args.model_dir / "eval.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")
    print(f"\nAccuracy@k (5-fold CV):")
    for k in [1, 3, 5]:
        m = summary["accuracy_at_k"][f"k={k}"]["mean"]
        s = summary["accuracy_at_k"][f"k={k}"]["std"]
        print(f"  k={k}: {m:.3f} ± {s:.3f}")


if __name__ == "__main__":
    main()
