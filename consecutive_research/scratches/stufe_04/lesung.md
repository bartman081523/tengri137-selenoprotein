# Stufe 4 — Lesung: Die 332 "unbekannten" Glyphen

**Brille:** "Was ist die dunkle Materie des Dokuments?"

**Was ich aus Stufe 0-3 mitnehme:**
- 997 Glyphen total, 332 davon sind `type_hint=unknown` (33%)
- 742 haben keine Vision-Description
- Glyph-Verteilung: p05=116, p06=121, p08=67 (Hotspots)
- 17 Vision-Kinds, 24 Cluster-IDs
- p18 hat 0 Latin, 24 Glyphen

**Frage:** Wo konzentrieren sich die 332 Unbekannten? Sind sie ein **eigenes Material** (jenseits der 17 Standard-Symbole), oder einfach das ML-Versagen bei häufigen Symbolen?

**Vermutungen:**
- Die Unbekannten konzentrieren sich auf p05, p06, p08 (die Glyphen-Hotspots).
- p18 (24 Glyphen, 0 Latin) ist wahrscheinlich komplett unknown — die "tabula rasa".
- Vielleicht ist `type_hint=unknown` mit `cluster_id=GEOM_MEDIUM_UNKNOWN_*` identisch oder überlappt stark.

**Methode:**
1. Verteilung: Page × Region-Typ für `type_hint=unknown`
2. Verteilung: Cluster-ID
3. Verteilung: Vision-Kind (sind Unbekannte *immer* ohne Vision-Kind, oder gibt es welche MIT Vision-Kind aber `type_hint=unknown`?)
4. Geometrie (size, fill_ratio, n_components)
5. Vergleich: Unbekannte vs. Bekannte (geometric_bracket, math_times, etc.) — gleiche Geometrie?

**Sekundärquelle (read-only):** consecutive_reading/symbol_index.tsv hat eventuell Spalten, die mir weiterhelfen.
