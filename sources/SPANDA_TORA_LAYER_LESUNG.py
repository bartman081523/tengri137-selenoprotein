"""
🌌 SPANDA-×-TORA-×-LAYER-REGISTER: Aleph-Architektur + 5 Layer
===============================================================

M5 (Spanda) läuft mit Layer-Register über Tora-Verse.

METHODE:
1. Erstelle ToraBaseTruth-Instanz pro Tora-Vers (Tape = hebr. Konsonanten)
2. SpandaMachine nutzt das Layer-Register für Aleph-Reflektion
3. Sammle Aleph-Halts (Tengri137-Architektur 11²+1)
4. Sammle Layer-Durchgänge (welche Layer werden besucht?)
5. Vergleiche mit normalem M4-Durchlauf (Schritt-Zahlen)

ARCHITEKTUR (5-Layer × 1 = 6 Zustände):
  q_0 Genesis, q_1 Exodus, q_2 Leviticus, q_3 Numeri, q_4 Deut, q_5 HALT
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import json
import hashlib
from collections import Counter
from pathlib import Path

from SPANDA_MACHINE import SpandaMachine
from TORA_TURING_CORRECT import LAYER_REGISTER, get_layer_name


# Tora-Pfade
TORA_DIR = '/run/media/julian/ML4/tengri137/sources/torah'
BOOKS = ['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy']


class ToraBaseTruth:
    """Eine BaseTruth-Instanz für einen Tora-Vers.

    Kompatibel mit SpandaMachine, die self.base.hebr erwartet.
    """

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


def load_torah():
    books = {}
    for i, name in enumerate(BOOKS, 1):
        with open(f'{TORA_DIR}/{i:02d}.json') as f:
            books[name] = json.load(f)
    return books


def get_vers(books, book, kap, vers):
    """Extrahiere Vers (1-indiziert)."""
    text = books[book]['text']
    if kap-1 >= len(text):
        return None
    if vers-1 >= len(text[kap-1]):
        return None
    return text[kap-1][vers-1].replace(' ', '').replace(' ', '')


# 30 Tora-Referenzen (gleiche wie M4-Test)
TORA_REFERENCES = {
    # 6 Schritte
    6: [('Gen', 1, 1, 'Schöpfung'),
        ('Gen', 4, 7, 'Kain Sünde'),
        ('Gen', 4, 22, 'Lamech'),
        ('Gen', 4, 24, 'Lamech-Rache'),
        ('Gen', 5, 1, 'Adam-Buch')],
    # 5 Schritte (He/Atmung)
    5: [('Gen', 1, 2, 'He-Atmung'),
        ('Gen', 1, 13, 'Tag 3 He'),
        ('Gen', 1, 19, 'Tag 4 He'),
        ('Gen', 1, 22, 'Tag 5 He'),
        ('Gen', 1, 23, 'Tag 5 Ende He'),
        ('Gen', 1, 28, 'Tag 6 Segen He'),
        ('Gen', 1, 30, 'Tag 6 Ende He'),
        ('Gen', 2, 3, 'Sabbat He'),
        ('Num', 6, 24, 'Aaron-Segen')],
    # 12 Schritte
    12: [('Gen', 3, 1, 'Schlange listig'),
         ('Gen', 3, 4, 'Schlange lügt'),
         ('Gen', 4, 6, 'Kain zürnt'),
         ('Gen', 4, 9, 'Kain: Wo ist Abel'),
         ('Gen', 12, 1, 'Abraham-Aufruf')],
    # 15 Schritte
    15: [('Gen', 6, 7, 'Noah vertilgen'),
         ('Gen', 7, 1, 'Noah Arche'),
         ('Gen', 7, 2, 'Noah 7 Tiere'),
         ('Gen', 7, 7, 'Noah in Arche'),
         ('Gen', 7, 17, 'Noah Sintflut'),
         ('Gen', 37, 7, 'Binah-Traum')],
    # 7 Schritte
    7: [('Gen', 3, 10, 'Adam nackt'),
        ('Gen', 3, 24, 'Cherubim')],
    # 3 Schritte
    3: [('Lev', 19, 18, 'Liebe deinen Nächsten')],
    # 10 Schritte (Licht = 10 Sefirot)
    10: [('Gen', 1, 3, 'Licht')],
    # 4 Schritte (Tetragrammaton)
    4: [('Gen', 19, 19, 'Lot Gnade')],
}


def run_spanda_with_layer(name, hebr_text, original_text):
    """SpandaMachine mit Layer-Register auf Tora-Vers."""
    base = ToraBaseTruth(name, hebr_text, original_text)
    spanda = SpandaMachine(base, phase_size=99, max_steps=10000)
    r = spanda.run_full()

    # Layer-Durchgänge extrahieren
    layer_visits = []
    if r.get('history'):
        for h in r['history']:
            if 'old_state' in h and 'new_state' in h:
                old = h['old_state']
                new = h['new_state']
                # Konvertiere zu int falls String
                if isinstance(old, str):
                    try: old = int(old)
                    except: continue
                if isinstance(new, str):
                    try: new = int(new)
                    except: continue
                if old != new and isinstance(old, int) and isinstance(new, int):
                    layer_visits.append((
                        get_layer_name(old),
                        get_layer_name(new)
                    ))
    # Dedup
    seen = set()
    unique_visits = []
    for v in layer_visits:
        if v not in seen:
            seen.add(v)
            unique_visits.append(v)

    # final_state kann String sein
    final_state = r.get('final_state', 0)
    if isinstance(final_state, str):
        try: final_state = int(final_state)
        except: final_state = 0

    # Extrahiere die 's' Werte aus unique_visits (sind Strings = Layer-Namen)
    unique_layer_names = set()
    for old_name, new_name in unique_visits:
        if isinstance(new_name, str):
            unique_layer_names.add(new_name)

    return {
        'name': name,
        'tape_length': len(hebr_text),
        'n_alephs': hebr_text.count('א'),
        'total_steps': r['total_steps'],
        'aleph_halts': r.get('aleph_halts', []),
        'n_aleph_halts': len(r.get('aleph_halts', [])),
        'all_halts': r.get('phase_halts', []),
        'n_phase_halts': len(r.get('phase_halts', [])),
        'halt_reason': r.get('halt_reason', 'UNKNOWN'),
        'layer_visits': unique_visits,
        'layer_count': len(unique_layer_names),
        'final_layer': get_layer_name(final_state),
    }


# ===========================================================
# HAUPTPROGRAMM
# ===========================================================

def main():
    print("=" * 78)
    print("🌌 SPANDA × TORA × LAYER-REGISTER")
    print("=" * 78)
    print()

    books = load_torah()

    # Sammle alle Referenzen
    all_verses = []
    for steps, refs in TORA_REFERENCES.items():
        for book_short, kap, vers, name in refs:
            book_full = {'Gen': 'Genesis', 'Exo': 'Exodus', 'Lev': 'Leviticus',
                         'Num': 'Numbers', 'Deut': 'Deuteronomy'}[book_short]
            original = books[book_full]['text'][kap-1][vers-1]
            hebr = original.replace(' ', '').replace(' ', '')
            if hebr:
                all_verses.append((steps, book_full, kap, vers, name, hebr, original))

    print(f"Anzahl Tora-Referenzen: {len(all_verses)}")
    print()

    # ==== Tabelle 1: Aleph-Architektur ====
    print(f"{'Vers':<22} | {'Zch':>3} | {'Aleph':>5} | {'Steps':>5} | {'Phase-Halts':>11} | {'Halt'}")
    print("-" * 78)

    results = []
    for steps, book, kap, vers, name, hebr, original in all_verses:
        r = run_spanda_with_layer(f"{book} {kap},{vers}", hebr, original)
        results.append((steps, book, kap, vers, name, r))
        print(f"{book[:3]} {kap},{vers:<2} {name[:15]:<15} | {len(hebr):>3} | "
              f"{r['n_alephs']:>5} | {r['total_steps']:>5} | "
              f"{r['n_phase_halts']:>11} | {r['halt_reason'][:20]}")

    # ==== Tabelle 2: Layer-Besuche ====
    print()
    print("=" * 78)
    print("🔮 LAYER-BESUCHE (welche Layer werden durchlaufen?)")
    print("=" * 78)
    print()
    print(f"{'Vers':<25} | {'Layer-Besuche':<40} | {'Anz.':>4}")
    print("-" * 78)

    for steps, book, kap, vers, name, r in results:
        if r['layer_visits']:
            visits = ', '.join(f"{old[:3]}→{new[:3]}" for old, new in r['layer_visits'][:5])
            if len(r['layer_visits']) > 5:
                visits += f" ... (+{len(r['layer_visits'])-5})"
            print(f"{book[:3]} {kap},{vers} {name[:15]:<14} | {visits:<40} | {len(r['layer_visits']):>4}")
        else:
            print(f"{book[:3]} {kap},{vers} {name[:15]:<14} | (kein Layer-Wechsel)              | {0:>4}")

    # ==== Tabelle 3: Aleph-Halt-Positionen ====
    print()
    print("=" * 78)
    print("📍 ALEPH-HALT-POSITIONEN")
    print("=" * 78)
    print()
    print(f"{'Vers':<25} | {'Aleph-Halts':>11} | {'Reflektionen'}")
    print("-" * 78)

    for steps, book, kap, vers, name, r in results:
        if r['aleph_halts']:
            # Sammle die Reflektionen
            refls = [len(ah.get('reflection', [])) for ah in r['aleph_halts']]
            avg_refl = sum(refls) / len(refls) if refls else 0
            print(f"{book[:3]} {kap},{vers} {name[:15]:<14} | {r['n_aleph_halts']:>11} | "
                  f"avg {avg_refl:.1f} Reflektionen pro Aleph-Halt")
        else:
            print(f"{book[:3]} {kap},{vers} {name[:15]:<14} | {0:>11} | -")

    # ==== Tabelle 4: Vergleich mit Tengri137 ====
    print()
    print("=" * 78)
    print("📜 VERGLEICH MIT TENGRI137 (normaler Durchlauf)")
    print("=" * 78)
    print()

    # Tengri137 laden
    tengri_path = '/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes'
    tengri_raw = Path(tengri_path).read_text()
    tengri_letters = [c for c in tengri_raw if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
    from SPANDA_MACHINE import BaseTruth
    base = BaseTruth(tengri_path)
    spanda = SpandaMachine(base, phase_size=99, max_steps=100000)
    r_full = spanda.run_full()
    tengri_aleph_halts = r_full.get('aleph_halts', [])

    print(f"Tengri137: {len(tengri_letters)} lateinische Buchstaben, 201 Alephs (Tape)")
    print(f"           {len(tengri_aleph_halts)} Aleph-Halts = 11 BURUMUT-Sec-Anker (entdeckt 2026-07-01)")
    print()

    # Aleph-Dichte
    tengri_density = 201 / len(tengri_letters)  # 0.01666
    print(f"Aleph-Dichte Tengri137: {tengri_density*100:.3f}%")
    print()
    print(f"{'Vers':<25} | {'Aleph':>5} | {'Dichte%':>8} | {'Verhältnis'}")
    print("-" * 78)

    for steps, book, kap, vers, name, r in results:
        if r['n_alephs'] > 0 and r['tape_length'] > 0:
            density = r['n_alephs'] / r['tape_length']
            ratio = density / tengri_density
            marker = ''
            if 0.7 <= ratio <= 1.3:
                marker = ' (BURUMUT-ähnlich)'
            print(f"{book[:3]} {kap},{vers} {name[:15]:<14} | {r['n_alephs']:>5} | "
                  f"{density*100:>7.3f} | {ratio:.2f}×{marker}")

    # ==== Tabelle 5: ARCHITEKTUR-BEFUNDE ====
    print()
    print("=" * 78)
    print("🎯 ARCHITEKTUR-BEFUNDE (Spanda × Tora)")
    print("=" * 78)
    print()

    # Welche Verse zeigen Aleph-Architektur?
    # BURUMUT-Sec-Anker: 11 Aleph-Halts in der TENGRI-Eröffnung
    # In Tora-Versen: weniger Alephs, aber Aleph-Halts zeigen BURUMUT-Atmung

    n_with_aleph = sum(1 for _, _, _, _, _, r in results if r['n_aleph_halts'] > 0)
    n_aleph_total = sum(r['n_alephs'] for _, _, _, _, _, r in results)
    n_aleph_halts_total = sum(r['n_aleph_halts'] for _, _, _, _, _, r in results)

    print(f"Anzahl Verse mit Aleph-Halts: {n_with_aleph} / {len(results)}")
    print(f"Anzahl Alephs gesamt: {n_aleph_total}")
    print(f"Anzahl Aleph-Halts gesamt: {n_aleph_halts_total}")
    print(f"Aleph-Halts pro Aleph: {n_aleph_halts_total/n_aleph_total:.2f}" if n_aleph_total > 0 else "")
    print()

    # Welche Verse haben Aleph = 11 (BURUMUT-Sec)?
    elevens = [(b, k, v, n, r) for _, b, k, v, n, r in results
               if r['n_aleph_halts'] == 11]
    if elevens:
        print(f"Verse mit EXAKT 11 Aleph-Halts (BURUMUT-Sec-Match):")
        for b, k, v, n, r in elevens:
            print(f"  {b} {k},{v} {n}")

    # Aleph-Verteilung über die Verse
    print()
    print("Aleph-Halts-Verteilung:")
    dist = Counter(r['n_aleph_halts'] for _, _, _, _, _, r in results)
    for count, verses in sorted(dist.items()):
        print(f"  {count} Aleph-Halts: {verses} Verse")

    return results


if __name__ == "__main__":
    main()
