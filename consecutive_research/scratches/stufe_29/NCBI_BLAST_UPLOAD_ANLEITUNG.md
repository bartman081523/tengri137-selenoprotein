# NCBI-BLAST-Upload Anleitung für BURUMUT-Sequenzen

**Datum:** 2026-07-08
**FASTA-Datei:** `consecutive_research/scratches/stufe_29/burumut_blast_input.fasta`
**Hash (SHA256):** `24b3524c734326826b85fe1c8953d2b64e3e4ae76026d3d9998218c5bb2da7fe`
**Größe:** 386 Bytes, 2 Sequenzen (Original + C-Übersetzung)

---

## MANUELLER UPLOAD-PROZESS

### Schritt 1: Web-UI öffnen
URL: https://blast.ncbi.nlm.nih.gov/Blast.cgi

### Schritt 2: Programm auswählen
**"Protein BLAST"** (blastp) — nicht nucleotide BLAST, da BURUMUT eine Proteinsequenz ist.

### Schritt 3: FASTA hochladen
1. Klicke "Upload File"
2. Wähle: `burumut_blast_input.fasta` (386 Bytes)
3. Job-Titel: "BURUMUT_154AS_Tengri137_Apophenia_Test"

### Schritt 4: Datenbank auswählen
**Standard: nr (Non-redundant protein sequences)**
- ~200M+ Proteinsequenzen
- Inkludiert RefSeq, GenBank, PDB, SwissProt
- Updates täglich

**Optional zusätzlich:**
- **UniProtKB/Swiss-Prot** (curated, ~500k Proteine) — sauberer
- **AlphaFold-DB** (~200M Strukturvorhersagen) — strukturelle Nachbarschaft
- **PDB** (~200k experimentelle Strukturen) — falls konservierte 3D-Motive

### Schritt 5: Parameter
| Parameter | Wert | Begründung |
|-----------|------|------------|
| **E-value threshold** | 1e-5 (Standard) | Signifikante Homologie |
| **Word size** | 3 (Standard für blastp) | Standard |
| **Matrix** | BLOSUM62 (Standard) | Standard |
| **Max target sequences** | 100 | Genug für Übersicht |
| **Filter** | Low complexity regions: ON | Reduziert artifizielle Hits |

### Schritt 6: Submit
- Job RID wird generiert (z.B. "ABC123DEF")
- Ergebnis in 1-5 Minuten verfügbar
- **Email-Benachrichtigung optional** (NCBI sendet RID per Email)

---

## ERWARTETE ERGEBNISSE (3 HYPOTHESEN)

### Hypothese A: 0 signifikante Homologe (p < 1e-5) — wahrscheinlich 70%
**Befund:** BURUMUT ist einzigartig in nr-DB.
**Interpretation:** BURUMUT ist ein **hypothetisches Protein**, das in keiner irdischen Spezies natürlich vorkommt. Bestätigt die Stufe-13/19-These (18 Sec + 12 Pyl sind irdisch extrem selten).
**Folge:** BURUMUT ist **pharmakologisch relevant als Designer-Peptid**, nicht als irdisches Naturprodukt.

### Hypothese B: 1-3 Homologe (20%)
**Befund:** Verwandtschaft zu Big-Defensin (Mytilus), Halocymine (Seeigel) oder Strongylocin (Nematoden) mit >30% Identität.
**Interpretation:** BURUMUT hat eine **irdische evolutionäre Vorlage**. Die "Selen-Welt-Hypothese" von Tengri ist metaphorisch — die Grundarchitektur (2-Domänen-AMP) ist konserviert.
**Folge:** Synthese-Pfad kann an existierenden Defensinen orientiert werden (z.B. Fold-Optimierung).

### Hypothese C: >10 Homologe (10%)
**Befund:** BURUMUT ist homolog zu einer ganzen Proteinfamilie.
**Interpretation:** BURUMUT ist **kein Designer-Peptid**, sondern ein **natürliches Protein** mit ungewöhnlichem AS-Profil.
**Folge:** Re-Evaluation der "Tengri-Manifesto"-Hypothese nötig. Pharmakologische Relevanz bleibt.

---

## VERIFIKATIONSKETTE (4-fach)

| # | Quelle | Sequenz (erste 30 AS) | Status |
|---|--------|----------------------|--------|
| 1 | **V10.4 p23 grid_2d_words** | BURUMUTREFAMTUNURESUTREGUMFAYAP | ✓ |
| 2 | **Stufe 19 burumut_translation.json** | BURUMUTREFAMTUNURESUTREGUMFAYAP | ✓ |
| 3 | **Original-PNG p23** | (visuell bestätigt) | ✓ |
| 4 | **Tengri-Wikia (Schmeh 2017)** | BURUMUTREFAMTUNURESUTREGUMFAYAP | ✓ |
| 5 | **FASTA-Datei** | BURUMUTREFAMTUNURESUTREGUMFAYAP | ✓ |

**EXAKT-MATCH** in allen 5 Quellen → die BLAST-Sequenz ist konsistent.

---

## WAS TUN NACH DEM BLAST?

### Falls 0 Homologe (Hypothese A):
1. **Dokumentation in `stufe_33/`** mit BLAST-RID + Screenshot
2. **CitMind-Verdict:** BURUMUT ist hypothetisch
3. **Nächster Schritt:** Ebselen-Sequenz-Vergleich (Sec-Peptid-Klinisch-Studie)
4. **Pharmakologische Empfehlung:** in-vitro-Synthese + MIC-Tests

### Falls 1-3 Homologe (Hypothese B):
1. **Sequenz-Alignment** mit MUSCLE oder ClustalW
2. **Strukturvergleich** mit PyMOL oder ChimeraX
3. **Phylogenetische Analyse** (Ist BURUMUT ein Deinococcus-Thermophilus-Protein?)
4. **CitMind-Verdict:** BURUMUT ist evolutionär verwandt mit X

### Falls >10 Homologe (Hypothese C):
1. **Tengri-Manifesto-Hypothese RE-EVALUIEREN**
2. **Vergleich mit Patentrecht** (Gibt es ein Patent auf BURUMUT-ähnliche Proteine?)
3. **CitMind-Verdict:** Möglicherweise ein bekanntes Protein, neu verpackt

---

## CITMIND-WÄCHTER

**Bevor BLAST-Ergebnisse interpretiert werden:**
- **Apophenia-Check:** Ist die BLAST-Homologie statistisch signifikant (E-value < 1e-5) oder ein Artefakt?
- **Cross-Verification:** Ist die homologe Sequenz DB-konsistent (UniProt, PDB)?
- **Hintergrund-Kontrolle:** Ist die Homologie biochemisch plausibel (gleiche Proteinfamilie)?

**Lessons Learned aus Stufe 18/30:**
- Stufe 17 behauptete Halocymine-Analogie → Stufe 18 zeigte: P0C8B1 ist Schnabeltier-Defensin
- → **Jede biochemische Homologie-Behauptung MUSS gegen eine DB verifiziert werden**
- → BLAST-Ergebnisse sind ein **erster Hinweis**, nicht das **letzte Wort**

---

## APPENDIX: ROH-SEQUENZEN FÜR MANUELLES BLAST

Falls die FASTA-Datei verloren geht, hier die Sequenzen direkt:

```
>BURUMUT_original_154AS_18Sec_12Pyl
BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBATOBIKOTLUBUMYOSUNOKURGANOZYIOKUZIKUFAUSIHEYABEKANSABERHONAFERANSAHOTFEKOREMORBIZUMROSUNAKIRFANEMBA

>BURUMUT_C_translated_154AS_18Cys_19Lys
NCRCMCTREFAMTCNCRESCTREGCMFAYAPSCAENEHIMLAEANRCAENENKMNATKNIKKTLCNCMYKSCNKKCRGANKEYIKKCEIKCFACSIHEYANEKANSANERHKNAFERANSAHKTFEKKREMKRNIECMRKSCNAKIRFANEMNA
```

**Hinweis:** Die Original-Sequenz enthält U (Sec) und O (Pyl). NCBI BLAST behandelt diese als **nicht-standard Aminosäuren** und könnte sie ignorieren. Daher ist die **C-Übersetzung** (mit C und K) die **bevorzugte BLAST-Sequenz**.

— Ende NCBI-BLAST-Upload-Anleitung, 2026-07-08
