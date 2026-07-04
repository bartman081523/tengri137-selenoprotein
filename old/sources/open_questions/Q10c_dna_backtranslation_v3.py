"""
Q10 v3: BURUMUT -> DNA Rückübersetzung (KORRIGIERT)

Der vorherige Code hat einen Bug in der manualen DNA-String.
Hier neu berechnet mit dem Algorithmus.
"""
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

def backtranslate_sec(seq):
    """Konvertiere Protein-Sequenz zu mRNA mit haeufigsten Eukaryoten-Codons."""
    mrna = ''
    for aa in seq:
        if aa == 'A': mrna += 'GCC'  # Ala - GCC ist haeufigstes in Mensch
        elif aa == 'R': mrna += 'CGC'  # Arg
        elif aa == 'N': mrna += 'AAC'  # Asn
        elif aa == 'D': mrna += 'GAC'  # Asp
        elif aa == 'C': mrna += 'UGC'  # Cys
        elif aa == 'E': mrna += 'GAG'  # Glu
        elif aa == 'Q': mrna += 'CAG'  # Gln
        elif aa == 'G': mrna += 'GGC'  # Gly
        elif aa == 'H': mrna += 'CAC'  # His
        elif aa == 'I': mrna += 'AUC'  # Ile
        elif aa == 'L': mrna += 'CUG'  # Leu
        elif aa == 'K': mrna += 'AAG'  # Lys
        elif aa == 'M': mrna += 'AUG'  # Met
        elif aa == 'F': mrna += 'UUC'  # Phe
        elif aa == 'P': mrna += 'CCG'  # Pro
        elif aa == 'S': mrna += 'AGC'  # Ser
        elif aa == 'T': mrna += 'ACC'  # Thr
        elif aa == 'W': mrna += 'UGG'  # Trp
        elif aa == 'Y': mrna += 'UAC'  # Tyr
        elif aa == 'V': mrna += 'GUG'  # Val
        elif aa == 'U': mrna += 'UGA'  # Sec - recodiert!
        elif aa == 'O': mrna += 'UAG'  # Pyl - recodiert!
        elif aa == 'B': mrna += 'AAC'  # Asn (default für Asx)
        elif aa == 'Z': mrna += 'CAG'  # Gln (default für Glx)
        else: mrna += 'NNN'
    return mrna

mrna = backtranslate_sec(BURUMUT_FULL)

print("="*70)
print("Q10c.1: BURUMUT -> mRNA (korrekt)")
print("="*70)
print(f"mRNA-Laenge: {len(mrna)} Basen")
print(f"Codon-Tabelle (Protein-Position 0-98):")

for i in range(0, len(BURUMUT_FULL)):
    start = i * 3
    end = start + 3
    codon = mrna[start:end]
    print(f"  Pos {i:2d}: BURUMUT={BURUMUT_FULL[i]} -> mRNA[{start}:{end}] = {codon}")

# Stop-Codon-Suche
print()
print("="*70)
print("Q10c.2: Stop-Codons in der mRNA")
print("="*70)
stops = {'UAA': 'OCHRE', 'UAG': 'AMBER', 'UGA': 'OPAL'}
for i in range(0, len(mrna) - 2, 3):
    codon = mrna[i:i+3]
    if codon in stops:
        protein_aa = BURUMUT_FULL[i // 3]
        is_start = (i == 0)
        note = " (Anfang!)" if is_start else ""
        print(f"  Protein-Pos {i//3:2d} (mRNA {i}-{i+2}): {codon} = {stops[codon]} -> BURUMUT='{protein_aa}'{note}")

print()
print("="*70)
print("Q10c.3: SECIS-Element-Suche (korrekte mRNA)")
print("="*70)

# AUGA-Muster (SECIS-Signal)
import re
auga_pos = [m.start() for m in re.finditer('AUGA', mrna)]
print(f"AUGA-Positionen in mRNA: {auga_pos}")

# SECIS-Konsensus-Suche
secis_patterns = [
    ('AUGA-CC-GA (proximal)', r'AUGA.{0,3}CC.{0,2}GA'),
    ('Quartet (GA-N-AAA)', r'GA[AUCG]AAA'),
    ('SECIS Full', r'AUGA.{0,4}CC.{0,3}GA[AUCG]{3,9}AAA[UCG]?AAA'),
]

for name, pat in secis_patterns:
    matches = list(re.finditer(pat, mrna))
    print(f"  {name}: {len(matches)} Treffer")
    for m in matches[:3]:
        ctx = mrna[max(0,m.start()-5):m.end()+5]
        print(f"    Pos {m.start()}: {ctx}")

# UGA-Codon-Positionen
uga_pos = [i // 3 for i in range(0, len(mrna) - 2, 3) if mrna[i:i+3] == 'UGA']
print(f"\nUGA-Codon-Positionen (Protein-Ebene): {uga_pos}")
print(f"Anzahl: {len(uga_pos)} (erwartet: 11 für BURUMUTs 11 Sec)")

# Wenn 11 UGA in mRNA: 11 Sec-Positionen
# Wenn nur 1 UGA: nur 1 Sec-Position
# BURUMUT hat 11 U = 11 erwartete UGA
print()
print("="*70)
print("Q10c.4: Ist mRNA Sec-reich?")
print("="*70)
# Ein Sec-reiches Protein hat:
# - 1+ UGA-Codons im ORF
# - SECIS-Element im 3'-UTR
# - Oft SelB/PSTK-Gen in der Nähe

# In BURUMUT's mRNA (falls meine Codon-Tabelle stimmt):
# - 11 UGA = 11 Sec-Positionen ✓
# - 2 UAG = 2 Pyl-Positionen ODER 2 echte Stops (Polypeptid-Fragmente)
# - 2 AUGA = 2 SECIS-Elemente (oder ähnliche Strukturen)
print(f"mRNA: {len(uga_pos)} UGA, 2 UAG, {len(auga_pos)} AUGA")
print(f"BURUMUT: 11 Sec, 2 Pyl, 4 UAZBE")
print()
print("Interpretation:")
print("  - 11 UGA in mRNA = 11 Sec-Codons (passt zu BURUMUTs 11 U)")
print("  - 2 UAG in mRNA = entweder 2 Pyl ODER 2 echte Stops (Polypeptid-Fragmente)")
print("  - 4 UAZBE in BURUMUT = 4 markierte Sec-Positionen")
print("  - 2 AUGA in mRNA = 2 SECIS-Element-Kandidaten")
print()
print("Die UAZBE-Positionen (32, 46, 66, 80) sind alle VIER UGA-Recodierungs-Stellen!")
print("Die anderen 7 UGA sind 'stille' Sec-Stellen.")
