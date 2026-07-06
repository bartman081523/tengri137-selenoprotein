# Tengri137 V8 — Glyph→English Complete Reproduction Pipeline

**Datum:** 2026-07-06
**Status:** ABGESCHLOSSEN — alle 8 Phasen durchgeführt

---

## Übersicht

V8-Pipeline versucht, **alle 23 Wikia-Plaintexte** mit den **17 V6-Glyphen** zu reproduzieren. Empirisches Ergebnis: **Tengri ist KEIN 1:1-lateinisches Substitutions-Alphabet**, sondern eine **eigenständige semantische Symbol-Schrift**.

## Outputs

```
bbox/
├── wikia_plaintexts_20260706_V8/    # Phase 0: 23 Wikia-Plaintexte + PGP-Verifikation
├── originals_compare_20260706_V8/   # Phase 1: Original-PNGs vs pages_png
├── align_wikia_20260706_V8/         # Phase 2: Token-Alignment
├── test_substitution_20260706_V8/   # Phase 3: Substitution-Tests
├── align_syllables_20260706_V8/     # Phase 4: Silben-Tests
├── template_matcher_20260706_V8/    # Phase 5: Konsolidierte Match-Tabelle
├── model_v8_20260706_V8/            # Phase 6: Trainings-Datensatz
└── final_20260706_V8/               # Phase 7: Mapping-Tabelle + Report
```

## Wichtigste Befunde

1. **Wikia-Plaintexte (23 Stück)** sind die einzige bekannte Quelle für die englischen Texte
2. **V6-Pipeline funktioniert auf höher-auflösenden Original-PNGs** (98.8% Bbox-Match)
3. **17 V6-Glyphen ≠ 22 distinkte lateinische Buchstaben** (mit Wikia-Regeln) — 1:1-Mapping unmöglich
4. **1 Glyph ≈ 7 lateinische Buchstaben** (N-Gramm-Test 7/8 Seiten)
5. **Pseudo-Schrift-Hypothese BESTÄTIGT** — Tengri ist semantisch, nicht orthographisch

## Vollständiger Report

Siehe: `bbox/final_20260706_V8/reproduction_report.md`

## Reproduzierbarkeit

```bash
TS=20260706_V8
python3 phase0_extract_wikia.py --out bbox/wikia_plaintexts_$TS
python3 phase1_originals_compare.py --out bbox/originals_compare_$TS
python3 phase2_align_wikia.py --out bbox/align_wikia_$TS
python3 phase3_substitution_tests.py --out bbox/test_substitution_$TS
python3 phase4_syllable_test.py --out bbox/align_syllables_$TS
python3 phase5_originals_matching.py --out bbox/template_matcher_$TS
python3 phase6_build_dataset.py --out bbox/model_v8_$TS
python3 phase7_finalize.py --out bbox/final_$TS
```
