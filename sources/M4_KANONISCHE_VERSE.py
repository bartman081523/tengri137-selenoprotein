"""
🔬 M4 RESONANZ: Welche Verse WIRKLICH passen
==============================================

Wir wollen wissen: Wenn M4 mehrere Verse mit der "richtigen" Schritt-Zahl
findet, welche sind die "kanonischen" Kandidaten?

Idee: Multi-Maschinen-Lesung — eine Maschine pro BURUMUT-Phase (6 Maschinen
für 6 Zustände), und wir nehmen nur Verse, die ALLE BURUMUT-Phasen gleich
behandeln.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import json
from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
from TORA_TURING_CORRECT import build_tora_transitions

# Tora
books = {}
for i, name in enumerate(['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'], 1):
    with open(f'/run/media/julian/ML4/tengri137/sources/torah/{i:02d}.json') as f:
        books[name] = json.load(f)

# Sammle alle Verse
all_verses = []
for book_name, data in books.items():
    for kap_idx, kap in enumerate(data['text']):
        if not isinstance(kap, list):
            continue
        for vers_idx, vers in enumerate(kap):
            if not vers:
                continue
            hebr = vers.replace(' ', '').replace(' ', '')
            if hebr:
                all_verses.append((book_name, kap_idx+1, vers_idx+1, hebr))

# Strategie: Wir suchen Verse, die bei M4 in MEHREREN BURUMUT-Phasen resonieren.
# BURUMUT-Phasen: 99, 198, 297, ... (= 99 * n)
PHASES = [99, 198, 297, 396, 495, 594, 693, 792, 891, 990, 1089]

print(f"Teste alle {len(all_verses)} Verse mit {len(PHASES)} BURUMUT-Phasen...")
print()

transitions = build_tora_transitions()

# Sammle Treffer pro Phase
phase_matches = {p: [] for p in PHASES}

# Sample 1000 Verse für Geschwindigkeit
SAMPLE = all_verses[:1000]
print(f"Sample-Größe: {len(SAMPLE)} Verse")

# Erwartete Schritt-Zahlen pro Phase
# Bei phase_size=p hängt steps von tape-Länge ab — wir suchen
# Verse die bei ALLEN Phasen dieselbe Schritt-Zahl geben? Zu strikt.

# Stattdessen: Wir suchen Verse, deren Schritt-Zahl ein Vielfaches von
# Phase/99 ist, oder die kanonische Schritt-Zahlen haben.
EXPECTED = [3, 5, 6, 7, 12, 15]

print("\nLasse M4 über alle Verse mit Phase 99 laufen...")
for i, (book, kap, vers, hebr) in enumerate(SAMPLE):
    if i % 100 == 0:
        print(f"  {i}/1000...")
    try:
        # Phase 99 (1 BURUMUT)
        m = ToraTuringMultiPhase(hebr, phase_size=99, transitions=transitions)
        m.run(max_steps=1000)
        steps = m.total_steps
        if steps in EXPECTED:
            phase_matches[99].append((book, kap, vers, hebr, steps))
    except Exception:
        pass

print(f"✓ Phase 99: {len(phase_matches[99])} Verse mit erwarteten Schritt-Zahlen")

# Welche Verse erscheinen mit MEHREREN erwarteten Schritt-Zahlen?
# Wir wollen: Verse, deren Schritt-Zahl "kanonisch" ist.
print()
print("=" * 60)
print("🎯 KANONISCHE VERSE (treten mit erwarteten Schritt-Zahlen auf)")
print("=" * 60)
print()

for book, kap, vers, hebr, steps in phase_matches[99][:30]:
    # Welche "Architektur" passt?
    label = {
        3: "3 (3 Summen / Liebe deinen Nächsten)",
        5: "5 (He / Atmung / Aaron-Segen)",
        6: "6 (5 Bücher + Sabbat / Schöpfung)",
        7: "7 (Schöpfungstage / Sabbat)",
        12: "12 (11+1 / Abraham / Stämme Israels)",
        15: "15 (3×5 / Binah / Sefirot-Atmung)",
    }.get(steps, str(steps))
    print(f"  {book} {kap},{vers} → {label}")

print()
print("=" * 60)
print("🏆 TOP-KANDIDATEN für M4-Maschinen-Resonanz")
print("=" * 60)
print()

# Welche Verse haben die "besten" Architektur-Matches?
# Kriterium: Schritt-Zahl ∈ {3, 5, 6, 7, 12, 15}
# UND Buch = Genesis (Anfang der Tora)
# UND Schöpfungs-bezogen

creation_verses = [
    (b, k, v, h, s) for b, k, v, h, s in phase_matches[99]
    if b == 'Genesis' and s in EXPECTED
]
print(f"\nGenesis-Verse mit kanonischen Schritt-Zahlen: {len(creation_verses)}")

# Gruppiere nach Schritt-Zahl
from collections import defaultdict
by_steps = defaultdict(list)
for b, k, v, h, s in creation_verses:
    by_steps[s].append((b, k, v, h))

for steps in [3, 5, 6, 7, 12, 15]:
    if steps in by_steps:
        print(f"\n  {steps} Schritte ({len(by_steps[steps])} Verse):")
        for b, k, v, h in by_steps[steps][:5]:
            # Heuristik: Welcher Architektur-Punkt?
            label = {
                3: "Liebe / 3 Summen",
                5: "He / Aaron-Segen",
                6: "Schöpfung / Sabbat",
                7: "Schöpfungstage",
                12: "11+1 / Abraham",
                15: "Binah / 3×5",
            }[steps]
            print(f"    {b} {k},{v} — {label}")
