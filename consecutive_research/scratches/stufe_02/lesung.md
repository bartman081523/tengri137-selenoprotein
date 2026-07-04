# Stufe 2 — Lesung: Welche Vision-Kinds gibt es, und was bedeuten sie geometrisch?

**Brille:** "Was ist die funktionale Grammatik der 17 Symbol-Typen?"

**Was ich aus Stufe 0/1 mitnehme:**
- 17 vision_kinds, 255 Glyphen MIT Vision-Description, 742 OHNE
- Region-Typen: 11 Typen, mit räumlicher Verteilung
- 4 Zonen: Glyphen-Konzentrat (p05/06/08), Latein-Korridor (p09-p16), Formel-Sturm (p17-p23), Übergangszone (p01-p04)

**Frage:** Welche Vision-Kinds sind CONTAINER (öffnen/schließen), welche INHALT (Buchstabe-ähnlich), welche MATHEMATISCH (Operatoren), welche IKONEN (Bilder)?

**Vermutung (zu prüfen):**
- `geometric_bracket` (92, 36%) → CONTAINER
- `geometric_diamond` (12) und `geometric_diamond_with_dot` (12) → INHALT
- `math_times` (13), `math_pi` (1), `math_exponentiation` (1) → MATH
- `magic_cube_3x3` (1), `odin_triple_horn` (1) → IKONEN
- `punctum` (12) → TRENNER
- `turkic_round_rune` (7) → INHALT (Runen-ähnlich)
- `geometric_circle` (9), `geometric_circle_with_dot` (1), `geometric_filled_square` (1) → INHALT
- `line` (5) → TRENNER/CONTAINER
- `digit` (3) → INHALT (Zahlen)
- `other` (52) → UNKLAR
- `unknown` (32) → UNKLAR

**Methode:**
1. Vision-Kind × Region-Typ-Matrix
2. Vision-Kind × Page-Verteilung
3. Vision-Kind × Geometrie (Größe, fill_ratio, n_components)
4. Vision-Kind × Cluster-ID (Passung?)

**Was die Daten mir sagen könnten:**
- Wenn ein Vision-Kind IMMER in derselben Region-Type auftaucht → funktional spezialisiert
- Wenn ein Vision-Kind überall auftaucht → funktional generisch
- Wenn die Geometrie zwischen zwei Vision-Kinds identisch ist → vielleicht dasselbe Symbol?
