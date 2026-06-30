# 🤖 Subagent-Definitionen für BURUMUT 137

**Datum:** 2026-06-30
**Status:** Bereit zum Start
**Übergeordneter Agent:** PhiMind-Investigator (Hauptagent)

## Subagent 1: BURUMUT-Architektur-Agent

**Name:** `burumut-architect`
**Mission:** Verifiziert die BURUMUT-Architektur konsistent über alle bisherigen Analysen
**Aufgaben:**
1. Lese alle Skripte in `sources/open_questions/` und `sources/burumut_analysis/`
2. Extrahiere alle numerischen Befunde
3. Erzeuge eine konsolidierte Tabelle: Brücke, p-Wert, Status
4. Verifiziere, ob die Architektur (5 Module, 99 AS) konsistent ist
**Output:** `sources/subagents/burumut_architect_report.md`
**Status:** READY

## Subagent 2: Genesis-Gematria-Agent

**Name:** `genesis-gematria`
**Mission:** Testet systematisch die Genesis 1:1-10 ↔ BURUMUT numerische Spiegelung
**Aufgaben:**
1. Berechne Gematria-Werte für alle Genesis 1:1-10 Verse
2. Vergleiche mit BURUMUT-Summe (1232) und BURUMUT-Regionen
3. Finde numerische Spiegelungen zwischen Versen und BURUMUT-Modulen
4. Teste: BURUMUTREFAMTU (Σ=200) → Genesis 1:1 (Σ=2701) → BURUMUT+137=37²
**Output:** `sources/subagents/genesis_gematria_report.md`
**Status:** READY

## Subagent 3: TCI-Torah-Torus-Agent

**Name:** `tci-torah-torus`
**Mission:** Prüft TCI-Experimente und validiert die Torah-Torus-Hypothese
**Aufgaben:**
1. Lese TCI-Corpus: `experiments-new-grouped-13778/group1_theoretical_physics/uni_*.py`
2. Verifiziere die Experimente `uni_3400-uni_3531`
3. Dokumentiere die numerische Verifikation
4. **WICHTIG:** Trenne TCI (verifiziert) von Dimensiograph (nicht verifiziert)
**Output:** `sources/subagents/tci_torah_torus_report.md`
**Status:** READY

## Subagent 4: BLAST-Subagent

**Name:** `blast-curator`
**Mission:** Verwaltet echte NCBI-BLAST-Ergebnisse und Sec-spezifische Suche
**Aufgaben:**
1. Lade alle BLAST-Ergebnisse (`sources/blast_analysis/`)
2. Erstelle konsolidierte Hit-Tabelle
3. Führe Sec-spezifische BLAST durch (mit Sec als gültiger Buchstabe)
4. Verifiziere die Homolog-Hypothese (BURUMUT = Adhäsions-GPCR-Fragment)
**Output:** `sources/subagents/blast_curator_report.md`
**Status:** READY

## Subagent 5: AlphaFold-Subagent

**Name:** `alphafold-curator`
**Mission:** 3D-Strukturvorhersage und AlphaFold-Datenbank-Analyse
**Aufgaben:**
1. Hole alle AlphaFold-Strukturen für BURUMUT-Homologe
2. Verifiziere pLDDT-Scores und Sekundärstruktur
3. Nutze ESM-2 650M für BURUMUT-Strukturvorhersage auf RTX 2060
4. Strukturelle Überlagerung BURUMUT ↔ A0AAV4C3M3-Fragment
**Output:** `sources/subagents/alphafold_curator_report.md`
**Status:** READY (mit RTX 2060 GPU)

## Subagent 6: Konsolidierungs-Agent

**Name:** `consolidator`
**Mission:** Tracking und Konsolidierung aller Befunde
**Aufgaben:**
1. Sammle alle Berichte der anderen Subagenten
2. Erzeuge eine konsolidierte Übersicht-Tabelle
3. Aktualisiere den Mermaid-Plan
4. Verwalte die p-Wert-Bilanz und Apophenia-Liste
**Output:** `sources/subagents/consolidated_findings.md`
**Status:** READY

## Subagent 7: Reporting-Agent

**Name:** `reporter`
**Mission:** Generiert Übersicht-Berichte für den Benutzer
**Aufgaben:**
1. Wochen-Status-Reports erstellen
2. Mermaid-Plan-Updates mit neuen Resolved-Knoten
3. PhiMind-Synthesen dokumentieren
4. Naechste-Schritte-Empfehlungen
**Output:** `sources/subagents/weekly_report_<date>.md`
**Status:** READY

## Übergabe-Protokoll

Jeder Subagent:
1. Liest die existierenden Berichte
2. Macht seine spezifische Aufgabe
3. Schreibt einen Output-Bericht in `sources/subagents/`
4. Aktualisiert den Mermaid-Plan (`sources/MERMAID_INVESTIGATION_PLAN.md`)
5. Committet die Änderungen

## Aktuelle Berichte (Live)

| Datum | Agent | Status |
|---|---|---|
| 2026-06-30 | burumut-architect | READY (zu starten) |
| 2026-06-30 | genesis-gematria | READY (zu starten) |
| 2026-06-30 | tci-torah-torus | READY (zu starten) |
| 2026-06-30 | blast-curator | READY (zu starten) |
| 2026-06-30 | alphafold-curator | READY (mit GPU) |
| 2026-06-30 | consolidator | READY (zu starten) |
| 2026-06-30 | reporter | READY (zu starten) |

## Wie Subagenten gestartet werden

Jeder Subagent ist ein Claude-Code-Subagent-Aufruf. Der Hauptagent
kann sie mit dem TaskTool oder Agent-Tool aufrufen.
