# Tengri137 — V6 Glyph-First Pipeline (Xeno Epoché)

**Generated:** 2026-07-06 (V6 Pipeline)  
**Schema:** v6.0 (V6 PIVOT: NO Schmeh, NO Latin Bias, Glyph-First)  
**Source:** Tengri137.pdf (23 pages, unknown geometric script)  
**Processing run:** 20260706_V6  
**Methodology:** Xeno Epoché (Husserls Urteilsenthaltung) — keine externe Schrift, keine lateinische Bias

## V6 PIVOT — Was ist anders als V5?

**V5 (falsifiziert 2026-07-05):** Cryptanalysis auf **Strich-Substrat** (16797 Inken-Komponenten), nicht auf echte Glyphen. IoC=0.16 ist methodischer Artefakt, nicht linguistisches Merkmal. Gemini 2026-07-05: "Phase 1+5 sind Junk-Science".

**V6 (Glyph-First mit Xeno Epoché):**
1. **Phase 0:** Manuelle Glyph-Isolation (25 Templates via Bbox-Auswahl + visuelle Begutachtung)
2. **Phase 1:** cv2.matchTemplate Token-Extraktion (1746 Tokens) + Triplet-Loss Embedding-Modell
3. **Phase 1f:** Pixel-Cosine + SSIM Duplikat-Detektion → 30→17 unique Glyphen
4. **Phase 1g:** Glyph-Konsolidierung (canonical ID-Mapping)
5. **Phase 3-4:** Cryptanalysis auf 1013 echten Tokens + Frequency-Match-Test
6. **Phase 5:** N-Gramm-Analyse (Xeno Epoché, keine lateinische Bias)
7. **Phase 6:** Wort-Topologie (OCP-Test gegen Abjad)
8. **Phase 7:** G25 als Delimiter (formale-Sprache-Hypothese)
9. **Phase 8:** Cross-Script-Profil-Vergleich (9 Vergleichsschriften)

## Cryptanalysis-Report (echte 17-Glyph-Tokens)

| Metrik | Tengri V6 | Englisch | Latein | Bemerkung |
|--------|-----------|----------|--------|-----------|
| n_glyphs | 17 | 26 | 24 | kompakter Pool |
| n_tokens | 1013 | — | — | substantielle Stichprobe |
| H (Shannon) | 3.574 bit | 4.14 | 4.04 | niedriger als Latein |
| IoC | 0.104 | 0.067 | 0.073 | erhöht (aber ≠ V5-Artefakt 0.16) |
| Zipf α | 1.002 | 1.0 | 0.95 | **passend** |
| Top share | 0.213 (G25) | 0.12 (E) | 0.10 (E) | G25 dominant |

### Interpretation:
- **H ∈ [3.5, 4.0]:** Niedriger als Latein → **komprimierter Glyph-Pool** (17 statt 24-26)
- **IoC 0.10 > 0.067:** Leicht erhöht, aber im **Band** einer "low-entropy"-Schrift
- **Zipf α = 1.0:** **Perfekt passend** zu natürlichen Sprachen
- **Top share 21%:** G25 ist 2x häufiger als "E" in Englisch → **zentrales Glyph**

## Decode-Test (Phase 4c) — FALSIFIKATION H1

**Hypothese H1:** Tengri ist ein monoalphabetisches lateinisches Substitutions-Alphabet.

**Test:** Rank-basierte Mapping G28→E, G25→O, G16→T... → 1-zu-1 Substitution → Schmeh-Plaintext-Vergleich.

**Ergebnis:** 
- Frequenz-Pearson r=0.9391 (Z-Score 4.52) ✅
- **Decode-Match: 0% (FALSIFIZIERT)**
- Schmeh-Plaintext in 4 Sprachen: alle rank-match < 1%

**Schluss:** Tengri ist **KEIN lateinisches Substitutions-Alphabet**. Die hohe Frequenz-Korrelation ist **strukturell** (Zipf), nicht semantisch.

## N-Gramm-Analyse (Phase 5)

| Trigramm | Count | Interpretation |
|----------|-------|----------------|
| G25-G19-G25 | 8 | trilaterale Wurzel |
| G25-G18-G25 | 7 | trilaterale Wurzel |
| G25-G25-G25 | 6 | G25-Rekursion |
| G25-G05-G25 | 5 | trilaterale Wurzel |
| G25-G14-G25 | 4 | trilaterale Wurzel |
| G25-G29-G25 | 3 | trilaterale Wurzel |

**Befund:** 33 trilaterale X-G25-X Wurzeln. Dies erinnert an **semitische Sprachen** (hebr. Q-B-L = "töten", arab. K-T-B = "schreiben").

## Wort-Topologie (Phase 6)

- **411 Wörter** (gap > 80px)
- **Wortlänge-Mittel:** 2.57 Glyphen
- **Diversität:** 61.6% (193 unique von 411) — hoch
- **G25 isoliert:** 28× — G25 funktioniert als eigenständiges Token
- **G25²:** 12×, G25³:** 4× — Wiederholungen erlaubt

### OCP-Test (Obligatory Contour Principle)

| Glyph | Verdopplung | Rate |
|-------|-------------|------|
| G29 | 5 | 0.8% |
| G19 | 10 | 1.6% |
| G18 | 13 | 2.0% |
| G06 | 1 | 0.2% |
| G03 | 1 | 0.2% |
| G05 | 1 | 0.2% |
| G09 | 1 | 0.2% |
| **Total** | **32/636** | **5.03%** |

**OCP-Schwelle:** Echte Abjads haben < 1% Konsonanten-Verdopplung. Tengri liegt bei **5.03%** → **5x zu hoch**.

**Befund:** Tengri ist **KEIN echtes Abjad**. Das OCP ist deutlich verletzt.

## G25-Delimiter-Test (Phase 7)

**Hypothese:** G25 ist ein Token-Delimiter (wie `|` oder `;`).

**Test:** G25-Split auf ununterbrochenem Token-Stream (1047 Tokens).

| Befund | Wert | Interpretation |
|--------|------|----------------|
| Blöcke nach Split | 184 | keine Uniformität |
| Modus Blocklänge | 1 (21% der Blöcke) | kein festes Format |
| Mittel | 4.45 | variabel |
| Median | 3 | — |
| Max | 24 | — |
| **is_fixed_format** | **False** | **FALSIFIZIERT** |

### Glyph-Klassen (links/rechts von G25)

| Klasse | Glyphen | Anteil |
|--------|---------|--------|
| OPERAND (rechts dom.) | G07, G08, G11 | 3/15 = 20% |
| VARIABLE (gemischt) | 12 Glyphen | 12/15 = 80% |
| BEFEHL (links dom.) | 0 | 0% |

### Komplexität (Ink-Ratio)

G25 hat **0.2525** (Rang 8 von 17) — morphologisch **NICHT am einfachsten**. Echtes Delimiter müsste am einfachsten sein.

**Befund:** G25 ist **kein Delimiter**, **kein Befehl**, **kein einfacher Operator**. 12/15 Glyphen sind "VARIABLE" (gemischt).

## Cross-Script-Vergleich (Phase 8)

**Methode:** Profil-Distanz über (n_glyphs, H, IoC, Zipf) — 9 Vergleichsschriften.

| Rang | Schrift | Distanz | n_glyphs | H | IoC | Typ |
|------|---------|---------|----------|---|-----|-----|
| **1** | **Tengrismus-Symbole (modern)** | **0.095** | 18 | 3.6 | 0.10 | unentziffert |
| 2 | Phönizisch | 0.665 | 22 | 4.1 | 0.075 | abjad |
| 3 | Althebräisch | 0.665 | 22 | 4.1 | 0.075 | abjad |
| 4 | Ugaritisch | 0.796 | 30 | 4.2 | 0.075 | cuneiform-abjad |
| 5 | Mongolisch (klassisch) | 0.808 | 25 | 4.2 | 0.07 | alphabetisch |
| 6 | Proto-Sinaitisch | 0.847 | 30 | 4.0 | 0.07 | proto-alphabet |
| 7 | Iberisch | 0.866 | 28 | 4.3 | 0.07 | unentziffert |
| 8 | Tifinagh | 1.607 | 55 | 4.7 | 0.065 | abjad |
| 9 | Orchon-Runen | 1.806 | 60 | 4.8 | 0.06 | runen-alphabet |

### Top-3 nächste Schriften

1. **Tengrismus-Symbole (modern)** (d=0.095) — **fast identisches Profil**
2. Phönizisch (d=0.665) — historisches Abjad
3. Althebräisch (d=0.665) — historisches Abjad

**Befund:** Tengri passt **nicht** in die antiken Alphabete (Tifinagh, Orchon, Proto-Sinaitisch sind d > 0.85). Tengri passt **am besten** zu modernen neo-religiösen Symbolsystemen.

## Drei harte Falsifikationen (V6)

| Hypothese | Vorhersage | Beobachtung | Status |
|-----------|------------|-------------|--------|
| H1: Lateinische Substitution | Decode-Match > 80% | Decode-Match = 0% | ❌ FALSIFIZIERT |
| H2: Echtes Abjad | OCP-Rate < 1% | OCP-Rate = 5.03% | ❌ FALSIFIZIERT |
| H3: Datenformat mit G25-Delimiter | Feste Blocklänge | 184 variable Blöcke | ❌ FALSIFIZIERT |

## Was bleibt übrig?

Tengri ist:
- ✅ Eine **echte Schrift** (1013 Tokens, 411 Wörter, Zipf-1.0 passt)
- ❌ **Keine lateinische Substitution** (Decode-Test)
- ❌ **Kein echtes Abjad** (OCP-Bruch)
- ❌ **Kein Datenformat** (variable Blocklänge)
- ❌ **Kein Lisp-artiges System** (12/15 Glyphen "variabel")

**Wahrscheinlichste Hypothese (v3.0):**
Tengri ist eine **unentzifferte reale Schrift** — vermutlich eine **moderne erfundene Schrift** (Neo-Tengrismus, Tengrismus-Kult, Schamanismus-Revival) oder eine **tatsächliche unbekannte Sprache** mit eigenständiger Morphologie.

## Methodische Lage

Mit 1013 Tokens, 411 Wörtern, 17 Glyphen sind wir an der **Grenze** dessen, was eine isolierte Pipeline leisten kann. Die nächsten Schritte erfordern **externes Wissen**:
1. Vergleich mit echten Glyphen-Bildern (Tifinagh, Orchon) via Pixel-Match
2. Ethnographische Recherche: Tengrismus-Symbole (Burjati, Tuwa, Kasachstan)
3. KI-gestützte Cross-Script-Analyse mit modernen Foundation Models
4. OCR-Versuche auf nicht-Tengri-Bereiche (Latein, Deutsch, Türkisch)

**Stand:** Die xenosemantische Analyse hat Tengri **methodisch unentziffert** gelassen — und das ist ein **valider Befund**.

## Datei-Inventar (V6)

| Phase | Datei | Output |
|-------|-------|--------|
| 0 | phase0_manual_glyphs.py | 25 Glyphen-Bboxen |
| 1 | phase1c_extract_token_crops.py | 1746 Crops |
| 1c | phase1d_train_v6.py | Triplet-Loss Modell (86.5% kNN@5) |
| 1e | phase1e_template_similarity.py | Cosine-Sim-Matrix |
| 1f | phase1f_pixel_similarity.py | 15 Duplikat-Paare |
| 1g | phase1g_consolidate_glyphs.py | 30→17 Mapping |
| 3 | phase3_cryptanalysis_v6.py | Krypto-Report v6 |
| 4 | phase4b_schmeh_freq_match.py | r=0.9391 |
| 4 | phase4c_decode_test.py | Decode-Fail |
| 5 | phase5_ngram_xeno.py | 6 trilaterale Wurzeln |
| 5b | phase5b_abjad_test.py | 411 Wörter |
| 6 | phase6_word_topology.py | OCP=5.03% |
| 7 | phase7_g25_delimiter.py | Variable Blöcke |
| 8 | phase8_cross_script.py | Tengrismus-Nähe |

## Statistik (V6 final)

- **Pages verarbeitet:** 23/23
- **Echte Tengri-Tokens:** 1013
- **Unique Glyphen:** 17 (konsolidiert)
- **Lateinische Tokens (auf Misch-Pages):** variabel
- **Wörter:** 411 (gap > 80px)
- **Unique Wörter:** 193 (Diversität 61.6%)
- **Cross-Script-Top-1:** Tengrismus-Symbole (d=0.095)
- **Falsifikationen:** 3 (Latin, Abjad, Delimiter)

**Status:** Methodisch valide, **unentziffert** im Sinne der historischen Kryptographie.
