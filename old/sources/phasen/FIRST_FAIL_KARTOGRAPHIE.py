"""
🌌 P76: FIRST-FAIL-KARTOGRAPHIE — Die 168 Maschinen-Tode
=========================================================

Kartographiert das erste M4-Versagen in allen 168 Phasen von
Tengri137. P70 zeigte: ALLE 168 Phasen scheitern an Step 1.
P76 zeigt: WO genau stirbt die Maschine? An welchem hebr.
Buchstaben?

WARUM P76?
- P70 hat nur die Step-Verteilung gemessen
- P69/73/74 haben einzelne Phasen seziert
- P76 macht die GESAMTKARTEN der First-Fails

ARCHITEKTUR:
- FirstFailRecord: phase_idx + fail_symbol + gematria + state +
  gematria_acc + mod_37 + mod_73 + tora
- FirstFailKartographie: Aggregation, Statistik
- kartographiere_first_fails: Master-Funktion
- phase_first_fail_lookup: Gezielte Abfrage
- verteilung_der_first_fails: Counter

DETERMINISMUS:
- 3/3 Läufe identisch
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import json
import math
import statistics
from collections import Counter
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase, EXTENDED_LATIN_TO_HEBR
from TORA_TURING_CORRECT import HEBR_VALUES, build_tora_transitions
from KANONIK_VALIDATOR_MODUL import KanonikValidator, GematriaAnchor, Snapshot
from PHASE_MAPPING_TORA import phase_to_torah, TORA_BOOKS
from TENGRI_ORAKEL import berechne_entropie


def load_tengri_hebr() -> str:
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        text = f.read()
    text_clean = re.sub(r'\s+', '', text.upper())
    lat = re.sub(r'[^A-Z]', '', text_clean)
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


def load_tengri_lat() -> str:
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        text = f.read()
    text_clean = re.sub(r'\s+', '', text.upper())
    return re.sub(r'[^A-Z]', '', text_clean)


# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass
class FirstFailRecord:
    """First-Fail einer Phase.

    Attribute:
        phase_idx: Index der Phase (0-167)
        fail_symbol: hebr. Buchstabe, der die Maschine stoppt
        fail_gematria: Gematria des Symbols
        fail_state: Maschinen-Zustand (q_0..q_5)
        fail_gematria_acc: Gematria-Akkumulation am Versagens-Punkt
        mod_37: fail_gematria mod 37
        mod_73: fail_gematria mod 73
        tora_book: Tora-Buch (Genesis, Exodus, ...)
        tora_chapter: Tora-Kapitel
        failure_step: Schritt des ersten Versagens (immer 1, P70)
    """
    phase_idx: int
    fail_symbol: str
    fail_gematria: int
    fail_state: int
    fail_gematria_acc: int
    mod_37: int
    mod_73: int
    tora_book: str
    tora_chapter: int
    failure_step: int = 1

    def to_dict(self) -> Dict[str, Any]:
        return {
            'phase_idx': self.phase_idx,
            'fail_symbol': self.fail_symbol,
            'fail_gematria': self.fail_gematria,
            'fail_state': self.fail_state,
            'fail_gematria_acc': self.fail_gematria_acc,
            'mod_37': self.mod_37,
            'mod_73': self.mod_73,
            'tora_book': self.tora_book,
            'tora_chapter': self.tora_chapter,
            'failure_step': self.failure_step,
        }


class FirstFailKartographie:
    """Sammlung von First-Fail-Records."""

    def __init__(self):
        self.records: List[FirstFailRecord] = []

    @property
    def n_total(self) -> int:
        return len(self.records)

    def add(self, rec: FirstFailRecord):
        self.records.append(rec)

    def verteilung(self) -> Dict[str, int]:
        """Verteilung der First-Fail-Symbole."""
        return dict(Counter(r.fail_symbol for r in self.records))

    def top_symbole(self, n: int = 5) -> List[tuple]:
        """Die n häufigsten First-Fail-Symbole."""
        c = Counter(r.fail_symbol for r in self.records)
        return c.most_common(n)

    def lookup(self, phase_idx: int) -> Optional[FirstFailRecord]:
        """Suche First-Fail für eine bestimmte Phase."""
        for r in self.records:
            if r.phase_idx == phase_idx:
                return r
        return None


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def korrelation_pearson(xs: List[float], ys: List[float]) -> Optional[float]:
    """Pearson-Korrelationskoeffizient. None wenn undefiniert."""
    n = len(xs)
    if n != len(ys) or n < 2:
        return None
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
    den_x = math.sqrt(sum((xs[i] - mean_x) ** 2 for i in range(n)))
    den_y = math.sqrt(sum((ys[i] - mean_y) ** 2 for i in range(n)))
    if den_x == 0 or den_y == 0:
        return None
    return num / (den_x * den_y)


# ============================================================
# MESSUNG PRO PHASE
# ============================================================

def messe_first_fail(tape: str, phase_idx: int) -> FirstFailRecord:
    """Messe First-Fail einer Phase.

    Args:
        tape: Phase als hebr. String (99 Zeichen)
        phase_idx: Globaler Index der Phase (0-167)

    Returns:
        FirstFailRecord mit allen Versagens-Daten
    """
    m = ToraTuringMultiPhase(
        tape, phase_size=99, transitions=build_tora_transitions()
    )
    anchor = GematriaAnchor(bridge=37)
    v = KanonikValidator(m, anchor=anchor, strict=False)

    # Initialer Snapshot
    init = Snapshot(
        state=m.state, head=m.head, gematria_acc=0,
        step=0, phase=m.phase, phase_start=m.phase * m.phase_size,
    )
    v.snapshots.append(init)
    v.last_valid_snapshot = init

    # Laufe bis zum ersten Versagen
    failure_step = None
    failure_symbol = None
    failure_gematria = None
    failure_state = None
    failure_gacc = None

    while (not m.halted and m.total_steps < 100
           and failure_step is None):
        m.step()
        if m.halted:
            break
        prev_acc = v.snapshots[-1].gematria_acc
        cur_gem = HEBR_VALUES.get(m.tape[m.head], 0) if m.head < len(m.tape) else 0
        gacc = prev_acc + cur_gem
        snap = Snapshot(
            state=m.state, head=m.head, gematria_acc=gacc,
            step=m.total_steps, phase=m.phase,
            phase_start=m.phase * m.phase_size,
        )
        v.snapshots.append(snap)
        if not anchor.is_anchor(gacc):
            failure_step = m.total_steps
            failure_symbol = m.tape[m.head] if m.head < len(m.tape) else None
            failure_gematria = cur_gem
            failure_state = m.state
            failure_gacc = gacc

    # Default: Step 1 (sollte nie passieren, aber defensiv)
    if failure_step is None:
        failure_step = 1
        failure_symbol = m.tape[0] if m.tape else '?'
        failure_gematria = HEBR_VALUES.get(failure_symbol, 0)
        failure_state = m.state
        failure_gacc = failure_gematria

    book, chap = phase_to_torah(phase_idx)
    return FirstFailRecord(
        phase_idx=phase_idx,
        fail_symbol=failure_symbol,
        fail_gematria=failure_gematria,
        fail_state=failure_state,
        fail_gematria_acc=failure_gacc,
        mod_37=failure_gematria % 37,
        mod_73=failure_gematria % 73,
        tora_book=book,
        tora_chapter=chap,
    )


# ============================================================
# HAUPTFUNKTION
# ============================================================

def kartographiere_first_fails() -> Dict[str, Any]:
    """Master-Funktion: kartographiert alle 168 First-Fails.

    Returns:
        Dict mit:
        - n_phases: 168
        - records: [FirstFailRecord]
        - verteilung: Counter
        - top_5: häufigste Symbole
        - per_day: 7-Tage-Aggregation
        - per_book: 5-Buch-Aggregation
        - correlation_h_fail_gem: H ↔ fail_gematria
    """
    tengri_hebr = load_tengri_hebr()
    tengri_lat = load_tengri_lat()

    topo = FirstFailKartographie()
    hs_list = []  # H pro Phase
    fail_gem_list = []  # fail_gematria pro Phase

    n_phases = (len(tengri_hebr) + 98) // 99
    for i in range(n_phases):
        tape = tengri_hebr[i*99:(i+1)*99]
        rec = messe_first_fail(tape, i)
        topo.add(rec)

        # H dieser Phase (lateinisch)
        phase_lat = tengri_lat[i*99:(i+1)*99]
        h = berechne_entropie(phase_lat)
        hs_list.append(h)
        fail_gem_list.append(float(rec.fail_gematria))

    # Verteilung
    verteilung = topo.verteilung()
    top_5 = topo.top_symbole(5)

    # Pro Tag
    per_day = []
    for day_idx in range(7):
        day_recs = [
            r for r in topo.records
            if day_idx * 24 <= r.phase_idx < (day_idx + 1) * 24
        ]
        if day_recs:
            fails = [r.fail_symbol for r in day_recs]
            per_day.append({
                'day_idx': day_idx + 1,
                'n_phases': len(day_recs),
                'top_fail': Counter(fails).most_common(1)[0],
                'unique_fails': len(set(fails)),
            })

    # Pro Tora-Buch
    per_book = {}
    for book in TORA_BOOKS:
        info = TORA_BOOKS[book]
        book_recs = [
            r for r in topo.records
            if info['phases_start'] <= r.phase_idx < info['phases_end']
        ]
        per_book[book] = len(book_recs)

    # Korrelation H ↔ fail_gematria
    corr_h_gem = korrelation_pearson(hs_list, fail_gem_list)

    return {
        'n_phases': n_phases,
        'records': topo.records,
        'verteilung': verteilung,
        'top_5': top_5,
        'per_day': per_day,
        'per_book': per_book,
        'correlation_h_fail_gem': corr_h_gem,
    }


def phase_first_fail_lookup(phase_idx: int) -> Optional[FirstFailRecord]:
    """Gezielte Abfrage für eine Phase."""
    tengri_hebr = load_tengri_hebr()
    tape = tengri_hebr[phase_idx*99:(phase_idx+1)*99]
    return messe_first_fail(tape, phase_idx)


def verteilung_der_first_fails() -> Dict[str, int]:
    """Convenience: nur die Verteilung."""
    return kartographiere_first_fails()['verteilung']


def top_symbole(n: int = 5) -> List[tuple]:
    """Convenience: die Top-N First-Fails."""
    return kartographiere_first_fails()['top_5'][:n]


# ============================================================
# SELBST-TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 78)
    print("🌌 P76: FIRST-FAIL-KARTOGRAPHIE — Die 168 Maschinen-Tode")
    print("=" * 78)
    print()
    print("An welchem hebr. Buchstaben stirbt die Maschine in jeder Phase?")
    print()

    result = kartographiere_first_fails()

    # Übersicht
    print("=" * 78)
    print("📊 ÜBERSICHT")
    print("=" * 78)
    print(f"  Total Phasen:       {result['n_phases']}")
    print(f"  Unique Fail-Symbole: {len(result['verteilung'])} (von 22 möglich)")
    print()

    # Top 10
    print("=" * 78)
    print("🏆 TOP 10 FIRST-FAIL-SYMBOLE")
    print("=" * 78)
    top_10 = Counter(result['verteilung']).most_common(10)
    for sym, count in top_10:
        g = HEBR_VALUES.get(sym, 0)
        bar = '█' * min(40, count)
        print(f"  {sym} (Gem {g:>3}): {count:>3} {bar}")
    print()

    # Pro Tag
    print("=" * 78)
    print("📅 PRO TAG (7-Tage-Aggregation)")
    print("=" * 78)
    for d in result['per_day']:
        marker = ''
        if d['day_idx'] == 7:
            marker = ' ← Sabbat'
        elif d['day_idx'] == 6:
            marker = ' ← Chaos'
        print(f"  Tag {d['day_idx']}: {d['n_phases']} Phasen, "
              f"{d['unique_fails']} unique fails, "
              f"top = {d['top_fail'][0]}({d['top_fail'][1]}×){marker}")
    print()

    # Pro Tora-Buch
    print("=" * 78)
    print("📚 PRO TORA-BUCH")
    print("=" * 78)
    for book, count in result['per_book'].items():
        print(f"  {book:<18}: {count} Phasen")
    print()

    # Korrelation
    print("=" * 78)
    print("🔗 KORRELATION")
    print("=" * 78)
    print(f"  r(H, fail_gematria) = {result['correlation_h_fail_gem']:.4f}")
    print()

    # Erste 20 Phasen als Tabelle
    print("=" * 78)
    print("📋 ERSTE 20 FIRST-FAILS")
    print("=" * 78)
    print(f"  {'Phase':>5} {'Tora':>10} {'Symbol':>3} {'Gem':>4} "
          f"{'mod37':>5} {'mod73':>5}")
    for r in result['records'][:20]:
        print(f"  {r.phase_idx:>5} {r.tora_book[:3]} {r.tora_chapter:>3} "
              f"{r.fail_symbol:>3} {r.fail_gematria:>4} "
              f"{r.mod_37:>5} {r.mod_73:>5}")
    print()

    # Speichern
    output = {
        'method': 'P76 — First-Fail-Kartographie',
        'principle': (
            'Welcher hebr. Buchstabe stoppt die Maschine '
            'in jeder der 168 Phasen?'
        ),
        'n_phases': result['n_phases'],
        'verteilung': result['verteilung'],
        'top_5': result['top_5'],
        'per_day': result['per_day'],
        'per_book': result['per_book'],
        'correlation_h_fail_gem': result['correlation_h_fail_gem'],
        'records': [r.to_dict() for r in result['records']],
    }

    with open('/run/media/julian/ML4/tengri137/sources/phasen/first_fail_kartographie.json',
              'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in first_fail_kartographie.json")
    print()
    print("=" * 78)
    print("🌌 P76 FIRST-FAIL-KARTOGRAPHIE ABGESCHLOSSEN")
    print("=" * 78)
