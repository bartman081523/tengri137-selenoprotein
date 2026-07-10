# AUDIT V10.4 ↔ Original-PNGs: Welche Behauptungen sind aus den 23 PNGs reproduzierbar?

**Datum:** 2026-07-10
**Kontext:** V10.4 Master-JSON (`consecutive_reading/bbox/v104_20260708/tengri137_complete_decoded_v104.json`) ist Gold-Standard. Diese Reverifikation prüft: **Welche V10.4-Werte lassen sich direkt aus den 23 Original-PNGs reproduzieren, welche sind methodische Konventionen, und welche stammen aus externen Quellen (Wikia, Schmeh, V7 Tappeiner, V8 Wikia-Alignment)?**

## Methodik der Klassifikation

Jeder V10.4-Claim wird einer von 4 Klassen zugeordnet:

| Klasse | Bedeutung | Reverifikation möglich? |
|--------|-----------|------------------------|
| **F** (Faktum) | Wert direkt aus PNG-Pixeln ableitbar (Tesseract, OpenCV, BBox-Detection, Y-Peaks) | JA, deterministisch |
| **K** (Konvention) | Wert durch heuristische Auswahl aus mehreren Möglichkeiten (z.B. "längster Kandidat") | NEIN ohne externe Quelle für die Auswahl |
| **E** (Extern) | Wert stammt aus externer Quelle (Wikia, Schmeh, Tappeiner-Decoder mit PERIODIC-Tabelle) | NEIN ohne Wikia |
| **P** (Pipeline) | Wert hängt von konkreter Pipeline ab (Tesseract-PSM, ML-Threshold) | BEDINGT, bei identischer Pipeline |

## Brücke 1: n_glyphs total = 1013 → **K + P**

**V10.4 sagt:** 1013 Glyphen (V9 v2 Smart-Parser), verteilt auf p1-p16 (p17-p23 = 0).
**V4 doc.json sagt:** 997 Glyphen (V4 Glyph-First PIVOT, 2026-07-04).
**Differenz:** 16 zusätzliche Glyphen aus V9 v2.

| Quelle | Methode | Wert | Klasse |
|--------|---------|------|--------|
| V4 doc.json | ML-Clustering auf BBox-Crops | 997 | F+P (Pipeline-spezifisch) |
| V10.4 v9/v10/v11 | V9 v2 Smart-Parser | 1013 | K (V9 v2 re-clustered V4-Glyphen) |

**Reverifikation aus PNGs:** Glyphen-Detection (BBox → ML-Cluster) ist **direkt reproduzierbar** (997 ± 5 sind plausibel). Der exakte Wert 1013 ist **V9 v2-Pipeline-spezifisch** und kann mit identischer Pipeline reproduziert werden, mit anderer Pipeline nicht.

**Konsequenz:** n_glyphs=1013 ist **kein Faktum**, sondern **V9 v2-Pipeline-Ergebnis**. Andere Pipelines (z.B. V4) liefern 997.

## Brücke 2: n_text_words_tesseract = 3677 → **P (Pipeline-abhängig)**

**V10.4 sagt:** 3677 lateinische Wörter total (p1-p23), z.B. p17=224, p20=313, p23=312.

| Seite | V10.4 Wert | Tesseract PSM | Reproduzierbar? |
|-------|-----------|---------------|-----------------|
| p17 | 224 | PSM=3 | JA, mit identischem Tesseract + p17-Region-Crop |
| p20 | 313 | PSM=3 | JA |
| p23 | 312 | PSM=3/4/6 | JA |

**Reverifikation:** Tesseract ist deterministisch (gleicher Input, gleicher Seed, gleiches Ergebnis). Wert ist **reproduzierbar mit identischer Pipeline**, aber Token-Definition (was ist ein "Wort"?) ist Pipeline-Wahl.

**Konsequenz:** n_text_words_tesseract ist **Pipeline-spezifisch**. Verschiedene Tesseract-Konfigurationen ergeben 5-15% Drift.

## Brücke 3: p23 BURUMUT 11×14 = 154 AS → **K (Konvention)**

**V10.4 sagt:** 11 Wörter × 14 AS = 154 AS, Akrostichon BNYZTSOYNKS.

**Drei Sub-Behauptungen:**

### 3.1 11 Faktor-Brüche (Z/N) auf p23 → **F (Faktum)**

**V1 Reverifikation bestätigt:** 22 Primfaktorzerlegungen auf p23, gruppiert als 11 Bruch-Paare (Z/N). Die Produkte sind Repunit-artige Zahlen (909090...9, 11111...1, 33333...3).

Beispiel: `2² × 17 × 19 × 55627057 × 7200332325968813 / 3² × 29 × 101 × 239 × 281 × 4649 × 909091 × 121499449`

**Klasse F**: Direkt aus p23-PNG ableitbar (Tesseract PSM=4 oder visuell mit Read-Tool verifiziert).

### 3.2 11 BURUMUT-Wörter à 14 AS → **K (Konvention)**

**Methode (V9 v2 Smart-Parser v2):**
1. Pro Bruch: Dezimal-Expansion berechnen
2. Periode extrahieren (z.B. 6-28 Ziffern)
3. **Dinome-to-Letters**: Periode in 2er-Pärchen teilen → PERIODIC[n][0] (H, He, Li, Be, ...)
4. **n_atoms = 14** (BURUMUT-spezifische Konvention!)
5. Resultat: 14-Buchstaben-Wort pro Bruch

**Problematik:** "n_atoms = 14" ist **kein Faktum aus p23**, sondern eine **Konvention** aus der BURUMUT-Hypothese. V9 v2 setzt das hartcodiert.

**V7 Tappeiner-Decoder:** Generiert 7 Kandidaten pro Bruch (7 Perioden × Atomnummer). V9 v2 wählt dann **"längster Kandidat"** (K-Konvention!). Aber:

- V7 enthält z.B. für Paar 1: `BURUMUTREFAMTU` (14 AS, BURUMUT-relevant) und `IYPKHIMHBCOMPA` (14 AS, beliebig). V9 v2 wählt `IYPKHIMHBCOMPA` (längster)! 
- Für Paar 9: V7 hat `NANPSSGNNRCSSSE` (15 AS, V9 v2 wählt diesen), aber V10.3 korrigiert zu `NAFERANSAHOTFE` (14 AS). **NAFERANSAHOTFE ist NICHT in V7 Kandidaten!**

**Woher kommen NAFERANSAHOTFE, KORENORBIZUMRO, KORENORBIZUMRO?**

→ Aus V8 Wikia-Alignment (Glyphe ↔ Wikia-Substring) oder V9 Wikia-Plaintext-Trigger. Beide sind **externe Quellen** (Wikia/Schmeh-Übersetzung).

**Klasse K + E**: BURUMUT-Wortliste ist **Konvention + Wikia-Korrekturen**, NICHT aus p23-PNGs direkt ableitbar.

### 3.3 Akrostichon BNYZTSOYNKS → **K + E**

**V10.4 sagt:** Akrostichon (erste Spalte der 11×14-Matrix) = BNYZTSOYNKS.

**Problem:** Die "erste Spalte" der BURUMUT-Matrix ist eine **Konvention der 11×14-Anordnung**. Aus p23-PNGs sieht man nur 11 Faktor-Brüche, keine 11×14-Matrix. Die Anordnung "Spalte 1" entsteht durch:

1. Dinome-to-Letters auf Periode des Bruchs
2. Auswahl von 14 Atomen
3. **Wahl der 1. Spalte** (= 1. Buchstabe jedes 14er-Worts)

**Klasse K + E**: Akrostichon ist **Konvention + Wikia-Trigger**. p<10⁻¹³ gegen random ist **statistisch signifikant** (V11/V12), aber die Auswahl der Spalte ist eine methodische Wahl.

## Brücke 4: Glyph→English (p1-p16) → **E (Extern wikia-getrieben)**

**V10.4 sagt:** 85-93% Match zu Wikia-Plaintext. Beispiel p01: G02→"TENGRI IS", G05→"THE SOURCE".

**Methode (V8 Wikia-Alignment):**
1. 17 Glyphen-Klassen aus V6 (ML-Clustering auf BBox-Crops)
2. **Wikia-Plaintext als Trainingsreferenz** (Schmehs Übersetzung, extern!)
3. Layout-Overlay: Glyphe ↔ Wikia-Substring (1 Glyph ≈ 7 lateinische Buchstaben)
4. ML-Modell mit V8-Alignment als Trainingsdaten
5. Decode: Glyphe → Konzept → Englisch

**Reverifikation:** V1 Reverifikation findet **1319 BBox-Cluster** auf p1-p16, aber **n_tengri_glyphs = 0** (V1 klassifiziert nicht semantisch). Die **Glyphen→Englisch-Zuordnung** ist **ohne Wikia nicht reproduzierbar**.

**Klasse E**: 'english_text' in V10.4 ist **wikia-getrieben**, nicht aus PNGs ableitbar.

## Brücke 5: p17 n_burumut_words_v9 = 0 → **F (Faktum, KORREKT)**

**V10.4 sagt:** p17 hat 0 BURUMUT-Wörter (V9 v2-Bug entfernt: hatte 11 = p23-Duplikate).
**V10.3 hatte:** p17=11 (Fehler, weil V9 v2 p23-Faktor-Brüche nach p17 projizierte).
**V10.4 Korrektur:** p17=0 (p17 hat visuell KEINE BURUMUT-Glyphen, nur 16 Faktor-Brüche).

**V1 Reverifikation bestätigt:** p17 hat nur Ziffern (0-9) und Faktor-Brüche, keine BURUMUT-Struktur. **p17 n_burumut = 0 ist FAKTUM-konform**.

**Klasse F**: Diese Korrektur ist **unabhängig von V10.4 reproduzierbar** und stellt eine **echte Verbesserung** dar.

## Brücke 6: Magic Cubes p5/p6 → **F (Faktum)**

**V10.4 sagt:** p5/p6 sind Magic-Cube-Seiten (3×3-Grid mit Summen 137/666).

**V1 Reverifikation:** 3×3-Raster visuell prüfbar. Summen (137, 666) sind **Konventionen der Magic-Cube-Hypothese**, aber die Existenz des 3×3-Grids ist Faktum.

**Klasse F + K**: 3×3-Grid = Faktum, Summen = Konvention.

## Brücke 7: n_formulas_bbox (p17-p23) = 119 → **P (Pipeline-abhängig)**

**V10.4 sagt:** 119 Formeln (BBox-Detection), z.B. p17=16, p20=43.

**Methode:** BBox-Detection auf p17-p23 mit Heuristik "Bruchstruktur" (Zähler, Bruchstrich, Nenner).

**Reverifikation:** BBox-Detection ist **direkt reproduzierbar** (OpenCV findContours), aber die Klassifikation als "Formel" hängt von der Heuristik ab. Verschiedene Pipelines (V9 v2, V10.4) können 5-10% Drift haben.

**Klasse P**: Faktum (BBox existiert) + Konvention (was ist eine "Formel"?).

## Brücke 8: n_drawings_bbox = 1 (nur p23) → **F (Faktum)**

**V10.4 sagt:** 1 Zeichnung auf p23 (vermutlich die Cytosin/Thymin-Strukturformel oben).

**V1 Reverifikation bestätigt:** p23 hat **2 chemische Strukturformeln** (Cytosin + Thymin), aber V10.4 zählt 1 (möglicherweise zählt nur 1 als "Drawing", die andere als "Formula"). Definitionssache.

**Klasse F + P**: Faktum (Strukturformel existiert) + Pipeline (was zählt als "Drawing"?).

## Zusammenfassung: Welche V10.4-Werte sind **Faktum**, welche **Konvention/Extern**?

| Claim | V10.4 Wert | Klasse | Reverifikation? |
|-------|-----------|--------|-----------------|
| n_glyphs = 1013 | 1013 | K + P | Mit V9 v2-Pipeline: ja. Sonst: 997 (V4) |
| n_text_words_tesseract = 3677 | 3677 | P | Mit identischer Tesseract-Konfig: ja |
| p23 hat 11 Faktor-Brüche | 11 | F | Ja, Tesseract PSM=4 oder Read-Tool |
| p23 BURUMUT-Wortliste (11×14) | 11 Wörter | K + E | NEIN ohne Wikia |
| p23 Akrostichon BNYZTSOYNKS | 11 Buchstaben | K + E | NEIN ohne Wikia |
| Glyph→English (p1-p16) | 85-93% Match | E | NEIN ohne Wikia |
| p17 n_burumut = 0 | 0 | F | Ja, p17 hat visuell keine BURUMUT-Struktur |
| p17 n_formulas = 16 | 16 | P | BBox-Detection: ja, Formel-Definition: pipeline-abhängig |
| p5/p6 Magic Cubes | 2 Seiten | F + K | 3×3-Grid: ja, Summen: Konvention |
| p23 n_drawings = 1 | 1 | F + P | Strukturformel: ja, Zählung: pipeline-abhängig |

## Konsequenz für die Reverifikation

**Was V10.4 zu Recht behauptet (aus PNGs reproduzierbar):**
1. p23 hat 11 Faktor-Brüche (22 Primfaktorzerlegungen, 11 Paare)
2. p17 hat 16 Faktor-Brüche
3. p17 hat KEINE BURUMUT-Struktur (Korrektur V9 v2 → V10.4)
4. p5/p6 haben 3×3-Grid-Struktur (Magic Cubes)
5. p23 hat chemische Strukturformeln (Cytosin, Thymin)
6. Alle 23 Seiten haben lateinischen Text (Tesseract-OCR möglich)

**Was V10.4 als High-Level-Interpretation liefert (Konvention + Wikia):**
1. 1013 Glyphen (V9 v2-Konvention, nicht 997 wie V4)
2. BURUMUT-Wortliste (11×14, V9 v2 "längster Kandidat" + Wikia-Korrekturen)
3. Akrostichon BNYZTSOYNKS (Konvention der 11×14-Anordnung)
4. Glyph→English-Mapping (wikia-getrieben)
5. Magic-Cube-Summen 137/666 (Konvention der Magic-Cube-Hypothese)

**Was V10.4 **nicht** aus PNGs reproduzierbar macht:**
1. Die exakte BURUMUT-Wortliste (NAFERANSAHOTFE ist nicht in V7, kommt aus Wikia)
2. Die Glyph→English-Zuordnung (V8 Wikia-Alignment als Trainingsreferenz)
3. Die 16 zusätzlichen Glyphen gegenüber V4 (V9 v2-Re-Clustering)

## Apophenia-Schutz

- **Monte-Carlo-Test** (p<10⁻¹³ für Akrostichon): methodisch sauber, aber **nur gültig, wenn die 11×14-Anordnung Faktum wäre** — und das ist sie nicht.
- **CitMind-Veto:** Wenn die "Faktoren" selbst Wikia-Plaintext als Trigger nutzen, ist die Akrostichon-Signifikanz **zirkulär**.
- **Konsequenz:** V10.4 ist methodisch wertvoll als **High-Level-Interpretations-Layer**, aber **nicht** als Faktum-Schicht. V1 (Reverifikation) zeigt die **Fakten** (Brüche, BBoxes, Latein), V2 (Brücke) dokumentiert die **Methodik-Reproduzierbarkeit** der High-Level-Interpretationen.

## V1-V10.4-Status-Tabelle

| V10.4-Claim | V1 Reverifikation | Status |
|-------------|-------------------|--------|
| 11 BURUMUT-Wörter (p23) | 11 algebraische Faktor-Paare | F (Faktum), aber WORTLISTE ist K+E |
| 154 AS BURUMUT-Peptid | 154 = 11×14 algebraisch | F (Anzahl), Sequenz ist K+E |
| p17 n_burumut = 0 | 0 (keine BURUMUT-Struktur) | F (Faktum) ✓ |
| 1013 Glyphen | 1319 BBox-Cluster (V1 hat andere Granularität) | P (Pipeline) |
| 3677 lateinische Wörter | 648 lateinische Wörter (V1, engerer Tesseract-PSM) | P (Pipeline) |
| Glyph→English 85-93% | Nicht reproduzierbar ohne Wikia | E (Extern) |

## Empfehlung

1. **V1 als Faktum-Schicht** akzeptieren: 11 Faktor-Brüche, BBox-Counts, Latein-OCR, Magic-Cube-Existenz.
2. **V10.4 als Interpretations-Layer** kennzeichnen: BURUMUT-Wortliste, Glyph→English, Akrostichon.
3. **V2-Brücke** (diese Reverifikation) zeigt, **wo** die High-Level-Interpretationen Wikia-Input nutzen.
4. **V3+**: Algebraische BURUMUT-Matrix **ohne** Wikia-Trigger (nur Faktor-Brüche → Wortliste deterministisch aus Brüchen ableiten, nicht aus V7 Kandidaten).

---

**Status:** V1 Reverifikation abgeschlossen. V2 Brücke dokumentiert. V3 vorbereitet (algebraische Alternative).
**Apophenia-Veto-Status:** CitMind-geprüft. V10.4 = Stufe 7 (Interpretations-Layer), V1 = Stufe 1 (Faktum-Schicht).
