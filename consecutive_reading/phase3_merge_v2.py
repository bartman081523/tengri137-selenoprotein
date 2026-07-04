#!/usr/bin/env python3
"""
Phase 3 v2 — Pixel + Vision → regions-Struktur (pro Seite).

Input:
  - bbox/pages_pixel_<TS>/p{NN}.json (Phase 1: Word-BBoxen, Blank/Color-Regionen)
  - bbox/vision_qa_<TS>/p{NN}/p{NN}_page.json (Phase 2: Vision-Region-Beschreibungen)
  - bbox/vision_qa_<TS>/p{NN}/p{NN}_glyphs/g{NNN}.json (Phase 2: Symbol-BBoxen + Labels)
  - bbox/symbols_global_<TS>/symbols_index.json (Phase 4b: Cluster-Index, optional)

Output:
  - bbox/pages_merged_<TS>/p{NN}.json mit regions-Struktur

Region-Typen:
  - text_block: Tesseract-Words
  - header/footer: spezielle Text-Regionen (oben/unten)
  - blank_region: Pixel-Blank-Region (z.B. für Sigille)
  - colored_region: Farbige Pixel-Region
  - drawing: Vision-only Drawing (z.B. norse_cosmic_circle)
  - mixed_media: Text + Symbol kombiniert (z.B. marginale Annotationen)

Jede Region hat:
  - region_id (p{NN}_R{nn})
  - bbox (Union aller Sub-BBoxen)
  - classification (text_block, header, magic_cube_3x3_exploded, etc.)
  - description
  - components[] (text_words, symbols, drawings)
  - uncertain[] (was unklar ist)
"""
import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def union_bbox(boxes):
    """Union mehrerer BBoxen [l,t,w,h] → [l_min, t_min, r_max-l_min, b_max-t_min]"""
    boxes = [list(b) for b in boxes if b and len(b) == 4]
    if not boxes:
        return None
    l = min(b[0] for b in boxes)
    t = min(b[1] for b in boxes)
    r = max(b[0] + b[2] for b in boxes)
    btm = max(b[1] + b[3] for b in boxes)
    return [l, t, r - l, btm - t]


def bbox_iou(b1, b2):
    """IoU zwischen [l,t,w,h] Boxen."""
    if b1 is None or b2 is None:
        return 0.0
    l1, t1, w1, h1 = b1
    l2, t2, w2, h2 = b2
    inter_l = max(l1, l2)
    inter_t = max(t1, t2)
    inter_r = min(l1 + w1, l2 + w2)
    inter_b = min(t1 + h1, t2 + h2)
    if inter_r <= inter_l or inter_b <= inter_t:
        return 0.0
    inter = (inter_r - inter_l) * (inter_b - inter_t)
    a1 = w1 * h1
    a2 = w2 * h2
    union = a1 + a2 - inter
    return inter / union if union > 0 else 0.0


def bbox_contains(outer, inner, threshold=0.7):
    """True wenn 'inner' zu >threshold in 'outer' enthalten ist."""
    if outer is None or inner is None:
        return False
    l1, t1, w1, h1 = outer
    l2, t2, w2, h2 = inner
    # Check overlap
    inter_l = max(l1, l2)
    inter_t = max(t1, t2)
    inter_r = min(l1 + w1, l2 + w2)
    inter_b = min(t1 + h1, t2 + h2)
    if inter_r <= inter_l or inter_b <= inter_t:
        return False
    inter = (inter_r - inter_l) * (inter_b - inter_t)
    inner_area = w2 * h2
    return (inter / inner_area) > threshold if inner_area > 0 else False


def identify_region_type(blk_words, blanks, colors, glyphs, vision_page):
    """Klassifiziere eine Region anhand der Komponenten.

    Strategie:
      - Wenn viele Words + keine Blanks/Glyphs: text_block
      - Wenn Words + Blanks: mixed_media
      - Wenn nur Blanks: blank_region
      - Wenn Vision-Page eine 'drawing' erwähnt: drawing
      - Wenn im Header/Footer (y < 100 oder y > 1500 @ 150dpi): header/footer
    """
    n_words = len(blk_words)
    n_blanks = len(blanks)
    n_colors = len(colors)
    n_glyphs = len(glyphs)
    if n_words == 0 and n_blanks == 0 and n_colors == 0 and n_glyphs == 0:
        return "empty"

    # Header/Footer-Detection (y < 80 or y > height-100)
    y_positions = []
    for w in blk_words:
        if len(w.get("bbox", [])) >= 2:
            y_positions.append(w["bbox"][1])
    for b in blanks:
        if len(b.get("bbox", [])) >= 2:
            y_positions.append(b["bbox"][1])
    if y_positions:
        ymin = min(y_positions)
        # Header wenn y < 100, Footer wenn y > 1500 (bei height=1754)
        if ymin < 100 and n_blanks == 0 and n_colors == 0:
            return "header"
    return "text_block" if n_words > 0 and n_blanks == 0 and n_colors == 0 else (
        "mixed_media" if n_words > 0 and (n_blanks > 0 or n_colors > 0) else
        "blank_region" if n_blanks > 0 and n_words == 0 else
        "colored_region" if n_colors > 0 and n_words == 0 else
        "drawing" if n_glyphs > 0 and n_words == 0 else
        "unknown"
    )


def cluster_blanks_with_vision(blanks, glyphs, vision):
    """Ordne Vision-Glyphs den Pixel-Blank-Regionen zu (IoU > 0.3).

    Returns: list of (blank_region, [glyphs_in_region])
    """
    # Sortiere Blanks nach Größe (größte zuerst)
    sorted_blanks = sorted(blanks, key=lambda b: -b.get("area_px", 0))
    used_glyphs = set()
    result = []
    for b in sorted_blanks:
        bbox = [b["left"], b["top"], b["width"], b["height"]]
        glyphs_in = []
        for j, g in enumerate(glyphs):
            if j in used_glyphs:
                continue
            g_bbox = g.get("crop_bbox")
            if not g_bbox or len(g_bbox) != 4:
                continue
            if bbox_iou(bbox, g_bbox) > 0.3:
                glyphs_in.append(g)
                used_glyphs.add(j)
        result.append((b, glyphs_in))
    # Verbleibende Glyphen (nicht zugeordnet)
    leftovers = [g for j, g in enumerate(glyphs) if j not in used_glyphs]
    return result, leftovers


def process_page(page_num: int, pixel_dir: Path, vision_dir: Path,
                 symbols_index: dict, next_synth_id: int = 1000000) -> tuple:
    """Prozessiere eine einzelne Seite → regions-Struktur."""
    page_id = f"p{page_num:02d}"

    # Lade Pixel-Daten
    pixel_path = pixel_dir / f"{page_id}.json"
    if not pixel_path.exists():
        return {"page_id": page_id, "error": "no pixel data"}, next_synth_id
    pixel = json.loads(pixel_path.read_text())
    img_size = pixel.get("image_size", [1754, 1240])
    blank_regions = pixel.get("blank_regions", [])
    colored_regions = pixel.get("colored_regions", [])
    words = pixel.get("text_words", [])

    # Lade Vision-Daten
    vision_page_path = vision_dir / page_id / f"{page_id}_page.json"
    vision_page = {}
    if vision_page_path.exists():
        try:
            vision_page = json.loads(vision_page_path.read_text())
        except json.JSONDecodeError:
            vision_page = {}

    # Lade Vision-Glyphs
    glyphs = []
    glyph_dir = vision_dir / page_id / f"{page_id}_glyphs"
    if glyph_dir.exists():
        for gf in sorted(glyph_dir.glob("g*.json")):
            try:
                g = json.loads(gf.read_text())
            except json.JSONDecodeError:
                continue
            if "error" in g and "crop_bbox" not in g:
                continue
            # Versuche crop_bbox zu rekonstruieren falls fehlt
            if "crop_bbox" not in g or not g["crop_bbox"]:
                # Aus Filename: g001_blank.png → index 001
                m = re.search(r"g(\d+)_(\w+)\.json$", gf.name)
                if m:
                    idx = int(m.group(1))
                    # Lookup in blank_regions (sortiert nach area_px desc)
                    sorted_blanks = sorted(blank_regions, key=lambda b: -b.get("area_px", 0))
                    if idx < len(sorted_blanks):
                        sb = sorted_blanks[idx]
                        g["crop_bbox"] = [sb["left"], sb["top"], sb["width"], sb["height"]]
            glyphs.append(g)

    # 1) Cluster Blanks + Vision-Glyphs
    blank_with_glyphs, leftover_glyphs = cluster_blanks_with_vision(
        blank_regions, glyphs, vision_page)

    # 2) Baue Regions
    regions = []
    region_counter = 0
    synth_id_counter = next_synth_id

    # Header/Footer-Detection: Words mit y < 80 oder y > height-80
    header_words = [w for w in words
                    if len(w.get("bbox", [])) >= 2 and w["bbox"][1] < 80]
    footer_words = [w for w in words
                    if len(w.get("bbox", [])) >= 2
                    and w["bbox"][1] > img_size[1] - 80]
    body_words = [w for w in words if w not in header_words and w not in footer_words]

    # 2a) Header
    if header_words:
        bboxes = [w["bbox"] for w in header_words if len(w.get("bbox", [])) == 4]
        bbox = union_bbox(bboxes)
        if bbox:
            region_counter += 1
            regions.append({
                "region_id": f"{page_id}_R{region_counter:02d}",
                "bbox": bbox,
                "classification": "header",
                "description": "Page header (top of page)",
                "text_words": [{
                    "text": w.get("text", ""),
                    "bbox": w.get("bbox"),
                    "conf_tesseract": w.get("conf_tesseract", w.get("conf", 0.0)),
                    "verified_by_vision": False,
                } for w in header_words],
                "symbols": [],
                "drawings": [],
                "uncertain": [],
            })

    # 2b) Footer
    if footer_words:
        bboxes = [w["bbox"] for w in footer_words if len(w.get("bbox", [])) == 4]
        bbox = union_bbox(bboxes)
        if bbox:
            region_counter += 1
            regions.append({
                "region_id": f"{page_id}_R{region_counter:02d}",
                "bbox": bbox,
                "classification": "footer",
                "description": "Page footer (bottom of page)",
                "text_words": [{
                    "text": w.get("text", ""),
                    "bbox": w.get("bbox"),
                    "conf_tesseract": w.get("conf_tesseract", w.get("conf", 0.0)),
                    "verified_by_vision": False,
                } for w in footer_words],
                "symbols": [],
                "drawings": [],
                "uncertain": [],
            })

    # 2c) Body-Regions: jede Blank-Region mit ihren Words + Glyphs
    used_words = set()
    for blank, glyphs_in in blank_with_glyphs:
        bbox_b = [blank["left"], blank["top"], blank["width"], blank["height"]]
        # Words in dieser Region (Text-inside-Blank)
        region_words = []
        for i, w in enumerate(body_words):
            if i in used_words:
                continue
            w_bbox = w.get("bbox")
            if not w_bbox or len(w_bbox) != 4:
                continue
            if bbox_contains(bbox_b, w_bbox, threshold=0.5):
                region_words.append(w)
                used_words.add(i)
        # Falls keine Words: klassifiziere als blank_region
        # Falls Words: klassifiziere als mixed_media (Text+Symbol)
        if region_words or glyphs_in:
            region_counter += 1
            bbox = union_bbox([bbox_b] +
                              [w["bbox"] for w in region_words
                               if len(w.get("bbox", [])) == 4] +
                              [g["crop_bbox"] for g in glyphs_in
                               if g.get("crop_bbox") and len(g["crop_bbox"]) == 4])
            # Classification
            if region_words and glyphs_in:
                cls = "mixed_media"
            elif region_words:
                cls = "text_in_blank"
            elif glyphs_in:
                # Vision-beschriebenes Symbol
                v = glyphs_in[0]
                cls = v.get("kind", "blank_region")
            else:
                cls = "blank_region"

            region = {
                "region_id": f"{page_id}_R{region_counter:02d}",
                "bbox": bbox,
                "classification": cls,
                "description": "",
                "text_words": [{
                    "text": w.get("text", ""),
                    "bbox": w.get("bbox"),
                    "conf_tesseract": w.get("conf_tesseract", w.get("conf", 0.0)),
                    "verified_by_vision": False,
                } for w in region_words],
                "symbols": [],
                "drawings": [],
                "uncertain": [],
            }

            # Vision-Symbole mit Cluster-Verknüpfung
            for g in glyphs_in:
                # Verwende pixel_crop_path (Original-Pixel-Crop) für Cluster-Lookup
                crop_path = g.get("pixel_crop_path") or g.get("crop_path", "")
                sym = {
                    "symbol_id": -1,  # wird unten gesetzt (synth_id falls unmatched)
                    "cluster_id": "GEOM_UNMATCHED_0000",
                    "vision_kind": g.get("kind", "unknown"),
                    "vision_description": g.get("description", ""),
                    "unicode_codepoint": g.get("unicode_codepoint", ""),
                    "vision_confidence": g.get("confidence", 0.0),
                    "page": page_id,
                    "bbox": g.get("crop_bbox"),
                    "crop_path": crop_path,  # IMMER setzen
                }
                # Lookup Cluster via crop_path
                if crop_path and symbols_index:
                    # Symbols_Index ist Liste pro Symbol
                    for sidx in symbols_index.get("symbols", []):
                        for occ in sidx.get("occurrences", []):
                            if occ.get("crop_path") and Path(occ["crop_path"]).name == Path(crop_path).name:
                                sym["symbol_id"] = sidx.get("symbol_id", 0)
                                sym["cluster_id"] = sidx.get("cluster_id", "GEOM_UNMATCHED_0000")
                                sym["first_appearance"] = (crop_path == sidx.get("representative_crop_path"))
                                break
                # Falls immer noch -1: synthetische ID vergeben
                if sym["symbol_id"] == -1:
                    sym["symbol_id"] = synth_id_counter
                    synth_id_counter += 1
                region["symbols"].append(sym)

            regions.append(region)

    # 2d) Leftover-Glyphs (nicht in Pixel-Blank-Liste)
    if leftover_glyphs:
        for g in leftover_glyphs:
            g_bbox = g.get("crop_bbox")
            if not g_bbox or len(g_bbox) != 4:
                continue
            region_counter += 1
            regions.append({
                "region_id": f"{page_id}_R{region_counter:02d}",
                "bbox": g_bbox,
                "classification": g.get("kind", "vision_symbol"),
                "description": g.get("description", ""),
                "text_words": [],
                "symbols": [{
                    "symbol_id": synth_id_counter,
                    "cluster_id": "GEOM_UNMATCHED_0000",
                    "vision_kind": g.get("kind", "unknown"),
                    "vision_description": g.get("description", ""),
                    "unicode_codepoint": g.get("unicode_codepoint", ""),
                    "vision_confidence": g.get("confidence", 0.0),
                    "page": page_id,
                    "bbox": g_bbox,
                    "crop_path": g.get("pixel_crop_path") or g.get("crop_path", ""),
                }],
                "drawings": [],
                "uncertain": [],
            })

    # 2e) Verbleibende Body-Words (nicht zugeordnet)
    remaining = [body_words[i] for i in range(len(body_words)) if i not in used_words]
    if remaining:
        # Sortiere nach (top, left) und gruppiere in Lines (gleicher top ±10)
        remaining.sort(key=lambda w: (w.get("bbox", [0,0,0,0])[1],
                                      w.get("bbox", [0,0,0,0])[0]))
        lines = []
        cur_line = []
        cur_top = -1
        for w in remaining:
            b = w.get("bbox", [0,0,0,0])
            if not b or len(b) < 4:
                continue
            if cur_top < 0 or abs(b[1] - cur_top) < 10:
                cur_line.append(w)
                cur_top = b[1] if cur_top < 0 else (cur_top + b[1]) / 2
            else:
                lines.append(cur_line)
                cur_line = [w]
                cur_top = b[1]
        if cur_line:
            lines.append(cur_line)
        for line in lines:
            region_counter += 1
            bboxes = [w["bbox"] for w in line if len(w.get("bbox", [])) == 4]
            bbox = union_bbox(bboxes)
            if not bbox:
                continue
            regions.append({
                "region_id": f"{page_id}_R{region_counter:02d}",
                "bbox": bbox,
                "classification": "text_line",
                "description": f"Text line: {' '.join(w.get('text','') for w in line[:5])}",
                "text_words": [{
                    "text": w.get("text", ""),
                    "bbox": w.get("bbox"),
                    "conf_tesseract": w.get("conf_tesseract", w.get("conf", 0.0)),
                    "verified_by_vision": False,
                } for w in line],
                "symbols": [],
                "drawings": [],
                "uncertain": [],
            })

    # 2f) Colored-Regions (separate, da anders als Blanks)
    for cr in colored_regions:
        bbox_c = [cr["left"], cr["top"], cr["width"], cr["height"]]
        region_counter += 1
        regions.append({
            "region_id": f"{page_id}_R{region_counter:02d}",
            "bbox": bbox_c,
            "classification": "colored_region",
            "description": f"Colored region, area={cr.get('area_px', 0)}",
            "text_words": [],
            "symbols": [],
            "drawings": [],
            "uncertain": [],
        })

    # 3) Page-Output
    page_out = {
        "page_id": page_id,
        "image_size": img_size,
        "source_pixel": str(pixel_path.name),
        "source_vision": str(vision_page_path.name) if vision_page_path.exists() else None,
        "n_regions": len(regions),
        "n_text_words": len(words),
        "n_blank_regions": len(blank_regions),
        "n_colored_regions": len(colored_regions),
        "n_glyphs_vision": len(glyphs),
        "regions": regions,
    }

    # Add Vision-Description (page-level)
    if vision_page and not (isinstance(vision_page, dict) and "$schema" in vision_page):
        page_out["vision_description"] = vision_page.get("description", "")
        page_out["vision_classification"] = vision_page.get("classification", "")

    return page_out, synth_id_counter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pixel", type=Path, required=True)
    ap.add_argument("--vision", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--symbols", type=Path, default=None,
                    help="Optional: bbox/symbols_global_<TS>/symbols_index.json")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    symbols_index = {}
    if args.symbols and args.symbols.exists():
        symbols_index = json.loads(args.symbols.read_text())
        print(f"Loaded symbols_index with {len(symbols_index.get('symbols', []))} symbols")

    # Total symbol_id counter for unmatched symbols
    next_synth_id = 1000000  # synthetic IDs for unmatched (>= 1M)

    for page_num in range(1, 24):
        page_id = f"p{page_num:02d}"
        try:
            page_data, next_synth_id = process_page(
                page_num, args.pixel, args.vision, symbols_index, next_synth_id)
            out_path = args.out / f"{page_id}.json"
            out_path.write_text(json.dumps(page_data, indent=2, ensure_ascii=False))
            print(f"  {page_id}: {page_data.get('n_regions', 0)} regions, "
                  f"{page_data.get('n_text_words', 0)} words, "
                  f"{page_data.get('n_glyphs_vision', 0)} glyphs")
        except Exception as e:
            print(f"  {page_id}: EXC {e}")
            import traceback
            traceback.print_exc()

    print(f"\nWrote 23 merged page files to {args.out}")


if __name__ == "__main__":
    main()
