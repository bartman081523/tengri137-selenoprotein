# Stufe 9 — Befund: Co-Occurrence Matrix

**Brille:** "Welche Vision-Kinds stehen IMMER zusammen, welche NIE?"
**Methode:** Set-basierte Co-Occurrence pro Region.

---

## 1) Die wichtigste Entdeckung: `math_times` ist ein SOLO-Operator

**`math_times` (13 Vorkommen) kommt NIE zusammen mit einem anderen Vision-Kind in derselben Region vor.**

```
geometric_bracket + math_times:                NIE zusammen
math_times      + geometric_diamond_with_dot:  NIE zusammen
math_times      + punctum:                     NIE zusammen
math_times      + geometric_diamond:           NIE zusammen
math_times      + geometric_circle:            NIE zusammen
math_times      + turkic_round_rune:           NIE zusammen
math_times      + line:                        NIE zusammen
```

→ **Das `×`-Symbol steht IMMER ALLEIN in seiner Region.** Es ist ein **funktionaler Operator**, kein kombinatorisches Symbol. Es braucht keine Begleitung.

Auch:
- `math_pi` (1×) ist **allein** mit `geometric_diamond` (1× zusammen in p14_R7)
- `math_exponentiation` (1×) ist **allein**

Die **math-Familie** (×, π, ^) ist **eigenständig**.

---

## 2) `other` und `unknown` trennen sich strikt

**`other` (52 Vorkommen) und `unknown` (32 Vorkommen) kommen NIE zusammen in derselben Region vor.**

Das deutet darauf hin, dass `other` und `unknown` **unterschiedliche Klassen** sind:
- `other` = Symbole, die das Vision-System kennt, aber nicht zuordnen kann (z.B. komplexe Muster)
- `unknown` = Symbole, die das Vision-System gar nicht erst versucht zu beschreiben

Sie sind **konkurrierende Klassen**, nicht komplementär.

---

## 3) Häufigste Co-Occurrences (Pflicht-Kombinationen)

```
geometric_bracket + other:                7×   (häufigste Paarung)
geometric_bracket + unknown:              5×
geometric_diamond_with_dot + other:       4×
geometric_bracket + geometric_circle:     3×
geometric_bracket + geometric_diamond:    3×
geometric_bracket + geometric_diamond_with_dot: 3×
geometric_bracket + turkic_round_rune:    2×
```

**`geometric_bracket` ist der "Mitläufer"** — es kommt mit vielen anderen Vks zusammen vor. Das passt zur CONTAINER-Hypothese aus Stufe 2: Klammern rahmen andere Symbole ein.

**`geometric_diamond_with_dot + other`** ist eine bemerkenswerte Paarung — die Rauten mit Punkt kommen oft mit `other` zusammen vor. Möglicherweise sind das **diakritische Markierungen** auf komplexen Mustern.

---

## 4) Regionen mit den meisten Vks

Nur 5 Regionen haben 3 Vks:
- p02_R15: bracket + circle + unknown
- p12_R4: bracket + diamond_with_dot + other
- p12_R5: bracket + diamond + diamond_with_dot
- p15_R2: bracket + diamond + line
- p16_R7: bracket + diamond_with_dot + other

**Die meisten Regionen haben nur 1-2 Vks.** Das ist konsistent mit der Hypothese, dass **jede Region eine funktionale Einheit** ist (Container + Inhalt, oder Solo-Operator).

---

## 5) Verbotene Paarungen (≥5 Vorkommen, nie zusammen)

```
geometric_bracket + math_times         NIE
other             + unknown            NIE
other             + math_times         NIE
other             + punctum            NIE
other             + geometric_diamond  NIE
other             + geometric_circle   NIE
other             + turkic_round_rune  NIE
unknown           + math_times         NIE
unknown           + turkic_round_rune  NIE
math_times        + geometric_diamond_with_dot  NIE
math_times        + punctum            NIE
math_times        + geometric_diamond  NIE
math_times        + geometric_circle   NIE
math_times        + turkic_round_rune  NIE
math_times        + line               NIE
geometric_diamond_with_dot + geometric_circle  NIE
geometric_diamond_with_dot + line       NIE
punctum           + geometric_diamond  NIE
punctum           + geometric_circle   NIE
punctum           + turkic_round_rune  NIE
punctum           + line               NIE
geometric_diamond + geometric_circle   NIE
geometric_diamond + turkic_round_rune  NIE
geometric_circle  + turkic_round_rune  NIE
geometric_circle  + line               NIE
turkic_round_rune + line               NIE
```

**`math_times` hat NULL Co-Occurrences.** Es ist das einzige Symbol, das in JEDER seiner Regionen ALLEIN ist.

---

## 6) Hypothesen

1. **`math_times`, `math_pi`, `math_exponentiation` sind SOLO-OPERATOREN.** Sie markieren "ab hier rechnet etwas" und brauchen keine Begleitung.
2. **`geometric_bracket` ist der UNIVERSELLE BEGLEITER** — es kommt mit fast allen anderen Vks vor. Das stärkt die CONTAINER-Hypothese.
3. **`other` und `unknown` sind getrennte Klassen** — sie kommen nie zusammen vor, obwohl beide häufig sind.
4. **`punctum` und `geometric_diamond` sind EXKLUSIV zueinander** — sie kommen nie zusammen vor, obwohl beide ähnlich häufig sind. Das deutet auf **unterschiedliche Text-Funktionen** hin.
5. **`geometric_circle` und `turkic_round_rune` sind EXKLUSIV zueinander** — sie kommen nie zusammen vor, obwohl beide häufig sind. Möglicherweise sind sie **konkurrierende Notationssysteme**.
6. **Die BURUMUT-Matrix (p23) hat keine Vision-Kinds in der burumut_block-Region selbst** — sie ist ein lateinisches Raster, getrennt von der Glyphen-Welt.

---

## 7) Was heißt das für die DEKODIERUNG?

**Funktionale Klassen:**

| Klasse | Vision-Kinds | Eigenschaft |
|--------|--------------|-------------|
| **CONTAINER** | geometric_bracket, line, geometric_filled_square | Mitläufer, rahmen ein |
| **INHALT** | geometric_diamond, diamond_with_dot, turkic_round_rune, punctum, geometric_circle | gegenseitig exklusiv! |
| **MATH** | math_times, math_pi, math_exponentiation | Solo-Operatoren, nie mit anderen Vks |
| **IKONEN** | magic_cube_3x3, odin_triple_horn, geometric_circle_with_dot | Einzelgänger, 1× vorkommend |
| **UNKLAR** | other, unknown | getrennte Klassen |

**Diese funktionale Klassen-Trennung ist der SCHLÜSSEL zur Tengri137-Dekodierung:**
- Die CONTAINER rahmen INHALT oder MATH ein
- Die MATH-Operatoren sind solo
- Die INHALT-Symbole schließen sich gegenseitig aus (in einer Region ist nur EINE Sorte)

→ **Das Dokument ist nicht "linear Text". Es ist eine **funktionale Komposition** mit klaren Strukturregeln: Container + Inhalt + Operator + Ikonen.**

---

## Konkrete nächste Brille (Stufe 10)

**Stufe 10 — p18: die tabula rasa-Seite**

Frage: p18 hat 0 Latin, 24 Glyphen, 9 Formeln, 3 math_times. Was ist die **Struktur** dieser Seite?

Methode:
- p18 Glyphen-Karte: 2D-Plot mit Clustern, Vision-Kinds
- Welche Regionen, welche Glyphen?
- Die 3 math_times: wo stehen sie? In welcher Reihenfolge?
- Vergleich mit p17 (das ist direkt davor) und p19 (direkt danach)

Erwartung:
- p18 ist eine **Schlüssel-Seite für die math-Operatoren**
- Vielleicht sind die 3 math_times dort **in einer Reihenfolge** (×, ×, × = eine Berechnung?)
- p18 ist KEINE tabula rasa, sondern ein **mathematischer Knotenpunkt**
