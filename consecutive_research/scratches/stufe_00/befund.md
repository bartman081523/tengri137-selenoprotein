# Stufe 0 — Befund: Was sagt die Topologie?

**Brille:** Aggregation. Reine Verteilung. Keine Deutung.
**Methode:** `script.py` aggregiert 997 Glyphen × 456 Latin-Tokens × 492 Regionen.

---

## 1) Region-Typen: das Skelett des Dokuments

```
latin_text         355  (72.2%)  ← das Lateinische, klar dominierend
formula_block       49  (10.0%)  ← 1/10 sind Formeln
footer              20  (4.1%)
graphic_line        15  (3.0%)
glyph_block         15  (3.0%)
numeric_table       14  (2.8%)
single_glyph        13  (2.6%)
glyph_raster         7  (1.4%)
header               2  (0.4%)
magic_cube           1  (0.2%)  ← 1 Region auf p06
burumut_block        1  (0.2%)  ← 1 Region auf p23
```

**Was mir auffällt (ohne zu deuten):**
- `latin_text` dominiert (72%) — aber das ist nur die *Hülle*, nicht der Inhalt.
- 10% sind `formula_block` — das ist nicht trivial. Es gibt **49 Formel-Regionen** über 23 Seiten ≈ 2 pro Seite.
- `burumut_block` existiert als Region-Typ (auf p23). Das ist ein **eigenes Strukturelement**, nicht nur Glyphen.
- `magic_cube` existiert auch als eigener Region-Typ (1×). Auf p06.

---

## 2) Vision-Kinds: was hat das ML-Modell "gesehen"?

**255 Glyphen haben eine Vision-Description. 742 haben KEINE.**

```
geometric_bracket          92  (36.1%)  ← Klammern dominieren
other                      52  (20.4%)
unknown                    32  (12.5%)
math_times                 13  (5.1%)
geometric_diamond_with_dot 12  (4.7%)
punctum                    12  (4.7%)
geometric_diamond          12  (4.7%)
geometric_circle            9  (3.5%)
turkic_round_rune           7  (2.7%)
line                        5  (2.0%)
digit                       3  (1.2%)
magic_cube_3x3              1  (0.4%)  ← der Würfel wurde erkannt
odin_triple_horn            1  (0.4%)  ← Odins Horn wurde erkannt
math_pi                     1  (0.4%)  ← π ist da
math_exponentiation         1  (0.4%)  ← ^ ist da
```

**Was mir auffällt:**
- 36% sind **Klammern**. Das ist *kein Zufall* — das Dokument verwendet Klammern als häufigstes Strukturelement.
- 12.5% sind `unknown` (vom Vision-System selbst). Das sind die "besonders schwierigen".
- `math_pi` und `math_exponentiation` tauchen je **1×** auf. Das sind die "Schlüssel-Symbole" für später.
- `magic_cube_3x3` (1×) und `odin_triple_horn` (1×) — beide vom Vision-System erkannt. Das ist stark: zwei **hochkomplexe Symbole**, eindeutig identifiziert.

---

## 3) Glyph-Type-Hints: die Geometrie-Klassifikation

```
complex_symbol     486  (48.7%)
unknown            332  (33.3%)
punctum             96  (9.6%)
geometric_symbol    42  (4.2%)
horizontal_line     24  (2.4%)
vertical_line       17  (1.7%)
```

**Was mir auffällt:**
- 49% sind `complex_symbol` — also **kein einzelner Strich**, sondern zusammengesetzt.
- 33% sind `unknown` (332 Glyphen!). Das ist die "dunkle Materie" des Dokuments.
- Nur 4% sind reine `geometric_symbol` (einfache geometrische Formen).
- Linien (horiz+vert) sind selten (~4%).

---

## 4) Latin-Tokens: 3 Quellen, unterschiedliches Gewicht

```
schmeh_hint        266  (58.3%)  ← externe Quelle, conf=0.5
schmeh_complete    102  (22.4%)
vision              88  (19.3%)  ← ML-eigene Erkennung, conf=0.7-0.96
```

**Was mir auffällt:**
- **88 vision-Latein-Tokens** sind die unabhängigste Datenquelle. Sie kommen aus dem ML-Modell selbst, nicht aus Schmeh.
- Die Kombination `vision × formula_block` (21) ist signifikant: das ML-Modell liest **Formeln**.
- 11 × `schmeh_complete × burumut_block` — die BURUMUT-Matrix ist **komplett lateinisch**.

---

## 5) Glyphen pro Page: die Verteilung

**Hotspots:**
- p05: 116 Glyphen
- p06: 121 Glyphen (Maximum!)
- p08: 67 Glyphen
- p11-p15: 45-56 Glyphen (das ist der "lange Mittelfluss")

**Cold:**
- p21: 16 Glyphen (Minimum)
- p22: 19 Glyphen
- p09: 18 Glyphen
- p17, p18: je 24 Glyphen

**Was mir auffällt:**
- p05 + p06 = **237 Glyphen auf 2 Seiten = 23.7%** des Gesamtbestands.
- p18 hat **0 Latin, nur Glyphen** — das ist die "tabula rasa" (Plan, Stufe 10).
- p17, p18, p21, p22 sind die glyphenarmen Seiten.

---

## 6) Cluster-IDs: die 24 distinkten Familien

```
GEOM_MEDIUM_MATH_TIMES_0018        294  ← größter Cluster (29.5%)
GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0008  189
GEOM_MEDIUM_PUNCTUM_0013            93
GEOM_MEDIUM_MATH_TIMES_0017         85
GEOM_MEDIUM_UNKNOWN_0003            58
GEOM_MEDIUM_UNKNOWN_0002            53
GEOM_MEDIUM_GEOMETRIC_CIRCLE_WIT_0009  37
GEOM_MEDIUM_TURKIC_ROUND_RUNE_0010  35
GEOM_MEDIUM_UNKNOWN_0005            32
GEOM_MEDIUM_UNKNOWN_0012            23
GEOM_MEDIUM_OTHER_0011              16
... (24 insgesamt, 1 SINGLETON bei glyph 996)
```

**Was mir auffällt:**
- Der größte Cluster heißt **MATH_TIMES_0018** mit 294 Glyphen. Aber er erstreckt sich über **glyph_index 5-993** — also *über das gesamte Dokument verteilt*. Das ist ein ubiquitäres Element.
- Die unbekannten Cluster (UNKNOWN_*) machen etwa 19% aller Glyphen aus.
- 1 SINGLETON (Cluster 0022, glyph 996) — eine Einzelerscheinung.
- **glyph 996 ist der einsamste Glyph des Dokuments.**

---

## 7) Geometrie: was sind das für Formen?

- **size_px:** 14 - 49.755. Median: 1.219. → Die meisten Glyphen sind mittelgroß (~1200px), einige winzig (14px), eines riesig (49.755px).
- **fill_ratio:** 0.033 - 0.771. Median: 0.363. → Die meisten Glyphen sind "luftig" (36% gefüllt), nicht kompakt.
- **n_components:** 1 dominiert (216 Glyphen sind EINKOMPONENTIG), aber 176 sind ZWEIKOMPONENTIG, 83 sind DREIKOMPONENTIG. → Die meisten Glyphen sind einfach, nicht zusammengesetzt. *Aber:* 7 Glyphen haben 637 Komponenten (!) — das sind die "Würfel".

---

## 8) High-Conf Vision-Latein: was liest das ML-Modell?

80 Vision-Tokens mit conf > 0.8. Beispiele:
- `IX` (p01, conf=0.85)
- `I CAN READ` (p01, conf=0.96)
- `Y` (p04, conf=0.95)
- `IF IS` (p05, conf=0.85)
- `DINARY INDIVIDUALS` (p09, conf=0.85) — **das ist deutsch! "dinary individuals" ≈ "gewöhnliche Individuen"?**
- `COMPLETE GAPS THE` (p11, conf=0.85-0.9) — **englisch! "Complete Gaps The ..."**
- `D` (p08, p10)
- `H` (p07 dreimal, p10)

**Was mir auffällt:**
- Das ML-Modell liest **Englisch und Deutsch** in lateinischen Texten.
- Auf p11 sagt es "COMPLETE GAPS THE" — das ist unvollständig, aber erkennbar.
- **p09 hat "DINARY INDIVIDUALS"** — das ist ein Fragment von "ordinary individuals"?
- Die Vision-Tokens sind also **kein Geheimcode**, sondern die normale lateinische Schrift, die das ML parallel mitliest.

---

## Was die Topologie **nicht** sagt (was wir nicht wissen)

- **Was die 332 unknown-Glyphen BEDEUTEN.**
- **Ob die 88 vision-Latein-Tokens korrekt sind** (einige sehen fragmentarisch aus).
- **Welche Sprache die Tengri-Glyphen "sprechen"** — falls sie eine sprechen.
- **Was der `burumut_block` semantisch darstellt** (BURUMUTREFAMTU ist lateinisch, aber die 30 Glyphen daneben?).
- **Ob der `magic_cube` ein Text, ein Bild, oder etwas Drittes ist.**

---

## Konkrete nächste Brille (Stufe 1)

**Stufe 1 — Die Region-Typen: Was steht WO?**

Frage: Welche Region-Typen dominieren pro Seite?
- Page × Region-Typ Matrix.
- Welche Seiten sind "lateinlastig", welche "glyphenlastig"?
- Wo sind die Formel-Seiten?
- Wo ist der `burumut_block` (p23), wo ist der `magic_cube` (p06)?

Erwartung: Es gibt **3-4 Klassen von Seiten**:
- Latein-DOMINANTE Seiten (p01-p04, p09-p22)
- Glyphen-DOMINANTE Seiten (p05, p06, p18, p23)
- Formel-CHARAKTER Seiten (überall 1-3 Formeln, aber konzentriert?)
- Hybrid-Seiten

Das wird die **räumliche Karte** des Dokuments liefern.
