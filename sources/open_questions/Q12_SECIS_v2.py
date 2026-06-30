"""
Q12 v2: SECIS-Strukturanalyse (ohne Nussinov, der zu langsam war)

Wir analysieren die mRNA aus Q10c mit vereinfachten Heuristiken.
"""
import re

# mRNA aus Q10c (Backtranslation)
mrna = ''
BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
codon_map = {
    'A': 'GCC', 'R': 'CGC', 'N': 'AAC', 'D': 'GAC', 'C': 'UGC',
    'E': 'GAG', 'Q': 'CAG', 'G': 'GGC', 'H': 'CAC', 'I': 'AUC',
    'L': 'CUG', 'K': 'AAG', 'M': 'AUG', 'F': 'UUC', 'P': 'CCG',
    'S': 'AGC', 'T': 'ACC', 'W': 'UGG', 'Y': 'UAC', 'V': 'GUG',
    'U': 'UGA', 'O': 'UAG', 'B': 'AAC', 'Z': 'CAG'
}
for aa in BURUMUT_FULL:
    mrna += codon_map[aa]

# Wichtige Positionen
sec_pos_mRNA = [3, 9, 15, 39, 45, 57, 72, 96, 138, 198, 240]
uazbe_sec = [96, 138, 198, 240]  # UAZBE
other_sec = [3, 9, 15, 39, 45, 57, 72]
pyl_pos = [156, 258]
auga_pos = [33, 159, 261]

print("="*70)
print("Q12 v2.1: SECIS-Element-Struktur")
print("="*70)
print(f"mRNA: {len(mrna)} Basen")
print()

# Kontext um jedes AUGA
print("Kontext-AUGA-Motive in mRNA (30 Basen Kontext):")
for i, auga in enumerate(auga_pos):
    before = mrna[max(0, auga-20):auga]
    after = mrna[auga+4:min(len(mrna), auga+24)]
    print(f"\n  SECIS #{i+1} an mRNA-Pos {auga}:")
    print(f"    5' ({len(before)} nt): {before}")
    print(f"    AUGA:                 {mrna[auga:auga+4]}")
    print(f"    3' ({len(after)} nt): {after}")

# Welche UGA werden von welchen AUGA dirigiert?
print()
print("="*70)
print("Q12 v2.2: SECIS-UGA-Zuordnung")
print("="*70)
# SECIS dirigiert alle UGA downstream bis zum naechsten Stop
# Wir sortieren SECIS-Kandidaten und UGA
sorted_uga = sorted(sec_pos_mRNA)
sorted_auga = sorted(auga_pos)
sorted_pyl = sorted(pyl_pos)
all_stops = sorted_uga + sorted_pyl + [len(mrna)]

# Baue eine Karte: welcher UGA wird von welchem SECIS dirigiert?
secis_to_uga = {auga: [] for auga in sorted_auga}
for ug in sorted_uga:
    # finde das naechste SECIS upstream
    upstream_secis = [a for a in sorted_auga if a < ug]
    if upstream_secis:
        # Naechstes (groesstes) upstream SECIS, das noch nicht 'verbraucht' ist
        # Vereinfachung: der letzte upstream SECIS
        closest = upstream_secis[-1]
        secis_to_uga[closest].append(ug)

print("SECIS dirigiert diese UGA-Codons:")
for secis, ugas in secis_to_uga.items():
    if ugas:
        print(f"  AUGA@{secis}: UGA@{ugas} ({len(ugas)} Codons)")
    else:
        print(f"  AUGA@{secis}: keine UGA-Codons")
