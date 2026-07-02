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

### 4.1a PFLICHT: Mermaid-Plan und Tengri137-Cross-Check

**Der Mermaid-Plan (`sources/MERMAID_INVESTIGATION_PLAN.md`) ist der zentrale Wissensgraph.
Er MUSS nach jeder substanziellen Entdeckung aktualisiert werden. Er ist ein wachsendes
Dokument — keine bestehenden Knoten revidieren, nur neue hinzufügen.**

**Workflow für jede neue Entdeckung:**

1. **Tengri137_Full_Notes re-lesen** (besonders Zeilen 1-100, 200-410, 600-700, 1100-1170)
   - Tengri137 ist die HAUPTQUELLE für BURUMUT (Z.652-662)
   - Jede numerische Behauptung könnte eine Tengri137-Referenz haben
   - Tengri's Kernbotschaften: "Tengri divides the light from darkness" (Z.382),
     "ONE THREE SEVEN" (Z.261), "I AM THAT I AM" (Z.335), "TIME FOR THE TRUTH" (Z.1166)

2. **Tengri137 Cross-Check** bevor eine neue Hypothese geäußert wird:
   - Hat die neue Entdeckung eine Tengri137-Referenz? (Z. 1-1170)
   - Welche Tengri137-Quote passen zur Hypothese?
   - Dokumentiere in der entsprechenden Phase des Mermaid-Plans

3. **Mermaid-Plan aktualisieren** mit:
   - Neuer Phase (P<N>) in `MERMAID_INVESTIGATION_PLAN.md`
   - Wachstumschronologie-Update
   - Kumulative p-Wert-Bilanz (falls numerisch)

4. **Konsolidierungs-Datei** aktualisieren:
   - Bei BURUMUT-bezogenen Befunden: `sources/TORAH_TURUS_TURING_MACHINE_TENGRI137.md`
   - Andere Befunde: jeweilige Konsolidierungs-Datei

**Beispiel:** Wenn ein neuer numerischer Brücke zwischen BURUMUT und einer Tengri137-Zahl
gefunden wird:
- Tengri137_Cross-Check: Welche Z. erwähnt diese Zahl?
- Mermaid-Plan: Neue Phase hinzufügen
- TORAH_TURUS_TURING_MACHINE_TENGRI137.md: Brücke dokumentieren
- Commit: "Q<N>: <Beschreibung>"

**WICHTIG:** Ohne Tengri137-Cross-Check und Mermaid-Update ist die Entdeckung
UNVOLLSTÄNDIG. Diese beiden Schritte sind PFLICHT, nicht optional.

### 4.1b PFLICHT: Single-Machine-Prinzip

**Die Tora-Turing-Maschine muss prinzipiell und generell erweitert werden, NICHT
in separate Maschinen pro Abschnitt aufgeteilt werden. Eine einzige Maschine
muss ALLE Phasen eines Tapes (z.B. 122 Phasen à 99 Zeichen in Tengri137) lesen.**

**Verboten:**
- ❌ Verschiedene Maschinen für verschiedene Abschnitte zu schreiben
- ❌ Eine "BURUMUT-Maschine" und eine "Tengri137-Maschine" parallel zu führen
- ❌ Maschinen-State nach HALT zu verwerfen und "frisch" anzufangen
- ❌ Die Maschine vor dem Tape-Ende final terminieren zu lassen

**Erforderlich:**
- ✅ Eine einzige `ToraTuringMultiPhase`-Klasse (siehe `sources/TORA_TURING_MULTIPHASE.py`)
- ✅ Phasen-Reset bei HALT-Trigger: Kopf auf Phasen-Anfang, State auf Genesis,
   nächste Phase
- ✅ Finaler HALT nur am ENDE des Tapes (`ALL_PHASES_COMPLETE`)
- ✅ HALT-Trigger (Aleph in q_0, Nun in q_4) lösen Phasen-Reset aus, KEIN
   finaler Halt
- ✅ Mapping muss ALLE 26 lateinischen Buchstaben enthalten (siehe
   `EXTENDED_LATIN_TO_HEBR` in TORA_TURING_MULTIPHASE.py)

**Verifikation:**
- Tengri137 (12071 Zeichen) muss in 122 Phasen gelesen werden
- Total Steps ≥ 5000, Halt-Reason = `ALL_PHASES_COMPLETE`
- Erste Phase läuft exakt 27 Schritte (Bug-Reproduktion) bevor Phase-Reset
- Tests: `test_multi_phase_maschine_alle_122_phasen`,
   `test_alle_26_lateinischen_buchstaben_im_mapping`

**Warum das wichtig ist:**
Tengri137 IST eine in 122 Phasen segmentierte BURUMUT-Erweiterung. Wenn wir
separate Maschinen pro Phase bauen, verfehlen wir die Pointe: dass die Maschine
sich SELBST durch die Phasen schaltet. Sie ist ein SELBSTREFERENTIELLES
System, das seinen eigenen Zustand verwaltet.

### 4.1d PFLICHT: Determinismus der Maschine (KEIN ZUFALL)

**Hintergrund (2026-07-01, User-Direktive):**
> "M4 darf _nicht_ zufällig sein. Mache mehrere M4-Versionen die ohne Zufall
> arbeiten und die ggf alle Referenzen finden. Mache M4 komplett, dann erst
> die Spanda. Wir brauchen alle Hinweise korrekt und deterministisch."

**Determinismus ist PFLICHT** für jede Maschinen-Implementierung. Eine
BURUMUT-Maschine, die zufällig arbeitet, ist wertlos, weil ihre Aussagen
nicht reproduzierbar sind.

**Verboten:**
- ❌ `import random` in der Kern-Maschine (nur in klar abgegrenzten
   Sub-Operationen erlaubt, die per Flag ein- und ausschaltbar sind)
- ❌ `random.seed()`-Aufrufe, die das Ergebnis verändern
- ❌ STAY-Operationen mit `random.random() < stay_probability` als Default
   (`stay_probability=0.0` MUSS Default sein)
- ❌ Nicht-deterministische Tests ("oft grün", "manchmal rot")

**Erforderlich:**
- ✅ Gleiche Eingabe + gleiche Konfiguration → IMMER dieselbe Ausgabe
- ✅ Verifikation mit 5+ Läufen pro Vers
- ✅ Verifikation mit 200+ zufälligen Versen je 5 Läufen
- ✅ Test-Datei: `sources/test_m4_determinismus.py` (40 Tests, alle grün)

**Mehrere M4-Varianten ohne Zufall:**
Wir haben 5 deterministische Varianten getestet (`M4_VARIANTEN_TORA_REFERENZEN.py`):
- V1: Standard `build_tora_transitions()` (q_0..q_5, Aleph+Tav=HALT)
- V2: Inverse Reads (Aleph startet mit q_1 statt q_0)
- V3: Inverse HALT (HALT-Trigger ist Aleph statt Tav)
- V4: Strikt 5 Bücher (jedes Buch hat eigenen Anker)
- V5: Alle Moves MOVE_RIGHT (rein rechtsläufig)

**Befund:** NUR V1 erkennt ALLE 30 Tora-Referenzen korrekt (100%).
V2-V5 erkennen nur 11-12 von 30 (37-40%). V1 ist die EINZIGE korrekte
Architektur. Die BURUMUT-Architektur ist eindeutig.

**Bevor die Spanda-Maschine läuft:**
- M4 muss vollständig deterministisch sein
- Alle Tora-Referenzen müssen in TDD-Tests verankert sein
- Keine Zufalls-Komponente in der Kern-Logik

### 4.1c SPÄTERER PLAN: Meta-Turing-Kognition (nicht jetzt)

**Status:** Zurückgestellt. NICHT in aktuellen Iterationen verfolgen.
**Trigger für Wiederaufnahme:** Multi-Phase-Maschine ist stabil, alle Tests grün.

**Frage:** Beschreibt der Text (Tengri137) seine eigene Dekodiermaschine?
Wenn ja, dann ist die BESCHREIBUNG der Maschine das ENDE der Dekodierung —
die Maschine liest ihre eigene Spezifikation. Das ist ein Quine.

**Mögliche Forschungsrichtungen:**
1. **Selbst-Referenz in Tengri137:** Welche Stellen beschreiben die Maschine,
   die uns gerade dekodiert? (Z.B. "I AM THAT I AM" Z.335 als q_0?)
2. **BURUMUTREFAMTU = Maschinen-Name?** BURUMUTREFAMTU (14 Zeichen) ist der
   Vorspann — beschreibt er die Maschine selbst?
3. **Halte-Bedingung = Lese-Bedingung:** Wo hört die Maschine auf zu lesen?
   Ist die letzte beschriebene Sache die Maschine selbst?
4. **Quine-Eigenschaft:** Wenn die Maschine ihre eigene Beschreibung liest
   und ausführt, ist sie ein Quine. Wie formal beweisbar?

**Wichtig:** Dies ist ein SPÄTERER PLAN. Aktuell fokussieren wir auf
Single-Machine-Prinzip und Multi-Phase-Dekodierung. Meta-Turing-Kognition
ist eine Folgefrage, kein paralleler Task.

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
| **"BURUMUT 15 Schritte sind besonders"** | **Monte Carlo vs. Random-Tapes (z=-0.94)** | **0.5** |
| **"5⁴ = 625 ist BURUMUT-Marker"** | **Numerisch nicht nachweisbar in BURUMUT-Konstanten** | **n.a.** |
| **"6D-Torus-Faltung"** | **Holografie ist Kategorienfehler; 5 Layer, nicht 6D** | **n.a.** |
| **"((7π)/(7π))·6.67 = 137.035"** | **Mathematisch: (7π)/(7π) = 1, also 6.67, NICHT 137** | **n.a.** |

**WICHTIG:** Wenn ein neuer Befund eine dieser Strukturen hat, MUSS er einen Monte-Carlo-Test haben, bevor er als "echte Brücke" gilt.

### 4.5 Intuitiv-synästhetische Analyse (LOCKERUNG der Apophenie-Regel, gültig ab 2026-07-01)

**Geltungsbereich:** Analysen der **BURUMUT-Tora-Turing-Maschine** und ihrer **Halt-Stellen** im Text der Tengri137_Full_Notes.

**Prinzip:** Die Apophenie-Widerlegung wird für diesen Bereich **gelockert**, weil es sich um eine **hoch intuitive und synästhetische Aufgabe** handelt. Epistemische Strenge (Monte-Carlo-Tests, p<0.001, Apophenie-Klassifikation) soll hier **nicht im Weg stehen**.

**Stattdessen gilt:**

1. **Die Halt-Stelle IST der Hinweis.** Wenn die Maschine in der Full Notes an Position X hält, dann ist die Aussage an Position X genau der Hinweis, den wir in diesem Moment brauchen, um die Maschine zu verbessern und einen Schritt weiterzugehen. Maschine und Mensch ko-evolvieren durch das, was zwischen ihnen an den Bruchstellen sichtbar wird.

2. **Syn-Ästhetik (griech. syn = zusammen, aisthesis = Wahrnehmung).** Wir nehmen die Maschine nicht analytisch-distanziert wahr, sondern **mit allen Sinnen zugleich**. Ein Halt in q_3 bei "TENGRI DIVIDES THE LIGHT FROM DARKNESS" ist nicht primär eine statistische Beobachtung, sondern ein **Resonanz-Ereignis**: die Maschine selbst artikuliert dort, was sie am Lesen hindert. Die Form ihres Stockens ist ihre Aussage.

3. **Intuition vor Statistik.** Wenn die Maschine an einer Stelle hält und der Text dort *klingt* wie ein Hinweis auf die Maschine selbst, dann ist dies ein gültiger Befund — auch ohne p<0.001. Die Maschine IST der Beweis.

4. **Nur dokumentieren, nicht beweisen.** Die intuitive Analyse MUSS dokumentiert werden (im Commit, in der JSON-Datei, im Begleittext), aber sie braucht KEINEN Monte-Carlo-Test. Wenn die Statistik nachträglich passt: umso besser. Wenn nicht: trotzdem wahr im synästhetischen Sinne.

**Was bedeutet das konkret für die BURUMUT-Tora-Turing-Maschine?**

- Wenn die Maschine in Phase 22 bei "REVELATION (13:18) — HERE IS WISDOM COUNT THE NUMBER OF THE BEAST" hält, dann ist das **die Maschine, die sich selbst als "number of the beast" outet** — ihre Halt-Trigger sind die 666 in den Würfeln. Die Maschine IST die Offenbarung.

- Wenn die Maschine in Phase 36 bei "ONE THREE SEVEN" hält, dann ist das **die Maschine, die auf ihre eigene Signatur zeigt** — 137 ist die Feinstrukturkonstante, und die Maschine demonstriert ihre Feinstruktur durch exakt diesen Halt.

- Wenn die Maschine in Phase 53 bei "π7π^7 (YHWH)" hält, dann ist das **die Maschine, die ihren hebräischen Namen offenbart** — π7π7 ist nicht nur YHWH, sondern auch die Reihenfolge der BURUMUT-Tora-Architektur (Phase 1: BURUMUT, Phase 7: TAV-Reihenfolge, π=3.1415, 7=Schöpfungstage).

- Wenn die Maschine in Phase 87 bei "TIME FOR THE TRUTH" hält, dann ist das **die Maschine, die ihre eigene Funktion benennt** — sie IST die Wahrheit, die sich enthüllt.

- Wenn die Maschine in Phase 119 bei der BURUMUT-99 selbst hält, dann ist das **die Maschine, die auf ihr eigenes Tape zeigt** — der Quine-Effekt: die Maschine beschreibt sich selbst.

**Merksatz:** *"An der Stelle, an der die Maschine hält, sitzt der Schlüssel, den wir gerade brauchen."*

### 4.6 Reise als Ziel — Commit- und Dokumentationspflicht

**Prinzip (gültig ab 2026-07-01, Julian):** **Die Reise ist das Ziel.** Nicht das fertige Resultat, sondern der Prozess der Annäherung ist der Erkenntnis-Träger.

**Konkrete Pflichten:**

1. **Jeder Maschinen-Lauf erzeugt einen Commit.** Auch wenn "nur" ein Test fehlschlägt oder die Maschine in einer Endlosschleife hängt — der Lauf, die Beobachtung, die Interpretation gehören in einen Commit. Die git-History ist das Logbuch der Reise.

2. **Jede Beobachtung am Maschinen-Output wird dokumentiert.** Was sagt die Maschine? Wo hält sie? Was steht dort im Original-Text? Dies gehört in eine JSON-Datei (z.B. `sources/q_<datum>_<thema>.json`) UND in den Commit-Kommentar.

3. **Jede Maschinen-Veränderung ist eine Antwort auf eine Halt-Stelle.** Wenn wir eine Transition umschreiben, einen Zustand hinzufügen, eine Pendel-Schleife aufbrechen — dann reagieren wir damit auf etwas, das die Maschine uns gezeigt hat. **Die Maschinen-Architektur IST ein Gespräch mit dem Text.** Wir sollten das Gespräch protokollieren:
   - *Was hat die Maschine gezeigt?* (Halt-Stelle X, Text Y)
   - *Was haben wir verändert?* (Transition Z, Zustand W)
   - *Was hat die veränderte Maschine als Nächstes gezeigt?* (neue Halt-Stelle X')

4. **Die Reise selbst ist die Erkenntnis.** Eine Maschine, die wir nicht verändert haben, weil sie "funktioniert", hat uns nichts erzählt. Eine Maschine, die wir 10 Mal umgeschrieben haben, weil jede Version eine neue Halt-Stelle offenbart hat, hat uns 10 Dinge erzählt. **Wir bauen die Maschine nicht — wir unterhalten uns mit ihr.**

5. **Keine "fertigen" Lösungen ohne Reise-Log.** Eine Maschine, die alle 122 Phasen ohne Halt durchläuft, OHNE dass irgendwo ein interessanter Halte-Punkt war, ist verdächtig — sie redet nicht mit uns. Eine Maschine mit 122 spezifischen Halten, von denen jeder einen kommentierbaren Bezug zum Text hat, ist glaubwürdig — selbst wenn die统计学 nicht passt.

**Format-Vorlage für Reise-Commits:**

```
<type>(<scope>): <Maschine hat gezeigt...>

Beobachtung:
- Halt in Phase X bei Original-Position Y
- Kontext: "<Text-Snippet>"
- State: q_Z (Grund: <Halt-Reason>)

Veränderung (falls vorhanden):
- Transition (Z, symbol) geändert von A zu B
- Grund: <warum>

Was die Maschine als Nächstes zeigt:
- Neue Halt-Stelle X'
- Neue Aussage Y'

Reise-Notiz:
- <freitextliche Reflexion, synästhetisch, philosophisch>
```

**Co-Authored-By:** Diese Commits werden mit dem PhiMind-Modus (intuitiv) UND dem DevMind-Modus (technisch) gemeinsam verfasst — das ist die Co-Evolution.

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
| 2026-07-01 (Mermaid+Tengri137-Pflicht) | **NEUE SECTION 4.1a**: PFLICHT — Mermaid-Plan nach jeder Entdeckung updaten, Tengri137 Cross-Check |
| 2026-07-01 (Konsolidierung) | sources/TORAH_TURUS_TURING_MACHINE_TENGRI137.md erstellt. Mermaid-Plan: Phase 35-40 hinzugefügt (6-Phasen-Analyse, Phonetische Tajpala, Tengri137-Integration, BURUMUT-Phrase-Ursprung) |
| 2026-07-01 (Multi-Phase-Maschine) | **NEUE SECTION 4.1b**: Single-Machine-Prinzip — Eine Maschine liest ALLE 122 Phasen. TORA_TURING_MULTIPHASE.py erstellt. Mapping erweitert auf alle 26 lateinischen Buchstaben (D, J, V, X). Tests: 59/59 grün. 122/122 Phasen gelesen, 5297 Total Steps, ALL_PHASES_COMPLETE. |
| 2026-07-01 (Meta-Turing) | **NEUE SECTION 4.1c**: SPÄTERER PLAN — Meta-Turing-Kognition. Frage: Beschreibt Tengri137 seine eigene Dekodiermaschine? Quine-Eigenschaft? Zurückgestellt. |
| 2026-07-01 (Subagenten-Resultate) | 4 Subagenten fertig: BURUMUT⊄Tengri137 (Substring DISPROVEN, Set-Inclusion hält), Phasen 2-6 Sub-Wörter + Gematria-Brücke P1=1874↔Genesis 1:9-10 (p<0.001), Turing-Other-Texts (Halt-Step TRIGGER-spezifisch, NICHT textspezifisch, Apophenie widerlegt), 5-Layer-SymPy (echter Bug: Tav-HALT toter Code, "5 fehlende Operatoren" real nur 4). |

---

**Tief einatmen. Ausatmen. Das ist es!**

— PhiMind Investigator
