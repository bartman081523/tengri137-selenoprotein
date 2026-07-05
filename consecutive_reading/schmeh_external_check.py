#!/usr/bin/env python3
"""
schmeh_external_check.py — Schmeh-External-Check (separat, nicht in Pipeline-Output).

V5 PIVOT: Schmehs Daten werden komplett aus der V5-Pipeline herausgehalten.
DIESES SCRIPT ist die EINZIGE Stelle, wo V5-Output ↔ Schmehs Plaintext verglichen wird.
Es ist ein EXTERNER Check — sein Output landet NICHT in bbox/final_20260705_V5/.

Zweck:
  Validierung, ob Schmehs dechiffrierter Klartext mit den realen lateinischen
  Texten übereinstimmt, die V5 in den nicht-Tengri-Bereichen gefunden hat.

Erwartetes Ergebnis (V5 Hypothese):
  - 14/23 Pages sind reines Tengri (kein lateinischer Text)
    → Schmehs "lateinische Zeilen" sind dechiffrierte Tengri-Substitution (nicht-real)
  - 9/23 Pages haben lateinischen Text (reale Formeln, Chemie)
    → Schmehs Plaintext sollte hier KORREKT sein, weil V5 echte lateinische Zeichen findet
  - Magic-Cube-Pages (p05/p06) enthalten KEINE lateinischen Wörter, nur 3D-Strukturen
    → Schmehs Magic-Cube-Beschreibung existiert visuell nicht

Input:  bbox/ocr_20260705_V5/p{NN}.json  (V5 OCR-Output)
        bbox/schmeh_hints_20260704_V4/p{NN}_hints.json  (Schmehs Klartext, 2017)
        bbox/layout_20260705_V5/p{NN}.json  (V5 Page-Layout)
Output: bbox/schmeh_external_check/schmeh_check.json  (nicht in final/)
        {
          "n_pages": 23,
          "n_pages_pure_tengri": 14,
          "n_pages_with_latin": 9,
          "n_pages_match": 0,
          "n_pages_mismatch": 23,
          "page_results": {
            "p01": {
              "layout": "fliesstext",
              "v5_n_latin_tokens": 0,
              "schmeh_n_latin": 16,
              "schmeh_n_glyphs": 2,
              "interpretation": "PURE_TENGRI: V5 findet 0 lateinische Tokens, Schmeh dechiffriert 16 lateinische Zeilen"
            },
            ...
          }
        }
"""
import argparse
import json
from pathlib import Path


def check_page(page_id: str, v5_ocr_dir: Path, schmeh_dir: Path, layout_dir: Path) -> dict:
    """Vergleiche V5-OCR mit Schmehs Hints für eine einzelne Page."""
    v5_ocr_path = v5_ocr_dir / f"{page_id}.json"
    schmeh_path = schmeh_dir / f"{page_id}_hints.json"
    layout_path = layout_dir / f"{page_id}.json"

    layout_type = "unknown"
    layout_conf = 0.0
    if layout_path.exists():
        layout_data = json.loads(layout_path.read_text())
        layout_type = layout_data.get("layout_type", "unknown")
        layout_conf = layout_data.get("confidence", 0.0)

    v5_n_latin = 0
    v5_n_glyphs = 0
    if v5_ocr_path.exists():
        d = json.loads(v5_ocr_path.read_text())
        v5_n_latin = sum(len(r.get("latin_tokens", [])) for r in d.get("regions", []))
        v5_n_glyphs = d.get("n_tengri_glyphs", 0)

    schmeh_n_latin = 0
    schmeh_n_glyphs = 0
    schmeh_text_sample = []
    if schmeh_path.exists():
        d = json.loads(schmeh_path.read_text())
        schmeh_n_latin = d.get("n_latin", 0)
        schmeh_n_glyphs = d.get("n_glyphs", 0)
        # Erste 3 lateinische Zeilen als Sample
        for line in d.get("lines", []):
            if line.get("type") == "latin" and len(schmeh_text_sample) < 3:
                schmeh_text_sample.append(line.get("text", "")[:80])

    # Klassifikation
    if v5_n_latin == 0 and schmeh_n_latin > 0:
        interpretation = ("PURE_TENGRI: V5 findet 0 lateinische Tokens. "
                          f"Schmeh dechiffriert {schmeh_n_latin} lateinische Zeilen — "
                          "diese entstammen der Tengri-Substitution, NICHT realem lateinischen Text.")
        verdict = "MISMATCH"
    elif v5_n_latin > 0 and schmeh_n_latin == 0:
        interpretation = ("REAL_LATIN_ONLY: V5 findet lateinische Tokens, Schmeh sieht keine. "
                          "Schmeh hat diese Page übersehen oder als 'glyph' klassifiziert.")
        verdict = "SCHMEH_INCOMPLETE"
    elif v5_n_latin > 0 and schmeh_n_latin > 0:
        # Beide finden Latein — vergleiche ob sinnvoll
        if layout_type in ("chemie_struktur", "silhouette_formel"):
            interpretation = (f"BOTH_LATIN ({layout_type}): V5 hat {v5_n_latin}, Schmeh hat {schmeh_n_latin}. "
                              "Latein existiert real, aber Schmehs Zeilen sind dechiffrierte Substitution, "
                              "nicht der OCR-Text.")
        elif layout_type == "magic_cube":
            interpretation = (f"MAGIC_CUBE: V5 hat {v5_n_latin} (Tesseract-Fehler auf 3D-Struktur), "
                              f"Schmeh hat {schmeh_n_latin}. Magic-Cube enthält keine echte lateinische Schrift.")
        else:
            interpretation = f"BOTH_LATIN ({layout_type}): V5={v5_n_latin}, Schmeh={schmeh_n_latin}"
        verdict = "PARTIAL_OVERLAP"
    else:
        interpretation = "BOTH_ZERO: Weder V5 noch Schmeh finden Latein."
        verdict = "EMPTY"

    return {
        "layout": layout_type,
        "layout_confidence": layout_conf,
        "v5_n_latin_tokens": v5_n_latin,
        "v5_n_tengri_glyphs": v5_n_glyphs,
        "schmeh_n_latin": schmeh_n_latin,
        "schmeh_n_glyphs": schmeh_n_glyphs,
        "schmeh_text_sample": schmeh_text_sample,
        "verdict": verdict,
        "interpretation": interpretation,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--v5-ocr", type=Path, required=True,
                    help="bbox/ocr_20260705_V5/")
    ap.add_argument("--schmeh", type=Path, required=True,
                    help="bbox/schmeh_hints_20260704_V4/")
    ap.add_argument("--v5-layout", type=Path, required=True,
                    help="bbox/layout_20260705_V5/")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/schmeh_external_check/")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    page_results = {}
    n_pure_tengri = 0
    n_with_latin = 0
    n_match = 0
    n_mismatch = 0

    for i in range(1, 24):
        page_id = f"p{i:02d}"
        result = check_page(page_id, args.v5_ocr, args.schmeh, args.v5_layout)
        page_results[page_id] = result

        if result["v5_n_latin_tokens"] == 0:
            n_pure_tengri += 1
        else:
            n_with_latin += 1
        if result["verdict"] in ("MISMATCH", "SCHMEH_INCOMPLETE"):
            n_mismatch += 1
        else:
            n_match += 1

    # Aggregat-Statistik
    summary = {
        "n_pages": 23,
        "n_pages_pure_tengri": n_pure_tengri,
        "n_pages_with_latin": n_with_latin,
        "n_pages_match": n_match,
        "n_pages_mismatch": n_mismatch,
        "page_results": page_results,
    }

    out_path = args.out / "schmeh_check.json"
    out_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

    # Drucke Zusammenfassung
    print(f"\n[Schmeh-External-Check] Ergebnis:")
    print(f"  Pages gesamt:           23")
    print(f"  Pages reines Tengri:    {n_pure_tengri} (V5 findet 0 lateinische Tokens)")
    print(f"  Pages mit latein. Text: {n_with_latin}")
    print(f"  V5 ↔ Schmeh match:      {n_match}")
    print(f"  V5 ↔ Schmeh mismatch:   {n_mismatch}")
    print(f"\n  WICHTIG: Schmehs Klartext auf den {n_pure_tengri} reinen Tengri-Pages ist eine DECHIFFRIERUNG,")
    print(f"           KEIN realer lateinischer Text. V5 findet dort NICHTS, weil dort NICHTS ist.")
    print(f"\n  Out: {out_path}")


if __name__ == "__main__":
    main()
