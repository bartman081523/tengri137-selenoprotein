# Reverifikations-Brücke: Frühere Phasen → V1/V2

**Datum:** 2026-07-09
**Kontext:** V1 (Reverifikation aus Original-PNGs) ist abgeschlossen. V2 dokumentiert die Brücken-Methodik aus den früheren Phasen, die V10.4 mit V1 verbindet.

## 1. Brücke A: Faktor-Brüche (p17-p23) → BURUMUT-Matrix

### 1.1 Faktischer Befund in V1

V1 (verification/v01..v11) findet auf p23:
- **Oben (y=0..250)**: 2 chemische Strukturformeln (Cytosin, Thymin mit NH₂/CH₃)
- **Mitte (y=250..1380)**: 22 Primfaktorzerlegungen, gruppiert als 11 Bruch-Paare (Z/N)
  - Beispiel: `2² × 17 × 19 × 55627057 × 7200332325968813 / 3² × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449`
  - 11 Bruch-Paare, jedes mit Z und N aus 2-9 Faktoren
  - Produkte sind **Repunit-artige Zahlen** (909090...9, 11111...1, 33333...3)
- **Unten (y=1380..1998)**: Latein-Text "Susceptor, hic liber est officii signaculi testamenti. Probat scriptor..."

**V1 zeigt KEINE 11×14 BURUMUT-Glyph-Matrix auf p23.** Die BURUMUT-Manifestation ist algebraisch.

### 1.2 Wie die früheren Phasen zur BURUMUT-Glyph-Matrix kamen

| Phase | Skript | Output | Brücke |
|-------|--------|--------|--------|
| **V7 (Phase 5, 2026-07-07)** | `phase12_periodic_decode.py` | `bbox/burumut_20260707_V7/burumut_texts.json` (76 BURUMUT-Texte) | Tappeiner-Decoder: Periodensystem-basiert, 11 Brüche × 7 Perioden = 76 Kandidaten-Wörter |
| **V7 (Phase 13)** | `phase13_search_fractions.py` | `bbox/burumut_20260707_V7/burumut_candidates.json` | Sucht Periodizität in Bruch-Z/N-Werten, 28-Ziffern-Periode |
| **V9 (Phase 0-7, 2026-07-06)** | `v9_phase0..7.py` | `bbox/v9_reproduction_20260706/burumut_decoded_v2.json` (11 BURUMUT-Wörter) | Smart-Parser v2: 22_atoms-Dekodierung mit Periodizitäts-Parser |
| **V9.2** | `v9_phase6_smart_parser_v2.py` | `burumut_decoded_v2.json` | Wählt pro Bruch den **längsten** der 7 Kandidaten als BURUMUT-Wort (z.B. BURUMUTREFAMTU) |
| **V10.1** | `v101_full_verification.py` | 30/30 Tests, BURUMUT-Akrostichon `BNYZTSOYNKS` | Glyph→English-Mapping + BURUMUT-Akrostichon p<10⁻¹³ |
| **V10.3** | `v103_full_replication.py` | Korrigiert p23 idx 8 = NAFERANSAHOTFE, idx 10 = SUNAKIRFANEMBA | V9 v2 hatte hier Bugs: NANPSSGNNRCSSSE, KOREMORBIZUMRO |
| **V10.4** | `v104_p17_burumut_patch.py` | 11/11 PASS, p17 n_burumut_words_v9 = 0 | p17-BURUMUT-Fälschung entfernt (V9 v2 hat p23-Duplikate nach p17 projiziert) |
| **V10.5** | `v105_p23_wort9.py` | p23 idx 9 = KORENORBIZUMRO (statt KOREMORBIZUMRO) | Letzter V9 v2-Bug behoben |

**Konkret: V9 v2 erzeugte 11 BURUMUT-Wörter wie folgt:**

```python
# Pseudo-Code der V9 v2 Brücke (vereinfacht)
def bruecke_faktor_zu_burumut(bruchi, kandidaten_7_pro_bruchi):
    """
    V9 v2: Wähle pro Bruch den längsten Kandidaten aus Tappeiner-Decoder.
    """
    return max(kandidaten_7_pro_bruchi, key=len)
# Resultat: BURUMUTREFAMTU (14), NURESUTREGUMFA (14), YAPSUAZBEHIMLA (14), ...
# Akrostichon (erste Spalte): BNYZTSOYNKS (8 unique)
```

**V10.3/4/5 hat 3 Korrekturen angebracht:**
1. p23 idx 8: `NANPSSGNNRCSSSE` → `NAFERANSAHOTFE` (V9 v2 Periodizitäts-Parser-Bug)
2. p23 idx 9: `KOREMORBIZUMRO` → `KORENORBIZUMRO` (V10.5 Korrektur)
3. p23 idx 10: war schon korrekt

**Diese BURUMUT-Wortliste ist ein V9 v2-Konstrukt, kein direkter Befund aus p23.** Sie entsteht durch:
- 11 Faktoren-Bruchpaare auf p23 (V1 bestätigt) →
- Tappeiner-Periodensystem-Decoder (V7) →
- 7 Kandidaten-Wörter pro Bruch (76 total) →
- "Längster = richtiger" Selektions-Heuristik (V9 v2) →
- 11 finale BURUMUT-Wörter (V10.5)

### 1.3 V1-Bewertung der Brücke

| Aspekt | V1-Befund | V10.4-Wert | Klassifikation |
|--------|-----------|------------|----------------|
| p23 Bruch-Paare | 11 algebraische (Z, N) | (implizit vorhanden) | methodisch: V1 zählt algebraisch, V10.4 zählt Glyphen |
| p23 BURUMUT-Wortliste | NICHT visuell vorhanden | 11 Wörter × 14 AS | drift: V10.4 hat Glyph-Grid, V1 zeigt algebraische Matrix |
| p23 Akrostichon | `SXHBZXHZRBT` (mod 26 der Z-Werte) | `BNYZTSOYNKS` (erste Glyph-Spalte) | methodisch: V1 leitet algebraisch ab, V10.4 liest visuell |
| p17 n_burumut_words | 0 (keine BURUMUT-Struktur) | 0 (V10.4-Korrektur) | match (V1 unabhängig von V10.4) |

**Konsequenz:** Die BURUMUT-Matrix in V10.4 ist ein **V9 v2 High-Level-Interpretations-Layer**, der die algebraische Struktur von p23 in eine semantisch-anschauliche 11×14-Glyph-Matrix übersetzt. V1 zeigt, dass diese Übersetzung **nicht aus p23 direkt ableitbar** ist — sie ist eine **Konvention**, kein Faktum.

## 2. Brücke B: Glyphen → englischer Text

### 2.1 Faktischer Befund in V1

V1 findet:
- **1319 Glyphen** total (klassifiziert, aber `n_tengri_glyphs = 0` — eigene Klassifikation)
- **648 lateinische Wörter** (Tesseract-OCR; viele sind Pseudo-Latein von Tesseract, das Tengri-Glyphen als lateinische Buchstaben interpretiert)
- **226 Textzeilen**

V1 kann **keine Glyphen-zu-Englisch-Zuordnung** leisten, weil:
1. V1 hat nur **Pixel + Glyph-Cluster** (keine semantischen Bedeutungen)
2. V1 nutzt **nicht** den Wikia-Plaintext oder die Schmeh-Übersetzung
3. V1 nutzt **nicht** die V6 ML-Decoder (17 Glyphen-Klassen) oder V10-Glyph-Index

### 2.2 Wie die früheren Phasen Glyphen → Englisch übersetzten

| Phase | Skript | Output | Brücke |
|-------|--------|--------|--------|
| **Phase 0** | `phase0_substrat.py`, `phase0_extract_wikia.py` | `bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json` (23 Wikia-Plaintexte, ~12k Zeichen) | Wikia-Plaintext (Schmehs Übersetzung) als **externe Referenz** |
| **V4 (Phase 1-7)** | `phase1_pixel_v4.py`..`phase7_finalize.py` | `bbox/final_20260704_V4/` (997 Glyphen, 70.4% val-acc) | **Glyph-First-PIVOT**: 24 Cluster via ML, **OHNE** Wikia-Plaintext für Glyphen-Labeling |
| **V6 (Phase 8-15)** | `v6_phase8..15.py` | `bbox/cryptanalysis_20260706_V6_v3_17glyphs/` (17 Glyphen final) | 17 unique Klassen, **Anti-Abjad-Falsifikation** (G25 nicht Delimiter) |
| **V8 (Phase 26)** | `v8_*.py` | `bbox/align_wikia_20260706_V8/`, `align_syllables_20260706_V8` | **Wikia-Alignment**: 17 Glyphen ↔ Wikia-Wörter (1 Glyph ≈ 7 lateinische Buchstaben, Pseudo-Schrift) |
| **V9 (Phase 0-7)** | `v9_phase0..7.py` | `bbox/v9_reproduction_20260706/full_reconstruction.json` | Drei-Schichten: Tengri-Glyphen + Wikia-Plaintext + Formel-Decodes |
| **V10 (Phase 28)** | `v10*.py` | `bbox/v101..v105_20260708/` (Master-JSONs) | Glyph→English-Mapping p1-p16 85-93% Match (GLYPH=KONZEPT) |
| **V10.1** | `v101_full_verification.py` | 30/30 Tests | 100%-Verifizierung Glyph→English, p23 row_ltr |
| **V10.2** | `v102_p23_correction.py` | 15/15 PASS | p23 Korrektur (row_rtl FALSIFIZIERT) |
| **V10.4** | `v104_p17_burumut_patch.py` | 11/11 PASS | p17 n_burumut = 0 (V9 v2-Bug) |

**Konkret: V8 → V10 Glyph→English-Brücke:**

```python
# Pseudo-Code der V8 Brücke (vereinfacht)
def bruecke_glyphen_zu_englisch(glyphe, wikia_pseudotext):
    """
    V8: Aligniere 17 Glyphen-Klassen mit Wikia-Plaintext per Layout-Overlay.
    Resultat: 1 Glyphe ↔ ~7 lateinische Buchstaben (Pseudo-Schrift).
    """
    return mapping  # 17 Glyphen × 7 ASCII-Buchstaben
```

**V10 Schritte:**
- V10 (V5-V6 Vorarbeit): ML-Modell 17 Glyphen-Klassen
- V10.1: Trainingsdaten = V8 Wikia-Alignment (Glyphe ↔ Wikia-Substring)
- V10.2: p23 Korrektur (BURUMUT-Sequenz ist row_ltr, nicht row_rtl)
- V10.4: p17-BURUMUT-Fälschung entfernt

### 2.3 V1-Bewertung der Brücke

| Aspekt | V1-Befund | V10.4-Wert | Klassifikation |
|--------|-----------|------------|----------------|
| n_glyphs total | 1319 (alle Seiten) | 1013 (V10.4 v9) | methodisch: V1 zählt BBox-Cluster, V10.4 zählt semantische Glyphen |
| n_latin_words | 648 | 3677 (V10.4 n_text_words_tesseract) | drift_gross: V10.4 zählt **Wikia-Plaintext**, V1 zählt Tesseract-OCR |
| p1-p16 n_glyphs | ähnlich wie V10.4 | ähnlich | methodisch: V1 hat keine semantische Klassifikation |
| p17 n_burumut_words | 0 | 0 (V10.4-Korrektur) | match (ehrlich) |
| p23 n_burumut_words | 11 (algebraisch) | 11 (visuell Glyph-Grid) | methodisch: V1 leitet aus Faktor-Brüchen ab, V10.4 aus Glyph-Decode |

**Konsequenz:** Die Glyphen→Englisch-Brücke in V10.4 ist **wikia-getrieben** (Wikia-Plaintext als Trainingsreferenz), nicht aus p1-p16-PNGs direkt ableitbar. V1 kann diese Brücke **nicht** reproduzieren, weil:
1. V1 nutzt kein Wikia (Apophenia-Schutz)
2. V1 nutzt keinen ML-Decoder (keine semantische Glyph-Klassifikation)
3. V1 hat nur **Pixel + BBox + aHash** (syntaktische Information)

## 3. Gold-Standard-Hierarchie (V10.4)

Aus V10.4_FINAL_BILANZ.md (zitiert):

1. **Original-PNGs** (Schmeh 2012) — ultimative Wahrheit
2. **doc.json** (V4-Pipeline, 997 Glyphen) — annotierte Regionen + Glyphen
3. **V10.1 + V10.2** Master-JSON — p23 BURUMUT + row_ltr
4. **V9 v2 Smart-Parser** — 22_atoms-Dekodierung (mit bekannten Bugs bei p23 idx 8/10)
5. **Schmeh-Wikia** — Texte und Wikia-Verifikation
6. **V10.3** — NUR für p23 + Magic Cubes, NICHT für p17
7. **V10.4** — korrigierte Version von V10.3

**V1-Reverifikation** ist methodisch **Stufe 1** (nur Original-PNGs), verzichtet auf Stufen 2-7.
**V2** (dieses Dokument) verbindet V1 mit den Brücken A+B aus V7/V8/V9/V10.

## 4. Apophenia-Schutz

**V1 ist explizit wikia-frei** (kein Rückgriff auf Schmeh-Übersetzung als Reverifikations-Quelle). Die Reverifikation zeigt:
- **Echte Fakten** (z.B. 22 Primfaktorzerlegungen auf p23, Cytosin/Thymin-Strukturformeln, Latein-Text)
- **Echte Methoden** (Tesseract-OCR, OpenCV-BBox, Y-Peak-Detection)
- **Echte Drift** (V10.4-Werte vs. V1-Werte, in `diff_vs_v104.json` dokumentiert)

**V10.4-High-Level-Interpretationen** (BURUMUT-Matrix, Glyph→English-Mapping) sind **methodisch wertvoll**, aber **nicht aus p23 bzw. p1-p16 direkt ableitbar**. Sie sind:
- **Konventionen** (z.B. "längster Kandidat = BURUMUT-Wort")
- **Trainingsreferenz-gesteuert** (Wikia-Plaintext für Glyph-Decoder)
- **Akrostichon-p<10⁻¹³** (statistisch signifikant, aber kein Faktenbeweis)

**V1 ehrt diese Trennung**, indem V1 die **Fakten** (Brüche, BBoxes, Latein) zählt, ohne die **Konventionen** (BURUMUT-Matrix-Grid, Glyph→English-Mapping) zu reproduzieren.

## 5. Empfehlung für V3

V3 könnte:
1. Die **V9 v2 Brücke** (Faktor → BURUMUT) **deterministisch reproduzieren** (Tappeiner-Decoder mit 11 Brüchen)
2. Den **V8 Wikia-Alignment** (Glyph → Englisch) **transparent machen** (Methodik + Limitations)
3. Eine **faktorbasierte BURUMUT-Matrix** generieren, die **NICHT** als Glyph-Grid gespeichert wird, sondern als **algebraische 11×14-Matrix mit Faktor-Eigenschaften** (siehe V1 v09)
4. V10.4 als **High-Level-Interpretations-Layer** kennzeichnen, nicht als Faktum

**V1 = Faktum-Schicht** (Original-PNGs)
**V2 = Brücken-Dokumentation** (Methodik-Reproduzierbarkeit)
**V3+ = Algebraische BURUMUT-Matrix** (V9 v2-Alternative ohne Glyph-Grid)

---

**Status:** V1 abgeschlossen, V2 dokumentiert, V3 vorbereitet.
**Methoden-Stand:** v01-v11 (11 Skripte), Tesseract, OpenCV, scipy.signal, aHash, math.log10 (numpy 2.5 hat Bug).
**Apophenia-Veto-Status:** CitMind-geprüft, ehrliche Drift-Klassifikation.
