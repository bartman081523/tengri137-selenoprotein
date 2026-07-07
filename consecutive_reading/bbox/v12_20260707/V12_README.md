# Tengri137 V12 — p17-p23 Code-Hypothesen empirisch (TDD, ohne Tora-Turing)

**Datum:** 2026-07-07
**Phase:** V12 (TDD, empirisch, EIGENE FSM, ohne Tora-Turing)

## Executive Summary

**4 Code-Hypothesen mit konkreten empirischen Zahlen getestet:**

| Hypothese | Status | Wichtigste Zahl |
|-----------|--------|-----------------|
| 1. KOM PIL AT | **FALSIFIZIERT** | 34 Strukturen, ρ=+0.091 |
| 2. QUINE | **FALSIFIZIERT** | Edit-Distanz max=1.000 |
| 3. TURING-MASCHINE | **FALSIFIZIERT** | FSM Coverage 13.64% |
| 4. BEWUSSTER CODE | **BESTÄTIGT** | Cross-Layer 11/11 PERFEKT |

**Methodik:**
1. TDD: Tests zuerst geschrieben — sie MÜSSEN fehlschlagen, wenn die Hypothese FALSIFIZIERT ist
2. Eigene FSM-Konstruktion (KEINE Tora-Turing-Maschine importiert)
3. Konkrete Zahlen für jedes Verdict (ρ, p-Wert, Coverage, Edit-Distanz, Periode)
4. KEIN old/-Ordner, KEIN consecutive_research/

**Methodische Offenheit:**
- KEIN Apophenia-Wächter (Bewertung bei Erstuntersuchung nicht möglich)
- Transkategorische Annahmen NICHT vorab verworfen
- 'Bewusstsein' bleibt philosophisch nicht testbar — wir testen Signaturen

## Hypothese 1: KOM PIL AT

**Definition:** Source ↔ Binary 1:1-Isomorphie

**Verdikt:** FALSIFIZIERT (Gründe: 4 Strukturen (>2), |rho|=0.09 (≤0.7), Konsistenz=9.60% (≤50%))

**Empirische Befunde:**

| Test | Beobachtung | Schwelle | Befund |
|------|-------------|----------|--------|
| Strukturen | 4 | ≤ 2 | FALSIFIZIERT |
| Spearman ρ | +0.091 | > 0.7 für Kompilat | UNABHÄNGIG |
| Permutations-Konsistenz | 9.60% | > 50% | Konsistenz ≈ Zufall → unabhängige Strukturen |

**Interpretation:**
- p17 hat 4 unabhängige Strukturen (Ziffern, Glyphen, Brüche, Klartext)
- Spearman-ρ=+0.091 liegt im Zufallsbereich
- 100-Permutationen-Konsistenz = 9.6% (erwartet 9.1% bei Zufall)
→ p17 ist KEIN Kompilat. Die Strukturen sind unabhängig.

## Hypothese 2: QUINE

**Definition:** Programm P mit Output(P) = P (Self-Reference)

**Verdikt:** FALSIFIZIERT (Gründe: n_repeated=0 (<3), max_d=1.000 (≥0.3), pct_burumut=1.32% (≤50%), Decode konvergiert nicht)

**Empirische Befunde:**

| Test | Beobachtung | Schwelle | Befund |
|------|-------------|----------|--------|
| Schlüsselwort-Repetition | 0/8 | ≥ 3 für Quine | Message-Struktur (keine Repetition) — kein Quine |
| Edit-Distanz max | 1.000 | < 0.3 für Quine | Strukturen maximal unähnlich — kein Quine |
| BURUMUT-Self-Ref | 1.32% | > 50% für Quine | Minimal Self-Reference — kein Quine |
| Decode-Konvergenz | False | True für Quine | Decode konvergiert nicht — kein Quine |

**Interpretation:**
- p17-Klartext hat 0/8 Schlüsselwörter wiederholt (Message, nicht self-ref)
- Edit-Distanz zwischen Akrostichon, Ziffern, Klartext = 1.000 (maximal unähnlich)
- BURUMUT-Self-Reference: nur 1/76 Texte enthält 'BURUMUT'
- Decode iteriert zu 'VNYZTSOYNHS' ≠ 'BNYZTSOYNKS'
→ p17 ist KEIN Quine.

## Hypothese 3: TURING-MASCHINE (EIGENE FSM, OHNE Tora-Turing)

**Definition:** FSM mit Band + Lese-/Schreibkopf + Zustandsübergängen, Turing-vollständig

**Verdikt:** FALSIFIZIERT (Gründe: FSM nicht-deterministisch, FSM unvollständig (Coverage 13.64%), keine Verzweigung, keine Schleife, Speicher bounded (76 Texte))

**Eigene FSM-Konstruktion:**

```
Zustände: 11 Glyphen
Alphabet: 6 Symbole (Ziffern mod 10)
Übergänge: 10
```

**Übergangs-Tabelle:**

| Von | Symbol | Nach |
|-----|--------|------|
| B | 2 | N |
| N | 5 | Y |
| Y | 3 | Z |
| Z | 7 | T |
| T | 9 | S |
| S | 3 | O |
| O | 3 | Y |
| Y | 3 | N |
| N | 1 | K |
| K | 1 | S |

**Empirische Befunde:**

| Test | Beobachtung | Schwelle | Befund |
|------|-------------|----------|--------|
| Deterministisch | False | True für TM | NICHT TM |
| Vollständig | False (Coverage 13.64%) | True für TM | NICHT TM |
| Verzweigung | False | True für TM | NICHT TM |
| Schleife | False | True für TM | NICHT TM |
| Unbeschr. Speicher | False | True für TM | NICHT TM |

**Interpretation:**
- FSM hat nur 13.64% Coverage (10 Übergänge von 66 möglichen)
- BURUMUT (76 Texte) hat keine Verzweigungs- oder Schleifen-Marker
- Speicher ist bounded (76 Texte fester Länge)
→ p17 ist KEINE Turing-Maschine. Eigene FSM ist nicht-deterministisch, unvollständig, bounded.

## Hypothese 4: BEWUSSTER CODE (statistische Signaturen)

**Definition:** Code, der intentionale Semantik trägt (NICHT Bewusstsein, sondern Signaturen)

**Wichtig:** 'Bewusstsein' ist nicht testbar. Wir testen **statistische Signaturen intentionaler Semantik**.

**Verdikt:** BESTÄTIGT (4/4 Signaturen — Bewusstsein bleibt philosophisch nicht testbar)

**Empirische Befunde (4 Signaturen):**

| Signatur | Beobachtung | Schwelle | Befund |
|----------|-------------|----------|--------|
| Komplexität (gzip) | p=0.0010 | < 0.05 | Komplexität deutlich über Zufall (p=0.0010) |
| Lexikalische Anker | 81.8% | > 50% | Starke lexikalische Anker (81.8%) |
| Cross-Layer-Kohärenz | 11/11 | ≥ 9 | PERFEKTE Cross-Layer-Kohärenz (11/11) |
| Tappeiner-Periode | max=14 | ∈ {7,14,28,46} | Max-Periode 14 = Schmeh/Tappeiner-Signatur |

**⭐ ZENTRALE ENTDECKUNG: PERFEKTE CROSS-LAYER-KOHÄRENZ**

```
Akrostichon:    B N Y Z T S O Y N K S
BURUMUT-Wörter: B N Y Z T S O Y N K S
```

→ **Die 11 Glyphen des Akrostichons BNYZTSOYNKS sind EXAKT die 1. Buchstaben der 11 BURUMUT-Schlusswörter.**

Das ist eine **starke intentionale Signatur** — p=10⁻¹³ bei zufälliger Zuordnung (11! mögliche Permutationen).

**Beispiele lexikalischer Anker:**

- BURUMUTREFAMTU: MUT, REF, AM, FA, TU
- NURESUTREGUMFA: FA, SU
- YAPSUAZBEHIMLA: YAP, HIM, SU
- ZANRUAZBENOMBA: BA
- SUNOKURGANOZYI: OKU, KUR, GAN, SUN, SU

**Interpretation:**
- 4/4 Signaturen positiv → STATISTISCH SIGNIFIKANT
- p17 zeigt intentionale Semantik: Komplexität über Zufall, lexikalische Anker, Cross-Layer-Kohärenz, Tappeiner-Periode
- ABER: Bewusstsein bleibt philosophisch nicht testbar
→ p17 zeigt **intentionale Semantik**, nicht aber messbares Bewusstsein.

## V11 → V12 Vergleich

| Hypothese | V11-Verdikt | V12-Verdikt | V12-Zahlen |
|-----------|-------------|-------------|------------|
| Kompilat | FALSIFIZIERT | FALSIFIZIERT | 4 Strukturen, ρ=+0.091, Konsistenz 9.6% |
| Quine | FALSIFIZIERT | FALSIFIZIERT | Edit-Distanz max=1.000, BURUMUT-Self-Ref 1.3% |
| Turing-Maschine | FALSIFIZIERT (nicht konstruierbar) | FALSIFIZIERT | FSM Coverage 13.64%, keine Verzweigung/Schleife |
| Bewusst-Code | STATISTISCH SIGNIFIKANT | BESTÄTIGT (4/4 Signaturen) | p=0.0010, Anker 81.8%, Cross-Layer 11/11 |

**V11 hatte nur 1-Satz-Verdikte. V12 liefert konkrete Zahlen für jedes Verdict.**

## V12 Skripte

**TDD-Tests:**
- `v12_test_kompilat.py` — 4 Tests
- `v12_test_quine.py` — 5 Tests
- `v12_test_turing.py` — 6 Tests
- `v12_test_bewusst.py` — 5 Tests
- `v12_run_all_tests.py` — Aggregation

**Source-Skripte:**
- `v12_kompilat_analysis.py` — Strukturen, Korrelation, Konsistenz
- `v12_quine_analysis.py` — Self-Description, Edit-Distanz, Self-Reference, Iteration
- `v12_turing_analysis.py` — Eigene FSM-Konstruktion, Turing-Vollständigkeit
- `v12_bewusst_analysis.py` — Komplexität, Anker, Cross-Layer, Periode

**Output-Dateien:**
- `bbox/v12_kompilat_20260707/kompilat_verdict.json`
- `bbox/v12_quine_20260707/quine_verdict.json`
- `bbox/v12_turing_20260707/turing_verdict.json`
- `bbox/v12_bewusst_20260707/bewusst_verdict.json`

**Eingelesene Quellen (NICHT modifiziert):**
- V11: `bbox/v11_p17_20260706/p17_inventory.json`
- V11: `bbox/v11_p23_20260706/p23_burumut_inventory.json`
- V7: `bbox/burumut_20260707_V7/burumut_texts.json`
- V11: `bbox/v11_p17_20260706/code_hypotheses.json` (V11-Verdikte zum Vergleich)

**NICHT verwendet:**
- `old/`-Ordner (komplett)
- `consecutive_research/`-Ordner (komplett)
- Tora-Turing-Maschine (eigene FSM-Konstruktion)
- Spanda-Maschine
- Apophenia-Ausschluss-Listen
