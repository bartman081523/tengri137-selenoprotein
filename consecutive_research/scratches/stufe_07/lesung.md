# Stufe 7 — Lesung: Geometrische Familien jenseits der 24 Cluster

**Brille:** "Welche Glyphen 'gehören zusammen' — über die offiziellen Cluster hinaus?"

**Was ich aus Stufe 0-6 mitnehme:**
- 997 Glyphen, 24 Cluster, 17 Vision-Kinds
- Größter Cluster MATH_TIMES_0018 (294 Glyphen, 30% der Gesamtmenge)
- Zweitgrößter CIRCLE_WIT_0008 (189 Glyphen, 19%)
- 5 kolossale Unbekannte (size>17000, fill<0.21) auf p03-R19, p04-R19, p07-R12, p08-R10, p09-R6
- 332 `type_hint=unknown`, davon 53% in CIRCLE_WIT_0008

**Frage:** Gibt es **geometrische Familien**, die die 24 offiziellen Cluster weiter unterteilen? Welche Glyphen sind sich ähnlich, obwohl sie verschiedenen Clustern zugeordnet sind?

**Vermutungen:**
- Die **5 kolossalen Unbekannten** sind eine eigene Familie (riesig, luftig, n_components > 100).
- Die **kleinen Kreise** in `CIRCLE_WIT_0009` (fill<0.3, size 1300-3800) sind eine andere Familie — vertikale Strich-Glyphen.
- Vielleicht ist `MATH_TIMES_0018` (der größte Cluster) **intern heterogen** — er enthält Klammern, Punkte, Rauten, alles in einem Topf.

**Sekundärquelle:** Schmehs `symbol_index.tsv` listet:
- LATIN_PRINT, LATIN_PRINT_RED
- MAGIC_SQUARE, RING (9 RINGS, 7 RINGS)
- ODIN_HORN, BURUMUT_CELL
- TURKIC_ROUND_RUNE
- TIAN (chinesisches Zeichen)
- TENGRI_RUNE, BRACKET, PUNCTUM, DIAMOND, CIRCLE, etc.

Diese Einteilung ist **eine andere als die V4-Cluster**. Möglicherweise gibt die Geometrie-Analyse Hinweise auf **familienübergreifende Ähnlichkeiten**.

**Methode:**
1. size_px × fill_ratio Plot, eingefärbt nach Cluster
2. n_components Verteilung
3. Sub-Cluster-Analyse: gibt es innerhalb der großen Cluster (MATH_TIMES, CIRCLE_WIT) unterscheidbare Untergruppen?
4. Korrelation: type_hint, vision_kind, cluster_id — wo stimmen sie überein, wo nicht?
5. Vergleich: Glyphen mit vs. ohne Vision-Description (Geometrie-Unterschied?)
