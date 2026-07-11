# verification/ — V10.4-Reverifikation aus Original-PNGs

**Datum:** 2026-07-09
**Zweck:** Alle Behauptungen aus `tengri137_complete_decoded_v104.json` (V10.4) unabhängig aus den 23 Original-PNGs (`/run/media/julian/ML4/tengri137/original_sources/137/`, `…/p011_p023_originals/`) re-verifizieren. **Kein** Rückgriff auf V10.4, doc.json, Schmeh-Notes oder Wikia als Werte-Quelle.

**Vergleichsmaß:** V10.4 / doc.json werden ERST am Ende in Phase 11 (v11_compose.py) geladen — ausschließlich für Side-by-side-Drift-Bestimmung.

## Phasen

| Phase | Skript | Output | Input |
|---|---|---|---|
| 0 | `code/v01_pixel_audit.py` | `data/audit.json` + 23 PNG-Tiles | Original-PNGs |
| 1 | `code/v02_bbox_detect.py` | `data/bboxes/pNN.json` | Original-PNGs |
| 2 | `code/v03_glyph_classes.py` | `data/glyphs/pNN.json` | BBox-Crops |
| 3 | `code/v04_latin_ocr.py` | `data/latin/pNN.json` | Original-PNGs |
| 4 | `code/v05_digits.py` | `data/digits/pNN.json` | Original-PNGs |
| 5 | `code/v06_formulas.py` | `data/formulas/pNN.json` | Original-PNGs |
| 6 | `code/v07_graphics.py` | `data/graphics/pNN.json` | BBox-Liste |
| 7 | `code/v08_magic_cubes.py` | `data/magic_cubes/pNN.json` | BBox-Liste |
| 8 | `code/v09_burumut_matrix.py` | `data/burumut/p23_grid.json` | p23-PNG + Glyph-Klassen |
| 9 | `code/v10_latein_text.py` | `data/text/pNN.json` | Latein-Wörter |
| 10 | `code/v11_compose.py` | `results/complete.json`, `results/diff_vs_v104.json`, `results/per_page.jsonl` | alle Phasen + V10.4 + doc.json |

## Determinismus

Alle Skripte setzen `random.seed(137)`, `np.random.seed(137)`. OpenCV deterministisch per `cv2.setNumThreads(1)`.

## Methoden-Referenz (NICHT als Quelle)

Die bestehenden `consecutive_reading/phase*_*.py` und `consecutive_research/scratches/stufe_*/*.py` Skripte sind erlaubt als Methoden-Referenz (z.B. "wie hat phase1_pixel_v4 BBoxes detektiert?") — aber ihre *Werte* werden NICHT übernommen. Die Reverifikation ist **unabhängig**.

## Out of Scope

Chemische Semantik (Cytosin, Amidin), M4 Tora-Turing, BURUMUT-Selbstprotein, Audio, AlphaFold, Magic-Cube-Summen. Wir zählen **was sichtbar ist**, nicht **was es bedeutet**.

## Erfolgs-Kriterien

- 23/23 Pages mit allen 7 Claim-Klassen (n_glyphs, n_latin, n_digits, n_formulas, n_drawings, n_magic_cubes, n_burumut)
- p23 Reverifikation: 11 BURUMUT-Wörter, je 14 Zeichen
- Akrostichon: BNYZTSOYNKS oder begründet abweichend
- p17 Reverifikation: n_burumut = 0 (V10.3-Fälschung unabhängig re-entdeckt)
- Side-by-side-Diff: ≥70% "Match" oder "methodischer Unterschied"
