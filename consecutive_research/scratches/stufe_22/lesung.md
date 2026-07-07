# Stufe 22 — Lesung: Leseraster-Analyse der BURUMUT-DNA

**Brille:** Welches Leseraster der BURUMUT-DNA ergibt eine offene Protein-Sequenz?

**Was ich aus Stufe 21 mitnehme:**
- p23_R17 enthält Cytosin + Thymin (DNA-Pyrimidin-Basen)
- BURUMUT = 154 AS × 3 = 462 DNA-Basen
- Sec-spezifische Codon-Tabelle: U→TGA, O→TAG
  - TGA erscheint 18× (= Sec in BURUMUT)
  - TAG erscheint 12× (= Pyl in BURUMUT)
  - **Perfekte Übereinstimmung — kein Zufall**

**Frage:** In welchem der 3 Leseraster (+1, +2, +3) wird BURUMUT translatiert?

**Sekundärquelle:** V4 doc.json (Eigenproduktion, `/run/media/julian/ML4/tengri137/consecutive_research/docs/doc.json`)

**Vermutungen:**
- Standard-Codon-Tabelle +1 ergibt 0 Stop-Codons (perfektes ORF)
- Aber: Standard-Tabelle kann Sec (TGA) und Pyl (TAG) nicht lesen
- Lösung: TGA und TAG sind KEINE Stop-Codons in der BURUMUT-Biochemie
- → Sec-spezifische Tabelle, aber dann ist +1 unterbrochen (30 Stops)

**Methode:**
1. DNA mit Standard- und Sec-spezifischer Codon-Tabelle
2. Alle 3 Leseraster in beiden Tabellen
3. Stop-Codon-Zählung pro Leseraster
4. ORF-Suche in beiden Tabellen
