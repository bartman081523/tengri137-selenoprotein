#!/usr/bin/env python3
"""
Phase 2 — Vision-Quercheck pro Seite.

Liest:
  - pages_png/page-NN.png  (Original 150 DPI)
  - bbox/pages_pixel_<TS>/p{NN}.json  (Phase 1, für Crop-Auswahl)

Schreibt:
  - bbox/vision_qa_<TS>/p{NN}_page.json      (Großbild, page.schema)
  - bbox/vision_qa_<TS>/p{NN}_glyphs/g00.json ... gNN.json
  - bbox/vision_qa_<TS>/p{NN}_summary.json   (Index)

Verwendet: claude-vision-json (in ~/.local/bin/)
"""
import argparse
import json
import os
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PNG_DIR = ROOT / "pages_png"


def shrink(src, dst, max_side=1024, quality=85):
    subprocess.run(
        ["magick", str(src), "-resize", f"{max_side}x{max_side}>",
         "-quality", str(quality), str(dst)],
        check=True,
    )


def crop_image(src, dst, bbox, pad=15):
    from PIL import Image
    img = Image.open(src)
    x0 = max(0, bbox[0] - pad)
    y0 = max(0, bbox[1] - pad)
    x1 = min(img.size[0], bbox[0] + bbox[2] + pad)
    y1 = min(img.size[1], bbox[1] + bbox[3] + pad)
    img.crop((x0, y0, x1, y1)).save(dst)


def run_vision(image_path: Path, schema_path: Path,
               prompt: str = None, max_retries: int = 3) -> dict:
    for attempt in range(max_retries):
        try:
            cmd = [
                "claude-vision-json", str(image_path),
                "--schema", str(schema_path),
            ]
            if prompt:
                cmd.extend(["--prompt", prompt])
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=180,
            )
            if result.returncode != 0:
                raise RuntimeError(f"rc={result.returncode}: "
                                   f"{result.stderr[:200]}")
            return json.loads(result.stdout)
        except (subprocess.TimeoutExpired, json.JSONDecodeError, RuntimeError) as e:
            if attempt == max_retries - 1:
                return {"error": str(e)}
            time.sleep(2 ** attempt)
    return {"error": "max retries exceeded"}


def process_page(page_num: int, schemas_dir: Path, out_dir: Path,
                 n_top_glyphs: int = 5):
    page_id = f"p{page_num:02d}"
    page_png = PNG_DIR / f"page-{page_num:02d}.png"
    page_dir = out_dir / page_id
    page_dir.mkdir(parents=True, exist_ok=True)
    glyph_dir = page_dir / f"{page_id}_glyphs"
    glyph_dir.mkdir(parents=True, exist_ok=True)

    # 2a: full-page vision
    with tempfile.TemporaryDirectory() as tmp:
        full_jpg = Path(tmp) / f"{page_id}.jpg"
        shrink(page_png, full_jpg)
        prompt = (
            "Beschreibe diese Folie möglichst genau. "
            "Identifiziere Textblöcke (mit Position), farbigen Text, "
            "Zeichnungen, Symbole/Sigille, Formeln und Mixed-Media-Bereiche "
            "(Regionen mit Text+Symbol+Zeichnung). Liste auch auf, was du "
            "nicht entziffern kannst."
        )
        full_result = run_vision(full_jpg, schemas_dir / "page.schema.json", prompt)
        (page_dir / f"{page_id}_page.json").write_text(
            json.dumps(full_result, indent=2, ensure_ascii=False))

    # Load pixel data to find top blanks
    pixel_path = ROOT / "bbox" / "pages_pixel" / "20260704_075228" / f"{page_id}.json"
    if not pixel_path.exists():
        # Fallback: find latest
        candidates = sorted((ROOT / "bbox" / "pages_pixel").glob("*/"))
        if candidates:
            pixel_path = candidates[-1] / f"{page_id}.json"
    pixel_data = json.loads(pixel_path.read_text()) if pixel_path.exists() else {}

    # 2b: top-N biggest blank regions as glyph crops
    blanks = sorted(pixel_data.get("blank_regions", []),
                    key=lambda x: -x.get("area_px", 0))[:n_top_glyphs]
    glyph_results = []
    for j, b in enumerate(blanks):
        bbox = [b["left"], b["top"], b["width"], b["height"]]
        crop_path = glyph_dir / f"g{j:02d}_crop.png"
        crop_image(page_png, crop_path, bbox)
        with tempfile.TemporaryDirectory() as tmp:
            small = Path(tmp) / f"g{j:02d}.jpg"
            shrink(crop_path, small, max_side=512)
            res = run_vision(
                small, schemas_dir / "small_glyph.schema.json",
                prompt=("Klassifiziere dieses einzelne Glyph. "
                        "Welche Unicode-Zeichen, geometrische Figuren oder "
                        "Schriftzeichen sind darin zu sehen? "
                        "Wenn unklar, gib confidence < 0.5 an.")
            )
            res["crop_bbox"] = bbox
            res["crop_path"] = str(crop_path.relative_to(ROOT))
            (glyph_dir / f"g{j:02d}.json").write_text(
                json.dumps(res, indent=2, ensure_ascii=False))
            glyph_results.append({"index": j, "bbox": bbox,
                                  "result_summary": {
                                      "kind": res.get("kind"),
                                      "description": res.get("description"),
                                      "confidence": res.get("confidence"),
                                  }})

    summary = {
        "page": page_id,
        "page_vision_status": "ok" if "error" not in full_result else "error",
        "glyphs_processed": len(glyph_results),
        "glyphs": glyph_results,
    }
    (page_dir / f"{page_id}_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False))
    return page_id, "ok" if "error" not in full_result else "error"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pixel", type=Path, required=True,
                    help="bbox/pages_pixel_<TS>/ with p{NN}.json")
    ap.add_argument("--schemas", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--n-top-glyphs", type=int, default=5)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    pages = list(range(1, 24))
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {
            pool.submit(process_page, p, args.schemas, args.out,
                        args.n_top_glyphs): p
            for p in pages
        }
        for fut in as_completed(futs):
            p = futs[fut]
            try:
                page_id, status = fut.result()
                print(f"  p{p:02d}: {status}")
            except Exception as e:
                print(f"  p{p:02d}: EXC {e}")


if __name__ == "__main__":
    main()
