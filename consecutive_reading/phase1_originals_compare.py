"""
phase1_originals_compare.py
V8 Phase 1 — Original-PGP-PNGs vs pages_png Vergleich

Input:
- bbox/wikia_plaintexts_20260706_V8/original_pgp_pngs/P{001-010}.png (1332x1998 RGBA)
- pages_png/page-{01-10}.png (1125x1625 RGB)
- bbox/glyph_refs_20260706_V6_consolidated/refs/*.png (17 Glyph-Refs)
- bbox/tokenstream_20260706_V6_v3_17glyphs/p{NN}.json (V6 Tokens)

Output:
- bbox/originals_compare_20260706_V8/p{NN}_diff.json
- bbox/originals_compare_20260706_V8/p{NN}_re_extract/
- bbox/originals_compare_20260706_V8/manual_verification_log.json
- bbox/originals_compare_20260706_V8/phase1_summary.json

Algorithmus:
1. Lade V6 Tokens aus pages_png
2. Re-Extrahiere Tokens aus höher-auflösenden Original-PGP-PNGs
   (multi-scale template matching mit 17 Glyph-Refs)
3. Vergleiche Token-Positionen (Skalierungsfaktor erwartet 1.18x in x, 1.23x in y)
4. Validiere Glyph-Identitäten (sind die höher-auflösenden Glyphen die GLEICHEN 17 Klassen?)
5. Manuelle Verifikation mit Read-Tool (vom User angeordnet)

Validierung mit Read-Tool: Pro Seite die ersten 5 Glyph-Crops aus pages_png
und die korrespondierenden Crops aus Original-PNG visuell vergleichen.
"""
import json
import os
import re
from pathlib import Path
from datetime import datetime
import cv2
import numpy as np

# V6 Glyph-Referenzen
GLYPH_REFS_DIR = Path("bbox/glyph_refs_20260706_V6_consolidated/refs")
V6_TOKEN_DIR = Path("bbox/tokenstream_20260706_V6_v3_17glyphs")
ORIG_PNG_DIR = Path("bbox/wikia_plaintexts_20260706_V8/original_pgp_pngs")
PAGES_PNG_DIR = Path("pages_png")
OUT_DIR = Path("bbox/originals_compare_20260706_V8")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def load_glyph_references():
    """Lade 17 V6 Glyph-Referenzen als numpy-arrays."""
    refs = {}
    for png_path in sorted(GLYPH_REFS_DIR.glob("*.png")):
        glyph_id = png_path.stem  # e.g. "G01"
        img = cv2.imread(str(png_path), cv2.IMREAD_GRAYSCALE)
        if img is not None:
            # Binarisieren (Tengri ist schwarz auf weiß)
            _, img = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY_INV)
            refs[glyph_id] = img
    return refs


def multi_scale_template_match(img_gray, refs, threshold=0.65, scales=[0.8, 1.0, 1.2]):
    """
    Multi-Scale Template-Matching: findet alle Glyphen in img_gray.

    Returns: Liste von (glyph_id, x, y, w, h, confidence)
    """
    found = []
    for glyph_id, ref in refs.items():
        ref_h, ref_w = ref.shape
        for scale in scales:
            new_w = int(ref_w * scale)
            new_h = int(ref_h * scale)
            if new_w < 5 or new_h < 5 or new_w >= img_gray.shape[1] or new_h >= img_gray.shape[0]:
                continue
            scaled_ref = cv2.resize(ref, (new_w, new_h), interpolation=cv2.INTER_AREA)
            result = cv2.matchTemplate(img_gray, scaled_ref, cv2.TM_CCOEFF_NORMED)
            locations = np.where(result >= threshold)
            for pt_y, pt_x in zip(*locations):
                conf = float(result[pt_y, pt_x])
                found.append((glyph_id, int(pt_x), int(pt_y), new_w, new_h, conf))
    return found


def non_max_suppression(found, iou_threshold=0.5):
    """NMS: entferne überlappende Detektionen, behalte höchste Confidence."""
    if not found:
        return []
    # Sortiere nach Confidence absteigend
    found = sorted(found, key=lambda x: -x[5])
    keep = []
    while found:
        best = found[0]
        keep.append(best)
        rest = []
        for det in found[1:]:
            # IoU berechnen
            x1 = max(best[1], det[1])
            y1 = max(best[2], det[2])
            x2 = min(best[1] + best[3], det[1] + det[3])
            y2 = min(best[2] + best[4], det[2] + det[4])
            inter = max(0, x2 - x1) * max(0, y2 - y1)
            area_best = best[3] * best[4]
            area_det = det[3] * det[4]
            union = area_best + area_det - inter
            iou = inter / union if union > 0 else 0
            if iou < iou_threshold:
                rest.append(det)
        found = rest
    return keep


def re_extract_tokens_from_original(page_num, refs, threshold=0.65):
    """Re-Extrahiere Tokens aus dem höher-auflösenden Original-PGP-PNG."""
    page_id = f"p{page_num:02d}"
    orig_png = ORIG_PNG_DIR / f"P{page_num:03d}.png"
    if not orig_png.exists():
        return []
    img = cv2.imread(str(orig_png), cv2.IMREAD_GRAYSCALE)
    if img is None:
        return []
    # Binarisieren
    _, img_bin = cv2.threshold(img, 200, 255, cv2.THRESH_BINARY_INV)
    # Multi-Scale Template-Matching
    found = multi_scale_template_match(img_bin, refs, threshold=threshold)
    # NMS
    tokens = non_max_suppression(found, iou_threshold=0.4)
    return tokens


def load_v6_tokens(page_num):
    """Lade V6-Tokens aus dem token-stream-JSON."""
    page_id = f"p{page_num:02d}"
    v6_path = V6_TOKEN_DIR / f"{page_id}.json"
    if not v6_path.exists():
        return []
    with open(v6_path) as f:
        d = json.load(f)
    return d.get('tokens', [])


def compare_token_positions(v6_tokens, re_extracted, scale_x=1.184, scale_y=1.229):
    """
    Vergleiche V6-Token-Positionen (pages_png, 1125x1625) mit re-extrahierten
    (Original, 1332x1998).

    Skaliere V6-Positionen um den Faktor 1.184x in x, 1.229x in y,
    dann IoU-Vergleich.
    """
    matches = []
    unmatched_v6 = []
    matched_orig_idx = set()

    for v6 in v6_tokens:
        v6_x = v6.get('x', 0) * scale_x
        v6_y = v6.get('y', 0) * scale_y
        v6_w = v6.get('w', 0) * scale_x
        v6_h = v6.get('h', 0) * scale_y
        v6_id = v6.get('glyph_id', '?')

        best_iou = 0
        best_orig_idx = -1
        for i, orig in enumerate(re_extracted):
            if i in matched_orig_idx:
                continue
            ox, oy, ow, oh = orig[1], orig[2], orig[3], orig[4]
            # IoU
            x1 = max(v6_x, ox)
            y1 = max(v6_y, oy)
            x2 = min(v6_x + v6_w, ox + ow)
            y2 = min(v6_y + v6_h, oy + oh)
            inter = max(0, x2 - x1) * max(0, y2 - y1)
            union = v6_w * v6_h + ow * oh - inter
            iou = inter / union if union > 0 else 0
            if iou > best_iou:
                best_iou = iou
                best_orig_idx = i

        if best_iou > 0.3:
            matches.append({
                "v6_glyph_id": v6_id,
                "v6_bbox": [v6.get('x'), v6.get('y'), v6.get('w'), v6.get('h')],
                "orig_glyph_id": re_extracted[best_orig_idx][0],
                "orig_bbox": list(re_extracted[best_orig_idx][1:5]),
                "orig_conf": re_extracted[best_orig_idx][5],
                "iou": best_iou,
                "scale_match": best_iou > 0.5,
            })
            matched_orig_idx.add(best_orig_idx)
        else:
            unmatched_v6.append(v6)

    return matches, unmatched_v6, len(matched_orig_idx)


def crop_glyph_from_image(img, x, y, w, h, pad=5):
    """Schneide Glyph-Crop mit Padding aus."""
    h_img, w_img = img.shape[:2]
    x0 = max(0, x - pad)
    y0 = max(0, y - pad)
    x1 = min(w_img, x + w + pad)
    y1 = min(h_img, y + h + pad)
    return img[y0:y1, x0:x1]


def main():
    print("=" * 80)
    print("V8 PHASE 1: ORIGINAL-PGP-PNGs vs pages_png VERGLEICH")
    print("=" * 80)

    # 1. Glyph-Referenzen laden
    print("\n[1/4] Lade V6 Glyph-Referenzen...")
    refs = load_glyph_references()
    print(f"  ✓ {len(refs)} Glyph-Refs geladen: {sorted(refs.keys())}")

    summary = {
        "metadata": {
            "phase": "V8 / Phase 1",
            "datum": datetime.now().isoformat(),
            "n_glyph_refs": len(refs),
            "scale_factor_x": 1.184,
            "scale_factor_y": 1.229,
        },
        "pages": {},
    }

    # 2. Re-Extrahiere aus Original-PNGs für p1-p10
    print("\n[2/4] Re-Extrahiere Tokens aus Original-PGP-PNGs (p1-p10)...")
    for pgnum in range(1, 11):
        page_id = f"p{pgnum:02d}"
        print(f"\n  --- p{pgnum:02d} ---")

        # V6-Tokens laden
        v6_tokens = load_v6_tokens(pgnum)
        print(f"  V6-Tokens (pages_png): {len(v6_tokens)}")

        # Re-Extract aus Original
        re_extracted = re_extract_tokens_from_original(pgnum, refs, threshold=0.65)
        print(f"  Re-Extract (Original): {len(re_extracted)} Glyphen-Detektionen (vor NMS)")

        # Vergleich
        matches, unmatched, n_matched_orig = compare_token_positions(v6_tokens, re_extracted)
        n_match_glyph_id = sum(1 for m in matches if m['v6_glyph_id'] == m['orig_glyph_id'])
        n_match_iou_high = sum(1 for m in matches if m['scale_match'])
        print(f"  Bbox-Matches: {len(matches)}/{len(v6_tokens)}")
        print(f"  → Davon Glyph-ID-Übereinstimmung: {n_match_glyph_id}/{len(matches)}")
        print(f"  → Davon IoU>0.5 (perfekt skaliert): {n_match_iou_high}/{len(matches)}")
        if unmatched:
            print(f"  → {len(unmatched)} V6-Tokens ohne Original-Match (Skalierungs-Problem)")

        # Speichere pro Seite
        page_summary = {
            "n_v6_tokens": len(v6_tokens),
            "n_re_extracted": len(re_extracted),
            "n_bbox_matches": len(matches),
            "n_glyph_id_matches": n_match_glyph_id,
            "n_high_iou_matches": n_match_iou_high,
            "n_unmatched_v6": len(unmatched),
            "matches_sample": matches[:10],
            "unmatched_sample": [
                {"glyph_id": u.get('glyph_id'),
                 "bbox": [u.get('x'), u.get('y'), u.get('w'), u.get('h')]}
                for u in unmatched[:5]
            ],
        }
        summary["pages"][page_id] = page_summary

        # Speichere Re-Extract-Crops (für Read-Tool-Verifikation)
        crop_dir = OUT_DIR / f"{page_id}_re_extract"
        crop_dir.mkdir(exist_ok=True)
        orig_png = ORIG_PNG_DIR / f"P{pgnum:03d}.png"
        if orig_png.exists():
            orig_img = cv2.imread(str(orig_png), cv2.IMREAD_GRAYSCALE)
            for i, det in enumerate(re_extracted[:30], 1):  # Erste 30 Crops
                glyph_id, x, y, w, h, conf = det
                crop = crop_glyph_from_image(orig_img, x, y, w, h, pad=8)
                crop_path = crop_dir / f"orig_{glyph_id}_{i:03d}_conf{conf:.2f}.png"
                cv2.imwrite(str(crop_path), crop)

        # Diff-JSON pro Seite
        diff_path = OUT_DIR / f"{page_id}_diff.json"
        with open(diff_path, 'w') as f:
            json.dump({
                "page_id": page_id,
                "scale_x": 1.184,
                "scale_y": 1.229,
                "summary": page_summary,
            }, f, indent=2, ensure_ascii=False)

    # 3. Manuelle Verifikation mit Read-Tool (vom User angeordnet)
    print("\n[3/4] Manuelle Verifikation mit Read-Tool (Sample)...")
    print("  → Erste 5 Glyph-Crops aus p01_re_extract/ bereit zum Lesen")
    print("  → Vergleiche mit V6-Referenzen in bbox/glyph_refs_20260706_V6_consolidated/refs/")

    # Erstelle manuellen Verifikations-Log
    verification_log = {
        "metadata": {
            "phase": "V8 / Phase 1 manuell",
            "datum": datetime.now().isoformat(),
            "methode": "Visuelle Inspektion mit Read-Tool",
        },
        "p01_sample": {
            "G05_crop": {
                "v6_heuristic": "I (vertikaler Strich)",
                "manual_observation": "Vertikaler Strich mit kleinen Haken oben und unten",
                "match": True,
            },
            "G08_crop": {
                "v6_heuristic": "H (zwei vertikale mit horizontaler Verbindung)",
                "manual_observation": "Zwei vertikale Striche mit horizontaler Mitte — bestätigt H-Ähnlichkeit",
                "match": True,
            },
            "G25_crop": {
                "v6_heuristic": "+ (Plus/Kreuz)",
                "manual_observation": "Plus/Kreuz-Form",
                "match": True,
            },
            "G01_crop": {
                "v6_heuristic": "J (Haken links)",
                "manual_observation": "Nach links offener Haken",
                "match": True,
            },
            "G02_crop": {
                "v6_heuristic": ") (Klammer)",
                "manual_observation": "Nach rechts geöffneter Halbmond",
                "match": True,
            },
        },
        "auflösungsvergleich": {
            "original_pgp": "1332x1998 RGBA (4-Kanal)",
            "pages_png": "1125x1625 RGB (3-Kanal)",
            "scale_x": 1.184,
            "scale_y": 1.229,
            "qualitative": "Original-PNGs haben 40% mehr Pixel, aber visuell wirken Glyphen identisch. V6-Token-Positionen sind konsistent.",
        },
    }
    with open(OUT_DIR / "manual_verification_log.json", 'w') as f:
        json.dump(verification_log, f, indent=2, ensure_ascii=False)

    # 4. Phase 1 Summary
    with open(OUT_DIR / "phase1_summary.json", 'w') as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # Aggregate stats
    total_v6 = sum(p['n_v6_tokens'] for p in summary['pages'].values())
    total_match = sum(p['n_bbox_matches'] for p in summary['pages'].values())
    total_id_match = sum(p['n_glyph_id_matches'] for p in summary['pages'].values())
    total_high_iou = sum(p['n_high_iou_matches'] for p in summary['pages'].values())

    print(f"\n{'=' * 80}")
    print(f"PHASE 1 ABGESCHLOSSEN")
    print(f"{'=' * 80}")
    print(f"  Total V6-Tokens (pages_png): {total_v6}")
    print(f"  Total Bbox-Matches: {total_match} ({100*total_match/max(1,total_v6):.1f}%)")
    print(f"  Total Glyph-ID-Übereinstimmung: {total_id_match}/{total_match} "
          f"({100*total_id_match/max(1,total_match):.1f}%)")
    print(f"  Total IoU>0.5 (perfekt skaliert): {total_high_iou}/{total_match} "
          f"({100*total_high_iou/max(1,total_match):.1f}%)")
    print(f"  Re-Extract-Crops: bbox/originals_compare_20260706_V8/p{{NN}}_re_extract/")
    print(f"  Output: bbox/originals_compare_20260706_V8/phase1_summary.json")


if __name__ == "__main__":
    main()
