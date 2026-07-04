#!/usr/bin/env python3
"""
Re-run Glyph-Vision nur — ohne die page.json neu zu generieren.
"""
import json
import subprocess
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PNG_DIR = ROOT / "pages_png"
PIXEL_DIR = ROOT / "bbox" / "pages_pixel_20260704_075228"
VISION_DIR = ROOT / "bbox" / "vision_qa_20260704_075228"
SCHEMAS_DIR = ROOT / "bbox" / "schemas_20260704_075228"


def shrink(src, dst, max_side=512, quality=85):
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


def process_page_glyphs(page_num: int, n_top: int = 5):
    page_id = f"p{page_num:02d}"
    page_png = PNG_DIR / f"page-{page_num:02d}.png"
    pixel_path = PIXEL_DIR / f"{page_id}.json"
    page_dir = VISION_DIR / page_id
    glyph_dir = page_dir / f"{page_id}_glyphs"
    glyph_dir.mkdir(parents=True, exist_ok=True)

    if not pixel_path.exists():
        return f"{page_id}: NO PIXEL DATA"

    pixel = json.loads(pixel_path.read_text())
    blanks = sorted(pixel.get("blank_regions", []),
                    key=lambda x: -x.get("area_px", 0))[:n_top]
    results = []
    for j, b in enumerate(blanks):
        bbox = [b["left"], b["top"], b["width"], b["height"]]
        crop_path = glyph_dir / f"g{j:02d}_crop.png"
        crop_image(page_png, crop_path, bbox)
        with tempfile.TemporaryDirectory() as tmp:
            small = Path(tmp) / f"g{j:02d}.jpg"
            shrink(crop_path, small, max_side=512)
            res = run_vision(
                small, SCHEMAS_DIR / "small_glyph.schema.json",
                prompt=("Klassifiziere dieses einzelne Glyph. "
                        "Welche Unicode-Zeichen, geometrische Figuren oder "
                        "Schriftzeichen sind darin zu sehen? "
                        "Wenn unklar, gib confidence < 0.5 an.")
            )
            res["crop_bbox"] = bbox
            res["crop_path"] = str(crop_path.relative_to(ROOT))
            (glyph_dir / f"g{j:02d}.json").write_text(
                json.dumps(res, indent=2, ensure_ascii=False))
            results.append({"index": j, "bbox": bbox,
                            "kind": res.get("kind"),
                            "description": (res.get("description") or "")[:80],
                            "confidence": res.get("confidence")})

    # Update summary
    summary_path = page_dir / f"{page_id}_summary.json"
    summary = {
        "page": page_id,
        "page_vision_status": "ok",
        "glyphs_processed": len(results),
        "glyphs": results,
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return f"{page_id}: {len(results)} glyphs"


def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        futs = {pool.submit(process_page_glyphs, p, 5): p
                for p in range(1, 24)}
        for fut in as_completed(futs):
            try:
                msg = fut.result()
                print(f"  {msg}")
            except Exception as e:
                print(f"  EXC: {e}")


if __name__ == "__main__":
    main()
