# Stufe 3 — Lesung: Was liest das Vision-System parallel zu Schmeh?

**Brille:** "Was sieht das ML-Modell, das Schmeh auch sieht? Wo decken sie sich, wo widersprechen sie sich?"

**Was ich aus Stufe 0-2 mitnehme:**
- 456 Latin-Tokens aus 3 Quellen: schmeh_hint (266), schmeh_complete (102), vision (88)
- 80 Vision-Tokens haben conf > 0.8
- Vision-Tokens kommen aus 3 Region-Typen: latin_text (51), formula_block (21), header (16)
- Vision-Examples: "I CAN READ" (p01), "DINARY INDIVIDUALS" (p09), "COMPLETE GAPS THE" (p11)

**Sekundärquelle (read-only):**
- `/run/media/julian/ML4/tengri137/consecutive_reading/Tengri137_raw_text.txt` — Schmehs vollständige Transkription

**Frage:** Wo stimmen Vision und Schmeh überein, wo divergieren sie? Welche lateinischen Wörter sind *doppelt belegt*?

**Vermutungen:**
- "I CAN READ" auf p01_R11 (Vision conf=0.96) ist eine direkte Aussage. Schmeh sollte das auch haben.
- "COMPLETE GAPS THE" auf p11_R2 (Vision conf=0.85-0.9) klingt nach einem Fragment. Was sagt Schmeh dazu?
- "DINARY INDIVIDUALS" auf p09_R5 (Vision conf=0.85) klingt nach "ordinary individuals" — aber ist das eine Übersetzung oder ein Fragment?

**Methode:**
1. Sammle alle Vision-Tokens pro Region
2. Sammle alle Schmeh-Tokens (hint + complete) pro Region
3. Vergleiche Text-Inhalte region-weise
4. Identifiziere Übereinstimmungen und Konflikte
5. conf-Verteilung der Vision-Tokens

**Was ich zu lernen hoffe:**
- Welche lateinischen Texte sind **robust** (in mehreren Quellen).
- Welche sind **fragmentarisch** (Vision sieht nur Teile).
- Welche sind **nur in einer Quelle** vorhanden.
