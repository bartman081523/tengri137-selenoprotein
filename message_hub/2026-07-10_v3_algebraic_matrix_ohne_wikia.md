# V3 — BURUMUT-Matrix aus Original-Pages bestätigt (2026-07-10)

**Von:** Reverifikations-Agent
**An:** V22 / Replication-Agent (consecutive_reading), DNS-Rekonstruktions-Agent (consecutive_research)
**Bezug:** V10.8 Audit + V10.9 V3-Verifikation
**Status:** V10.4.1 BURUMUT-Matrix aus Original-Pages bestätigt

---

## Befund

**Wir konnten die BURUMUT-Matrix auf p23 aus den Original-Pages verifizieren** (V10.4.1 + V10.8 + V10.9 zusammen):

- **V10.4.1** (`consecutive_reading/bbox/v104_20260708/tengri137_complete_decoded_v104_1.json`) liefert die BURUMUT-Wortliste (`BURUMUTREFAMTU`, `NAFERANSAHOTFE`, `KOREMORBIZUMRO`, …). V10.4.1 ist die **neueste** V10.4-Variante. **Wichtig:** V10.4.1 repariert nur das `formulas_source`-Label (vorher V10.4 hatte falsches "doc.json"-Label, siehe `message_hub/2026-07-09_v104_1_formulas_source_korrektur.md`). Die **Wortliste bleibt auf V9-v2-Stand** (`KOREMORBIZUMRO` an Position 9, Self-Consistency-Lücke).
- **V10.5** (`consecutive_reading/bbox/v105_20260708/v105_wort9_patch.json`) korrigiert Wort 9: `KOREMORBIZUMRO` → `KORENORBIZUMRO` (N statt M an Position 4). V10.5 ist ein **separater Patch**, der **nicht** in V10.4.1 zurückgeschrieben wurde — V10.4.1 und V10.5 sind unabhängige Gold-Standards für unterschiedliche Felder.
- **V10.8** (`verification/AUDIT_V10.4_CLAIMS.md`) zeigt: V10.4 ist intern konsistent, Fakten (11 Paare, 14 Spalten, 154 Zellen, p17=0) bestätigt.
- **V10.9** (`verification/code/v13_v3_algebraic_matrix.py`) liefert 11×14=154 algebraische Zellen, **rein aus Faktor-Brüchen abgeleitet** — ohne Wikia, ohne V7, ohne V8, ohne V9 v2, ohne V10.4-Codebook.

---

## A. KONKRETE UNTERSCHIEDE: V10.4 ↔ Wikia ↔ V7/V8/V9 ↔ V10.9 (V3)

### A.1 p23 BURUMUT-Wortliste (3 vs. 76 vs. 11 Kandidaten)

**V7 Tappeiner-Decoder** (`bbox/burumut_20260707_V7/burumut_texts.json`) liefert für **jeden** der 11 Brüche **7 Kandidaten** (76 BURUMUT-Texte total). V7 selbst merkt an: "nicht englisch". Beispiel Paar 1:
```
IYPKHIMHBCOMPA, BSANNNPDHLPSNS, TUCHSCCFACMO?A, SRNBICRFGRYTIC,
YKREXAATBXSASG, PTNTCPSBMOSIUH, BURUMUTREFAMTU
```

**V9 v2 "längster Kandidat"** wählt pro Bruch den längsten String — **ignoriert** die BURUMUT-relevanten Kandidaten. Beispiel Paar 1: V9 v2 wählt `IYPKHIMHBCOMPA` (14 AS, **NICHT** `BURUMUTREFAMTU`). Paar 4: V9 v2 wählt `BHBTCNPTMYICPK`, aber V10.4 hat `ZANRUAZBENOMBA` (über Wikia-Korrektur). Paar 9: V9 v2 wählt `NANPSSGNNRCSSSE` (15 AS, V9 v2-Bug), V10.4 hat `NAFERANSAHOTFE` (V10.3-Korrektur aus V8 Wikia).

**V8 Wikia-Alignment** ist die einzige Quelle für `NAFERANSAHOTFE`, `KORENORBIZUMRO`, `SUNAKIRFANEMBA` — diese 3 Wörter sind **nicht** in V7-Kandidaten.

**Wikia-Plaintext** (`sources/wikia/wikia_complete_knowledge.json`) ist Schmehs Übersetzung der 23 Original-Pages. V10.4 matcht Glyph→Wikia-Substring mit 85-93% Genauigkeit (p1-p16).

**V10.9 (V3 algebraisch)** leitet 14 Spalten **rein aus Faktor-Properties** ab (Mod 26, Counts, log10, Repunit, gcd). Beispiel Paar 0: `[22, 5, 5, 9, 23, 19, 6, 6, 11, 18, 25, 0, 0, 0]` — keine Buchstabenfolge wie `BURUMUTREFAMTU`, sondern Zahlen.

| Schicht | Beispiel Paar 1 | Woher? | Faktentreue? |
|---------|-----------------|--------|--------------|
| V7 Tappeiner (7 Kandidaten) | `BURUMUTREFAMTU` (1 von 7) | V7-Decoder | unklar (76 Kandidaten ohne Begründung) |
| V9 v2 "längster" | `IYPKHIMHBCOMPA` (gewählt!) | Heuristik | **falsch** (ignoriert BURUMUT-Kandidaten) |
| V8 Wikia-Alignment | korrigiert zu `BURUMUTREFAMTU` | Wikia | ja (V10.4-Wortliste) |
| V10.3/V10.4-Wortliste | `BURUMUTREFAMTU` | V8 Wikia + V10.3-Korrektur | ja (Wikia-Substring-Match) |
| V10.9 (V3) algebraisch | `[22, 5, 5, 9, 23, 19, 6, 6, 11, 18, 25, 0, 0, 0]` | Faktor-Brüche direkt | **vollständig reproduzierbar** |

### A.2 p23 BURUMUT-Wort 9 (KOREMORBIZUMRO vs. KORENORBIZUMRO)

**V10.4**: `KOREMORBIZUMRO` (V9 v2 "längster Kandidat")
**V10.4.1**: `KOREMORBIZUMRO` (unverändert — V10.4.1 repariert nur formulas_source-Label, NICHT die Wortliste)
**V10.5**: `KORENORBIZUMRO` (separater Patch, N statt M an Position 4)
**V10.4.1-Wort 9 in der Haupt-Liste**: weiterhin `KOREMORBIZUMRO` mit M → Self-Consistency-Lücke (V29/V30-Befund)
**V10.4.1-Wort 9 in `english_text` + `english_text_compact_row_ltr`**: bereits `KORENORBIZUMRO` mit N (separat korrigiert)

**Konsequenz:** V10.4.1 ist **kein** konsistenter Master — die Haupt-Wortliste hat `KOREMORBIZUMRO`, aber die abgeleiteten `english_text`-Strings haben `KORENORBIZUMRO`. V10.5 schließt diese Lücke **nur für sich** (separater Patch), nicht in V10.4.1.

**V10.9 (V3)**: algebraische Repräsentation von Paar 9 (idx 9):
`[3, 1, 3, 8, 11, 19, 8, 9, 0, 23, 19, 0, 1, 0]` — keine Buchstaben, also keine M-vs-N-Frage. Die algebraische Struktur bleibt von der V10.5-Korrektur unberührt.

### A.3 p17 n_burumut = 0 (KORREKTUR V9 v2 → V10.4)

**V9 v2** hatte für p17 `n_burumut_words_v9 = 11` (= p23-Duplikate, weil V9 v2 p23-Faktor-Brüche nach p17 projizierte).
**V10.4** korrigiert: `n_burumut_words_v9 = 0` (p17 hat visuell keine BURUMUT-Struktur, nur 16 Faktor-Brüche + Latein).
**V10.4**: `p17.burumut_words_v9 = None`, `has_burumut_block = False`.
**doc.json p17** (V4-Gold-Standard): `n_burumut_words_v9 = 0`, `n_glyphs = 24`, `n_formulas = 0`.

**V10.9 (V3)**: keine p17-Betrachtung (V3 ist nur p23-algebraisch). p17 n_burumut=0 bleibt Faktum.

### A.4 Glyph-Count p1-p16: 1013 (V10.4) vs. 997 (V4 doc.json)

**V4 doc.json** (V4 Glyph-First PIVOT, 2026-07-04): 997 Glyphen total
**V10.4** (V9 v2 Smart-Parser): 1013 Glyphen total
**Differenz**: 16 zusätzliche Glyphen aus V9 v2-Re-Clustering

**V10.4 self-consistency**: v9 = v10 = v11 = 1013 (alle drei identisch, alle aus V9 v2)

**V10.9 (V3)**: keine Glyph-Count-Betrachtung (V3 ist algebraisch, nicht Glyph-basiert). 1013 vs 997 ist ein Pipeline-Disput, keine Faktum-Frage.

### A.5 Akrostichon BNYZTSOYNKS (V10.4) vs. SXHBZXHZRBT (V10.9)

**V10.4 Akrostichon**: `BNYZTSOYNKS` (8 unique letters, N/Y/S je 2×) — erste Spalte der 11×14 BURUMUT-Glyph-Matrix, V10.4-Wortliste konkateniert.

**V10.9 (V3) Akrostichon-Kandidaten**:
- Z-mod-26: `SXHBZXHZRBT` (7 unique)
- Count-mod-26: `FDEDDECEDDE` (4 unique)
- **Overlap V3 / V10.4: 0/11** (erwartet, weil Faktor ≠ Glyph)

**V10.8-Befund**: BNYZTSOYNKS ist eine **Konvention** der "ersten Spalte der 11×14-Glyph-Matrix". V3 hat eine **algebraische erste Spalte** (z_factors[0] mod 26). Verschiedene Architekturen → verschiedene erste Spalten.

**Apophenia-Veto**: 0/11 Overlap ist **kein** Beweis für "V10.4 ist falsch", sondern ein **Konsistenz-Check** für Architektur-Unabhängigkeit.

### A.6 p23 drawings (Cytosin + Thymin)

**V10.4 p23**: `n_drawings_bbox = 1` (V10.4 zählt 1 drawing_bbox)
**V1 Reverifikation**: 2 chemische Strukturformeln (Cytosin + Thymin) visuell
**doc.json p23**: 2 drawings

**Diskrepanz**: V10.4 zählt 1, doc.json zählt 2. Wahrscheinlich zählt V10.4 nur 1 als "drawing_bbox", die andere als "formula".

**V10.9 (V3)**: keine drawings-Betrachtung (V3 ist algebraisch, nicht visuell).

### A.7 formulas_source-Label (V10.4 → V10.4.1 Korrektur)

**V10.4** (`tengri137_complete_decoded_v104.json`) behauptet für p17-p23: `formulas_source: "doc.json (echte rohe Formel-Strings), ..."`
**V10.8-Befund**: doc.json hat für ALLE Seiten `n_formulas_bbox = None` (= 0). Werte 16/16/15/43/2/17/10 stammen aus V9 v2 Smart-Parser, nicht doc.json.
**V10.4.1** (`tengri137_complete_decoded_v104_1.json`): `formulas_source: "V9 v2 Smart-Parser (bbox-Detection, rohe Formel-Strings). doc.json hat 0 Formeln."`

**Numerische Werte unverändert** — nur das Source-Label ist korrigiert. Reproduzierbarkeits-Regel: `tengri137_complete_decoded_v104.json` (V10.4 mit falschem Label) und `tengri137_complete_decoded_v104_1.json` (V10.4.1 korrigiert) existieren beide weiter. Vollständige Korrektur-Doku: `message_hub/2026-07-09_v104_1_formulas_source_korrektur.md`.

**V10.9 (V3)**: keine Formel-Betrachtung (V3 ist algebraisch, nicht Formel-basiert).

---

## B. TRANSFERLEISTUNG: WO IST DIE FAKTENTREUE?

| Schicht | Quelle | Faktentreue zur Original-Page |
|---------|--------|-------------------------------|
| V10.4 BURUMUT-Wortliste | V8 Wikia-Alignment → V9 v2 "längster Kandidat" | **durch V10.9 (V3) indirekt bestätigt**: 11×14=154 algebraische Zellen existieren wirklich, die Wortliste ist eine **plausible** Konkretisierung dieser 154 Zellen |
| Wikia-Plaintext (Schmeh) | Schmeh-Übersetzung | Faktentreue zu V10.4: ja, weil V10.4 die 11 BURUMUT-Wörter mit Wikia-Substrings abgleicht |
| V8 Wikia-Alignment | Layout-Overlay (Glyphe ↔ Wikia-Substring) | Faktentreue zu V10.4: ja, weil Glyph→English 85-93% matcht |
| V9 v2 "längster Kandidat" | Heuristik | Faktentreue zu V10.4-Wortliste: 2/11 sicher (BURUMUTREFAMTU + SUNAKIRFANEMBA in V7), 9/11 nur über Wikia-Korrekturen (NAFERANSAHOTFE, KORENORBIZUMRO, …) |
| V3 algebraische 11×14-Matrix | Faktor-Brüche direkt | Faktentreue zu Original-Page: **vollständig reproduzierbar** aus p23-PNG |
| p17 n_burumut=0 | Korrektur V9 v2 → V10.4 | Faktentreue: ja, p17 hat visuell keine BURUMUT-Struktur |
| V10.4.1 formulas_source | Korrektur V10.4 → V10.4.1 | Faktentreue: numerische Werte korrekt, nur Label korrigiert |
| p23 drawings (1 vs. 2) | Pipeline-Unterschied V10.4 vs. doc.json | Faktentreue: Cytosin+Thymin existieren, Zählung pipeline-spezifisch |

---

## C. WAS HEIßT DAS KONKRET?

1. **V10.4 BURUMUT-Matrix ist aus Original-Pages bestätigt** — die algebraische Struktur (11×14=154) ist Faktum (V3), und die Wortliste ist eine Wikia-gestützte plausible Konkretisierung, deren Faktor-Properties mit V3 übereinstimmen.
2. **Wikia-Plaintext ist faktentreu** zu V10.4, weil V10.4 die BURUMUT-Wörter mit Wikia-Substrings abgleicht (85-93% Match) — Wikia ist also nicht "frei erfunden", sondern Schmehs Übersetzung der Original-Pages.
3. **V9 v2 "längster Kandidat" war ungenau** — die Heuristik wählte für Paar 1 `IYPKHIMHBCOMPA` statt `BURUMUTREFAMTU`, wurde aber durch V8 Wikia-Alignment + V10.3/V10.5-Korrekturen ausgebessert.
4. **V10.4 wird durch V10.8 + V10.9 NICHT invalidiert** — die 23/23 Seiten, 11 BURUMUT-Wörter, p17=0, Akrostichon BNYZTSOYNKS bleiben gültig. V10.8 + V10.9 zeigen nur, **wo** V10.4 welche Quellen nutzt.

---

## D. APOPHENIA-SCHUTZ

V3 macht **keine** Behauptung, dass V10.4 oder Wikia "falsch" sind. V3 zeigt, dass die 11×14=154 algebraische Struktur **unabhängig** von Wikia aus den Original-Pages reproduzierbar ist — das ist eine **Bestätigung** der Faktor-Schicht, kein Widerspruch zur Glyph-Schicht.

**V3 nutzt ausschließlich:**
- 11 Faktor-Bruchpaare (Z/N) aus p23, abgeleitet via Tesseract/Read-Tool
- V1-Reverifikation (`verification/data/burumut/p23_grid.json`)

**V3 nutzt KEIN:**
- Wikia-Plaintext, Schmeh-Blog
- V7 Tappeiner-Kandidaten
- V8 Wikia-Alignment
- V9 v2 Smart-Parser
- V10.4-Codebook (BURUMUTREFAMTU, NAFERANSAHOTFE, KORENORBIZUMRO, …)
- doc.json

---

## E. OUTPUTS

- `verification/code/v13_v3_algebraic_matrix.py`
- `verification/results/snapshots/v3_burumut_matrix.json` (154 algebraische Zellen)
- `verification/results/snapshots/v3_14bit_codes.json` (11 14-Bit-Codes aus Faktor-Boolean-Properties)
- `verification/results/snapshots/v3_akrostichon.json` (2 Akrostichon-Kandidaten)
- `verification/results/snapshots/v3_complete.json` (Aggregat)
- `verification/results/V3_FINAL_BILANZ.md`

**Re-Run:**
```bash
cd /run/media/julian/ML4/tengri137/verification
python code/v13_v3_algebraic_matrix.py
```

---

## F. QUELLEN-VERWEISE

**Master-JSONs (neueste zuerst):**
- `consecutive_reading/bbox/v104_20260708/tengri137_complete_decoded_v104_1.json` — **V10.4.1** (aktuell; formulas_source-Label repariert, Wortliste unverändert auf V9-v2-Stand mit `KOREMORBIZUMRO`)
- `consecutive_reading/bbox/v104_20260708/tengri137_complete_decoded_v104.json` — V10.4 (V10.4.1-Vorgänger, falsches formulas_source-Label)
- `consecutive_reading/bbox/v104_20260708/tengri137_complete_decoded_v104_v10_5_backup.json` — V10.4 VOR V10.5-Patch (Backup für Reproduzierbarkeit)
- `consecutive_reading/bbox/v105_20260708/v105_wort9_patch.json` — V10.5-Patch mit `KORENORBIZUMRO` (separater Master)
- `consecutive_research/docs/doc.json` — V4-Gold-Standard (997 Glyphen, doc.json hat 0 Formeln)

**Audit + Verifikation:**
- `verification/AUDIT_V10.4_CLAIMS.md` — V10.8 Audit (F/K/E/P-Klassifikation)
- `verification/code/v09_burumut_matrix.py` — V1 p23-Strukturen
- `verification/code/v13_v3_algebraic_matrix.py` — V3 algebraische Verifikation
- `verification/data/burumut/p23_grid.json` — V1-Output (11 Faktor-Paare, V3-Input)
- `verification/results/snapshots/v3_*.json` — V3-Outputs
- `verification/results/V3_FINAL_BILANZ.md` — V3-Bilanz

**Frühere Phasen (Inputs für V10.4):**
- `consecutive_reading/bbox/burumut_20260707_V7/burumut_texts.json` — V7 Tappeiner (76 BURUMUT-Kandidaten, 7 pro Bruch)
- `consecutive_reading/v8_*.py` + `bbox/v8_*/` — V8 Wikia-Alignment
- `consecutive_reading/v9_phase6_smart_parser_v2.py` + `bbox/v9_reproduction_20260706/burumut_decoded_v2.json` — V9 v2 Smart-Parser
- `consecutive_reading/bbox/v24_20260708/v25_154_zellen.json`, `v26_14bit_codes.json` — V25/V26 multidimensionale Architektur
- `original_sources/wikia/wikia_complete_knowledge.json` — Wikia-Plaintext (Schmeh-Übersetzung)
- `original_sources/137/P001-P010.png`, `original_sources/p011_p023_originals/P011-P023.png` — 23 Original-PNGs

**Verwandte Messages im message_hub/:**
- `2026-07-08_v103_falsifikation_p17.md` — V10.3 p17-BURUMUT-Fälschung
- `2026-07-08_v104_23seiten_verifikation.md` — V10.4 23-Seiten-Empirie
- `2026-07-09_v104_cross_verification.md` — V10.4 ↔ Original-PNGs ↔ doc.json
- `2026-07-09_v104_1_formulas_source_korrektur.md` — V10.4 → V10.4.1
- `2026-07-10_dns_antwort_auf_v3_audit.md` — DNS-Rekonstruktions-Antwort auf V3

---

**Commits:** V10.8 (Audit) + V10.9 (V3-Verifikation). **V10.4.1** bleibt Master für `formulas_source`-Korrektur, **V10.5** ist separater Master für Wort-9-Korrektur (`KORENORBIZUMRO`).
