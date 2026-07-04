# Stufe 10 — Lesung: p18, die "tabula rasa"-Seite

**Brille:** "Was ist die Struktur von p18?"

**Was ich aus Stufe 0-9 mitnehme:**
- 997 Glyphen, 23 Seiten
- 4 Zonen identifiziert: Glyphen-Hotspot, Latein-Korridor, Formel-Sturm, Übergang
- p17_R7 und p18_R7 haben identische 49755-px-Glyphen (senkrechte Spalte) — Stufe 8
- math_times ist SOLO-OPERATOR (Stufe 9) — kommt nie mit anderen Vks zusammen vor
- BURUMUT-Matrix auf p23 ist ein 11×11-Raster
- 5 kolossale Unbekannte auf den Seiten

**Frage:** p18 hat 0 Latin, 24 Glyphen, 9 Formeln, 3 math_times. Was macht diese Seite strukturell aus?

**Schmeh-Quelle** (`/run/media/julian/ML4/tengri137/consecutive_reading/Tengri137_raw_text.txt`):
- p18 enthält **16 gepaarte Primfaktorzerlegungs-Quotienten** (gleich wie p17)
- "16 paired prime-factorisation quotients, same structure as page 17; '-' dash rows act as fraction bars."
- Beispiel-Struktur:
  ```
  2 * 3^2 * 5 * 163 * 179 * 643 * 1557763 * 5161229
  --------------------------------------------------
  19 * 23 * 131 * 1039776975733464433
  ```

**Sekundärquelle:** Schmehs `symbol_index.tsv`:
- "3x3 magic square (P05–P08); row/column/diagonal sums to 666." → 3x3-Strukturen erwartet
- "Row of '-' used as a typographic fraction bar" → Bruchstrich-Struktur
- "Vertical line" → 49755-px-Glyph auf p17/p18

**Vermutungen:**
- p18 ist KEINE tabula rasa, sondern eine **Primfaktorzerlegungs-Tabelle** mit 16 Zeilen
- Die 3 math_times markieren die Multiplikations-Operatoren
- Die 49755-px-Glyphe (senkrechte Linie) ist die Bezugslinie
- Die "-" rows (Bindestriche) sind Bruchstriche (Schmeh: "fraction bars")
- p17 und p18 sind spiegelsymmetrisch in der Struktur

**Methode:**
1. p18 Glyphen in x,y-Reihenfolge auflisten
2. 3 math_times lokalisieren und Relation zu den anderen Glyphen
3. 49755-px-Glyph-Position mit p17 vergleichen
4. Schmeh-Struktur (16 Quotienten) mit Vision-Struktur (24 Glyphen) abgleichen
