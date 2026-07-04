# Stufe 9 — Lesung: Co-Occurrence Matrix

**Brille:** "Welche Vision-Kinds stehen IMMER zusammen, welche NIE?"

**Was ich aus Stufe 0-8 mitnehme:**
- 997 Glyphen, 23 Seiten, 4 Zonen
- 17 vision_kinds, 24 cluster_ids
- geometric_bracket als CONTAINER
- geometric_diamond, punctum, geometric_circle, turkic_round_rune als INHALT
- math_times, math_pi, math_exponentiation als MATH
- magic_cube_3x3, odin_triple_horn, geometric_circle_with_dot als IKONEN
- 5 kolossale Unbekannte (size > 17000px)
- 2 identische 49755px-Glyphen auf p17/p18
- p05/p06 sind layout-zwillinge

**Frage:** Welche Vision-Kinds erscheinen IMMER zusammen, welche NIE?

**Sekundärquelle:** Schmehs `symbol_index.tsv`:
- "A 3x3 magic square (P05–P08); row/column/diagonal sums to 666." → 3x3-Strukturen
- "One of the 120 character cells in the 12x10 BURUMUT block" → Rasterstruktur
- "Row of '-' used as a typographic fraction bar" → lineare Strukturen

**Vermutungen:**
- Vielleicht steht `magic_cube_3x3` IMMER neben `geometric_bracket` (Container)
- Vielleicht steht `odin_triple_horn` IMMER neben `turkic_round_rune`
- Vielleicht gibt es "Pflicht-Trios" oder "verbotene Paarungen"

**Methode:**
1. Pro Region: alle Vision-Kinds sammeln (SET-basiert)
2. Co-Occurrence-Matrix (welche Paarungen kommen zusammen vor)
3. Pflicht-Paarungen (immer zusammen)
4. Verbotene Paarungen (nie zusammen, obwohl einzeln häufig)
5. Jaccard-Index: Wie ähnlich sind die Regions-Sets?
