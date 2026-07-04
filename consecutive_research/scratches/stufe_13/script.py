"""
Stufe 13 — Biochemische Analyse: Amidin-Gruppen und Aminosäuren.

Frage: Sind die Amidin-Gruppen auf p23_R4 ein Schlüssel zur BURUMUT-Matrix?

Methode:
  1) BURUMUT als Aminosäure-Sequenz lesen (1-Buchstaben-Code)
  2) Verteilung der Aminosäuren analysieren
  3) Klassen-Komposition: basisch, sauer, polar, hydrophob, selten
  4) Vergleich mit bekannten Proteinen
  5) Die Amidin-Gruppen sind die Guanidin-Gruppe des Arginins
"""
from collections import Counter
from pathlib import Path
import json

# BURUMUT-Matrix (11 Zeilen x 14 Buchstaben)
burumut_lines = [
    "BURUMUTREFAMTU",
    "NURESUTREGUMFA",
    "YAPSUAZBEHIMLA",
    "ZANRUAZBENOMBA",
    "TOBIKOTLUBUMYO",
    "SUNOKURGANOZYI",
    "OKUZIKUFAUSIHE",
    "YABEKANSABERHO",
    "NAFERANSAHOTFE",
    "KOREMORBIZUMRO",
    "SUNAKIRFANEMBA",
]

# Aminosäure-Code
amino_acids = {
    'A': ('Alanin', 'hydrophob'),
    'B': ('Asparagin/Aspartat', 'polar/sauer'),
    'C': ('Cystein', 'hydrophob'),
    'D': ('Aspartat', 'sauer'),
    'E': ('Glutamat', 'sauer'),
    'F': ('Phenylalanin', 'hydrophob'),
    'G': ('Glycin', 'hydrophob'),
    'H': ('Histidin', 'basisch'),
    'I': ('Isoleucin', 'hydrophob'),
    'J': ('Leucin (künstl.)', 'hydrophob'),
    'K': ('Lysin', 'basisch'),
    'L': ('Leucin', 'hydrophob'),
    'M': ('Methionin', 'hydrophob'),
    'N': ('Asparagin', 'polar'),
    'O': ('Pyrrolysin (A22)', 'selten'),
    'P': ('Prolin', 'hydrophob'),
    'Q': ('Glutamin', 'polar'),
    'R': ('Arginin', 'basisch'),
    'S': ('Serin', 'polar'),
    'T': ('Threonin', 'polar'),
    'U': ('Selenocystein (A21)', 'selten'),
    'V': ('Valin', 'hydrophob'),
    'W': ('Tryptophan', 'hydrophob'),
    'X': ('unbekannt', 'unbekannt'),
    'Y': ('Tyrosin', 'polar'),
    'Z': ('Glutamat/Glutamin', 'sauer/polar'),
}

# === REPORT ===
print("=" * 80)
print("STUFE 13 — BIOCHEMISCHE ANALYSE: BURUMUT ALS AMINOSÄURE-SEQUENZ")
print("=" * 80)
print()

# 1) Sequenz aufbauen
all_chars = ''.join(burumut_lines)
print("=" * 80)
print("1) BURUMUT ALS AMINOSÄURE-SEQUENZ")
print("=" * 80)
print()
print(f"  Total: {len(all_chars)} Buchstaben")
print(f"  Unique: {len(set(all_chars))}")
print()

# 2) Aminosäure-Verteilung
print("=" * 80)
print("2) AMINOSÄURE-VERTEILUNG")
print("=" * 80)
print()

counts = Counter(all_chars)
print(f"  {'Code':4s} {'Name':25s} {'Klasse':12s}  {'#':4s}  {'%':5s}")
print(f"  {'-'*4} {'-'*25} {'-'*12}  {'-'*4}  {'-'*5}")
for aa, count in sorted(counts.items(), key=lambda x: -x[1]):
    name, klasse = amino_acids.get(aa, ('?', '?'))
    pct = 100*count/len(all_chars)
    print(f"  {aa:4s} {name:25s} {klasse:12s}  {count:4d}  {pct:5.1f}%")
print()

# 3) Klassen-Statistik
print("=" * 80)
print("3) KLASSEN-KOMPOSITION")
print("=" * 80)
print()

classes = {
    'Basisch (R, K, H)': ['R', 'K', 'H'],
    'Sauer (D, E)': ['D', 'E'],
    'Polar (N, Q, S, T, Y)': ['N', 'Q', 'S', 'T', 'Y'],
    'Hydrophob (A, V, L, I, M, F, W, P, G, C)': ['A', 'V', 'L', 'I', 'M', 'F', 'W', 'P', 'G', 'C'],
    'Selten (O, U, J, B, Z)': ['O', 'U', 'J', 'B', 'Z'],
}

for cls, aas in classes.items():
    present = [aa for aa in aas if aa in counts]
    absent = [aa for aa in aas if aa not in counts]
    n_present = sum(counts[aa] for aa in present)
    pct = 100*n_present/len(all_chars)
    print(f"  {cls}:")
    print(f"    vorhanden: {present}  ({n_present} Vorkommen, {pct:.1f}%)")
    print(f"    fehlend:   {absent}")
print()

# 4) Fehlende Standard-Aminosäuren
print("=" * 80)
print("4) FEHLENDE STANDARD-AMINOSÄUREN")
print("=" * 80)
print()

standard_aa = 'ACDEFGHIKLMNPQRSTVWY'
missing = [aa for aa in standard_aa if aa not in counts]
print(f"  Im Standard-Code fehlend: {missing}")
print()
for aa in missing:
    name, klasse = amino_acids[aa]
    print(f"  {aa} = {name} ({klasse})")
print()

# 5) BURUMUT im Vergleich zu bekannten Proteinen
print("=" * 80)
print("5) VERGLEICH MIT BEKANNTEN PROTEINEN")
print("=" * 80)
print()

# Ein typisches Protein hat ca.:
# A 7-9%, R 5-6%, N 4%, D 5%, C 1-2%, E 6-7%, Q 4%, G 7-8%, H 2-3%, I 5-6%,
# L 9-11%, K 5-6%, M 2-3%, F 3-4%, P 4-5%, S 6-7%, T 5-6%, W 1%, Y 3%, V 6-7%

# BURUMUT hat:
# A 12.3% (HÖHER als normal 7-9%)
# U 11.7% (UNGEWÖHNLICH HOCH)
# R 7.8% (HÖHER als normal 5-6%)
# E 7.8% (HÖHER als normal 6-7%)
# O 7.8% (UNGEWÖHNLICH HOCH)
# C 0% (UNGEWÖHNLICH NIEDRIG, normal 1-2%)
# D 0% (UNGEWÖHNLICH NIEDRIG, normal 5%)
# Q 0% (UNGEWÖHNLICH NIEDRIG, normal 4%)
# V 0% (UNGEWÖHNLICH NIEDRIG, normal 6-7%)
# W 0% (UNGEWÖHNLICH NIEDRIG, normal 1%)

print("  Vergleich mit typischem Protein (% Differenz):")
typical = {
    'A': 8, 'C': 1.5, 'D': 5, 'E': 6.5, 'F': 3.5, 'G': 7.5, 'H': 2.5, 'I': 5.5,
    'K': 5.5, 'L': 10, 'M': 2.5, 'N': 4, 'P': 4.5, 'Q': 4, 'R': 5.5, 'S': 6.5,
    'T': 5.5, 'V': 6.5, 'W': 1, 'Y': 3,
}
print(f"  {'AA':4s} {'BURUMUT':>8s} {'Typisch':>8s} {'Δ':>8s}")
for aa, typ in sorted(typical.items()):
    bur = 100*counts.get(aa, 0)/len(all_chars)
    delta = bur - typ
    flag = ' ⬆' if delta > 2 else (' ⬇' if delta < -2 else '')
    print(f"  {aa:4s} {bur:8.1f} {typ:8.1f} {delta:+8.1f}{flag}")
print()

# 6) Biochemische Profile
print("=" * 80)
print("6) BIOCHEMISCHE PROFILE")
print("=" * 80)
print()

# Berechne basische/saure/hydrophobe/polare/sauren Index
# BURUMUT:
# basisch: R+K+H = 12+7+4 = 23 = 14.9%
# sauer: E+D = 12+0 = 12 = 7.8%
# polar: N+Q+S+T+Y = 10+0+7+6+4 = 27 = 17.5%
# hydrophob: A+L+I+M+F+P+G+V+W+C = 19+2+7+9+6+1+2+0+0+0 = 46 = 29.9%
# selten: O+U+B+Z+J = 12+18+10+6+0 = 46 = 29.9%

# Lade-Werte (charge at pH 7)
# R: +1, K: +1, H: +0.5, D: -1, E: -1
# N, Q, S, T, Y, C, M: 0
# A, F, G, I, L, V, W, P: 0
# Selenocystein (U): ähnlich C (0)
# Pyrrolysin (O): ähnlich K (+1)

burumut_charge = (
    counts.get('R', 0) * 1 +
    counts.get('K', 0) * 1 +
    counts.get('H', 0) * 0.5 +
    counts.get('D', 0) * -1 +
    counts.get('E', 0) * -1 +
    counts.get('O', 0) * 1  # Pyrrolysin ist Lysin-analog
)
print(f"  BURUMUT Nettoladung bei pH 7: {burumut_charge} (von {len(all_chars)} AS)")
print(f"  → BURUMUT ist BASISCH (Netto +{burumut_charge})")
print()

# 7) Suche nach bekannten Proteinen
print("=" * 80)
print("7) ÄHNLICHE BEKANNTE PROTEINE")
print("=" * 80)
print()

print("  BURUMUT-Profil:")
print("    - 154 Aminosäuren lang")
print("    - 12% Alanin (hoch)")
print("    - 12% Selenocystein (UNGEWÖHNLICH HOCH)")
print("    - 8% Pyrrolysin (UNGEWÖHNLICH HOCH)")
print("    - 8% Arginin (mittel-hoch)")
print("    - 8% Glutamat (mittel-hoch)")
print("    - 0% Cystein, Aspartat, Glutamin, Valin, Tryptophan")
print("    - Netto +23 basisch")
print()
print("  Ähnliche bekannte Proteine:")
print("    - Selenoprotein P (10 Sec in 381 AS = 2.6% Sec — VIEL weniger)")
print("    - Protamine (65% Arginin — viel mehr)")
print("    - Histone (~13% Arginin — ähnlich)")
print("    - KEIN bekanntes Protein hat 12% Selenocystein!")
print()

# 8) Die Amidin-Gruppen
print("=" * 80)
print("8) DIE AMIDIN-GRUPPEN: BIOCHEMISCHE BEDEUTUNG")
print("=" * 80)
print()

print("  p23_R4 enthält:")
print("    - HN=CH-NH-CH=NH (Di-Amidin)")
print("    - H2N-C=N-C-NH (Mono-Amidin)")
print()
print("  Beide enthalten das N-C-N-Rückgrat (Guanidin-/Amidin-Gruppe)")
print()
print("  Biochemische Vorkommen:")
print("    - Arginin (R) trägt eine Guanidin-Gruppe (Amidin-Gruppe)")
print("    - Die Amidin-Gruppe in BURUMUT ist möglicherweise die")
print("      Guanidin-Gruppe der 12 R-Vorkommen")
print()
print("  Klinische Bedeutung:")
print("    - Pentamidin, Propamidin, Stilbamidin: 4,4'-Diamidine")
print("    - Werden gegen Pneumocystis, Leishmania, Trypanosoma eingesetzt")
print("    - Wichtige Antimykotika/Antiprotozoika")
print()

# 9) JSON-Export
out = {
    'burumut_length': len(all_chars),
    'burumut_lines': burumut_lines,
    'aa_counts': dict(counts),
    'aa_percent': {aa: round(100*c/len(all_chars), 2) for aa, c in counts.items()},
    'missing_standard_aa': missing,
    'net_charge_ph7': burumut_charge,
    'classes': {cls: {'present': [aa for aa in aas if aa in counts], 'absent': [aa for aa in aas if aa not in counts], 'n': sum(counts[aa] for aa in aas if aa in counts)} for cls, aas in classes.items()},
}
with open(Path('/run/media/julian/ML4/tengri137/consecutive_research/scratches/stufe_13/burumut_aa.json'), 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\nJSON-Export: scratches/stufe_13/burumut_aa.json")
