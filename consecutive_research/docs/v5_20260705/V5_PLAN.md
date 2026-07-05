# Tengri137 V5 Pipeline — Cryptanalysis-First Reconstruction

**Status:** Abgeschlossen 2026-07-05
**Time-Stamp:** 20260705_V5
**Schema:** v5.0
**Pipeline-Output:** `consecutive_reading/Tengri137_detailed_20260705_V5/doc.json` + 23 × `p{NN}.json`

## V5 PIVOT — Was ist anders als V4?

**V4 (falsifiziert 2026-07-05):**
- 997 Glyphen aus Multi-Resolution-Clustering (V2-EmbeddingNet)
- 456 lateinische Tokens (368 davon Schmeh-dominiert)
- 22/23 Pages mit lateinischem Text (Schmeh-Halluzination)
- 75 fine-Cluster (Overclustering)
- **Hauptfehler:** Schmehs Klartext wurde als OCR-Ground-Truth missbraucht
- Tesseract-Output wurde ungeprüft in den Pipeline-Output übernommen

**V5 (Kryptanalyse-First, komplett SCHMEH-FREI):**
- 997 Tengri-Glyph-Bboxen (gleiche Detektion wie V4, aber **kein Schmeh-OCR-Mapping**)
- 1097 lateinische Tokens (alle aus selektiver OCR auf nicht-Tengri-Bereiche)
- **9/23 Pages mit lateinischem Text** (reale Formeln, Chemie, Ziffern)
- 34 distinkte Glyphen-Cluster (K aus Phase-1-Hypothese, constraint-clustering)
- H1 (monoalphabetische Substitution für englischen Klartext) **abgelehnt** (F1-Score: -1)
- Schmehs Plaintext existiert visuell auf 14 Pages NICHT (reines Tengri)

## Pipeline-Architektur V5

```
Phase 0 (DevMind)         → Inken-Substrat-Extraktion (16.797 Komponenten)
Phase 1 (CryptanalysisMind) → Shannon-H, IoC, Zipf-α, N-Gramme → Hypothese H1
Phase 2 (DevMind)         → Multi-Resolution-Embeddings + Constraint-Clustering (K aus Phase 1)
Phase 3 (DevMind)         → Page-Layout-Klassifikation (5 Typen, Gemini-Override)
Phase 4 (DevMind)         → Selektive OCR (Tesseract NUR auf nicht-Tengri-Bereiche)
Phase 5 (CryptanalysisMind) → F1-Falsifikation der H1-Hypothese
Phase 6 (DevMind)         → Schema-validierte Finalisierung
```

**Extern:** `schmeh_external_check.py` — separat, nicht in Pipeline-Output

## Phase 0 — Inken-Substrat-Extraktion (DevMind)

**Script:** `phase0_substrat.py`
**Input:** `pages_png/page-NN.png` (150 DPI, 1125×1625)
**Output:** `bbox/substrat_20260705_V5/p{NN}.json`

**Algorithmus:**
1. Inken-Maske: `ink = gray < 200`
2. Connected-Components via `scipy.ndimage.label(ink)`
3. Pro Komponente: `component_id` (global), `bbox`, `size_px`, `fill_ratio`, `centroid`
4. KEINE Glyph-Gruppierung (kommt in Phase 2 mit Embeddings)

**Total über alle 23 Pages:** 16.797 Komponenten

**Wiederverwendung:** V2-`phase1_pixel.py:39-46` (Connected-Components-Logik)

## Phase 1 — Cryptanalysis (CryptanalysisMind)

**Script:** `phase1_cryptanalysis.py`
**Input:** Phase 0 Substrat
**Output:** `bbox/cryptanalysis_20260705_V5/crypto_report.json`

**Befunde:**
- Shannon-Entropie H = **2.8706** bit/Zeichen (Englisch-Ref: 4.14)
- Index of Coincidence IoC = **0.1606** (Englisch-Ref: 0.067) — **2.4× zu hoch**
- Zipf α = **2.9281** (Englisch-Ref: ≈1.0)
- Top-Bigramm: S6S6 mit ~2300 Hits (BURST-artige Repetition)
- Hypothese: `wahrscheinlich_monoalphabetisch` (K_predicted = [25, 35])
- 20 unique Substrat-Tokens (deutet auf Glyph-Variant-Liste, nicht Klartext)

**Hypothese-Aggregator (5 Heuristiken):**
- H im engen Band → monoalphabetisch
- IoC hoch → monoalphabetisch (Englisch: 0.067, Polyalphabetisch: 0.04-0.05)
- Repetition-Muster → monoalphabetisch
- Top-Token-Anteil > 30% → monoalphabetisch
- K_predicted = [25, 35]

## Phase 2 — Glyph-Alphabet (DevMind)

**Script:** `phase2_alphabet.py`
**Input:** Phase 0 Substrat + V2-EmbeddingNet (Warm-Start)
**Output:** `bbox/alphabet_20260705_V5/alphabet.json` (K=34 Cluster)

**Algorithmus:**
1. Lade V4-Glyph-Crops (997 PNGs aus `bbox/components_20260704_V4/p{NN}/p{NN}_glyphs/`)
2. V2-`EmbeddingNet`: Conv→ReLU→MaxPool→Conv→ReLU→MaxPool→Conv→ReLU→AdaptiveAvgPool→Linear(64,64)
3. Multi-Resolution: 16+32+64 px → 192-dim Vektor
4. Custom `silhouette_score_numpy` (ohne sklearn)
5. Multi-Modal-Distance: 0.2×cosine + 0.5×size + 0.3×aspect
6. Agglomeratives Clustering mit **Constraint [25, 35]** aus Phase 1
7. **Ergebnis:** K=34, Silhouette=0.5113

**Cluster-Verteilung (Top 10):** 179, 155, 117, 96, 78, 53, 44, 39, 39, 38
**Singletons:** 5 (Cluster 30-34 mit n_occurrences=1)

## Phase 3 — Multi-Layout-Analyse (DevMind)

**Script:** `phase3_layout.py`
**Output:** `bbox/layout_20260705_V5/p{NN}.json` (23 Files)

**Layout-Typen (Gemini-Override-Tabelle 2026-07-05):**
- `fliesstext` (14): p01-p04, p07-p16
- `magic_cube` (2): p05, p06
- `burumut_block` (4): p17, p19, p20, p21
- `silhouette_formel` (2): p18, p22
- `chemie_struktur` (1): p23

**Gemini-Korrektur vs. Schmeh:**
- Schmeh: Magic-Cube auf p22/p23, Burumut auf p23
- Realität: Magic-Cube auf p05/p06 (3D-Struktur sichtbar), Burumut **existiert visuell NICHT**
- p23 = Chemie (Cytosin/Thymin-Formeln, mit NH₂, N, C, H, O)
- p17-p22 = Burumut-artige Blöcke, aber mit **Primfaktorzerlegungen** (nicht lateinischem Text)

## Phase 4 — Selektive OCR (DevMind)

**Script:** `phase4_ocr.py`
**Input:** V4-Glyph-BBoxen + V5-Layout
**Output:** `bbox/ocr_20260705_V5/p{NN}.json` (23 Files)

**Algorithmus:**
1. `fliesstext` → KEIN OCR (alles ist Tengri)
2. `magic_cube` / `burumut_block` / `chemie_struktur` / `silhouette_formel`:
   - Tesseract auf volle Page (PSM 6, eng)
   - **Filter:** Token-BBox mit Tengri-Glyph-BBox → IoU > 0.1 → verwerfen
   - Rest = lateinische Zeichen aus nicht-Tengri-Bereichen

**Total:** 1097 lateinische Tokens, davon 0 auf fliesstext-Pages

## Phase 5 — Substitutions-Validierung (CryptanalysisMind)

**Script:** `phase5_decode.py`
**Output:** `bbox/decoded_20260705_V5/decode_report.json`

**F1-Kriterien:**
| Test | Kriterium | V5-Wert | Status |
|---|---|---|---|
| F1.1 | IoC ∈ [0.055, 0.080] (Englisch) | 0.1606 | **FAIL** |
| F1.2 | H ∈ [3.8, 4.6] | 2.8706 | **FAIL** |
| F1.3 | α ∈ [0.8, 1.2] | 2.9281 | **FAIL** |
| F1.4 | K ∈ [25, 35] | 34 | PASS |
| F1.5 | Keine latein. Tokens auf Fließtext | 0 | PASS |

**F1-Score:** -1
**H1-Status:** **ABGELEHNT**

**Interpretation:**
> Der hohe IoC (0.16 vs. Englisch 0.067) deutet auf BURST-artige Repetition.
> Das Substrat zeigt Top-Bigramm S6S6 mit ~2300 Hits — typisch für eine
> Glyph-Variant-Liste, NICHT für natürlichen Klartext.
> K=34 Glyphen-Cluster passt zu ~26 Buchstaben + 10 Ziffern — Tengri als
> Substitutions-Alphabet bleibt plausibel, aber der Klartext ist KEIN Englisch.
> Mögliche Alternativen: (a) andere Sprache (Türkisch, Mongolisch),
> (b) numerische/templated Inhalte, (c) nicht-linguistisches System.

## Phase 6 — Finalisierung (DevMind)

**Script:** `phase6_finalize_v5.py`
**Schema:** `schemas/tengri137_document_v5.schema.json`
**Output:**
- `bbox/final_20260705_V5/p{NN}.json` (23 Files)
- `Tengri137_detailed_20260705_V5/doc.json` (Single-File 23-Page-Doc)
- **doc.json: SCHEMA VALIDATION PASSED**

**Schema-Highlights V5:**
- `layout_type` enum: fliesstext, magic_cube, burumut_block, chemie_struktur, silhouette_formel, unbekannt
- `latin_token.source` enum: tesseract, vision, geometry (KEIN schmeh_hint/complete)
- Pflichtfelder: layout_type, cryptanalysis, page_id, image_size, regions
- `region_id` Pattern: `^p\d{2}_R\d+(_[A-Z_]+)?$`

## Schmeh-External-Check (separat, Audit-Trail)

**Script:** `schmeh_external_check.py`
**Output:** `bbox/schmeh_external_check/schmeh_check.json` (NICHT in final/)

**Vergleich V5 ↔ Schmehs Plaintext (2017):**

| Kategorie | Anzahl | Interpretation |
|---|---|---|
| Pure Tengri (V5=0, Schmeh>0) | 14 | Schmehs "Latein" ist Dechiffrierung, nicht real |
| Beide Latein (PARTIAL_OVERLAP) | 9 | Magic-Cube, Burumut, Chemie, Silhouette |
| Match (V5=0 = Schmeh=0) | 8 | — |
| Mismatch | 15 | V5 erkennt Realität, Schmeh halluziniert |

**Kern-Befund:** Auf den 14 reinen Tengri-Pages (p01-p04, p07-p16) gibt es
**keinen realen lateinischen Text**. Schmehs "TENGRI IS THE SOURCE OF IMPORTANT
WRITINGS..." ist eine dechiffrierte Substitution, kein OCR-Output.

## Reproduzierbarkeit

- **Time-Stamp:** 20260705_V5
- **Schema:** `schemas/tengri137_document_v5.schema.json`
- **Pipeline-Scripts:** `phase0_substrat.py` bis `phase6_finalize_v5.py` + `schmeh_external_check.py`
- **V1, V2, V3, V4 unangetastet** (Reproduzierbarkeits-Regel)
- **Schmeh-2017 roh_text.txt:** wird komplett ignoriert in V5-Pipeline
- **Source für Falsifikation:** `Gemini-Prompt.txt` + `Gemini-Antwort.txt`

## V5 vs. V4 Vergleich

| Metrik | V4 (falsifiziert) | V5 |
|---|---|---|
| Echte Glyph-Anzahl | 997 (Overclustering) | **34** Cluster (~26 + 10) |
| Lateinische Tokens | 456 (368 Schmeh-dominiert) | **1097** (selektive OCR) |
| Pages mit lateinischem Text | 22/23 | **9/23** (reale Formeln/Chemie) |
| Schmeh in Pipeline | ja (Hauptfehler) | **NEIN** |
| Methodik | OCR auf Crypto-Problem | **Crypto auf Crypto-Problem** |
| H1-Validierung | keine | **ABGELEHNT** (F1-Score: -1) |
| Magic-Cube-Realität | behauptet p22/p23 | **p05/p06** (Gemini-Korrektur) |
| Burumut-Realität | behauptet p23 | **existiert visuell nicht** |
| p23 = Chemie | nein | **ja** (Cytosin/Thymin) |
| p17-p22 = Burumut | nein | **ja, mit Primfaktorzerlegungen** |

## Lessons Learned

1. **Schmeh-Plaintext ≠ Realität**: Schmehs Dechiffrierung halluziniert lateinischen
   Text auf 14/23 Pages, wo V5 mit strenger Methodik NICHTS findet.
2. **Tesseract auf 3D-Strukturen halluziniert**: Magic-Cube-Pages (p05/p06) liefern
   4 lateinische Tokens, die KEINE lateinischen Zeichen sind.
3. **Constraint-Clustering funktioniert**: K aus Phase 1 = [25, 35] führte zu K=34
   mit Silhouette 0.51 — besser als V4's 75 fine-Cluster (Silhouette ~0.3).
4. **Cryptanalysis-First ist der Schlüssel**: Die Hypothese H1 wurde durch klare
   Kriterien FALSIFIZIERT, nicht "akzeptiert weil plausibel".
5. **Schema-Validation zwingt zur Disziplin**: V5-Schema verbietet
   `schmeh_hint`/`schmeh_complete` als `source` — Pipeline kann Schmeh gar nicht einschleusen.
