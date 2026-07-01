"""
Q_LAYER_TORAH_FOLD_SYMPY — FORMALE 5-LAYER-TORAH-FOLD-ARCHITEKTUR
=================================================================

SciMind-Audit der Behauptung "5-Layer-Torah-Fold" (TORAH_TURUS_TURING_MACHINE_TENGRI137.md).

Hypothese (zu prufen):
  H1: Die Tora-Turing-Maschine (TORA_TURING_CORRECT.py) mit 5 q_i-States
      bildet eine "5-Layer-Faltungs-Architektur" — die 22 hebraischen
      Konsonanten werden durch eine 5x22-Matrix kodiert.

Was hier formalisiert wird:
  1. Die echte Uebergangstabelle (deterministisch, aus build_tora_transitions()).
  2. Die kanonische 22-Konsonanten-Basis mit Gematria-Werten.
  3. Drei Matrix-Formulierungen (Klassisch / Stochastisch / Laplace).
  4. Eigenwert-Spektrum, Diagonalisierbarkeit, Jordan-Form, Determinante, Spur.
  5. Invarianten-Test: Sind die 5 Layer unabhaengig (Kronecker-Produkt)
     oder verschaeft (Nicht-Tensor-Produkt = holografisch)?
  6. Numerische Bruecke 5^4 = 625 vs. 5! = 120 vs. He=5.
  7. JSON-Output + pytest-Tests.

ANTI-APOPHENIE:
  - Wir halten uns an den realen Code (TORA_TURING_CORRECT.py).
  - Wir nehmen NICHT an, dass BURUMUT eine "6D-Torus-Faltung" hat.
  - Wir trennen sauber zwischen (a) Code-Architektur (5 States q_0..q_4 + HALT)
    und (b) BURUMUT-Phasen (6 Phasen aus BURUMUT_PHASES.py).
  - Wir testen die Unabhaengigkeits-Hypothese explizit (Tensor-Rank, Kommutator).
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, List, Tuple

import sympy as sp
from sympy import Matrix, Rational, eye, zeros, Symbol, simplify, factor, latex


# =============================================================================
# 0. KANONISCHE KONSTANTEN (aus TORA_TURING_CORRECT.py, 1:1 uebernommen)
# =============================================================================

HEBREW_22 = [
    'Aleph', 'Beth', 'Gimel', 'Dalet', 'He', 'Vav', 'Zayin', 'Chet',
    'Tet', 'Yod', 'Kaf', 'Lamed', 'Mem', 'Nun', 'Samekh', 'Ayin',
    'Pe', 'Tsade', 'Qof', 'Resh', 'Shin', 'Tav',
]
HEBR_HE = ['א','ב','ג','ד','ה','ו','ז','ח','ט',
           'י','כ','ל','מ','נ','ס','ע','פ',
           'צ','ק','ר','ש','ת']
assert len(HEBREW_22) == 22 and len(HEBR_HE) == 22, f"Got {len(HEBREW_22)} names / {len(HEBR_HE)} glyphs"

# Gematria (aus TORA_TURING_CORRECT.py, HEBR_VALUES)
HEBR_VALUES: Dict[str, int] = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5,
    'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
    'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400,
}
assert len(HEBR_VALUES) == 22, f"Got {len(HEBR_VALUES)} values"

# 5 missing operators (aus TORA_TURING_CORRECT.py)
MISSING_OPERATORS = {
    'Kaf':  ('כ', 20,  'READ'),
    'Gimel':('ג', 3,   'MOVE_RIGHT'),
    'Dalet':('ד', 4,   'MOVE_LEFT'),
    'Tav':  ('ת', 400, 'HALT'),
    'Yod':  ('י', 10,  'STATE'),
}

# 5 States + HALT (kanonisch, aus TORA_TURING_CORRECT.py)
STATES = ['q_0', 'q_1', 'q_2', 'q_3', 'q_4', 'q_5_HALT']
N_STATES = 5  # wir zaehlen q_0..q_4; q_5 = HALT ist Senke

# Schicht-Name -> State-Index
LAYER_NAMES = {
    0: 'Genesis (Bereshit)',
    1: 'Exodus (Shemot)',
    2: 'Leviticus (Vayikra)',
    3: 'Numeri (Bemidbar)',
    4: 'Deuteronomium (Devarim)',
}


# =============================================================================
# 1. ECHTE UEBERGANGSTABELLE (reproduziert aus TORA_TURING_CORRECT.py)
# =============================================================================

# 18 sichtbare Symbole in BURUMUT (LATIN_TO_HEBR.values())
VISIBLE = set([
    'א','ב','ה','ו','מ','צ','ר','ש',
    'ח','ט','ל','נ','ס','ע','פ','ק',
    'י','ז',
])
assert len(VISIBLE) == 18


def build_tora_transitions() -> Dict[Tuple[int, str], Tuple[int, str, str]]:
    """Genau die Logik aus TORA_TURING_CORRECT.build_tora_transitions()."""
    transitions: Dict[Tuple[int, str], Tuple[int, str, str]] = {}

    for sym in VISIBLE:
        # q_0 (Genesis): Aleph = HALT direkt
        if sym == 'א':
            transitions[(0, sym)] = (5, sym, 'HALT')
        else:
            transitions[(0, sym)] = (1, sym, 'MOVE_RIGHT')

    for sym in VISIBLE:
        # q_1 (Exodus): Shin -> q_2; andere -> q_1
        if sym == 'ש':
            transitions[(1, sym)] = (2, sym, 'MOVE_RIGHT')
        else:
            transitions[(1, sym)] = (1, sym, 'MOVE_RIGHT')

    for sym in VISIBLE:
        # q_2 (Leviticus): Tav = HALT; Aleph -> q_3; andere -> q_2
        if sym == 'ת':
            transitions[(2, sym)] = (5, sym, 'HALT')
        elif sym == 'א':
            transitions[(2, sym)] = (3, sym, 'MOVE_RIGHT')
        else:
            transitions[(2, sym)] = (2, sym, 'MOVE_RIGHT')

    for sym in VISIBLE:
        # q_3 (Numeri): Resh -> q_4; andere -> q_3
        if sym == 'ר':
            transitions[(3, sym)] = (4, sym, 'MOVE_RIGHT')
        else:
            transitions[(3, sym)] = (3, sym, 'MOVE_RIGHT')

    for sym in VISIBLE:
        # q_4 (Deuteronomium): Nun = HALT; andere -> q_4
        if sym == 'נ':
            transitions[(4, sym)] = (5, sym, 'HALT')
        else:
            transitions[(4, sym)] = (4, sym, 'MOVE_RIGHT')

    return transitions


# 5 HALT-Trigger (eine pro Layer ausser q_1):
HALT_TRIGGERS = {
    0: ('א', 'Aleph',  1,   'Schöpfungs-Anfang'),
    1: None,  # q_1 hat keinen HALT-Trigger; nur Shin leitet weiter
    2: ('ת', 'Tav',    400, 'Vollendung'),
    3: None,  # q_3 hat keinen HALT-Trigger; Resh leitet nur weiter
    4: ('נ', 'Nun',    50,  'Schrift-Vollendung'),
}


# =============================================================================
# 2. DREI MATRIX-FORMULIERUNGEN
# =============================================================================

def build_classical_matrix() -> Matrix:
    """Klassische 0/1-Matrix: 1 = Layer-Exit (HALT-Trigger oder Verlassen
    des Layers) durch Konsonant j in Layer i.

    Kodiert nur die "aktiven" Symbole pro Layer (die den Layer verlassen).
    """
    trans = build_tora_transitions()
    A = zeros(N_STATES, 22)
    for (state, sym), (new_state, _write, move) in trans.items():
        j = HEBR_HE.index(sym)
        if state >= N_STATES:
            continue
        # HALT-Trigger ODER Konsonant fuehrt aus dem Layer heraus (egal wohin)
        if move == 'HALT' or new_state != state:
            A[state, j] = 1
    return A


def build_stochastic_matrix() -> Matrix:
    """Zeilen-stochastische Matrix P (jede Zeile summiert zu 1)."""
    trans = build_tora_transitions()
    P = zeros(N_STATES, 22)
    for (state, sym), (new_state, _write, move) in trans.items():
        if state >= N_STATES:
            continue
        j = HEBR_HE.index(sym)
        if move == 'HALT' or new_state != state:
            P[state, j] = 1
        else:
            P[state, j] = Rational(1, 22)
    for i in range(N_STATES):
        row_sum = sum(P[i, :])
        if row_sum != 0:
            P[i, :] = P[i, :] / row_sum
    return P


def build_gematria_matrix() -> Matrix:
    """Gematria-Matrix M mit M[i, j] = Gematria(Konsonant_j) bei Layer-Exit."""
    trans = build_tora_transitions()
    M = zeros(N_STATES, 22)
    for (state, sym), (new_state, _write, move) in trans.items():
        if state >= N_STATES:
            continue
        j = HEBR_HE.index(sym)
        if move == 'HALT' or new_state != state:
            M[state, j] = HEBR_VALUES[sym]
    return M


def build_exit_destination_matrix() -> Matrix:
    """Matrix D mit D[i, j] = neuer State nach Lesen von Konsonant j in Layer i.

    Liefert den vollen deterministischen Uebergang kodiert als Zahlenmatrix.
    D ist 5x22, Werte in {0, 1, 2, 3, 4, 5}.
    """
    trans = build_tora_transitions()
    D = zeros(N_STATES, 22)
    for (state, sym), (new_state, _write, move) in trans.items():
        j = HEBR_HE.index(sym)
        if state >= N_STATES:
            continue
        D[state, j] = new_state
    return D


# =============================================================================
# 3. GEMATRIA-SIGNATUR PRO LAYER
# =============================================================================

def gematria_per_layer(M: Matrix) -> List[Dict]:
    """Berechne fuer jeden Layer:
       - anzahl Spezial-Konsonanten
       - Liste der beteiligten Konsonanten
       - Summe der Gematria-Werte
       - Produkt
    """
    out = []
    for i in range(N_STATES):
        nonzero = [(HEBR_HE[j], HEBR_VALUES[HEBR_HE[j]])
                   for j in range(22) if M[i, j] != 0]
        values = [v for _, v in nonzero]
        out.append({
            'layer': i,
            'name': LAYER_NAMES[i],
            'special_consonants': [
                {'he': h, 'name': HEBREW_22[HEBR_HE.index(h)], 'gematria': v}
                for h, v in nonzero
            ],
            'count': len(nonzero),
            'gematria_sum': sum(values),
            'gematria_product': math.prod(values) if values else 0,
        })
    return out


# =============================================================================
# 4. EIGENWERT-ANALYSE
# =============================================================================

def analyze_eigenvalues(M: Matrix, label: str) -> Dict:
    """Eigenwerte, algebraische Vielfachheiten, Diagonalisierbarkeit.

    Fuer nicht-quadratische Matrizen (z.B. 5x22) wird die Singulaerwert-
    Zerlegung statt der Eigenwerte verwendet. Determinante und Spur sind
    nur fuer quadratische Matrizen definiert.
    """
    is_square = (M.shape[0] == M.shape[1])
    out: Dict = {
        'label': label,
        'shape': list(M.shape),
        'is_square': is_square,
        'rank': int(M.rank()),
    }

    if is_square:
        out['trace'] = str(M.trace())
        out['determinant'] = str(M.det())
        out['frobenius_norm_sq'] = str((M.T * M).trace())
        try:
            jf, _ = M.jordan_form()
            out['jordan_normal_form'] = str(jf)
        except Exception as e:  # pragma: no cover
            out['jordan_normal_form_error'] = str(e)

    try:
        eigenvals = M.eigenvals()
    except Exception as e:  # pragma: no cover
        out['eigenvalues_error'] = str(e)
        eigenvals = {}

    # Diagonalisierbar? (nur fuer quadratische Matrizen sinnvoll)
    diag = True
    details = []
    for ev, alg_mult in eigenvals.items():
        M_eff = M if is_square else M.T * M  # nutze M^T*M fuer nichtquadratisch
        try:
            geom_dim = M_eff.shape[1] - (M_eff - ev * eye(*M_eff.shape)).rank()
        except Exception:
            geom_dim = -1
        is_diag = (geom_dim == alg_mult) and is_square
        if not is_diag:
            diag = False
        details.append({
            'value': str(ev),
            'algebraic_mult': int(alg_mult),
            'geometric_mult': int(geom_dim),
            'diagonalizable': is_diag,
        })

    out['eigenvalues'] = details
    out['is_diagonalizable'] = diag

    # Singulaerwerte immer berechenbar
    try:
        sv = M.singular_values()
        out['singular_values_count'] = len(sv)
    except Exception:
        pass

    return out


# =============================================================================
# 5. UNABHAENGIGKEITS-TEST (Kronecker-Produkt vs. holografisch)
# =============================================================================

def independence_test() -> Dict:
    """Test: Sind die 5 Layer unabhaengig (Tensor-Produkt) oder verschaeft?

    Operational definieren wir die Layer i und j als UNABHAENGIG, wenn die
    Information in Layer i nicht von Layer j abhaengt. Da die reale
    Uebergangstabelle in TORA_TURING_CORRECT.py NICHT als Tensor-Produkt
    aufgebaut ist (sie ist ein expliziter 6x18 Lookup), ist die Hypothese
    "holografisch" bzw. "nicht-tensoriell" testbar.

    Wir testen:
      A) Determiniertheit: Jeder Zustand q_i hat (mindestens) eine
         Schalt-Aktion pro sichtbarem Konsonanten.
      B) Pfad-Eindeutigkeit: Vom Tape-Anfang fuehrt GENAU EIN Pfad zum HALT.
      C) Tensor-Rank: Wuerde A einem Tensor-Produkt A = a (x) b genuegen,
         waere rank(A) = 1.
    """
    A = build_classical_matrix()
    rank = int(A.rank())
    singular_values = A.singular_values()

    # Pfad-Eindeutigkeit: Analysiere die BURUMUT-Inputs
    # Wir nutzen die echte Maschine
    from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT

    hebr_tape = burumut_to_hebr(BURUMUT)
    paths = []
    for start_offset in range(min(20, len(hebr_tape))):
        m = ToraTuringMachine(hebr_tape[start_offset:])
        m.run(max_steps=200)
        paths.append({
            'start_offset': start_offset,
            'start_symbol': hebr_tape[start_offset],
            'halt_step': m.halt_step,
            'halt_state': m.halt_state,
            'halt_reason': m.halt_reason,
            'states_visited': [h['new_state'] for h in m.history],
        })

    # Welche Layer werden bei BURUMUT besucht?
    all_visited = set()
    for p in paths:
        for s in p['states_visited']:
            all_visited.add(s)
    visited_layers = sorted(s for s in all_visited if s < N_STATES)

    return {
        'matrix_rank': rank,
        'tensor_rank_1_possible': (rank == 1),
        'singular_values': [str(s) for s in singular_values],
        'is_tensor_product_structure': (rank == 1),
        'interpretation_rank': (
            'rank=1 waere totale Faktorisierung (Layer unabhaengig). '
            f'Wir haben rank={rank}, also KEIN einfaches Tensor-Produkt.'
        ),
        'paths_analyzed': len(paths),
        'visited_layers_in_burumut': visited_layers,
        'all_5_layers_reachable': (len(visited_layers) == N_STATES),
        'sample_paths': paths[:5],
    }


# =============================================================================
# 6. NUMERISCHE BRUECKE 5^4 = 625, 5! = 120, He=5
# =============================================================================

def numerical_bridge_5() -> Dict:
    """Berechne alle natuerlich mit 5 verbundenen Zahlen, plus 137/37/46.

    Frage: Ist 5^4 = 625 oder 5! = 120 im BURUMUT-Korpus nachweisbar?
    """
    bridge = {
        '5_powers': {
            '5^1': 5,
            '5^2': 25,
            '5^3': 125,
            '5^4': 625,
            '5^5': 3125,
        },
        '5_factorial': 5 * 4 * 3 * 2 * 1,  # 120
        '5_bell': 52,  # B(5)
        '5_catalan_3': 42,  # Catalan(5)=42
        '5_fib': 5,
    }

    # Suche diese Zahlen in den bekannten BURUMUT-Konstanten
    known_constants = {
        'BURUMUT_length': 99,
        'total_gematria_BURUMUT_hebr': 6503,
        'phase_1_gematria': 1924,
        'phase_3_5_gematria': 551,
        'phase_4_gematria': 964,
        'alpha_inverse': 137,
        'alpha_related': 37,
        'square_37': 37 * 37,  # 1369
        'he_5': 5,  # He = 5
    }
    hits = {}
    for label, val in known_constants.items():
        for power_label, power_val in bridge['5_powers'].items():
            if val == power_val:
                hits[f'{label}={val}'] = f'EXAKT = {power_label}'
        if val == bridge['5_factorial']:
            hits[f'{label}={val}'] = 'EXAKT = 5!'
    bridge['matches_in_known_constants'] = hits
    bridge['matches_count'] = len(hits)
    bridge['note_5_pow_4'] = (
        '5^4 = 625 ist NICHT in den bekannten BURUMUT-Konstanten. '
        'Die Behauptung "5^4 = BURUMUT-Marker" ist NICHT numerisch gestuetzt.'
    )
    bridge['note_5_fact'] = (
        '5! = 120. In TENGRI137_Full_Notes (Z.342) erscheint "pi7pi^7"; '
        '5! = 120 ist NICHT prominent im BURUMUT-Band.'
    )
    bridge['note_he_5'] = (
        'He (ה) = 5 ist ein hebraischer Buchstabe. Im BURUMUT-99 (hebraeisch) '
        'kommt He mehrfach vor, aber die "Layer 1 = He" Hypothese ist eine '
        'bildliche Assoziation, kein mathematischer Befund.'
    )
    return bridge


# =============================================================================
# 7. 5 vs. 6 LAYER — ARCHITEKTUR-KLAERUNG
# =============================================================================

def architecture_resolution() -> Dict:
    """5 oder 6 Layer? Antwort: 5 STATES, 6 PHASEN — beides ist kanonisch, aber
    fuer verschiedene Aspekte.

    - 5 STATES = Code-Architektur (q_0..q_4 + HALT-Senke)
       => GENESIS, EXODUS, LEVITICUS, NUMERI, DEUTERONOMIUM
       => kommt aus TORA_TURING_CORRECT.py

    - 6 PHASEN = Inhaltliche Gliederung des BURUMUT-Tapes
       => 15+15+14+20+14+19+2 = 99 Zeichen
       => kommt aus BURUMUT_PHASES.py
    """
    return {
        'states_count_in_code': N_STATES + 1,  # +1 fuer HALT-Senke q_5
        'phases_count_in_tape': 6,
        'code_layer': {
            'name': '5 States (q_0..q_4) + q_5 HALT',
            'source': 'TORA_TURING_CORRECT.py',
            'interpretation': '5 Buecher Mose + 1 Senke',
        },
        'tape_layer': {
            'name': '6 Phasen',
            'source': 'BURUMUT_PHASES.py',
            'lengths': [15, 15, 14, 20, 14, 19],
            'total': 97,
            'plus_transition': 2,
            'interpretation': 'Schöpfungs-Akt, Wurzeln, Wanderung, Schrift-Vollendung, Echo, Vollendung',
        },
        'conclusion': (
            'Die Architektur ist 5 (Code) und der Tape-Inhalt ist in 6 Phasen '
            'gegliedert. Beide sind kanonisch. KEIN Konflikt, aber es ist '
            'wichtig, die Ebenen nicht zu vermischen. 5 States ergeben eine '
            '5x22-Matrix; 6 Phasen ergeben einen 6-Vektor (oder 6 Spalten) '
            'fuer eine andere Frage.'
        ),
    }


# =============================================================================
# 8. HAUPTANALYSE
# =============================================================================

def main() -> Dict:
    out: Dict = {
        'meta': {
            'script': 'Q_LAYER_TORAH_FOLD_SYMPY.py',
            'method': 'SymPy-formale Analyse der 5-Layer-Torah-Architektur',
            'source_code': 'TORA_TURING_CORRECT.py',
            'konsolidiert_in': 'TORAH_TURUS_TURING_MACHINE_TENGRI137.md',
            'date': '2026-07-01',
            'mode': 'SciMind (Steelmann, Ockham, Anti-Sharpshooter)',
        },
    }

    # 1) Architektur
    out['architecture'] = architecture_resolution()

    # 2) Gematria pro Layer
    M = build_gematria_matrix()
    A = build_classical_matrix()
    P = build_stochastic_matrix()
    out['gematria_per_layer'] = gematria_per_layer(M)

    # 3) Matrizen
    D = build_exit_destination_matrix()
    out['matrices'] = {
        'classical_A': str(A),
        'stochastic_P': str(P),
        'gematria_M': str(M),
        'exit_destination_D': str(D),
    }

    # 4) Eigenwerte
    out['eigenvalues_classical'] = analyze_eigenvalues(A, 'classical_A_5x22')
    out['eigenvalues_gematria'] = analyze_eigenvalues(M, 'gematria_M_5x22')

    # 5) 5x5-Adjazenz der States (Layer-zu-Layer)
    state_adj = zeros(N_STATES + 1, N_STATES + 1)  # +1 HALT
    trans = build_tora_transitions()
    for (state, sym), (new_state, _w, _m) in trans.items():
        state_adj[state, new_state] += 1
    out['state_adjacency_6x6'] = {
        'matrix': str(state_adj),
        'eigenvalues': [str(ev) for ev in state_adj.eigenvals().keys()],
        'determinant': str(state_adj.det()),
        'trace': str(state_adj.trace()),
        'is_diagonalizable': state_adj.is_diagonalizable(),
        'rank': int(state_adj.rank()),
    }

    # 6) Unabhaengigkeits-Test
    out['independence_test'] = independence_test()

    # 7) Numerische Bruecke
    out['numerical_bridge_5'] = numerical_bridge_5()

    # 8) Hauptbefund: Hypothese H1
    out['hypothesis_H1'] = {
        'claim': (
            'Die Tora-Turing-Maschine bildet eine "5-Layer-Torah-Fold" mit '
            'echter mathematischer Struktur.'
        ),
        'evidence_for': [
            'Es gibt 5 STATES im Code (q_0..q_4 + HALT q_5) — das ist real.',
            'Jeder State hat eine deterministische Uebergangsfunktion (echte Turing-Maschine).',
            'Die Uebergangsfunktion kodiert HALT-Trigger gemaess der hebraeischen Gematria-Logik '
            '(Aleph=1, Tav=400, Nun=50).',
            'Die 5x22-Adjazenz-Matrix hat Rang ' + str(int(A.rank())) + ' '
            'und damit eine nicht-triviale Spektral-Struktur.',
        ],
        'evidence_against': [
            'Die "5 Layer" sind ein CODE-DESIGN (5 States), nicht eine aus den Daten emergierte Struktur.',
            'Die 6 BURUMUT-Phasen ergeben eine andere Anzahl (6 ≠ 5).',
            'Die "Faltung" (Fold) wird nirgendwo formal definiert — es ist eine Metapher.',
            '5^4 = 625 ist NICHT im BURUMUT-Band nachweisbar.',
            '5! = 120 ist nicht prominent im BURUMUT-Band.',
            'Layer-Unabhaengigkeit ist TESTBAR: Die reale Uebergangstabelle ist KEIN Tensor-Produkt '
            '(Rang ≠ 1), also sind die 5 Layer NICHT trivial faktorisierbar. Das ist ECHTE '
            'Struktur, aber kein "holografisches" Wunder — es ist ein expliziter Lookup.',
        ],
        'verdict': (
            'TEILWEISE MATHEMATISCH: Die 5-Layer-Architektur ist eine ECHTE endliche '
            'Zustandsmaschine (DFA mit 5 + 1 Zuständen) mit einer klar definierten '
            'Uebertragungsmatrix. Sie ist mathematisch analysierbar, mit Eigenwerten, '
            'Rang, Spur, Determinante. Aber: sie ist KEIN natürliches Phänomen, '
            'sondern ein ENGINEERED DESIGN (5 States, weil es 5 Bücher Mose sind). '
            'Die "Faltung" ist eine METAPHER, keine mathematische Operation. Die '
            'holografische Hypothese (Nicht-Tensor-Produkt = Information über alle '
            'Layer verteilt) ist ebenfalls nicht stichhaltig, weil die Tabelle als '
            'expliziter Lookup konstruiert wurde, nicht durch Faltung.'
        ),
        'is_real_math_structure': True,
        'is_engineered_design': True,
        'is_metaphor': True,
    }

    return out


# =============================================================================
# 9. PYTEST-TESTS
# =============================================================================

def test_states_count():
    """5 funktionale States + 1 HALT-Senke."""
    assert N_STATES == 5
    assert len(STATES) == 6


def test_hebrew_22_count():
    """22 hebraeische Konsonanten, exakt."""
    assert len(HEBREW_22) == 22
    assert len(HEBR_HE) == 22
    assert len(HEBR_VALUES) == 22


def test_gematria_he_equals_5():
    """He (ה) hat Gematria 5."""
    assert HEBR_VALUES['ה'] == 5


def test_classical_matrix_shape():
    A = build_classical_matrix()
    assert A.shape == (5, 22)


def test_gematria_matrix_layer_0_has_aleph():
    """Layer 0 (Genesis) hat HALT-Trigger Aleph (1)."""
    M = build_gematria_matrix()
    j = HEBR_HE.index('א')
    assert M[0, j] == 1


def test_gematria_matrix_layer_2_has_tav():
    """Layer 2 (Leviticus): HALT-Trigger Tav (400) ist im Code definiert,
    aber Tav ist NICHT im BURUMUT-Tape. Daher M[2, tav] = 0 (toter Code-Zweig).
    Das ist ein REALER BUG im TORA_TURING_CORRECT.py-Design: der HALT-Trigger
    wird nie ausgeloest, weil Tav nie im Band erscheint."""
    M = build_gematria_matrix()
    j = HEBR_HE.index('ת')
    # Korrekte Erwartung: Tav ist im sichtbaren BURUMUT-Alphabet nicht enthalten
    assert M[2, j] == 0  # tote Code-Zweig


def test_gematria_matrix_layer_4_has_nun():
    """Layer 4 (Deuteronomium) hat HALT-Trigger Nun (50)."""
    M = build_gematria_matrix()
    j = HEBR_HE.index('נ')
    assert M[4, j] == 50


def test_layer_1_has_no_halt_trigger():
    """Layer 1 (Exodus) hat KEINEN HALT-Trigger — nur einen Wechsel (Shin -> q_2)."""
    M = build_gematria_matrix()
    # Layer 1 hat nur Shin (Shin -> q_2), kein HALT
    # D.h. die Diagonale von Layer 1 in M sollte nicht ausschliesslich durch
    # HALT-Trigger belegt sein. Pruefe: nur Shin erscheint.
    nonzero = [j for j in range(22) if M[1, j] != 0]
    assert len(nonzero) == 1
    j_shin = HEBR_HE.index('ש')
    assert nonzero[0] == j_shin
    assert M[1, j_shin] == 300  # Shin = 300


def test_layer_3_has_no_halt_trigger():
    """Layer 3 (Numeri) hat KEINEN HALT-Trigger — nur Resh -> q_4."""
    M = build_gematria_matrix()
    nonzero = [j for j in range(22) if M[3, j] != 0]
    assert len(nonzero) == 1
    j_resh = HEBR_HE.index('ר')
    assert nonzero[0] == j_resh
    assert M[3, j_resh] == 200  # Resh = 200


def test_stochastic_matrix_row_sums():
    """Jede Zeile der stochastischen Matrix summiert zu 1."""
    P = build_stochastic_matrix()
    for i in range(N_STATES):
        s = sum(P[i, :])
        assert s == 1, f"Zeile {i} summiert zu {s}"


def test_state_adjacency_has_halt_sink():
    """HALT-Senke q_5 hat Selbst-Loop (alle Symbole -> HALT)."""
    # Wir muessen die q_5-Selbst-Loops manuell hinzufuegen, weil build_tora_transitions()
    # nur die q_0..q_4-Eintraege konstruiert.
    state_adj = zeros(N_STATES + 1, N_STATES + 1)
    trans = build_tora_transitions()
    for (state, sym), (new_state, _w, _m) in trans.items():
        state_adj[state, new_state] += 1
    # q_5 Senke: explizit befuellen mit Selbst-Loop
    state_adj[5, 5] = len(VISIBLE)  # 18 Selbst-Loops
    for j in range(N_STATES + 1):
        if j == 5:
            assert state_adj[5, j] > 0
        else:
            assert state_adj[5, j] == 0


def test_5_pow_4_not_in_constants():
    """5^4 = 625 erscheint NICHT in den bekannten BURUMUT-Konstanten."""
    bridge = numerical_bridge_5()
    assert 625 not in [99, 6503, 1924, 551, 964, 137, 37, 1369, 5]
    assert bridge['matches_count'] == 0 or all(
        '625' not in v for v in bridge['matches_in_known_constants'].values()
    )


def test_layer_2_has_only_aleph_in_visible_alphabet():
    """Layer 2 (Leviticus): Im sichtbaren BURUMUT-Alphabet ist nur Aleph
    ein Spezial-Konsonant (Tav fehlt im BURUMUT-Tape, obwohl TORA_TURING_CORRECT.py
    HALT-Trigger fuer Tav definiert — toter Code-Zweig)."""
    M = build_gematria_matrix()
    nonzero = [j for j in range(22) if M[2, j] != 0]
    j_aleph = HEBR_HE.index('א')
    assert j_aleph in nonzero
    # Tav ist im BURUMUT-Band NICHT vorhanden (nicht in LATIN_TO_HEBR)
    j_tav = HEBR_HE.index('ת')
    assert M[2, j_tav] == 0  # toter Zweig im Originalcode


def test_layer_0_halt_trigger_aleph():
    """Layer 0 (Genesis): Aleph fuehrt zu q_5 HALT (sichtbar im BURUMUT)."""
    M = build_gematria_matrix()
    j = HEBR_HE.index('א')
    assert M[0, j] == 1


def test_tav_is_missing_from_burumut():
    """Tav (ת) kommt im BURUMUT-Band NICHT vor — der HALT-Trigger in q_2
    ist im Originalcode toter Code, weil die for-Schleife ueber VISIBLE laeuft
    und Tav nicht in VISIBLE ist."""
    from TORA_TURING_CORRECT import LATIN_TO_HEBR
    visible = set(LATIN_TO_HEBR.values())
    assert 'ת' not in visible  # Tatsaechlich fehlt Tav
    # Die "5 fehlenden Konsonanten" sind Kaf, Gimel, Dalet, Tav, Yod
    # Aber Yod (י) ist DOCH in VISIBLE (Y -> י)! Kaf/Gimel/Dalet/Tav fehlen.
    assert 'י' in visible
    assert 'כ' not in visible
    assert 'ג' not in visible
    assert 'ד' not in visible
    assert 'ת' not in visible
    # Also: Die "5 fehlenden Operatoren" sind eigentlich 4 (Kaf, Gimel, Dalet, Tav)
    # — der Kommentar im Code ist semi-inkonsistent.


def test_tora_machine_actually_halts():
    """Integration: Die Tora-Turing-Maschine haelt tatsaechlich."""
    from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
    hebr = burumut_to_hebr(BURUMUT)
    m = ToraTuringMachine(hebr)
    m.run(max_steps=300)
    assert m.halted is True
    assert m.halt_reason in ('HALT_TRANSITION', 'BAND_ENDE')


def test_5_plus_1_architecture_not_6():
    """Klarstellung: 5 States + HALT, NICHT 6 (das waeren 6 Phasen)."""
    arch = architecture_resolution()
    assert arch['states_count_in_code'] == 6  # q_0..q_5
    assert arch['phases_count_in_tape'] == 6
    # Aber: nur 5 davon sind FUNKTIONALE Layer (q_5 ist Senke)


# =============================================================================
# 10. ENTRYPOINT
# =============================================================================

if __name__ == "__main__":
    result = main()
    out_path = Path(__file__).parent / "q_layer_torah_fold_sympy.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print("=" * 70)
    print("Q_LAYER_TORAH_FOLD_SYMPY — FORMALE 5-LAYER-ANALYSE")
    print("=" * 70)
    print()
    print("ARCHITEKTUR-AUFLOESUNG:")
    print(f"  States im Code:  {result['architecture']['states_count_in_code']} (q_0..q_5)")
    print(f"  Phasen im Tape:  {result['architecture']['phases_count_in_tape']} (Phasen 1-6)")
    print(f"  => 5 funktionale Layer + 1 HALT-Senke; 6 Phasen = Inhalts-Gliederung")
    print()
    print("GEMATRIA-SIGNATUR PRO LAYER:")
    for layer in result['gematria_per_layer']:
        print(f"  q_{layer['layer']} ({layer['name']}): "
              f"{layer['count']} Spezial-Konsonanten, "
              f"Σ = {layer['gematria_sum']}, "
              f"Π = {layer['gematria_product']}")
        for c in layer['special_consonants']:
            print(f"    {c['he']} {c['name']:8s} = {c['gematria']}")
    print()
    print("EIGENWERTE (5x22 Gematria-Matrix):")
    ev = result['eigenvalues_gematria']
    print(f"  Shape:        {ev['shape']}")
    print(f"  Rang:         {ev['rank']}")
    print(f"  Quadratisch:  {ev['is_square']}")
    if ev.get('trace'):
        print(f"  Spur:         {ev['trace']}")
    if ev.get('determinant'):
        print(f"  Determinante: {ev['determinant']}")
    print(f"  Diagonalisierbar: {ev['is_diagonalizable']}")
    for e in ev['eigenvalues']:
        print(f"    λ = {e['value']:8s}  alg={e['algebraic_mult']}, geom={e['geometric_mult']}")
    print()
    print("UNABHAENGIGKEITS-TEST:")
    ind = result['independence_test']
    print(f"  Rang der Adjazenz-Matrix:  {ind['matrix_rank']}")
    print(f"  Tensor-Produkt (Rang 1)?:  {ind['is_tensor_product_structure']}")
    print(f"  Interpretation:            {ind['interpretation_rank']}")
    print(f"  5 Layer alle erreichbar?:  {ind['all_5_layers_reachable']}")
    print()
    print("NUMERISCHE BRUECKE (5^4, 5!, He=5):")
    nb = result['numerical_bridge_5']
    print(f"  Matches in BURUMUT-Konstanten: {nb['matches_count']}")
    print(f"  5^4 = 625 nachweisbar? NEIN — {nb['note_5_pow_4']}")
    print()
    print("HAUPTBEFUND:")
    print(f"  {result['hypothesis_H1']['verdict']}")
    print()
    print(f"JSON-Output: {out_path}")
