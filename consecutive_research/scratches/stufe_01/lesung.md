# Stufe 1 — Lesung: Wo steht was?

**Brille:** "Welche Region-Typen dominieren pro Seite?"

**Was ich aus Stufe 0 mitnehme:**
- 11 Region-Typen (siehe topologie.json)
- 23 Seiten, 492 Regionen total
- magic_cube (1×, auf p06) und burumut_block (1×, auf p23) sind Einzelregionen
- latin_text dominiert global (72%)

**Frage:** Welche Seiten sind "lateinlastig", welche "glyphenlastig", welche "hybrid"?

**Vermutung (zu prüfen):**
- p05, p06 (Magic-Cube-Bereich) werden glyphenlastig sein
- p18 wird glyphen-only sein (0 Latin)
- p23 wird hybrid sein (Latin BURUMUTREFAMTU + 30 Glyphen)
- p01-p04 sind wahrscheinlich lateinlastig (Header, einleitender Text)

**Methode:** Page × Region-Typ-Matrix. Für jede Seite zähle ich die Regionen pro Typ.
Anschließend: Klassifikation in "latein-dominant" / "glyph-dominant" / "hybrid" / "formel-schwer".
