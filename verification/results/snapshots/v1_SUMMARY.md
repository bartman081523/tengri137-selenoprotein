# Reverifikations-Summary (V10.4 vs Original-PNGs)

**Datum:** 2026-07-09T16:27:25.953961
**Seiten reverifiziert:** 23 / 23

## Methoden-Stack

- **Quellen:** Nur `/run/media/julian/ML4/tengri137/original_sources/{137,p011_p023_originals}/P001.png..P023.png`
- **NICHT als Quelle verwendet:** V10.4 JSON, doc.json, Full_Notes, Wikia, Schmeh-Blog
- **Determinismus:** numpy.random.seed(137), cv2.setNumThreads(1)

## Aggregat-Totale

| Feld | Reverifikation |
|------|----------------|
| n_bboxes | 8771 |
| n_glyphs | 1319 |
| n_tengri_glyphs | 0 |
| n_latin_words | 648 |
| n_digits | 1497 |
| n_formulas | 2563 |
| n_graphics | 11 |
| n_magic_cubes | 0 |
| n_text_lines | 226 |

## Diff-Klassifikation

- **Match:** 2
- **Methodisch unterschiedlich:** 16
- **Drift klein (±10-30%):** 7
- **Drift groß (>30%):** 8
- **Unknown:** 0

## p23 BURUMUT (kritische Erkenntnis)

V10.4 speichert eine 11×14 BURUMUT-Glyph-Matrix mit 11 Wortlisten (BURUMUTREFAMTU, NURESUTREGUMFA, ...) und Akrostichon BNYZTSOYNKS.

**Reverifikation auf p23 zeigt:**
- Oben (y=0..250): 2 chemische Strukturformeln (Cytosin, Thymin)
- Mitte (y=250..1380): 22 Primfaktorzerlegungen, 11 Bruch-Paare (Z/N)
- Unten (y=1380..1998): Latein-Text "Susceptor, hic liber est officii signaculi testamenti..."

**Die 11×14 BURUMUT-Glyph-Matrix ist auf p23 NICHT visuell vorhanden.** Die BURUMUT-Manifestation auf p23 ist **algebraisch** (Faktor-Brüche) und entspricht der 154-AS-BURUMUT-Peptid-Sequenz aus Stufe_14_Befund.

**Konsequenz:** V10.4 hat die BURUMUT-Wortlisten möglicherweise aus p23 algebraisch rekonstruiert (Faktor-Brüche → Peptid-AS-Sequenz → 11 Wörter × 14 AS), aber als Glyph-Matrix gespeichert. Das ist methodisch erlaubt (V10.4 = High-Level-Interpretations-Layer), aber nicht aus p23 direkt ableitbar.

## Apophenia-Schutz

- **CitMind-Veto:** Jeder Claim gegen die 23 apophenia findings in `minds/CitMind.json` geprüft
- **Keine Monte-Carlo-Tests** in dieser Reverifikation (deterministische Pixel-/OCR-Pipeline)
- **Ehrliche Drift-Klassifikation** statt "V10.4 ist falsch"-Schlussfolgerungen
