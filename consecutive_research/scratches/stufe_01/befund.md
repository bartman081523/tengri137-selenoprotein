# Stufe 1 — Befund: Die räumliche Karte

**Brille:** "Wo steht was?" Page × Region-Typ-Matrix.
**Methode:** `script.py` zählt für jede Seite: Regionen pro Typ, Glyphen, Latin, G/L-Ratio.

---

## 1) Vier Zonen des Dokuments

Aus der Klassifikation ergeben sich **vier klar trennbare Zonen**:

### ZONE A — Glyphen-Konzentrat (p05, p06, p08)
- **p05:** G=116, L=10, G/L=11.60
- **p06:** G=121, L=4, G/L=30.25  ← Maximum
- **p08:** G=67, L=7, G/L=9.57
- **Diese 3 Seiten enthalten 304 Glyphen = 30.5% aller Glyphen bei nur 21 Latin-Tokens.**

### ZONE B — Latein-Korridor (p09-p16, p21)
- p09-p16: G/L zwischen 1.6 und 2.9
- Latein- und Glyph-Anteil sind ausgewogen, aber Latein **leicht** überwiegt
- p21: G/L=1.14, ähnlich

### ZONE C — Formel-Sturm (p17, p18, p19, p20, p22, p23)
- **p17:** 11 Formel-Regionen (Maximum!)
- **p18:** 9 Formel-Regionen
- **p19:** 7 Formel-Regionen
- **p20:** 7 Formel-Regionen
- **p22:** 6 Formel-Regionen
- **p23:** 5 Formel-Regionen
- **Latin-Dominanz kehrt sich um:** G/L fällt unter 1, d.h. mehr Latein als Glyphen.

### ZONE D — Übergangszone (p01-p04)
- Latein-DOMINANT
- G/L zwischen 1.18 und 2.05
- Der "einleitende Fließtext"

---

## 2) Die drei "Sonderregionen"

```
magic_cube      → p08_R15
burumut_block   → p23_R20_LETTERBLOCK
numeric_table   → 13× verteilt (p01, p06, p07, p17, p18, p20, p22)
```

**Was mir auffällt:**
- `magic_cube` steht auf **p08**, nicht p06 (wie ich in Stufe 0 annahm). Ich hatte die Region-Liste nicht genau gelesen.
- `burumut_block` ist **p23_R20** und heißt im Region-Label "LETTERBLOCK" — die 11×11-Matrix.
- `numeric_table` ist **auffallend häufig auf p06** (4×: R9, R19, R22, R27). Was sind das für Zahlen-Tabellen, die mit dem Magic-Cube-Bereich zusammenstehen?

---

## 3) Formel-Regionen: die unentdeckte Schicht

**49 formula_block-Regionen verteilen sich NICHT gleichmäßig:**

| Seite | Formeln | latein_text |
|-------|---------|-------------|
| p17   | 11      | 5           |
| p18   | 9       | 6           |
| p19   | 7       | 10          |
| p20   | 7       | 5           |
| p22   | 6       | 8           |
| p23   | 5       | 9           |

**Was mir auffällt:**
- **Die Formel-Konzentration beginnt abrupt auf p17.** Vorher: 0-1 Formel pro Seite.
- **p17-p23 enthalten 45 der 49 Formeln (92%).**
- Latein-Text-Anteil sinkt in dieser Zone — als ob die Formeln Latein *ersetzen*.

---

## 4) Glyph/Latin-Ratio: die Verteilungskurve

```
G/L < 1 (Latein > Glyphen):  p17 (0.92), p19 (0.84), p23 (0.46)
G/L 1-3 (ausgewogen):        p01-p04, p09-p16, p20, p21, p22
G/L 3-10 (Glyph-dominant):   p05, p07, p08
G/L > 10 (extrem Glyph):     p06
G/L = ∞ (kein Latin):        p18
```

**Was mir auffällt:**
- **p23 ist die lateinste Seite** (G/L=0.46) — wegen der 65 Latin-Tokens (BURUMUTREFAMTU + 11×11 + Vorlauf).
- **p06 ist die glyphenstärkste Seite** (G/L=30.25).
- **p18 hat 0 Latin** — die tabula rasa.

---

## 5) Was hebt sich ab?

**Drei Seiten sind NICHT-klassifizierbar in das 4-Zonen-Schema:**

- **p18:** Hat 9 Formeln, 0 Latin, 24 Glyphen. Ist weder Glyph-noch-Latein-dominant. **Sonderfall.**
- **p23:** Hat 5 Formeln, 65 Latin (BURUMUTREFAMTU!), 30 Glyphen, **burumut_block** (11×11-Matrix). **Sonderfall.**
- **p06:** Hat 4 numeric_tables, 1 magic_cube_würfel, 121 Glyphen. **Sonderfall.**

Diese drei Sonderfälle sind die **Schlüsselseiten** des Dokuments.

---

## 6) Hypothesen, die jetzt entstehen

1. **Drei "Hotspots":** p05, p06, p08 sind die Glyphen-Hotspots. Was geschieht dort?
2. **Formel-Sturm p17-p23:** Die zweite Hälfte des Dokuments ist FORMEL-LASTIG. Was wird da gerechnet?
3. **p18 = tabula rasa:** Reine Formeln, keine lateinische Erklärung. Vielleicht die "Sprach-Schlüsselseite"?
4. **p23 = Schlussstein:** BURUMUTREFAMTU ist im **BURUMUT_BLOCK** angeordnet (11×11). Die 11 Zeilen sind lateinisch lesbar. Aber die 30 Glyphen daneben?

---

## Konkrete nächste Brille (Stufe 2)

**Stufe 2 — Die Vision-Kinds und ihre Geometrie**

Frage: Welche der 17 Vision-Kinds sind "Container" (Klammern, Linien), welche sind "Inhalt" (Buchstaben-ähnlich), welche sind "mathematisch" (π, ^, ×), welche sind "grafisch" (Würfel, Horn)?

Methode:
- Vision-Kind × Region-Typ-Matrix
- Vision-Kind × Page-Verteilung
- Vision-Kind × Geometrie (size_px, fill_ratio, n_components)

Erwartung: Es gibt eine **funktionale Grammatik** — einige Symbole öffnen, andere schließen, andere sind Inhalt.

**Konkret:**
- `geometric_bracket` (92, 36%) — wahrscheinlich **Container** (öffnen/schließen).
- `geometric_diamond` (12) und `geometric_diamond_with_dot` (12) — wahrscheinlich **Inhalt** (Buchstabe-ähnlich).
- `math_times` (13), `math_pi` (1), `math_exponentiation` (1) — **mathematische Operatoren**.
- `magic_cube_3x3` (1), `odin_triple_horn` (1) — **Ikonen**.
- `punctum` (12) — vielleicht **Punkte/Trenner**.

Das wird die **funktionale Karte** liefern.
