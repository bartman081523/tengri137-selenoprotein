# Stufe 0 — Lesung: Was haben wir eigentlich?

**Brille:** Keine. Reine Aggregation.

**Was ich getan habe:** Ich habe die `doc.json` geöffnet und geschaut,
was die Top-Level-Struktur ist. Dann habe ich die `pages/p01.json`
geöffnet, um eine Region im Detail zu sehen. Dann habe ich zurück zur
`doc.json` und aggregiert.

**Was ich sehe (ohne irgendetwas zu wissen):**

1. **23 Seiten** mit maschinenlesbarer Beschreibung.
2. Jede Seite hat:
   - `image_size` (Pixel)
   - `n_glyphs`, `n_latin_tokens`, `n_regions` (Counts)
   - `schmeh_hint` (was eine externe Quelle für richtig hält)
   - `schmeh_validation` (Vergleich mit V4-Pipeline)
   - `regions[]` (das eigentliche Material)
3. Jede Region hat:
   - `region_id`, `bbox` (Position)
   - `region_type` (latin_text, numeric_table, single_glyph, graphic_line, magic_cube, glyph_block, glyph_raster, burumut_block, formula_block, header, footer, …)
   - `description` (kurze Notiz)
   - `glyphs[]` (jede Glyphe mit Metadaten)
   - `latin_tokens[]` (jeder lateinische Text-Token mit Quelle und Konfidenz)

**Was mich stutzen lässt (erstes naives Bemerken):**

- Es gibt **3 Quellen** für lateinische Texte: `schmeh_hint`, `schmeh_complete`, `vision`. Das deutet darauf hin, dass die V4-Pipeline lateinische Texte **erkannt** hat (vision), nicht nur kopiert.
- Es gibt **745 Glyphen ohne Vision-Confidence** (von 997) — also 75% der Glyphen sind dem Vision-System unbekannt. Was sind das für Glyphen?
- Es gibt **17 vision_kinds** — eine ganze Taxonomie von Symbol-Typen.
- Es gibt einen `burumut_block` Region-Typ (auf p23) — ein bekanntes 11×11-Schema.
- Es gibt `magic_cube_3x3` und `odin_triple_horn` als vision_kinds — also wurde der Würfel und Odins Horn vom Vision-System erkannt.

**Was ich NICHT weiß:**

- Was die Glyphen BEDEUTEN.
- Welche Sprache der "Tengri-Schrift" zugrunde liegt.
- Ob die 88 `vision`-lateinischen Tokens korrekt sind.
- Wie die Schmeh-Hints zustande kamen.
- Was der "BURUMUTREFAMTU"-Block darstellt.

**Frage der Stufe 0:** Was ist die *Topologie* der Daten?
- Welche Region-Typen dominieren?
- Welche Vision-Kinds kommen vor, wie oft, wo?
- Welche Cluster-IDs gibt es, wie verteilt?
- Welche Latin-Token-Quellen dominieren pro Region-Typ?

Das ist die Grundkarte. Sie sagt mir, wo ich anfange.
