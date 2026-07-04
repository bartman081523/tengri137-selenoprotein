# Stufe 4 — Befund: Die dunkle Materie — enttarnt

**Brille:** "Wo konzentrieren sich die 332 Unbekannten, was unterscheidet sie?"
**Methode:** Page × Region-Typ, Cluster-ID, Vision-Kind, Geometrie für `type_hint=unknown`.

---

## 1) Die Widerlegung einer Annahme

**Ich hatte angenommen, die Unbekannten seien auf p05/06/08 konzentriert.** Das ist nur **teilweise** richtig:

```
p08: 80.6% unknown  ← Maximum (54 von 67 Glyphen)
p05: 56.9% unknown  (66 von 116)
p06: 52.1% unknown  (63 von 121)
p07: 48.1% unknown  (13 von 27)
p14: 35.7% unknown
p03: 32.6% unknown
p13: 29.6% unknown
...
p21:  6.2% unknown  ← Minimum
p22:  5.3% unknown
p09:  0.0% unknown  ← komplett erkannt!
p18:  8.3% unknown  ← NICHT die tabula rasa der Unbekannten
```

**Überraschungen:**
- **p09 hat 0% unknown** — alle 18 Glyphen haben einen type_hint ≠ unknown. Komplett klassifiziert.
- **p18 hat nur 8.3% unknown** (2 von 24). Ich hatte vermutet, p18 sei die "unbekannte Seite", aber sie ist **eher mathematisch** (siehe unten).
- **p08 ist mit Abstand am unbekanntesten** (80.6%). Das ist der "Magic-Cube"-Bereich.

---

## 2) Wo sitzen die Unbekannten? Region-Typ-Verteilung

```
latin_text         206  (62%)  ← in lateinischen Text-Regionen
glyph_block         32  (10%)  ← in Glyphen-Blöcken
graphic_line        27  (8%)
numeric_table       25  (8%)
glyph_raster        18  (5%)
single_glyph         9  (3%)
magic_cube           9  (3%)  ← der Magic-Cube hat 9 unbekannte Glyphen
formula_block        4  (1%)
footer               1
header               1
```

**62% der Unbekannten sind in `latin_text`-Regionen.** Das ist ein klarer Hinweis: Die Unbekannten stehen **mitten im lateinischen Text** — sie sind nicht separate "Dekor-Symbole", sondern **Bestandteil des Leseflusses**.

---

## 3) Die Cluster-ID-Identität

**53% aller Unbekannten (177 von 332) sind in EINEM einzigen Cluster:**

```
GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0008:  177  ← DER UNBEKANNT-Cluster
GEOM_MEDIUM_UNKNOWN_0003:                55
GEOM_MEDIUM_PUNCTUM_0013:                32
GEOM_MEDIUM_TURKIC_ROUND_RUNE_0010:      28
GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0009:   16
...
```

**WICHTIGE ENTDECKUNG:** Der **zweitgrößte Cluster** (189 Glyphen insgesamt, siehe Stufe 0) heißt `GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0008` und enthält:
- 177 Unbekannte (94% dieses Clusters!)
- 7 geometric_circle (mit Vision-Kind, aber als "circle" erkannt)
- 5 andere Vision-Kinds (siehe Stufe 2)

→ **Dieser Cluster ist die "Kreis-mit-Inhalt"-Familie.** Die meisten seiner Mitglieder sind so unklar, dass nicht mal `type_hint` sie klassifizieren kann. Aber das Vision-System hat **bei einigen** den konkreten Subtyp erkannt (`geometric_circle` 7×, `geometric_circle_with_dot` 1×).

**Was bedeutet das geometrisch?** "Kreis mit ... " — aber WAS ist im Kreis? Das ist die Frage.

---

## 4) Vision-Kind der Unbekannten: ein Widerspruch

**45 der 332 Unbekannten HABEN einen Vision-Kind, sind aber trotzdem `type_hint=unknown`!**

```
geometric_bracket:  12  (Klammern, die nicht als "bracket" erkannt wurden)
other:               9
geometric_circle:    7
unknown (vk):        7
line:                3
geometric_diamond:   2
turkic_round_rune:   1
odin_triple_horn:    1
geometric_circle_with_dot: 1
digit:               1
geometric_diamond_with_dot: 1
```

**→ Das Vision-System und der type_hint-Klassifizierer sind ZWEI UNABHÄNGIGE Systeme.** Sie stimmen nur teilweise überein. Es gibt:
- Glyphen, die Vision kennt, aber type_hint nicht (45 Fälle).
- Glyphen, die type_hint kennt, aber Vision nicht (viele).

**Folgerung:** Die "Unbekannten" sind nicht einheitlich "vom System übersehen". Es sind Glyphen, die **in mindestens einer Pipeline-Stufe nicht klassifiziert** werden konnten.

---

## 5) Geometrie der Unbekannten

```
size_px:     min=40,   max=28177,  median=243
fill_ratio:  min=0.041, max=0.771, median=0.384
n_components:min=1,    max=4,      median=2
```

**Im Vergleich zum Gesamtdokument:**
- Median size: 243 vs. 1219 (Gesamt) — **Unbekannte sind 5× kleiner**
- Median fill_ratio: 0.384 vs. 0.363 (etwas voller)
- Median n_components: 2 vs. ? (Gesamt-Median 1) — **etwas komplexer**

**Die Unbekannten sind klein und einfach strukturiert** (1-4 Komponenten, sehr klein). Das passt zu **kleinen Markierungs-Glyphen**, die zwischen oder neben lateinischem Text stehen — möglicherweise **Interpunktions-Zeichen** oder **diakritische Marker**.

---

## 6) p18 — die tabula rasa ist KEINE Unbekannten-Seite

**p18 hat 24 Glyphen, nur 2 davon sind `type_hint=unknown`.**

```
complex_symbol:     16  (67%)
punctum:             3  (12.5%)
unknown:             2  (8.3%)
vertical_line:       1
geometric_symbol:    1
horizontal_line:     1
```

**Die Vision-Kinds auf p18:**
```
math_times:   3
unknown:      1
(20 ohne Vision-Kind)
```

**`math_times` (3×) auf p18!** Das ist ein **Schlüssel-Befund**: Die "tabula rasa"-Seite (0 Latin) hat **drei Multiplikationszeichen**. Das ist nicht "leer" — das ist eine **MATHEMATISCHE Seite**.

**Außerdem:** Die meisten p18-Glyphen (16 von 24) sind `complex_symbol`. Das deutet auf **strukturierte Glyphen-Kompositionen** hin, nicht auf isolierte Zeichen.

---

## 7) Beispiele der Unbekannten (aus Stichprobe)

```
idx=  1  cluster=TURKIC_ROUND_RUNE_0010  vk=None  size=1263  fill=0.350
idx=  2  cluster=CIRCLE_WIT_0009          vk=None  size=1644  fill=0.314
idx= 13  cluster=CIRCLE_WIT_0008          vk=geometric_bracket  size=263  fill=0.457
idx= 47  cluster=CIRCLE_WIT_0008          vk=geometric_bracket  size=388
idx= 57  cluster=TURKIC_ROUND_RUNE_0010  vk=turkic_round_rune  size=808
idx= 82  cluster=PUNCTUM_0013            vk=other  size=594
idx= 97  cluster=UNKNOWN_0024            vk=None  size=17590  fill=0.130  ← RIESIG
idx= 98  cluster=UNKNOWN_0024            vk=None  size=26290  fill=0.205  ← RIESIG
idx=131  cluster=UNKNOWN_0024            vk=None  size=24527  fill=0.211  ← RIESIG
```

**Drei "kolossale" Unbekannte** (idx 97, 98, 131) auf p03_R19 und p04_R19 — Größen 17.590 - 26.290 px. Die sind 50-100× größer als die mittleren Unbekannten (median 243). **Was sind das für Glyphen?**

- Sie sind in `cluster=GEOM_MEDIUM_UNKNOWN_0024` (5 Mitglieder in diesem Cluster)
- fill_ratio ist sehr niedrig (0.13-0.21) → sehr "luftig", vielleicht ein dünner Strich oder eine große offene Form
- n_components=1 → einteilig

Möglicherweise sind das **Buchstaben-Tengri-Formen** im Originalformat (sehr groß).

---

## 8) Hypothesen

1. **Die Unbekannten sind keine "Geheimsymbole"**, sondern kleine Interpunktions-/Markierungs-Glyphen.
2. **Der `CIRCLE_WIT_0008`-Cluster ist die größte unerkannte Familie** — 94% seiner Mitglieder sind `type_hint=unknown`. Das Vision-System kennt ihn nicht.
3. **p08 ist die "unbekannteste" Seite** (80.6% unknown). Das ist die Magic-Cube-Region. Vielleicht ist der Magic Cube selbst in diesem Cluster.
4. **p18 ist KEINE tabula rasa** — sie hat 3 math_times. Sie ist eine Formel-Seite.
5. **Die "kolossalen Unbekannten" (idx 97, 98, 131)** sind möglicherweise Tengri-Buchstaben in Original-Größe.

---

## Konkrete nächste Brille (Stufe 5)

**Stufe 5 — Der Magic Cube 3x3**

Frage: Welche Glyphen bilden den 3×3-Würfel auf p08? Welche Geometrie, welche Vision-Kinds, welche Cluster-IDs?

Methode:
- p08_R15 (die `magic_cube`-Region) im Detail
- Alle Glyphen dort: Position (bbox), Vision-Kind, Cluster-ID
- Welche Symbole sind in den 9 Zellen?
- Hat die Zellen-Position eine Bedeutung (Ecke/Mitte/Kante)?

Erwartung:
- 9 Zellen mit je 1-2 Glyphen
- Möglicherweise Position-abhängige Symbolvarianten
- Vielleicht sind die Glyphen die "Schlüsselzeichen" der gesamten BURUMUT-Architektur (Schmehs Kontext: 3x3 Magic Square, alle Reihen/Spalten/Diagonalen summieren sich zu 666)

Außerdem: Schmeh sagt, der Magic-Cube ist Teil des "Odin triple horn" Layouts (4×4 Magic Squares, sechs an der Zahl) — ist die Region p08_R15 ein EINZELNER 3x3, oder Teil eines größeren Layouts?
