#!/usr/bin/env python3
"""
Phase 3 — Pixel + Vision zusammenführen.

Liest:
  - bbox/pages_pixel_<TS>/p{NN}.json
  - bbox/vision_qa_<TS>/p{NN}/p{NN}_page.json   (optional, sobald vorhanden)
  - bbox/vision_qa_<TS>/p{NN}/p{NN}_glyphs/*.json

Schreibt:
  - bbox/pages_merged_<TS>/p{NN}.json  im Schema page.schema.json
"""
import argparse
import json
import re
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pixel", type=Path, required=True)
    ap.add_argument("--vision", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    for i in range(1, 24):
        page_id = f"p{i:02d}"
        pixel_path = args.pixel / f"{page_id}.json"
        if not pixel_path.exists():
            print(f"  {page_id}: SKIP (no pixel data)")
            continue
        pixel = json.loads(pixel_path.read_text())

        # Vision data
        vision_page = args.vision / page_id / f"{page_id}_page.json"
        vision_glyphs = args.vision / page_id / f"{page_id}_glyphs"
        page_v = {}
        if vision_page.exists():
            try:
                page_v = json.loads(vision_page.read_text())
            except json.JSONDecodeError:
                page_v = {"error": "invalid_json"}
        glyph_vs = []
        if vision_glyphs.exists():
            for gj in sorted(vision_glyphs.glob("g*.json")):
                try:
                    glyph_vs.append(json.loads(gj.read_text()))
                except json.JSONDecodeError:
                    pass

        # Build merged page
        # text_words from pixel
        text_words = pixel.get("text_words", [])

        # symbols: combine pixel blanks + vision symbols + vision glyph descriptions
        symbols = []
        seen_boxes = []
        # Add pixel-derived blank regions as candidate symbol entries (to be
        # classified in Phase 4)
        for j, b in enumerate(pixel.get("blank_regions", [])):
            bbox = [b["left"], b["top"], b["width"], b["height"]]
            # Check if any vision glyph description is near this bbox
            kind = None
            description = None
            for gv in glyph_vs:
                if gv.get("crop_bbox") == bbox:
                    kind = gv.get("kind")
                    description = gv.get("description")
                    break
            symbols.append({
                "symbol_index": None,  # filled in Phase 4
                "page": page_id,
                "first_appearance": False,  # filled in Phase 4
                "bbox": bbox,
                "kind": kind or "blank_region_to_classify",
                "description": description or (
                    f"Empty/blank region {b['width']}x{b['height']} px, "
                    f"fill_ratio={b.get('fill_ratio', 0):.2f}"),
                "vision_verified": kind is not None,
                "geometry_ref": None,
            })

        # Add vision-reported symbols that don't overlap with blanks
        for vs in page_v.get("symbols", []):
            # Vision-symbols are textual descriptions, no exact bbox;
            # attach a generic "see vision description" entry
            symbols.append({
                "symbol_index": None,
                "page": page_id,
                "first_appearance": False,
                "bbox": None,
                "kind": vs.get("kind", "unknown"),
                "description": vs.get("description", ""),
                "position": vs.get("position"),
                "vision_verified": True,
                "geometry_ref": None,
            })

        # drawings from vision decorations
        drawings = []
        for j, d in enumerate(page_v.get("decorations", [])):
            drawings.append({
                "drawing_id": f"{page_id}_D{j+1}",
                "page": page_id,
                "bbox": None,
                "type": d.get("type", "unknown"),
                "description": d.get("description", ""),
                "components": d.get("components", []),
                "vision_verified": True,
            })

        # digits and formulas from pixel
        digits = pixel.get("digits", [])
        formulas = pixel.get("formulas", [])

        # mixed_media_regions: build from overlapping text+blank+color regions
        mixed = []
        for c in pixel.get("colored_regions", []):
            cb = [c["left"], c["top"], c["width"], c["height"]]
            # find text words inside this region
            inside = [w for w in text_words
                      if w["bbox"][0] >= cb[0] - 5 and
                         w["bbox"][1] >= cb[1] - 5 and
                         w["bbox"][0] + w["bbox"][2] <= cb[0] + cb[2] + 5 and
                         w["bbox"][1] + w["bbox"][3] <= cb[1] + cb[3] + 5]
            if inside:
                mixed.append({
                    "region_id": f"{page_id}_M{len(mixed)+1}",
                    "bbox": cb,
                    "components": [f"colored text ({c.get('color', 'unknown')})"]
                                 + [w["text"] for w in inside[:5]],
                    "description": (f"Colored region containing "
                                    f"{len(inside)} text words"),
                })

        # uncertain
        uncertain = list(page_v.get("uncertain_or_unreadable", []))

        # Schema-validate: all required fields present
        out = {
            "page": page_id,
            "image_size": pixel.get("image_size"),
            "text_words": text_words,
            "symbols": symbols,
            "drawings": drawings,
            "digits": digits,
            "formulas": formulas,
            "mixed_media_regions": mixed,
            "uncertain": uncertain,
        }
        (args.out / f"{page_id}.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False))
        n_text = len(text_words)
        n_sym = len(symbols)
        n_dra = len(drawings)
        n_dig = len(digits)
        n_for = len(formulas)
        n_mix = len(mixed)
        print(f"  {page_id}: text={n_text} sym={n_sym} drw={n_dra} "
              f"dig={n_dig} frm={n_for} mix={n_mix}")


if __name__ == "__main__":
    main()
