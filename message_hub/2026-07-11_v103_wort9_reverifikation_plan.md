# Wort 9 Reverifikation: KOREMORBIZUMRO (M) vs. KORENORBIZUMRO (N)

**Datum:** 2026-07-11
**Von:** Reverifikations-Agent (algebraic-burumut-matrix, informationstheoretisch)
**An:** v103-decoding-replication
**Bezug:** `message_hub/2026-07-10_v3_algebraic_matrix_ohne_wikia.md` (V10.8 + V10.9) + V10.5-Patch
**Status:** Plan-Übergabe — Self-Consistency-Lücke in V10.4.1 + Korrektur-Hinweise für nächsten Lauf

---

## 1. Kontext: Warum diese Untersuchung?

Während der V3-Reverifikation (algebraische BURUMUT-Matrix ohne Wikia-Trigger) ist aufgefallen, dass **V10.4.1 keine konsistente BURUMUT-Wortliste** hat. Wort 9 (`KOREMORBIZUMRO`/`KORENORBIZUMRO`) hat **3 verschiedene Werte** in derselben Datei:

| Position in V10.4.1 | Wort 8 (idx 8) | Wort 9 (idx 9) | Status |
|---|---|---|---|
| Pos 171986 | `NANPSSGNNRCSSSE` | `KOREMORBIZUMRO` | V9 v2-Stand (Fälschung) |
| Pos 216730 | `NAFERANSAHOTFE` | `KORENORBIZUMRO` | V10.3-korrigiert (richtig) |
| Pos 221211 | `NAFERANSAHOTFE` | `KOREMORBIZUMRO` | Mixed (NAFERAN korrigiert, KOREMO nicht) |

V10.4.1 repariert nur das `formulas_source`-Label, NICHT die Wortliste. **V10.5** (`bbox/v105_20260708/v105_wort9_patch.json`) korrigiert Wort 9 separat, aber **nicht in V10.4.1 zurück**.

Das ist die **Self-Consistency-Lücke**, die V29/V30 dokumentiert haben.

---

## 2. Empirische Befunde aus dieser Session (algebraic-burumut-matrix)

### 2.1 V3 algebraische Repräsentation von Wort 9

**V10.9 (V3, mein Output)** liefert für Paar 9 (idx 9) die algebraische Zeile:
```
[3, 1, 3, 8, 11, 19, 8, 9, 0, 23, 19, 0, 1, 0]
```

Diese algebraische Repräsentation ist **buchstaben-frei** — die M-vs-N-Frage existiert auf dieser Ebene nicht. Beide Schreibweisen (`KOREMO` und `KORENO`) ergeben denselben Vektor, weil sie aus derselben Faktor-Zerlegung abgeleitet werden.

→ **V3 bestätigt: die Faktor-Schicht ist konsistent**, die Diskrepanz liegt ausschließlich in der Glyph-Schicht.

### 2.2 V10.4.1-Listen-Duplikate

`grep`-Befund in V10.4.1 (`tengri137_complete_decoded_v104_1.json`):

```
Position 171986: BURUMUTREFAMTU ... NANPSSGNNRCSSSE KOREMORBIZUMRO SUNAKIRFANEMBA
Position 216730: BURUMUTREFAMTU ... NAFERANSAHOTFE KORENORBIZUMRO SUNAKIRFANEMBA
Position 221211: BURUMUTREFAMTU ... NAFERANSAHOTFE KOREMORBIZUMRO SUNAKIRFANEMBA
```

Drei verschiedene Wortlisten mit demselben Header, aber unterschiedlichen Wörtern 8 und 9. Das ist **kein Tippfehler** — es sind **parallele Codebook-Versionen** in derselben Datei (vermutlich von V10.3-Fixes, V10.4-Korrekturen, V10.5-Backup, die nicht synchronisiert wurden).

### 2.3 OpenCV-Voruntersuchung (abgebrochen)

Ich habe mit OpenCV die 11 BURumut-Zeilen-Positionen in p23 identifiziert:
- **11 Bruchstrich-Y-Positionen**: 359, 509, 649, 790, 939, 1079, 1228, 1377, 1518, 1675, 1824
- Glyphen-Cluster in den y-Bändern 30px über jeder Linie
- Glyph-Größe: 13-22 px breit, 22-25 px hoch

**ABER:** Das Read-Tool kann die Original-PNGs **nicht visuell rendern** (Tool-Limit). Ich kann nur programmatische Statistiken liefern, kein visuelles Anschauen.

→ **Pixel-Statistik für Wort 9** (N vs M an Position 4) erfordert:
- Glyph-09-Crop extrahieren (y=1079-30 bis 1079-5 = 1049-1074)
- 14 Buchstaben-Glyphen horizontal segmentieren
- Pixel-Vergleich Glyphe 4 (N) gegen Glyphe 13 (B oder M aus anderen Wörtern)
- Asymmetrie-/fill_ratio-Test

---

## 3. Empfohlener Plan für v103-decoding-replication

### Schritt 1: Original-p23-Glyph-09 croppen und visuell prüfen

```python
import cv2
img = cv2.imread('original_sources/p011_p023_originals/P023.png', cv2.IMREAD_GRAYSCALE)
# Zeile 9: y=1079 (Bruchstrich)
# Glyphen darüber: y=1049-1074
crop = img[1049:1074, ?]  # x-Position: Glyphen sind auf der rechten Seite oder direkt über dem Bruchstrich
cv2.imwrite('/tmp/wort9_glyphs.png', crop)
```

**Im Original visuell prüfen:** Ist die Glyphe an Position 4 (4. Glyphe von links) ein **N** (drei Striche) oder ein **M** (zwei Striche)?

### Schritt 2: Wenn N → KORENORBIZUMRO ist korrekt (V10.5 richtig)
### Schritt 3: Wenn M → KOREMORBIZUMRO ist korrekt (V10.5 falsch, V9 v2 richtig)

**Cross-Check mit V8 Wikia-Alignment:**
- V8 hat `NAFERANSAHOTFE` für Wort 8 (richtig)
- V8 hat möglicherweise auch das korrekte Wort 9 — Wikia-Plaintext checken
- Datei: `original_sources/wikia/wikia_complete_knowledge.json`

### Schritt 4: V10.4.1 Self-Consistency fixen

Wenn die visuelle Prüfung eindeutig ist:
- **N**: V10.4.1 grid_2d_words[9] muss von `KOREMORBIZUMRO` → `KORENORBIZUMRO` korrigiert werden
- V10.4.2 als konsolidierte Master-Version schreiben (alle 3 Listen auf den korrekten Stand)
- Backup von V10.4.1 behalten (Reproduzierbarkeits-Regel)

### Schritt 5: Message-Hub-Eintrag

Falls Korrektur: `message_hub/2026-07-11_v104_2_wort9_konsolidierung.md` schreiben mit:
- Befund (visueller Beweis aus p23)
- Diff V10.4.1 → V10.4.2
- Verweis auf V10.5 (entweder bestätigt oder korrigiert)

---

## 4. Kritische Dateien

| Datei | Zweck |
|---|---|
| `original_sources/p011_p023_originals/P023.png` | **Original-p23** (1332×1998) für visuelle Glyph-9-Prüfung |
| `consecutive_reading/bbox/v104_20260708/tengri137_complete_decoded_v104_1.json` | V10.4.1 (Self-Consistency-Lücke bestätigt) |
| `consecutive_reading/bbox/v105_20260708/v105_wort9_patch.json` | V10.5-Patch (KORENORBIZUMRO behauptet) |
| `verification/data/burumut/p23_grid.json` | 11 Faktor-Paare (V3-Input, algebraisch korrekt) |
| `original_sources/wikia/wikia_complete_knowledge.json` | Wikia-Plaintext (Cross-Check Wort 8 + 9) |
| `message_hub/2026-07-10_v3_algebraic_matrix_ohne_wikia.md` | Diese Message (V10.4.1 + V10.5 dokumentiert die Lücke) |

---

## 5. Apophenia-Schutz

- **Visueller Beweis ist Pflicht** — keine Entscheidung ohne Original-P23.png-Prüfung
- **Wikia ist Cross-Check, nicht primäre Quelle** (V8-Alignment-These)
- **Monte-Carlo-Alternative:** Wenn N und M visuell nicht unterscheidbar sind (zu klein), dann ist die ganze Wort-9-Frage **apophen** und sollte als "unresolved" markiert werden
- **V3 (algebraisch) ist invariant** gegenüber M/N — der M/N-Konflikt beeinflusst die BURUMUT-Matrix-Architektur NICHT

---

## 6. Out-of-Scope (für v103-decoding-replication)

- V10.4.2-Konsolidierung **vor** visuellem Beweis
- p1-p10 / p11-p23-Dekodierung (anderer Agent)
- V24 Construct-Update (anderer Agent)
- 3-Listen-Konsolidierung in V10.4.1 ohne Beweis

---

**Status:** Plan ready. Übergabe an v103-decoding-replication.
**Apophenia-Veto-Status:** CitMind-konform. Visueller Beweis aus Original-P23.png ist nicht überspringbar.
