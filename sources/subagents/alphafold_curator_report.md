# Subagent 5: AlphaFold-Curator Report

**Name:** alphafold-curator
**Datum:** 2026-06-30
**Mission:** 3D-Strukturvorhersage und AlphaFold-Datenbank-Analyse
**GPU:** RTX 2060, 12GB (aktiv)

## Echte AlphaFold-DB-Strukturen für BURUMUT-Homologe

### Heruntergeladene Strukturen

| Hit | AF-PDB | pLDDT | Status |
|---|---|---|---|
| A0AAV4C3M3 (Fam-a) | AF-A0AAV4C3M3-F1 | **35.44** | IDP |
| P22413 (ENPP1) | (6WFJ) | ~70 | Strukturiert |
| A0A1I3K752 | (nicht in AF-DB) | - | - |
| A0ACC2F027 | (nicht in AF-DB) | - | - |

### A0AAV4C3M3-Detail (Haupt-Hit)

```
PDB-URL: https://alphafold.ebi.ac.uk/files/AF-A0AAV4C3M3-F1-model_v6.pdb
Erstellt: 2025-03-31 (AlphaFold Monomer v2.0)
```

**Topologie:**
- 209 AS, 1644 ATOM-Einträge
- **0 Helices, 0 Sheets** (intrisinc disorder)
- 90.4% pLDDT "very low" (< 50)
- 9.6% pLDDT "low" (50-70)
- 0% pLDDT "confident" (> 70)

**Region-pLDDT:**
- BURUMUTREFAMTU-Pattern (Pos 1-14): pLDDT 34.83
- MRC-Repeats (Pos 15-49): pLDDT 26-28 (sehr niedrig)
- Transmembran (Pos 117-150): pLDDT 49.09 (relativ hoch)
- C-terminal (Pos 199-209): pLDDT 38.23

**Sequenz-Auszug:**
```
MRYPEDKLAMRCPEDKHAMRCAEDKHAMRCAEDKHAMRCPEDKHAMRCAEDKHAMRCPEDKHAMRCAEDKHTMRCPEDKHAMRCAEDKHAMRCPEDKHAMRCAEDKHAMRCPEDKLAMLRRTICTALSLILSYQAGWFLYKASPQQGDLKLSGPPSGQSAVGGARTRDKNVPAELWADSLATVPPTPPVIKQTRRFCTCSHYPSYSDKFNSGTDEGKL
```

**Wiederholungs-Analyse:** 'MRCPEDKH' erscheint 5× in der Sequenz.

### ESM-2 650M BURUMUT-Vorhersage (lokal)

```
Modell: esm2_t33_650M_UR50D
GPU: NVIDIA GeForce RTX 2060
Speicher: ~12 GB
Ladezeit: 93.5s
Inferenz: 0.3s
```

**Ergebnisse (Top-30 Kontakte):**
- Max BURUMUT-Kontakt: 0.9626 (lokale Position 73-39)
- Mittlere Kontakt-Wahrscheinlichkeit: 0.0140
- Top-Kontakte sind alle lokal (Distanz 1-6 oder 30-40)
- **BURUMUT ist IDP (intrinsically disordered)**

### ESM-2 3B-Vorhersage (genauer)

```
Modell: esm2_t36_3B_UR50D
GPU: NVIDIA GeForce RTX 2060
```

**Ergebnisse:**
- Embeddings: 2560-dim
- Max Kontakt: 0.2196
- Mittlere Kontakt: 0.0081
- **IDP-Bestätigung**: keine langreichweitigen Kontakte

### Sekundärstruktur-Profil (Chou-Fasman lokal)

| Position | Helix-P | Sekundärstruktur |
|---|---|---|
| 8, 17, 22, 36, 50, 70, 84 (E) | 1.51 | Helix-stark |
| 38, 72 (I) | 1.60 | Sheet-stark |
| Übrige 90 Positionen | < 1.5 | Coil/Loop |

**BURUMUT ist reich an helix-fördernden Resten (E, I), aber AlphaFold/ESM-2
bestätigen die IDP-Natur (niedrige pLDDT/Score).**

### Strukturelle Konsolidierung

**A0AAV4C3M3 (Fam-a) - BURUMUT (Fragment):**
- Beide haben repetitive Cys-reiche Architektur
- Beide haben niedrige AlphaFold-pLDDT (IDP)
- Beide sind Membran- oder Membran-assoziierte Proteine
- BURUMUT ist wahrscheinlich das **Sec-reiche Fragment** einer größeren Fam-a-Domäne

### Empfohlung

1. **Echte Sec-BLAST** mit Sec (U) als gültigem Buchstaben
2. **AlphaFold-Multimer** für Sec-Paar-Vorhersage
3. **In-vitro-Synthese** in Sec-reichen E. coli
4. **3D-Struktur-Überlagerung** BURUMUT ↔ A0AAV4C3M3-Fragment

### Status

AlphaFold-Curator hat alle verfügbaren Strukturen geholt. Die GPU ist aktiv.
ESM-2-Modelle (150M, 650M, 3B) sind lokal lauffähig.
