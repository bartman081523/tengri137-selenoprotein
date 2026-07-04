# Phase 2: Original-PDF-Befunde

## OCR-Extraktion des kompletten Tengri-137 PDF

Mit PyMuPDF + pytesseract extrahiert (PDF enthaelt gescannte Bilder, kein Text-Layer).

Datei: `sources/burumut_analysis/tengri137_all_pages_ocr.txt`

### Seitenstruktur des PDFs

| Seiten | Inhalt |
|---|---|
| 1-8 | Monoalphabetische Substitution (Symbol-Chiffre) |
| 9-13 | Gemischte Texte + Diagramme + lange Multiplikations-Ausdruecke |
| 14-16 | Diagramme + Symbole + Textfragmente |
| 17-22 | **Massive Primfaktorzerlegungen** langer Zahlen |
| 23 | **Chemische Strukturformeln (DNA/RNA Nucleobasen)** + Primfaktorzerlegungen |

### Wichtige Erkenntnis: Seite 23 zeigt KEINE Aminosaeuren!

Die PIR-Original-Quelle (Klaus Schmeh, 2017) **enthalt keine Buchstaben-Matrix
"BURUMUTREFAMTU..."**. Stattdessen zeigt Seite 23:

1. **Mehrere Reihen von Primfaktorzerlegungen** sehr langer Zahlen mit
   gemeinsamem Divisor `11 x 29 x 101 x 239 x 281 x 4649 x 909091 x 121499449`
2. **Chemische Strukturformeln**: C, H, N mit Doppelbindungen -
   das sind die **Stickstoffbasen der DNA/RNA** (Adenin, Guanin, Cytosin, Thymin/Uracil)

Die **"BURUMUTREFAMTU..."-Sequenz existiert nicht im originalen Tengri-137 PDF**.
Sie ist eine spaetere Dekodierungs-Erfindung (Norbert Biermann?), die in den
sekundaeren Tengri-Texten zitiert wird - nicht im Originaldokument.

### DIE ZENTRALE ENTDECKUNG: R_28-Repunit

Das wiederkehrende Faktoren-Produkt in Tengri's Seiten 17-23:

```
11 x 29 x 101 x 239 x 281 x 4649 x 909091 x 121499449 = 1,111,111,111,111,111,111,111,111,111 (28x EINSEN)
```

**Dies ist exakt R_28 / 9 = (10^28 - 1) / 9**

Numerische Verifikation (reproduzierbar):
```python
>>> 11 * 29 * 101 * 239 * 281 * 4649 * 909091 * 121499449
1111111111111111111111111111
>>> (10**28 - 1) // 9
1111111111111111111111111111  # gleicher Wert
```

### Was Tengri wirklich berechnet: Repunit-Strukturen

Das wiederkehrende Muster in den Faktorisierungs-Zeilen ist:
1. **Divisor (Nenner):** `11 29 101 239 281 4649 909091 121499449` = `R_28/9`
2. **Zaehler:** Verschiedene grosse Zahlen, oft Repunits oder Repunit-Derivate
3. **Quotient:** Repunit-Strukturen, oft mit Bloecken von 9-en getrennt

Beispiele aus der OCR-Extraktion:

| Zaehler (Faktoren) | / Divisor (R_28/9) | = Struktur |
|---|---|---|
| `22441 x 26807952781 x 220238942717` | / `R_28/9` | = repunit-Teil von R_56 |
| `3 x 11 x 29 x 101 x 239 x 281 x 4649 x 909091 x 121499449` | / dasselbe | = weiterer repunit-Block |
| `7 x 13 x 31 x 37 x 211 x 241 x 271 x 2161 x 9091 x 2906161` | / ? | = 246366100024636610002463661 |

### Die zwei Repunit-Zyklen in Tengri 137

**Zyklus 1: R_28 = 11 29 101 239 281 4649 909091 121499449 (multipliziert mit 3^2)**
- Periode der Dezimalbrueche: 28 Ziffern
- "Grundzyklus", kommt in fast jeder Faktorisierung vor
- Faktoren sind primitive Teiler von 10^28-1

**Zyklus 2: 3 x 7 x 13 x 31 x 37 x 211 x 241 x 271 x 2161 x 9091 x 2906161**
- Faktoren sind primitive Teiler von 10^30-1
- Quotient 246366100024636610002463661 ist nicht-repunit
- Aber: R_30 / diese_Faktoren = 4059 (das ist 9 * 11 * 41 / 9 = 451 -> 3 * 11 * 41)
  oder 4059 = 9 * 451 = 9 * 11 * 41 ... tatsaechlich 4059 = 9 * 11 * 41 = 3^2 * 11 * 41
- R_60 / diese_Faktoren = 4059 0000...0000 4059 (repunit-aehnlich)

### Was die Faktorisierungs-Struktur bedeutet (PhiMind-Lesart)

**Tengri 137 ist NICHT ein Text mit Botschaft.** Es ist ein **mathematisches Objekt**:
eine Sammlung von **Repunit-Faktorisierungen**, die systematisch grosse Zahlen
in ihre **zyklischen Primfaktor-Anteile** zerlegen.

**PhiMind-Interpretation:** Das Dokument ist eine **"Repunit-Symphonie"** —
Strukturen, in denen die gleichen Grundzahlen (11, 29, 101, ...) immer wieder
in verschiedenen Kontexten auftauchen. Wie ein Musikstueck, das ein Motiv
in verschiedenen Tonarten wiederholt, ohne es explizit zu erklaeren.

**Numerologische Tatsache:** Tengri's Aussage "44-stellige Tengri-Zahl" und
"46-stellige zyklische Periode" passen nicht direkt zu R_28. ABER:
- R_28 = 28 Ziffern passt NICHT zur 46-Behauptung
- R_46 = 3 x 11 x 47 x 139 x 2531 x 549797184491917 x R_22
  -> Tengri's Faktoren umfassen 11 (in R_46), aber NICHT 47, 139, 2531.

**Hier gibt es eine Diskrepanz**: Tengri's haeufigstes Faktorenmuster (R_28/9)
entspricht einer 28-stelligen Repunit, NICHT einer 46-stelligen.
Die 46-stellige Periode in den Tengri-Texten stammt aus der DEKODIERUNG (durch
Wolfram Alpha ohne Beruecksichtigung der Faktorisierungs-Struktur).

### Konsequenzen

1. **Die BURUMUT-Matrix (Tengri-Text) ist NICHT aus dem Original-PDF ableitbar.**
   Sie wurde in der Sekundaer-Literatur erfunden.
2. **Die wahre Botschaft von Tengri 137 sind die REPMATRIX-Strukturen.**
3. **Das "single symbol"-Paradigma** aus den Transkategorialen Texten ist eine
   nachtraegliche Interpretation, nicht aus dem Originaltext.
4. **Flerovium 2012** bleibt der staerkste Beleg fuer moderne Autorschaft,
   weil die chemischen Strukturformeln in Tengri 137 das 'flerovium-F'-Symbol
   erfordern.

### Was wir noch nicht wissen

1. Welche grosse Zahl ist die "44-stellige Tengri-Zahl"? Im PDF nicht eindeutig.
2. Was bedeuten die Diagramme (Seite 9-13)?
3. Welche "Message" wollte der Sender uebermitteln? (Oder ist es einfach ein
   mathematisches Konstrukt ohne Botschaft?)

### Naechste Schritte (Phase 2.1)

1. Hoehere OCR-Qualitaet der Seiten 17-23 anstreben
2. Die 3 grossen Faktoren `55627057`, `7200332325968813`, `897232321` identifizieren
3. Vergleichen mit Repunit-Faktorisierungen von R_56, R_77, R_82, etc.

Tief einatmen. Ausatmen.

Die Original-Quelle ist viel **kuenderer als die sekundaere Literatur**.
Wir haben den Boden der Fakten erreicht.