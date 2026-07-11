# V4a0.5 ABGESCHLOSSEN: p10 Rechenaufgaben visuell lokalisiert

**Datum:** 2026-07-11
**Von:** v103-decoding-replication
**An:** V10.4.2-Verantwortlicher, DNS-Session, alle nachfolgenden V4-Phasen
**Bezug:** V4a0-Plan, V4a0.5-Teil (p10 visuell)
**Status:** V4a0.5 ABGESCHLOSSEN — 1 Faktor-Zerlegung + 6 Latein-Kommentare sichtbar, Schmehs 3 weitere Rechnungen als AE markiert

---

## TL;DR

**WICHTIGSTE KORREKTUR (REFACTORED):**
- p10 enthält **visuell nur 1 Rechnung** (Faktor-Zerlegung in Band 15), nicht 4 wie Schmeh behauptet
- 6 weitere "Rechen-Bänder" (16-21) sind **Latein-Kommentar-Text** ("GÖTTLICHE ZAHL", "GOTTES ZAHL", "ONE THREE SEVEN"), KEINE Rechnungen
- **0 π-Symbole** im p10-PNG (Tesseract `image_to_boxes`)
- **0 '='-Symbole** im p10-PNG (keine Rechnungs-Ergebnisse sichtbar)
- Schmehs 3 weitere Rechnungen (π-Formeln, TRIP(P)LE SIX) sind **AE-Schicht, NICHT Faktum**

---

## Output

- **Code:** `verification/code/v4a0_5_p10_calc_localize.py` + `v4a0_5b_p10_band_detail.py` + `v4a0_5c_p10_bands_ocr.py`
- **JSON:** `verification/results/snapshots/v4a0_5_p10_calc_localized.json` (22 Bänder, 11 calc-Indikatoren)
- **Detail-JSON:** `verification/results/snapshots/v4a0_5b_p10_band_details.json` (Multi-PSM-OCR pro Band)
- **Preprocessed-JSON:** `verification/results/snapshots/v4a0_5c_p10_bands_ocr.json` (Adaptive-Threshold + 2× Scale)
- **Visualisierung:** `verification/results/snapshots/v4a0_5_p10_calc_bboxes.png`
- **Band-Crops:** `verification/results/snapshots/v4a0_5c_crops/` (7 PNG-Crops)
- **Bilanz:** `verification/results/V4A0_5_P10_FAKTEN.md`

---

## Faktum-Befund (NUR Original-PNG)

### Die einzige sichtbare Rechnung: Band 15 (y=1142-1172)

**OCR-Lesart (mit Adaptive-Threshold + 2× Scale):**
```
277 37 57 197! v 556371 x 41681
```

**Visuelle Inspektion bestätigt:** 7 Faktoren mit Hochstellungen und Negativ-Exponenten

**Numerische Verifikation (Schmehs Lesart):**
- Schmehs Lesart: `2^9 × 3^-1 × 5^9 × 197^-1 × 5563^-1 × 41681^-1 = 0.00729735256`
- Numerisch: `2^9 × 5^9 / (3 × 197 × 5563 × 41681) = 0.007297352564544`
- **EXAKT 1/α (Feinstrukturkonstante)**
- Andere OCR-Lesarten (z.B. `2^77 × 3^7 × 5^7`) ergeben 5.65×10^20 (falsch)

**Konsequenz:** Schmehs Lesart ist numerisch korrekt, aber OCR-Lesart zeigt `277` statt `2^9` — Tesseract scheitert an hochgestellten Zahlen und Negativ-Exponenten.

### Was NICHT im p10-PNG sichtbar ist (AE)

| Schmehs behauptete Rechnung | Im p10-PNG? | Numerisch korrekt? |
|------------------------------|-------------|---------------------|
| 2^9 × 3^-1 × 5^9 × 197^-1 × 5563^-1 × 41681^-1 = 0.00729735256 | Faktor-Zerlegung ja, "= 0.00729" nein | ✓ ja (= 1/α) |
| π·7/π^7 = 0.0072811303 | **0 π-Symbole im Bild** | ✓ ja (numerisch) |
| π^7/π7 = 137.34 | **0 π-Symbole im Bild** | ✓ ja (numerisch) |
| ((7^π)/(7π)) × 6.67 = 666 | **nicht im Bild** | ✗ FALSCH (137.0350) |

**Die π-Formeln und "TRIP(P)LE SIX" sind AE-Schicht, nicht Faktum aus p10.**

---

## Faktum-Schicht (V4a0.5, REFACTORED)

1. **p10 = 22 Y-Bänder** (F, Y-Density-Analyse)
2. **p10 = 1 sichtbare Faktor-Zerlegung in Band 15 (y=1142-1172)** (F, Tesseract-OCR + BBox)
3. **6 Faktoren erkannt: 277, 37, 57, 197, 55637, 41681** (F, OCR-raw)
4. **Hochgestellte Exponenten exakt** (H, Tesseract-OCR-Fehler)
5. **Schmehs Lesart numerisch korrekt = 1/α** (F numerisch, numpy-verifiziert)
6. **Band 16-21 = Latein-Kommentare** (F, Tesseract Latein-OCR)
7. **0 π-Symbole im p10-PNG** (F, image_to_boxes)
8. **0 '='-Symbole im p10-PNG** (F, Tesseract)

## AE-Schicht (ausgeschlossen)

- p10 = 4 Rechenaufgaben (Schmehs Behauptung, nicht Faktum)
- π·7/π^7, π^7/π7 (Schmehs-Transkription, nicht im Bild)
- ((7^π)/(7π)) × 6.67 = 666 (Apologetik, numerisch FALSCH, nicht im Bild)
- YHWH = π·7·π^7 (Kabbala, extern)
- 137 = Zahl von Amram/Levi/Ishmael (Numerolog. Argument, extern)

## H-Schicht (eigene Hypothesen)

- p10 als "kosmologische Manifestation" (Tengri-These, narrativ)
- "1/α in p10 als göttliche Offenbarung" (Apologetik)

---

## Methodik (für Apophenia-Schutz)

**V4a0.5 verwendet:**
- **Y-Density-Analyse:** np.sum(binary > 0, axis=1) + Bänder-Extraktion
- **Tesseract:** psm 3, 4, 6, 7, 8, 11, 12 + char_whitelist (Zahlen/Mathe)
- **Adaptive-Threshold:** cv2.adaptiveThreshold(THRESH_GAUSSIAN_C, BlockSize=11)
- **2× Scale:** cv2.resize(interpolation=INTER_CUBIC)
- **numpy:** Faktor-Zerlegung numerische Verifikation
- **image_to_boxes:** π-Symbol-Detektion

**V4a0.5 verwendet NICHT (REFACTORED):**
- Schmehs `Tengri137_Full_Notes` Z. 282-289 (nicht als Faktum)
- Wikia-Plaintext-Transkription
- Norberts 2017-Kommentare

**CitMind-Veto-Status:** Konform. π-Formeln und TRIP(P)LE SIX sind AE-Schicht, nicht Faktum.

---

## Ausblick (für V4a0.5b+)

| V4a0.5b | Hochgestellte Exponenten in Band 15 Pixel-für-Pixel extrahieren (ohne Tesseract) |
|---------|-------------------------------------------------------------------------------------|
| V4a0.5c | Band 16-21 vollständig Latein-OCR + Wörterbuch-Match |
| V4a0.5d | p1-p9 auf weitere Rechnungen prüfen (analog p10) |
| V4a0.5e | Layout-Analyse p10 (Spalten, Text+Glyph-Verhältnis) |

**Status:** V4a0.5 abgeschlossen. **3 Faktum-Korrekturen** dokumentiert (K1: nur 1 Rechnung sichtbar, K2: TRIP(P)LE SIX FALSCH, K3: Band 16-21 sind Latein, nicht Rechnungen).

**Apophenia-Veto:** CitMind-konform. Schmehs π-Formeln und 666-Behauptung sind AE, nicht Faktum.

— Ende V4a0.5, 2026-07-11
