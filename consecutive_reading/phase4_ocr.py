#!/usr/bin/env python3
"""
phase4_ocr.py — Selektive OCR (DevMind).

V5 PIVOT: V4 hat Tesseract auf ganze Zeilen angewendet, was lateinische Buchstaben
in Tengri-Glyphen halluzinierte. V5 wendet Tesseract NUR auf Bereiche an, die
NICHT von Tengri-Glyphen bedeckt sind (Komplement der Glyph-Bboxen).

Input:  bbox/substrat_20260705_V5/p{NN}.json
        bbox/alphabet_20260705_V5/alphabet.json
        bbox/components_20260704_V4/p{NN}/p{NN}_glyphs.json  (V4-Glyph-Bboxen)
        bbox/layout_20260705_V5/p{NN}.json  (Page-Layout-Typ)
        bbox/cryptanalysis_20260705_V5/crypto_report.json
Output: bbox/ocr_20260705_V5/p{NN}.json
        {
          "page_id": "p01",
          "layout_type": "fliesstext",
          "regions": [
            {
              "region_id": "p01_R1",
              "region_type": "fliesstext",
              "tengri_glyph_bboxes": [[x, y, w, h], ...],
              "ocr_applied": false,  # Fließtext → kein OCR
              "latin_tokens": []
            }
          ]
        }

WICHTIG:
  - fliesstext → KEIN OCR (alles ist Tengri)
  - magic_cube → Tesseract auf nicht-Glyph-Bereiche (erwartet: 9 Ziffern)
  - burumut_block → Tesseract auf nicht-Glyph-Bereiche (erwartet: lateinische Buchstaben)
  - chemie_struktur → Tesseract auf nicht-Glyph-Bereiche (erwartet: NH₂, N, C, H, O)
  - silhouette_formel → Tesseract auf nicht-Glyph-Bereiche
"""
import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

from PIL import Image


def has_tesseract() -> bool:
    """Prüfe, ob tesseract auf dem System verfügbar ist."""
    return shutil.which("tesseract") is not None


def run_tesseract(image_path: Path, lang: str = "eng", psm: int = 6) -> list:
    """Führe Tesseract auf einem Bild aus und gib Tokens + BBoxen zurück."""
    if not has_tesseract():
        return []
    try:
        result = subprocess.run(
            ["tesseract", str(image_path), "-", "-l", lang, "--psm", str(psm),
             "-c", "tessedit_create_tsv=1"],
            capture_output=True, text=True, timeout=30
        )
        # Parse TSV
        lines = result.stdout.strip().split("\n")
        if len(lines) < 2:
            return []
        header = lines[0].split("\t")
        tokens = []
        for line in lines[1:]:
            parts = line.split("\t")
            if len(parts) < len(header):
                continue
            row = dict(zip(header, parts))
            try:
                conf = float(row.get("conf", "-1"))
                text = row.get("text", "").strip()
                if conf < 60 or not text:
                    continue
                x = int(row.get("left", 0))
                y = int(row.get("top", 0))
                w = int(row.get("width", 0))
                h = int(row.get("height", 0))
                tokens.append({
                    "text": text,
                    "bbox": [x, y, w, h],
                    "conf": round(conf / 100.0, 3),
                    "source": "tesseract",
                })
            except (ValueError, KeyError):
                continue
        return tokens
    except (subprocess.TimeoutExpired, FileNotFoundError) as ex:
        print(f"  WARNUNG: tesseract failed: {ex}", file=sys.stderr)
        return []


def filter_tengri_regions(tokens: list, tengri_bboxes: list, iou_threshold: float = 0.1) -> list:
    """Filtere Tokens, deren BBox mit einer Tengri-Glyph-BBox überlappt (IoU > threshold)."""
    def iou(b1, b2):
        x1, y1, w1, h1 = b1
        x2, y2, w2, h2 = b2
        xa = max(x1, x2); ya = max(y1, y2)
        xb = min(x1 + w1, x2 + w2); yb = min(y1 + h1, y2 + h2)
        inter = max(0, xb - xa) * max(0, yb - ya)
        union = w1 * h1 + w2 * h2 - inter
        return inter / union if union > 0 else 0.0

    filtered = []
    for tok in tokens:
        overlaps_tengri = any(iou(tok["bbox"], tb) > iou_threshold for tb in tengri_bboxes)
        if not overlaps_tengri:
            filtered.append(tok)
    return filtered


def get_tengri_bboxes_from_v4(v4_components_dir: Path, page_id: str) -> list:
    """Lade Tengri-Glyph-BBoxen aus V4-Glyphs-Output."""
    glyphs_path = v4_components_dir / page_id / f"{page_id}_glyphs.json"
    if not glyphs_path.exists():
        return []
    data = json.loads(glyphs_path.read_text())
    return [g["bbox"] for g in data.get("glyphs", []) if g.get("bbox")]


def process_page(page_id: str, substrat_dir: Path, v4_components_dir: Path,
                 layout_dir: Path, pages_png_dir: Path, out_dir: Path):
    """Verarbeite eine einzelne Page."""
    substrat = json.loads((substrat_dir / f"{page_id}.json").read_text())
    layout = json.loads((layout_dir / f"{page_id}.json").read_text())
    layout_type = layout["layout_type"]

    tengri_bboxes = get_tengri_bboxes_from_v4(v4_components_dir, page_id)

    # PNG-Page laden
    png_path = pages_png_dir / f"page-{int(page_id[1:]):02d}.png"
    if not png_path.exists():
        print(f"  {page_id}: SKIP (kein PNG)", file=sys.stderr)
        return

    regions = []

    if layout_type == "fliesstext":
        # KEIN OCR — alles ist Tengri
        regions.append({
            "region_id": f"{page_id}_R1_FLIESSTEXT",
            "region_type": "fliesstext",
            "tengri_glyph_count": len(tengri_bboxes),
            "ocr_applied": False,
            "ocr_reason": "fliesstext: alles ist Tengri, kein lateinischer Text erwartet",
            "latin_tokens": [],
        })
    else:
        # Tesseract auf nicht-Tengri-Bereiche
        tokens = run_tesseract(png_path, lang="eng", psm=6)
        filtered = filter_tengri_regions(tokens, tengri_bboxes, iou_threshold=0.1)
        region = {
            "region_id": f"{page_id}_R1_{layout_type.upper()}",
            "region_type": layout_type,
            "tengri_glyph_count": len(tengri_bboxes),
            "ocr_applied": True,
            "ocr_total_tokens": len(tokens),
            "ocr_after_tengri_filter": len(filtered),
            "latin_tokens": filtered,
        }
        regions.append(region)

    out = {
        "page_id": page_id,
        "layout_type": layout_type,
        "layout_confidence": layout.get("confidence", 0.0),
        "n_tengri_glyphs": len(tengri_bboxes),
        "regions": regions,
    }
    (out_dir / f"{page_id}.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))

    n_latin = sum(len(r["latin_tokens"]) for r in regions)
    print(f"  {page_id}: {layout_type:<20} tengri={len(tengri_bboxes):3d}, "
          f"ocr_tokens={n_latin}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--substrat", type=Path, required=True)
    ap.add_argument("--v4-components", type=Path, required=True,
                    help="bbox/components_20260704_V4/ (für Tengri-Bboxen)")
    ap.add_argument("--layout", type=Path, required=True)
    ap.add_argument("--pages-png", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    if not has_tesseract():
        print("WARNUNG: tesseract nicht verfügbar — OCR wird übersprungen", file=sys.stderr)

    total_tengri = 0
    total_latin = 0
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        substrat_path = args.substrat / f"{page_id}.json"
        if not substrat_path.exists():
            print(f"  {page_id}: SKIP", file=sys.stderr)
            continue
        process_page(page_id, args.substrat, args.v4_components,
                     args.layout, args.pages_png, args.out)
        # Totals
        out_data = json.loads((args.out / f"{page_id}.json").read_text())
        total_tengri += out_data["n_tengri_glyphs"]
        total_latin += sum(len(r["latin_tokens"]) for r in out_data["regions"])

    print(f"\n[Phase 4] Total: {total_tengri} Tengri-Glyph-Bboxen, "
          f"{total_latin} lateinische Tokens (nach Tengri-Filter)")


if __name__ == "__main__":
    main()
