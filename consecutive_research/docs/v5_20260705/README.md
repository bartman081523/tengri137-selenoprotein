# Tengri137 — V5 Cryptanalysis-First Reconstruction

**Generated:** 2026-07-05 (V5 Pipeline)  
**Schema:** v5.0 (V5 PIVOT: NO Schmeh, Kryptanalyse-First)  
**Source:** Tengri137.pdf (23 pages, unknown geometric script)  
**Processing run:** 20260705_V5

## V5 PIVOT — Was ist anders als V4?

**V4 (falsifiziert 2026-07-05):** Schmehs Klartext wurde als OCR-Ground-Truth missbraucht. 997 Glyphen, 456 lateinische Tokens, 75 fine-Cluster. Schema-validiert, aber **methodisch fundamental falsch**.

**V5 (Kryptanalyse-First):** Schmehs Daten komplett ignoriert. Pipeline:
1. **Phase 0** (DevMind): Inken-Substrat (16.797 Komponenten) ohne Glyph-Gruppierung
2. **Phase 1** (CryptanalysisMind): Shannon-Entropie, IoC, Zipf, N-Gramme
3. **Phase 2** (DevMind): Multi-Resolution-Embeddings + Constraint-Clustering (K aus Phase 1)
4. **Phase 3** (DevMind): Page-Layout-Klassifikation (Fließtext / Magic-Cube / Burumut / Chemie / Silhouette)
5. **Phase 4** (DevMind): Selektive OCR (Tesseract nur auf nicht-Tengri-Bereiche)
6. **Phase 5** (CryptanalysisMind): Substitutions-Validierung (H1 falsifiziert)
7. **Phase 6** (DevMind): Schema-validierte Finalisierung OHNE Schmeh

## Cryptanalysis-Report (Phase 1 + Phase 5)

- **H1-Hypothese:** wahrscheinlich_monoalphabetisch
- **H1-Status:** abgelehnt (F1-Score: -1)
- **Shannon-Entropie H:** 2.8706 bit/Zeichen (Englisch-Ref: 4.14)
- **Index of Coincidence:** 0.1606 (Englisch-Ref: 0.067)
- **Zipf α:** 2.9281 (Englisch-Ref: ≈1.0)

### F1-Falsifikations-Kriterien:

- F1.1 FAIL: IoC 0.1606 ∉ [0.055, 0.080] (Abweichung: 0.0936)
- F1.2 FAIL: H 2.8706 ∉ [3.8, 4.6]
- F1.3 FAIL: α 2.9281 ∉ [0.8, 1.2]
- F1.4 PASS: K=34 in [25, 35]
- F1.5 PASS: Keine lateinischen Tokens auf Fließtext-Pages (Tengri-only)

### Interpretation:

Der hohe IoC (0.1606 vs. Englisch 0.067) deutet auf eine ungewöhnlich repetitive Substrat-Struktur hin. Der Klartext scheint KEIN englisches Englisch zu sein. Mögliche Alternativen: (a) andere Sprache (Türkisch, Mongolisch), (b) numerische/templated Inhalte, (c) nicht-linguistisches System.

## Total-Statistik (V5)

- **Pages:** 23/23
- **Tengri-Glyph-Bboxen:** 997 (Phase 4 Input)
- **Distinkte Glyphen-Cluster (Phase 2):** 34 (Vorhersage aus Phase 1: [25, 35])
- **Lateinische Tokens (Phase 4):** 1097 (nur aus selektiver OCR)
- **Pages mit lateinischen Tokens:** 9/23

## Page-Layout-Verteilung (Phase 3)

| Layout-Typ | Anzahl Pages | Pages |
|---|---|---|
| fliesstext | 14 | p01, p02, p03, p04, p07, p08, p09, p10, p11, p12, p13, p14, p15, p16 |
| burumut_block | 4 | p17, p19, p20, p21 |
| magic_cube | 2 | p05, p06 |
| silhouette_formel | 2 | p18, p22 |
| chemie_struktur | 1 | p23 |

## Glyph-Alphabet (Phase 2)

**K = 34 distinkte Glyphen-Cluster** aus 997 Multi-Resolution-Embeddings (16+32+64 px) auf V4-Crops. Silhouette = 0.51. Cluster-Verteilung:

| Cluster-Range | n_occurrences |
|---|---|
| 1–5 | 179, 155, 117, 96, 78 |
| 6–10 | 53, 44, 39, 39, 38 |
| 11–15 | 26, 23, 16, 13, 10 |
| 16–20 | 9, 9, 8, 7, 6 |
| 21–25 | 5, 4, 4, 3, 3 |
| 26–30 | 3, 2, 2, 1, 1 |
| 31–34 | 1, 1, 1, 1 |

## V5 vs V4 Vergleich

| Metrik | V4 (falsifiziert) | V5 |
|---|---|---|
| Echte Glyph-Anzahl | 997 (Overclustering) | **34** Cluster (~26 + 10) |
| Lateinische Tokens | 456 (368 Schmeh-dominiert) | **1097** (selektive OCR) |
| Pages mit lateinischem Text | 22/23 (V4-Schmeh-Halluzination) | **9/23** (reale Formeln/Chemie) |
| Schmeh in Pipeline | ja (Hauptfehler) | **NEIN** |
| Methodik | OCR auf Crypto-Problem | **Crypto auf Crypto-Problem** |
| H1-Validierung | keine | **ABGELEHNT** (F1-Score: -1) |
| Magic-Cube-Realität | behauptet p22/p23 | **p05/p06** (Gemini-Korrektur) |
| Burumut-Realität | behauptet p23 | **existiert visuell nicht** (Schmehs Dechiffrierung) |
| p23 = Chemie | nein | **ja** (Cytosin/Thymin-Formeln) |
| p17-p22 = Burumut | nein | **ja, aber mit Primfaktorzerlegungen** (kein lateinischer Text) |

## Reproduzierbarkeit

- **Time-Stamp:** 20260705_V5
- **Schema:** `schemas/tengri137_document_v5.schema.json`
- **Pipeline-Scripts:** `phase0_substrat.py` bis `phase6_finalize_v5.py`
- **V1, V2, V3, V4 unangetastet** (Reproduzierbarkeits-Regel)
- **Schmeh-2017 roh_text.txt:** wird komplett ignoriert
- **Source für Falsifikation:** `Gemini-Prompt.txt` + `Gemini-Antwort.txt`
