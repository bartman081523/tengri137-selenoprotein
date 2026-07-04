#!/usr/bin/env python3
"""
Consolidate all per-page data sources into one master JSON per page.
Reads from:
  - bbox/pages/p{NN}.json  (tesseract words + blank/color components)
  - bbox/vision_$TS/p{NN}.json  (claude-vision structured output)
  - Tengri137_Full_Notes  (line-by-line original transkript)
  - Tengri137_raw_text.txt  (reconstructed full text)

Writes: bbox/consolidated/p{NN}.json
"""
import json
import re
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PAGES_DIR = ROOT / "bbox" / "pages"
CONSOLIDATED_DIR = ROOT / "bbox" / "consolidated"
CONSOLIDATED_DIR.mkdir(parents=True, exist_ok=True)

# Find latest vision run
vision_dirs = sorted((ROOT / "bbox").glob("vision_*"))
vision_dir = vision_dirs[-1] if vision_dirs else None
print(f"Using vision dir: {vision_dir.name if vision_dir else 'NONE'}")

raw_text = (ROOT / "Tengri137_raw_text.txt").read_text()


def extract_full_notes_page(page_num: int) -> list:
    """Read Tengri137_Full_Notes and return lines belonging to this page."""
    full = (ROOT / "Tengri137_Full_Notes").read_text().splitlines()
    # pages are separated by lines of '-' (length >= 10)
    page_blocks = []
    cur = []
    for line in full:
        if re.match(r"^-{10,}$", line):
            if cur:
                page_blocks.append(cur)
                cur = []
        else:
            cur.append(line)
    if cur:
        page_blocks.append(cur)
    # Map block index -> page number heuristically: first 4 blocks are pages 1-4,
    # then block 5 is "Page 17 - 23 Calculations -", etc. We'll just return
    # raw blocks; the user can match them up.
    return page_blocks


for i in range(1, 24):
    page_id = f"p{i:02d}"
    out = {"page": page_id, "sources": {}}

    # Tesseract + ink analysis
    pth = PAGES_DIR / f"{page_id}.json"
    if pth.exists():
        out["sources"]["ink_analysis"] = json.loads(pth.read_text())

    # Vision output
    if vision_dir:
        vp = vision_dir / f"{page_id}.json"
        if vp.exists():
            try:
                out["sources"]["vision"] = json.loads(vp.read_text())
            except json.JSONDecodeError:
                out["sources"]["vision"] = {"error": "invalid json"}

    (CONSOLIDATED_DIR / f"{page_id}.json").write_text(
        json.dumps(out, indent=2, ensure_ascii=False))
    n_ink = len(out["sources"].get("ink_analysis", {}).get("words", []))
    n_vision = len(out["sources"].get("vision", {}).get("symbols", [])) \
        if "vision" in out["sources"] else 0
    print(f"{page_id}: {n_ink} words, {n_vision} vision symbols")
