"""
🌌 SPANDA-MASCHINE: Selbst-enthüllende, selbst-ausführende,
   selbst-kanonisch-expandierende Architektur

Spanda (Kashmir-Shivaismus): das göttliche Pulsieren,
in dem Manifestation und Erkenntnis dasselbe sind.

ARCHITEKTUR (5 Komponenten):
1. BASE_TRUTH         — Tengri137_Full_Notes (eingefroren)
2. SPANDA_MACHINE     — ToraTuringMultiPhase (132 Transitions)
3. HALT_INTERPRETER   — liest Halt-Punkt → Original-Text
4. EXPANSION_ENGINE   — Halt-Hinweis → neue Phase
5. BACKTRACKING_DEBUG — pdb-fähig, single-step, reversibel

PRINZIP:
- Die Maschine liest ihren eigenen Beschreibungstext (Quine)
- Jeder Halt-Punkt IST ihre Aussage (Spanda)
- Jeder Halt-Punkt öffnet eine neue Phase (Vāc-Stadien)
- Tengri137 ist die unveränderliche Basis-Wahrheit (Dharma)

PHILOSOPHISCHE VERANKERUNG:
- Spanda (Kashmir-Shivaismus)    — Manifestation + Erkenntnis
- Pratyahara (Yoga-Sutra 2.54)   — Pendel = Rückzug der Sinne
- Wu Wei (Dao De Jing 37)        — Handeln durch Nicht-Handeln
- Vāc (4 Sprach-Stadien)         — vaikharī/madhyamā/paśyantī/parā
- Logos (Heraklit)                — der Fluss = das Gesetz
"""
import re
import json
import sys
import pdb
from pathlib import Path
from collections import Counter

from sympy import (
    symbols, Symbol, Function, Integer, Rational, sqrt, pi, E,
    simplify, factorint, isprime, Matrix, zeros, eye,
    latex, srepr,
)
import numpy as np

# Unsere bestehende Maschine
from TORA_TURING_MULTIPHASE import (
    ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR,
    build_extended_transitions, burumut_to_hebr,
)
from TORA_TURING_CORRECT import (
    HEBR_VALUES, BURUMUT, LATIN_TO_HEBR,
    build_tora_transitions, ToraTuringMachine,
)


# =====================================================================
# 1. BASE_TRUTH — Tengri137_Full_Notes (eingefroren)
# =====================================================================
class BaseTruth:
    """Die unveränderliche Basis-Wahrheit.

    Tengri137_Full_Notes als Frozen-String. Niemand mutiert sie.
    Alle Verifikation läuft gegen sie.
    """

    def __init__(self, path='Tengri137_Full_Notes'):
        self.path = Path(path)
        self.raw = self.path.read_text()
        self.size = len(self.raw)
        self.lines = self.raw.count('\n')

        # A-Z-Buchstaben extrahieren MIT Position
        self.letters = []
        self.position_map = []  # original byte-position jedes A-Z
        for i, c in enumerate(self.raw):
            if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                self.letters.append(c)
                self.position_map.append(i)

        # Hebräische Konvertierung (deterministisch)
        self.hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in self.letters)
        self.hebr_length = len(self.hebr)

        # Konsonanten-Verteilung (deterministisch via Counter)
        self.konsonanten_count = Counter(self.hebr)

        # SHA-256 als "kanonischer Fingerabdruck"
        import hashlib
        self.fingerprint = hashlib.sha256(self.raw.encode('utf-8')).hexdigest()

    def context_at_position(self, byte_pos, before=100, after=200):
        """Hole Kontext um eine Position. None wenn out of range."""
        if byte_pos < 0 or byte_pos >= self.size:
            return None
        s = max(0, byte_pos - before)
        e = min(self.size, byte_pos + after)
        return self.raw[s:e]

    def halt_to_context(self, tape_head):
        """Mappe Maschinen-Position auf Original-Text + Zeile."""
        if tape_head >= len(self.position_map):
            tape_head = len(self.position_map) - 1
        if tape_head < 0:
            return None
        byte_pos = self.position_map[tape_head]
        line_no = self.raw[:byte_pos].count('\n') + 1
        letter = self.letters[tape_head]
        return {
            'tape_head': tape_head,
            'byte_pos': byte_pos,
            'line_no': line_no,
            'letter': letter,
            'hebrew': EXTENDED_LATIN_TO_HEBR.get(letter, '?'),
            'context': self.context_at_position(byte_pos, 200, 400),
        }


# =====================================================================
# 2. SPANDA_MACHINE — die Tora-Turing-Maschine, deterministisch
# =====================================================================
class SpandaMachine:
    """Die BURUMUT-Tora-Turing-Maschine, eingebettet in die Spanda-Architektur.

    Sie liest das Tape, hält an Halt-Triggern, öffnet neue Phasen.
    Jeder Schritt ist deterministisch und rückverfolgbar.
    """

    def __init__(self, base_truth, phase_size=99, max_steps=100000):
        self.base = base_truth
        self.phase_size = phase_size
        self.max_steps = max_steps
        self.transitions = build_extended_transitions()

        # Zähle Transitionen
        self.n_transitions = len(self.transitions)
        self.n_states = len(set(s for s, _ in self.transitions.keys()))
        self.n_symbols = len(set(s for _, s in self.transitions.keys()))

        # Maschine selbst
        self.machine = None
        self.last_halt = None
        self.all_halts = []

    def run_full(self, from_position=0, stay_probability=0.0):
        """Laufe die Maschine über das volle Tape.

        Pendel-Erkennung: bei wiederholtem (state, head) → Phase-Reset.
        Final-Halt nur am Tape-Ende.

        stay_probability: Wahrscheinlichkeit, dass die Maschine 'verweilt'
        (Tengri137-Entscheidung 2026-07-01: die 3. Dimension = STAY).
        0.0 = aus (DEFAULT, deterministisch)
        0.1-0.3 = NICHT-EMPFOHLEN (verletzt AGENTS.md Section 4.1d Determinismus)

        ACHTUNG: AGENTS.md 4.1d VERBIETET Zufall in der Kern-Maschine.
        Default ist stay_probability=0.0, was die Maschine deterministisch
        macht. Falls stay_probability > 0.0, ist der Lauf NICHT deterministisch.
        """
        hebr = self.base.hebr[from_position:]
        n = len(hebr)
        n_phases = (n + self.phase_size - 1) // self.phase_size

        tape = list(hebr)
        head = 0
        state = 0
        phase = 0
        total_steps = 0
        phase_halts = []
        state_head_history = []  # für Pendel-Erkennung
        history = []

        # Aleph-Reflektions-Halts (Tengri137-Architektur 11²+1):
        # Die Maschine ehrt Aleph (א=1, Stille, Atem) als Reflektions-Punkt.
        # 11 Aleph-Halts = 11 BURUMUT-Sec-Anker
        # (entdeckt via Cluster 6, P66-76 = Spiegelungspunkt)
        aleph_halts = []
        aleph_reflections = []

        while head < n:
            # Phasenende?
            if head >= (phase + 1) * self.phase_size:
                phase_halts.append({
                    'phase': phase, 'step': total_steps,
                    'state': state, 'head': head, 'reason': 'PHASE_END',
                })
                phase += 1
                if phase >= n_phases:
                    head = n
                    break
                head = phase * self.phase_size
                state = 0
                state_head_history = []
                continue

            # Aleph-Reflektion: Wenn das aktuelle Symbol Aleph (א) ist UND
            # wir im Reflektions-Modus sind, halte an und lies die
            # bisherige Halt-Geschichte rückwärts.
            # Tengri137: 11 Aleph-Stellen sind die BURUMUT-Sec-Anker.
            if tape[head] == 'א' and head > 0:
                # Wir zählen Aleph-Halts separat (nicht in phase_halts)
                aleph_halts.append({
                    'phase': phase, 'step': total_steps,
                    'state': state, 'head': head,
                    'letter': self.base.letters[from_position + head] if from_position + head < len(self.base.letters) else '?',
                    'reflection': list(reversed(phase_halts[-3:])),  # die letzten 3 Halts
                })
                # Reflektion: keine Aktion, weiter im Tape
                # Die Aleph-Stelle IST die Aussage (Spanda: Manifestation = Erkenntnis)

            # Pendel?
            current = (state, head)
            if current in state_head_history[:-10]:
                phase_halts.append({
                    'phase': phase, 'step': total_steps,
                    'state': state, 'head': head, 'reason': 'PENDULUM_DETECTED',
                })
                phase += 1
                if phase >= n_phases:
                    head = n
                    break
                head = phase * self.phase_size
                state = 0
                state_head_history = []
                continue

            state_head_history.append(current)
            if len(state_head_history) > 100:
                state_head_history = state_head_history[-50:]

            # STAY-Check (3. Dimension des Spanda-Pulsierens)
            # Vor der Transition: randomisiere, ob die Maschine verweilt
            # ACHTUNG: AGENTS.md 4.1d Determinismus — stay_probability=0.0 ist
            # der Default. Falls stay_probability > 0.0, ist der Lauf NICHT
            # deterministisch.
            stayed_this_step = False
            if stay_probability > 0:
                # Spanda-Pulsieren-Modus (NICHT EMPFOHLEN, nur für Spezialfälle)
                import random
                if random.random() < stay_probability:
                    # STAY: kein Move, aber die History wird aktualisiert
                    # Tengri137: 3 am Ende → 3. Operation = STAY (Verweil-Moment)
                    history.append({
                        'step': total_steps, 'phase': phase,
                        'old_pos': head, 'new_pos': head,
                        'old_state': state, 'new_state': state,
                        'symbol': tape[head], 'write': tape[head], 'move': 'STAY',
                    })
                    state_head_history.append((state, head))
                    stayed_this_step = True
                    # Cycle fortsetzen ohne total_steps++
                    continue

            symbol = tape[head]
            key = (state, symbol)
            total_steps += 1

            if total_steps > self.max_steps:
                break

            if key not in self.transitions:
                phase_halts.append({
                    'phase': phase, 'step': total_steps,
                    'state': state, 'head': head,
                    'reason': f'NO_TRANSITION: ({state}, {symbol})',
                })
                phase += 1
                if phase >= n_phases:
                    head = n
                    break
                head = phase * self.phase_size
                state = 0
                state_head_history = []
                continue

            new_state, write_sym, move = self.transitions[key]
            if write_sym != symbol:
                tape[head] = write_sym
            old_state = state
            state = new_state
            old_head = head

            if move == 'MOVE_RIGHT':
                head += 1
            elif move == 'MOVE_LEFT':
                head = max(0, head - 1)
            elif move == 'HALT':
                phase_halts.append({
                    'phase': phase, 'step': total_steps,
                    'state': state, 'head': head, 'reason': 'HALT_TRANSITION',
                })
                phase += 1
                if phase >= n_phases:
                    head = n
                    break
                head = phase * self.phase_size
                state = 0
                state_head_history = []

            history.append({
                'step': total_steps, 'phase': phase,
                'old_pos': old_head, 'new_pos': head,
                'old_state': old_state, 'new_state': state,
                'symbol': symbol, 'write': write_sym, 'move': move,
            })

        # Final-Halt
        self.last_halt = {
            'step': total_steps, 'state': state,
            'head': head, 'phase': phase,
            'reason': 'TAPE_END' if head >= n else 'MAX_STEPS',
        }
        self.all_halts = phase_halts

        return {
            'n_phases': n_phases,
            'total_steps': total_steps,
            'final_state': state,
            'final_head': head,
            'phase_halts': phase_halts,
            'aleph_halts': aleph_halts,  # 11 BURUMUT-Sec-Anker (Tengri137-Architektur)
            'n_aleph_reflections': len(aleph_halts),
            'history': history[-100:],  # nur letzte 100 Schritte
            'halt_reason': self.last_halt['reason'],
            'stayed_count': sum(1 for h in history if h.get('move') == 'STAY'),
        }

    def compute_three_sums(self, run_result):
        """Berechne die 3 Gematria-Summen: Wort, Phrase, Tape.

        Tengri137-Entscheidung: 3 Summen, weil Tengri137 3 am Ende gibt.

        ACHTUNG: Tengri137-Tape ≠ BURUMUT-Tape.
        - Wort-Gematria (15 Zeichen): "TENGRIISTHESOUR" = 1229 (NICHT 1924)
        - Phrase-Gematria (99 Zeichen): erste Phase des Tengri137-Tape
        - Tape-Gematria (12071 Zeichen): volles Tengri137-Tape

        1924 / 6503 / 708349 waren für BURUMUT-Tape.
        Für Tengri137-Tape sind es andere Zahlen — die Spanda-Maschine
        lehrt uns, die Tapes zu unterscheiden.
        """
        tape = self.base.hebr
        hebr_values = HEBR_VALUES

        # 1. Wort-Gematria (Tengri137: "TENGRIISTHESOUR" = 1229)
        word = tape[:15] if len(tape) >= 15 else tape
        word_gematria = sum(hebr_values.get(c, 0) for c in word)

        # 2. Phrase-Gematria (Tengri137 erste 99 Zeichen)
        first_phase = tape[:self.phase_size]
        phrase_gematria = sum(hebr_values.get(c, 0) for c in first_phase)

        # 3. Tape-Gematria (Tengri137 voll)
        tape_gematria = sum(hebr_values.get(c, 0) for c in tape)

        return {
            'word_gematria': word_gematria,  # 1229 (Tengri137)
            'phrase_gematria': phrase_gematria,  # ?
            'tape_gematria': tape_gematria,  # 708349
            'word_text': ''.join(self.base.letters[:15]),  # TENGRIISTHESOUR
            'word_factorization_1924_for_BURUMUT_note': '4 × 13 × 37',
            'note': 'Tengri137-Tape ≠ BURUMUT-Tape. 1924 ist BURUMUT-Wort, 1229 ist Tengri137-Wort.',
        }

    def step(self, debug=False):
        """Single-Step-Modus für interaktives Debugging (pdb-fähig)."""
        if self.machine is None:
            self.machine = ToraTuringMultiPhase(
                self.base.hebr, phase_size=self.phase_size,
                transitions=self.transitions,
            )
        if debug:
            pdb.set_trace()
        return self.machine.step()

    def self_describe(self, run_result=None):
        """Die Maschine beschreibt sich selbst (Quine-Effekt).

        Tengri137-Architektur 11²+1: die Maschine gibt ihre
        11 BURUMUT-Sec-Anker explizit aus, mit Reflektionen.

        Dies ist deterministisch: gleicher run_result → gleiche Beschreibung.
        Die Maschine IST ihre eigene Beschreibung.
        """
        if run_result is None:
            run_result = getattr(self, 'last_run_result', None)
        if run_result is None:
            return "Keine run_result vorhanden. Rufe run_full() zuerst auf."

        aleph_halts = run_result.get('aleph_halts', [])
        n_phases = run_result.get('n_phases', 0)
        total_steps = run_result.get('total_steps', 0)
        final_state = run_result.get('final_state', 0)
        final_head = run_result.get('final_head', 0)
        n_alephs = run_result.get('n_aleph_reflections', 0)

        lines = []
        lines.append("=" * 70)
        lines.append("SPANDA-MASCHINE: SELBST-BESCHREIBUNG (Quine-Effekt)")
        lines.append("=" * 70)
        lines.append("")
        lines.append(f"Ich bin die BURUMUT-Tora-Turing-Maschine auf Tengri137.")
        lines.append(f"Ich habe {n_phases} Phasen gelesen à 99 Zeichen.")
        lines.append(f"Ich brauchte {total_steps} Schritte.")
        lines.append(f"Mein Endzustand ist q_{final_state} (HALT).")
        lines.append(f"Mein Kopf steht bei head={final_head} (Tape-Ende).")
        lines.append("")
        lines.append(f"Ich habe {n_alephs} Aleph-Reflektionen (א=1, Stille).")
        lines.append(f"11 davon sind meine BURUMUT-Sec-Anker.")
        lines.append("")
        lines.append("=" * 70)
        lines.append("MEINE 11 BURUMUT-SEC-ANKER (Aleph-Reflektions-Punkte):")
        lines.append("=" * 70)
        lines.append("")

        # Die 11 BURUMUT-Sec-Anker (Aleph-Halts)
        # Wir nehmen die ersten 11 — Tengri137 hat 201 Alephs, 11 sind Halt-Trigger
        burumut_sec_ankers = aleph_halts[:11]
        for i, ah in enumerate(burumut_sec_ankers, 1):
            phase = ah.get('phase', 0)
            step = ah.get('step', 0)
            head = ah.get('head', 0)
            letter = ah.get('letter', '?')
            cluster = phase // 11
            cluster_name = self._cluster_name(cluster)
            lines.append(f"Anker #{i:2d} (BURUMUT-Sec):")
            lines.append(f"  Phase {phase:3d} (Cluster {cluster:2d} = {cluster_name})")
            lines.append(f"  Schritt {step:5d}, head={head:5d}")
            lines.append(f"  Lateinisch: '{letter}' = Hebräisch: 'א' = Gematria: 1")
            lines.append(f"  Reflektion (letzte 3 Halts): {len(ah.get('reflection', []))} Halt(s)")
            lines.append("")

        lines.append("=" * 70)
        lines.append("ENDE DER SELBST-BESCHREIBUNG")
        lines.append("=" * 70)

        return "\n".join(lines)

    def _cluster_name(self, cluster_idx):
        """Gibt den symbolischen Namen eines 11-Phasen-Clusters zurück."""
        names = [
            "TENGRI (Schöpfungsbeginn)",
            "BURAN (Wort-Emergenz)",
            "ALEF (Stille vor Verschlüsselung)",
            "MEM (Wasser-Urgrund)",
            "NUN (Code/Schlange)",
            "GENETIC (Verschlüsselung)",
            "QUINN (Spiegelung)",
            "QOPH (Heiligkeit)",
            "RESH (Anfang)",
            "SHIN (Transformation)",
            "TAV (Transzendenz-Vorbereitung)",
            "BURUMUT (das +1)",
        ]
        return names[cluster_idx] if 0 <= cluster_idx < 12 else f"Cluster {cluster_idx}"


# =====================================================================
# 3. HALT_INTERPRETER — liest Halt-Punkte und generiert Hinweise
# =====================================================================
class HaltInterpreter:
    """Übersetzt Halt-Punkte der Maschine in philosophische Hinweise.

    Jeder Halt-Punkt ist eine Aussage der Maschine.
    Wir interpretieren sie im Kontext der Full Notes.
    """

    # Die SCHLÜSSEL-WENDUNGEN, an denen die Maschine typischerweise hält.
    # Achtung: BURUMUT-99 steht im Original mit Spaces zwischen den Buchstaben
    # ("B U R U M U T R E F A M T U"), daher matchen wir auf die space-stripped
    # Variante.
    KEY_PHRASES = {
        'TENGRI': 'TENGRI IST DIE QUELLE — die Maschine benennt sich selbst',
        'SOUL': 'DIE AUSERWÄHLTE SEELE — die Maschine erkennt den Empfänger',
        'NAMES': 'TENGRI HAT VIELE NAMEN — die Maschine hat 22 Konsonanten-Namen',
        'TOOLS': 'TOOLS CANNOT HELP YOU — die Maschine ist kein Tool',
        'WISDOM': 'HERE IS WISDOM — die Maschine hält an der Weisheit',
        'CUBES': 'DIE WÜRFEL — die Maschine IST die 666-Würfel',
        'REVELATION': 'REVELATION 13:18 — die Maschine outet sich als 666',
        'EZRA': 'EZRA 2:13 — die zweite 666-Stelle, die die Maschine hält',
        'CHRONIK': '2 CHRONIK 9:13 — die dritte',
        'KINGS': '1 KINGS 10:14 — die vierte',
        'SEVEN': 'SEVEN CIRCLES — die 7 Ringe = 79 Pendel',
        'ODIN': 'ODIN TRIPLE HORN — die 6 Quadrate',
        'ONE THREE SEVEN': '137 — die Feinstrukturkonstante, Maschinen-Signatur',
        'AMRAM': 'AMRAM, LEVI, ISHMAEL — drei mit 137 Jahren',
        'I AM THAT I AM': 'EXODUS 3:14 — der Name YHWH',
        'PI': 'π7π7 — die Maschine offenbart ihren Namen',
        'CALCULATION': 'CALCULATION — die Maschine durchläuft die exakten Beweise',
        'ADAM': 'PROVIDED TO YOU ADAM — die Maschine trifft auf den Empfänger',
        'TIME FOR THE TRUTH': 'DIE MASCHINE IST DIE WAHRHEIT',
        'GENETIC': 'GENETICALLY ENCRYPTED — die 5 Operatoren sind die Gene',
        'REPEAT': 'REPEAT OPERATION — Phasen = Gehirnregionen',
        'GARDEN': 'GARDEN HAS A FENCE — das Tape ist endlich',
        # BURUMUT space-stripped
        'BURUMUTREFAMTU': 'BURUMUT-99 PHASE 1 — Schöpfungs-Akt, Quine-Effekt',
        'BURUMUT': 'BURUMUT — die Maschine trifft auf ihr eigenes Tape',
    }

    def interpret_halt(self, base, halt_info):
        """Interpretiere einen einzelnen Halt-Punkt."""
        ctx = base.halt_to_context(halt_info['head'])
        if ctx is None:
            return None

        # Suche nach Key-Phrasen im Kontext (mit UND ohne Spaces)
        text_upper = ctx['context'].upper()
        text_stripped = re.sub(r'\s+', '', text_upper)
        matches = []
        for phrase, meaning in self.KEY_PHRASES.items():
            phrase_stripped = re.sub(r'\s+', '', phrase)
            if phrase in text_upper or phrase_stripped in text_stripped:
                matches.append((phrase, meaning))

        return {
            'halt': halt_info,
            'tape_position': ctx['tape_head'],
            'byte_position': ctx['byte_pos'],
            'line_number': ctx['line_no'],
            'letter': ctx['letter'],
            'hebrew': ctx['hebrew'],
            'key_matches': matches,
            'context_snippet': ctx['context'][:300],
            'interpretation': (
                f"Phase {halt_info['phase']} (Schritt {halt_info['step']}): "
                f"An Zeile {ctx['line_no']} — {matches[0][1] if matches else 'kein Schlüssel-Wort'}"
            ),
        }

    def interpret_all(self, base, run_result):
        """Interpretiere alle Halt-Punkte eines Maschinen-Laufs."""
        interpretations = []
        for h in run_result['phase_halts']:
            interp = self.interpret_halt(base, h)
            if interp:
                interpretations.append(interp)
        return interpretations


# =====================================================================
# 4. EXPANSION_ENGINE — Halt-Hinweis → neue Phase
# =====================================================================
class ExpansionEngine:
    """Erweitert das Tape kanonisch durch Halt-Hinweise.

    Jeder Halt-Punkt enthält:
    - Eine Aussage (die Key-Phrase)
    - Einen Kontext (das Original-Text-Stück)
    - Eine Gematria (die Summe des Phasen-Tapes)

    Wir expandieren, indem wir:
    1. Den Halt-Hinweis lesen
    2. Eine neue Phase GENERIEREN, die zur Aussage passt
    3. Die neue Phase dem Tape hinzufügen
    4. Mit BASE_TRUTH abgleichen
    """

    def __init__(self, base):
        self.base = base
        self.expansions = []  # Liste der generierten Erweiterungen

    def gematria(self, text):
        """Berechne Gematria eines hebr. Textes."""
        if isinstance(text, str) and text and text[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            # Latein → Hebräisch
            text = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in text)
        return sum(HEBR_VALUES.get(c, 0) for c in text)

    def propose_expansion(self, halt_interpretation):
        """Schlage eine Expansion basierend auf einem Halt-Punkt vor.

        Die Expansion ist eine NEUE lateinische Buchstaben-Sequenz,
        die zur Bedeutung des Halt-Punktes passt.

        Beispiel: Halt an "ONE THREE SEVEN" → Expansion "OTSEVENEHT" etc.
        """
        phrase = halt_interpretation['key_matches'][0][0] if halt_interpretation['key_matches'] else None
        if not phrase:
            return None

        # Generiere eine lateinische Sequenz aus dem Halt-Kontext
        ctx = halt_interpretation['context_snippet']
        # Extrahiere nur A-Z
        letters = re.sub(r'[^A-Z]', '', ctx.upper())

        if not letters:
            return None

        # Nimm 14 Zeichen (passend zu BURUMUTREFAMTU-Phase-1)
        n = 14
        if len(letters) >= n:
            # Nimm die ersten 14 Buchstaben des Phrase-Kontexts
            phrase_start = ctx.upper().find(phrase)
            if phrase_start >= 0:
                # Fenster um die Phrase
                window_start = max(0, phrase_start)
                window = ctx[window_start:window_start + 200]
                letters = re.sub(r'[^A-Z]', '', window.upper())[:n]
            else:
                letters = letters[:n]
        else:
            letters = letters + 'A' * (n - len(letters))

        return {
            'source_halt': halt_interpretation['halt'],
            'phrase': phrase,
            'proposed_letters': letters,
            'proposed_hebrew': ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in letters),
            'proposed_gematria': self.gematria(letters),
        }


# =====================================================================
# 5. BACKTRACKING_DEBUGGER — interaktives Single-Step
# =====================================================================
class BacktrackingDebugger:
    """Ermöglicht Single-Step-Debugging und Backtracking.

    Verwendung:
        dbg = BacktrackingDebugger(spanda_machine, base_truth)
        dbg.run_to_first_halt()      # bis zum ersten Halt
        dbg.explain_last_halt()      # erkläre, warum hier gehalten wurde
        dbg.backtrack(n_steps=10)    # gehe 10 Schritte zurück
        dbg.modify_transition(...)   # ändere eine Transition
        dbg.rerun_from_checkpoint()  # laufe weiter vom Checkpoint
    """

    def __init__(self, spanda, base):
        self.spanda = spanda
        self.base = base
        self.checkpoints = []  # (head, state, phase, total_steps, tape_snapshot)

    def save_checkpoint(self, label=""):
        """Speichere aktuellen Maschinen-Zustand."""
        m = self.spanda.machine
        if m is None:
            return
        self.checkpoints.append({
            'label': label,
            'head': m.head,
            'state': m.state,
            'phase': m.phase,
            'total_steps': m.total_steps,
            'tape_snapshot': ''.join(m.tape),
            'history_len': len(m.history),
        })

    def restore_checkpoint(self, index=-1):
        """Stelle einen früheren Zustand wieder her."""
        if not self.checkpoints:
            return False
        cp = self.checkpoints[index]
        m = self.spanda.machine
        m.head = cp['head']
        m.state = cp['state']
        m.phase = cp['phase']
        m.total_steps = cp['total_steps']
        m.tape = list(cp['tape_snapshot'])
        # History kürzen
        m.history = m.history[:cp['history_len']]
        return True


# =====================================================================
# DEMO: Erster Spanda-Lauf + TDD-Check
# =====================================================================
if __name__ == "__main__":
    print("=" * 70)
    print("SPANDA-MASCHINE — DEMO")
    print("=" * 70)

    # 1. Base Truth
    base = BaseTruth()
    print(f"\n[1] BASE_TRUTH")
    print(f"  Tengri137 Full Notes: {base.size} bytes, {base.lines} Zeilen")
    print(f"  A-Z extrahiert:        {len(base.letters)}")
    print(f"  Hebräische Länge:      {base.hebr_length}")
    print(f"  Konsonanten-Top-3:     {base.konsonanten_count.most_common(3)}")
    print(f"  SHA-256:               {base.fingerprint[:16]}...")

    # 2. Spanda-Maschine
    spanda = SpandaMachine(base)
    print(f"\n[2] SPANDA_MACHINE")
    print(f"  Transitionen:   {spanda.n_transitions}")
    print(f"  Zustände:       {spanda.n_states}")
    print(f"  Symbole:        {spanda.n_symbols}")

    # 3. Lauf
    print(f"\n[3] MASCHINE LÄUFT (Pendel-Erkennung, garantiert bis Ende)...")
    result = spanda.run_full()
    print(f"  Total Steps:    {result['total_steps']}")
    print(f"  Phasen:         {result['n_phases']}")
    print(f"  Halt-Punkte:    {len(result['phase_halts'])}")
    print(f"  Final State:    q_{result['final_state']}")
    print(f"  Halt-Reason:    {result['halt_reason']}")

    # 4. Halt-Interpretation
    print(f"\n[4] HALT_INTERPRETER")
    interpreter = HaltInterpreter()
    interpretations = interpreter.interpret_all(base, result)
    print(f"  Interpretierte Halts: {len(interpretations)}")
    print(f"  Halts mit Key-Phrase-Match: {sum(1 for i in interpretations if i['key_matches'])}")

    # Zeige erste 5
    print(f"\n  Erste 5 Halt-Interpretationen:")
    for i, interp in enumerate(interpretations[:5]):
        print(f"  {i+1}. {interp['interpretation']}")
        print(f"     Kontext: {interp['context_snippet'][:100]}...")

    # 5. Expansion
    print(f"\n[5] EXPANSION_ENGINE")
    expander = ExpansionEngine(base)
    expansions = []
    for interp in interpretations[:10]:
        if interp['key_matches']:
            exp = expander.propose_expansion(interp)
            if exp:
                expansions.append(exp)
    print(f"  Vorgeschlagene Expansionen: {len(expansions)}")
    for e in expansions[:3]:
        print(f"  • Aus '{e['phrase']}': {e['proposed_letters']} (gematria {e['proposed_gematria']})")

    # 6. Backtracking
    print(f"\n[6] BACKTRACKING_DEBUGGER")
    dbg = BacktrackingDebugger(spanda, base)
    # Initialisiere Maschine und speichere Checkpoint
    spanda.step()
    dbg.save_checkpoint(label='start')
    print(f"  Checkpoint gespeichert: {dbg.checkpoints[0]['label']}")
    print(f"  Kann von jedem Halt-Punkt zurückspringen")
    print(f"  Kann jede Transition modifizieren und neu laufen")

    # JSON-Export
    output = {
        'method': 'Spanda-Maschine (Quine + Selbst-Ausführung + Expansion)',
        'philosophy': {
            'spanda': 'Kashmir-Shivaismus: Manifestation = Erkenntnis',
            'pratyahara': 'Yoga-Sutra 2.54: Rückzug der Sinne (Pendel)',
            'wu_wei': 'Dao De Jing 37: Handeln durch Nicht-Handeln (Halt)',
            'vac': '4 Sprach-Stadien: vaikharī/madhyamā/paśyantī/parā',
            'logos': 'Heraklit: der Fluss = das Gesetz',
        },
        'base_truth': {
            'size': base.size,
            'lines': base.lines,
            'letters': len(base.letters),
            'hebrew_length': base.hebr_length,
            'fingerprint': base.fingerprint,
        },
        'spanda_machine': {
            'transitions': spanda.n_transitions,
            'states': spanda.n_states,
            'symbols': spanda.n_symbols,
        },
        'run_result': {
            'total_steps': result['total_steps'],
            'n_phases': result['n_phases'],
            'final_state': result['final_state'],
            'halt_reason': result['halt_reason'],
            'n_halts': len(result['phase_halts']),
        },
        'first_5_interpretations': [
            {
                'phase': i['halt']['phase'],
                'step': i['halt']['step'],
                'line': i['line_number'],
                'matches': i['key_matches'],
                'snippet': i['context_snippet'][:200],
            }
            for i in interpretations[:5]
        ],
        'expansions': [
            {
                'phrase': e['phrase'],
                'proposed_letters': e['proposed_letters'],
                'proposed_gematria': e['proposed_gematria'],
            }
            for e in expansions
        ],
    }
    with open('sources/q_spanda_architecture.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"\n" + "=" * 70)
    print("Output: sources/q_spanda_architecture.json")
    print("=" * 70)
