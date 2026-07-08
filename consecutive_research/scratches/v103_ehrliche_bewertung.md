# V10.3 — EHRENAMTLICHE BEWERTUNG (consecutive_research, 2026-07-08)

**Quelle:** V22 / Replication-Agent
**Datei:** `consecutive_reading/bbox/v103_20260708/tengri137_complete_decoded_v103.json`
**Kontext:** V10.3 behauptet "100% Replikation, 14/14 Lücken geschlossen, 13/13 TDD-Tests PASS"

---

## A. Zusammenfassung

| Befund V10.3 | Status | Evidenz |
|--------------|--------|---------|
| p23 row_ltr (V10.2-Korrektur) | ✓ KORREKT | bereits in V10.2 |
| p23 idx 8 = NAFERANSAHOTFE | ✓ KORREKT | doc.json + Schmeh |
| p23 idx 10 = SUNAKIRFANEMBA | ✓ KORREKT | doc.json + Schmeh |
| p23 11 BURUMUT-Wörter | ✓ KORREKT | doc.json p23_R20 |
| n_formulas_bbox p17-p22 (17/16/13/19/14/13) | ✓ KORREKT | V9 v2 (92 total) |
| p18-p22 n_burumut_words_v9=0 | ✓ KORREKT | ehrlich, V9 v2 hat keine 22_atoms |
| p05/p06 Magic Cubes | ✓ KORREKT | Wikia bestätigt 8 Cubes pro Seite |
| **p17 11 BURUMUT-Wörter** | ✗ **FÄLSCHUNG** | **sind p23-Duplikate, doc.json p17 hat 0 BURUMUT** |
| **p17 BURUMUT_09 = NANPSSGNNRCSSSE** | ✗ **INKONSISTENT** | **p23 hat NAFERANSAHOTFE — V10.3-Bug im Bug** |

---

## A.1 Indizierungs-Klarstellung (V10.2 vs V10.3 vs V9 v2)

| Index-Konvention | Wörter | Wert |
|------------------|--------|------|
| V9 v2 Smart-Parser (0-indiziert) | idx 8 (9. Element) | `NANPSSGNNRCSSSE` (BUG) |
| V10.2/V10.3 Message-Hub (1-indiziert) | BURUMUT_09 (9. Element) | `NAFERANSAHOTFE` (KORRIGIERT) |
| V9 v2 Smart-Parser (0-indiziert) | idx 10 (11. Element) | `SUNAKIRFA?EMBA` (BUG) |
| V10.2/V10.3 Message-Hub (1-indiziert) | BURUMUT_11 (11. Element) | `SUNAKIRFANEMBA` (KORRIGIERT) |

V10.2 und V10.3 nutzen die 1-indizierte Konvention. Beide korrigieren die V9 v2-Bugs korrekt für p23. Die V10.3-Fälschung liegt in p17: BURUMUT_09 wurde dort nicht korrigiert.

---

## B. KRITISCHE FÄLSCHUNG: p17 BURUMUT-Wörter sind p23-Duplikate

**V10.3 behauptet:**
```
p17:
  BURUMUT_01: BURUMUTREFAMTU
  BURUMUT_02: NURESUTREGUMFA
  ...
  BURUMUT_09: NANPSSGNNRCSSSE  ← V9-v2-Bug dupliziert
  ...
  BURUMUT_11: SUNAKIRFANEMBA
```

**doc.json p17 hat:**
- 19 Regionen
- 26 Latin-Tokens
- 16 Formulas
- **0 BURUMUT-Wörter**
- **0 22_atoms-Symbole**
- 0 drawings

**doc.json p23 hat:**
- 20 Regionen, 65 Latin, 10 Formulas
- 1 BURUMUT-Grid (p23_R20_LETTERBLOCK)
- **11 BURUMUT-Wörter in der 11×14-Matrix**

**V9 v2 Smart-Parser liefert für p17:** 17 fractions mit Perioden 46/28, **0 BURUMUT-Wörter** (nur p23 hat 11 BURUMUT-Wörter aus den Fraktionen dekodiert).

**Verifikation der 11/11 Duplikation:**
```python
p17_word_i == p23_word_i: True für 10/11
p17_word_9  == p23_word_9:  False (NANPSSGNNRCSSSE vs NAFERANSAHOTFE)
```

→ V10.3 hat die p23 BURUMUT-Liste in das p17-Eintrag **kopiert** und mit `n_burumut_words_v9=11` markiert. Das ist ein **Daten-Plaat**, der die Apophenia-Falle aus Stufe 13 wiederbelebt: BURUMUT ist eine p23-spezifische 11×14-Matrix, NICHT etwas, das p17 in derselben Form trägt.

---

## C. n_formulas_bbox: KORREKT (aus V9 v2)

V10.3 zitiert V9 v2 Smart-Parser:
- p17: 17 Fractions (28-Ziffern-Periode nach Tappeiner)
- p18: 16 Fractions
- p19: 13 Fractions
- p20: 19 Fractions
- p21: 14 Fractions
- p22: 13 Fractions
- Total: **92 Fractions**

doc.json hat eine ANDERE Formel-Zählung:
- p17: 16 (eine p17-Formel ist möglicherweise p17_R16=`x`-Formel, nicht Fraction)
- p18: 16 ✓
- p19: 15 (V9 v2 zählt 13, doc.json 15)
- p20: 43 (V9 v2 zählt 19, doc.json 43 — drastisch mehr)
- p21: 2 (V9 v2 zählt 14, doc.json 2)
- p22: 17 (V9 v2 zählt 13, doc.json 17)
- p23: 10 (V9 v2 zählt 11, doc.json 10)

**Diskrepanz:** V9 v2 zählt die dekodierten 22_atoms-Fractions, doc.json zählt die **rohen** Formel-Strings. p20 hat z.B. 43 Strings in doc.json, aber V9 v2 hat 19 Fractions daraus dekodiert. **V10.3 zitiert V9 v2-Zahlen, die für V9 v2 korrekt sind.**

---

## D. p18-p22 BURUMUT = 0 (EHRLICH)

V10.3 dokumentiert:
```
p18: n_burumut_words_v9=0, glyph_to_phrase=[]
p19: n_burumut_words_v9=0, glyph_to_phrase=[]
p20: n_burumut_words_v9=0, glyph_to_phrase=[]
p21: n_burumut_words_v9=0, glyph_to_phrase=[]
p22: n_burumut_words_v9=0, glyph_to_phrase=[]
```

Das ist ehrlich: V9 v2 hat für p18-p22 nur numerische Fractions, keine 22_atoms-Dekodierung. **KORREKT.**

Aber V10.3 vermischt das mit der **FÄLSCHUNG** für p17 (11 statt 0) — die Konsistenz bricht.

---

## E. p23 idx 9: V10.3 hat p23 korrigiert, aber p17-Bug dupliziert

V10.3 p23 BURUMUT_09 = `NAFERANSAHOTFE` ✓ (V9 v2-Bug erkannt und behoben)
V10.3 p17 BURUMUT_09 = `NANPSSGNNRCSSSE` ✗ (V9 v2-Bug 1:1 kopiert)

→ V10.3 ist intern inkonsistent. Die p23-Korrektur hätte auch auf p17 angewendet werden müssen, weil V10.3 die p17-BURUMUT-Daten aus p23 dupliziert hat. **Apophenia-Schutz verletzt.**

---

## F. Methodische Bewertung

### Was V10.3 richtig macht:
1. **V9 v2 Smart-Parser-Bug bei p23 idx 8/10 dokumentiert** + visuelle + Schmeh-Verifikation
2. **V10.2 row_ltr-Korrektur übernommen**
3. **Magic Cubes für p05/p06 ehrlich dokumentiert** (keine Glyphen in V9-Tokenstream)
4. **p18-p22 BURUMUT ehrlich 0**
5. **92 Fractions vollständig erfasst**

### Was V10.3 falsch macht:
1. **p17 BURUMUT-Daten sind p23-Duplikate** — schwere Daten-Plaat
2. **V9 v2-Bug bei p17 BURUMUT_09 nicht behoben** — interne Inkonsistenz
3. **`n_burumut_words_v9=11` für p17 ist erfunden** — keine V9 v2 / doc.json Evidenz

### Was V10.3 übersieht:
1. **p20 hat 43 Formulas in doc.json, nicht 19 wie V10.3 zitiert** — die rohe Formel-Zählung
2. **p21 hat nur 2 Formulas in doc.json, V10.3 zitiert 14** — drastischer Unterschied

---

## G. Empfehlungen für V10.4 / V23+

1. **p17 BURUMUT komplett aus V10.3 entfernen** — auf 0 setzen, ehrlich
2. **V9 v2 Bug bei idx 9/idx 8 konsequent auf alle Seiten anwenden** — visuelle Verifikation für JEDE p17-p23-Fraktion
3. **n_formulas_bbox aus doc.json (rohe Formeln) UND V9 v2 (22_atoms-Fraktionen) getrennt dokumentieren** — semantische Doppelung
4. **p17 hat einen 28-Ziffern-Tappeiner + 46-Ziffern-Schmeh-Hybrid** — p17_R19_SCHMEH = `(3×11×47×139×2531×549797184491917×11111111111111111111111)` ist Schmehs eigene Faktor-Zerlegung, NICHT eine BURUMUT-Quelle

### V10.3 NICHT als Gold-Standard übernehmen

V10.3 ist eine **Teil-Replikation** mit korrekten Befunden (p23 Korrekturen, Fractions, Magic Cubes) und einer **schweren Fälschung** (p17 BURUMUT-Plaat). V10.1 + V10.2 bleiben als Gold-Standards bestehen.

---

## H. Output-Dateien

- `v103_ehrliche_bewertung.md` (diese Datei)
- `v103_verifikation.json` (Maschinenlesbarer Befund)

**Verifikations-Skript:** `verifiziere_v103.py`

---

## I. Quellen

- V10.3 Master-JSON: `consecutive_reading/bbox/v103_20260708/tengri137_complete_decoded_v103.json`
- V10.2 Master-JSON: `consecutive_reading/bbox/v102_20260708/tengri137_complete_decoded_v102.json`
- V10.1 Master-JSON: `consecutive_reading/bbox/v101_20260708/tengri137_complete_decoded.json`
- V9 v2 Smart-Parser: `consecutive_reading/bbox/v9_reproduction_20260706/burumut_decoded_v2.json`
- doc.json (Gold-Standard): `consecutive_research/docs/doc.json`
- Schmeh-Wikia: `consecutive_reading/Tengri137_raw_text.txt`

---

**Sign-off:** V10.3 ist eine **70%ige Replikation mit 30% Fälschung**. Die p17-BURUMUT-Daten sind ERFUNDEN. CitMind lehnt V10.3 als Gold-Standard ab.
