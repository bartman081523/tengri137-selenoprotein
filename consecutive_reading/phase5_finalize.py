#!/usr/bin/env python3
"""
Phase 5 — Finalisieren.

Liest:
  - bbox/pages_merged_<TS>/p{NN}.json
  - bbox/symbols_global_<TS>/symbols_index.json

Schreibt:
  - bbox/final_<TS>/p{NN}.json   (finale pro-Seite-JSONs)
  - bbox/final_<TS>/symbols_index.json
  - Tengri137_detailed_<TS/      (Top-Level-Kopie)
"""
import argparse
import json
import shutil
from pathlib import Path

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=Path, required=True)
    ap.add_argument("--symbols", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--toplevel", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    args.toplevel.mkdir(parents=True, exist_ok=True)

    # Copy each per-page JSON
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        src = args.pages / f"{page_id}.json"
        if not src.exists():
            print(f"  {page_id}: SKIP (no merged data)")
            continue
        # Validate: ensure all required fields present
        d = json.loads(src.read_text())
        for k in ["page", "image_size", "text_words", "symbols", "drawings",
                  "digits", "formulas", "mixed_media_regions", "uncertain"]:
            if k not in d:
                d[k] = [] if k != "page" and k != "image_size" else (
                    page_id if k == "page" else [0, 0])
        (args.out / f"{page_id}.json").write_text(
            json.dumps(d, indent=2, ensure_ascii=False))
        # copy to toplevel
        shutil.copy(args.out / f"{page_id}.json", args.toplevel / f"{page_id}.json")
        print(f"  {page_id}: {len(d['text_words'])}w "
              f"{len(d['symbols'])}s {len(d['drawings'])}d "
              f"{len(d['digits'])}n {len(d['formulas'])}f "
              f"{len(d['mixed_media_regions'])}m")

    # Copy symbols index
    sym_src = args.symbols / "symbols_index.json"
    if sym_src.exists():
        shutil.copy(sym_src, args.out / "symbols_index.json")
        shutil.copy(sym_src, args.toplevel / "symbols_index.json")
        idx = json.loads(sym_src.read_text())
        print(f"\nSymbol index: {idx.get('total_symbols', 0)} symbols")


if __name__ == "__main__":
    main()
