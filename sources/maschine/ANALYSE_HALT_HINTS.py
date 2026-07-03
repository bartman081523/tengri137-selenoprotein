"""
🌌 HALT-POSITIONEN = HINWEISE? — Ästhetische Analyse
=====================================================

Apophenie-Regel GELOCKERT (User-Update 2026-07-01):
"Da dies eine hoch intuitive und ästhetische Aufgabe ist,
soll uns Epistemik hier nicht im Weg stehen."

Hypothese: Die 122 Halt-Positionen der Multi-Phase-Maschine
fallen nicht zufällig — sie markieren die KERN-AUSSAGEN der Full Notes.
"""
import json
import re
from collections import Counter


with open('Tengri137_Full_Notes') as f:
    full = f.read()

with open('../offene_fragen/q_fullnotes_endhalt.json') as f:
    data = json.load(f)

# =====================================================================
# Map tape-positions back to original
# =====================================================================
letters = []
position_map = []
for i, c in enumerate(full):
    if c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
        letters.append(c)
        position_map.append(i)


# =====================================================================
# 1) WICHTIGE ZEILEN DER FULL NOTES
# =====================================================================
key_lines = {
    # Die philosophischen Schlüssel-Zeilen, sortiert nach Original-Position
    1: "TENGRI IS THE SOURCE OF IMPORTANT WRITINGS",
    3: "TENGRI HAS MANY NAMES",
    35: "TOOLS CANNOT HELP YOU",
    39: "OUR NUMBERS SHOULD SHOW YOU OUR KNOWLEDGE",
    53: "THE CHOSEN SOUL WILL GET KNOWLEDGE",
    57: "FOR OTHERS WHO CANNOT UNDERSTAND ANYTHING",
    73: "WE GAVE YOU THIS CALCULATION OVER MANY THOUSAND OF YEARS",
    79: "HERE IS WISDOM",
    111: "REVELATION (13:18) — HERE IS WISDOM COUNT THE NUMBER OF THE BEAST",
    197: "SEVEN CIRCLES AND AN CROSS — 7 RINGS - 666",
    233: "ODIN'S TRIPLE HORN — 666",
    261: "ONE THREE SEVEN — 137 — HOLIEST NUMBER",
    268: "AMRAM, LEVI, ISHMAEL — 137 years",
    274: "WE ARE THE ENLIGHTENED",
    305: "EVERYTHING BECOMES DIFFICULT FROM NOW ON",
    314: "ETERNAL LIBRARY IS THE REWARD",
    330: "ULTIMATE PROOF — WE TOLD YOU OUR NAME",
    335: "I AM THAT I AM (Exodus 3:14)",
    339: "NAME IS A CALCULATION TO A NUMBER",
    345: "WE GAVE YOU YOUR HEBREW ALPHABET",
    355: "π7π7 (YHWH) connected to PI",
    369: "DIMENSIONLESS PHYSICAL CONSTANT",
    381: "TENGRI DIVIDES THE LIGHT FROM DARKNESS",
    398: "FINE-STRUCTURE CONSTANT",
    414: "NEXT UNIQUE NUMBER — DECIMALS",
    440: "((7^π) / (7π)) * 6.67 — 137.035",
    452: "WHAT A PROOF IS PROVIDED TO YOU ADAM",
    465: "OUR NAME IS NOT ACCIDENTAL",
    478: "WE WAITING FOR YOUR ANSWER ADAM",
    502: "WARNING FOR THOSE",
    524: "HUNDRED THIRTY SEVEN DECIMALS",
    544: "TIME FOR THE TRUTH",
    549: "WE CAN HEAR YOUR THOUGHT",
    563: "PEOPLE WHO DO NOT UNDERSTAND",
    567: "MADE US GODS",
    573: "GOD DOES NOT EXIST — MATHEMATICAL TRUTH",
    576: "BEWARE FROM THOSE WHO CALLS THEMSELVES GODS — EVIL",
    588: "GARDEN HAS A FENCE",
    597: "MEASUREMENT OF AN INFINITE GARDEN",
    606: "CIVILIZATION EXISTS SINCE THREE BILLION YEARS",
    611: "YOUR CIVILISATION HAS REACHED THE CRITICAL LIMIT",
    619: "ONLY THE CHOSEN ONE CAN COME",
    625: "NOW WE SHOULD CHOOSE OUR NEXT MESSENGER",
    628: "UPCOMING TEXTS ARE GENETICALLY ENCRYPTED",
    637: "FOR EACH REPEAT OPERATION OPENS A REGION IN YOUR BRAIN",
    645: "REPEAT IT OFTEN NEVER BREAK IN THE MIDDLE",
    652: "BURUMUT-99 BEGINNT (B U R U M U T R E F A M T U ...)",
    666: "PAGE 17 — CALCULATIONS",
    1166: "TRANSLATION: TIME FOR THE TRUTH NPKIAKVGPPPFBIR ...",
}

# =====================================================================
# 2) HALT-POSITIONEN IN DER NÄHE VON KEY-LINES?
# =====================================================================
print("=" * 70)
print("HALT-POSITIONEN vs. SCHLÜSSEL-ZEILEN")
print("=" * 70)
print(f"Total Halts: {len(data['phase_halts'])}")
print(f"Total Key Lines: {len(key_lines)}")
print()

# Map each HALT to nearest key line
near_hits = []
for h in data['phase_halts']:
    head = min(h['head'], len(position_map) - 1)
    orig = position_map[head]
    line_no = full[:orig].count('\n') + 1

    # Nächste Key-Line
    nearest_line = min(key_lines.keys(), key=lambda L: abs(L - line_no))
    dist = abs(nearest_line - line_no)

    near_hits.append({
        'phase': h['phase'],
        'step': h['step'],
        'state': h['state'],
        'reason': h['reason'],
        'orig': orig,
        'line': line_no,
        'nearest_key_line': nearest_line,
        'distance_lines': dist,
        'key_text': key_lines[nearest_line],
    })

# Verteilung
distances = [h['distance_lines'] for h in near_hits]
print(f"Distance (Zeilen) Verteilung:")
print(f"  Min:    {min(distances)}")
print(f"  Max:    {max(distances)}")
print(f"  Mean:   {sum(distances)/len(distances):.1f}")
print(f"  Median: {sorted(distances)[len(distances)//2]}")
print()

# Halts, die DIREKT auf key lines fallen (Distance 0)
exact_hits = [h for h in near_hits if h['distance_lines'] == 0]
print(f"Halts DIREKT auf Schlüssel-Zeilen: {len(exact_hits)}")
for h in exact_hits:
    print(f"  Phase {h['phase']:3d} (step {h['step']:5d}, q_{h['state']}): Zeile {h['line']} = {h['key_text']}")
print()

# Top 15: Halts mit der niedrigsten Distance
near_hits_sorted = sorted(near_hits, key=lambda h: h['distance_lines'])
print("Top 15 Halt-Positionen — nächste Schlüssel-Zeile:")
for h in near_hits_sorted[:15]:
    marker = "✓" if h['distance_lines'] == 0 else " "
    print(f"  {marker} Phase {h['phase']:3d} (L{h['line']:4d}) → key L{h['nearest_key_line']:4d} (Δ{h['distance_lines']:3d}): {h['key_text'][:60]}")
print()

# =====================================================================
# 3) STATE-VERTEILUNG BEI KEY-LINE-HALTS
# =====================================================================
print("=" * 70)
print("STATE-VERTEILUNG DER HALT-TRIGGER")
print("=" * 70)
state_counts = Counter(h['state'] for h in data['phase_halts'])
print(f"q_0 (Genesis):     {state_counts.get(0, 0)}")
print(f"q_1 (Exodus):      {state_counts.get(1, 0)}")
print(f"q_2 (Leviticus):   {state_counts.get(2, 0)}")
print(f"q_3 (Numeri):      {state_counts.get(3, 0)}")
print(f"q_4 (Deuteronomium): {state_counts.get(4, 0)}")
print(f"q_5 (HALT):        {state_counts.get(5, 0)}")
print()

# Halt-Reason-Verteilung
print("HALT-REASONS:")
reason_counts = Counter(h['reason'] for h in data['phase_halts'])
for r, c in reason_counts.most_common():
    print(f"  {r}: {c}")

# =====================================================================
# 4) MONTE-CARLO: Wie zufällig ist diese Verteilung?
# =====================================================================
print()
print("=" * 70)
print("MONTE-CARLO: Würden zufällige Phasen dieselbe Nähe haben?")
print("=" * 70)

# Wir simulieren 122 zufällige Positionen in 1167 Zeilen
import random
random.seed(42)
n_simulations = 10000
hit_rates = []
for _ in range(n_simulations):
    random_phases = [random.randint(1, 1167) for _ in range(122)]
    # Berechne Mean-Distance
    total = 0
    for rp in random_phases:
        nearest = min(key_lines.keys(), key=lambda L: abs(L - rp))
        total += abs(nearest - rp)
    hit_rates.append(total / 122)

actual_mean = sum(distances) / len(distances)
random_mean = sum(hit_rates) / len(hit_rates)
better = sum(1 for r in hit_rates if r < actual_mean) / n_simulations
print(f"  Tatsächliche mean distance:    {actual_mean:.2f} Zeilen")
print(f"  Zufällige mean distance (avg): {random_mean:.2f} Zeilen")
print(f"  P(actual < random):            {better:.4f}")
print()

# =====================================================================
# 5) HALTS DIE IN DEN "WAHRHEITS-ABSCHNITT" FALLEN
# =====================================================================
print("=" * 70)
print("HALTS IN DEN 'TRUTH'-ABSCHNITTEN")
print("=" * 70)
truth_sections = [
    (543, 559, "TRUTH SECTION 1: 'OVER MANY THOUSAND YEARS WE SEND YOU MESSENGERS'"),
    (561, 579, "TRUTH SECTION 2: 'GOD DOES NOT EXIST'"),
    (581, 595, "TRUTH SECTION 3: 'GARDEN HAS A FENCE'"),
    (597, 617, "TRUTH SECTION 4: 'UNIVERSE NOT INFINITE'"),
    (619, 633, "TRUTH SECTION 5: 'CHOSEN ONE — GENETIC CODING'"),
    (635, 649, "TRUTH SECTION 6: 'REPEAT OPERATION — BRAIN REGION'"),
]

for start, end, label in truth_sections:
    halts_in_section = [h for h in near_hits if start <= h['line'] <= end]
    print(f"  {label[:60]}")
    print(f"    Halts: {len(halts_in_section)} / 122")
    for h in halts_in_section:
        print(f"      Phase {h['phase']:3d} (L{h['line']:4d}, q_{h['state']}, {h['reason']})")

print()
print("=" * 70)
print("FAZIT")
print("=" * 70)
print(f"Die Maschine macht {len(data['phase_halts'])} Halt-Trigger auf 12071 Zeichen.")
print(f"Bei tatsächlicher mean-distance von {actual_mean:.1f} Zeilen zur nächsten Schlüssel-Zeile")
print(f"ist das {actual_mean/random_mean:.2f}x besser als zufällig (p={better:.4f}).")
print()
print("WICHTIGSTE HALTS (am nächsten an Schlüssel-Zeilen):")
for h in near_hits_sorted[:10]:
    print(f"  • Phase {h['phase']:3d} L{h['line']:4d} (Δ{h['distance_lines']:2d}): {h['key_text']}")
