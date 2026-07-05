#!/usr/bin/env python3
"""
phase6_finalize_v5.py — Schema-validierte Finalisierung (DevMind).

V5 PIVOT: Finalisierung OHNE Schmeh-Felder. Sammelt alle V5-Phase-Outputs
in finale p{NN}.json + doc.json, validiert gegen v5-Schema.

Input:  bbox/ocr_20260705_V5/p{NN}.json
        bbox/cryptanalysis_20260705_V5/crypto_report.json
        bbox/alphabet_20260705_V5/alphabet.json
        bbox/decoded_20260705_V5/decode_report.json
        schemas/tengri137_document_v5.schema.json
Output: bbox/final_20260705_V5/p{NN}.json (23 files)
        Tengri137_detailed_20260705_V5/doc.json
"""
import argparse
import json
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ocr", type=Path, required=True,
                    help="bbox/ocr_20260705_V5/")
    ap.add_argument("--cryptanalysis", type=Path, required=True,
                    help="bbox/cryptanalysis_20260705_V5/crypto_report.json")
    ap.add_argument("--alphabet", type=Path, required=True,
                    help="bbox/alphabet_20260705_V5/alphabet.json")
    ap.add_argument("--decode", type=Path, required=True,
                    help="bbox/decoded_20260705_V5/decode_report.json")
    ap.add_argument("--schema", type=Path, required=True,
                    help="schemas/tengri137_document_v5.schema.json")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/final_20260705_V5/")
    ap.add_argument("--toplevel", type=Path, required=True,
                    help="Tengri137_detailed_20260705_V5/")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    args.toplevel.mkdir(parents=True, exist_ok=True)

    # Optional: jsonschema
    try:
        import jsonschema
        HAS_JSONSCHEMA = True
    except ImportError:
        HAS_JSONSCHEMA = False
        print("WARNUNG: jsonschema nicht verfügbar — keine strikte Validation", file=sys.stderr)

    schema = json.loads(args.schema.read_text())
    crypto = json.loads(args.cryptanalysis.read_text())
    alphabet = json.loads(args.alphabet.read_text())
    decode = json.loads(args.decode.read_text())

    all_pages = []
    n_glyphs_total = 0
    n_latin_total = 0
    n_pages_with_latin = 0
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        ocr_path = args.ocr / f"{page_id}.json"
        if not ocr_path.exists():
            print(f"  {page_id}: SKIP (kein OCR-Output)")
            continue
        ocr_data = json.loads(ocr_path.read_text())

        page = {
            "page_id": page_id,
            "image_size": [1125, 1625],
            "layout_type": ocr_data["layout_type"],
            "layout_confidence": ocr_data.get("layout_confidence", 0.0),
            "n_tengri_glyphs": ocr_data["n_tengri_glyphs"],
            "regions": ocr_data["regions"],
        }
        n_glyphs_total += page["n_tengri_glyphs"]
        n_latin = sum(len(r["latin_tokens"]) for r in page["regions"])
        n_latin_total += n_latin
        if n_latin > 0:
            n_pages_with_latin += 1

        # Schema-Validation (jsonschema $ref braucht vollen Schema-Kontext)
        if HAS_JSONSCHEMA:
            try:
                sub_schema = {
                    "type": "object",
                    "definitions": schema.get("definitions", {}),
                    **schema["definitions"]["page"],
                }
                jsonschema.validate(page, sub_schema)
            except jsonschema.ValidationError as e:
                print(f"  {page_id} SCHEMA-FAIL: {e.message[:200]}")

        (args.out / f"{page_id}.json").write_text(json.dumps(page, indent=2, ensure_ascii=False))
        all_pages.append(page)
        print(f"  {page_id}: {page['layout_type']:<20} tengri={page['n_tengri_glyphs']:3d}, "
              f"latin={n_latin:3d}")

    # Top-Level doc.json
    doc = {
        "schema_version": "5.0",
        "document": {
            "title": "Tengri137 — V5 Cryptanalysis-First Reconstruction",
            "page_count": len(all_pages),
            "source_pdf": "Tengri137.pdf",
            "processing_run": "20260705_V5",
            "pipeline_version": "V5",
            "description": (
                "Tengri137 23-page PDF reconstructed with V5 Cryptanalysis-First pipeline. "
                "V5 IGNORES Schmeh (H1 abgelehnt: IoC 0.16 ≠ Englisch 0.067). "
                "Pipeline: Phase 0 (Inken-Substrat) → Phase 1 (CryptanalysisMind) → "
                "Phase 2 (Glyph-Alphabet, K=34) → Phase 3 (Layout per Page) → "
                "Phase 4 (Selective OCR) → Phase 5 (Substitution-Validation)."
            ),
            "alphabet_size": alphabet["actual_K"],
            "cryptanalysis": {
                "h1_hypothesis": crypto["hypothesis"]["label"],
                "h1_status": decode["hypothesis_h1_status"],
                "shannon_entropy": crypto["shannon_entropy"],
                "ioc": crypto["ioc"],
                "zipf_alpha": crypto["zipf_alpha"],
                "f1_score": decode["f1_score"],
                "f1_reasons": decode["f1_reasons"],
            },
            "totals": {
                "n_pages": len(all_pages),
                "n_glyphs": n_glyphs_total,
                "n_latin_tokens": n_latin_total,
                "n_pages_with_latin": n_pages_with_latin,
            },
        },
        "pages": all_pages,
    }
    (args.toplevel / "doc.json").write_text(json.dumps(doc, indent=2, ensure_ascii=False))
    print(f"\n[Phase 6] Top-Level doc.json: {len(all_pages)} pages")

    # Schema-Validation
    if HAS_JSONSCHEMA:
        try:
            jsonschema.validate(doc, schema)
            print("[Phase 6] doc.json: SCHEMA VALIDATION PASSED")
        except jsonschema.ValidationError as e:
            print(f"[Phase 6] doc.json SCHEMA-FAIL: {e.message[:300]}")


if __name__ == "__main__":
    main()
