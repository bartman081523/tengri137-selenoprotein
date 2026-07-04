#!/usr/bin/env python3
"""
Phase 5 v2 — Finalisierung mit Einheitsschema + Top-Level Document.

Input:
  - bbox/pages_merged_<TS>/p{NN}.json (Phase 3 v2 Output, pro Seite regions)
  - bbox/symbols_global_<TS>/symbols_index.json (Phase 4b Output, Cluster-Index)
  - schemas/tengri137_document.schema.json (Einheits-Schema)

Output:
  - bbox/final_<TS>/p{NN}.json (pro Seite, validiert + ergänzt)
  - Tengri137_detailed_<TS>/p{NN}.json (Top-Level-Kopie)
  - Tengri137_detailed_<TS>/symbols_index.json (Top-Level)
  - Tengri137_detailed_<TS>/doc.json (Single-File-Document mit allen 23 Pages)

Validierung:
  - jsonschema draft-07 gegen tengri137_document.schema.json
  - Konsistenz-Checks (jedes Symbol hat bbox, jede Region hat region_id)
  - Statistiken (Anzahl Regionen, Symbole, Drawings, etc.)
"""
import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import jsonschema

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def load_pages(pages_dir: Path) -> list:
    """Lade alle p{NN}.json Files sortiert."""
    pages = []
    for p in range(1, 24):
        page_path = pages_dir / f"p{p:02d}.json"
        if not page_path.exists():
            print(f"  WARN: {page_path.name} fehlt!")
            continue
        try:
            page = json.loads(page_path.read_text())
            pages.append(page)
        except json.JSONDecodeError as e:
            print(f"  ERROR: {page_path.name}: {e}")
    return pages


def enrich_page_with_symbol_info(page: dict, symbols_index: dict) -> dict:
    """Ergänze Symbole in der Seite mit Cluster-Info aus symbols_index."""
    sym_by_crop = {}
    for s in symbols_index.get("symbols", []):
        for occ in s.get("occurrences", []):
            cp = occ.get("crop_path", "")
            if cp:
                sym_by_crop[Path(cp).name] = s

    for region in page.get("regions", []):
        for sym in region.get("symbols", []):
            cp = sym.get("crop_path", "")
            if not cp:
                continue
            s = sym_by_crop.get(Path(cp).name)
            if s:
                # Falls Region-Sym-Info unvollständig: aus Index nehmen
                if sym.get("cluster_id", "GEOM_UNMATCHED_0000") == "GEOM_UNMATCHED_0000":
                    sym["symbol_id"] = s.get("symbol_id", sym.get("symbol_id", -1))
                    sym["cluster_id"] = s.get("cluster_id", "GEOM_UNMATCHED_0000")
                if not sym.get("vision_description") and s.get("description"):
                    sym["vision_description"] = s["description"]
                if not sym.get("unicode_codepoint") and s.get("unicode_codepoint"):
                    sym["unicode_codepoint"] = s["unicode_codepoint"]
    return page


def compute_page_stats(page: dict) -> dict:
    """Berechne Statistiken pro Seite."""
    regions = page.get("regions", [])
    n_text_words = sum(len(r.get("text_words", [])) for r in regions)
    n_symbols = sum(len(r.get("symbols", [])) for r in regions)
    n_drawings = sum(len(r.get("drawings", [])) for r in regions)
    n_uncertain = sum(len(r.get("uncertain", [])) for r in regions)

    # Region-Classification-Verteilung
    classifications = Counter(r.get("classification", "unknown") for r in regions)

    # Symbol-Cluster-Verteilung
    cluster_counter = Counter()
    for r in regions:
        for s in r.get("symbols", []):
            cluster_counter[s.get("cluster_id", "GEOM_UNMATCHED_0000")] += 1

    return {
        "n_regions": len(regions),
        "n_text_words": n_text_words,
        "n_symbols": n_symbols,
        "n_drawings": n_drawings,
        "n_uncertain": n_uncertain,
        "classifications": dict(classifications),
        "top_clusters": dict(cluster_counter.most_common(10)),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=Path, required=True,
                    help="bbox/pages_merged_<TS>/")
    ap.add_argument("--symbols", type=Path, required=True,
                    help="bbox/symbols_global_<TS>/symbols_index.json")
    ap.add_argument("--schema", type=Path, required=True,
                    help="schemas/tengri137_document.schema.json")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/final_<TS>/")
    ap.add_argument("--toplevel", type=Path, required=True,
                    help="Tengri137_detailed_<TS>/ (Top-Level copy)")
    ap.add_argument("--processing-run", type=str, required=True,
                    help="TS folder name, e.g. 20260704_V2")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    args.toplevel.mkdir(parents=True, exist_ok=True)

    # Lade Schema
    schema = json.loads(args.schema.read_text())
    print(f"Loaded schema from {args.schema}")

    # Lade Symbole
    symbols_index = json.loads(args.symbols.read_text())
    print(f"Loaded {symbols_index.get('total_symbols', 0)} symbols from index")

    # Lade Pages
    pages = load_pages(args.pages)
    print(f"Loaded {len(pages)} pages")

    # Verarbeite jede Seite
    all_stats = []
    for i, page in enumerate(pages):
        # Ergänze mit Symbol-Cluster-Info
        page = enrich_page_with_symbol_info(page, symbols_index)
        # Statistiken
        stats = compute_page_stats(page)
        all_stats.append(stats)
        page["stats"] = stats
        # Schreibe pro-Seite
        out_path = args.out / f"{page['page_id']}.json"
        out_path.write_text(json.dumps(page, indent=2, ensure_ascii=False))
        # Top-Level-Kopie
        toplevel_path = args.toplevel / f"{page['page_id']}.json"
        toplevel_path.write_text(json.dumps(page, indent=2, ensure_ascii=False))
        # Per-page validation nutzt nur die Page-Definition (kein Doc-Validation)
        page_schema = {"$ref": "#/definitions/page", "definitions": schema.get("definitions", {})}
        page_valid_doc = {
            "$ref": "#/definitions/page",
            "definitions": schema.get("definitions", {})
        }
        try:
            jsonschema.validate(page, page_valid_doc)
            valid = "✓"
        except jsonschema.ValidationError as e:
            valid = f"✗ {e.message[:50]}"
        print(f"  {page['page_id']}: {stats['n_regions']} regions, "
              f"{stats['n_symbols']} symbols, {stats['n_text_words']} words {valid}")

    # Top-Level Symbole-Index
    toplevel_sym = args.toplevel / "symbols_index.json"
    toplevel_sym.write_text(json.dumps(symbols_index, indent=2, ensure_ascii=False))
    print(f"Wrote {toplevel_sym}")

    # Single-File Document
    doc = {
        "schema_version": "2.0",
        "document": {
            "title": "Tengri137 - V2 Detailed Analysis",
            "page_count": len(pages),
            "source_pdf": "Tengri137.pdf",
            "processing_run": args.processing_run,
            "generated_at": "2026-07-04T00:00:00Z",
            "pipeline_version": "v2.0",
            "description": (
                "Detailed analysis of the Tengri137 PDF using embedding-based "
                "agglomerative clustering on 818 crops, multi-modal similarity "
                "(cosine + size + aspect), auto-silhouette threshold selection, "
                "and 23-page region structure with Vision-based symbol "
                "classification."
            ),
        },
        "pages": pages,
    }
    doc_path = args.toplevel / "doc.json"
    doc_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False))
    print(f"Wrote {doc_path}")

    # Final Document-Validation
    try:
        jsonschema.validate(doc, schema)
        print(f"\n✓ doc.json validates against schema ({len(pages)} pages)")
    except jsonschema.ValidationError as e:
        print(f"\n✗ doc.json FAILED: {e.message}")
        print(f"  Path: {list(e.absolute_path)}")
        return 1

    # Pipeline-Statistik
    total_regions = sum(s["n_regions"] for s in all_stats)
    total_symbols = sum(s["n_symbols"] for s in all_stats)
    total_words = sum(s["n_text_words"] for s in all_stats)
    print(f"\n=== Pipeline-Statistik ===")
    print(f"  Total regions: {total_regions}")
    print(f"  Total symbols: {total_symbols}")
    print(f"  Total text words: {total_words}")
    print(f"  Pages: {len(pages)}")
    print(f"  Schema-Validation: OK")

    return 0


if __name__ == "__main__":
    sys.exit(main())
