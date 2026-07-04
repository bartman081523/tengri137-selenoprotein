# Sources — Kategorie-Struktur

**Stand:** 2026-07-03 (P76)
**Struktur:** 6 Kategorie-Ordner, alle Tests in den Ordnern ihrer Experimente.

```
sources/
├── AGENTS.md                ← Orchestrator-Prompt (5-Mind-Konsortium)
├── project-specs.md         ← Was Tengri137 IST
├── MERMAID_INVESTIGATION_PLAN.md  ← Forschungsnarrativ
├── Tengri137_Full_Notes     ← Original-Transkription
├── Tengri-137.pdf           ← Quell-PDF
│
├── maschine/                ← M4-Turing-Maschine & Ausführungen
│   ├── TORA_TURING_*.py           (10 Varianten + Multiphase)
│   ├── M4_*.py                    (3 M4-Analysen)
│   ├── SPANDA_*.py                (5 Spanda-Module)
│   ├── QUINE_PROOF_M4.py
│   ├── META_TURING_KOGNITION.py
│   ├── RUN_MACHINE_*.py
│   ├── TENGRI137_TURING_MACHINE.py
│   ├── TENGRI_ORAKEL.py
│   ├── TENGRI137_PHONETIC_TAJPALA.py
│   ├── PHIMIND_VERIFY.py
│   ├── BUG_REPORT.py
│   ├── ANALYSE_*.py
│   ├── WAS_STEHT_AN.py
│   ├── conftest.py
│   └── test_*.py                  (16 Tests)
│
├── phasen/                  ← 168-Phasen-Analysen
│   ├── FIRST_FAIL_KARTOGRAPHIE.py
│   ├── ENTROPIE_TOPOGRAPHIE.py
│   ├── PHASE3_SEZIERUNG.py
│   ├── PHASE26_SEZIERUNG.py
│   ├── PHASE122_SEZIERUNG.py
│   ├── PHASE_MAPPING_TORA.py
│   ├── TOPOLOGIE_PROFIL.py
│   ├── SEVEN_DAYS_BURUMUT.py
│   ├── SIEBEN_TAGE_ANALYSE.py
│   ├── MULTI_PHASE_FULL_NOTES.py
│   ├── MULTI_MASCHINE_TORA_LESUNG.py
│   ├── BRUMMTON_*.py              (4 Brummton-Experimente)
│   ├── conftest.py
│   └── test_*.py                  (11 Tests)
│
├── burumut/                 ← BURUMUT-99 + KVM-Analysen
│   ├── BURUMUT_3D_STRUCTURE.py
│   ├── BURUMUT_FULL_TEXT.py
│   ├── BURUMUT_HOLOGRAPHIC.py
│   ├── BURUMUT_PHASES.py
│   ├── BURUMUT-SPANDA.txt         (PhiMind-Notiz)
│   ├── BINAH_ALEPH_TORUS.py
│   ├── KANONIK_VALIDATOR_MODUL.py (KVM = 护法)
│   ├── KVM_ANALYSE.py
│   ├── conftest.py
│   └── test_*.py                  (6 Tests)
│
├── holografie_sefirot/      ← Holografie + Sefer Yetzirah
│   ├── HOLOGRAFIC_BURUMUT_GENESIS.py
│   ├── HOLOGRAFIC_EXPANSION.py
│   ├── HOLOGRAPHIC_DEEP.py
│   ├── HOLOGRAPHIC_SYMMETRY_ANALYSIS.py
│   ├── SEFER_YETZIRAH_*.py        (6 Sefer-Yetzirah-Module)
│   ├── conftest.py
│   └── test_*.py                  (1 Test)
│
├── offene_fragen/           ← Q29, Q30, Q_FORMAL_PROOF, Q_PHASES_2_TO_6_DEEP,
│   │                              Q_TURING_OTHER_TEXTS, Q_LAYER_TORAH_FOLD_SYMPY,
│   │                              MULTI_LESUNG (P75)
│   ├── Q29_MISSING_LETTERS_TURING.py
│   ├── Q30_TURING_MACHINE.py
│   ├── Q_FORMAL_PROOF_BURUMUT_TENGRI137.py
│   ├── Q_LAYER_TORAH_FOLD_SYMPY.py
│   ├── Q_PHASES_2_TO_6_DEEP.py
│   ├── Q_TURING_OTHER_TEXTS.py
│   ├── MULTI_LESUNG.py
│   ├── conftest.py
│   └── (kein Test — Analyse-Module)
│
├── philosophie/             ← Philosophische Reflektion
│   ├── TORA_TURING_PHILOSOPHY.py
│   ├── PHILOSOPHICAL_ANALYSIS.py
│   ├── conftest.py
│   └── test_layer_register.py
│
├── burumut_analysis/        ← (P1-P9 Archiv, NICHT verschoben — historisch)
├── open_questions/          ← (Q1-Q28 Archiv, NICHT verschoben — historisch)
├── torah/                   ← Tora-Kapitel-JSON
├── blast_analysis/          ← NCBI-BLAST Resultate
├── verification/            ← Frühe Verifikation
├── mysticism/               ← Mystik-Skizzen
├── subagents/               ← (intern)
├── riemann_documents/, riemann_code/   ← Riemann-Archive
├── tci_documents/, tci_code/           ← TCI-Archive
├── tci_experiments_179_189/, tci_experiments_13730_13739/  ← TCI-Exp.
├── frameworks/              ← (leer — Inhalt nach /minds/ verschoben)
├── gpu_workspace/           ← GPU-beschleunigte Analysen
└── __pycache__/, .pytest_cache/
```

## Verifikations-Befehl

```bash
cd /run/media/julian/ML4/tengri137
python -m pytest sources/maschine/ sources/burumut/ sources/phasen/ \
                sources/philosophie/ sources/holografie_sefirot/ \
                sources/offene_fragen/
# → 877 tests grün (Stand P76)
```

## Warum diese 6 Kategorien?

1. **`maschine/`** — Alles, was die M4-Tora-Turing-Maschine betrifft:
   ihre Definition, ihre Ausführungen, ihre Diagnostik.
2. **`phasen/`** — Alles, was die 168 Phasen der Tengri137 betrifft:
   Sezierungen, Kartographien, Resonanz-Profile, Brummton-Phasen.
3. **`burumut/`** — Alles, was die BURUMUT-99-Matrix betrifft:
   3D-Struktur, holographische Lesung, KVM (Kanonik-Validator).
4. **`holografie_sefirot/`** — Holografie + Sefer Yetzirah —
   Brücke zur Kabbalistik.
5. **`offene_fragen/`** — Die großen offenen Fragen (Q29, Q30, Q-LAYER, etc.)
   + Multi-Lesungs-Experimente (P75).
6. **`philosophie/`** — Philosophische Reflektion: Was ist diese Maschine
   *ontologisch*? Layer-Register als Apophanie-Schutz.

Tests sind jeweils im selben Ordner wie ihre Experimente (per Anweisung).

## Apophenie-Schutz

Die 23 negativen Tests in `sources/maschine/test_apophenia_list.py`
sind in `maschine/`, weil sie an die Maschine gebunden sind. CitMind ist
zuständig; siehe `minds/CitMind.json`.

*Strukturiert von PhiMind Investigator + 5 Minds, 2026-07-03*
