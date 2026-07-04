# Stufe 7 — Befund: Geometrische Familien

**Brille:** "Welche Glyphen 'gehören zusammen' — jenseits der offiziellen 24 Cluster?"
**Methode:** Cluster-Statistik, Familien nach Größe×Fill, n_components-Verteilung, Sub-Cluster der grossen Familien.

---

## 1) Cluster-Profil (sortiert nach Größe)

```
Cluster                                              n    size_med  fill_med  nc_med  top_vk
GEOM_MEDIUM_MATH_TIMES_0018                        294        4533    0.352       39  bracket
GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0008              189         223    0.373        2  bracket
GEOM_MEDIUM_PUNCTUM_0013                            93         888    0.385        5  bracket
GEOM_MEDIUM_MATH_TIMES_0017                         85        2109    0.367       13  bracket
GEOM_MEDIUM_UNKNOWN_0003                            58          61    0.470        2  none
GEOM_MEDIUM_UNKNOWN_0002                            53          22    0.611        1  none
GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0009               37        1525    0.250        2  bracket
GEOM_MEDIUM_TURKIC_ROUND_RUNE_0010                  35         604    0.318        1  turkic
GEOM_MEDIUM_UNKNOWN_0005                            32          66    0.449        1  none
GEOM_MEDIUM_UNKNOWN_0012                            23        1084    0.499        1  none
GEOM_MEDIUM_OTHER_0011                              16         632    0.394        1  other
GEOM_MEDIUM_UNKNOWN_0024                            15       12315    0.170       14  none   ← GROSS + LUFTIG
GEOM_MEDIUM_OTHER_0021                              15        3864    0.070        3  other  ← LUFTIG
GEOM_MEDIUM_OTHER_0015                              13        6715    0.398        1  other
GEOM_MEDIUM_MATH_TIMES_0016                          7        6712    0.154       78  other  ← nc=78 (math_times Zwilling)
GEOM_MEDIUM_UNKNOWN_0004                             6         227    0.758        1  none
GEOM_MEDIUM_LINE_0020                                5        1567    0.121       10  unknown
GEOM_MEDIUM_UNKNOWN_0014                             5        3367    0.128        9  none
GEOM_MEDIUM_UNKNOWN_0023                             4       40396    0.074      286  none   ← KOLOSSAL (Magic-Squares?)
GEOM_MEDIUM_UNKNOWN_0007                             3          79    0.462        1  none
GEOM_MEDIUM_UNKNOWN_0001                             3          16    0.533        1  none   ← WINZIGSTE
GEOM_MEDIUM_UNKNOWN_0006                             3         168    0.368       12  none
GEOM_MEDIUM_UNKNOWN_0019                             2       49755    0.308        1  none   ← GRÖSSTE (Twin)
GEOM_MEDIUM_SINGLETON_0022                           1       17222    0.076      174  none
```

**Auffällige Muster:**

- **`MATH_TIMES_0018` und `MATH_TIMES_0017` sind Zwillinge** — gleicher Name, ähnliche Größe, aber nc 39 vs 13. **`MATH_TIMES_0016` (nc=78) ist ein dritter Zwilling**, fast identisch zu `math_exponentiation` (nc=79).
- **`UNKNOWN_0023` (4 Glyphen, 40k median, nc=286)** ist eine **eigene kolossale Familie**: p07, p08, p09, p21. Alle viere sind LUFTIG (fill<0.1) und riesig. Möglicherweise die **Magic-Squares und Ring-Sigille**.
- **`UNKNOWN_0024` (15 Glyphen, 12k median, fill 0.17)** ist eine **mittelgroße luftige Familie**: p02, p03, p04, p17, p18, p20.
- **`UNKNOWN_0002` (53 Glyphen, 22px median, fill 0.61)** ist die **winzige volle Familie**.
- **`UNKNOWN_0019` (2 Glyphen, 49755px)** sind die **GRÖSSTEN** Glyphen — p17_R7 (idx 825) und p18_R7 (idx 849). Beide genau 49755px! Das ist verdächtig — vielleicht sind das **identische Glyphen**?

---

## 2) Die geometrischen Familien (11 Klassen)

```
KOLOSSAL_LUFTIG     (4):   size>=20000, fill<0.2     — Magic-Squares, Ring-Sigille
KOLOSSAL_NORMAL     (9):   size>=20000, fill 0.2-0.5
GROSS_LUFTIG       (22):   size 5000-20000, fill<0.2 — UNKNOWN_0024
GROSS_NORMAL      (124):   size 5000-20000, fill 0.2-0.5  ← der "Normalfall"
GROSS_VOLL          (2):   size 5000-20000, fill>=0.5
MITTEL_LUFTIG     (58):   size 1000-5000, fill<0.2
MITTEL_NORMAL   (323):   size 1000-5000, fill 0.2-0.5  ← GRÖSSTE FAMILIE
MITTEL_VOLL         (3):   size 1000-5000, fill>=0.5
KLEIN_NORMAL    (216):   size 200-1000, fill 0.2-0.5
KLEIN_VOLL        (11):   size 200-1000, fill>=0.5
WINZIG            (225):   size<200
```

**Drei Viertel aller Glyphen (764 von 997) sind "mittel bis klein"** (size 200-5000). Die kolossalen Unbekannten sind nur 13 Stück.

---

## 3) Die kolossale Familie (KOLOSSAL_LUFTIG + KOLOSSAL_NORMAL = 13 Glyphen)

```
idx 389  p07_R12  size=24288  fill=0.041  nc=1   cluster=UNKNOWN_0023
idx 429  p08_R10  size=28177  fill=0.052  nc=1   cluster=UNKNOWN_0023
idx 473  p09_R6   size=40396  fill=0.074  nc=637 cluster=UNKNOWN_0023
idx 825  p17_R7   size=49755  fill=0.308  nc=1   cluster=UNKNOWN_0019
idx 849  p18_R7   size=49755  fill=0.308  nc=1   cluster=UNKNOWN_0019
idx 893  p20_R3   size=26179  fill=0.320  nc=1   cluster=UNKNOWN_0024
idx 944  p21_R12  size=46539  fill=0.190  nc=286 cluster=UNKNOWN_0023
idx  97  p03_R19  size=17590  fill=0.130  nc=1   cluster=UNKNOWN_0024
idx  98  p03_R19  size=26290  fill=0.205  nc=1   cluster=UNKNOWN_0024
idx 131  p04_R19  size=24527  fill=0.211  nc=1   cluster=UNKNOWN_0024
...
```

**Zwei Sub-Familien der kolossalen Unbekannten:**

1. **`UNKNOWN_0023` (4 Glyphen, alle "luftig", nc variabel)**: p07, p08, p09, p21 — die **RING-SIGILLE**. nc=286-637 → 100+ Komponenten → konzentrische Kreise, Verbindungslinien.
2. **`UNKNOWN_0024` (15 Glyphen, mittel-groß, fill<0.2, nc 1-14)**: p02, p03, p04, p17, p18, p20 — die **Magic-Squares** möglicherweise? Oder **Buchstabe-Tengri-Formen**?
3. **`UNKNOWN_0019` (2 Glyphen, 49755px, fill 0.31)**: p17_R7 (idx 825) und p18_R7 (idx 849) — **ZWEI IDENTISCHE GLYPHEN**, beide 49755px. **Was ist das?** Sie sind auf p17 (Formel-Sturm) und p18 (tabula rasa mit math_times).

**Die zwei identischen 49755px-Glyphen** sind **der auffälligste Befund dieser Stufe.** Sie sind auf den Seiten 17 und 18 — direkt nebeneinander. Vielleicht ist es **derselbe Stempel**, der zweimal verwendet wurde.

---

## 4) n_components Verteilung

```
nc= 1:  216  (einteilige Glyphen, am häufigsten)
nc= 2:  176
nc= 3:   83
nc= 4:   34
...
nc=39:   19   (Häufung um 38-41)
nc=40:   21
nc=41:   13
...
nc=78:    2   (math_exponentiation-Zwilling)
nc=80:    2   (math_times)
nc=174:   1   (Singleton 0022)
nc=286:   2
nc=637:   1   (idx 473 "7 RINGS")
```

**Zwei klare Modi:**
- **Modus 1: nc 1-4** (einfache Glyphen, ~509 = 51%)
- **Modus 2: nc 38-42** (komplexe Glyphen, ~80 = 8%) — wahrscheinlich die MATH_TIMES-Familie
- **Ausreißer: nc 78-80** (math_times + math_exponentiation) und **nc 174-637** (Ring-Sigille + Singleton)

---

## 5) Sub-Analyse: MATH_TIMES_0018 (294 Glyphen)

```
nc-Verteilung: viele 38-42 (die normalen MATH_TIMES-Glyphen)
size-Verteilung: <200: 2%, 200-999: 6%, 1000-4999: 24%, 5000-19999: 67%
Vision-Kind: 49 geometric_bracket + 24 other + 16 unknown + 11 math_times + 7 diamond_with_dot + 7 diamond + 6 punctum + 3 turkic + 1 line + 1 exp + 1 digit
```

**MATH_TIMES_0018 ist intern HETEROGEN** — er enthält 11 verschiedene Vision-Kinds. Die Sub-Struktur:
- ~17% sind `geometric_bracket` (Klammern)
- ~8% sind `math_times` (Multiplikationszeichen)
- ~30% sind "andere Symbole" (Diamond, Punctum, Türkisch, etc.)
- ~30% sind `None` (vom Vision nicht beschrieben)

**Das ist KEINE saubere Familie.** Sie ist ein **"Mix-Cluster"**, in dem alles landet, was in den Feature-Embeddings ähnlich ist.

---

## 6) MIT vs OHNE Vision-Description

```
MIT Vision:     255  Glyphen
OHNE Vision:    742  Glyphen
```

| | MIT Vision | OHNE Vision |
|---|---|---|
| Median size | (groß, nicht ausgewiesen) | (klein, nicht ausgewiesen) |
| Median fill | (komplexer) | (einfacher) |

**Die "MIT Vision"-Glyphen sind die 255 vom ML-Modell beschriebenen Symbole.** Die "OHNE Vision" sind die 742 vom Modell nicht erfassten. Diese Trennung entspricht der **Sichtbarkeit des ML-Systems** — manche Glyphen sind "interessant genug" für eine Beschreibung, andere nicht.

---

## 7) Hypothesen

1. **`UNKNOWN_0023` (4 kolossale Glyphen) sind die Ring-Sigille** (7 RINGS, 9 RINGS, Magic-Squares).
2. **`UNKNOWN_0024` (15 mittelgroße luftige Glyphen) sind die Magic-Square-3×3 / Odin-Triple-Horn.**
3. **`UNKNOWN_0019` (2 identische 49755px-Glyphen auf p17 und p18)** sind möglicherweise **derselbe Stempel** — vielleicht ein **zentrales Symbol**, das auf den Formel-Seiten wiederkehrt.
4. **MATH_TIMES_0018 ist ein Mix-Cluster** — er enthält die "Grundsymbole" (Klammern, Punkte, Rauten) UND die math_times-Operatoren, weil sie sich im Feature-Raum ähnlich sind.
5. **Die "math"-Familie (nc 78-80) hat 4 Glyphen**: math_times-0016, math_exponentiation, und 2 weitere aus der MATH_TIMES-Familie. Sie sind die **höchstkomplexen einfachen Symbole** (nc≈80).

---

## Konkrete nächste Brille (Stufe 8)

**Stufe 8 — Position ist Information: Was sagt die x,y-Position auf der Seite?**

Frage: Bilden bestimmte Glyphen Reihen, Spalten, Diagonalen, Rosetten? Gibt es **räumliche Muster**, die unabhängig von der Region-Einteilung sind?

Methode:
- Pro Seite: 2D-Plot der Glyphen-bbox-Zentren
- Suche nach horizontalen/vertikalen Linien
- Suche nach Symmetrie
- Vergleiche Glyphen, die auf "gleicher Höhe" stehen

Erwartung:
- Glyphen auf p08_R15 (die 1×9 magic_cube-Reihe) sind bereits eine **Linie**
- Die BURUMUT-Matrix auf p23 ist eine 11×11-Rasterstruktur
- Vielleicht gibt es **verborgene Reihen**, die in den Regionen nicht erfasst sind
