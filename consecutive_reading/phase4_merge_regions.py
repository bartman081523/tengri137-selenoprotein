#!/usr/bin/env python3
"""
Phase 4 v4 — Region-Building mit Glyph-Indexen.

Input:
  - bbox/components_20260704_V4/p{NN}/p{NN}_glyphs.json  (Phase 2 v4 Glyphen)
  - bbox/components_20260704_V4/p{NN}/p{NN}_lines.json   (Phase 2 v4 Zeilen)
  - bbox/vision_qa_20260704_V4/p{NN}/p{NN}_line_*.json  (Phase 3 v4 Vision)
  - bbox/schmeh_hints_20260704_V4/p{NN}_hints.json       (Schmeh 2017, HINT-Quelle)

Output:
  - bbox/pages_merged_20260704_V4/p{NN}.json
    {
      "page_id": "p01",
      "image_size": [1125, 1625],
      "n_glyphs": 95,
      "n_latin_tokens": 0,
      "schmeh_hint": {...},
      "regions": [
        {
          "region_id": "p01_R1",
          "bbox": [196, 421, 733, 50],
          "region_type": "glyph_raster",
          "lines": [1],
          "glyphs": [
            {"glyph_index": 1, "page": "p01", "bbox": [469, 252, 200, 96],
             "size_px": 5000, "fill_ratio": 0.36, "n_components": 5,
             "components": [12, 14, 17, 19, 22],
             "type_hint": "geometric_symbol",
             "vision_kind": "geometric_diamond",
             "vision_description": "Rautenförmiges Symbol mit zentralem Punkt",
             "vision_confidence": 0.78,
             "cluster_id": null, "line_id": 1}
          ],
          "latin_tokens": [], "formulas": [], "numerics": [], "graphics": [],
          "uncertain": []
        }
      ]
    }

Algorithmus:
1. Pro Zeile aus Phase 2: Region-Building (eine Region pro Zeile + ggf. Header/Footer-Splits)
2. Pro Glyph: lookup Vision-Match (Phase 3) → vision_kind, vision_description
3. Pro lateinischer Token: nur aus Vision (Phase 3), NIE Tesseract
4. region_type-Heuristik:
   - is_likely_latin → "latin_text"
   - is_likely_glyph_raster → "glyph_raster"
   - Header (y<200) → "header"
   - Footer (y>1500) → "footer"
   - Schmeh has_magic_cube → "magic_cube"
   - Schmeh has_rings → "rings_sigil"
   - Schmeh has_burumut_block → "burumut_block"
5. Glyph-Cluster-Lookup (Phase 6 Output, optional)
6. Schmeh-Hint-Vergleich: zähle Übereinstimmungen / Widersprüche
"""
import argparse
import json
import re
import sys
from pathlib import Path
from collections import defaultdict

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def bbox_union(boxes):
    """Union mehrerer BBoxen [x0,y0,w,h]."""
    if not boxes:
        return None
    x0 = min(b[0] for b in boxes)
    y0 = min(b[1] for b in boxes)
    x1 = max(b[0] + b[2] for b in boxes)
    y1 = max(b[1] + b[3] for b in boxes)
    return [int(x0), int(y0), int(x1 - x0), int(y1 - y0)]


def classify_region_type(line: dict, vision: dict, schmeh: dict, y_pos: int) -> str:
    """region_type-Heuristik. Vision hat VORRANG vor Heuristik."""
    # V4: Vision-Ergebnisse haben Vorrang
    if vision:
        ltype = vision.get("line_type", "")
        if ltype == "pure_latin_line":
            return "latin_text"
        if ltype == "pure_numeric_line":
            return "numeric_table"
        if ltype == "pure_formula_line":
            return "formula_block"
        if ltype == "graphic_line":
            return "graphic_line"
        if ltype == "empty_line":
            return "graphic_line"  # leere Zeile
    if y_pos < 200:
        return "header"
    if y_pos > 1500:
        return "footer"
    if schmeh.get("has_magic_cube") and line.get("n_glyphs", 0) >= 9:
        return "magic_cube"
    if schmeh.get("has_rings"):
        return "rings_sigil"
    # V4: Heuristik nur als Fallback, wenn keine Vision
    if line.get("is_likely_latin", False):
        return "latin_text"
    if line.get("is_likely_glyph_raster", False):
        return "glyph_raster"
    if line.get("n_glyphs", 0) == 1:
        return "single_glyph"
    if line.get("n_glyphs", 0) > 1:
        return "glyph_block"
    return "mixed"


def get_cluster_id_for_glyph(glyph_index: int, cluster_lookup: dict) -> str:
    """Lookup cluster_id aus Phase 6 output."""
    return cluster_lookup.get(str(glyph_index)) or cluster_lookup.get(glyph_index)


def process_page(page_num: int, components_dir: Path, vision_dir: Path,
                 schmeh_dir: Path, out_dir: Path, cluster_lookup: dict = None):
    """Verarbeitet eine einzelne Page."""
    page_id = f"p{page_num:02d}"
    components_path = components_dir / page_id / f"{page_id}_glyphs.json"
    lines_path = components_dir / page_id / f"{page_id}_lines.json"
    if not components_path.exists() or not lines_path.exists():
        print(f"  {page_id}: SKIP (missing components/lines)")
        return None

    glyphs_data = json.loads(components_path.read_text())
    lines_data = json.loads(lines_path.read_text())
    glyphs = {g["glyph_index"]: g for g in glyphs_data.get("glyphs", [])}

    # Schmeh-Hint
    schmeh_path = schmeh_dir / f"{page_id}_hints.json"
    schmeh = {}
    if schmeh_path.exists():
        schmeh_full = json.loads(schmeh_path.read_text())
        schmeh = {
            "n_latin": schmeh_full.get("n_latin", 0),
            "n_glyphs": schmeh_full.get("n_glyphs", 0),
            "has_glyphs": schmeh_full.get("has_glyphs", False),
            "has_magic_cube": schmeh_full.get("has_magic_cube", False),
            "has_rings": schmeh_full.get("has_rings", False),
            "has_burumut_block": schmeh_full.get("has_burumut_block", False),
        }

    # Vision-Output pro Zeile
    vision_per_line = {}
    if vision_dir:
        vpage_dir = vision_dir / page_id
        if vpage_dir.exists():
            # Pattern: p01_line02.json (zweistellig) oder p01_line_02.json
            for vf in sorted(list(vpage_dir.glob(f"{page_id}_line*.json"))):
                vdata = json.loads(vf.read_text())
                lid = vdata.get("line_id")
                if lid is not None:
                    vision_per_line[lid] = vdata

    # Pro Zeile: Region bauen
    regions = []
    n_glyphs_in_regions = 0
    n_latin_in_regions = 0
    n_matched_with_vision = 0
    for line in lines_data.get("lines", []):
        lid = line["line_id"]
        y_center = line.get("y_center", 0)
        y_pos = line.get("bbox", [0, 0, 0, 0])[1]

        vision = vision_per_line.get(lid, {})
        rtype = classify_region_type(line, vision, schmeh, y_pos)

        # Glyphen dieser Zeile
        region_glyphs = []
        glyph_ids_in_line = line.get("glyph_ids", [])
        for gid in glyph_ids_in_line:
            g = glyphs.get(gid)
            if not g:
                continue
            # Vision-Match: suche in vision.matched_glyphs
            vision_match = None
            for vm in vision.get("matched_glyphs", []):
                if vm.get("matched_glyph_index") == gid:
                    vision_match = vm
                    break
            vg = vision_match.get("vision_glyph", {}) if vision_match else {}
            v_kind = vg.get("visual_kind", "")
            v_desc = vg.get("description", "")
            v_conf = vg.get("confidence", 0.0)
            v_unicode = vg.get("unicode_codepoint_candidate", "")
            if v_kind or v_desc:
                n_matched_with_vision += 1

            cluster_id = None
            if cluster_lookup:
                cluster_id = get_cluster_id_for_glyph(gid, cluster_lookup)

            region_glyphs.append({
                "glyph_index": gid,
                "page": page_id,
                "page_glyph_id": g.get("page_glyph_id"),
                "cluster_id": cluster_id,
                "line_id": lid,
                "bbox": g["bbox"],
                "size_px": g.get("size_px"),
                "fill_ratio": g.get("fill_ratio"),
                "n_components": g.get("n_components"),
                "components": g.get("components", []),
                "type_hint": g.get("type_hint"),
                "vision_kind": v_kind or None,
                "vision_description": v_desc or None,
                "vision_confidence": v_conf if v_conf else None,
                "unicode_codepoint_candidate": v_unicode or None,
            })

        # Latin-Tokens (nur aus Vision, NICHT Tesseract)
        # V4: Konfidenz-Filter (>=0.7) verhindert Halluzinationen einzelner Buchstaben
        region_latin = []
        for lt in vision.get("latin_tokens", []):
            text = lt.get("text", "").strip()
            if not text:
                continue
            conf = lt.get("confidence", 0.0)
            # Filter: nur multi-char tokens mit conf>=0.7 ODER high-conf single chars
            if len(text) > 1 and conf < 0.7:
                continue
            if len(text) == 1 and conf < 0.85:
                continue
            lt_bbox = lt.get("bbox", [])
            lt_bbox_clean = [max(0, int(c)) for c in lt_bbox] if lt_bbox else []
            region_latin.append({
                "text": text,
                "bbox": lt_bbox_clean,
                "conf": conf,
                "line_id": lid,
                "source": "vision",
            })
        # Schmeh-Hint: nur lateinische Zeilen aus Schmeh, falls Vision leer
        if not region_latin and schmeh.get("n_latin", 0) > 0:
            # Suche Schmeh-Zeile mit line_id
            schmeh_lines = []
            if schmeh_path.exists():
                schmeh_lines = json.loads(schmeh_path.read_text()).get("lines", [])
            slines_latin = [sl for sl in schmeh_lines if sl.get("type") == "latin"]
            if lid - 1 < len(slines_latin):
                sl = slines_latin[lid - 1]
                if sl.get("type") == "latin":
                    region_latin.append({
                        "text": sl.get("text", "").strip(),
                        "bbox": line.get("bbox", [0, 0, 0, 0]),
                        "conf": 0.5,  # Schmeh ist Hinweis, nicht Wahrheit
                        "line_id": lid,
                        "source": "schmeh_hint",
                    })

        # Formulas / Numerics (Vision)
        region_formulas = []
        for f in vision.get("formulas", []):
            f_bbox = [max(0, int(c)) for c in f.get("bbox", [])] if f.get("bbox") else []
            region_formulas.append({
                "raw": f.get("raw", ""),
                "bbox": f_bbox,
                "line_id": lid,
            })
        region_numerics = []
        for n in vision.get("numerics", []):
            bbox = [max(0, int(c)) for c in n.get("bbox", [])] if n.get("bbox") else []
            region_numerics.append({
                "value": n.get("value", ""),
                "bbox": bbox,
            })
        region_graphics = []
        for gr in vision.get("graphics", []):
            region_graphics.append({
                "type": gr.get("type", "unknown"),
                "description": gr.get("description", ""),
                "bbox": gr.get("bbox", []),
            })

        # Uncertain: Glyphen mit vision_confidence < 0.5
        uncertain = [g["glyph_index"] for g in region_glyphs
                     if g.get("vision_confidence") is not None
                     and g["vision_confidence"] < 0.5]

        region = {
            "region_id": f"{page_id}_R{lid}",
            "bbox": [max(0, int(c)) for c in line.get("bbox", [0, 0, 0, 0])],
            "region_type": rtype,
            "description": (
                f"Line {lid}, y_center={y_center}, "
                f"glyphs={len(region_glyphs)}, latin={len(region_latin)}"
            ),
            "lines": [lid],
            "glyphs": region_glyphs,
            "latin_tokens": region_latin,
            "formulas": region_formulas,
            "numerics": region_numerics,
            "graphics": region_graphics,
            "uncertain": uncertain,
        }
        regions.append(region)
        n_glyphs_in_regions += len(region_glyphs)
        n_latin_in_regions += len(region_latin)

    out = {
        "page_id": page_id,
        "image_size": [1125, 1625],
        "n_glyphs": n_glyphs_in_regions,
        "n_latin_tokens": n_latin_in_regions,
        "n_regions": len(regions),
        "n_glyphs_with_vision_match": n_matched_with_vision,
        "schmeh_hint": schmeh,
        "regions": regions,
    }
    out_path = out_dir / f"{page_id}.json"
    out_path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--components", type=Path, required=True,
                    help="bbox/components_<TS>/")
    ap.add_argument("--vision", type=Path, default=None,
                    help="bbox/vision_qa_<TS>/ (optional)")
    ap.add_argument("--schmeh", type=Path, default=None,
                    help="bbox/schmeh_hints_<TS>/ (optional, HINT only)")
    ap.add_argument("--symbols", type=Path, default=None,
                    help="bbox/symbols_global_<TS>/level_medium/ (optional, cluster lookup)")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Cluster-Lookup laden
    cluster_lookup = {}
    if args.symbols:
        sym_index = args.symbols / "symbols_index.json"
        if sym_index.exists():
            sdata = json.loads(sym_index.read_text())
            for entry in sdata.get("symbols", []):
                cid = entry.get("cluster_id")
                if not cid:
                    continue
                # Top-Level glyph_index (falls vorhanden) + alle members durchgehen
                gids = set()
                top_gid = entry.get("glyph_index")
                if top_gid is not None:
                    gids.add(top_gid)
                for m in entry.get("members", []):
                    mgi = m.get("glyph_index")
                    if mgi is not None:
                        gids.add(mgi)
                for g in gids:
                    cluster_lookup[g] = cid
            print(f"Cluster-Lookup geladen: {len(cluster_lookup)} Glyphen")

    n_pages = 0
    n_glyphs_total = 0
    n_latin_total = 0
    n_vision_matched = 0
    for i in range(1, 24):
        result = process_page(
            i, args.components, args.vision, args.schmeh, args.out,
            cluster_lookup=cluster_lookup,
        )
        if result is None:
            continue
        n_pages += 1
        n_glyphs_total += result["n_glyphs"]
        n_latin_total += result["n_latin_tokens"]
        n_vision_matched += result["n_glyphs_with_vision_match"]
        print(f"  p{i:02d}: regions={result['n_regions']}, "
              f"glyphs={result['n_glyphs']}, latin={result['n_latin_tokens']}, "
              f"vision_matched={result['n_glyphs_with_vision_match']}")
    print(f"\nTotal: {n_pages} pages, {n_glyphs_total} glyphs, "
          f"{n_latin_total} latin tokens, {n_vision_matched} vision-matched")


if __name__ == "__main__":
    main()
