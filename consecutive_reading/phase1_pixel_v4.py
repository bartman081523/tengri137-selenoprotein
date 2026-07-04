#!/usr/bin/env python3
"""
Phase 1 v4 — Inken-Components + Layout-Analyse (KEIN Tesseract).

Fundamentale Änderung ggü. V2/V3:
- Connected-Components auf der Inken-Maske (NICHT auf weißen Blanks)
- Jeder Inken-Component bekommt eine globale component_id (fortlaufend über alle 23 Pages)
- Multi-Resolution-Component-Liste (micro/meso/macro)
- Layout-Analyse via DBSCAN auf Component-Centroiden (Zeilen, Spalten, Raster)

Wichtige Erkenntnis aus Tengri137_raw_text.txt (Schmeh 2017):
- Schmehs Rekonstruktion ist eine HINWEIS-Quelle, nicht Wahrheit
- V1-V3 haben Glyphen (z.B. "1Y3", "XY", "IT") fälschlich als lateinische Buchstaben
  interpretiert — Schmehs Rekonstruktion enthält tatsächlich lateinische Wörter
  ("TENGRI IS THE SOURCE..."), aber daneben dekorative Glyphen
- Latein-Text ist in ALL-CAPS, Glyphen sind isolierte komplexe Strukturen
- Validierung in V7: jede Komponente bekommt einen "Hinweis" aus Schmeh, der angibt
  ob die Zeile in der Rekonstruktion lateinisch oder ein {description}-Block ist

Input:
  - pages_png/page-NN.png  (Original 150 DPI, 1125×1625)

Output:
  - bbox/pages_pixel_<TS>/p{NN}.json  (mit globalen Component-IDs + Layout)
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage


def cluster_1d(values: list, eps: float, min_samples: int = 1) -> list:
    """Einfache 1D-Clusterung (DBSCAN-äquivalent) ohne sklearn.

    Returns eine Liste von Cluster-Labels (-1 = noise/ungeclustert).
    """
    if not values:
        return []
    sorted_idx = sorted(range(len(values)), key=lambda i: values[i])
    labels = [-1] * len(values)
    cluster_id = 0
    current_cluster = [sorted_idx[0]]
    for i in range(1, len(sorted_idx)):
        prev_val = values[sorted_idx[i - 1]]
        cur_val = values[sorted_idx[i]]
        if cur_val - prev_val <= eps:
            current_cluster.append(sorted_idx[i])
        else:
            # Cluster abschließen
            if len(current_cluster) >= min_samples:
                for idx in current_cluster:
                    labels[idx] = cluster_id
                cluster_id += 1
            current_cluster = [sorted_idx[i]]
    # Letzten Cluster abschließen
    if len(current_cluster) >= min_samples:
        for idx in current_cluster:
            labels[idx] = cluster_id
    return labels

ROOT = Path("/run/media/julian/ML4/tengri137/consecutive_reading")
PNG_DIR = ROOT / "pages_png"


# Globaler Component-Counter (über alle 23 Pages)
class ComponentIdGen:
    def __init__(self):
        self._next = 1  # 1-basiert, 0 = ungültig

    def next_id(self) -> int:
        cid = self._next
        self._next += 1
        return cid


def detect_ink(img: Image.Image) -> np.ndarray:
    """Return a boolean mask: True = ink, False = white."""
    g = img.convert("L")
    a = np.array(g)
    return a < 200  # anything darker than light grey = ink


def extract_components(ink: np.ndarray, cid_gen: ComponentIdGen,
                       min_size: int = 10) -> list:
    """Label connected ink components and return list of dicts.

    Returns a list of component dicts with global IDs. The min_size filter
    removes specks smaller than ~10 pixels (anti-aliasing noise).
    """
    lbl, n = ndimage.label(ink)
    out = []
    for i in range(1, n + 1):
        ys, xs = np.where(lbl == i)
        area = len(ys)
        if area < min_size:
            continue
        x0, x1 = int(xs.min()), int(xs.max())
        y0, y1 = int(ys.min()), int(ys.max())
        w, h = x1 - x0 + 1, y1 - y0 + 1
        cx = float(xs.mean())
        cy = float(ys.mean())
        bbox_area = w * h
        fill_ratio = area / max(1, bbox_area)
        aspect = w / max(1, h)
        # Class hint from aspect + size (V4-Heuristik)
        if area < 100 and w <= 5 and h <= 5:
            class_hint = "punctum"
        elif w > 800 and h < 5:
            class_hint = "horizontal_line"
        elif h > 1400 and w < 5:
            class_hint = "vertical_line"
        elif w / max(1, h) > 5:
            class_hint = "horizontal_stroke"
        elif h / max(1, w) > 5:
            class_hint = "vertical_stroke"
        elif area > 2000:
            class_hint = "macro_glyph_part"
        else:
            class_hint = "meso_glyph_part"
        out.append({
            "id": cid_gen.next_id(),
            "bbox": [x0, y0, w, h],
            "size_px": int(area),
            "fill_ratio": round(fill_ratio, 4),
            "centroid": [round(cx, 1), round(cy, 1)],
            "bounding_box_aspect": round(aspect, 3),
            "class_hint": class_hint,
        })
    out.sort(key=lambda c: (c["centroid"][1], c["centroid"][0]))
    return out


def classify_resolution(component: dict) -> str:
    """Multi-Resolution-Klassifikation (size_px-basiert)."""
    s = component["size_px"]
    if s < 100:
        return "micro"
    if s < 2000:
        return "meso"
    return "macro"


def detect_rows(components: list, eps_y: int = 15, min_samples: int = 2) -> list:
    """1D-Clusterung auf centroid_y → Zeilen-Cluster."""
    if not components:
        return []
    ys = [c["centroid"][1] for c in components]
    labels = cluster_1d(ys, eps=eps_y, min_samples=min_samples)
    rows = {}
    for c, lbl in zip(components, labels):
        if lbl == -1:
            continue
        rows.setdefault(int(lbl), []).append(c)
    out = []
    for lbl, members in rows.items():
        ys = [m["centroid"][1] for m in members]
        y0 = int(min(m["bbox"][1] for m in members))
        y1 = int(max(m["bbox"][1] + m["bbox"][3] for m in members))
        out.append({
            "row_label": int(lbl),
            "y_start": y0,
            "y_end": y1,
            "y_center": round(float(np.mean(ys)), 1),
            "n_components": len(members),
        })
    out.sort(key=lambda r: r["y_center"])
    return out


def detect_cols_in_rows(components: list, rows: list, eps_x: int = 25,
                        min_samples: int = 2) -> list:
    """Für jede Zeile: 1D-Clusterung auf centroid_x → Spalten-Cluster."""
    out = []
    for r in rows:
        row_components = [
            c for c in components
            if r["y_start"] - 5 <= c["centroid"][1] <= r["y_end"] + 5
        ]
        if len(row_components) < min_samples:
            continue
        xs = [c["centroid"][0] for c in row_components]
        labels = cluster_1d(xs, eps=eps_x, min_samples=min_samples)
        cols = {}
        for c, lbl in zip(row_components, labels):
            if lbl == -1:
                continue
            cols.setdefault(int(lbl), []).append(c)
        col_list = []
        for lbl, members in cols.items():
            xs = [m["centroid"][0] for m in members]
            col_list.append({
                "col_label": int(lbl),
                "x_start": int(min(m["bbox"][0] for m in members)),
                "x_end": int(max(m["bbox"][0] + m["bbox"][2] for m in members)),
                "x_center": round(float(np.mean(xs)), 1),
                "n_components": len(members),
            })
        col_list.sort(key=lambda c: c["x_center"])
        out.append({
            "row_y_center": r["y_center"],
            "cols": col_list,
            "n_cols": len(col_list),
        })
    return out


def detect_raster(rows: list, cols_per_row: list,
                  min_rows: int = 2, min_cols: int = 2) -> dict:
    """Heuristik: wenn ≥2 Zeilen mit ≥2 Spalten und ähnlicher Geometrie → Raster."""
    if len(rows) < min_rows:
        return {"is_raster": False, "raster_dim": [0, 0]}
    rows_with_cols = [r for r in cols_per_row if r["n_cols"] >= min_cols]
    if len(rows_with_cols) < min_rows:
        return {"is_raster": False, "raster_dim": [0, 0]}
    mean_cols = float(np.mean([r["n_cols"] for r in rows_with_cols]))
    if mean_cols < 2 or mean_cols > 12:
        return {"is_raster": False, "raster_dim": [0, 0]}
    ys = sorted([r["row_y_center"] for r in rows_with_cols])
    if len(ys) >= 2:
        y_diffs = [ys[i+1] - ys[i] for i in range(len(ys)-1)]
        mean_row_height = float(np.mean(y_diffs))
    else:
        mean_row_height = 0
    if mean_row_height < 20 or mean_row_height > 200:
        return {"is_raster": False, "raster_dim": [0, 0]}
    return {
        "is_raster": True,
        "raster_dim": [int(round(mean_cols)), len(rows_with_cols)],
        "mean_row_height_px": round(mean_row_height, 1),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--min-component-size", type=int, default=10,
                    help="Minimum size in pixels (default 10 — drop anti-alias specks).")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    cid_gen = ComponentIdGen()

    for i in range(1, 24):
        png = PNG_DIR / f"page-{i:02d}.png"
        if not png.exists():
            print(f"  p{i:02d}: SKIP (missing input)", file=sys.stderr)
            continue
        img = Image.open(png)
        a_rgb = np.array(img.convert("RGB"))
        a_g = np.array(img.convert("L"))
        ink = a_g < 200
        total_ink_px = int(ink.sum())
        ink_ratio = round(float(total_ink_px) / (a_g.shape[0] * a_g.shape[1]), 4)

        # 1. Component-Extraktion (globale IDs)
        components = extract_components(ink, cid_gen, min_size=args.min_component_size)

        # 2. Multi-Resolution-Klassifikation
        n_micro = sum(1 for c in components if classify_resolution(c) == "micro")
        n_meso = sum(1 for c in components if classify_resolution(c) == "meso")
        n_macro = sum(1 for c in components if classify_resolution(c) == "macro")
        for c in components:
            c["level"] = classify_resolution(c)

        # 3. Layout-Analyse (DBSCAN auf Centroiden)
        rows = detect_rows(components, eps_y=15, min_samples=2)
        cols_per_row = detect_cols_in_rows(components, rows, eps_x=25, min_samples=2)
        raster = detect_raster(rows, cols_per_row)

        out = {
            "page_id": f"p{i:02d}",
            "image_size": list(img.size),
            "total_ink_px": total_ink_px,
            "ink_ratio": ink_ratio,
            "n_components": len(components),
            "n_micro": n_micro,
            "n_meso": n_meso,
            "n_macro": n_macro,
            "components": components,
            "layout": {
                "n_rows": len(rows),
                "n_rows_with_cols": sum(1 for r in cols_per_row if r["n_cols"] >= 2),
                "rows": rows,
                "cols_per_row": cols_per_row,
                "is_raster": raster["is_raster"],
                "raster_dim": raster["raster_dim"],
                "mean_row_height_px": raster.get("mean_row_height_px", 0.0),
            },
        }
        (args.out / f"p{i:02d}.json").write_text(
            json.dumps(out, indent=2, ensure_ascii=False))
        raster_mark = " [RASTER]" if raster["is_raster"] else ""
        print(f"  p{i:02d}: components={len(components)} "
              f"(micro={n_micro}, meso={n_meso}, macro={n_macro}), "
              f"rows={len(rows)}, ink_ratio={ink_ratio}{raster_mark}")


if __name__ == "__main__":
    main()
