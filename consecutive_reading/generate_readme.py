#!/usr/bin/env python3
"""
Generate README v2 — Übersichtsdokumentation des V2-Pipeline-Laufs.

Input:
  - Tengri137_detailed_<TS>/doc.json
  - bbox/symbols_global_<TS>/symbols_index.json
  - models/symbols_<TS>/eval.json

Output:
  - Tengri137_README_<TS>.md
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def fmt(x, default="—"):
    if x is None:
        return default
    if isinstance(x, float):
        return f"{x:.3f}"
    return str(x)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--doc", type=Path, required=True,
                    help="Tengri137_detailed_<TS>/doc.json")
    ap.add_argument("--symbols", type=Path, required=True)
    ap.add_argument("--eval", type=Path, default=None,
                    help="models/symbols_<TS>/eval.json (optional)")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    doc = json.loads(args.doc.read_text())
    symbols = json.loads(args.symbols.read_text())
    eval_data = None
    if args.eval and args.eval.exists():
        eval_data = json.loads(args.eval.read_text())

    md = []
    md.append("# Tengri137 — V2 Detailed Analysis\n")
    md.append(f"**Pipeline:** Embedding-Clustering + Triplet-Loss ML + Auto-Silhouette\n")
    md.append(f"**Processing Run:** `{doc['document']['processing_run']}`\n")
    md.append(f"**Pipeline Version:** {doc['document'].get('pipeline_version', '—')}\n")
    md.append(f"**Generated:** {doc['document'].get('generated_at', '—')}\n")
    md.append("\n---\n\n")

    # Document-Info
    md.append("## Document\n\n")
    md.append(f"- **Title:** {doc['document'].get('title', '—')}\n")
    md.append(f"- **Page Count:** {doc['document'].get('page_count', 0)}\n")
    md.append(f"- **Source PDF:** `{doc['document'].get('source_pdf', '—')}`\n")
    md.append(f"- **Description:** {doc['document'].get('description', '—')}\n")
    md.append("\n")

    # Clustering-Übersicht
    md.append("## Clustering\n\n")
    md.append(f"- **Method:** {symbols.get('clustering_method', '—')}\n")
    md.append(f"- **Threshold (t):** {fmt(symbols.get('clustering_threshold'))}\n")
    md.append(f"- **Silhouette Score:** {fmt(symbols.get('silhouette_score'))}\n")
    md.append(f"- **Total Symbols:** {fmt(symbols.get('total_symbols', 0))}\n")
    md.append(f"- **N Clusters:** {fmt(symbols.get('n_clusters', 0))}\n")
    md.append(f"- **N Singletons:** {fmt(symbols.get('n_singletons', 0))}\n")
    md.append(f"- **N Multi-member:** {fmt(symbols.get('n_multi_member', 0))}\n")
    md.append(f"- **Distance Weights:** {symbols.get('distance_weights', '—')}\n")
    md.append(f"- **Ordering:** {symbols.get('ordering_rule', '—')}\n")
    md.append("\n")

    # Eval-Results
    if eval_data:
        md.append("## ML-Eval (5-fold Cross-Validation)\n\n")
        md.append("| k | Accuracy (mean ± std) |\n|---|---|\n")
        for k_str in ["k=1", "k=3", "k=5"]:
            d = eval_data["accuracy_at_k"].get(k_str, {})
            m = fmt(d.get("mean"))
            s = fmt(d.get("std"))
            md.append(f"| {k_str} | {m} ± {s} |\n")
        md.append(f"\n- **Total Samples:** {eval_data.get('total_samples', 0)}\n")
        md.append(f"- **N Classes:** {eval_data.get('n_classes', 0)}\n")
        md.append(f"- **N Clusters (post-clustering):** {eval_data.get('n_clusters', 0)}\n")
        md.append("\n")

    # Top-Cluster mit Vorkommen (aus Pages aggregiert, nicht aus Index)
    md.append("## Top-20 Häufigste Symbole (nach Occurrences, aggregiert über alle Pages)\n\n")
    cluster_counter = Counter()
    cluster_meta = {}  # cluster_id → {vision_kind, description, vision_confidence}
    for page in doc.get("pages", []):
        for region in page.get("regions", []):
            for s in region.get("symbols", []):
                cid = s.get("cluster_id", "GEOM_UNMATCHED_0000")
                cluster_counter[cid] += 1
                if cid not in cluster_meta and s.get("vision_kind") and s["vision_kind"] != "unknown":
                    cluster_meta[cid] = {
                        "vision_kind": s.get("vision_kind", "—"),
                        "description": (s.get("vision_description") or "—")[:60],
                        "first_page": page.get("page_id", "?"),
                    }
    md.append("| Cluster | Vorkommen | Vision-Kind | Description | Erste Seite |\n")
    md.append("|---|---|---|---|---|\n")
    for cid, n in cluster_counter.most_common(20):
        meta = cluster_meta.get(cid, {"vision_kind": "—", "description": "—",
                                       "first_page": "—"})
        desc = meta["description"].replace("|", "/")
        md.append(f"| `{cid}` | {n} | {meta['vision_kind']} | {desc} | {meta['first_page']} |\n")
    md.append("\n")

    # Pages-Übersicht
    md.append("## Page-Übersicht\n\n")
    md.append("| Page | Regions | Symbole | Wörter | Klassifikationen (Top-3) |\n")
    md.append("|---|---|---|---|---|\n")
    for page in doc.get("pages", []):
        stats = page.get("stats", {})
        cls_top = ", ".join(f"{k}={v}" for k, v in
                            list(stats.get("classifications", {}).items())[:3])
        md.append(f"| {page.get('page_id', '?')} "
                  f"| {stats.get('n_regions', 0)} "
                  f"| {stats.get('n_symbols', 0)} "
                  f"| {stats.get('n_text_words', 0)} "
                  f"| {cls_top} |\n")
    md.append("\n")

    # Region-Classificationen global
    md.append("## Region-Klassifikationen (global)\n\n")
    all_cls = Counter()
    for page in doc.get("pages", []):
        for cls, n in page.get("stats", {}).get("classifications", {}).items():
            all_cls[cls] += n
    md.append("| Classification | Count |\n|---|---|\n")
    for cls, n in all_cls.most_common():
        md.append(f"| {cls} | {n} |\n")
    md.append("\n")

    # Vision-Descriptions pro Page
    md.append("## Vision-Beschreibungen (Page-Level)\n\n")
    for page in doc.get("pages", []):
        vdesc = page.get("vision_description", "")
        vcls = page.get("vision_classification", "")
        if vdesc or vcls:
            md.append(f"### {page.get('page_id', '?')}\n\n")
            if vcls:
                md.append(f"**Classification:** {vcls}\n\n")
            if vdesc:
                md.append(f"> {vdesc[:300]}{'...' if len(vdesc) > 300 else ''}\n\n")

    # Unklare Bereiche
    md.append("## Unklare Bereiche (`uncertain[]`)\n\n")
    unc_total = 0
    for page in doc.get("pages", []):
        for r in page.get("regions", []):
            for u in r.get("uncertain", []):
                md.append(f"- **{page.get('page_id', '?')}/{r.get('region_id', '?')}:** {u}\n")
                unc_total += 1
    if unc_total == 0:
        md.append("_(Keine unsicheren Bereiche gemeldet)_\n")
    md.append("\n")

    # Reproduzierbarkeits-Hinweis
    md.append("## Reproduzierbarkeit\n\n")
    md.append("Alle Outputs sind mit Zeitstempel-Ordnern organisiert; "
              "vorherige Läufe bleiben unangetastet (siehe CLAUDE.md).\n\n")
    md.append("### Re-Run der kompletten Pipeline\n\n")
    md.append("```bash\n")
    md.append("TS=20260704_V2\n\n")
    md.append("# Phase 1 (idempotent)\n")
    md.append("python3 phase1_pixel.py --out bbox/pages_pixel_$TS\n\n")
    md.append("# Phase 2 v2 — Vision-Fix + alle 818 Crops\n")
    md.append("python3 phase2_vision_v2.py \\\n")
    md.append("  --pixel bbox/pages_pixel_$TS \\\n")
    md.append("  --schemas bbox/schemas_20260704_075228/ \\\n")
    md.append("  --out bbox/vision_qa_$TS --workers 4 --n-top-glyphs 999\n\n")
    md.append("# Phase 3 v2 — regions-Struktur\n")
    md.append("python3 phase3_merge_v2.py \\\n")
    md.append("  --pixel bbox/pages_pixel_$TS \\\n")
    md.append("  --vision bbox/vision_qa_$TS \\\n")
    md.append("  --out bbox/pages_merged_$TS\n\n")
    md.append("# Phase 4a — Embedding\n")
    md.append("python3 phase4a_embed_crops.py \\\n")
    md.append("  --crops bbox/crops \\\n")
    md.append("  --model models/symbols_20260704_075228/model.pt \\\n")
    md.append("  --out bbox/embeddings_$TS\n\n")
    md.append("# Phase 4b — Auto-Silhouette Clustering\n")
    md.append("python3 phase4b_cluster_symbols.py \\\n")
    md.append("  --embeddings bbox/embeddings_$TS \\\n")
    md.append("  --vision bbox/vision_qa_$TS \\\n")
    md.append("  --out bbox/symbols_global_$TS\n\n")
    md.append("# Phase 5 v2 — Schema-Validation + Final\n")
    md.append("python3 phase5_finalize_v2.py \\\n")
    md.append("  --pages bbox/pages_merged_$TS \\\n")
    md.append("  --symbols bbox/symbols_global_$TS/symbols_index.json \\\n")
    md.append("  --schema schemas/tengri137_document.schema.json \\\n")
    md.append("  --out bbox/final_$TS \\\n")
    md.append("  --toplevel Tengri137_detailed_$TS \\\n")
    md.append("  --processing-run $TS\n\n")
    md.append("# Phase 6 v2 — Triplet-Loss + Augmentations\n")
    md.append("python3 phase6_train_v2.py \\\n")
    md.append("  --embeddings bbox/embeddings_$TS \\\n")
    md.append("  --symbols bbox/symbols_global_$TS/symbols_index.json \\\n")
    md.append("  --crops bbox/crops \\\n")
    md.append("  --init-model models/symbols_20260704_075228/model.pt \\\n")
    md.append("  --out models/symbols_$TS \\\n")
    md.append("  --epochs 30 --bs 32\n\n")
    md.append("# Eval + Inference\n")
    md.append("python3 eval_v2.py --model-dir models/symbols_$TS \\\n")
    md.append("  --symbols bbox/symbols_global_$TS/symbols_index.json\n\n")
    md.append("python3 models/symbols_$TS/inference.py \\\n")
    md.append("  --model-dir models/symbols_$TS \\\n")
    md.append("  --crops bbox/crops/p01_blank_000.png\n\n")
    md.append("# README regenerieren\n")
    md.append("python3 generate_readme.py \\\n")
    md.append("  --doc Tengri137_detailed_$TS/doc.json \\\n")
    md.append("  --symbols bbox/symbols_global_$TS/symbols_index.json \\\n")
    md.append("  --eval models/symbols_$TS/eval.json \\\n")
    md.append("  --out Tengri137_README_$TS.md\n")
    md.append("```\n\n")

    md.append("## Inference-Usage\n\n")
    md.append("Predict cluster_id for new crops:\n\n")
    md.append("```bash\n")
    md.append("python3 models/symbols_20260704_V2/inference.py \\\n")
    md.append("  --model-dir models/symbols_20260704_V2 \\\n")
    md.append("  --crops bbox/crops/p01_blank_000.png\n")
    md.append("```\n\n")
    md.append("Output: `cluster_id`, Top-3 mit Wahrscheinlichkeiten, `uncertain`-Flag.\n\n")

    md.append("---\n\n")
    md.append("**V2-Pipeline-Status:** ✓ Reproducible. Alle Outputs mit Zeitstempel-Ordner, "
              "frühere Läufe (TS=20260704_075228) bleiben unangetastet.\n")

    args.out.write_text("".join(md))
    print(f"Wrote {args.out} ({sum(len(l) for l in md)} chars)")


if __name__ == "__main__":
    main()
