#!/usr/bin/env python3
"""
Phase 4 — Globaler Symbol-Index.

Indexierungs-Regel: Symbole werden in der Reihenfolge ihres **ersten
Auftretens im Fließtext** durchnummeriert, beginnend bei Seite 1,
Koordinate (0,0), oben-links nach unten-rechts lesend.

Liest:
  - bbox/pages_merged_<TS>/p{NN}.json

Schreibt:
  - bbox/symbols_global_<TS>/symbols_index.json
  - bbox/symbols_global_<TS>/p{NN}_symbols.json  (pro Seite nur die Symbole)
  - bbox/symbols_global_<TS>/p{NN}.json  (aktualisierte Seiten-JSON mit symbol_index)
"""
import argparse
import hashlib
import json
import re
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PNG_DIR = ROOT / "pages_png"


def get_crop_hash(page_num: int, bbox: list, size: int = 32) -> str:
    """Compute a perceptual hash of the symbol crop."""
    if not bbox or len(bbox) != 4:
        return ""
    img = Image.open(PNG_DIR / f"page-{page_num:02d}.png")
    x0 = max(0, bbox[0]); y0 = max(0, bbox[1])
    x1 = min(img.size[0], bbox[0] + bbox[2])
    y1 = min(img.size[1], bbox[1] + bbox[3])
    if x1 <= x0 or y1 <= y0:
        return ""
    crop = img.crop((x0, y0, x1, y1)).convert("L")
    # Pad to square
    w, h = crop.size
    side = max(w, h)
    sq = Image.new("L", (side, side), 255)
    sq.paste(crop, ((side - w) // 2, (side - h) // 2))
    sq = sq.resize((size, size), Image.LANCZOS)
    a = np.array(sq, dtype=float)
    avg = a.mean()
    bits = (a > avg).astype(np.uint8).flatten()
    h_int = 0
    for b in bits:
        h_int = (h_int << 1) | int(b)
    return hashlib.sha256(f"{h_int:0{2*len(bits)//8}x}".encode()).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pages", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Step 1: collect all symbol candidates per page, in reading order
    by_page = {}
    for i in range(1, 24):
        page_id = f"p{i:02d}"
        pf = args.pages / f"{page_id}.json"
        if not pf.exists():
            continue
        d = json.loads(pf.read_text())
        syms = d.get("symbols", [])
        # Sort by reading order: top first, then left
        def sort_key(s):
            bb = s.get("bbox") or [None, None, None, None]
            return (bb[1] if bb[1] is not None else 99999,
                    bb[0] if bb[0] is not None else 99999)
        syms_sorted = sorted(syms, key=sort_key)
        by_page[page_id] = syms_sorted

    # Step 2: iterate in reading order, assign symbol_index
    index = []  # list of {symbol_index, geometry_id, kind, first_*}
    seen_by_hash = {}  # crop_hash -> symbol_index
    seen_by_kind = {}  # kind -> symbol_index (fallback)
    next_idx = 1
    page_index_assignments = {}  # page_id -> list of (sym_ref, idx)
    for page_id in sorted(by_page.keys()):
        page_assignments = []
        for sym in by_page[page_id]:
            bbox = sym.get("bbox")
            kind = sym.get("kind", "unknown")
            phash = get_crop_hash(int(page_id[1:]), bbox) if bbox else ""
            matched = None
            if phash and phash in seen_by_hash:
                matched = seen_by_hash[phash]
            elif kind in seen_by_kind and not phash:
                matched = seen_by_kind[kind]
            if matched is None:
                # New symbol
                idx = next_idx
                next_idx += 1
                geom_id = f"GEOM_{idx:04d}"
                index.append({
                    "symbol_index": idx,
                    "geometry_id": geom_id,
                    "first_seen_page": page_id,
                    "first_seen_position": bbox,
                    "kind": kind,
                    "description": sym.get("description", ""),
                    "occurrences": [{"page": page_id, "bbox": bbox}],
                    "fingerprint_hash": phash,
                })
                if phash:
                    seen_by_hash[phash] = idx
                seen_by_kind[kind] = idx
                sym["symbol_index"] = idx
                sym["first_appearance"] = True
                sym["geometry_ref"] = geom_id
                page_assignments.append({"symbol_index": idx,
                                          "bbox": bbox, "kind": kind,
                                          "first_appearance": True})
            else:
                # Existing symbol
                idx = matched
                # Add occurrence
                for s in index:
                    if s["symbol_index"] == idx:
                        s["occurrences"].append({"page": page_id, "bbox": bbox})
                        break
                sym["symbol_index"] = idx
                sym["first_appearance"] = False
                # Look up geometry_id
                geom_id = next((s["geometry_id"] for s in index
                                if s["symbol_index"] == idx), None)
                sym["geometry_ref"] = geom_id
                page_assignments.append({"symbol_index": idx,
                                          "bbox": bbox, "kind": kind,
                                          "first_appearance": False})
        page_index_assignments[page_id] = page_assignments
        # Write per-page symbol file
        (args.out / f"{page_id}_symbols.json").write_text(
            json.dumps(page_assignments, indent=2, ensure_ascii=False))
        # Update the merged page JSON
        merged_path = args.pages / f"{page_id}.json"
        if merged_path.exists():
            d = json.loads(merged_path.read_text())
            d["symbols"] = by_page[page_id]  # now with symbol_index
            merged_path.write_text(
                json.dumps(d, indent=2, ensure_ascii=False))

    # Write global index
    out_index = {
        "schema_version": "1.0",
        "generated_at": "2026-07-04T07:52:28Z",
        "ordering_rule": (
            "Reihenfolge des ersten Auftretens im Fließtext; "
            "Seite 1 oben-links (Koordinate 0,0) nach unten-rechts lesend."
        ),
        "total_symbols": len(index),
        "symbols": index,
    }
    (args.out / "symbols_index.json").write_text(
        json.dumps(out_index, indent=2, ensure_ascii=False))

    # Also add a geometry section: for each symbol, compute geometry features
    for s in index:
        bb = s.get("first_seen_position")
        if bb and len(bb) == 4:
            w, h = bb[2], bb[3]
            s["geometry"] = {
                "geometry_id": s["geometry_id"],
                "kind": s["kind"],
                "aspect_ratio": round(w / max(1, h), 3),
                "bounding_box_normalized": [0, 0, 1, 1],
                "fingerprint_hash": s["fingerprint_hash"],
                "stroke_count_estimate": None,
            }
    (args.out / "symbols_index.json").write_text(
        json.dumps(out_index, indent=2, ensure_ascii=False))

    print(f"Total symbols indexed: {len(index)}")
    for s in index[:30]:
        n_occ = len(s["occurrences"])
        print(f"  {s['symbol_index']:>3}  {s['first_seen_page']}  "
              f"{s['kind']:<35}  n_occ={n_occ}  "
              f"{s['description'][:50]}")


if __name__ == "__main__":
    main()
