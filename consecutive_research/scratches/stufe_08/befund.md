# Stufe 8 — Befund: Position ist Information

**Brille:** "Was sagen die x,y-Koordinaten der Glyphen?"
**Methode:** 2D-Plot, Reihen-Suche, identische Glyphen auf verschiedenen Seiten.

---

## 1) Identische Glyphen auf p17 und p18 (DER Befund)

```
p17 p17_R7  idx=825  cx=893  cy=845  w=138  h=1170  cluster=UNKNOWN_0019
p18 p18_R7  idx=849  cx=893  cy=845  w=138  h=1170  cluster=UNKNOWN_0019
```

**Beide Glyphen sind:**
- **Identische Größe** (138×1170 px — eine senkrechte, schmale Spalte)
- **Identische Position** (cx=893, cy=845 — bei 70% der Seitenbreite, 60% der Seitenhöhe)
- **Identische Geometrie** (49755 px Fläche, fill=0.308)
- **Identische Cluster-Zugehörigkeit** (UNKNOWN_0019, der Cluster mit nur 2 Mitgliedern)

→ **Das ist kein Zufall.** Diese zwei Glyphen sind **identische Stempel**, möglicherweise eine **Bezugslinie** oder ein **vertikaler Markierungsstrich**, der die Formel-Seiten p17 und p18 verbindet.

---

## 2) Universal-Glyph: UNKNOWN_0012 = die Footer-Linie

```
GEOM_MEDIUM_UNKNOWN_0012  size=1084  n=23
bbox: [21, 1624, 1085, 2]  ← 1085×2 px horizontale Linie
type_hint: horizontal_line
```

**Auf ALLEN 23 Seiten** gibt es genau eine Glyphe mit dieser Geometrie — die **untere Trennlinie am Seitenfuß** (Footer). Das ist nur ein Layout-Element, kein rätselhafter Inhalt. Es ist die letzte Glyphe jeder Seite (idx 29, 63, 106, ..., 997).

---

## 3) Reihen gleicher Glyphen (gleiche y ± 30px)

**Hotspots:**
- **p13_R2 hat 12 Glyphen in einer Reihe** (y≈450, x=178-954, idx 622-633) — Möglicherweise die "9 RINGS" + 3 Extra-Glyphen.
- **p05/p06 haben ~6-7 Glyphen pro Zeile** in vielen y-Ebenen (270, 330, 360, 420, 450, 510, 540, 600, 630, 990, 1050, 1080, 1140, 1170, 1230, 1260, 1320, 1350) — sehr dichtes Glyphen-Raster.
- **p08 hat 5-6 Glyphen pro Zeile** in y 570-1380.

**Beobachtung:** p05 und p06 haben **sehr ähnliche Zeilenstrukturen**:
- p05 Zeile 270: x=[544, 619, 701]  vs  p06 Zeile 270: x=[538, 613, 695]
- p05 Zeile 330: x=[482, 563, 639, 686, 765]  vs  p06 Zeile 330: x=[486, 563, 644, 686, 765]

**Die x-Positionen sind fast identisch** (Differenz <10px). Das deutet auf ein **gemeinsames Layout-Raster** hin, das auf p05 und p06 wiederholt wird.

---

## 4) Die zwei "Zwillings-Seiten" p05 und p06

p05 und p06 haben:
- **fast identische Glyphen-Anzahl** (116 vs 121)
- **fast identische Zeilenstrukturen** (gleiche y-Ebenen, ähnliche x-Positionen)
- **denselben Glyph-Index-Bereich** (p05: 133-248, p06: 249-369)

→ **p05 und p06 sind VARIANTEN voneinander.** Möglicherweise sind sie **zwei Hälften eines größeren Musters** (z.B. zwei Spalten einer Tabelle, oder zwei Wiederholungen).

Auch **p07 und p08** haben ähnliche Strukturen (p07: 27 Glyphen, p08: 67 Glyphen — p08 ist möglicherweise eine "Expansion" von p07).

---

## 5) Was die 2D-Plots zeigen

Aus den ASCII-Plots:

- **p01-p04:** Glyphen in der oberen Hälfte (y < 1100), wenige in der unteren — typisches "Header + Body" Layout.
- **p05, p06, p07, p08:** Glyphen **dicht gepackt** in der oberen Hälfte (y < 800) — die Glyphen-Hotspots.
- **p09-p16:** Vereinzelte Glyphen, in verschiedenen Höhen — der "Latein-Korridor".
- **p17, p18, p19, p20, p21, p22, p23:** Mehr Glyphen in der **unteren** Hälfte — die Formel-Zone.

---

## 6) Glyphen, die auf mehreren Seiten an DENSELBEN Positionen stehen

```
GEOM_MEDIUM_UNKNOWN_0002  size=22: 21x auf 2 Seiten (p05, p06) — sehr ähnlich
GEOM_MEDIUM_UNKNOWN_0003  size=62: 10x auf 2 Seiten (p05, p06)
GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0008  size=230: 5x auf 2 Seiten (p07, p08)
```

**Diese Glyphen sind "Seiten-Stempel"** — sie wiederholen sich auf benachbarten Seiten. Das verstärkt die Hypothese, dass **p05/p06 ein Paar** und **p07/p08 ein Paar** sind.

---

## 7) Hypothesen

1. **p17_R7 und p18_R7 sind IDENTISCHE Glyphen** (senkrechte Spalte, 1170px hoch). Sie sind **kein Zufall**, sondern ein **gemeinsames Strukturelement**, das die beiden Formel-Seiten verbindet. Möglicherweise eine **"Bezugslinie"** oder ein **"Indexstrich"**.
2. **p05 und p06 sind layout-zwillinge** — gleiche Zeilenstrukturen, ähnliche Glyphen-Größen, gemeinsame Glyphen-Cluster.
3. **p07 und p08 sind layout-zwillinge** (in kleinerem Maßstab).
4. **p13_R2 hat 12 Glyphen in einer Reihe** (y≈450, x=178-954). Das ist möglicherweise die "9 RINGS"-Glyphenreihe + 3 Extra-Marker.
5. **Es gibt keinen einzelnen "geheimen" Glyph**, der nur auf einer Seite vorkommt — alle Glyphen wiederholen sich auf 2-23 Seiten.

---

## 8) Was heißt das für die DEKODIERUNG?

**Die BURUMUT-Matrix ist nicht die einzige "Raster-Struktur" im Dokument.** Es gibt:
- BURUMUT-Matrix auf p23 (11×11 lateinische Buchstaben)
- Magic-Cube-Reihe auf p08_R15 (1×9 kleine Glyphen)
- Reihen auf p05, p06, p07, p08, p13 (variable Glyphen-Anzahl)
- Zwillings-Glyphen auf p17/p18 (senkrechte Spalten)

**Alle diese Strukturen sind BILDER, keine Texte.** Sie sind **Zahlen-Magie** (666-Summen, Ring-Zählungen, Magic-Squares), nicht Sprache.

**Was die lateinischen Texte sind:** "GENETICALLY ENCRYPTED", "EMBEDDED IN OURR GENES" — der lateinische Text ist eine **ANLEITUNG**, nicht die Daten selbst. Die **Daten** sind die geometrischen Strukturen.

---

## Konkrete nächste Brille (Stufe 9)

**Stufe 9 — Co-Occurrence: Was steht zusammen?**

Frage: Welche Glyphen-Cluster / Vision-Kinds erscheinen IMMER zusammen in derselben Region? Gibt es **Pflicht-Kombinationen**?

Methode:
- Co-Occurrence-Matrix aller vision_kinds über alle Regionen
- Welche Vision-Kinds kommen NIE zusammen vor?
- Welche kommen IMMER zusammen vor?

Erwartung:
- Vielleicht steht `magic_cube_3x3` IMMER neben `geometric_bracket` (Container)
- Vielleicht steht `odin_triple_horn` IMMER neben `turkic_round_rune`
- Vielleicht gibt es "Pflicht-Trios" oder "verbotene Paarungen"
