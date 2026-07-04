# Stufe 2 — Befund: Die funktionale Grammatik der Symbole

**Brille:** "Welche Vision-Kinds sind CONTAINER / INHALT / MATH / IKONEN / TRENNER?"
**Methode:** Vision-Kind × Region-Typ, × Page, × Geometrie, × Cluster-ID. 255 Glyphen, 17 Vision-Kinds.

---

## 1) Die KLASSIFIKATION (mit Begründung)

| Vision-Kind | n | Funktion | Wo? | Geometrie-Hinweis |
|-------------|---|----------|-----|-------------------|
| `geometric_bracket` | 92 | **CONTAINER** | 91× in latin_text | size_med 3100, fill 0.365, nc 18 |
| `other` | 52 | UNKLAR | 43× latin_text | 4008, 0.362, 16 |
| `unknown` | 32 | UNKLAR | 30× latin_text | 2890, 0.360, 16 |
| `math_times` | 13 | **MATH** | 12× formula_block | 2669, 0.203, **80** |
| `geometric_diamond_with_dot` | 12 | **INHALT** | 11× latin_text | 4885, 0.367, 28 |
| `punctum` | 12 | **TRENNER/INHALT** | 12× latin_text | 2695, 0.363, 18 |
| `geometric_diamond` | 12 | **INHALT** | 10× latin_text | 5446, 0.364, 32 |
| `geometric_circle` | 9 | **INHALT** | 5× graphic_line, 3× latin_text | 262, 0.364, **2** |
| `turkic_round_rune` | 7 | **INHALT** | 5× latin_text | 2748, 0.367, 14 |
| `line` | 5 | **TRENNER** | latin_text | 861, 0.398, 4 |
| `digit` | 3 | **ZAHL** | formula_block | 1015, 0.177, 36 |
| `geometric_filled_square` | 1 | INHALT | p02 latin | 1889, 0.386, 12 |
| `magic_cube_3x3` | 1 | **IKONE** | p06 graphic_line | 3573, 0.065, 2 |
| `odin_triple_horn` | 1 | **IKONE** | p06 latin_text | 784, 0.358, 4 |
| `geometric_circle_with_dot` | 1 | INHALT | p08 numeric_table | 278, 0.414, 2 |
| `math_pi` | 1 | **MATH** | p14 formula_block | 1647, 0.404, 8 |
| `math_exponentiation` | 1 | **MATH** | p19 formula_block | 2504, 0.236, **79** |

---

## 2) Die CONTAINER-Frage

**`geometric_bracket` ist der Container (91 von 92 in latin_text).** Das ist 36% aller Vision-beschriebenen Glyphen.

**Aber:** 92 Glyphen mit "Klammer"-Beschreibung. In 92 lateinischen Text-Regionen. Das deutet darauf hin, dass **jede lateinische Zeile Klammern enthält** — möglicherweise als Text-Marker.

**Außerdem:** `punctum` (12, alle in latin_text) hat **gleiche Geometrie** wie `geometric_bracket` (fill_med 0.363 vs 0.365). Vielleicht sind das **verwandte Formen** (Punkt innerhalb/außerhalb der Klammer)?

---

## 3) Die IKONEN (1er-Glyphen)

Drei "Sonderlinge":
- **`magic_cube_3x3`** auf **p06** (graphic_line) — die Würfel-Glyphe, fill_ratio 0.065 (sehr "luftig" — ein Gitter?)
- **`odin_triple_horn`** auf **p06** (latin_text) — Odins dreifaches Horn
- **`geometric_circle_with_dot`** auf **p08** (numeric_table) — Kreis mit Punkt, klein (278px)

**Was mir auffällt:**
- **p06 hat BEIDE Ikonen** (magic_cube_3x3 UND odin_triple_horn). Das ist kein Zufall — p06 ist die "Ikonen-Seite".
- Aber: Der Region-Typ `magic_cube` ist auf **p08_R15** (nicht p06)! Die Glyphe `magic_cube_3x3` ist auf p06. **Region und Glyphe sind nicht dasselbe.**

---

## 4) Die MATH-Symbole

| Symbol | Position | Geometrie |
|--------|----------|-----------|
| `math_times` (13) | über 9 Seiten verteilt, **12× in formula_block** | nc=80 (sehr komplex!) |
| `math_pi` (1) | p14 formula_block | nc=8 |
| `math_exponentiation` (1) | p19 formula_block | nc=79 (fast wie math_times!) |

**Was mir auffällt:**
- `math_times` und `math_exponentiation` haben **fast identische n_components** (80 vs 79). Sie sind **geometrisch Zwillinge**.
- `math_pi` ist geometrisch viel einfacher (nc=8) — passt zum griechischen Buchstaben.
- **math_times verteilt sich über 9 Seiten** — ist ein *allgegenwärtiger Operator*.
- `digit` (3) verteilt sich auf p12, p19, p23 — Konzentration in der FORMEL-ZONE (p17-p23).

---

## 5) Die INHALT-Taxonomie

**`geometric_diamond` (12) und `geometric_diamond_with_dot` (12):**
- Beide haben hohe `n_components` (28-32)
- `geometric_diamond_with_dot` ist **kleiner** (4885 vs 5446)
- Vielleicht sind das **Buchstabe-ähnliche** Symbole — der "Punkt in der Raute" deutet auf **diakritische Zeichen** hin.

**`geometric_circle` (9):**
- 5 von 9 sind in `graphic_line` (nicht in latin_text!)
- nc=2 (sehr einfach)
- size_med nur 262 — sehr kleine Glyphen
- **Könnten PUNKT-Markierungen am Zeilenrand sein**, nicht Inhalt.

**`turkic_round_rune` (7):**
- 5 von 7 in latin_text
- Größe 2748, nc=14
- **Runen-Form**, möglicherweise die "tatsächlichen Buchstaben" des Tengri-Skripts

**`line` (5):**
- ALLE in latin_text
- Größe 861, sehr klein
- **Trennstriche** zwischen lateinischen Elementen

---

## 6) Das `other` (52) — der größte unbestimmte Block

**52 Glyphen, 20% aller Vision-beschriebenen.** Sie sind:
- 43× in latin_text
- Über 14 Seiten verteilt
- Geometrie ähnlich wie `geometric_bracket` (4008, 0.362, 16)
- **Höchstwahrscheinlich eine Variante der Klammer-Form**, aber vom Vision-System als "andere Form" klassifiziert.

**Frage:** Ist `other` = `geometric_bracket` mit leichten Variationen? Oder eine eigene Symbolklasse?

---

## 7) Was die Cluster-IDs sagen

**Top-Zuordnungen:**
- `geometric_bracket` (49) ↔ `GEOM_MEDIUM_MATH_TIMES_0018` (der größte Cluster, 294 Glyphen)
- `other` (24) ↔ `GEOM_MEDIUM_MATH_TIMES_0018`
- `unknown` (16) ↔ `GEOM_MEDIUM_MATH_TIMES_0018`
- `punctum` (21) ↔ `GEOM_MEDIUM_PUNCTUM_0013`

**Was mir auffällt:**
- Der größte geometrische Cluster (`MATH_TIMES_0018`, 294 Glyphen) enthält:
  - 49 Klammern
  - 24 "other"
  - 16 unknown
  - 11 math_times
  - 7 turkic_round_rune
  - 7 geometric_diamond
  - 7 geometric_diamond_with_dot
  - 6 punctum

  → **Das ist der "Grundstock" des Dokuments.** Ein ubiquitärer Cluster, der Klammern, math_times UND Inhalt enthält. Sehr seltsam — sollte er nicht spezialisiert sein?

- Der **zweite** Hauptcluster ist `PUNCTUM_0013` (93 Glyphen), in dem `punctum` (21) und `other` (10) dominieren. Das ist konsistent — der Punctum-Cluster enthält vor allem Punkte.

---

## 8) Hypothesen, die jetzt entstehen

1. **`geometric_bracket` und `punctum` sind Container** — sie rahmen lateinischen Text ein, möglicherweise als visuelles Layout-Element.
2. **`math_times` ist ALLGEGENWÄRTIG** — nicht nur in Formeln, sondern überall. Ist es wirklich "Multiplikation" oder ein häufig verwendetes Layout-Zeichen?
3. **`turkic_round_rune` (7) ist möglicherweise der "echte Tengri-Buchstabe"** — die Runen-Form hebt sich ab.
4. **`geometric_diamond` und `geometric_diamond_with_dot` sind Diakritika** — der Punkt-in-Raute unterscheidet Varianten.
5. **`math_pi` und `math_exponentiation` sind isoliert** (je 1×) — sie sind Schlüssel-Symbole an Schlüssel-Positionen (p14, p19).
6. **p06 ist die Ikonen-Seite** (Magic Cube + Odin Horn).

---

## 9) Die unbeantworteten Fragen

- **Was sind die 52 `other`-Glyphen?** Warum unterscheidet das Vision-System sie von `geometric_bracket`?
- **Was sind die 32 `unknown`?** Warum scheitert die Klassifikation?
- **Warum ist `math_times` in einem Cluster mit `geometric_bracket`?** Sind sie sich geometrisch ähnlich?
- **Was symbolisiert `geometric_circle_with_dot` in einer numeric_table auf p08?**

---

## Konkrete nächste Brille (Stufe 3)

**Stufe 3 — Die Latin-Tokens: Schmeh vs Vision**

Frage: Bei welchen lateinischen Wörtern stimmen Vision und Schmeh überein? Bei welchen nicht?

Methode:
- Pro lateinischem Token-Vorkommen: Schmeh-Text und Vision-Text gegenüberstellen
- Übereinstimmungen: vielleicht "I CAN READ", "COMPLETE SERIES WITHOUT GAPS" etc.
- Konflikte: wo sagt Schmeh A und Vision sagt B?
- Welche Quellen dominieren pro Region-Type?

Erwartung:
- Vision-Latein ist eine **unabhängige zweite Lesart**.
- Wo Vision und Schmeh übereinstimmen → wahrscheinlich korrekt.
- Wo sie divergieren → vielleicht ist der Text **kontaminiert** oder es gibt Mehrdeutigkeiten.

Außerdem: **80 Vision-Tokens mit conf > 0.8** wurden in Stufe 0 identifiziert. Was steht da genau?
