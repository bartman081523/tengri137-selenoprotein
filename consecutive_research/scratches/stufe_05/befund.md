# Stufe 5 — Befund: Was sind die Ring-Sigille und der "Magic Cube"?

**Brille:** "Was sind die großen Unbekannten geometrisch, und was ist die `magic_cube`-Region wirklich?"
**Methode:** Detail p08_R15, 5 kolossale Unbekannte, Ring-Suche über alle Seiten.

---

## 1) P08_R15 ist KEIN 3×3-Würfel

**Schmehs Kontext:** "A 3x3 magic square (P05–P08); row/column/diagonal sums to 666."

**V4-Pipeline-Befund:** p08_R15 ist eine **1×9-Reihe**:

```
x= 273  idx=444
x= 353  idx=445
x= 427  idx=446
x= 490  idx=447
x= 545  idx=448
x= 605  idx=449
x= 668  idx=450
x= 741  idx=451
x= 833  idx=452
```

- 9 Glyphen in einer **horizontalen Linie** (y-Werte alle ~1080-1118, also ±20px Streuung)
- Abstand zwischen Glyphen: ~70-80px (sehr regelmäßig!)
- Alle 9 sind `cluster=GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0008`, alle `type_hint=unknown`
- Größe: 31×22 px (sehr kleine, einheitliche Glyphen)
- KEIN lateinischer Text in der Region

**Was das geometrisch sein KANN:**
- 9 kleine Markierungs-Glyphen (Punkte, Kreise, Stempel)
- KEIN 3×3-Würfel (V4 hat keine 3×3-Struktur)
- Möglicherweise **eine Trennlinie aus 9 gleichen Symbolen** zwischen Textblöcken
- Die "magische Summe zu 666" wäre nur als Beschriftung sichtbar (nicht in der Region)

**Achtung:** Schmehs "3x3 magic square" passt **nicht direkt** zu dem, was V4 als `magic_cube` markiert. Die V4-Pipeline hat eine **1×9-Reihe** gefunden, nicht ein 3×3-Layout. Schmeh interpretiert möglicherweise die **Bild-Ebene** (was er auf dem PDF sieht), während V4 die **Layout-Ebene** (Region-Strukturierung) erfasst.

---

## 2) Die 5 kolossalen Unbekannten — die echten Sigille?

| Glyph | Page | Region | Cluster | size_px | fill | nc | bbox (w×h) |
|-------|------|--------|---------|---------|------|-----|------------|
| idx=97 | p03 | R19 | UNKNOWN_0024 | 17.590 | 0.130 | ? | 366×370 |
| idx=98 | p03 | R19 | UNKNOWN_0024 | 26.290 | 0.205 | ? | 357×360 |
| idx=131 | p04 | R19 | UNKNOWN_0024 | 24.527 | 0.211 | ? | 293×397 |
| idx=389 | p07 | R12 | UNKNOWN_0023 | 24.288 | **0.041** | ? | 769×765 |
| idx=429 | p08 | R10 | UNKNOWN_0023 | 28.177 | **0.052** | ? | 735×734 |
| idx=473 | **p09** | R6 | UNKNOWN_0023 | **40.396** | 0.074 | **637** | 754×727 |

(Die 6. ist p09_R6 = "7 RINGS - 666" laut Schmeh.)

**Beobachtungen:**
- **Drei Familien** der Riesen-Glyphen, basierend auf Position:
  1. **p03_R19 + p04_R19** (3 Glyphen, Cluster UNKNOWN_0024, Größe 17-26k, fill 0.13-0.21)
  2. **p07_R12 + p08_R10** (2 Glyphen, Cluster UNKNOWN_0023, Größe 24-28k, fill 0.04-0.05 → SEHR luftig)
  3. **p09_R6** (1 Glyph, Cluster UNKNOWN_0023, Größe 40k, fill 0.07, **nc=637**)

- **Alle sind QUADRATISCH** (Höhe ≈ Breite, alle 700-770 px Kantenlänge)
- **Alle haben sehr niedrige fill_ratio** (0.04-0.21) → das sind OFFENE FORMEN, keine vollen Glyphen
- **Die nc-Werte** (Komponenten) sind extrem hoch — 637 für die "7 RINGS" ist plausibel (7 verschachtelte Kreise = 7+ Komponenten + Verbindungslinien)

**Was diese Glyphen sind (sehr wahrscheinlich):**
- **idx 97, 98, 131** (p03-R19, p04-R19): die **3×3 Magic-Squares** aus Schmehs Kontext (3 Stück, weil 3+3=6 in der "Odin triple horn"-Anordnung? Oder weil sie auf 2 Seiten verteilt sind?)
- **idx 389, 429** (p07-R12, p08-R10): die **6×6 Layouts**? Oder ein **2. Magic-Square-Paar**?
- **idx 473** (p09_R6): die **"7 RINGS"** (Schmehs Wortlaut, lateinischer Text dazu vorhanden: "SEVEN CIRCLES AND AN CROSS. A CONTINUOUS SEQUENCE W")

---

## 3) Die "9 RINGS" (p10) — wo sind sie?

**Schmehs Kontext:** "9 RINGS - 666" auf p10.

**V4-Pipeline-Befund:** Auf p10 gibt es **keine** Region mit großen quadratischen Glyphen. Aber:
- p10_R22 hat 1 Glyph (idx 518, cluster=OTHER_0021, size 2580, bbox 255×129) — ein **länglicher** Glyph, nicht quadratisch. Vielleicht ein Repräsentant der Ringe?
- p10_R18 hat 3 kleine CIRCLE_WIT-Glyphen (idx 508-510) — möglicherweise Teile der Ringe.

**Auf p10 gibt es möglicherweise eine ANDERE Art von "9 RINGS"** als auf p09. Vielleicht nicht-konzentrisch, sondern als Reihe?

---

## 4) Die "RING-VERDÄCHTIGEN" Glyphen (CIRCLE_WIT_0009)

Es gibt eine zweite Familie von "kreisförmigen" Glyphen, **vom Cluster `GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0009`**, mit fill_ratio 0.24-0.37 und Größen 1300-3800:

- p01_R1: idx 2, 3 (zwei große, in einer Reihe)
- p12_R13: idx 599-601 (drei große)
- p13_R2: idx 623-632 (acht große, vermutlich in einer Reihe)  ← das ist **die "9 RINGS" auf p13?!**
- p19_R15: idx 878
- p20_R16: idx 929

**p13_R2 hat 8 Glyphen vom Cluster CIRCLE_WIT_0009** (idx 623, 624, 626, 627, 628, 629, 631, 632). Sie sind in einer **horizontalen Reihe** (bbox x-Werte 201, 281, 363, 423, 621, 722, 807, 886 — das sind 8 Positionen, nicht 9, aber die meisten sind ~80-100px auseinander).

→ Möglicherweise sind die **"9 RINGS" auf p13**, nicht p10 wie Schmeh sagt. Oder Schmehs Seitenzuordnung ist falsch.

---

## 5) Was hat die V4-Pipeline ÜBERSEHEN?

Die V4-Pipeline hat:
- p08_R15 als `magic_cube` markiert (1×9-Reihe gleicher Glyphen)
- p09_R6 als "normale" `latin_text`-Region mit 1 großem Glyph (idx 473)
- p10, p11 nicht als `magic_cube` markiert (obwohl Schmeh dort Ringe sieht)
- Die 5 Riesen-Glyphen sind alle in `latin_text` oder `glyph_raster`-Regionen, NICHT als eigene Strukturelemente erkannt

**Folgerung:** Die V4-Pipeline hat die **großen Sigill-Strukturen nicht als eigene Regionen klassifiziert**, sondern als "Teile" des lateinischen Textes behandelt. Die `magic_cube`-Region p08_R15 ist NICHT das, was Schmeh als "3x3 magic square" beschreibt — das ist eine 1×9-Reihe kleiner Glyphen.

---

## 6) Hypothesen, die jetzt entstehen

1. **Die 5 Riesen-Glyphen sind die echten Sigille**, nicht p08_R15. p08_R15 ist eine Trennlinie.
2. **Drei Sigill-Gruppen:**
   - p03-R19 + p04-R19 (3 Magic-Squares, evtl. "Odin triple horn"-Layout)
   - p07-R12 + p08-R10 (zwei weitere Magic-Squares, evtl. "7+9 rings"-Paar)
   - p09-R6 (das "7 RINGS" Sigil, lateinisch beschriftet)
3. **Die "9 RINGS" auf p10 (Schmeh) sind möglicherweise p13_R2** (8 Glyphen, ähnliche Geometrie).
4. **Schmehs Seitenzuordnung weicht von V4 ab.** Schmehs "3x3 magic square (P05-P08)" ist möglicherweise etwas anderes als die V4-Region p08_R15.
5. **Die Riesen-Glyphen sind alle sehr "luftig"** (fill < 0.21). Das deutet auf **Kreise, Ringe, offene Muster** — möglicherweise konzentrische Kreise mit Verbindungslinien.

---

## Konkrete nächste Brille (Stufe 6)

**Stufe 6 — Die BURUMUT-Matrix auf p23**

Frage: Was ist die 11×11-Matrix `burumut_block` auf p23? Welche lateinischen Buchstaben, welche Glyphen, welche Anordnung?

Methode:
- p23_R20_LETTERBLOCK (= burumut_block) im Detail
- 11 Zeilen, je 11 Buchstaben
- Welche lateinischen Buchstaben kommen vor? Häufigkeit?
- Welche Glyphen sind in der Region?
- Schmehs Kontext: "BURUMUTREFAMTU" als Sequenz

Erwartung:
- Die 11×11-Matrix ist ein lateinisches Alphabet-Bild
- 30 Glyphen daneben: Was sind sie?
- Vision-Token auf p23: chemische Symbole (C, N, H, O) — ist die 11×11 ein molekularer Fingerprint?
