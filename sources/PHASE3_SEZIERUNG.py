"""
🌌 P73: PHASEN-3-SEZIERUNG — Die Anatomie der absoluten Stille
=================================================================

Seziert Phase 3 (Genesis 4: Kain & Abel) — die geordnetste Stelle
in Tengri137 (H = 3.6385, das absolute Minimum aller 168 Phasen).
Fünf Klassen analog zu P69 (Phase 26), aber mit umgekehrtem
Fokus: STRUKTURELLE ERSTARRUNG statt Punkt des Versagens.

EMPIRISCHE BEFUNDE (P72):
- H = 3.6385 (Minimum der 168 Phasen)
- n_unique = 16 lateinische Symbole
- Top-4: I=N=E=A=12 (perfekte Gleichverteilung)
- 14 hebr. Sec-Operatoren: 8× ג (MOVE_RIGHT), 5× ד (MOVE_LEFT), 1× י (STATE)
- TENGRI 2×, NAMES 2×, TIAN ≥ 1× als lateinische Wörter

ARCHITEKTUR:
- Phase3FrequenzAnatomie: vollständige Verteilung
- Phase3OperatorKarte: hebr. Sec-Operatoren
- Phase3MaschinenLauf: M4 beobachtend
- Phase3EntropieVergleich: H im Kontext
- Phase3SemantischeSignatur: lateinische Wörter
- seziere_phase_3: Master-Funktion

DETERMINISMUS:
- 3/3 Läufe identisch
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import math
import json
from collections import Counter
from typing import List, Dict, Any
from TENGRI_ORAKEL import berechne_entropie
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import (
    HEBR_VALUES, MISSING_OPERATORS, build_tora_transitions
)
from KANONIK_VALIDATOR_MODUL import (
    KanonikValidator, GematriaAnchor, Snapshot
)
from PHASE_MAPPING_TORA import phase_to_torah


def load_tengri_text():
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        return f.read()


def get_phase_3_lat() -> str:
    """Extrahiere Phase 3 (lateinisch) aus Tengri137."""
    text = load_tengri_text()
    text_clean = re.sub(r'\s+', '', text.upper())
    lat = re.sub(r'[^A-Z]', '', text_clean)
    return lat[3*99:4*99]


def get_phase_3_hebr() -> str:
    """Extrahiere Phase 3 (hebr.) aus Tengri137."""
    lat = get_phase_3_lat()
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


# ============================================================
# 1) Phase3FrequenzAnatomie
# ============================================================

class Phase3FrequenzAnatomie:
    """Vollständige Frequenz-Analyse von Phase 3 (lateinisch).

    Bestimmt:
    - counts: Häufigkeit jedes lateinischen Buchstabens
    - n_unique: Anzahl verschiedener Symbole
    - top4: Die 4 häufigsten Symbole (mit Positionen)
    - bigram_counts: Bigramm-Häufigkeiten
    - top_bigram: Häufigstes Bigramm
    - self_similarity: Anteil sich wiederholender 3er-Sequenzen
    """

    def __init__(self, phase_3: str):
        self.phase_3 = phase_3
        self.counts = Counter(phase_3)
        self.n_unique = len(self.counts)
        # Top-4
        self.top4 = [
            {'symbol': s, 'freq': f, 'positions': [i for i, c in enumerate(phase_3) if c == s]}
            for s, f in self.counts.most_common(4)
        ]
        # Positionen pro Symbol
        self.positions = {
            s: [i for i, c in enumerate(phase_3) if c == s]
            for s in self.counts
        }
        # Bigramme
        bigrams = [phase_3[i:i+2] for i in range(len(phase_3) - 1)]
        self.bigram_counts = Counter(bigrams)
        self.top_bigram = self.bigram_counts.most_common(1)[0] if self.bigram_counts else None
        # Trigramm-Selbstähnlichkeit: Anteil sich wiederholender 3er
        trigrams = [phase_3[i:i+3] for i in range(len(phase_3) - 2)]
        tri_counts = Counter(trigrams)
        n_repeated = sum(1 for c in tri_counts.values() if c > 1)
        self.n_repeated_trigrams = n_repeated
        self.trigram_counts = tri_counts

    def analyse(self) -> Dict[str, Any]:
        return {
            'phase_length': len(self.phase_3),
            'n_unique': self.n_unique,
            'top4': self.top4,
            'top_bigram': self.top_bigram,
            'n_repeated_trigrams': self.n_repeated_trigrams,
            'all_counts': dict(self.counts),
            'all_bigrams': dict(self.bigram_counts),
        }


# ============================================================
# 2) Phase3OperatorKarte (hebr.)
# ============================================================

class Phase3OperatorKarte:
    """Karte der 14 hebr. Sec-Operatoren in Phase 3.

    Bestimmt:
    - sec_positions: Liste der Positionen (0-98)
    - sec_letters: Liste der hebr. Buchstaben
    - sec_distribution: Verteilung
    - n_sec_total: 14
    - avg_gap: durchschnittlicher Abstand
    """

    def __init__(self, phase_3_hebr: str):
        self.phase_3_hebr = phase_3_hebr
        positions = []
        letters = []
        for i, c in enumerate(phase_3_hebr):
            if c in MISSING_OPERATORS:
                positions.append(i)
                letters.append(c)
        self.sec_positions = positions
        self.sec_letters = letters
        self.sec_distribution = Counter(letters)
        self.n_sec_total = len(positions)
        # Abstände
        if len(positions) >= 2:
            gaps = [positions[i+1] - positions[i]
                    for i in range(len(positions) - 1)]
        else:
            gaps = []
        self.sec_gaps = gaps
        self.avg_gap = sum(gaps) / len(gaps) if gaps else 0

    def analyse(self) -> Dict[str, Any]:
        return {
            'n_sec_total': self.n_sec_total,
            'sec_positions': self.sec_positions,
            'sec_letters': self.sec_letters,
            'sec_distribution': dict(self.sec_distribution),
            'avg_gap': self.avg_gap,
            'positions_by_type': {
                op: [i for i, c in enumerate(self.phase_3_hebr) if c == op]
                for op in MISSING_OPERATORS
            },
        }


# ============================================================
# 3) Phase3MaschinenLauf
# ============================================================

class Phase3MaschinenLauf:
    """M4 beobachtend auf Phase 3.

    Bestimmt:
    - first_violation_step: Schritt der ersten 37²-Violation
    - first_violation_symbol: Auslöser
    - first_violation_state: q_0..q_5
    - n_unique_states: Anzahl Zustände
    - max_gematria_acc: Maximale Akkumulation
    - total_steps: Anzahl Schritte
    - halt_reason: HALT-Grund (falls)
    """

    def __init__(self, phase_3_hebr: str):
        self.phase_3_hebr = phase_3_hebr
        self.machine = ToraTuringMultiPhase(
            phase_3_hebr, phase_size=99, transitions=build_tora_transitions()
        )
        self.anchor = GematriaAnchor(bridge=37)
        self.validator = KanonikValidator(
            self.machine, anchor=self.anchor, strict=False
        )

    def run(self, max_steps: int = 200) -> Dict[str, Any]:
        """Laufe beobachtend, dokumentiere erste Violation."""
        # Initialer Snapshot
        initial = Snapshot(
            state=self.machine.state,
            head=self.machine.head,
            gematria_acc=0,
            step=0,
            phase=self.machine.phase,
            phase_start=self.machine.phase * self.machine.phase_size,
        )
        self.validator.snapshots.append(initial)
        self.validator.last_valid_snapshot = initial

        first_violation_step = None
        first_violation_symbol = None
        first_violation_state = None
        first_violation_gem = None
        first_violation_gem_acc = None
        max_gematria_acc = 0
        states_visited = {self.machine.state}

        while (not self.machine.halted
               and self.machine.total_steps < max_steps
               and first_violation_step is None):
            self.machine.step()
            if self.machine.halted:
                break
            states_visited.add(self.machine.state)

            # Gematria-Akkumulation
            prev_acc = (self.validator.snapshots[-1].gematria_acc
                        if self.validator.snapshots else 0)
            if self.machine.head < len(self.machine.tape):
                current_gem = HEBR_VALUES.get(self.machine.tape[self.machine.head], 0)
            else:
                current_gem = 0
            gematria_acc = prev_acc + current_gem
            max_gematria_acc = max(max_gematria_acc, gematria_acc)

            snap = Snapshot(
                state=self.machine.state,
                head=self.machine.head,
                gematria_acc=gematria_acc,
                step=self.machine.total_steps,
                phase=self.machine.phase,
                phase_start=self.machine.phase * self.machine.phase_size,
            )
            self.validator.snapshots.append(snap)

            # Anchor-Prüfung
            if not self.anchor.is_anchor(gematria_acc):
                first_violation_step = self.machine.total_steps
                first_violation_symbol = (
                    self.machine.tape[self.machine.head]
                    if self.machine.head < len(self.machine.tape) else None
                )
                first_violation_state = self.machine.state
                first_violation_gem = current_gem
                first_violation_gem_acc = gematria_acc

        return {
            'first_violation_step': first_violation_step,
            'first_violation_symbol': first_violation_symbol,
            'first_violation_state': first_violation_state,
            'first_violation_gematria': first_violation_gem,
            'first_violation_gematria_acc': first_violation_gem_acc,
            'n_unique_states': len(states_visited),
            'max_gematria_acc': max_gematria_acc,
            'total_steps': self.machine.total_steps,
            'halt_reason': self.machine.halt_reason,
            'halted': self.machine.halted,
        }


# ============================================================
# 4) Phase3EntropieVergleich
# ============================================================

class Phase3EntropieVergleich:
    """H(Phase 3) im Kontext der 168-Phasen-Topographie (P72).

    Bestimmt:
    - h: Shannon-Entropie
    - alphabet_eff: 2^H (effektive Alphabetgröße)
    - distance_to_mean: H - 3.9938 (P72-mean)
    - distance_to_max: H - 4.1844 (P72-max)
    - z_score: (H - mean) / std
    """

    P72_MEAN = 3.9938
    P72_STD = 0.0987
    P72_MAX = 4.1844
    P72_MIN = 3.6385

    def __init__(self, phase_3: str):
        self.phase_3 = phase_3
        self.h = berechne_entropie(phase_3)
        self.alphabet_eff = 2 ** self.h
        self.distance_to_mean = self.h - self.P72_MEAN
        self.distance_to_max = self.h - self.P72_MAX
        self.z_score = self.distance_to_mean / self.P72_STD if self.P72_STD > 0 else 0
        self.is_minimum = abs(self.h - self.P72_MIN) < 0.001

    def analyse(self) -> Dict[str, Any]:
        return {
            'h': self.h,
            'alphabet_eff': self.alphabet_eff,
            'distance_to_mean': self.distance_to_mean,
            'distance_to_max': self.distance_to_max,
            'z_score': self.z_score,
            'is_p72_minimum': self.is_minimum,
            'p72_mean': self.P72_MEAN,
            'p72_max': self.P72_MAX,
        }


# ============================================================
# 5) Phase3SemantischeSignatur
# ============================================================

class Phase3SemantischeSignatur:
    """Lateinische Wort-Wand in Phase 3.

    Sucht nach erkennbaren Wörtern (≥ 4 Zeichen):
    - TENGRI 2×, NAMES 2× (laut Direktive)
    - Weitere: TIAN, TIANDI, RANGI, SHANGDI, SHADDAI, DINGIR, TENGERE
    """

    WORD_CANDIDATES = [
        'TENGRI', 'TENGRE', 'TENG', 'TIAN', 'TIANDI', 'RANGI',
        'SHANGDI', 'SHADDAI', 'DINGIR', 'TENGERE', 'NAMES', 'NAME',
        'BETTER', 'HAS', 'MANY', 'ARE', 'SOME', 'THIS', 'ARE',
    ]

    def __init__(self, phase_3: str):
        self.phase_3 = phase_3
        self.word_counts = {}
        self.word_positions = {}
        for word in self.WORD_CANDIDATES:
            positions = []
            for i in range(len(phase_3) - len(word) + 1):
                if phase_3[i:i+len(word)] == word:
                    positions.append(i)
            if positions:
                self.word_counts[word] = len(positions)
                self.word_positions[word] = positions

    def analyse(self) -> Dict[str, Any]:
        return {
            'word_counts': self.word_counts,
            'word_positions': self.word_positions,
            'n_distinct_words': len(self.word_counts),
        }


# ============================================================
# 6) seziere_phase_3 — Master-Funktion
# ============================================================

def seziere_phase_3() -> Dict[str, Any]:
    """Kombinierte Sezierung: alle 5 Analysen.

    Returns:
        Dict mit frequenz, operatoren, maschine, entropie, semantik, phase_3_meta
    """
    p3 = get_phase_3_lat()
    p3h = get_phase_3_hebr()

    # 1) Frequenz
    fa = Phase3FrequenzAnatomie(p3)
    fa_result = fa.analyse()

    # 2) Operator-Karte
    ok = Phase3OperatorKarte(p3h)
    ok_result = ok.analyse()

    # 3) Maschinen-Lauf
    ml = Phase3MaschinenLauf(p3h)
    ml_result = ml.run()

    # 4) Entropie
    ec = Phase3EntropieVergleich(p3)
    ec_result = ec.analyse()

    # 5) Semantik
    ss = Phase3SemantischeSignatur(p3)
    ss_result = ss.analyse()

    # Meta
    book, chap = phase_to_torah(3)
    meta = {
        'book': book,
        'chapter': chap,
        'phase_idx': 3,
        'length': len(p3),
        'gematria_lat': sum(ord(c) - ord('A') + 1 for c in p3),
        'gematria_hebr': sum(HEBR_VALUES.get(c, 0) for c in p3h),
    }

    return {
        'frequenz': fa_result,
        'operatoren': ok_result,
        'maschine': ml_result,
        'entropie': ec_result,
        'semantik': ss_result,
        'phase_3_meta': meta,
    }


# ============================================================
# SELBST-TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 78)
    print("🌌 P73: PHASEN-3-SEZIERUNG — Die Anatomie der absoluten Stille")
    print("=" * 78)
    print()
    print("Phase 3 = Genesis 4 (Kain & Abel), H = 3.6385, das Minimum.")
    print("Fünf Analysen:")
    print("  1. Frequenz-Anatomie: lateinische Verteilung")
    print("  2. Operator-Karte: 14 hebr. Sec-Operatoren")
    print("  3. Maschinen-Lauf: M4 beobachtend")
    print("  4. Entropie-Vergleich: H im P72-Kontext")
    print("  5. Semantische Signatur: lateinische Wörter")
    print()

    result = seziere_phase_3()

    # Meta
    meta = result['phase_3_meta']
    print("=" * 78)
    print("📍 META")
    print("=" * 78)
    print(f"  Buch: {meta['book']} {meta['chapter']}")
    print(f"  Phase: {meta['phase_idx']}")
    print(f"  Länge: {meta['length']}")
    print(f"  Gematria (lat): {meta['gematria_lat']}")
    print(f"  Gematria (hebr): {meta['gematria_hebr']} (mod 37 = {meta['gematria_hebr'] % 37})")
    print()

    # Frequenz
    fr = result['frequenz']
    print("=" * 78)
    print("🔤 FREQUENZ-ANATOMIE")
    print("=" * 78)
    print(f"  n_unique: {fr['n_unique']}")
    print(f"  Top-4 (perfekte Gleichverteilung):")
    for e in fr['top4']:
        print(f"    '{e['symbol']}': {e['freq']}× (Positionen: {e['positions'][:5]}...)")
    print(f"  Top-Bigramm: {fr['top_bigram']}")
    print(f"  Repeated Trigramme: {fr['n_repeated_trigrams']}")
    print()
    print("  Vollständige Verteilung:")
    for sym, freq in sorted(fr['all_counts'].items(), key=lambda x: -x[1]):
        print(f"    {sym}: {freq}")
    print()

    # Operator-Karte
    op = result['operatoren']
    print("=" * 78)
    print("🗺️ OPERATOR-KARTE (14 hebr. Sec)")
    print("=" * 78)
    print(f"  Total Sec: {op['n_sec_total']}")
    print(f"  Verteilung: {op['sec_distribution']}")
    print(f"  Mittlerer Abstand: {op['avg_gap']:.2f}")
    print()
    print("  Per-Operator Positionen:")
    for op_type, positions in op['positions_by_type'].items():
        if positions:
            print(f"    {op_type} ({MISSING_OPERATORS[op_type]}): {positions}")
    print()

    # ASCII-Karte
    print("  ASCII-Karte der 99 Zeichen (S=Sec):")
    p3h = get_phase_3_hebr()
    line = ''
    for i, c in enumerate(p3h):
        if c in MISSING_OPERATORS:
            line += 'S'
        else:
            line += '.'
    for i in range(0, 99, 33):
        print(f"    {i:>3}: {line[i:i+33]}")
    print()

    # Maschinen-Lauf
    ml = result['maschine']
    print("=" * 78)
    print("⚙️ MASCHINEN-LAUF (M4 beobachtend)")
    print("=" * 78)
    if ml['first_violation_step'] is not None:
        print(f"  Erste Violation-Step: {ml['first_violation_step']}")
        print(f"  Violation-Symbol: {ml['first_violation_symbol']} (Gematria {ml['first_violation_gematria']})")
        print(f"  Violation-State: q_{ml['first_violation_state']}")
        print(f"  Violation-Gematria-Acc: {ml['first_violation_gematria_acc']} "
              f"(mod 37 = {ml['first_violation_gematria_acc'] % 37})")
    print(f"  Total Steps: {ml['total_steps']}")
    print(f"  Halted: {ml['halted']}")
    print(f"  Halt-Reason: {ml['halt_reason']}")
    print(f"  n_unique_states: {ml['n_unique_states']}")
    print(f"  max_gematria_acc: {ml['max_gematria_acc']}")
    print()

    # Entropie
    en = result['entropie']
    print("=" * 78)
    print("📊 ENTROPIE-VERGLEICH")
    print("=" * 78)
    print(f"  H(Phase 3) = {en['h']:.4f}")
    print(f"  H_max (lat. 26 Symbole) = {math.log2(26):.4f}")
    print(f"  H_mean (P72) = {en['p72_mean']:.4f}")
    print(f"  H_max (P72) = {en['p72_max']:.4f}")
    print(f"  Alphabet-Eff: {en['alphabet_eff']:.2f}")
    print(f"  ΔH vom P72-Mittel: {en['distance_to_mean']:+.4f}")
    print(f"  Z-Score: {en['z_score']:+.2f}")
    print(f"  Ist P72-Minimum? {en['is_p72_minimum']}")
    print()

    # Semantik
    se = result['semantik']
    print("=" * 78)
    print("📜 SEMANTISCHE SIGNATUR")
    print("=" * 78)
    print(f"  Gefundene Wörter: {len(se['word_counts'])}")
    for word, count in sorted(se['word_counts'].items(), key=lambda x: -x[1]):
        positions = se['word_positions'][word]
        print(f"    {word}: {count}× an Pos {positions}")
    print()

    # Speichern
    output = {
        'method': 'P73 — Phasen-3-Sezierung (Anatomie der absoluten Stille)',
        'principle': ('Strukturelle Erstarrung in der geordnetsten '
                      'Stelle von Tengri137. Reine Beobachtung.'),
        'phase_3_meta': meta,
        'frequenz': fr,
        'operatoren': op,
        'maschine': ml,
        'entropie': en,
        'semantik': se,
    }

    with open('/run/media/julian/ML4/tengri137/sources/phase_3_sezierung.json',
              'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in phase_3_sezierung.json")
    print()
    print("=" * 78)
    print("🌌 P73 PHASEN-3-SEZIERUNG ABGESCHLOSSEN")
    print("=" * 78)
