#!/usr/bin/env python3
"""
Builds per-page contact sheets (mosaics) of all crops, so a human can
visually inspect what was detected as "blank" or "colored" regions
without opening 800+ individual files.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
CROP_DIR = ROOT / "bbox" / "crops"
INDEX = ROOT / "bbox" / "crops_index.json"
SHEET_DIR = ROOT / "bbox" / "contact_sheets"
SHEET_DIR.mkdir(parents=True, exist_ok=True)

THUMB = 80
COLS = 12
PAD = 6

def main():
    crops = json.loads(INDEX.read_text())
    by_page = {}
    for c in crops:
        by_page.setdefault(c["page"], []).append(c)

    for page, lst in sorted(by_page.items()):
        # Sort by kind then idx
        lst.sort(key=lambda x: (x["kind"], x["idx"]))
        n = len(lst)
        rows = (n + COLS - 1) // COLS
        sheet_w = COLS * (THUMB + PAD) + PAD
        sheet_h = rows * (THUMB + PAD + 16) + PAD
        sheet = Image.new("RGB", (sheet_w, sheet_h), "white")
        draw = ImageDraw.Draw(sheet)
        for k, c in enumerate(lst):
            r, k2 = divmod(k, COLS)
            x = PAD + r * (THUMB + PAD) + k2 * (THUMB + PAD)  # bug: should be (col, row)
            # correct: r is row, k2 is col
            x = PAD + k2 * (THUMB + PAD)
            y = PAD + r * (THUMB + PAD + 16)
            try:
                im = Image.open(ROOT / c["path"])
                im.thumbnail((THUMB, THUMB), Image.LANCZOS)
                sheet.paste(im, (x, y))
            except Exception as e:
                pass
            draw.text((x, y + THUMB + 1), f"{c['kind'][:3]}{c['idx']:02d}", fill="black")
        out = SHEET_DIR / f"{page}_sheet.png"
        sheet.save(out)
        print(f"{page}: {n} crops -> {out.name}")


if __name__ == "__main__":
    main()
