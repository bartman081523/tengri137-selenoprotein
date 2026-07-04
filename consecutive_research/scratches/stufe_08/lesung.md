# Stufe 8 — Lesung: Position ist Information

**Brille:** "Sagen die x,y-Koordinaten der Glyphen etwas?"

**Was ich aus Stufe 0-7 mitnehme:**
- 997 Glyphen, 23 Seiten
- 4 Zonen: Glyphen-Hotspot p05/06/08, Latein-Korridor p09-p16, Formel-Sturm p17-p23, Übergang p01-p04
- Die BURUMUT-Matrix auf p23 ist ein 11×11-Raster
- p08_R15 ist eine 1×9-Reihe (magic_cube-Region)
- 5 kolossale Unbekannte, 2 identische 49755px-Glyphen auf p17/p18

**Frage:** Gibt es räumliche Muster, die **über die Region-Einteilung hinausgehen**? Reihen, Spalten, Diagonalen, Symmetrien?

**Vermutungen:**
- Auf p17_R7 und p18_R7 sind 2 identische 49755px-Glyphen. Beide könnten ein **zentrales Symbol** sein, das auf den Formel-Seiten wiederkehrt.
- Die BURUMUT-Matrix ist in einem Raster angeordnet (11×11).
- Vielleicht gibt es **Reihen gleicher Glyphen** auf einer Seite, die das V4-Region-System nicht erfasst hat.

**Sekundärquelle:** Schmehs `symbol_index.tsv`:
- "A 3x3 magic square (P05–P08); row/column/diagonal sums to 666." → 3x3-Strukturen erwartet
- "One of the 120 character cells in the 12x10 BURUMUT block" → Rasterstruktur
- "Row of '-' used as a typographic fraction bar" → lineare Strukturen

**Methode:**
1. Pro Seite: Glyphen-Centroids plotten (x, y)
2. Suche nach Reihen (gleiche y, ähnliche x)
3. Suche nach Spalten (gleiche x, ähnliche y)
4. Suche nach Symmetrie (links-rechts, oben-unten)
5. Identische Glyphen auf gleichen Positionen auf verschiedenen Seiten
