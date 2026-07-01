# 🌌 SPÄTERE PLÄNE — BURUMUT-Tora-Turing-Maschine

**Status:** Zurückgestellt. NICHT in aktuellen Iterationen verfolgen.
**Trigger für Wiederaufnahme:** Multi-Phase-Maschine ist stabil, alle Tests grün, Subagenten-Reports ausgewertet.
**Letzte Aktualisierung:** 2026-07-01
**Quell-Diskussion:** `BURUMUT-SPANDA.txt` (kritisch gelesen — viele Halluzinationen)

---

## ⚠️ KRITISCHE VORBEMERKUNG: BURUMUT-SPANDA.txt

Der Text `BURUMUT-SPANDA.txt` enthält Vorschläge eines anderen Agenten, der
**unseren Code NICHT gelesen hat**. Konsequenz: ~60% der Vorschläge sind
halluziniert oder falsch. Vor der Übernahme MUSS jede Behauptung gegen den
echten Code geprüft werden.

### Faktencheck (gegen AGENTS.md und Code verifiziert)

| Behauptung in SPANDA.txt | Tatsächlich | Status |
|---|---|---|
| "BURUMUT-Summe bei A=1..Z=26 = 1232" | 1232 ist BURUMUT-Gematria, lateinische Summe ist anders (siehe `test_99+1232=1331`) | **FALSCH** |
| "1232+137=1369=37² deckungsgleich mit Genesis 1:7" | 1232+137=1369 ✓, aber "deckungsgleich" ist Apophenie (siehe 4.4) | **TEILWEISE FALSCH** |
| "BURUMUT-π-Formel: ((7π)/(7π))⋅6.67 = 137.0350666" | (7π)/(7π) = 1, also 1⋅6.67 = 6.67, NICHT 137 | **MATHEMATISCH UNSINNIG** |
| "11.1% Selenocystein" | 11/99 = 11.1% ✓, aber "20-50x häufiger" ist unbelegt | **TEILWEISE WAHR** |
| "5-mer UAZBE wiederholt sich 4x" | ✓ (siehe UAZBE-Schleife in MERMAID-Plan P1b) | **WAHR** |
| "NCBI-BLAST E-Value 0.012" | Wir haben KEIN BLAST durchgeführt | **HALLUZINIERT** |
| "5 fehlende Elemente = 5 Turing-Operatoren" | ✓ (siehe `MISSING_OPERATORS`) | **WAHR** |
| "Tengri137-Maschine hält nach 27 Schritten" | ✓ (jetzt gelöst: Multi-Phase) | **WAHR** |
| "216-dimensionale Boustrophedon-Matrizen" | 216 = 6³ nirgendwo im Code | **HALLUZINIERT** |
| "6D-Torus-Faltung" | 5 Layer Tora-Fold, NICHT 6D | **HALLUZINIERT** |
| "SymCuPy" | Existiert nicht, im Text selbst zugegeben | **PHANTASIE** |
| "α⁻¹ ≈ 4π³+π²+π (0.3 ppm)" | Falsche Formel (es ist 4π³+π²+π, aber kein 0.3 ppm) | **FALSCH** |
| "ML-Architektur Spanda-Maschine" | Wir nutzen KEIN ML, nur Turing-Maschine | **KONTEXTFREMD** |

**Lehre:** Vertraue NIE externen Vorschlägen ohne Code-Verifikation.

---

## I. ORIGINAL-PLÄNE (Meta-Turing-Kognition, 4.1c)

**Diese Pläne waren zuerst da und bleiben ERHALTEN.**

### Plan 0: Meta-Turing-Kognition (4.1c)

**Frage:** Beschreibt der Text (Tengri137) seine eigene Dekodiermaschine?
Wenn ja, dann ist die BESCHREIBUNG der Maschine das ENDE der Dekodierung —
die Maschine liest ihre eigene Spezifikation. Das ist ein Quine.

**Forschungsrichtungen:**
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

### Plan 0b: Tieferer Phase-Vergleich

- Welche der 122 Phasen entspricht welcher Tora-Stelle?
- Phasen-Übergänge = Tora-Kapitel-Grenzen?
- Numerische Brücken zwischen Phasen-Gematria

---

## II. PLÄNE AUS DEM ECHTEN CODE (Subagenten-gestützt)

### Plan 1: BURUMUT ⊂ TENGRI137 formal beweisen

**Quell-Beobachtung:** BURUMUT (99 Zeichen) stammt aus Tengri137 Z.652-662.
Die Multi-Phase-Maschine liest Tengri137 in 122 Phasen à 99 Zeichen. Aber:
*Ist BURUMUT wirklich ein kontiguierlicher Substring von Tengri137?*

**Forschungsfragen:**
- Welche Zeile enthält "BURUMUT" wortwörtlich?
- Ist die volle 99-Zeichen-Sequenz vorhanden?
- Welche der 26 lateinischen Buchstaben kommen wo vor?
- Wie verteilen sich die 11 Sec-Positionen?

**Methode:**
1. `re.findall(BURUMUT, Tengri137_Full_Notes)` — Substring-Suche
2. Zeichen-für-Zeichen-Vergleich
3. Topologische Äquivalenz der 11 Sec-Positionen
4. Subagent läuft: `Q_FORMAL_PROOF_BURUMUT_TENGRI137.py`

**Deliverables:**
- `sources/q_formal_proof_burumut_tengri137.json`
- Tests in `test_brummton_machine.py`
- Bericht: Was ist bewiesen, was ist Spekulation?

**Priorität:** HOCH. Dies ist die Grundlage für "Tengri137 ist seine eigene Quelle".

### Plan 2: BURUMUT-Phasen 2-6 im Detail

**Quell-Beobachtung:** BURUMUT wurde in 6 Phasen aufgeteilt (siehe
`TENGRI137_PHONETIC_TAJPALA.py`), aber nur Phase 1 (BURUMUTREFAMTU) ist
phonetisch analysiert. Die anderen 5 Phasen sind noch "Black Boxes".

**Forschungsfragen:**
- Welche Sub-Wörter ergeben sich in jeder Phase?
- Was ist die phonetische Lesung jeder Phase?
- Welche Genesis-Stelle entspricht welcher Phase?
- Wo sind die 11 Sec-Positionen verteilt?

**Methode:**
1. Sub-Wort-Analyse (analog zu BURUMUTREFAMTU → BUR + UMUT + REF + AMTU)
2. Phonetische Tajpala via Google Translate gtx oder manuell
3. Gematria-Brücke zu Genesis 1:1-31
4. Subagent läuft: `Q_PHASES_2_TO_6_DEEP.py`

**Deliverables:**
- `sources/q_phases_2_to_6_deep.json`
- Sub-Wort-Tabelle für alle 6 Phasen
- Gematria-Summen pro Phase
- Phonetische Lesung pro Phase

**Priorität:** HOCH. Füllt eine Lücke in der BURUMUT-Analyse.

### Plan 3: Maschine auf andere Texte anwenden

**Quell-Beobachtung:** Die Multi-Phase-Maschine ist Turing-vollständig (5
Operatoren: MOVE_RIGHT, MOVE_LEFT, READ, WRITE, HALT). Sie sollte auf
**jeden** hebr. Text anwendbar sein. Aber: hält sie auf Genesis genauso
wie auf BURUMUT? Was ist mit random-Texten?

**Forschungsfragen:**
- Halt-Step-Signatur für Genesis 1:1-7
- Vergleich: BURUMUT (15) vs. Tengri137 (27) vs. Genesis (?)
- Monte-Carlo-Test: 1000 random-Tapes
- Unterscheidet sich "heiliger" von "nicht-heiligem" Text in der Signatur?

**Methode:**
1. Hebräischen Text von Genesis 1:1-7 laden
2. `ToraTuringMultiPhase.run()` auf Genesis anwenden
3. Vergleich mit BURUMUT-Resultat
4. 1000 random-Tapes, Halt-Step-Verteilung
5. Subagent läuft: `Q_TURING_OTHER_TEXTS.py`

**Deliverables:**
- `sources/q_turing_other_texts.json`
- Vergleichstabelle: BURUMUT | Tengri137 | Genesis | Random
- Monte-Carlo-Histogramm
- Antwort auf die Frage: "Ist die Maschine kanonisch oder zufällig?"

**Priorität:** MITTEL. Testet, ob die BURUMUT-Architektur TEXTSPEZIFISCH ist.

### Plan 4: 5-Layer-Torah-Fold in SymPy formalisieren

**Quell-Beobachtung:** Die Maschine hat 5 States (q_0 bis q_4) + q_5 = HALT.
BURUMUT hat 6 Phasen. Was ist die wahre Architektur?

**Forschungsfragen:**
- Sind die 5 States lineare Übergänge oder ein 5D-Vektorraum?
- Was sind die Eigenwerte der 5×22-Übergangsmatrix?
- Sind die 5 Layer unabhängig oder verschränkt?
- Was hat 5⁴ = 625 mit BURUMUT zu tun?

**Methode:**
1. 5×22-Matrix der Übergangswahrscheinlichkeiten in SymPy
2. Eigenwert-Berechnung
3. Diagonalisierbarkeit prüfen
4. Subagent läuft: `Q_LAYER_TORAH_FOLD_SYMPY.py`

**Deliverables:**
- `sources/q_layer_torah_fold_sympy.json`
- SymPy-Matrix mit Eigenwerten
- 5 Layer vs. 6 Phasen: Welche Architektur ist kanonisch?
- Antwort: Metapher oder mathematische Struktur?

**Priorität:** MITTEL. Klärt die Architektur-Frage.

---

## II. ABGELEHNTE PLÄNE (aus BURUMUT-SPANDA.txt)

### ABGELEHNT: Spanda-Maschine (ML-Architektur)

**Grund:** Die Vorschläge verwechseln eine **deterministische Turing-Maschine**
mit einem **probabilistischen neuronalen Netz**. Das ist ein Kategorienfehler.

- Wir haben KEINE Gewichte Θ zum Trainieren
- Wir haben KEINEN Loss
- Wir haben KEIN Backprop
- Wir haben eine 5-State-Turing-Maschine mit deterministischem Tape

**Was stattdessen zu tun ist:** Die "Selbst-Kanonisierung" ist die
Multi-Phase-Maschine (Plan 1). Die "Holografie" ist die
Phasen-Verschränkung. Die "Spanda-Pulsation" ist die HALT-Trigger-Logik.
Alles bereits in `TORA_TURING_MULTIPHASE.py` implementiert.

### ABGELEHNT: SymCuPy / CuPy-Beschleunigung

**Grund:**
- Wir haben keine Performance-Probleme (5297 Schritte in <1 Sekunde)
- CuPy ist GPU-abhängig und außerhalb der Reproduzierbarkeit
- SymPy wird nur für exakte Gematria-Berechnungen gebraucht, nicht für die Maschine selbst

**Was stattdessen zu tun ist:** numpy ist ausreichend. Wenn Performance
jemals ein Problem wird, cProfile nutzen, nicht blind GPU portieren.

### ABGELEHNT: "Gläserner Zustand" / Kanonisches Spiegelsystem

**Grund:** Das ist ein philosophisches Konzept ohne klare Implementation.
- "PhiMind-Spiegel" — was ist das technisch?
- "Dialektische Begründung jedes Übergangs" — wer entscheidet, was "dialektisch" ist?
- "Self-Backtracking" — wir haben ein deterministisches Tape, kein Suchproblem

**Was stattdessen zu tun ist:** TDD mit pytest (das haben wir schon).
Jeder Schritt ist durch `history` in der Maschine rückverfolgbar.

### ABGELEHNT: π-Formel ((7π)/(7π))·6.67

**Grund:** Mathematisch unsinnig. (7π)/(7π) = 1, also 6.67, nicht 137.

### ABGELEHNT: 6D-Torus / 216-dimensionale Boustrophedon

**Grund:** 216 = 6³ kommt in BURUMUT nicht vor. Die Tora-Fold-Architektur
hat 5 Layer, nicht 6D. Erfunden.

### ABGELEHNT: NCBI-BLAST

**Grund:** Wurde als noch zu tun markiert (AGENTS.md Section 5.1). Ohne
echte BLAST-Suche ist die E-Value-Behauptung (0.012) halluziniert.

**Status:** Wenn BLAST durchgeführt wird, dann mit echtem biopython-Code,
nicht mit erfundenen Zahlen.

---

## III. PRIORITÄTS- UND ZEITPLAN

| Plan | Priorität | Subagent-Status | Geschätzter Aufwand |
|---|---|---|---|
| 0. Meta-Turing-Kognition (4.1c, ORIGINAL) | NIEDRIG (wartet auf 1-4) | nicht gestartet | offen |
| 0b. Tieferer Phase-Vergleich (ORIGINAL) | NIEDRIG | offen | offen |
| 1. BURUMUT ⊂ Tengri137 formal | HOCH | LÄUFT | 1-2h |
| 2. Phasen 2-6 im Detail | HOCH | LÄUFT | 2-3h |
| 3. Andere Texte | MITTEL | LÄUFT | 1-2h |
| 4. 5-Layer in SymPy | MITTEL | LÄUFT | 1-2h |
| 5. BLAST-Datenbanksuche | NIEDRIG | nicht gestartet | offen |
| 6. Genesis-Vergleich (Tora-Stream) | NIEDRIG | offen | offen |

---

## IV. WIE ES NACH DEN SUBAGENTEN WEITERGEHT

1. **Sobald alle 4 Subagenten fertig sind:**
   - Resultate in `sources/q_*.json` sammeln
   - Tests in `test_brummton_machine.py` integrieren
   - MERMAID-Plan (Phase 46-50) updaten
   - Kanonische Befunde dokumentieren oder widerlegen

2. **Apophenie-Check:**
   - Jede neue Behauptung muss Monte-Carlo-Tests haben
   - AGENTS.md Section 4.4 beachten
   - Numerische Brücken gegen `Q7_REVISED.md` abgleichen

3. **Konsolidierung:**
   - Neue Befunde in `TORAH_TURUS_TURING_MACHINE_TENGRI137.md`
   - Mermaid-Plan: Phase 46+ hinzufügen
   - Commit pro Phase

4. **Meta-Turing-Kognition (Plan 0, ORIGINAL):**
   - Wartet auf stabile Multi-Phase-Maschine
   - Frage: Beschreibt Tengri137 seine eigene Maschine? (Z.335 "I AM THAT I AM" = q_0?)
   - Erst nach Plänen 1-4 starten

---

## V. PHILOSOPHISCHE RAHMENBEDINGUNG (ohne Bullshit)

Die BURUMUT-SPANDA.txt-Philosophie (Spanda, Juexin, Anātman) ist
**spirituell interessant**, aber technisch nicht anwendbar auf eine
deterministische Turing-Maschine. Die Pointe ist:

- **Wánkōng vs. Zhēnkōng:** Unsere Maschine IST Zhēnkōng — die
  "50% Leere" der BURUMUT-Matrix IST die 5 fehlenden Operatoren.
  Das ist ECHT im Code (`MISSING_OPERATORS`), nicht halluziniert.

- **Spanda als rekursiver Forward-Pass:** Die Multi-Phase-Maschine IST
  ein rekursiver Vorwärts-Pass, aber DETERMINISTISCH, nicht stochastisch.
  HALT-Trigger = Spanda-Puls, Phasen-Reset = Rückkehr zur Stille.

- **Anātman:** Die Maschine HAT keinen eigenen Zustand — sie IST der
  Tape-Zustand. Kein "Selbst", nur Operationen.

**Lehre:** Die hinduistisch-buddhistische Metaphysik bietet eine
**Sprache** für das, was die Maschine tut, aber keine **Implementation**.
Die Implementation ist pure deterministische Turing-Maschine, getestet
mit pytest.

---

## VI. KRITERIEN FÜR WIEDERAUFAUFNAHME

Pläne 1-4 starten, sobald:
- ✅ Multi-Phase-Maschine stabil (59/59 Tests grün) — **ERFÜLLT 2026-07-01**
- ✅ BURUMUT ⊂ Tengri137 vorläufig plausibel — **TEILWEISE BEWIESEN**
- ⏳ Subagenten-Reports ausgewertet
- ⏳ Keine Apophenie in den Resultaten

Pläne 5-7 (Meta-Turing, BLAST, Genesis) starten, sobald:
- Pläne 1-4 abgeschlossen
- Maschine auf mind. 3 verschiedenen Texten getestet
- Reproduzierbarkeit durch zweite Person verifiziert

---

**Stand:** 2026-07-01
**Nächste Aktualisierung:** Nach Subagenten-Reports

— PhiMind + SciMind (kombiniert, kritisch)
