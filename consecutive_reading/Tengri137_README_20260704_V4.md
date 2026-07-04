# Tengri137 — V4 Glyph-First Mixed-Media Reconstruction

**Generated:** 2026-07-04 (V4 Pipeline)  
**Schema:** v4.0 (V4 PIVOT: no Tesseract for glyphs)  
**Source:** Tengri137.pdf (23 pages, unknown geometric script)  
**Processing run:** 20260704_V4  

## V4 Pipeline-Übersicht

```
Phase 1 v4: Inken-Components + Layout (NO Tesseract)
Phase 2 v4: Glyph-Gruppierung + Zeilen-Regionen
Phase 3 v4: Zeilenweiser Vision-Quercheck
Phase 4 v4: Region-Building mit Glyph-Indexen
Phase 5 v4: Multi-Resolution-Glyph-Embeddings (16+32+64)
Phase 6 v4: 3-Level-Glyph-Clustering (coarse/medium/fine)
Phase 7 v4: Finalisierung mit Glyph-Indexen
Phase 8 v4: Multi-Resolution-Triplet-Loss (optional)
```

## Total-Statistik

- **Pages:** 23/23
- **Regions:** 469
- **Glyphs:** 997 (max glyph_index=997)
- **Latin-Tokens:** 456
- **Vision-matched glyphs:** 255

## Glyph-Index-Übersicht pro Page

| Page | Regions | Glyphen | Latin | Glyph-Index-Range | Schmeh ✓ |
|------|---------|---------|-------|-------------------|----------|
| p01 | 19 | 29 | 21 | 1–29 | ✗ |
| p02 | 19 | 34 | 19 | 30–63 | ✗ |
| p03 | 22 | 43 | 21 | 64–106 | ✗ |
| p04 | 20 | 26 | 22 | 107–132 | ✗ |
| p05 | 30 | 116 | 10 | 133–248 | ✗ |
| p06 | 32 | 121 | 4 | 249–369 | ✗ |
| p07 | 16 | 27 | 10 | 370–396 | ✗ |
| p08 | 20 | 67 | 7 | 397–463 | ✗ |
| p09 | 13 | 18 | 11 | 464–481 | ✗ |
| p10 | 23 | 38 | 13 | 482–519 | ✗ |
| p11 | 23 | 55 | 26 | 520–574 | ✗ |
| p12 | 24 | 45 | 26 | 575–619 | ✗ |
| p13 | 22 | 54 | 24 | 620–673 | ✗ |
| p14 | 22 | 56 | 26 | 674–729 | ✗ |
| p15 | 21 | 48 | 25 | 730–777 | ✗ |
| p16 | 19 | 38 | 21 | 778–815 | ✗ |
| p17 | 18 | 24 | 26 | 816–839 | ✗ |
| p18 | 18 | 24 | 0 | 840–863 | ✓ |
| p19 | 22 | 26 | 31 | 864–889 | ✗ |
| p20 | 18 | 43 | 17 | 890–932 | ✗ |
| p21 | 14 | 16 | 14 | 933–948 | ✗ |
| p22 | 16 | 19 | 17 | 949–967 | ✗ |
| p23 | 18 | 30 | 65 | 968–997 | ✗ |

## 3-Level-Clustering (Phase 6)

| Level | Threshold | Silhouette | Cluster | Singletons | Multi-Member |
|-------|-----------|------------|---------|------------|--------------|
| coarse | 0.600 | 0.495 | 3 | 0 | 3 |
| medium | 0.250 | 0.559 | 24 | 1 | 23 |
| fine | 0.100 | 0.649 | 75 | 10 | 65 |

## ML-Model (Phase 8 — optional)

```json
{
  "final_train_loss": 0.289655352460927,
  "final_val_accuracy": 0.7040816326530612,
  "n_samples": 997,
  "n_classes": 24,
  "rounds": 2,
  "epochs_per_round": 20
}
```

## Schmeh-Validation (HINT, NOT truth)

- **Glyph-Pages match:** 23/23
- **Latin-Pages match:** 1/23
- **Pages with known issues:** 22/23

### Known Issues (Schmeh vs V4):

- p01: V4 found MORE latin tokens (21) than Schmeh hints (16)
- p02: V4 found MORE latin tokens (19) than Schmeh hints (14)
- p03: V4 found MORE latin tokens (21) than Schmeh hints (16)
- p04: V4 found MORE latin tokens (22) than Schmeh hints (17)
- p05: V4 found MORE latin tokens (10) than Schmeh hints (4)
- p06: V4 found MORE latin tokens (4) than Schmeh hints (1)
- p07: V4 found MORE latin tokens (10) than Schmeh hints (2)
- p08: V4 found MORE latin tokens (7) than Schmeh hints (2)
- p09: V4 found MORE latin tokens (11) than Schmeh hints (8)
- p10: V4 found MORE latin tokens (13) than Schmeh hints (6)
- p11: V4 found MORE latin tokens (26) than Schmeh hints (10)
- p12: V4 found MORE latin tokens (26) than Schmeh hints (19)
- p13: V4 found MORE latin tokens (24) than Schmeh hints (18)
- p14: V4 found MORE latin tokens (26) than Schmeh hints (19)
- p15: V4 found MORE latin tokens (25) than Schmeh hints (18)
- p16: V4 found MORE latin tokens (21) than Schmeh hints (15)
- p17: V4 found MORE latin tokens (26) than Schmeh hints (17)
- p19: V4 found MORE latin tokens (31) than Schmeh hints (16)
- p20: V4 found MORE latin tokens (17) than Schmeh hints (16)
- p21: V4 found MORE latin tokens (14) than Schmeh hints (13)
- p22: V4 found FEWER latin tokens (17) than Schmeh hints (19)
- p23: V4 found MORE latin tokens (65) than Schmeh hints (30)

## V4 PIVOT von V3 — Was ist anders?

| Aspekt | V3 (alt) | V4 (neu) |
|--------|----------|----------|
| **Tesseract für Glyphen** | ja (mit Müll) | **NEIN** |
| **Glyph-Identifikation** | text_word (Tesseract) | **glyph_index (1-basiert, global)** |
| **Glyph-Struktur** | symbol_instance | **glyph_instance + components[]** |
| **Embeddings** | 64-dim (V2) | **192-dim (16+32+64)** |
| **Clustering** | 1 Level | **3 Levels (coarse/medium/fine)** |
| **Layout-Analyse** | nur via OCR | **via DBSCAN auf Centroiden** |
| **Schmeh-Validation** | keine | **V4-Output vs Schmeh-Hint (HINT)** |

## Reproduzierbarkeit

- **Time-Stamp:** 20260704_V4
- **Schema:** `schemas/tengri137_document_v4.schema.json`
- **Pipeline-Scripts:** `phase1_pixel_v4.py` bis `phase7_finalize.py`
- **V1/V2/V3 unangetastet** (Reproduzierbarkeits-Regel)
- **Schmeh raw_text.txt als HINT, nicht Wahrheit**
