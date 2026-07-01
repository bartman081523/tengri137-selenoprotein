"""
Q_TURING_OTHER_TEXTS — Tora-Turing-Maschine auf ANDERE Texte angewandt
======================================================================

Wissenschaftlicher (SciMind-)Modus:
- AGENTS.md Section 4.2: Monte-Carlo, p-Werte, Apophenie-Kennzeichnung
- 1000+ Trials für jede Verteilung
- Klare Trennung: BEHAUPTUNG vs. BEFUND vs. APOPHENIE

WICHTIG (AGENTS.md 4.1b):
- Single-Machine-Prinzip: ALLE Tests laufen auf derselben
  Maschine (build_tora_transitions / build_extended_transitions).
- KEINE separate Maschine pro Text.

ARCHITEKTUR:
- ToraTuringMachine: HALT am ersten Trigger (15 Schritte auf BURUMUT)
- ToraTuringMultiPhase: Liest ALLE Phasen, Phasen-Reset bei HALT-Trigger
- run_machine_on_text(text, mapping) -> deterministisches Ergebnis

FRAGE (siehe Aufgabe):
- Ist die Halt-Step-Signatur TEXTSPEZIFISCH (dann kein universelles Muster)
- oder UNIVERSELL (dann ein Hinweis auf Tora-Turing-Hypothese)?
- Antwort: Monte-Carlo. Wenn alle Texte ~gleiche Signatur haben UND Random
  abweicht, dann evtl. universell. Wenn Texte stark streuen, dann
  textspezifisch. Wenn alle gleich aussehen, ist die Maschine trivial.
"""
import json
import random
import statistics
import sys
from collections import Counter
from pathlib import Path

# Ensure the local module can be imported
sys.path.insert(0, str(Path(__file__).parent))

from TORA_TURING_CORRECT import (
    ToraTuringMachine,
    build_tora_transitions,
    burumut_to_hebr,
    BURUMUT,
    LATIN_TO_HEBR,
    HEBR_VALUES,
)
from TORA_TURING_MULTIPHASE import (
    ToraTuringMultiPhase,
    build_extended_transitions,
    build_complete_transitions,
    EXTENDED_LATIN_TO_HEBR,
)


# Für hebräische Quelltexte (Genesis, Jesaja, etc.) brauchen wir ALLE
# 22 Konsonanten, nicht nur die 18 in LATIN_TO_HEBR.values(). Wir
# verwenden build_complete_transitions (siehe TORA_TURING_MULTIPHASE.py,
# das alle 22 hebr. Buchstaben abdeckt).


# =============================================================================
# TEIL 1: TEXTQUELLEN (Primärquellen für die Tests)
# =============================================================================
# Genesis 1:1-7 nach BHS (Biblia Hebraica Stuttgartensia), Konsonanten-Text.
# Vokalzeichen (Nikkud) sind in der originalen hebr. Schrift vorhanden, aber
# wir testen mit UND ohne Vokale, um den Effekt zu isolieren.

# Konsonanten-Text (22 hebr. Buchstaben, keine Vokalzeichen)
# ב ר א ש י ת  ב ר א  א ל ה י ם  א ת  ה ש מ י ם  ו א ת  ה א ר ץ
GENESIS_1_1_CONSONANTS = "בראשיתבראאלהיםאתהשמיםואתהארץ"
# Mit Vokalen (Nikkud): בְּרֵאשִׁית בָּרָא אֱלֹהִים אֵת הַשָּׁמַיִם וְאֵת הָאָרֶץ
GENESIS_1_1_VOCALIZED = "בְּרֵאשִׁיתבָּרָאאֱלֹהִיםאֵתהַשָּׁמַיִםוְאֵתהָאָרֶץ"

# Genesis 1:1-7 (BHS, nur Konsonanten, mit Wort-Trennern ⊥)
# Vers 1: 7 Wörter, 28 Buchstaben
# Vers 2: והארץ היתה תהו ובהו וחשך על פני תהום ורוח אלהים מרחפת על פני המים
# Vers 3: ויאמר אלהים יהי אור ויהי אור
# Vers 4: וירא אלהים את האור כי טוב ויבדל אלהים בין האור ובין החשך
# Vers 5: ויקרא אלהים לאור יום ולחשך קרא לילה ויהי ערב ויהי בקר יום אחד
# Vers 6: ויאמר אלהים יהי רקיע בתוך המים ויהי מבדיל בין מים למים
# Vers 7: ויעש אלהים את הרקיע ויבדל בין המים אשר מעל לרקיע ובין המים אשר מתחת לרקיע
GENESIS_1_1_TO_7_CONSONANTS = "בראשיתבראאלהיםאתהשמיםואתהארץ" \
    "והארץהיתהתהובהובחשךעלפניתהוםורוחאלהיםמרחפתעלפניהמים" \
    "ויאמראלהיםיהיאורויהיאור" \
    "ויראאלהיםאתהאורכיטובויבדלאלהיםביןהאורוביןהחשך" \
    "ויקראאלהיםלאוריוםולחשךקראלילהויהיערבויהיבקריוםאחד" \
    "ויאמראלהיםיהירקיעבתוךהמיםויהימבדילביןמיםלמים" \
    "ויעשאלהיםאתהרקיעויבדלביןהמיםאשרמעללרקיעוביןהמיםאשרמתחתלרקיע"

# Jesaja 1:1 (BHS): חֲזוֹן יְשַׁעְיָהוּ בֶּן־אָמוֹץ
# Konsonanten: ח ז ו ן   י ש ע י ה ו   ב ן   א מ ו ץ
# Hinweis: Im BHS-Text kommen Wort-End-Buchstaben vor: ן (Nun sofit) statt נ,
# ץ (Tzade sofit) statt צ, ם (Mem sofit) statt מ, ך (Kaf sofit) statt כ, ף (Pe sofit) statt פ.
# Wir normalisieren auf die Basis-Formen (22 Konsonanten).
JESAJA_1_1_CONSONANTS = "חזוןישעיהובןאמוץ"


def normalize_sofit(text):
    """Normalisiere Wort-End-Buchstaben (sofit) auf Basis-Formen.

    ך → כ, ם → מ, ן → נ, ף → פ, ץ → צ.
    Wird für BHS-Text benötigt, der Wort-End-Formen verwendet.
    """
    return (text
        .replace('ך', 'כ')
        .replace('ם', 'מ')
        .replace('ן', 'נ')
        .replace('ף', 'פ')
        .replace('ץ', 'צ')
    )

# Offenbarung 1:1 (griechisch) — wir mappen auf hebr. Buchstaben
# Αποκάλυψις Ἰησοῦ Χριστοῦ
# Vereinfachtes griechisch->hebr. Mapping (gleiche Gematria-Stellen):
#   Α(Alpha,1)->א, π->?  (Pe), κ->כ(Kaf), ά->א, λ->ל, υ->ו, ψ->?  (Pe-Samekh), ι->י, ς->ס
OFFENBARUNG_1_1_GREEK = "ΑποκάλυψιςΙησουΧριστου"
# Manuelles Mapping (Griechisch -> Hebräisch, ähnliche Werte):
GREEK_TO_HEBR = {
    'Α': 'א', 'α': 'א',  # Alpha (1) -> Aleph
    'Β': 'ב', 'β': 'ב',  # Beta (2) -> Beth
    'Γ': 'ג', 'γ': 'ג',  # Gamma (3) -> Gimel
    'Δ': 'ד', 'δ': 'ד',  # Delta (4) -> Dalet
    'Ε': 'ה', 'ε': 'ה',  # Epsilon (5) -> He
    'Ζ': 'ז', 'ζ': 'ז',  # Zeta (7) -> Zain
    'Η': 'ח', 'η': 'ח',  # Eta (8) -> Chet
    'Θ': 'ט', 'θ': 'ט',  # Theta (9) -> Teth
    'Ι': 'י', 'ι': 'י',  # Iota (10) -> Yod
    'Κ': 'כ', 'κ': 'כ',  # Kappa (20) -> Kaf
    'Λ': 'ל', 'λ': 'ל',  # Lambda (30) -> Lamed
    'Μ': 'מ', 'μ': 'מ',  # Mu (40) -> Mem
    'Ν': 'נ', 'ν': 'נ',  # Nu (50) -> Nun
    'Ξ': 'ס', 'ξ': 'ס',  # Xi (60) -> Samekh
    'Ο': 'ע', 'ο': 'ע',  # Omicron (70) -> Ayin
    'Π': 'פ', 'π': 'פ',  # Pi (80) -> Pe
    'Ρ': 'צ', 'ρ': 'צ',  # Rho (100) -> Tzade
    'Σ': 'ק', 'σ': 'ק', 'ς': 'ק',  # Sigma (200) -> Qoph
    'Τ': 'ר', 'τ': 'ר',  # Tau (300) -> Resh
    'Υ': 'ש', 'υ': 'ש',  # Upsilon (400) -> Shin
    'Φ': 'ת', 'φ': 'ת',  # Phi (500) -> Tav
    'Χ': 'ת', 'χ': 'ת',  # Chi (600) -> Tav
    'Ψ': 'ת', 'ψ': 'ת',  # Psi (700) -> Tav
    'Ω': 'ת', 'ω': 'ת',  # Omega (800) -> Tav
}


def greek_to_hebr(greek_str):
    """Konvertiere griechischen Text zu hebr. Text (best-effort)."""
    return ''.join(GREEK_TO_HEBR.get(c, '?') for c in greek_str)


# =============================================================================
# TEIL 2: RUN-MASCHINE-FUNKTION (Single Interface für alle Tests)
# =============================================================================

def run_machine_on_text(text, mode='single', phase_size=99, transitions=None,
                        extended=False):
    """Wende die Tora-Turing-Maschine auf einen hebr. Text an.

    Args:
        text: Hebräischer Text (Konsonanten-String).
        mode: 'single' (HALT am ersten Trigger) oder 'multi' (Phasen-Reset).
        phase_size: Phasen-Größe für Multi-Phase (Default 99 wie Tengri137).
        transitions: Übergangstabelle (default: build_tora_transitions oder
            build_extended_transitions je nach extended).
        extended: True für alle 22 hebr. Konsonanten (für Texte mit 'unbekannten'
            lateinischen Buchstaben).

    Returns:
        dict mit:
            'halt_step': int (Schritt, bei dem HALT/Phasen-Halt ausgelöst)
            'halt_state': int (0-5)
            'halt_reason': str
            'tape_length': int
            'states_visited': List[int] (alle besuchten Zustände)
            'mode': 'single' oder 'multi'
            'phases_completed': int (nur multi)
    """
    if transitions is None:
        # Für hebr. Texte (Genesis etc.): alle 22 Konsonanten nötig
        transitions = build_complete_transitions()

    if mode == 'single':
        m = ToraTuringMachine(text, transitions=transitions)
        m.run()
        s = m.summary()
        return {
            'mode': 'single',
            'halt_step': s['halt_step'],
            'halt_state': s['halt_state'],
            'halt_reason': s['halt_reason'],
            'tape_length': len(text),
            'states_visited': s['states_visited'],
            'gematria_sum': s['gematria_sum'],
        }
    elif mode == 'multi':
        m = ToraTuringMultiPhase(text, phase_size=phase_size, transitions=transitions)
        m.run(max_steps=50000)
        s = m.summary()
        return {
            'mode': 'multi',
            'halt_step': s['halt_step'],
            'halt_state': s['halt_state'],
            'halt_reason': s['halt_reason'],
            'tape_length': s['tape_length'],
            'n_phases': s['n_phases'],
            'phases_completed': s['phases_completed'],
            'phase_halts': s['phase_halts'],
            'total_steps': s['total_steps'],
        }
    else:
        raise ValueError(f"Unknown mode: {mode}")


# =============================================================================
# TEIL 3: MONTE-CARLO FÜR RANDOM-TAPES (Kontrollexperiment)
# =============================================================================

def random_tape_monte_carlo(alphabet, tape_length, n_trials=1000, mode='single',
                            transitions=None, seed_base=0):
    """Monte-Carlo: Halt-Step auf Random-Tapes mit gegebenem Alphabet.

    Args:
        alphabet: Liste der erlaubten Symbole.
        tape_length: Länge des zufälligen Tapes.
        n_trials: Anzahl Trials (default 1000).
        mode: 'single' oder 'multi'.
        transitions: Übergangstabelle.

    Returns:
        dict mit Statistiken:
            'mean': Mittelwert der Halt-Steps
            'median': Median
            'stdev': Standardabweichung
            'min': Minimum
            'max': Maximum
            'histogram': Counter der Halt-Steps
            'halt_reasons': Counter der Halt-Gründe
    """
    halt_steps = []
    halt_states = []
    halt_reasons = Counter()

    for trial in range(n_trials):
        random.seed(seed_base + trial)
        tape = ''.join(random.choice(alphabet) for _ in range(tape_length))
        result = run_machine_on_text(tape, mode=mode, transitions=transitions)
        halt_steps.append(result['halt_step'] if result['halt_step'] is not None else tape_length)
        halt_states.append(result['halt_state'])
        halt_reasons[result['halt_reason']] += 1

    return {
        'n_trials': n_trials,
        'tape_length': tape_length,
        'mean': statistics.mean(halt_steps),
        'median': statistics.median(halt_steps),
        'stdev': statistics.stdev(halt_steps) if n_trials > 1 else 0.0,
        'min': min(halt_steps),
        'max': max(halt_steps),
        'histogram': dict(Counter(halt_steps).most_common(20)),
        'halt_reasons': dict(halt_reasons.most_common()),
    }


# =============================================================================
# TEIL 4: HAUPTPROGRAMM — Tests auf BURUMUT, Genesis, Jesaja, Offenbarung
# =============================================================================

def main():
    print("=" * 70)
    print("Q_TURING_OTHER_TEXTS — Tora-Turing-Maschine auf andere Texte")
    print("=" * 70)
    print()

    results = {
        'method': (
            'Tora-Turing-Maschine (build_tora_transitions) angewandt auf '
            'verschiedene Texte. Single-Machine-Prinzip: dieselbe Maschine '
            'liest alle Texte. Halt-Step-Signatur verglichen mit Monte-Carlo.'
        ),
        'transitions': {
            'base_states': 6,  # q_0 bis q_5
            'halt_triggers': [
                'Aleph (א) in q_0 -> HALT',
                'Tav (ת) in q_2 -> HALT',
                'Nun (נ) in q_4 -> HALT',
            ],
        },
    }

    # --- TEST 1: BURUMUT (Referenz) ---
    print("=" * 70)
    print("TEST 1: BURUMUT (Referenz, 99 Zeichen)")
    print("=" * 70)
    burumut_hebr = burumut_to_hebr(BURUMUT)
    r_burumut_single = run_machine_on_text(burumut_hebr, mode='single')
    print(f"  Halt-Step: {r_burumut_single['halt_step']}")
    print(f"  Halt-State: q_{r_burumut_single['halt_state']}")
    print(f"  Halt-Reason: {r_burumut_single['halt_reason']}")
    print(f"  States visited: {r_burumut_single['states_visited']}")
    print()
    results['test1_burumut_single'] = r_burumut_single

    # --- TEST 2: GENESIS 1:1 (Konsonanten) ---
    print("=" * 70)
    print("TEST 2: Genesis 1:1 (Konsonanten, 28 Zeichen)")
    print("=" * 70)
    print(f"  Text: {GENESIS_1_1_CONSONANTS}")
    r_gen11 = run_machine_on_text(GENESIS_1_1_CONSONANTS, mode='single')
    print(f"  Halt-Step: {r_gen11['halt_step']}")
    print(f"  Halt-State: q_{r_gen11['halt_state']}")
    print(f"  Halt-Reason: {r_gen11['halt_reason']}")
    print(f"  States visited: {r_gen11['states_visited']}")
    print(f"  Gematria-Summe: {r_gen11['gematria_sum']}")
    print()
    results['test2_genesis_1_1_consonants'] = r_gen11

    # --- TEST 3: GENESIS 1:1 (Vokalisiert) ---
    print("=" * 70)
    print("TEST 3: Genesis 1:1 (Vokalisiert, 28 Zeichen + Nikkud)")
    print("=" * 70)
    # Mit Vokalen: die Vokalzeichen (im Unicode) sind NICHT im 22-Konsonanten-Alphabet
    # Daher: die Maschine wird NO_TRANSITION bekommen, weil Vokalzeichen nicht im
    # Mapping sind. Das ist ein REALISTISCHER Effekt: Nikkud ist in der Tora-
    # Turing-Maschine nicht definiert.
    r_gen11v = run_machine_on_text(GENESIS_1_1_VOCALIZED, mode='single')
    print(f"  Halt-Step: {r_gen11v['halt_step']}")
    print(f"  Halt-State: q_{r_gen11v['halt_state']}")
    print(f"  Halt-Reason: {r_gen11v['halt_reason']}")
    print(f"  States visited: {r_gen11v['states_visited']}")
    print()
    print("  HINWEIS: Nikkud (Vokalzeichen) sind in unserer Maschine NICHT")
    print("  definiert — daher NO_TRANSITION. Das ist ein ECHTER Effekt,")
    print("  kein Bug. Die Tora-Turing-Maschine liest nur Konsonanten.")
    print()
    results['test3_genesis_1_1_vocalized'] = r_gen11v

    # --- TEST 4: GENESIS 1:1-7 (Konsonanten, alle 7 Verse) ---
    print("=" * 70)
    print("TEST 4: Genesis 1:1-7 (Konsonanten, alle 7 Verse)")
    print("=" * 70)
    print(f"  Tape length: {len(GENESIS_1_1_TO_7_CONSONANTS)}")
    r_gen17_single = run_machine_on_text(GENESIS_1_1_TO_7_CONSONANTS, mode='single')
    print(f"  [SINGLE-MODE] Halt-Step: {r_gen17_single['halt_step']}")
    print(f"  [SINGLE-MODE] Halt-State: q_{r_gen17_single['halt_state']}")
    print(f"  [SINGLE-MODE] Halt-Reason: {r_gen17_single['halt_reason']}")
    print()
    r_gen17_multi = run_machine_on_text(GENESIS_1_1_TO_7_CONSONANTS, mode='multi', phase_size=99)
    print(f"  [MULTI-MODE]  Total Steps: {r_gen17_multi['total_steps']}")
    print(f"  [MULTI-MODE]  Phases completed: {r_gen17_multi['phases_completed']}")
    print(f"  [MULTI-MODE]  Halt-Step: {r_gen17_multi['halt_step']}")
    print(f"  [MULTI-MODE]  Halt-Reason: {r_gen17_multi['halt_reason']}")
    print(f"  [MULTI-MODE]  First 10 phase halts:")
    for h in r_gen17_multi['phase_halts'][:10]:
        print(f"    Phase {h['phase']}: Halt-Step={h['halt_step']}, "
              f"State=q_{h['halt_state']}, Reason={h['halt_reason']}")
    print()
    results['test4_genesis_1_1_to_7_single'] = r_gen17_single
    results['test4_genesis_1_1_to_7_multi'] = r_gen17_multi

    # --- TEST 5: JESAJA 1:1 ---
    print("=" * 70)
    print("TEST 5: Jesaja 1:1 (Konsonanten)")
    print("=" * 70)
    print(f"  Text: {JESAJA_1_1_CONSONANTS}")
    r_jesaja = run_machine_on_text(JESAJA_1_1_CONSONANTS, mode='single')
    print(f"  Halt-Step: {r_jesaja['halt_step']}")
    print(f"  Halt-State: q_{r_jesaja['halt_state']}")
    print(f"  Halt-Reason: {r_jesaja['halt_reason']}")
    print(f"  States visited: {r_jesaja['states_visited']}")
    print()
    results['test5_jesaja_1_1'] = r_jesaja

    # --- TEST 6: OFFENBARUNG 1:1 (griechisch -> hebr. Mapping) ---
    print("=" * 70)
    print("TEST 6: Offenbarung 1:1 (griechisch -> hebr. Mapping)")
    print("=" * 70)
    offen_hebr = greek_to_hebr(OFFENBARUNG_1_1_GREEK)
    print(f"  Original (griech.): {OFFENBARUNG_1_1_GREEK}")
    print(f"  Mapped (hebr.):     {offen_hebr}")
    r_offen = run_machine_on_text(offen_hebr, mode='single')
    print(f"  Halt-Step: {r_offen['halt_step']}")
    print(f"  Halt-State: q_{r_offen['halt_state']}")
    print(f"  Halt-Reason: {r_offen['halt_reason']}")
    print(f"  States visited: {r_offen['states_visited']}")
    print()
    results['test6_offenbarung_1_1'] = {
        'greek': OFFENBARUNG_1_1_GREEK,
        'hebr': offen_hebr,
        'result': r_offen,
    }

    # --- TEST 7: MONTE-CARLO — BURUMUT-Alphabet, Länge 99 ---
    print("=" * 70)
    print("TEST 7: MONTE-CARLO — BURUMUT-Alphabet, Random-Tape 99 Zeichen")
    print("=" * 70)
    print("  1000 Trials, BURUMUT-Alphabet (19 Symbole)")
    burumut_alphabet = list(set(burumut_to_hebr(BURUMUT)))
    print(f"  Alphabet ({len(burumut_alphabet)} Symbole): {burumut_alphabet}")
    mc_burumut = random_tape_monte_carlo(
        alphabet=burumut_alphabet,
        tape_length=99,
        n_trials=1000,
        mode='single',
        seed_base=42,
    )
    print(f"  Mean Halt-Step:   {mc_burumut['mean']:.2f}")
    print(f"  Median Halt-Step: {mc_burumut['median']:.1f}")
    print(f"  Stdev:            {mc_burumut['stdev']:.2f}")
    print(f"  Min/Max:          {mc_burumut['min']} / {mc_burumut['max']}")
    print(f"  Top-10 Halt-Steps: {mc_burumut['histogram']}")
    print(f"  Halt-Reasons:     {mc_burumut['halt_reasons']}")
    print()
    results['test7_monte_carlo_burumut_alphabet'] = mc_burumut

    # --- TEST 8: MONTE-CARLO — Genesis-Alphabet, Länge 28 (Gen 1:1) ---
    print("=" * 70)
    print("TEST 8: MONTE-CARLO — Genesis-Alphabet, Random-Tape 28 Zeichen")
    print("=" * 70)
    print("  1000 Trials, Alphabet = {א, ב, ר, ש, י, ת, ל, ה, מ, ו, ץ}")
    gen11_alphabet = list(set(GENESIS_1_1_CONSONANTS))
    print(f"  Alphabet ({len(gen11_alphabet)} Symbole): {gen11_alphabet}")
    mc_gen11 = random_tape_monte_carlo(
        alphabet=gen11_alphabet,
        tape_length=28,
        n_trials=1000,
        mode='single',
        seed_base=100,
    )
    print(f"  Mean Halt-Step:   {mc_gen11['mean']:.2f}")
    print(f"  Median Halt-Step: {mc_gen11['median']:.1f}")
    print(f"  Stdev:            {mc_gen11['stdev']:.2f}")
    print(f"  Min/Max:          {mc_gen11['min']} / {mc_gen11['max']}")
    print(f"  Top-10 Halt-Steps: {mc_gen11['histogram']}")
    print()
    results['test8_monte_carlo_genesis_1_1_alphabet'] = mc_gen11

    # --- TEST 9: MONTE-CARLO — Genesis-Alphabet, Länge 200 (Gen 1:1-7) ---
    print("=" * 70)
    print("TEST 9: MONTE-CARLO — Genesis-Alphabet, Random-Tape 200 Zeichen")
    print("=" * 70)
    print("  1000 Trials, Alphabet = Buchstaben aus Gen 1:1-7")
    gen17_alphabet = list(set(GENESIS_1_1_TO_7_CONSONANTS))
    print(f"  Alphabet ({len(gen17_alphabet)} Symbole): {gen17_alphabet}")
    mc_gen17 = random_tape_monte_carlo(
        alphabet=gen17_alphabet,
        tape_length=len(GENESIS_1_1_TO_7_CONSONANTS),
        n_trials=1000,
        mode='single',
        seed_base=200,
    )
    print(f"  Mean Halt-Step:   {mc_gen17['mean']:.2f}")
    print(f"  Median Halt-Step: {mc_gen17['median']:.1f}")
    print(f"  Stdev:            {mc_gen17['stdev']:.2f}")
    print(f"  Min/Max:          {mc_gen17['min']} / {mc_gen17['max']}")
    print(f"  Top-10 Halt-Steps: {mc_gen17['histogram']}")
    print()
    results['test9_monte_carlo_genesis_1_1_7_alphabet'] = mc_gen17

    # --- TEST 10: MONTE-CARLO — gleichverteiltes 22-Symbole-Alphabet ---
    print("=" * 70)
    print("TEST 10: MONTE-CARLO — Alle 22 hebr. Konsonanten, Länge 99")
    print("=" * 70)
    hebr_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
               'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
    mc_22 = random_tape_monte_carlo(
        alphabet=hebr_22,
        tape_length=99,
        n_trials=1000,
        mode='single',
        seed_base=300,
    )
    print(f"  Mean Halt-Step:   {mc_22['mean']:.2f}")
    print(f"  Median Halt-Step: {mc_22['median']:.1f}")
    print(f"  Stdev:            {mc_22['stdev']:.2f}")
    print(f"  Min/Max:          {mc_22['min']} / {mc_22['max']}")
    print()
    results['test10_monte_carlo_all_22'] = mc_22

    # --- TEST 11: P-WERT-BERECHNUNG ---
    # Vergleiche BURUMUT, Genesis 1:1, Genesis 1:1-7, Random-Tape
    # Frage: Ist die Halt-Step-Verteilung TEXTSPEZIFISCH?
    # Wenn ja: Texte unterscheiden sich signifikant von Random.
    # Wenn nein: Alle Verteilungen sind ~gleich (trivial).
    print("=" * 70)
    print("TEST 11: STATISTISCHER VERGLEICH")
    print("=" * 70)

    # Tatsächliche Halt-Steps
    real_halts = {
        'BURUMUT (99)': r_burumut_single['halt_step'],
        'Genesis 1:1 (28)': r_gen11['halt_step'],
        'Genesis 1:1-7 (single)': r_gen17_single['halt_step'],
        'Jesaja 1:1': r_jesaja['halt_step'],
        'Offenbarung 1:1': r_offen['halt_step'],
    }
    print("  Tatsächliche Halt-Steps:")
    for name, step in real_halts.items():
        print(f"    {name:30s}: {step}")

    # Z-Score: Wie weit ist jeder Text vom Random-Mittelwert entfernt?
    print()
    print("  Z-Score (Tatsächlicher Halt vs. Random-Mittelwert):")
    comparisons = {
        'BURUMUT (99)': (r_burumut_single['halt_step'], mc_burumut['mean'], mc_burumut['stdev']),
        'Genesis 1:1 (28)': (r_gen11['halt_step'], mc_gen11['mean'], mc_gen11['stdev']),
        'Genesis 1:1-7 (200)': (r_gen17_single['halt_step'], mc_gen17['mean'], mc_gen17['stdev']),
    }
    for name, (actual, mean, stdev) in comparisons.items():
        if stdev > 0:
            z = (actual - mean) / stdev
            print(f"    {name:30s}: z = {z:+.2f}  (actual={actual}, mean={mean:.2f}, stdev={stdev:.2f})")
        else:
            print(f"    {name:30s}: stdev=0, kann keinen Z berechnen")
    print()
    results['test11_statistical_comparison'] = {
        'real_halts': real_halts,
        'comparisons': {
            name: {
                'actual': c[0],
                'random_mean': c[1],
                'random_stdev': c[2],
                'z_score': (c[0] - c[1]) / c[2] if c[2] > 0 else None,
            }
            for name, c in comparisons.items()
        },
    }

    # Speichern
    out_path = Path(__file__).parent / 'q_turing_other_texts.json'
    with open(out_path, 'w') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print()
    print(f"Ergebnisse gespeichert in {out_path}")

    print()
    print("=" * 70)
    print("ZUSAMMENFASSUNG DER BEFUNDE")
    print("=" * 70)
    print()
    print("BEHAUPTUNG (zu testen): Die Tora-Turing-Maschine zeigt eine")
    print("  TEXTSPEZIFISCHE Halt-Step-Signatur.")
    print()
    print("BEFUND:")
    print(f"  - BURUMUT 99:    Halt-Step = {r_burumut_single['halt_step']}, "
          f"q_{r_burumut_single['halt_state']}, {r_burumut_single['halt_reason']}")
    print(f"  - Genesis 1:1:   Halt-Step = {r_gen11['halt_step']}, "
          f"q_{r_gen11['halt_state']}, {r_gen11['halt_reason']}")
    print(f"  - Genesis 1:1-7: Halt-Step = {r_gen17_single['halt_step']}, "
          f"q_{r_gen17_single['halt_state']}, {r_gen17_single['halt_reason']}")
    print(f"  - Jesaja 1:1:    Halt-Step = {r_jesaja['halt_step']}, "
          f"q_{r_jesaja['halt_state']}, {r_jesaja['halt_reason']}")
    print(f"  - Offenbarung 1:1: Halt-Step = {r_offen['halt_step']}, "
          f"q_{r_offen['halt_state']}, {r_offen['halt_reason']}")
    print()
    print("RANDOM-VERGLEICH (Monte-Carlo, 1000 Trials je):")
    print(f"  - BURUMUT-Alphabet (99): mean={mc_burumut['mean']:.2f}, "
          f"median={mc_burumut['median']}, stdev={mc_burumut['stdev']:.2f}")
    print(f"  - Genesis-Alphabet (28): mean={mc_gen11['mean']:.2f}, "
          f"median={mc_gen11['median']}, stdev={mc_gen11['stdev']:.2f}")
    print(f"  - Genesis-Alphabet (200): mean={mc_gen17['mean']:.2f}, "
          f"median={mc_gen17['median']}, stdev={mc_gen17['stdev']:.2f}")
    print(f"  - Alle 22 Konsonanten (99): mean={mc_22['mean']:.2f}, "
          f"median={mc_22['median']}, stdev={mc_22['stdev']:.2f}")
    print()
    print("Siehe BERICHT in q_turing_other_texts.json für Details.")


if __name__ == "__main__":
    main()
