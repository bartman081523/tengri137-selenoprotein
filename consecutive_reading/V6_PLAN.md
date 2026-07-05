# Tengri137 V6 Pipeline — Glyph-First mit Template-Matching

**Status:** Plan-Entwurf 2026-07-05, basierend auf Gemini's V5-Falsifikation
**Kontext:** V5-Kryptanalyse (Phase 1+5) wurde am 2026-07-05 falsifiziert.
**Source der Falsifikation:** `consecutive_reading/Gemini-Antworten2.txt`

## V5 → V6 PIVOT

**V5 PIVOT (verworfen):** Cryptanalysis-First → Constraint-Clustering → Layout → OCR → F1-Falsifikation
**V6 PIVOT:** Glyph-First (Template-Matching) → Token-Stream → Cryptanalysis → Frequency-Match

| Was V5 falsch macht | Was V6 anders macht |
|---|---|
| Cryptanalysis auf 16.797 Inken-Strichen | Cryptanalysis auf ~5.000 diskreten Glyph-Tokens |
| IoC/H/α messen Font-Redundanz | IoC/H/α messen Sprachstruktur |
| 997 V4-Crops + Constraint [25,35] | 30 manuelle Referenz-Glyphen + cv2.matchTemplate |
| H1 abgelehnt (F1=-1) | H1 noch offen — wird ERST mit echtem Token-Stream getestet |
| Tesseract auf p17-p22 (Mathe) | MathPix/Nougat für Formel-OCR |

## Gemini's V6-Empfehlung im Detail

> 1. Manuelle Glyph-Isolation aus p01 (242 echte Buchstaben)
> 2. cv2.matchTemplate auf alle 23 Seiten
> 3. Cryptanalysis auf diskretem Token-Stream
> 4. Frequency-Match-Test gegen Englisch (E=12%, T=9%, A=8%)
> 5. MathPix/Nougat für Formel-OCR

## V6 — Architektur (6 Phasen)

```
Phase 0 (DevMind)         → Manuelle Glyph-Isolation aus p01 (30 Referenz-Glyphen)
Phase 1 (DevMind)         → cv2.matchTemplate auf alle 23 Seiten → Token-Stream
Phase 2 (DevMind)         → Token-Validation (Coverage, Konflikte, Mehrfach-Match)
Phase 3 (CryptanalysisMind) → ECHTE Cryptanalysis: IoC, H, α, N-Gramme auf Token-Stream
Phase 4 (CryptanalysisMind) → Frequency-Match-Test (Englisch, Türkisch, Mongolisch, Deutsch)
Phase 5 (DevMind)         → MathPix/Nougat für Formel-OCR (p17-p23)
Phase 6 (DevMind)         → Schema-validierte Finalisierung
```

## Phase 0 — Manuelle Glyph-Isolation (DevMind)

**Script:** `phase0_manual_glyphs.py`
**Input:** `pages_png/page-01.png` (p01 hat 242 echte Buchstaben laut Gemini)
**Output:** `bbox/glyph_refs_20260706_V6/glyphs.json` + 30 PNG-Crops

**Algorithmus:**
1. **Visuelle Inspektion von p01** durch Julian/PhiMind:
   - 242 Buchstaben identifizieren (Augen + Lupe)
   - 30 distinkte Glyph-Typen klassifizieren (Label 1-30, vorläufig)
   - Pro Glyph: bbox + Klartext-Label (`G01` bis `G30`) + Sample-Crop speichern
2. **Crop-Speicherung:** `glyph_refs_20260706_V6/refs/G01.png` ... `G30.png`
3. **Glyph-Index-Map:** pro Glyph zentrale Pixel-Struktur dokumentieren

**Sanity-Check:** Wenn 30 Glyphen × ~8 Vorkommen/Page × 14 Text-Pages = ~3.360 Glyphen-Total. V5 hatte 997 Crops — passt.

**Manuelle Vorab-Fragen an Gemini:**
- Welche Glyphen sind visuelle Varianten (z.B. `G05_strich_dick`, `G05_strich_dünn`)?
- Sind die Tengri-Glyphen in 26 lateinische Buchstaben abbildbar (Frequency-Match)?
- Oder sind es unbekannte Glyphen ohne lateinisches Pendant?

## Phase 1 — Template-Matching (DevMind)

**Script:** `phase1_template_match.py`
**Input:** Phase 0 Glyph-Refs + alle 23 Pages
**Output:** `bbox/tokenstream_20260706_V6/p{NN}.json` (pro Page eine Token-Liste)

**Algorithmus:**
```python
import cv2
import numpy as np

# Pro Referenz-Glyph:
for ref_path in refs:
    template = cv2.imread(ref_path, cv2.IMREAD_GRAYSCALE)
    result = cv2.matchTemplate(page_gray, template, cv2.TM_CCOEFF_NORMED)
    # Threshold: 0.85 (streng, um False-Positives zu vermeiden)
    locations = np.where(result >= 0.85)
    # Non-Max-Suppression: lokale Maxima innerhalb 30 px
    # → Liste von (x, y, glyph_id, conf)
```

**Konfiguration:**
- `matchTemplate` Methode: `TM_CCOEFF_NORMED` (normalisiert, robust gegen Beleuchtung)
- Threshold: 0.85 (initial; falls zu wenig Matches → 0.80; zu viele → 0.90)
- Non-Max-Suppression: max 1 Match pro 30×30-px-Fenster
- **Multi-Scale:** Templates in 3 Größen testen (16, 32, 64 px) — Tengri könnte unterschiedliche Glyph-Größen haben

**Token-Stream pro Page:** Liste wie `["G03", "G12", "G07", "G03", "G22", ...]` mit Position und Confidence.

**Erwartung:** ~3.000-5.000 Glyphen-Tokens total über 23 Seiten

## Phase 2 — Token-Validation (DevMind)

**Script:** `phase2_validate_tokens.py`
**Input:** Phase 1 Token-Streams
**Output:** `bbox/token_validation_20260706_V6/validation.json`

**Validierungs-Kriterien:**
1. **Coverage:** Was % der Inken-Pixel sind durch Token-Match erklärt? Ziel: > 80%
2. **Konflikte:** Token überlappt mit anderer Glyph? → IoU-Check, höhere Confidence gewinnt
3. **Unmatched Glyphen:** Pixel die nicht matchen — sind das (a) Glyphen-Varianten, (b) Beschädigung, (c) neue Glyphen?
4. **Mehrfach-Match:** Ein Pixel-Bereich matched mit mehreren Templates → Auswahl durch höchste Confidence
5. **Layout-Konsistenz:** Token-Positionen sollten mit Gemini's Layout-Annotation übereinstimmen (Header, Body, Footer)

**Falls Coverage < 60%:** Zurück zu Phase 0, neue Glyphen-Refs hinzufügen

## Phase 3 — Echte Cryptanalysis (CryptanalysisMind)

**Script:** `phase3_cryptanalysis_v6.py`
**Input:** Phase 2 validierte Token-Streams
**Output:** `bbox/cryptanalysis_20260706_V6/crypto_report.json`

**Berechnungen AUF DEM ECHTEN TOKEN-STROM:**
1. **Shannon-Entropie H** = -Σ p(glyph_i) × log₂(p(glyph_i))
2. **Index of Coincidence** = Σ n_i(n_i-1) / N(N-1)
3. **Zipf α** via linearer Fit auf log(freq) vs log(rank)
4. **Bigramm-Häufigkeiten** (Top-50)
5. **Trigramm-Häufigkeiten** (Top-20)
6. **Per-Page-Statistik** (sind manche Glyphen nur auf bestimmten Pages?)

**Hypothesen-Aggregator (5 Heuristiken — SELBE wie V5, aber auf echtem Stream):**
- H im engen Band [3.8, 4.6] → monoalphabetisch
- IoC in [0.055, 0.080] → englische Substitution
- Repetition-Muster → ?
- Top-Token-Anteil → ?
- K_predicted (jetzt aus echter Glyph-Anzahl, nicht aus Strichen)

**Vergleich V5 vs V6 erwartet:**

| Metrik | V5 (auf Strichen) | V6 erwartet (auf Glyphen) |
|---|---|---|
| Shannon H | 2.8706 | ~4.0-4.5 (im Englisch-Band) |
| IoC | 0.1606 | ~0.065 (Englisch-konsistent) |
| Zipf α | 2.9281 | ~1.0 (Englisch-konsistent) |
| Top-Bigramm | S6S6 (Strich) | wahrscheinlich sinnvoller Bigramm |
| K predicted | [25, 35] (aus Strichen) | echte Glyph-Anzahl |

## Phase 4 — Frequency-Match-Test (CryptanalysisMind)

**Script:** `phase4_frequency_match.py`
**Input:** Phase 3 Token-Stream + Referenz-Sprachstatistiken
**Output:** `bbox/frequency_match_20260706_V6/freq_match.json`

**Algorithmus:**
```python
# Referenz-Sprachstatistiken
ref_freqs = {
    "english": {"E": 0.127, "T": 0.091, "A": 0.082, ...},
    "turkish": {"A": 0.122, "I": 0.098, "E": 0.091, ...},
    "mongolian": {"А": 0.131, "Н": 0.099, "..."},
    "german": {"E": 0.174, "N": 0.098, "I": 0.076, ...}
}

# Tengri-Glyph-Frequenzen
tengri_freqs = compute_frequencies(tokenstream)

# Korrelation pro Sprache
for lang, ref in ref_freqs.items():
    # Mappe Tengri-Glyphs (sortiert nach Frequenz) auf Sprach-Buchstaben
    sorted_glyphs = sorted(tengri_freqs, key=lambda g: -tengri_freqs[g])
    sorted_letters = sorted(ref, key=lambda l: -ref[l])
    mapping = dict(zip(sorted_glyphs, sorted_letters))
    # Berechne Korrelation der Frequenz-Vektoren
    corr = pearson_correlation(tengri_freqs, mapped_ref_freqs)
```

**Output:** Pearson-Korrelation pro Sprache
- **Englisch > 0.95:** Schmeh-Hypothese (englische Substitution) bestätigt
- **Türkisch > 0.95:** Hypothese türkischer Text
- **Alle < 0.7:** Nicht-sprachlich oder unbekannte Sprache

## Phase 5 — Formel-OCR (DevMind)

**Script:** `phase5_formula_ocr.py`
**Input:** `bbox/layout_20260705_V5/p{NN}.json` + Page-PNGs
**Output:** `bbox/formula_ocr_20260706_V6/p{NN}.json`

**Algorithmus:**
- **Pages 17-22 (burumut_block, silhouette_formel):** MathPix API oder Nougat
- **Page 23 (chemie_struktur):** Nougat oder RDKit für Strukturformel-Parsing
- **Magic-Cube p05/p06:** KEINE OCR (Gemini: Tokens verwerfen)

**Tool-Auswahl:**
- **Nougat** (Meta): Open-Source, läuft lokal, gut für mathematische Formeln
- **MathPix**: API-basiert, sehr genau, kostenpflichtig
- **SymPy + Regex-Fallback:** Lokal, primitiv, nur für einfache Brüche

**Erwartung:** p17-p22 enthalten Primfaktorzerlegungen wie `2^5 × 3^2 × ...` statt "Burumut-Buchstaben"

## Phase 6 — Schema + Finalisierung (DevMind)

**Script:** `phase6_finalize_v6.py`
**Schema:** `schemas/tengri137_document_v6.schema.json`
**Output:**
- `bbox/final_20260706_V6/p{NN}.json` (23 Files)
- `Tengri137_detailed_20260706_V6/doc.json`

**Schema-Highlights V6:**
- NEU: `token_stream[]` pro Page (Liste von Glyph-IDs + Position + Confidence)
- NEU: `frequency_match` (Korrelations-Werte pro Sprache)
- `layout_type` wie V5
- `cryptanalysis` mit ECHTEN Glyph-Metriken (nicht Strich-Metriken)
- `formula_ocr` für p17-p23 (MathPix/Nougat-Output)

## V6 — Erwartete Verbesserungen ggü. V5

| Metrik | V5 (falsifiziert) | V6 (erwartet) |
|---|---|---|
| Cryptanalysis-Datensatz | 16.797 Striche | ~5.000 Glyphen-Tokens |
| Shannon H | 2.8706 (Font-Redundanz) | ~4.0-4.5 (Sprache) |
| IoC | 0.1606 (Font) | ~0.065 (Englisch-konsistent) |
| H1-Status | "abgelehnt" (auf Strichen) | echt getestet (auf Glyphen) |
| K | 34 (constrained) | echt (aus Template-Match) |
| Frequency-Match | nicht getestet | Pearson-Korrelation pro Sprache |
| Mathe-OCR | Tesseract (Datensalat) | MathPix/Nougat |
| Schmehs Klartext | ignoriert (richtig) | ignoriert (richtig) |

## V6 — Kritische Dateien

**Komplett neu:**
- `phase0_manual_glyphs.py` — Manuelle Glyph-Isolation (semi-automatisch)
- `phase1_template_match.py` — cv2.matchTemplate + Non-Max-Suppression
- `phase2_validate_tokens.py` — Coverage + Konflikte + Mehrfach-Match
- `phase3_cryptanalysis_v6.py` — Echte Cryptanalysis auf Token-Stream
- `phase4_frequency_match.py` — Pearson-Korrelation pro Sprache
- `phase5_formula_ocr.py` — MathPix/Nougat-Wrapper
- `phase6_finalize_v6.py` — Schema + Final
- `generate_readme_v6.py` — README mit Frequency-Match-Tabelle
- `schemas/tengri137_document_v6.schema.json` — V6-Schema

**Wiederverwendet:**
- V5-Phase 3 Layout-Output (`bbox/layout_20260705_V5/p{NN}.json`) — Gemini-Override steht
- V5-Phase 4 OCR für Latein-Bereiche (Magic-Cube, Chemie) — Tesseract hier OK, weil keine Glyphen
- V2-`EmbeddingNet` — optional, falls Template-Match unsicher

**V1-V5 bleiben unangetastet** (Reproduzierbarkeits-Regel)

## V6 — Ausführungsreihenfolge

```bash
TS=20260706_V6
mkdir -p bbox/glyph_refs_$TS \
         bbox/tokenstream_$TS \
         bbox/token_validation_$TS \
         bbox/cryptanalysis_$TS \
         bbox/frequency_match_$TS \
         bbox/formula_ocr_$TS \
         bbox/final_$TS \
         Tengri137_detailed_$TS

# Phase 0 (semi-manuell, ~30 min für Glyph-Isolation)
python3 phase0_manual_glyphs.py --page pages_png/page-01.png --out bbox/glyph_refs_$TS

# Phase 1 (Template-Match auf alle 23 Seiten, ~5-10 min)
python3 phase1_template_match.py --refs bbox/glyph_refs_$TS --out bbox/tokenstream_$TS

# Phase 2 (Token-Validation, ~1 min)
python3 phase2_validate_tokens.py --stream bbox/tokenstream_$TS --out bbox/token_validation_$TS

# Phase 3 (Cryptanalysis auf echtem Token-Stream, ~1 min)
python3 phase3_cryptanalysis_v6.py --stream bbox/tokenstream_$TS --out bbox/cryptanalysis_$TS

# Phase 4 (Frequency-Match, ~1 min)
python3 phase4_frequency_match.py --stream bbox/tokenstream_$TS --out bbox/frequency_match_$TS

# Phase 5 (Mathe-OCR, ~5-15 min, je nach API)
python3 phase5_formula_ocr.py --layout bbox/layout_20260705_V5 --pages-png pages_png --out bbox/formula_ocr_$TS

# Phase 6 (Final)
python3 phase6_finalize_v6.py --stream bbox/tokenstream_$TS \
                              --crypto bbox/cryptanalysis_$TS \
                              --freq bbox/frequency_match_$TS \
                              --formula bbox/formula_ocr_$TS \
                              --schema schemas/tengri137_document_v6.schema.json \
                              --out bbox/final_$TS \
                              --toplevel Tengri137_detailed_$TS
```

## V6 — Verifikation

1. **Coverage:** ≥ 80% der Inken-Pixel auf Text-Pages (p01-p04, p07-p16) sind durch Template-Match erklärt
2. **Glyph-Identität:** 30 distinkte Glyphen, jede mit ≥ 10 Vorkommen über alle Pages
3. **Cryptanalysis-Konsistenz:** IoC ∈ [0.055, 0.080], H ∈ [3.8, 4.6], α ∈ [0.8, 1.2] (zumindest für eine der getesteten Sprachen)
4. **Frequency-Match:** Pearson-Korrelation > 0.7 für mindestens eine Sprache
5. **Schmeh-Vergleich:** Separater V6↔Schmeh-Check (analog zu V5)
6. **Schema-Validation:** jsonschema-Validation für alle 23 Pages + doc.json

## V6 — Risiken / Edge-Cases

1. **Manuelle Glyph-Isolation aufwändig:** 30 Glyphen × 5 min = 2.5 h. **Mitigation:** Semi-automatisch (User markiert erste 5, Script schlägt die nächsten 25 vor)
2. **Template-Match zu starr:** Tengri könnte Glyph-Varianten haben (handschriftliche Abweichungen). **Mitigation:** Multi-Scale + leichtes Threshold-Tuning
3. **Frequency-Match mehrdeutig:** Englisch/Türkisch/Mongolisch könnten ähnliche Frequenz-Profile haben. **Mitigation:** Nicht nur Pearson, sondern auch Bigramm-Übereinstimmung testen
4. **Schmeh-Lösung könnte doch stimmen:** Wenn V6 Frequency-Match > 0.95 für Englisch zeigt, hat Schmeh (2017) doch recht und V5 hat die Cryptanalysis nur am falschen Datensatz gemacht. **Mitigation:** Separater Audit-Trail mit Gemini-Cross-Check
5. **Formel-OCR (MathPix) kostenpflichtig:** API-Key nötig. **Mitigation:** Nougat als Open-Source-Fallback
6. **V6 bricht V5 nicht:** V5-Layout + V5-Schmeh-Rauswurf sind weiterhin gültig, nur V5-Cryptanalysis ist falsch

## V6 — Konkrete nächste Schritte

1. User-Auftrag abwarten: "ja, mach V6"
2. `phase0_manual_glyphs.py` schreiben (semi-automatisch, User markiert erste 5 Glyphen)
3. User-Session: gemeinsam 30 Referenz-Glyphen aus p01 isolieren
4. `phase1_template_match.py` schreiben (cv2-basiert, ~150 Zeilen)
5. Test auf p01 (Coverage, Glyph-Identität)
6. Lauf auf alle 23 Pages
7. `phase3_cryptanalysis_v6.py` (V5-Phase-1-Code refactorn mit echtem Token-Input)
8. `phase4_frequency_match.py` (Sprach-Referenz-Tabelle + Pearson)
9. `phase5_formula_ocr.py` (Nougat-Wrapper)
10. `phase6_finalize_v6.py` + V6-Schema
11. **Validierung der Falsifikation:** Falls V6-IoC ≈ 0.065, ist V5-IoC = 0.16 als Font-Redundanz bestätigt

## Lessons für V6

- **Cryptanalysis MUSS auf diskreten linguistischen Einheiten laufen** (Gemini's Kernkritik)
- **Template-Matching statt Connected-Components** für gesetzte Schriften
- **Frequency-Match statt IoC-Ausschluss** für Sprach-Identifikation
- **Manuelle Verifikation schlägt automatische Heuristik** (242 vs. 541)
- **Schema-Disziplin** (V5 hat Schmeh rausgehalten, V6 muss V5-Layout erben)
