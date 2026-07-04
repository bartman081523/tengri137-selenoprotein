# Subagenten für BURUMUT 137 Untersuchung

**Datum:** 2026-06-30
**Auf Wunsch des Benutzers:** Tracking und Konsolidierung

## Aktive Subagenten (geplant)

### 1. BURUMUT-Subagent
**Aufgabe:** Verifiziert die BURUMUT-Architektur
- 5 Module, 32+14+20+14+19 = 99 AS
- UAZBE × 4, HIMLAZANR × 2, NOMBA × 2
- Sec-Verteilung, hydrophob-Anteil
- Skript: `sources/open_questions/Q23-Q26`

### 2. Genesis-Subagent
**Aufgabe:** Vergleicht BURUMUT mit Genesis 1:1-10 Gematria
- 1:1 Σ = 2701 = 37·73
- 1:7 Σ = 1369 = 37² (BURUMUT + 137 = 37²)
- 1:9 Σ = 1701 = 37·46
- 5 Modul-zu-Tag-Mapping
- Skript: `sources/open_questions/Q27_burumut_genesis_matrix.py`

### 3. TCI-Subagent
**Aufgabe:** Prüft TCI-Experimente und Torah-Torus-Hypothese
- Experimente uni_3400-3531 in TCI-Corpus
- 5-Layer-Torah-Architektur
- Verifiziert die verifizierten Ergebnisse
- **WICHTIG:** Dimensiograph ist NICHT verifiziert (nur TCI selbst)

### 4. BLAST-Subagent
**Aufgabe:** Echte NCBI-BLAST (Sec-spezifisch)
- Sec als gültiger Buchstabe (mit PySec-BLAST oder erweitertem Alphabet)
- In-vitro-Vergleiche
- Skript: `sources/blast_analysis/`

### 5. AlphaFold-Subagent
**Aufgabe:** 3D-Strukturvorhersage (BURUMUT-ESMFold)
- ESMFold auf RTX 2060
- Sekundärstruktur-Vorhersage
- Vergleich mit A0AAV4C3M3 (Fam-a)
- Skript: `sources/gpu_workspace/`

### 6. Konsolidierungs-Subagent
**Aufgabe:** Reports und Tracking der Befunde
- Sammelt alle validierten Befunde
- Erstellt Übersichts-Berichte
- Verwaltet Mermaid-Plan
- Aktualisiert Findings-Reports

### 7. Reporting-Subagent
**Aufgabe:** Generiert Übersicht-Berichte
- Wochen-Status-Reports
- Mermaid-Plan-Updates
- p-Wert-Bilanz
- Phasen-Fortschritt

## Tracking-Tabelle

| Datum | Commit | Subagent | Aktion |
|---|---|---|---|
| 2026-06-30 | 46dc508 | Initial-Setup | Repo init, alle Quellen kopiert |
| 2026-06-30 | 2eec092 | Q1-Q7 | BURUMUT-Grundlagen + Apophenie-Widerlegung |
| 2026-06-30 | fd5c239 | Q8-Q9 | Selenoprotein-Hypothese + UAZBE-Sec-Korrelation |
| 2026-06-30 | 4fffa2b | Konsolidierung | Mermaid Plan R10-R12 |
| 2026-06-30 | 9862a94 | Q10-Q17 | DNA-Backtranslation + SECIS + 5-mer p<10⁻⁴ |
| 2026-06-30 | 751d37c | Q18-Q22 | HIMLAZANR, NOMBA, Linguistic-Density |
| 2026-06-30 | 432783d | Q25-Q26 | 4 Modi + Sec-Mechanismus |
| 2026-06-30 | a66eec3 | Q23-Q24 | mRNA-Architektur + Sec-Constraints |
| 2026-06-30 | c223074 | BLAST-Subagent | Echte NCBI-BLAST (4 Homologe) |
| 2026-06-30 | d8ff58e | BLAST-Subagent | Swiss-Prot: ENPP1 |
| 2026-06-30 | c74b1c6 | BLAST-Subagent | PDB: 6WFJ |
| 2026-06-30 | fc1300b | BLAST-Subagent | Eukaryota: Fam-a |
| 2026-06-30 | f397246 | Meta-Subagent | Meta-kognitive Analyse |
| 2026-06-30 | 84bc5db | Korrektur | Torah-Torus verifiziert, Dimensiograph NICHT |
| 2026-06-30 | 09d6b38 | Reporting | GRAND FINAL SYNTHESE |
| 2026-06-30 | 1686fed | Konsolidierung | Mermaid Plan Phase 11 |
| 2026-06-30 | 86e4d35 | AlphaFold-Subagent | A0AAV4C3M3 AlphaFold-Struktur |
| 2026-06-30 | eca3381 | Reporting | FINAL VALIDATED REPORT |
| 2026-06-30 | d202bc3 | Konsolidierung | PATHS_SEPARATION |
| 2026-06-30 | 49c9df1 | AlphaFold-Subagent | ESMFold lokal (Chou-Fasman) |
| 2026-06-30 | 154e602 | Korrektur | DIMENSIOGRAPH_CORRECTION |
| 2026-06-30 | f476ed2 | Konsolidierung | BLAST + Q27-Q28 + mysticism |
| 2026-06-30 | 3072e42 | AlphaFold-Subagent | GPU-workspace: ESM-2 + ESM-2 650M |

## GPU-Setup (RTX 2060, 12GB)

```bash
# Aktiviere das neue Env
micromamba activate tengri137

# Test
python -c "import torch; print('CUDA:', torch.cuda.is_available()); print('Device:', torch.cuda.get_device_name(0))"
# CUDA: True
# Device: NVIDIA GeForce RTX 2060
```

## Wechsel von Python 3.14 (venv) zu Python 3.11 (micromamba)

**Grund:** PyTorch hat keine Wheels für Python 3.14.
Lösung: Neues micromamba-Environment `tengri137` mit Python 3.11 + PyTorch 2.5.1 + CUDA 12.4.
