#!/usr/bin/env python3
"""
generate_readme_v4.py — Generiert V4-README mit Glyph-Index-Übersicht + Cluster-Statistik.

Input:
  - Tengri137_detailed_<TS>/doc.json
  - bbox/components_<TS>/ (für Glyph-Statistik)
  - bbox/symbols_global_<TS>/ (für Cluster-Statistik)
  - models/symbols_<TS>/eval.json (für ML-Statistik)

Output:
  - Tengri137_README_<TS>.md
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--toplevel", type=Path, required=True,
                    help="Tengri137_detailed_<TS>/")
    ap.add_argument("--components", type=Path, required=True,
                    help="bbox/components_<TS>/")
    ap.add_argument("--symbols-dir", type=Path, default=None,
                    help="bbox/symbols_global_<TS>/")
    ap.add_argument("--model-dir", type=Path, default=None,
                    help="models/symbols_<TS>/")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    doc = json.loads((args.toplevel / "doc.json").read_text())
    document = doc.get("document", {})
    pages = doc.get("pages", [])

    # Glyph-Statistik pro Page
    page_stats = []
    all_glyph_indices = []
    for p in pages:
        page_stats.append({
            "page_id": p["page_id"],
            "n_regions": p.get("n_regions", 0),
            "n_glyphs": p.get("n_glyphs", 0),
            "n_latin_tokens": p.get("n_latin_tokens", 0),
            "schmeh_match": (
                p.get("schmeh_validation", {}).get("n_latin_pages_match", False)),
            "glyph_index_range": None,  # will fill later
        })

    # Lade Glyph-Index-Range pro Page
    for ps in page_stats:
        pid = ps["page_id"]
        glyphs_path = args.components / pid / f"{pid}_glyphs.json"
        if glyphs_path.exists():
            gd = json.loads(glyphs_path.read_text())
            indices = [g["glyph_index"] for g in gd.get("glyphs", [])]
            if indices:
                ps["glyph_index_range"] = (min(indices), max(indices))
                all_glyph_indices.extend(indices)
    if all_glyph_indices:
        glyph_total = max(all_glyph_indices)
    else:
        glyph_total = 0

    # Cluster-Statistik
    cluster_stats = {}
    if args.symbols_dir:
        for level in ("coarse", "medium", "fine"):
            sp = args.symbols_dir / f"level_{level}" / "symbols_index.json"
            if sp.exists():
                sd = json.loads(sp.read_text())
                cluster_stats[level] = {
                    "n_clusters": sd.get("n_clusters", 0),
                    "n_singletons": sd.get("n_singletons", 0),
                    "n_multi_member": sd.get("n_multi_member", 0),
                    "silhouette": sd.get("silhouette_score", 0.0),
                    "threshold": sd.get("clustering_threshold", 0.0),
                }

    # ML-Statistik
    ml_stats = {}
    if args.model_dir:
        eval_path = args.model_dir / "eval.json"
        if eval_path.exists():
            ml_stats = json.loads(eval_path.read_text())

    # Schmeh-Validation
    schmeh_v = document.get("schmeh_validation", {})

    # README generieren
    lines = []
    lines.append("# Tengri137 — V4 Glyph-First Mixed-Media Reconstruction")
    lines.append("")
    lines.append(f"**Generated:** 2026-07-04 (V4 Pipeline)  ")
    lines.append(f"**Schema:** v4.0 (V4 PIVOT: no Tesseract for glyphs)  ")
    lines.append(f"**Source:** Tengri137.pdf (23 pages, unknown geometric script)  ")
    lines.append(f"**Processing run:** {document.get('processing_run', 'unknown')}  ")
    lines.append("")
    lines.append("## V4 Pipeline-Übersicht")
    lines.append("")
    lines.append("```")
    lines.append("Phase 1 v4: Inken-Components + Layout (NO Tesseract)")
    lines.append("Phase 2 v4: Glyph-Gruppierung + Zeilen-Regionen")
    lines.append("Phase 3 v4: Zeilenweiser Vision-Quercheck")
    lines.append("Phase 4 v4: Region-Building mit Glyph-Indexen")
    lines.append("Phase 5 v4: Multi-Resolution-Glyph-Embeddings (16+32+64)")
    lines.append("Phase 6 v4: 3-Level-Glyph-Clustering (coarse/medium/fine)")
    lines.append("Phase 7 v4: Finalisierung mit Glyph-Indexen")
    lines.append("Phase 8 v4: Multi-Resolution-Triplet-Loss (optional)")
    lines.append("```")
    lines.append("")

    lines.append("## Total-Statistik")
    lines.append("")
    totals = document.get("totals", {})
    lines.append(f"- **Pages:** {totals.get('n_pages', 0)}/23")
    lines.append(f"- **Regions:** {totals.get('n_regions', 0)}")
    lines.append(f"- **Glyphs:** {totals.get('n_glyphs', 0)} (max glyph_index={glyph_total})")
    lines.append(f"- **Latin-Tokens:** {totals.get('n_latin_tokens', 0)}")
    lines.append(f"- **Vision-matched glyphs:** {totals.get('n_vision_matched', 0)}")
    lines.append("")

    lines.append("## Glyph-Index-Übersicht pro Page")
    lines.append("")
    lines.append("| Page | Regions | Glyphen | Latin | Glyph-Index-Range | Schmeh ✓ |")
    lines.append("|------|---------|---------|-------|-------------------|----------|")
    for ps in page_stats:
        rng = ps["glyph_index_range"]
        rng_str = f"{rng[0]}–{rng[1]}" if rng else "—"
        match = "✓" if ps["schmeh_match"] else "✗"
        lines.append(
            f"| {ps['page_id']} | {ps['n_regions']} | {ps['n_glyphs']} | "
            f"{ps['n_latin_tokens']} | {rng_str} | {match} |"
        )
    lines.append("")

    if cluster_stats:
        lines.append("## 3-Level-Clustering (Phase 6)")
        lines.append("")
        lines.append("| Level | Threshold | Silhouette | Cluster | Singletons | Multi-Member |")
        lines.append("|-------|-----------|------------|---------|------------|--------------|")
        for level, cs in cluster_stats.items():
            lines.append(
                f"| {level} | {cs['threshold']:.3f} | {cs['silhouette']:.3f} | "
                f"{cs['n_clusters']} | {cs['n_singletons']} | {cs['n_multi_member']} |"
            )
        lines.append("")

    if ml_stats:
        lines.append("## ML-Model (Phase 8 — optional)")
        lines.append("")
        lines.append("```json")
        lines.append(json.dumps(ml_stats, indent=2, ensure_ascii=False))
        lines.append("```")
        lines.append("")

    lines.append("## Schmeh-Validation (HINT, NOT truth)")
    lines.append("")
    lines.append(f"- **Glyph-Pages match:** {schmeh_v.get('n_glyph_pages_match', 0)}/23")
    lines.append(f"- **Latin-Pages match:** {schmeh_v.get('n_latin_pages_match', 0)}/23")
    lines.append(f"- **Pages with known issues:** {schmeh_v.get('n_pages_with_known_issues', 0)}/23")
    if schmeh_v.get("known_issues"):
        lines.append("")
        lines.append("### Known Issues (Schmeh vs V4):")
        lines.append("")
        for iss in schmeh_v["known_issues"][:30]:
            lines.append(f"- {iss}")
    lines.append("")

    lines.append("## V4 PIVOT von V3 — Was ist anders?")
    lines.append("")
    lines.append("| Aspekt | V3 (alt) | V4 (neu) |")
    lines.append("|--------|----------|----------|")
    lines.append("| **Tesseract für Glyphen** | ja (mit Müll) | **NEIN** |")
    lines.append("| **Glyph-Identifikation** | text_word (Tesseract) | **glyph_index (1-basiert, global)** |")
    lines.append("| **Glyph-Struktur** | symbol_instance | **glyph_instance + components[]** |")
    lines.append("| **Embeddings** | 64-dim (V2) | **192-dim (16+32+64)** |")
    lines.append("| **Clustering** | 1 Level | **3 Levels (coarse/medium/fine)** |")
    lines.append("| **Layout-Analyse** | nur via OCR | **via DBSCAN auf Centroiden** |")
    lines.append("| **Schmeh-Validation** | keine | **V4-Output vs Schmeh-Hint (HINT)** |")
    lines.append("")

    lines.append("## Reproduzierbarkeit")
    lines.append("")
    lines.append(f"- **Time-Stamp:** {document.get('processing_run', 'unknown')}")
    lines.append("- **Schema:** `schemas/tengri137_document_v4.schema.json`")
    lines.append("- **Pipeline-Scripts:** `phase1_pixel_v4.py` bis `phase7_finalize.py`")
    lines.append("- **V1/V2/V3 unangetastet** (Reproduzierbarkeits-Regel)")
    lines.append("- **Schmeh raw_text.txt als HINT, nicht Wahrheit**")
    lines.append("")

    args.out.write_text("\n".join(lines))
    print(f"Wrote {args.out} ({len(lines)} lines)")


if __name__ == "__main__":
    main()
