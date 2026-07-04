# Tengri137 — V2 Detailed Analysis
**Pipeline:** Embedding-Clustering + Triplet-Loss ML + Auto-Silhouette
**Processing Run:** `20260704_V2`
**Pipeline Version:** v2.0
**Generated:** 2026-07-04T00:00:00Z

---

## Document

- **Title:** Tengri137 - V2 Detailed Analysis
- **Page Count:** 23
- **Source PDF:** `Tengri137.pdf`
- **Description:** Detailed analysis of the Tengri137 PDF using embedding-based agglomerative clustering on 818 crops, multi-modal similarity (cosine + size + aspect), auto-silhouette threshold selection, and 23-page region structure with Vision-based symbol classification.

## Clustering

- **Method:** agglomerative_average_auto_silhouette
- **Threshold (t):** 0.400
- **Silhouette Score:** 0.753
- **Total Symbols:** 5
- **N Clusters:** 5
- **N Singletons:** 0
- **N Multi-member:** 5
- **Distance Weights:** {'embedding': 0.7, 'size': 0.15, 'aspect': 0.15}
- **Ordering:** Reihenfolge des ersten Auftretens im Fließtext; Seite 1 oben-links (0,0) nach unten-rechts lesend.

## ML-Eval (5-fold Cross-Validation)

| k | Accuracy (mean ± std) |
|---|---|
| k=1 | 0.947 ± 0.015 |
| k=3 | 0.953 ± 0.016 |
| k=5 | 0.956 ± 0.015 |

- **Total Samples:** 818
- **N Classes:** 5
- **N Clusters (post-clustering):** 5

## Top-20 Häufigste Symbole (nach Occurrences, aggregiert über alle Pages)

| Cluster | Vorkommen | Vision-Kind | Description | Erste Seite |
|---|---|---|---|---|
| `GEOM_LATIN_PRINT_0005` | 258 | image | A horizontal code-like sequence showing digits '6', '14', an | p05 |
| `GEOM_LATIN_PRINT_0002` | 248 | geometric_circle | Thick, irregular black ring with an oval-shaped white hole i | p01 |
| `GEOM_LATIN_PRINT_0001` | 152 | image | A stylized decorative letter 'R' (or 'B') formed by a tower- | p02 |
| `GEOM_LATIN_PRINT_0003` | 152 | image | A circular illustration containing multiple elements: a sun  | p02 |
| `GEOM_GEOMETRIC_CIRCLE_0004` | 6 | chinese_seal_script | A rectangular seal-script style glyph with two horizontal ba | p03 |
| `GEOM_UNMATCHED_0000` | 2 | latin_print | Red bold lowercase letters 'rhJ' in a thick sans-serif font, | p05 |

## Page-Übersicht

| Page | Regions | Symbole | Wörter | Klassifikationen (Top-3) |
|---|---|---|---|---|
| p01 | 20 | 2 | 138 | footer=1, geometric_circle=1, latin_print=1 |
| p02 | 44 | 27 | 127 | footer=1, image=11, stick_figure=3 |
| p03 | 82 | 57 | 162 | footer=1, mixed_media=2, image=14 |
| p04 | 19 | 0 | 181 | footer=1, text_line=18 |
| p05 | 74 | 63 | 39 | footer=1, image=20, latin_print=11 |
| p06 | 71 | 63 | 39 | latin_print=17, image=15, red_label_stenographic=9 |
| p07 | 58 | 46 | 70 | footer=1, image=21, geometric_circle=8 |
| p08 | 114 | 108 | 60 | footer=1, geometric_circle=29, image=50 |
| p09 | 197 | 183 | 116 | footer=1, image=115, mixed_media=6 |
| p10 | 34 | 10 | 202 | footer=1, image=1, face_circle_three_dots=9 |
| p11 | 37 | 20 | 167 | footer=1, image=2, stick_figure=1 |
| p12 | 16 | 8 | 73 | face_circle_three_dots=6, image=2, text_line=8 |
| p13 | 33 | 13 | 175 | footer=1, face_circle_three_dots=11, geometric_circle=1 |
| p14 | 38 | 17 | 143 | footer=1, latin_print=4, face_circle_three_dots=13 |
| p15 | 36 | 14 | 187 | footer=1, face_circle_three_dots=14, text_line=21 |
| p16 | 129 | 113 | 142 | footer=1, prime_digit=10, latin_print=28 |
| p17 | 35 | 1 | 224 | footer=1, image=1, text_line=33 |
| p18 | 35 | 1 | 246 | footer=1, face_circle_three_dots=1, text_line=33 |
| p19 | 29 | 0 | 167 | footer=1, text_line=28 |
| p20 | 43 | 4 | 313 | footer=1, chinese_seal_script=1, image=1 |
| p21 | 51 | 18 | 202 | footer=1, unknown=9, chinese_seal_script=6 |
| p22 | 76 | 50 | 192 | footer=1, image=27, chinese_seal_script=13 |
| p23 | 44 | 0 | 312 | header=1, footer=1, text_line=42 |

## Region-Klassifikationen (global)

| Classification | Count |
|---|---|
| text_line | 484 |
| image | 316 |
| latin_print | 114 |
| face_circle_three_dots | 103 |
| geometric_circle | 75 |
| chinese_seal_script | 37 |
| red_label_stenographic | 34 |
| prime_digit | 22 |
| footer | 21 |
| unknown | 18 |
| geometric_diamond | 16 |
| stick_figure | 15 |
| dash_frac_bar | 15 |
| geometric_bracket | 11 |
| mixed_media | 9 |
| address_hex | 7 |
| geometric_circle_with_cross | 5 |
| chinese_oracle_script | 3 |
| math_pi | 2 |
| geometric_circle_with_dot | 2 |
| turkic_round_rune | 2 |
| colored_region | 2 |
| geometric_filled_square | 1 |
| header | 1 |

## Vision-Beschreibungen (Page-Level)

## Unklare Bereiche (`uncertain[]`)

_(Keine unsicheren Bereiche gemeldet)_

## Reproduzierbarkeit

Alle Outputs sind mit Zeitstempel-Ordnern organisiert; vorherige Läufe bleiben unangetastet (siehe CLAUDE.md).

### Re-Run der kompletten Pipeline

```bash
TS=20260704_V2

# Phase 1 (idempotent)
python3 phase1_pixel.py --out bbox/pages_pixel_$TS

# Phase 2 v2 — Vision-Fix + alle 818 Crops
python3 phase2_vision_v2.py \
  --pixel bbox/pages_pixel_$TS \
  --schemas bbox/schemas_20260704_075228/ \
  --out bbox/vision_qa_$TS --workers 4 --n-top-glyphs 999

# Phase 3 v2 — regions-Struktur
python3 phase3_merge_v2.py \
  --pixel bbox/pages_pixel_$TS \
  --vision bbox/vision_qa_$TS \
  --out bbox/pages_merged_$TS

# Phase 4a — Embedding
python3 phase4a_embed_crops.py \
  --crops bbox/crops \
  --model models/symbols_20260704_075228/model.pt \
  --out bbox/embeddings_$TS

# Phase 4b — Auto-Silhouette Clustering
python3 phase4b_cluster_symbols.py \
  --embeddings bbox/embeddings_$TS \
  --vision bbox/vision_qa_$TS \
  --out bbox/symbols_global_$TS

# Phase 5 v2 — Schema-Validation + Final
python3 phase5_finalize_v2.py \
  --pages bbox/pages_merged_$TS \
  --symbols bbox/symbols_global_$TS/symbols_index.json \
  --schema schemas/tengri137_document.schema.json \
  --out bbox/final_$TS \
  --toplevel Tengri137_detailed_$TS \
  --processing-run $TS

# Phase 6 v2 — Triplet-Loss + Augmentations
python3 phase6_train_v2.py \
  --embeddings bbox/embeddings_$TS \
  --symbols bbox/symbols_global_$TS/symbols_index.json \
  --crops bbox/crops \
  --init-model models/symbols_20260704_075228/model.pt \
  --out models/symbols_$TS \
  --epochs 30 --bs 32

# Eval + Inference
python3 eval_v2.py --model-dir models/symbols_$TS \
  --symbols bbox/symbols_global_$TS/symbols_index.json

python3 models/symbols_$TS/inference.py \
  --model-dir models/symbols_$TS \
  --crops bbox/crops/p01_blank_000.png

# README regenerieren
python3 generate_readme.py \
  --doc Tengri137_detailed_$TS/doc.json \
  --symbols bbox/symbols_global_$TS/symbols_index.json \
  --eval models/symbols_$TS/eval.json \
  --out Tengri137_README_$TS.md
```

## Inference-Usage

Predict cluster_id for new crops:

```bash
python3 models/symbols_20260704_V2/inference.py \
  --model-dir models/symbols_20260704_V2 \
  --crops bbox/crops/p01_blank_000.png
```

Output: `cluster_id`, Top-3 mit Wahrscheinlichkeiten, `uncertain`-Flag.

---

**V2-Pipeline-Status:** ✓ Reproducible. Alle Outputs mit Zeitstempel-Ordner, frühere Läufe (TS=20260704_075228) bleiben unangetastet.
