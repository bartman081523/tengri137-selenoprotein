# V10.3 EMPIRISCHE ORIGINAL-VERIFIKATION (2026-07-08)

**Quellen:** `/run/media/julian/ML4/tengri137/original_sources/137/P001-P010.png` + `/run/media/julian/ML4/tengri137/original_sources/p011_p023_originals/P011-P023.png` (1332×1998 RGBA, Original-Schmeh 2012)
**Methode:** Visuelle Inspektion der Original-PNGs + Vergleich mit V10.3 Master-JSON

---

## A. VERIFIKATIONS-MATRIX (V10.3 vs ORIGINAL)

| V10.3-Behauptung | ORIGINAL-Befund | Status |
|------------------|-----------------|--------|
| p05: is_magic_cube_page=True, n_magic_cubes=8 | 8 Magic Cubes (3×3), 666er-Summen sichtbar | ✓ BESTÄTIGT |
| p06: is_magic_cube_page=True, n_magic_cubes=8 | 8 Magic Cubes (3×3), 666er-Summen sichtbar | ✓ BESTÄTIGT |
| p17: n_burumut_words_v9=11 | 17 Fraktionen, Latein-Text, **0 BURUMUT-Wörter** | ✗ **FÄLSCHUNG** |
| p17 BURUMUT_09 = NANPSSGNNRCSSSE | ORIGINAL p17 hat 0 BURUMUT-Wörter | ✗ **PHANTOM** |
| p18: n_burumut_words_v9=0 | 16 Fraktionen, Latein-Text, 0 BURUMUT | ✓ BESTÄTIGT |
| p19: n_burumut_words_v9=0 | Latein + 13 Fraktionen, 0 BURUMUT | ✓ BESTÄTIGT |
| p20: n_burumut_words_v9=0 | Latein + ~19-43 Formel-Strings, 0 BURUMUT | ✓ BESTÄTIGT |
| p21: n_burumut_words_v9=0 | 14 Fraktionen, 0 BURUMUT | ✓ BESTÄTIGT |
| p22: n_burumut_words_v9=0 | 13 Fraktionen, 0 BURUMUT | ✓ BESTÄTIGT |
| p23 BURUMUT_09 = NAFERANSAHOTFE | ORIGINAL Zeile 9: `N A F E R A N S A H O T F E` | ✓ **BESTÄTIGT** |
| p23 BURUMUT_10 = KOREMORBIZUMRO | ORIGINAL Zeile 10: `K O R E M O R B I Z U M R O` | ✓ BESTÄTIGT |
| p23 BURUMUT_11 = SUNAKIRFANEMBA | ORIGINAL Zeile 11: `S U N A K I R F A N E M B A` | ✓ **BESTÄTIGT** |
| p23 Akrostichon BNYZTSOYNKS | Spalte 1: B N Y Z T S O Y N K S | ✓ BESTÄTIGT |
| p11: keine Magic Cubes, keine BURUMUT | Latein-Korridor, Tengri-Glyphen | ✓ BESTÄTIGT |
| p16: keine BURUMUT | Latein-Korridor, Glyphen | ✓ BESTÄTIGT |
| p01: Übergangszone | Glyphen + Latein-Mix | ✓ BESTÄTIGT |

---

## B. KRITISCHE BEFUNDE AUS DER ORIGINAL-INSPEKTION

### B.1 P23 BURUMUT-MATRIX (3x vergrößert) — alle 11 Zeilen klar lesbar

| idx | Glyph | Original-Buchstaben (1-spaced) |
|-----|-------|-------------------------------|
| 0 | BURUMUT_01 | B U R U M U T R E F A M T U |
| 1 | BURUMUT_02 | N U R E S U T R E G U M F A |
| 2 | BURUMUT_03 | Y A P S U A Z B E H I M L A |
| 3 | BURUMUT_04 | Z A N R U A Z B E N O M B A |
| 4 | BURUMUT_05 | T O B I K O T L U B U M Y O |
| 5 | BURUMUT_06 | S U N O K U R G A N O Z Y I |
| 6 | BURUMUT_07 | O K U Z I K U F A U S I H E |
| 7 | BURUMUT_08 | Y A B E K A N S A B E R H O |
| 8 | BURUMUT_09 | N A F E R A N S A H O T F E |
| 9 | BURUMUT_10 | K O R E M O R B I Z U M R O |
| 10 | BURUMUT_11 | S U N A K I R F A N E M B A |

→ **V10.3 p23 BURUMUT-Wörter 100% korrekt (visuell + Schmeh)**

### B.2 P23 Akrostichon (Spalte 1)

```
B  ←  BURUMUTREFAMTU
N  ←  NURESUTREGUMFA
Y  ←  YAPSUAZBEHIMLA
Z  ←  ZANRUAZBENOMBA
T  ←  TOBIKOTLUBUMYO
S  ←  SUNOKURGANOZYI
O  ←  OKUZIKUFAUSIHE
Y  ←  YABEKANSABERHO
N  ←  NAFERANSAHOTFE
K  ←  KOREMORBIZUMRO
S  ←  SUNAKIRFANEMBA
```

→ **Akrostichon BNYZTSOYNKS im ORIGINAL sichtbar** (vertikale Selbst-Referenz, V12/V15 p<10⁻¹³)

### B.3 P17 ORIGINAL — 17 Fraktionen, KEINE BURUMUT-Wörter

Sichtbar im Original:
- 17 Fraktionen mit 28/46-Ziffern-Perioden
- Latein-Text: "IF YOU ARE NOT CONVINCED THEN CALCULATE THE NEXT NUMBER AND SEE WHAT A PROOF IS PROVIDED TO YOU ADAM MEAN. DECIMALS HAVE THEIR OWN MEANING. A REPETITIVE INTERVAL OF EXACT FORTY SIX. THIS INTERVAL IS NOT ARBITRARY. THIS IS A CALCULATION TO SHOW YOU OUR KNOWLEDGE AND OUR WISDOM..."
- p17_R19_SCHMEH = "(3×11×47×139×2531×549797184491917×11111111111111111111111)" — Schmehs eigene Faktor-Zerlegung

→ **V10.3 p17 n_burumut_words_v9=11 ist EMPIRISCH FALSCH**. doc.json p17 hat 0 BURUMUT.

### B.4 P05/P06 Magic Cubes (2x vergrößert)

8 Würfel-Anordnungen sichtbar mit Summen ≈ 666 pro Zeile/Spalte/Diagonale.
Beispiele:
- Cube 1: 638+24+4=666, 19+10+637=666, 9+632+25=666
- Cube 2: 5+639+22=666, 635+13+18=666, 26+14+626=666
- Cube 3: 23+3+640=666, 12+643+11=666, 631+20+15=666
- Cube 4-8: ähnlich, jeweils 3×3 mit 666er-Summen

→ **V10.3 n_magic_cubes=8 für p05/p06 = EMPIRISCH KORREKT**

---

## C. EHRLICHE BILANZ (12 VERIFIKATIONEN)

| Kategorie | Korrekt | Falsch |
|-----------|---------|--------|
| Magic Cubes p05/p06 | 2/2 ✓ | 0/2 |
| p18-p22 BURUMUT = 0 | 5/5 ✓ | 0/5 |
| p23 BURUMUT-Wörter (11) | 11/11 ✓ | 0/11 |
| p23 Akrostichon BNYZTSOYNKS | 1/1 ✓ | 0/1 |
| p23 idx 8/10 Korrekturen | 2/2 ✓ | 0/2 |
| **p17 BURUMUT = 11 (Fälschung)** | 0/1 ✗ | **1/1** |
| p17 BURUMUT_09 = NANPSSGNNRCSSSE | 0/1 ✗ | **1/1** |
| p11/p16/p01 Latein-Korridor | 3/3 ✓ | 0/3 |
| **TOTAL** | **24/26 (92%)** | **2/26 (8%)** |

→ **V10.3 ist 92% korrekt + 8% Fälschung** (nur p17-BURUMUT ist falsch)

---

## D. WO GENAU LIEGT DER V10.3-FEHLER?

**Vermutung:** Das V10.3-Skript hat `n_burumut_words_v9=11` für p17 gesetzt, weil:
1. Es hat p23 BURUMUT-Wörter 1:1 in das p17-Eintrag kopiert
2. Es hat den V9 v2-Bug bei BURUMUT_09 nicht behoben (p17 hat NANPSSGNNRCSSSE statt NAFERANSAHOTFE)
3. Es hat n_formulas_bbox aus V9 v2 (17) statt doc.json (16) zitiert

**Resultat:** V10.3 ist im p17-Bereich eine Fälschung, im p23-Bereich eine korrekte Verbesserung.

---

## E. EMPFEHLUNG FÜR V22 / V23+

1. **V10.3 p17 BURUMUT entfernen** — auf 0 setzen, ehrlich
2. **V10.3 p23 Korrekturen übernehmen** — visuell+Schmeh bestätigt
3. **V10.3 Magic Cubes p05/p06 übernehmen** — Original bestätigt
4. **V10.3 p18-p22 n_burumut_words_v9=0 übernehmen** — Original bestätigt
5. **V10.3 p17 BURUMUT_09 = NAFERANSAHOTFE korrigieren** (in V10.4) — statt NANPSSGNNRCSSSE

---

## F. SCHLUSS-URTEIL

**V10.3 ist eine 92% korrekte Verbesserung von V10.1/V10.2 + 8% Fälschung im p17-Bereich.**

Die p23 BURUMUT-Matrix (idx 8/10 Korrekturen), Magic Cubes, und ehrliche p18-p22-Dokumentation sind **empirisch durch die Original-PNGs bestätigt**.

Die p17-BURUMUT-Fälschung ist die einzige schwere Inkorrektheit, die V10.4 patchen muss.

**V10.1 + V10.2 bleiben Gold-Standard für p17-BURUMUT-Frage. V10.3 ist teilweise als Ergänzung brauchbar.**

---

## G. OUTPUT-DATEIEN

- `/tmp/p05_2x.png` — P05 Magic Cubes (2x vergrößert)
- `/tmp/p23_matrix_3x.png` — P23 BURUMUT-Matrix (3x vergrößert)
- `/tmp/p17_bereich_2x.png` — P17 Fraktionen (2x vergrößert)
- `consecutive_research/scratches/v103_original_verifikation.md` — diese Datei

---

**Sign-off:** Empirische Original-Verifikation 2026-07-08 abgeschlossen. 24/26 V10.3-Behauptungen sind korrekt, 2 sind Fälschungen (p17 BURUMUT × 2).
