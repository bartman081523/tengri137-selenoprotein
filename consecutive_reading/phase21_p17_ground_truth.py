"""
phase21_p17_ground_truth.py
V7 Phase 21 — p17 OCR-Ground-Truth via Re-Extraction

Problem: p17_G*.png Crops aus Phase 11e sind leer/schwarz.
Lösung: Re-Extrahiere Crops aus pages_png/page-17.png mit den
        verifizierten BBox-Koordinaten aus p17_ziffern.json.

Output: Saubere Crops + Visualisierung + Heuristik-Klassifikation.
KEINE Halluzination: nur Geometrie + Inken-Pixel-Analyse.
"""
import json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

OUT = Path("bbox/mathe_ocr_20260707_V7")
OUT_NEW = Path("bbox/mathe_ground_truth_20260707_V7")
OUT_NEW.mkdir(parents=True, exist_ok=True)

# 1. Lade Original-p17
src = Image.open("pages_png/page-17.png").convert("L")
arr = np.array(src)
H, W = arr.shape
print(f"p17 Original: {W}x{H}, ink={(arr<200).sum()}")

# 2. Lade verifizierte BBox-Koordinaten
with open(OUT / "p17_ziffern.json") as f:
    ziffern = json.load(f)

clusters = ziffern["clusters"]
print(f"BBox-Cluster: {len(clusters)}")

# 3. Saubere Re-Extraktion
# Trenne: Striche (aspect > 5) vs Glyphen (aspect <= 5)
striche = [c for c in clusters if c["aspect"] > 5]
glyphs = [c for c in clusters if c["aspect"] <= 5]
print(f"  Striche: {len(striche)}")
print(f"  Glyphen: {len(glyphs)}")

# 4. Sortiere Glyphen nach Lesereihenfolge (top-to-bottom, left-to-right)
glyphs_sorted = sorted(glyphs, key=lambda c: (c["y_start"], c["x_start"]))

# 5. Extrahiere und speichere Crops mit Padding
PAD = 10
crops_extracted = []
for i, c in enumerate(glyphs_sorted, 1):
    x1 = max(0, c["x_start"] - PAD)
    y1 = max(0, c["y_start"] - PAD)
    x2 = min(W, c["x_end"] + PAD)
    y2 = min(H, c["y_end"] + PAD)
    crop = arr[y1:y2, x1:x2]
    # Behalte Original-Graustufen (Tinte = dunkel, Hintergrund = hell)
    img_crop = Image.fromarray(crop)
    out_path = OUT_NEW / f"glyph_{i:02d}_row_{c['row']}_x{c['x_start']:04d}_y{c['y_start']:04d}.png"
    img_crop.save(out_path)
    crops_extracted.append({
        "id": i,
        "row": c["row"],
        "bbox_orig": [c["x_start"], c["y_start"], c["x_end"], c["y_end"]],
        "bbox_padded": [x1, y1, x2, y2],
        "size_px": c["size"],
        "w": c["w"],
        "h": c["h"],
        "aspect": c["aspect"],
        "est_digits": c["est_digits"],
        "crop_path": str(out_path.relative_to(".")),
    })
    print(f"  Glyph {i:2d} {c['row']}: x={c['x_start']:4d}-{c['x_end']:4d} y={c['y_start']:4d}-{c['y_end']:4d} w={c['w']:3d} h={c['h']:2d} asp={c['aspect']:.2f} → {out_path.name}")

# 6. Striche extrahieren (für visuelle Verifikation)
strich_crops = []
for i, s in enumerate(sorted(striche, key=lambda c: (c["y_start"], c["x_start"])), 1):
    x1 = max(0, s["x_start"] - PAD)
    y1 = max(0, s["y_start"] - PAD)
    x2 = min(W, s["x_end"] + PAD)
    y2 = min(H, s["y_end"] + PAD)
    crop = arr[y1:y2, x1:x2]
    img_crop = Image.fromarray(crop)
    out_path = OUT_NEW / f"strich_{i:02d}_row_{s['row']}.png"
    img_crop.save(out_path)
    strich_crops.append({"id": i, "row": s["row"], "bbox": [s["x_start"], s["y_start"], s["x_end"], s["y_end"]], "w": s["w"], "path": str(out_path.relative_to("."))})

print(f"\nStriche extrahiert: {len(strich_crops)}")

# 7. Visualisierung: BBox-Overlay auf p17
img_rgb = Image.open("pages_png/page-17.png").convert("RGB")
draw = ImageDraw.Draw(img_rgb)
for c in clusters:
    color = (255, 0, 0) if c["aspect"] > 5 else (0, 0, 255)  # rot=Strich, blau=Glyph
    draw.rectangle([c["x_start"], c["y_start"], c["x_end"], c["y_end"]], outline=color, width=2)
img_rgb.save(OUT_NEW / "p17_bbox_overlay.png")
print(f"Visualisierung: {OUT_NEW}/p17_bbox_overlay.png")

# 8. Geometrische Heuristik pro Glyph
# - aspect ≈ 1.0: einzelne Ziffer (kann 0, 1, 2, 3, 5, 7, 8 sein)
# - aspect > 2.0: mehrstellige Ziffernfolge
# - height ≈ 30: Standard-Zifferngröße
# - height > 30: tiefgestellte Ziffern
# - size_px / (w*h) = fill_ratio: hoher Wert = kompakte Ziffer
print("\n" + "="*80)
print("HEURISTIK-KLASSIFIKATION PRO GLYPH")
print("="*80)
for g in crops_extracted:
    fill = g["size_px"] / max(1, g["w"] * g["h"])
    h_class = "STANDARD" if 25 <= g["h"] <= 35 else ("TIEFGESTELLT" if g["h"] > 35 else "KLEIN")
    print(f"  Glyph {g['id']:2d} {g['row']:8s} w={g['w']:3d} h={g['h']:2d} asp={g['aspect']:.2f} est_d={g['est_digits']} fill={fill:.2f} → {h_class}")

# 9. Match mit Tappeiners 11 verifizierten Periode-7-Werten
# Wir wissen: p17 ist die Header-Berechnungen-Seite
# Tappeiner hat uns 11 Brüche gegeben, aber die sind auf p18+ (BURUMUT-Ebene)
# Die p17-Header sind die 2 besonderen Berechnungen:
#   val1 = 2 × 23 × 499 × 19214759967251 × 55150662460749672076915609  (44 digits)
#   val2 = 3 × 11 × 47 × 139 × 2531 × 549797184491917 × 11111111111111111111111  (46 digits)
#   Periode = 46 Ziffern verifiziert

# 10. Speichere JSON-Manifest
manifest = {
    "metadata": {
        "phase": "V7 / Phase 21",
        "datum": "2026-07-05",
        "methode": "Re-Extraction mit verifizierten BBox-Koordinaten",
        "quelle": "bbox/mathe_ocr_20260707_V7/p17_ziffern.json (Phase 11e)",
        "n_glyphs": len(crops_extracted),
        "n_striche": len(strich_crops),
    },
    "glyphs": crops_extracted,
    "striche": strich_crops,
    "row_legend": {
        "ROW_1": "y≈273: Header-Rechnung 1 (val1 mit Faktorzerlegung)",
        "ROW_2": "y≈338: Header-Rechnung 1 (val2 mit Faktorzerlegung)",
        "ROW_3-6": "y≈403-669: 4 Faktorzerlegungs-Paare (Schmehs 16 Paare?)",
        "ROW_7-10": "y≈1071-1404: Lateinische Beschreibungen / p17-Bottom",
    },
    "hinweis": "Schmehs 16 Faktorzerlegungs-Paare sind in Full_Notes dokumentiert, aber mathematisch inkonsistent. Diese Re-Extraction ist die Ground-Truth für eigene OCR-Validierung.",
}
with open(OUT_NEW / "manifest.json", "w") as f:
    json.dump(manifest, f, indent=2, ensure_ascii=False)
print(f"\nManifest: {OUT_NEW}/manifest.json")
print(f"\n✓ {len(crops_extracted)} Glyph-Crops + {len(strich_crops)} Strich-Crops extrahiert")
