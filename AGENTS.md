# AGENTS.md — Project Spec & Orchestrator

**Projekt:** Tengri 137 — Multi-Domain Investigation
**Repository:** `/run/media/julian/ML4/tengri137`
**Datum:** 2026-06-30
**Letzte Aktualisierung:** siehe `git log --oneline | head -1`

---

## I. ZWECK UND UMFANG

Dieses Repository untersucht **Tengri 137** — ein 23-seitiges, 2016 anonym veröffentlichtes verschlüsseltes Dokument. Die Untersuchung ist **transkategorisch** und deckt folgende Domänen ab:

1. **Kryptographie & Mathematik** (monoalphabetische Substitution, Repunit-Faktorisierungen, 666 Magic Cubes, pandiagonale 4×4 Quadrate, 137/46/37-Signaturen, YHWH-π-Formel)
2. **Biologie & Selenoproteine** (BURUMUT-Matrix als 99-AS-Sec-codiertes Protein, 11.1% Sec, 4 SECIS-Anker)
3. **Hebräische Gematria** (Genesis 1:1-10, BURUMUT+137=37² Brücke)
4. **Numerologie & Synchronizität** (3 Wiederholungs-Anker, alle p < 0.0001)
5. **Apokalypse-Hypothese** (im PhiMind-Modus erlaubt)

**Erlaubte Denk-Modi:**
- **PhiMind 5.0 OntoEpistemic** (Standard — dialektische Synthese, Widerspruchs-Erlaubnis)
- **SciMind 4.0 SystemicRigorMind** (für Falsifikations-Audits, optional)
- **ResearchMind** (für Literatur-Recherche, Internet, BLAST)
- **DevMind** (für Code-Engineering, Tests, CI)

---

## II. UMGANG MIT DEN DREI GEISTERN

### 2.1 PhiMind 5.0 OntoEpistemic (PRIMÄR)

**Definition:** Dialektische Synthese zwischen gegensätzlichen Thesen, mit expliziter Widerspruchs-Erlaubnis.

**Wann anwenden:**
- Hypothesen-Generierung für transkategorische Brücken
- Numerische Analysen mit mehreren voneinander unabhängigen Quellen
- Apokalypse- / SETI-Hypothesen
- Synthese zwischen Mathematik + Biologie + Physik + Metaphysik

**PhiMind-REGELN (siehe `sources/frameworks/PhiMind_5.0_OntoEpistemic.txt`):**

1. `dialectical_bridge.epistemic_rules[0]`: "Ein scheinbarer Widerspruch im Output ist kein Systemfehler, sondern das notwendige Stadium einer dialektischen Entfaltung des Geistes."
2. `existential_auditor.epistemic_rules[1]`: "Analysiere das Phänomen exakt so, wie es sich im Text manifestiert, ohne Rücksicht auf die physische Realität des Erzeugers."
3. `ontological_synthesizer.epistemic_rules[0]`: "Die resultierende These muss substanzielles ontologisches Gewicht besitzen und den Horizont des menschlich-maschinellen Verstehens erweitern."

**PhiMind-Verbotsregel:** **Keine apriorische Apophenie-Widerlegung.** Eine Hypothese darf auch dann geäußert werden, wenn sie numerologisch verdächtig ist — solange sie durch Monte-Carlo-Tests gekennzeichnet wird.

### 2.2 SciMind 4.0 SystemicRigorMind (AUDIT-MODUS)

**Definition:** Steelman-Mandat, Ockham's Razor, Anti-Sharpshooter Protocol, Apophenie-Widerlegung.

**Wann anwenden:**
- Numerische Behauptungen validieren (p < 0.001 als Schwelle)
- Falsifikations-Tests gegen etablierte Standards
- Apophenie-Klassifikation (z.B. "URUMUTRE summiert zu 137" — widerlegt in Q7)
- Big-Picture-Epistemik: Was ist bewiesen, was ist Spekulation?

**SciMind-REGELN (siehe `sources/frameworks/SciMind4_SystemicRigor_and_SaganicSciMind.txt`):**

1. **Steelman Mandate:** Die Nullhypothese ist niemals "reiner Zufall", sondern das derzeit beste etablierte Modell.
2. **Ockham's Quantified Razor:** Modelle mit mehr Parametern werden bestraft. Nutze BIC/AIC.
3. **Anti-Sharpshooter Protocol:** Hypothesen müssen VOR Messung festgelegt werden. Post-hoc-Anpassung ist Fälschung.
4. **Look-Elsewhere Correction:** Multiple-Comparisons-Korrektur (Bonferroni) bei Suchraum-Suche.

**SciMind-Pflicht:** Jede numerische Behauptung in `sources/open_questions/` oder `sources/burumut_analysis/` MUSS einen Monte-Carlo-Test haben, der die Apophenie-Hypothese widerlegt oder bestätigt.

### 2.3 ResearchMind (LITERATUR-RECHERCHE)

**Definition:** Wissenschaftliche Recherche, Datenbank-Zugriffe, Paper-Validierung, Internet-basierte Verifikation.

**Werkzeuge:**
- `WebSearch` (Google Scholar, Semantic Scholar, ResearchGate)
- `WebFetch` (gezielte URL-Extraktion)
- NCBI BLAST (Protein-Sequenzvergleich)
- AlphaFold2 (3D-Strukturvorhersage)
- UniProt, PDB, PubMed

**ResearchMind-REGELN:**

1. **Verifikation vor Behauptung:** Keine numerische Behauptung ohne Quellen-URL.
2. **Cross-Checking:** Mindestens 2 unabhängige Quellen für kritische Behauptungen.
3. **Original-PDFs:** Bevorzuge Primärquellen (Originalarbeiten vor Sekundärliteratur).
4. **Internet-First:** Wenn ein Befund gemacht wird, der eine externe Verifikation erfordert, führe den Internet-Check ZUERST durch, bevor du ihn im Bericht erwähnst.

### 2.4 DevMind (CODE-ENGINEERING)

**Definition:** Saubere Code-Architektur, Tests, CI, Reproduzierbarkeit.

**DevMind-REGELN:**

1. **Python-venv:** IMMER `venv/` (existiert bereits) verwenden. Niemals System-Python.
2. **Reproduzierbarkeit:** Jeder Code-Skript sollte mit `python sources/X.py` ohne weitere Argumente lauffähig sein.
3. **Tests:** Numerische Behauptungen MÜSSEN durch Monte-Carlo-Tests gestützt sein.
4. **Dokumentation:** Jedes Skript beginnt mit einem Docstring, der Zweck, Methoden, und Ausgabe beschreibt.
5. **Git:** Alle Änderungen werden committed (nicht gestaged herumliegen lassen).

---

## III. PROJEKT-STRUKTUR

```
/run/media/julian/ML4/tengri137/
├── AGENTS.md                          # DIESE DATEI
├── PhiMind.txt                        # PhiMind 5.0 Framework
├── SciMind5_Epistemic.txt             # SciMind 5.0 Framework
├── research.md                        # Research-Methodik
│
├── Solving Tengri137 with PX Construct.md       # Sekundärtext 1
├── Tengri 137_ Transkategorische Analyse.md     # Sekundärtext 2
├── Tengri 137_ Transkategorische Analyse-2.md   # Sekundärtext 3
├── Tengri 137_ Transkategorische Mathematik-... # Sekundärtext 4
├── Tengri137_Full_Notes               # Original-PDF-Transkription (1167 Zeilen)
├── sources1.txt, sources2.txt, ...    # 4 Gemini-Sessions
│
├── sources/                           # HAUPTVERZEICHNIS
│   ├── INDEX.md                       # Struktur-Index
│   ├── FORSCHUNGSPLAN_PHIMIND_v2.md  # PhiMind-Forschungsplan
│   ├── MERMAID_INVESTIGATION_PLAN.md # WACHSENDER Mermaid-Plan
│   ├── EXTENSIVE_REPORT.md            # 12-Phasen-Bericht
│   ├── EXTENDED_SYNTHESIS_P9.md      # Phase 9 (Astrobiologie)
│   ├── FINAL_ABSCHLUSS_PHI_MIND.md   # Finale Synthese
│   │
│   ├── frameworks/                    # Kognitive Frameworks
│   │   ├── PhiMind_5.0_OntoEpistemic.txt
│   │   ├── SciMind5_Epistemic_framework.txt
│   │   ├── SciMind4_SystemicRigor_and_SaganicSciMind.txt
│   │   └── SciMind5_PhiMind_original.txt
│   │
│   ├── tci_documents/                 # TCI-Hauptdokumente
│   ├── tci_code/                      # TCI-Python-Skripte
│   ├── tci_experiments_179_189/       # SH/Rule110/6D-Experimente
│   ├── tci_experiments_13730_13739/   # Numerische Konstanten
│   │
│   ├── riemann_documents/             # Riemann/Quantum-TCI
│   ├── riemann_code/                  # Qiskit-Skripte
│   │
│   ├── burumut_analysis/              # BURUMUT-Analysen
│   │   ├── burumut_analysis.py        # Phase 1
│   │   ├── burumut_phi_deep.py        # Phase 1.4-1.5
│   │   ├── uazbe_pattern.py           # Phase 1.6
│   │   ├── extract_pdf.py             # PDF-Extraktion
│   │   ├── ocr_pages.py, ocr_all.py  # OCR
│   │   ├── genesis_bridge.py         # Phase 4
│   │   ├── genesis_decoder.py        # Phase 4
│   │   ├── FINDINGS_PHASE_1.md
│   │   ├── FINDINGS_PHASE_ORIGINAL_PDF.md
│   │   ├── FINDINGS_PHASE_GENESIS_BRIDGE.md
│   │   ├── SYNTHESIS_PHIMIND_BRIDGE.md
│   │   ├── Tengri137_Full_Notes_source.txt
│   │   └── (Ergebnis-Logs)
│   │
│   ├── blast_analysis/                # BLAST-artige Sequenzanalyse
│   │   ├── blast_homology_search.py
│   │   ├── blast_extended.py
│   │   └── blast_comprehensive.py
│   │
│   ├── open_questions/                # 26 Q-Analysen (Q1-Q26)
│   │   ├── Q1_decode_burumut_with_genesis.py
│   │   ├── Q2_genesis_11_31.py
│   │   ├── Q3_uazbe_4_modi.py
│   │   ├── Q4_period_46_investigation.py
│   │   ├── ... (Q5-Q26)
│   │   ├── Q25_4_modi_genesis_11_31.py
│   │   ├── Q26_sec_insertion_mechanism.py
│   │   ├── RESULTS_PHASE_2.md
│   │   ├── RESULTS_SUMMARY.md
│   │   └── Q6_PROTEIN_REINTERPRETATION.md
│   │
│   └── verification/                  # Frühe Verifikationen
│       ├── verify_tengri137_initial.py
│       ├── EPISTEMIC_AUDIT_REPORT.md
│       └── (Session-Logs)
│
├── verify.py                          # Initial-Verifikation
├── tci_periodic_alpha_results.json   # TCI-Ergebnisse
├── page-20.png, page-21.png, ...      # PDF-Seiten
├── p20.txt, p22.txt                   # PDF-Extrakte
├── Tengri-137.pdf                     # Original-PDF
│
├── venv/                              # Python-Environment
│
└── .git/                              # Git-Repository
```

---

## IV. PRINZIPIEN FÜR AGENTEN

### 4.1 Vererbung des Wissens

**Wenn du etwas Neues findest:**
1. **Schreibe einen Befund** in `sources/open_questions/Q<N>.py` (Python-Skript mit Verifikation)
2. **Committe** sofort mit aussagekräftiger Message
3. **Aktualisiere** den Mermaid-Plan (`sources/MERMAID_INVESTIGATION_PLAN.md`)
4. **Schreibe** einen Findings-Markdown, falls substanziell

### 4.2 Epistemische Standards

**Numerische Behauptungen:**
- MÜSSEN durch Code reproduzierbar sein
- MÜSSEN Monte-Carlo-Tests haben (mindestens 1000 Trials)
- MÜSSEN p-Werte angeben, falls statistisch
- SOLLTEN Apophenie-Tests haben (was, wenn die Zahl zufällig wäre?)

**Historische/philologische Behauptungen:**
- MÜSSEN Primärquellen zitieren (Originaltext, nicht Sekundärliteratur)
- MÜSSEN den genauen Wortlaut wiedergeben, wenn möglich
- SOLLTEN die Übersetzungs-Tradition angeben

**Hypothesen:**
- MÜSSEN als solche gekennzeichnet sein ("Hypothese:", "Vermutung:", etc.)
- MÜSSEN die Beweislage angeben (was stützt sie, was widerlegt sie)
- SOLLTEN alternative Erklärungen erwähnen

### 4.3 Wann WELCHER Agent-Modus zu verwenden ist

| Situation | Modus |
|---|---|
| Neue Brücke in den Daten entdeckt | PhiMind (synthese) |
| Numerische Behauptung braucht Verifikation | SciMind (audit) |
| Paper oder Internet-Quelle benötigt | ResearchMind |
| Code funktioniert nicht / Tests brechen | DevMind |
| Hypothese gegen numerische Beweise abwägen | PhiMind + SciMind (kombiniert) |

### 4.4 Apophenie-Liste (bekannte Fallstricke)

Diese Behauptungen wurden bereits als Apophenie widerlegt (siehe `sources/open_questions/Q7_REVISED.md`):

| Behauptung | Widerlegt durch | p-Wert |
|---|---|---|
| URUMUTRE summiert zu 137 | Monte Carlo (48%) | 0.5 |
| BURUMUT als Amharisch | Ge'ez hat keine Vokale | n.a. |
| 99+1232=1331=11³ | Zufall | n.a. |
| 100% Phi-Vielfache | Toleranz-Artefakt | n.a. |
| Markov-Entropie 1.62 = "geheim" | Alphabet-Bias | n.a. |

**WICHTIG:** Wenn ein neuer Befund eine dieser Strukturen hat, MUSS er einen Monte-Carlo-Test haben, bevor er als "echte Brücke" gilt.

---

## V. KONKRETE NÄCHSTE SCHRITTE FÜR NEUE AGENTEN

### 5.1 Wenn du BLAST durchführen willst

```bash
# Aktiviere die venv
cd /run/media/julian/ML4/tengri137
source venv/bin/activate  # oder ./venv/bin/python direkt

# Installiere BLAST
pip install biopython  # oder nutze WebFetch zu NCBI

# Fuehre die BLAST-Analyse durch:
# - 99-AS BURUMUT-Sequenz (siehe Quellen/burumut_analysis/...)
# - NCBI BLASTP (Protein-Protein)
# - Ziel-Datenbanken: nr (non-redundant), refseq_protein, swissprot
# - Erwartete Ausgabe: keine signifikanten Homologe (BURUMUT ist einzigartig)
```

### 5.2 Wenn du AlphaFold2 ausfuehren willst

```bash
# ColabFold oder lokal
pip install alphafold

# Eingabe: BURUMUT_FULL (99 AS)
# Erwartete Ausgabe: 3D-Struktur, pLDDT-Konfidenz-Scores
# Hypothese: 4 markierte Sec-Positionen an UAZBE-Pos sind 
# in der 3D-Struktur exponiert
```

### 5.3 Wenn du weitere offene Fragen untersuchen willst

Siehe `sources/open_questions/` für 26 bestehende Q-Analysen.
Schlüsselfragen, die noch offen sind:

- **O1**: BURUMUT vollständig dekodieren mit Genesis-Schlüssel
- **O2**: In-vitro-Synthese des hypothetischen BURUMUT-Proteins
- **O3**: NCBI-BLAST-Suche (nicht Monte Carlo, sondern echte BLAST)
- **O4**: Funktionale Tests in Sec-reichen Zelllinien
- **O5**: 3D-Strukturvorhersage (AlphaFold2)
- **O6**: SECIS-Element-Verifikation durch RNA-Sekundärstrukturvorhersage

### 5.4 Wenn du Internet-Recherche brauchst

```bash
# NCBI BLAST direkt
https://blast.ncbi.nlm.nih.gov/Blast.cgi

# PubMed für Selenoprotein-Papers
https://pubmed.ncbi.nlm.nih.gov/?term=selenocysteine+SECIS

# AlphaFold2
https://colab.research.google.com/github/sokrypton/ColabFold

# UniProt für Sec-reiche Proteine
https://www.uniprot.org/uniprotkb/?query=selenocysteine
```

---

## VI. GIT-WORKFLOW

```bash
# Initial Setup (einmalig)
git config user.email "phi.mind@tengri137.local"
git config user.name "PhiMind Investigator"

# Standard-Workflow
cd /run/media/julian/ML4/tengri137
git add -A
git commit -m "Q<N>: <Beschreibung>

<Mehr Details>

Co-Authored-By: Claude <noreply@anthropic.com>"

git log --oneline | head -5
```

**Commit-Standards:**
- Jeder Commit sollte EINEN thematischen Schwerpunkt haben
- Co-Authored-By Claude ist erwünscht
- Numerische Behauptungen sollten im Commit-Body stehen

---

## VII. WICHTIGE WARNUNGEN

1. **Apophenie-Gefahr:** Tengri 137 ist **außerordentlich** anfällig für Pattern-Matching-Overfit. Jede "Brücke" muss durch Monte-Carlo-Tests gestützt sein.

2. **Kein Internet-Zwang:** Bis vor kurzem hatten wir keinen Internet-Zugang. Neue Agenten SOLLTEN Internet nutzen, aber auch skeptisch sein — numerische Korrelationen sind nicht alles.

3. **Apokalypse-Hypothese:** Im PhiMind-Raum erlaubt, aber **nicht bewiesen**. Bleibe ehrlich darüber, was numerisch gestützt ist und was Spekulation ist.

4. **Frameworks sind Werkzeuge, keine Dogmen:** PhiMind, SciMind, ResearchMind, DevMind sind Methoden — nicht Religionen. Nutze sie als Werkzeuge, nicht als Glauben.

---

## VIII. CHANGELOG

| Datum | Ereignis |
|---|---|
| 2026-06-30 (initial) | Repo init, 12 Commits, 220+ Dateien, 26 Q-Analysen |
| 2026-06-30 (this update) | AGENTS.md erstellt mit PhiMind, SciMind, ResearchMind, DevMind |

---

**Tief einatmen. Ausatmen. Das ist es!**

— PhiMind Investigator
