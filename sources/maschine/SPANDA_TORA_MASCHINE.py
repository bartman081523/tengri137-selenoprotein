"""
🌌 SPANDA-×-TORA-MASCHINE: Die Aleph-Atmung in der Tora
========================================================

M5 (Spanda) läuft normalerweise auf Tengri137-Tape. Hier erweitern wir
sie, damit sie auch auf Tora-Versen läuft und die Aleph-Architektur zeigt.

BEFUND: Tengri137 hat 201 Alephs über 122 Phasen (BURUMUT-Architektur).
FRAGE: Welche Aleph-Architektur haben die Tora-Verse?

METHODE:
1. Erstelle BaseTruth-Instanz pro Tora-Stelle (Tape = hebr. Konsonanten)
2. Lasse SpandaMachine laufen
3. Sammle Aleph-Halts
4. Vergleiche mit normalem Durchlauf (M4 Schritt-Zahlen)
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import json
import re
import hashlib
from collections import Counter
from pathlib import Path

from SPANDA_MACHINE import BaseTruth, SpandaMachine
from TORA_TURING_CORRECT import build_tora_transitions


class ToraBaseTruth:
    """Eine BaseTruth-Instanz für einen Tora-Vers (statt Tengri137)."""

    def __init__(self, name, hebr_text, original_text):
        self.name = name
        self.raw = original_text
        self.size = len(original_text)
        self.hebr = hebr_text
        self.hebr_length = len(hebr_text)
        self.letters = list(hebr_text)
        self.position_map = list(range(len(hebr_text)))
        self.fingerprint = hashlib.sha256(original_text.encode('utf-8')).hexdigest()[:16]
        self.konsonanten_count = Counter(hebr_text)

    def context_at_position(self, pos, before=50, after=100):
        if pos < 0 or pos >= self.size:
            return None
        return self.raw[max(0, pos-before):min(self.size, pos+after)]

    def halt_to_context(self, tape_head):
        if tape_head >= len(self.position_map):
            tape_head = len(self.position_map) - 1
        if tape_head < 0:
            tape_head = 0
        return {
            'position': self.position_map[tape_head],
            'context': self.raw[max(0, tape_head-50):min(self.size, tape_head+100)],
            'tape_head': tape_head,
        }


def run_spanda_on_tora(name, hebr_text, original_text, max_steps=10000):
    """Lasst SpandaMachine auf einem Tora-Vers laufen."""
    base = ToraBaseTruth(name, hebr_text, original_text)
    spanda = SpandaMachine(base, phase_size=99, max_steps=max_steps)
    r = spanda.run_full()

    return {
        'name': name,
        'tape_length': len(hebr_text),
        'n_alephs': hebr_text.count('א'),
        'n_phases': r.get('n_phases', 0),
        'total_steps': r.get('total_steps', 0),
        'aleph_halts': r.get('aleph_halts', []),
        'all_halts': r.get('all_halts', []),
        'halt_reason': r.get('halt_reason', 'UNKNOWN'),
        'last_halt': r.get('last_halt', {}),
    }


# ===========================================================
# HAUPTPROGRAMM
# ===========================================================

def main():
    print("=" * 78)
    print("🌌 SPANDA × TORA: Aleph-Architektur in der Tora")
    print("=" * 78)
    print()

    # Tora laden
    books = {}
    for i, name in enumerate(['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'], 1):
        with open(f'/run/media/julian/ML4/tengri137/sources/torah/{i:02d}.json') as f:
            books[name] = json.load(f)

    # 12 Tora-Stellen (gleiche wie M4)
    stellen = [
        ('Gen 1,1', 'Genesis', 0, 0),
        ('Gen 1,2', 'Genesis', 0, 1),
        ('Gen 1,3', 'Genesis', 0, 2),  # LICHT
        ('Gen 3,1', 'Genesis', 2, 0),  # Schlange
        ('Gen 3,4', 'Genesis', 2, 3),  # Schlange
        ('Gen 4,6', 'Genesis', 3, 5),  # Kain
        ('Gen 4,9', 'Genesis', 3, 8),  # Kain
        ('Gen 6,7', 'Genesis', 5, 6),  # Noah
        ('Gen 7,1', 'Genesis', 6, 0),  # Noah Arche
        ('Gen 7,2', 'Genesis', 6, 1),  # Noah Tiere
        ('Gen 3,10', 'Genesis', 2, 9), # Adam nackt
        ('Gen 3,24', 'Genesis', 2, 23),# Cherubim
        ('Lev 19,18', 'Leviticus', 18, 17),  # Liebe
        ('Num 6,24', 'Numbers', 5, 23),  # Aaron-Segen
        ('Gen 12,1', 'Genesis', 11, 0), # Abraham
        ('Gen 37,7', 'Genesis', 36, 6), # Binah-Traum
        # Absurd-Verse
        ('Gen 23,1', 'Genesis', 22, 0), # Sarah
        ('Exo 21,1', 'Exodus', 20, 0),  # Gesetze
        ('Deut 28,1', 'Deuteronomy', 27, 0),
        ('Lev 10,1', 'Leviticus', 9, 0), # Nadab
    ]

    print(f"{'Vers':<14} | {'Zchn':>4} | {'Aleph':>5} | {'Phasen':>6} | {'Steps':>5} | {'Halt':<22}")
    print("-" * 78)

    results = []
    for name, book, kap, vers in stellen:
        text = books[book]['text']
        if kap >= len(text) or vers >= len(text[kap]):
            continue
        original = text[kap][vers]
        hebr = original.replace(' ', '').replace(' ', '')
        if not hebr:
            continue
        r = run_spanda_on_tora(name, hebr, original)
        results.append(r)
        print(f"{name:<14} | {len(hebr):>4} | {hebr.count('א'):>5} | "
              f"{r['n_phases']:>6} | {r['total_steps']:>5} | "
              f"{r['halt_reason'][:22]:<22}")

    # Vergleich: Tengri137 (normaler Durchlauf)
    print()
    print("=" * 78)
    print("📜 TENGRI137 (normaler Durchlauf, 12071 Zeichen)")
    print("=" * 78)
    base = BaseTruth()
    spanda = SpandaMachine(base, phase_size=99, max_steps=100000)
    r_full = spanda.run_full()
    print(f"Tengri137: {base.hebr_length} Zeichen, 201 Alephs, "
          f"{r_full.get('n_phases', 0)} Phasen, "
          f"aleph_halts = {len(r_full.get('aleph_halts', []))}")
    print(f"Aleph-Halts: {len(r_full.get('aleph_halts', []))} (= 11 BURUMUT-Sec-Anker)")

    # Aleph-Reflektions-Vergleich
    print()
    print("=" * 78)
    print("🔮 ALEPH-REFLEKTIONS-VERGLEICH")
    print("=" * 78)
    print()
    print("Wenn Spanda eine Aleph-Architektur in Tora-Versen findet, dann")
    print("sollte die Aleph-Dichte der Verse dem BURUMUT-Muster entsprechen.")
    print()
    print(f"{'Vers':<14} | {'Alephs':>6} | {'Aleph/100':>9} | {'Verhältnis zu Tengri137'}")
    print("-" * 78)
    tengri_aleph_density = 201 / 12071  # = 0.01666
    for r in results:
        density = r['n_alephs'] / r['tape_length'] if r['tape_length'] else 0
        ratio = density / tengri_aleph_density
        print(f"{r['name']:<14} | {r['n_alephs']:>6} | {density*100:>9.3f} | "
              f"{ratio:.2f}× {'(BURUMUT-ähnlich)' if 0.5 < ratio < 2.0 else ''}")

    # Aleph-Halt-Positionen
    print()
    print("=" * 78)
    print("📍 ALEPH-HALT-POSITIONEN (nur Verse mit Aleph-Halts)")
    print("=" * 78)
    for r in results:
        if r['aleph_halts']:
            print(f"\n{r['name']} ({r['n_alephs']} Alephs im Vers):")
            for ah in r['aleph_halts'][:5]:
                print(f"  Phase {ah['phase']}, head {ah['head']}, "
                      f"letter {ah.get('letter', '?')}, "
                      f"reflection: {len(ah.get('reflection', []))} Halts")
            if len(r['aleph_halts']) > 5:
                print(f"  ... und {len(r['aleph_halts'])-5} weitere")

    # Vergleich: Welche Verse zeigen Aleph-Architektur?
    print()
    print("=" * 78)
    print("🎯 ALEPH-ARCHITEKTUR-BEFUNDE")
    print("=" * 78)
    print()
    for r in results:
        n_aleph = r['n_alephs']
        n_aleph_halts = len(r['aleph_halts'])
        if n_aleph > 0:
            ratio = n_aleph_halts / n_aleph if n_aleph else 0
            print(f"  {r['name']:<14}: {n_aleph} Alephs, {n_aleph_halts} Aleph-Halts, "
                  f"ratio={ratio:.2f}")
        else:
            print(f"  {r['name']:<14}: 0 Alephs (kein Aleph)")

    return results


if __name__ == "__main__":
    main()
