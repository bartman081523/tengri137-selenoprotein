#!/usr/bin/env python3
"""
Phase 2 v2 — Vision-Quercheck pro Seite (mit Bug-Fix für hartkodierten Pfad).

Unterschiede zu phase2_vision.py:
- --pixel Argument wird sauber durchgereicht (nicht mehr hartkodiert)
- N-Top-Glyphs ist als Argument konfigurierbar (default: ALLE Crops der Seite)
- Bessere Fehlerbehandlung für kaputte Vision-Outputs (Schemadefinitionen werden erkannt)
- 13 bereits gute Pages können optional übersprungen werden (--skip-existing)

Liest:
  - pages_png/page-NN.png  (Original 150 DPI)
  - bbox/pages_pixel_<TS>/p{NN}.json  (Phase 1, für Crop-Auswahl)

Schreibt:
  - bbox/vision_qa_<TS>/p{NN}/{page_id}_page.json      (Großbild, page.schema)
  - bbox/vision_qa_<TS>/p{NN}/{page_id}_glyphs/g{NNN}_crop.png + g{NNN}.json
  - bbox/vision_qa_<TS>/p{NN}/{page_id}_summary.json   (Index)

Verwendet: claude-vision-json (in ~/.local/bin/)
"""
import argparse
import json
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
               prompt: str = None, max_retries: int = 3,
               timeout: int = 240) -> dict:
    for attempt in range(max_retries):
        try:
            cmd = [
                "claude-vision-json", str(image_path),
                "--schema", str(schema_path),
            ]
            if prompt:
                cmd.extend(["--prompt", prompt])
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=timeout,
            )
            if result.returncode != 0:
                raise RuntimeError(f"rc={result.returncode}: "
                                   f"{result.stderr[:200]}")
            d = json.loads(result.stdout)
            # Detect schema-leaking: when vision returns the schema definition
            # instead of data, keys are "$schema", "type", "required", "properties"
            if isinstance(d, dict) and "$schema" in d and "type" in d and "properties" in d:
                raise ValueError("vision returned schema definition, not data")
            return d
        except (subprocess.TimeoutExpired, json.JSONDecodeError, RuntimeError, ValueError) as e:
            if attempt == max_retries - 1:
                return {"error": str(e), "_failed_after_retries": True}
            time.sleep(2 ** attempt)
    return {"error": "max retries exceeded"}


def process_page(page_num: int, pixel_dir: Path, schemas_dir: Path,
                 out_dir: Path, n_top_glyphs: int):
    page_id = f"p{page_num:02d}"
    page_png = PNG_DIR / f"page-{page_num:02d}.png"
    page_dir = out_dir / page_id
    page_dir.mkdir(parents=True, exist_ok=True)
    glyph_dir = page_dir / f"{page_id}_glyphs"
    glyph_dir.mkdir(parents=True, exist_ok=True)

    # 2a: full-page vision
    page_vision_status = "ok"
    full_result = {}
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
        if "error" in full_result:
            page_vision_status = "error"
        (page_dir / f"{page_id}_page.json").write_text(
            json.dumps(full_result, indent=2, ensure_ascii=False))

    # Load pixel data to find blanks
    pixel_path = pixel_dir / f"{page_id}.json"
    pixel_data = json.loads(pixel_path.read_text()) if pixel_path.exists() else {}

    # 2b: top-N (or all) blank regions as glyph crops
    blanks = sorted(pixel_data.get("blank_regions", []),
                    key=lambda x: -x.get("area_px", 0))
    if n_top_glyphs > 0:
        blanks = blanks[:n_top_glyphs]
    # Also include colored regions as crops
    colored = pixel_data.get("colored_regions", [])
    glyph_results = []
    for j, b in enumerate(blanks):
        bbox = [b["left"], b["top"], b["width"], b["height"]]
        crop_path = glyph_dir / f"g{j:03d}_blank.png"
        try:
            crop_image(page_png, crop_path, bbox)
        except Exception as e:
            print(f"  {page_id}/g{j:03d}_blank: crop failed ({e})")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            small = Path(tmp) / f"g{j:03d}.jpg"
            shrink(crop_path, small, max_side=512)
            res = run_vision(
                small, schemas_dir / "small_glyph.schema.json",
                prompt=("Klassifiziere dieses einzelne Glyph. "
                        "Welche Unicode-Zeichen, geometrische Figuren oder "
                        "Schriftzeichen sind darin zu sehen? "
                        "Wenn unklar, gib confidence < 0.5 an.")
            )
            res["crop_bbox"] = bbox
            try:
                res["crop_path"] = str(crop_path.relative_to(ROOT))
            except ValueError:
                res["crop_path"] = str(crop_path)
            # Auch: Verweis auf Original-Pixel-Blank-Crop (für Phase 3/4b-Verknüpfung)
            res["pixel_crop_path"] = f"bbox/crops/{page_id}_blank_{j:03d}.png"
            res["kind_crop"] = "blank"
            (glyph_dir / f"g{j:03d}.json").write_text(
                json.dumps(res, indent=2, ensure_ascii=False))
            glyph_results.append({"index": j, "kind_crop": "blank", "bbox": bbox,
                                  "result_summary": {
                                      "kind": res.get("kind"),
                                      "description": res.get("description"),
                                      "confidence": res.get("confidence"),
                                  }})

    for j, c in enumerate(colored):
        bbox = [c["left"], c["top"], c["width"], c["height"]]
        crop_path = glyph_dir / f"g{len(blanks)+j:03d}_color.png"
        try:
            crop_image(page_png, crop_path, bbox)
        except Exception as e:
            print(f"  {page_id}/color_{j}: crop failed ({e})")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            small = Path(tmp) / f"g{len(blanks)+j}.jpg"
            shrink(crop_path, small, max_side=512)
            res = run_vision(
                small, schemas_dir / "small_glyph.schema.json",
                prompt=("Klassifiziere dieses farbige Element. "
                        "Welche Unicode-Zeichen, Formen oder Symbole sind zu sehen? "
                        "Wenn unklar, gib confidence < 0.5 an.")
            )
            res["crop_bbox"] = bbox
            try:
                res["crop_path"] = str(crop_path.relative_to(ROOT))
            except ValueError:
                res["crop_path"] = str(crop_path)
            # Original-Pixel-Color-Crop-Pfad
            res["pixel_crop_path"] = f"bbox/crops/{page_id}_color_{j:03d}.png"
            res["kind_crop"] = "color"
            (glyph_dir / f"g{len(blanks)+j:03d}.json").write_text(
                json.dumps(res, indent=2, ensure_ascii=False))
            glyph_results.append({"index": len(blanks)+j, "kind_crop": "color",
                                  "bbox": bbox,
                                  "result_summary": {
                                      "kind": res.get("kind"),
                                      "description": res.get("description"),
                                      "confidence": res.get("confidence"),
                                  }})

    summary = {
        "page": page_id,
        "page_vision_status": page_vision_status,
        "glyphs_processed": len(glyph_results),
        "n_blank_crops": len(blanks),
        "n_color_crops": len(colored),
        "glyphs": glyph_results,
    }
    (page_dir / f"{page_id}_summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False))
    return page_id, page_vision_status, len(glyph_results)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pixel", type=Path, required=True,
                    help="bbox/pages_pixel_<TS>/ with p{NN}.json")
    ap.add_argument("--schemas", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--n-top-glyphs", type=int, default=999,
                    help="Top-N biggest blanks per page; 0 = skip, 999 = all")
    ap.add_argument("--skip-existing", action="store_true",
                    help="Skip pages that already have a complete vision output")
    ap.add_argument("--only-broken", action="store_true",
                    help="Re-run only pages whose vision output starts with '{\"$schema\"'")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    pages = list(range(1, 24))
    if args.skip_existing or args.only_broken:
        pages = [p for p in pages if (args.out / f"p{p:02d}" / f"p{p:02d}_page.json").exists()
                 and not (args.only_broken and _looks_broken(args.out / f"p{p:02d}" / f"p{p:02d}_page.json"))]
        if args.only_broken:
            pages = [p for p in range(1, 24) if _looks_broken(args.out / f"p{p:02d}" / f"p{p:02d}_page.json")]

    print(f"Processing {len(pages)} pages with {args.workers} workers...")
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futs = {
            pool.submit(process_page, p, args.pixel, args.schemas, args.out,
                        args.n_top_glyphs): p
            for p in pages
        }
        for fut in as_completed(futs):
            p = futs[fut]
            try:
                page_id, status, n = fut.result()
                print(f"  {page_id}: {status} ({n} glyphs)")
            except Exception as e:
                print(f"  p{p:02d}: EXC {e}")


def _looks_broken(path: Path) -> bool:
    if not path.exists():
        return True
    try:
        d = json.loads(path.read_text())
        if isinstance(d, dict) and "$schema" in d and "type" in d:
            return True
    except Exception:
        return True
    return False


if __name__ == "__main__":
    main()
