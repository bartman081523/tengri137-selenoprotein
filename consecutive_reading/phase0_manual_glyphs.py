#!/usr/bin/env python3
"""
phase0_manual_glyphs.py — V6 Phase 0: Manuelle Glyph-Isolation (DevMind).

V6 PIVOT: Gemini hat 30 Tengri-Referenz-Glyphen visuell identifiziert (Gemini-Glyph-Auftrag-Antwort.json).
Wir nutzen Gemini's KLASSIFIKATION + visuelle Beschreibungen, aber leiten die EXAKTEN Bbox-Koordinaten
aus dem V5-Substrat ab (meso-Components auf p01, 10-25x20-30 px).

Output: bbox/glyph_refs_20260706_V6/refs/glyphs.json + 30 PNG-Crops
        {
          "metadata": {
            "source": "Gemini-Glyph-Auftrag-Antwort.json",
            "page_used": "p01",
            "n_glyphs": 30,
            "method": "Gemini-Klassifikation + V5-Substrat-Koordinaten"
          },
          "glyphs": [
            {
              "glyph_id": "G01",
              "page_id": "p01",
              "bbox": [210, 425, 13, 25],  # Aus V5-Substrat
              "visual_description": "...",
              "type": "letter_like",
              "estimated_frequency_on_p01": 15,
              "similar_to_latin": "J",
              "template_path": "refs/G01.png"
            }
          ]
        }
"""
import argparse
import json
from pathlib import Path

from PIL import Image
import numpy as np


def find_closest_meso_component(gemini_glyph: dict, meso_components: list, max_distance: int = 100, used_ids: set = None) -> dict:
    """Finde das nächste V5-meso-Component zum Gemini-Glyph (basierend auf bbox-Center).
    used_ids: Set von bereits zugewiesenen Component-IDs (für eindeutige Zuordnung).
    """
    gx = gemini_glyph["bbox"][0] + gemini_glyph["bbox"][2] / 2
    gy = gemini_glyph["bbox"][1] + gemini_glyph["bbox"][3] / 2

    if used_ids is None:
        used_ids = set()

    best = None
    best_dist = float("inf")
    for c in meso_components:
        if c["id"] in used_ids:
            continue
        cx = c["bbox"][0] + c["bbox"][2] / 2
        cy = c["bbox"][1] + c["bbox"][3] / 2
        d = ((gx - cx) ** 2 + (gy - cy) ** 2) ** 0.5
        if d < best_dist and d < max_distance:
            best_dist = d
            best = c

    return best


def extract_crop(png_path: Path, bbox: list, padding: int = 5) -> np.ndarray:
    """Extrahiere Glyph-Crop mit Padding."""
    img = Image.open(png_path).convert("L")
    arr = np.array(img)
    x, y, w, h = bbox
    x0 = max(0, x - padding)
    y0 = max(0, y - padding)
    x1 = min(arr.shape[1], x + w + padding)
    y1 = min(arr.shape[0], y + h + padding)
    crop = arr[y0:y1, x0:x1]
    return crop


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gemini-response", type=Path, required=True,
                    help="Gemini-Glyph-Auftrag-Antwort.json")
    ap.add_argument("--v5-substrat", type=Path, required=True,
                    help="bbox/substrat_20260705_V5/p01.json")
    ap.add_argument("--page-png", type=Path, required=True,
                    help="pages_png/page-01.png")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/glyph_refs_20260706_V6/")
    ap.add_argument("--max-distance", type=int, default=100,
                    help="Max Pixel-Distanz für Gemini→V5-Match")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    refs_dir = args.out / "refs"
    refs_dir.mkdir(exist_ok=True)

    # 1. Lade Gemini-Antwort
    gemini = json.loads(args.gemini_response.read_text())
    gemini_glyphs = gemini["glyphs"]

    # 2. Lade V5-Substrat (meso-Components)
    substrat = json.loads(args.v5_substrat.read_text())
    meso_components = [c for c in substrat["components"] if c.get("level") == "meso"]
    print(f"Gemini-Glyphen: {len(gemini_glyphs)}")
    print(f"V5-meso-Components auf p01: {len(meso_components)}")

    # 3. Pro Gemini-Glyph: finde nächstes V5-Component + extrahiere Crop
    matched = []
    unmatched = []
    used_v5_ids = set()  # Für eindeutige Zuordnung
    for g in gemini_glyphs:
        match = find_closest_meso_component(g, meso_components, max_distance=args.max_distance, used_ids=used_v5_ids)
        if match is None:
            print(f"  {g['glyph_id']}: KEIN MATCH (>{args.max_distance}px oder alle verbraucht)")
            unmatched.append(g)
            continue

        used_v5_ids.add(match["id"])

        # Nutze V5-bbox als exakte Koordinaten
        bbox = match["bbox"]
        crop = extract_crop(args.page_png, bbox, padding=5)
        crop_path = refs_dir / f"{g['glyph_id']}.png"
        Image.fromarray(crop).save(crop_path)

        matched_glyph = {
            **g,
            "bbox": bbox,  # Überschreibe Gemini-Schätzung mit V5-bbox
            "template_path": f"refs/{g['glyph_id']}.png",
            "v5_component_id": match["id"],
            "v5_fill_ratio": match.get("fill_ratio", 0.0),
            "v5_size_px": match.get("size_px", 0),
        }
        matched.append(matched_glyph)
        dist = ((g['bbox'][0]+g['bbox'][2]/2-(bbox[0]+bbox[2]/2))**2 + (g['bbox'][1]+g['bbox'][3]/2-(bbox[1]+bbox[3]/2))**2)**0.5
        print(f"  {g['glyph_id']}: matched v5-{match['id']} (dist={dist:.0f}px), bbox={bbox}, crop saved")

    # 4. Output
    out_data = {
        "metadata": {
            "source": args.gemini_response.name,
            "v5_substrat": str(args.v5_substrat),
            "page_used": gemini["metadata"]["page_used"],
            "n_glyphs": len(matched),
            "n_unmatched": len(unmatched),
            "method": "Gemini-Klassifikation + V5-Substrat-Koordinaten (meso-Components)",
            "max_distance_px": args.max_distance,
            "tenri_alphabet_hypothesis": gemini.get("tenri_alphabet_hypothesis", {}),
        },
        "glyphs": matched,
        "unmatched": [g["glyph_id"] for g in unmatched],
    }
    out_path = args.out / "glyphs.json"
    out_path.write_text(json.dumps(out_data, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")
    print(f"Matched: {len(matched)}/{len(gemini_glyphs)}")
    print(f"Unmatched: {len(unmatched)} ({[g['glyph_id'] for g in unmatched]})")


if __name__ == "__main__":
    main()
