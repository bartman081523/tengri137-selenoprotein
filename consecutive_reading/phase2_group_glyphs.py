#!/usr/bin/env python3
"""
Phase 2 v4 — Glyph-Gruppierung + Zeilen-Regionen + Crops.

Input:  bbox/pages_pixel_<TS>/p{NN}.json  (Phase 1 v4: Components + Layout)
Output:
  - bbox/components_<TS>/p{NN}/p{NN}_components.json  (alle Components mit globalen IDs)
  - bbox/components_<TS>/p{NN}/p{NN}_layout.json       (Zeilen + Spalten + Raster)
  - bbox/components_<TS>/p{NN}/p{NN}_glyphs.json       (gruppiert + indiziert)
  - bbox/components_<TS>/p{NN}/p{NN}_glyphs/g*.png     (Glyph-Crops)
  - bbox/components_<TS>/p{NN}/p{NN}_lines.json        (Zeilen mit Glyph-Indexen)
  - bbox/components_<TS>/p{NN}/p{NN}_lines/line_*.png  (Zeilen-Crops)

Algorithmus:
1. Glyph-Gruppierung: Inken-Components werden zu "Glyph-Knoten" zusammengefasst
   (DBSCAN-ähnlich, 1D auf centroid_x innerhalb von Zeilen + Größen-Heuristik)
2. Glyph-Indexierung: globale glyph_index (1-basiert, fortlaufend über alle 23 Pages)
3. Glyph-Typ-Heuristik aus Geometrie (punctum, line, geometric_symbol, complex_symbol, unknown)
4. Zeilen-Detektion (DBSCAN auf centroid_y)
5. Latein-Heuristik pro Zeile: viele kleine meso-Components mit hoher fill_ratio
   UND keine großen Glyphen → "likely_latin_line"
"""
import argparse
import json
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


# Import aus Phase 1 v4
sys.path.insert(0, str(Path(__file__).parent))
from phase1_pixel_v4 import cluster_1d, classify_resolution  # noqa: E402

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PNG_DIR = ROOT / "pages_png"


def glyph_grouping_in_row(row_components: list, eps_x: int = 30,
                          min_samples: int = 1) -> list:
    """Gruppiert Components in einer Zeile zu Glyph-Knoten via 1D-Clusterung
    auf centroid_x. Komponenten mit kleinem Abstand (< eps_x) werden zusammengefasst.

    Returns: Liste von Glyph-Dicts (innerhalb dieser Zeile).
    """
    if not row_components:
        return []
    xs = [c["centroid"][0] for c in row_components]
    labels = cluster_1d(xs, eps=eps_x, min_samples=min_samples)
    glyphs = []
    by_cluster = {}
    for c, lbl in zip(row_components, labels):
        if lbl == -1:
            # Single-Component-Glyph
            by_cluster.setdefault(("single", c["id"]), []).append(c)
        else:
            by_cluster.setdefault(int(lbl), []).append(c)
    for cluster_id, members in by_cluster.items():
        # Union-BBox
        x0 = min(m["bbox"][0] for m in members)
        y0 = min(m["bbox"][1] for m in members)
        x1 = max(m["bbox"][0] + m["bbox"][2] for m in members)
        y1 = max(m["bbox"][1] + m["bbox"][3] for m in members)
        size = sum(m["size_px"] for m in members)
        glyphs.append({
            "members": members,
            "bbox": [int(x0), int(y0), int(x1 - x0 + 1), int(y1 - y0 + 1)],
            "size_px": int(size),
            "fill_ratio": round(size / max(1, (x1 - x0 + 1) * (y1 - y0 + 1)), 4),
            "n_components": len(members),
            "centroid": [round(float(np.mean([m["centroid"][0] for m in members])), 1),
                         round(float(np.mean([m["centroid"][1] for m in members])), 1)],
        })
    glyphs.sort(key=lambda g: g["centroid"][0])
    return glyphs


def classify_glyph_type(glyph: dict) -> str:
    """Type-Hint aus Geometrie der Glyph-Gruppe."""
    s = glyph["size_px"]
    w, h = glyph["bbox"][2], glyph["bbox"][3]
    n = glyph["n_components"]
    fr = glyph["fill_ratio"]
    aspect = w / max(1, h)
    if n == 1 and s < 200:
        return "punctum"
    if n == 1 and aspect < 0.3:
        return "vertical_line"
    if n == 1 and aspect > 5:
        return "horizontal_line"
    if n >= 2 and n <= 5 and fr < 0.3:
        return "geometric_symbol"
    if n >= 5:
        return "complex_symbol"
    if fr > 0.7 and aspect > 5:
        return "horizontal_line"
    if fr > 0.7 and aspect < 0.3:
        return "vertical_line"
    return "unknown"


def detect_rows(components: list, eps_y: int = 15, min_samples: int = 1) -> list:
    """1D-Clusterung auf centroid_y (min_samples=1, damit auch isolierte Components eine Zeile bekommen)."""
    if not components:
        return []
    ys = [c["centroid"][1] for c in components]
    labels = cluster_1d(ys, eps=eps_y, min_samples=min_samples)
    rows = {}
    for c, lbl in zip(components, labels):
        if lbl == -1:
            # Komponente ohne Zeile — wird Zeile -1 zugewiesen
            rows.setdefault(-1, []).append(c)
        else:
            rows.setdefault(int(lbl), []).append(c)
    out = []
    for lbl, members in rows.items():
        y0 = int(min(m["bbox"][1] for m in members))
        y1 = int(max(m["bbox"][1] + m["bbox"][3] for m in members))
        out.append({
            "row_label": int(lbl),
            "y_start": y0,
            "y_end": y1,
            "y_center": round(float(np.mean([m["centroid"][1] for m in members])), 1),
            "n_components": len(members),
            "component_ids": [m["id"] for m in members],
        })
    # Sortiere: zuerst echte Zeilen (>= 0) nach y_center, dann -1 (Rauschen) zuletzt
    out.sort(key=lambda r: (r["row_label"] == -1, r["y_center"]))
    return out


def line_latin_score(line_glyphs: list, all_line_components: list) -> float:
    """Heuristik: wie wahrscheinlich ist diese Zeile lateinischer Text?
    Lateinisch = viele kleine meso-Components mit hoher fill_ratio,
                 Wort-Cluster (mehrere Components pro Wort), keine großen Glyphen.
    """
    if not line_glyphs:
        return 0.0
    # Wie viele Components sind klein (meso) mit hoher fill_ratio?
    n_small = sum(1 for c in all_line_components
                  if c["size_px"] < 500 and c["fill_ratio"] > 0.4)
    n_total = len(all_line_components)
    if n_total == 0:
        return 0.0
    small_ratio = n_small / n_total
    # Gibt es große Glyphen? (size > 2000)
    n_macro_in_line = sum(1 for c in all_line_components
                          if c["size_px"] >= 2000)
    # Latein: small_ratio hoch, n_macro niedrig
    score = small_ratio - 0.3 * (1 if n_macro_in_line > 0 else 0)
    return max(0.0, min(1.0, score))


def process_page(page_num: int, pixel_dir: Path, components_dir: Path):
    """Verarbeitet eine einzelne Page."""
    page_id = f"p{page_num:02d}"
    pixel_path = pixel_dir / f"{page_id}.json"
    if not pixel_path.exists():
        print(f"  {page_id}: SKIP (missing {pixel_path})")
        return None
    pixel_data = json.loads(pixel_path.read_text())
    components = pixel_data["components"]
    if not components:
        print(f"  {page_id}: no components")
        return None

    out_dir = components_dir / page_id
    out_dir.mkdir(parents=True, exist_ok=True)
    glyphs_dir = out_dir / f"{page_id}_glyphs"
    lines_dir = out_dir / f"{page_id}_lines"
    glyphs_dir.mkdir(parents=True, exist_ok=True)
    lines_dir.mkdir(parents=True, exist_ok=True)

    # 1. Zeilen-Detektion
    rows = detect_rows(components, eps_y=15, min_samples=1)

    # 2. Pro Zeile: Glyph-Gruppierung
    page_png = PNG_DIR / f"page-{page_num:02d}.png"
    img = Image.open(page_png) if page_png.exists() else None

    glyph_index_start = None  # wird von außen gesetzt
    line_records = []
    glyph_records = []
    glyph_index = 0  # placeholder

    for r_idx, row in enumerate(rows, start=1):
        row_component_ids = set(row["component_ids"])
        row_components = [c for c in components if c["id"] in row_component_ids]
        # Glyph-Gruppierung in dieser Zeile
        line_glyphs = glyph_grouping_in_row(row_components, eps_x=30, min_samples=1)
        # Type-Hints
        for g in line_glyphs:
            g["type_hint"] = classify_glyph_type(g)
        # Latein-Score
        lat_score = line_latin_score(line_glyphs, row_components)

        # Zeilen-Crop (für Phase 3 Vision)
        y_top = max(0, row["y_start"] - 10)
        y_bot = min(img.size[1] if img else 9999, row["y_end"] + 10)
        x_left = min(c["bbox"][0] for c in row_components) - 10 if row_components else 0
        x_right = max(c["bbox"][0] + c["bbox"][2] for c in row_components) + 10 if row_components else 100
        x_left = max(0, x_left)
        x_right = min(img.size[0] if img else 9999, x_right)
        line_crop_path = None
        if img is not None and row_components:
            line_crop = img.crop((x_left, y_top, x_right, y_bot))
            line_crop_path = lines_dir / f"line_{r_idx:02d}.png"
            line_crop.save(line_crop_path)
            try:
                rel = line_crop_path.relative_to(ROOT)
            except ValueError:
                rel = line_crop_path

        line_records.append({
            "line_id": r_idx,
            "bbox": [int(x_left), int(y_top), int(x_right - x_left), int(y_bot - y_top)],
            "y_start": row["y_start"],
            "y_end": row["y_end"],
            "y_center": row["y_center"],
            "n_components": row["n_components"],
            "n_glyphs": len(line_glyphs),
            "glyph_count_per_glyph": [g["n_components"] for g in line_glyphs],
            "latin_score": round(lat_score, 3),
            "is_likely_latin": lat_score > 0.5,
            "is_likely_glyph_raster": (
                len(line_glyphs) >= 2
                and not any(g["type_hint"] in ("punctum", "vertical_line", "horizontal_line")
                            for g in line_glyphs)
                and any(g["type_hint"] in ("geometric_symbol", "complex_symbol")
                        for g in line_glyphs)
            ),
            "glyph_ids": [],  # wird nach globaler Indexierung gesetzt
            "line_crop_path": str(rel) if line_crop_path else None,
        })

    # 3. Globale Glyph-Indexierung (über ALLE Pages)
    # Wir sammeln erst alle Glyphen, dann wird der Index fortlaufend vergeben
    return {
        "page_id": page_id,
        "n_components": len(components),
        "n_rows": len(rows),
        "n_glyphs_local": sum(1 for r in line_records for _ in r["glyph_count_per_glyph"]),
        "line_records": line_records,
        "rows": rows,
        "components": components,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pixel", type=Path, required=True,
                    help="bbox/pages_pixel_<TS>/")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/components_<TS>/")
    ap.add_argument("--glyph-eps-x", type=int, default=30,
                    help="eps_x für Glyph-Gruppierung (default 30)")
    args = ap.parse_args()
    args.out = args.out.resolve()
    args.out.mkdir(parents=True, exist_ok=True)

    # Globale Glyph-Index-Vergabe
    global_glyph_index = 0
    all_glyph_records = []  # (page, line_id, glyph_local_id, glyph_dict)

    for i in range(1, 24):
        page_data = process_page(i, args.pixel, args.out)
        if page_data is None:
            continue
        page_id = page_data["page_id"]
        out_dir = args.out / page_id
        out_dir.mkdir(parents=True, exist_ok=True)

        # Glyphen mit globalen Indexen versehen
        glyph_records = []
        lines_with_glyphs = []
        for r_idx, line in enumerate(page_data["line_records"], start=1):
            line_glyph_ids = []
            # Re-run glyph grouping (deterministisch) — wir holen die Glyphen
            # aus page_data["rows"]
            row = page_data["rows"][r_idx - 1]
            row_component_ids = set(row["component_ids"])
            row_components = [c for c in page_data["components"]
                              if c["id"] in row_component_ids]
            line_glyphs = glyph_grouping_in_row(row_components,
                                                eps_x=args.glyph_eps_x,
                                                min_samples=1)
            for g_lid, g in enumerate(line_glyphs, start=1):
                global_glyph_index += 1
                g["type_hint"] = classify_glyph_type(g)
                g["glyph_index"] = global_glyph_index
                g["page_glyph_id"] = g_lid
                g["line_id"] = r_idx
                g["components"] = [m["id"] for m in g["members"]]
                # Crop speichern
                page_png = PNG_DIR / f"page-{i:02d}.png"
                if page_png.exists():
                    img = Image.open(page_png)
                    bbox = g["bbox"]
                    pad = 15
                    x0 = max(0, bbox[0] - pad)
                    y0 = max(0, bbox[1] - pad)
                    x1 = min(img.size[0], bbox[0] + bbox[2] + pad)
                    y1 = min(img.size[1], bbox[1] + bbox[3] + pad)
                    glyph_crop = img.crop((x0, y0, x1, y1))
                    crop_path = out_dir / f"{page_id}_glyphs" / f"g{global_glyph_index:04d}.png"
                    glyph_crop.save(crop_path)
                    try:
                        g["crop_path"] = str(crop_path.relative_to(ROOT))
                    except ValueError:
                        g["crop_path"] = str(crop_path)
                glyph_records.append({
                    "glyph_index": global_glyph_index,
                    "page": page_id,
                    "page_glyph_id": g_lid,
                    "line_id": r_idx,
                    "bbox": g["bbox"],
                    "size_px": g["size_px"],
                    "fill_ratio": g["fill_ratio"],
                    "n_components": g["n_components"],
                    "components": g["components"],
                    "type_hint": g["type_hint"],
                    "centroid": g["centroid"],
                    "crop_path": g.get("crop_path"),
                })
                line_glyph_ids.append(global_glyph_index)
            line["glyph_ids"] = line_glyph_ids
            lines_with_glyphs.append(line)

        # Schreibe p{NN}_components.json (alle Components mit Klassen-Hints)
        (out_dir / f"{page_id}_components.json").write_text(
            json.dumps({
                "page_id": page_id,
                "n_components": len(page_data["components"]),
                "components": page_data["components"],
            }, indent=2, ensure_ascii=False))

        # Schreibe p{NN}_layout.json
        (out_dir / f"{page_id}_layout.json").write_text(
            json.dumps({
                "page_id": page_id,
                "n_rows": len(page_data["rows"]),
                "rows": page_data["rows"],
            }, indent=2, ensure_ascii=False))

        # Schreibe p{NN}_glyphs.json
        (out_dir / f"{page_id}_glyphs.json").write_text(
            json.dumps({
                "page_id": page_id,
                "n_glyphs": len(glyph_records),
                "glyphs": glyph_records,
            }, indent=2, ensure_ascii=False))

        # Schreibe p{NN}_lines.json
        (out_dir / f"{page_id}_lines.json").write_text(
            json.dumps({
                "page_id": page_id,
                "n_lines": len(lines_with_glyphs),
                "lines": lines_with_glyphs,
            }, indent=2, ensure_ascii=False))

        n_glyphs = len(glyph_records)
        n_lines = len(lines_with_glyphs)
        n_latin = sum(1 for l in lines_with_glyphs if l["is_likely_latin"])
        n_raster = sum(1 for l in lines_with_glyphs if l["is_likely_glyph_raster"])
        print(f"  {page_id}: components={page_data['n_components']}, "
              f"lines={n_lines} (latin={n_latin}, raster={n_raster}), "
              f"glyphs={n_glyphs}")

    print(f"\nTotal glyphs across all pages: {global_glyph_index}")


if __name__ == "__main__":
    main()
