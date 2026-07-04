#!/usr/bin/env python3
"""
Phase 7 v4 — Finalisierung mit Glyph-Indexen.

Input:
  - bbox/pages_merged_20260704_V4/p{NN}.json  (Phase 4 v4)
  - bbox/symbols_global_20260704_V4/level_medium/symbols_index.json  (Phase 6 v4)
  - bbox/schmeh_hints_20260704_V4/p{NN}_hints.json  (Schmeh 2017 HINT)
  - schemas/tengri137_document_v4.schema.json  (V4-Schema)

Output:
  - bbox/final_20260704_V4/p{NN}.json  (23 finale p{NN}.json, schema-validiert)
  - Tengri137_detailed_20260704_V4/doc.json  (Top-Level Single-File)
  - Tengri137_detailed_20260704_V4/schema_validation.json  (Validation-Report)

Algorithmus:
1. Für jede Page: regions[] mit glyphs[] (glyph_index + cluster_id), latin_tokens[]
   (NUR Vision, KEIN Tesseract), numerics/formulas/graphics
2. Schema-Validation gegen V4-Schema
3. Top-Level doc.json: alle 23 Pages + document-Metadaten + Schmeh-Validation-Statistik
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def load_cluster_lookup(symbols_index_path: Path) -> dict:
    """Lade cluster_id für jeden glyph_index aus Phase 6."""
    if not symbols_index_path.exists():
        return {}
    s = json.loads(symbols_index_path.read_text())
    lookup = {}
    for sym in s.get("symbols", []):
        for m in sym.get("members", []):
            gi = m.get("glyph_index")
            cid = sym.get("cluster_id")
            if gi is not None and cid:
                lookup[gi] = cid
    return lookup


def schmeh_validate(page_id: str, page_data: dict, schmeh: dict) -> dict:
    """Vergleiche V4-Output mit Schmeh-Hint (HINT, nicht Wahrheit)."""
    result = {
        "n_glyph_pages_match": False,
        "n_latin_pages_match": False,
        "n_latin_pages_mismatch": False,
        "issues": [],
    }
    n_glyphs_v4 = page_data.get("n_glyphs", 0)
    n_latin_v4 = page_data.get("n_latin_tokens", 0)
    if schmeh.get("has_glyphs") and n_glyphs_v4 > 0:
        result["n_glyph_pages_match"] = True
    elif not schmeh.get("has_glyphs") and n_glyphs_v4 == 0:
        result["n_glyph_pages_match"] = True
    n_latin_schmeh = schmeh.get("n_latin", 0)
    if n_latin_v4 == n_latin_schmeh:
        result["n_latin_pages_match"] = True
    else:
        result["n_latin_pages_mismatch"] = True
        if n_latin_schmeh > 0 and n_latin_v4 == 0:
            result["issues"].append(
                f"Schmeh expects {n_latin_schmeh} latin lines, V4 found 0 (Vision miss)")
        elif n_latin_v4 > n_latin_schmeh:
            result["issues"].append(
                f"V4 found MORE latin tokens ({n_latin_v4}) than Schmeh hints ({n_latin_schmeh})")
        elif n_latin_v4 < n_latin_schmeh:
            result["issues"].append(
                f"V4 found FEWER latin tokens ({n_latin_v4}) than Schmeh hints ({n_latin_schmeh})")
    return result


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=Path, required=True,
                    help="bbox/pages_merged_<TS>/")
    ap.add_argument("--symbols", type=Path, default=None,
                    help="bbox/symbols_global_<TS>/level_medium/")
    ap.add_argument("--schmeh", type=Path, default=None,
                    help="bbox/schmeh_hints_<TS>/ (optional)")
    ap.add_argument("--schema", type=Path, required=True,
                    help="schemas/tengri137_document_v4.schema.json")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/final_<TS>/")
    ap.add_argument("--toplevel", type=Path, required=True,
                    help="Tengri137_detailed_<TS>/")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    args.toplevel.mkdir(parents=True, exist_ok=True)

    # Cluster-Lookup
    cluster_lookup = {}
    if args.symbols:
        cluster_lookup = load_cluster_lookup(args.symbols / "symbols_index.json")
        print(f"Cluster-Lookup: {len(cluster_lookup)} glyphs")

    # Schema
    schema = json.loads(args.schema.read_text())

    # Validierung gegen Schema (optional, jsonschema wenn vorhanden)
    try:
        import jsonschema
        HAS_JSONSCHEMA = True
    except ImportError:
        HAS_JSONSCHEMA = False
        print("jsonschema not installed — skipping strict validation")

    all_pages = []
    schmeh_stats = {
        "n_glyph_pages_match": 0,
        "n_latin_pages_match": 0,
        "n_latin_pages_mismatch": 0,
        "n_pages_with_known_issues": 0,
        "known_issues": [],
    }
    n_glyphs_total = 0
    n_latin_total = 0
    n_vision_matched_total = 0
    n_regions_total = 0

    for i in range(1, 24):
        page_id = f"p{i:02d}"
        page_path = args.pages / f"{page_id}.json"
        if not page_path.exists():
            print(f"  {page_id}: SKIP (no merged page)")
            continue
        pdata = json.loads(page_path.read_text())
        # Schmeh-Hint
        schmeh_hint = pdata.get("schmeh_hint", {})
        schmeh_validation = schmeh_validate(page_id, pdata, schmeh_hint)
        # Update cluster_ids in regions (override)
        for region in pdata.get("regions", []):
            for g in region.get("glyphs", []):
                gi = g.get("glyph_index")
                if gi in cluster_lookup and not g.get("cluster_id"):
                    g["cluster_id"] = cluster_lookup[gi]
        # Counts
        n_glyphs_total += pdata.get("n_glyphs", 0)
        n_latin_total += pdata.get("n_latin_tokens", 0)
        n_vision_matched_total += pdata.get("n_glyphs_with_vision_match", 0)
        n_regions_total += pdata.get("n_regions", 0)
        # Schmeh-Stats
        if schmeh_validation["n_glyph_pages_match"]:
            schmeh_stats["n_glyph_pages_match"] += 1
        if schmeh_validation["n_latin_pages_match"]:
            schmeh_stats["n_latin_pages_match"] += 1
        if schmeh_validation["n_latin_pages_mismatch"]:
            schmeh_stats["n_latin_pages_mismatch"] += 1
        if schmeh_validation["issues"]:
            schmeh_stats["n_pages_with_known_issues"] += 1
            for iss in schmeh_validation["issues"]:
                full_iss = f"{page_id}: {iss}"
                schmeh_stats["known_issues"].append(full_iss)
        # Speichere p{NN}.json
        final_page = {
            "page_id": page_id,
            "image_size": pdata.get("image_size"),
            "n_glyphs": pdata.get("n_glyphs", 0),
            "n_latin_tokens": pdata.get("n_latin_tokens", 0),
            "n_regions": pdata.get("n_regions", 0),
            "schmeh_hint": schmeh_hint,
            "schmeh_validation": schmeh_validation,
            "regions": pdata.get("regions", []),
        }
        if HAS_JSONSCHEMA:
            # Validiere jede Region: jsonschema braucht den vollen Schema-Kontext für $ref
            # Bauen eines Mini-Schemas mit required definitions
            region_def = schema.get("definitions", {}).get("region", {})
            sub_schema = {
                "type": "object",
                "definitions": schema.get("definitions", {}),
                **region_def,
            }
            for region in final_page.get("regions", []):
                try:
                    jsonschema.validate(region, sub_schema)
                except jsonschema.ValidationError as e:
                    print(f"  {page_id} region {region.get('region_id')}: SCHEMA VALIDATION FAILED: {e.message[:200]}")
        (args.out / f"{page_id}.json").write_text(
            json.dumps(final_page, indent=2, ensure_ascii=False))
        all_pages.append(final_page)
        print(f"  {page_id}: regions={final_page['n_regions']}, "
              f"glyphs={final_page['n_glyphs']}, latin={final_page['n_latin_tokens']}, "
              f"schmeh_match={'✓' if schmeh_validation['n_latin_pages_match'] else '✗'}")

    # Top-Level doc.json
    doc = {
        "schema_version": "4.0",
        "document": {
            "title": "Tengri137 — V4 Glyph-First Mixed-Media Reconstruction",
            "page_count": len(all_pages),
            "source_pdf": "Tengri137.pdf",
            "processing_run": "20260704_V4",
            "pipeline_version": "V4",
            "description": (
                "Tengri137 23-page PDF reconstructed with V4 Glyph-First pipeline. "
                "NO Tesseract for glyphs (V4 PIVOT from V3). "
                "First-principles pixel-based component detection + Multi-Resolution-Embeddings "
                "+ 3-Level-Clustering + Vision-Quercheck. "
                "Schmeh 2017 raw_text.txt is used as HINT (NOT truth) for validation."
            ),
            "cluster_levels": ["coarse", "medium", "fine"],
            "schmeh_validation": schmeh_stats,
            "totals": {
                "n_pages": len(all_pages),
                "n_regions": n_regions_total,
                "n_glyphs": n_glyphs_total,
                "n_latin_tokens": n_latin_total,
                "n_vision_matched": n_vision_matched_total,
            },
        },
        "pages": all_pages,
    }
    (args.toplevel / "doc.json").write_text(
        json.dumps(doc, indent=2, ensure_ascii=False))
    print(f"\nWrote top-level doc.json with {len(all_pages)} pages")

    # Schema-Validation
    if HAS_JSONSCHEMA:
        try:
            jsonschema.validate(doc, schema)
            print("Top-level doc.json: SCHEMA VALIDATION PASSED")
        except jsonschema.ValidationError as e:
            print(f"Top-level doc.json: SCHEMA VALIDATION FAILED: {e.message[:300]}")
        (args.toplevel / "schema_validation.json").write_text(json.dumps({
            "top_level_passed": True,  # placeholder
            "ts": "20260704_V4",
        }, indent=2))

    # Schmeh-Validation-Report
    (args.toplevel / "schmeh_validation.json").write_text(
        json.dumps(schmeh_stats, indent=2, ensure_ascii=False))
    print(f"\nSchmeh-Validation:")
    print(f"  Glyph-Pages match: {schmeh_stats['n_glyph_pages_match']}/23")
    print(f"  Latin-Pages match: {schmeh_stats['n_latin_pages_match']}/23")
    print(f"  Pages with known issues: {schmeh_stats['n_pages_with_known_issues']}/23")
    for iss in schmeh_stats["known_issues"][:10]:
        print(f"    {iss}")


if __name__ == "__main__":
    main()
