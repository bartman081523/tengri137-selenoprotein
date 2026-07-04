"""
Q20 (NEU): BURUMUT vs DNA-Sequenzen gleicher Laenge

Wenn BURUMUT eine mRNA- oder DNA-Projektion ist, sollte sie
gewisse DNA-Statistiken aufweisen.

Wir testen:
1. GC-Gehalt (eukaryotisch ~50%)
2. CpG-Island-Haeufigkeit
3. Hairpin-Stabilitaet (Sekundaerstruktur)
4. Codon-Usage-Bias (wenn mRNA)
5. Open Reading Frame (ORF) Vorhersage
"""
import random
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Wir brauchen eine DNA-Repraesentation
# BURUMUT-19-Buchstaben -> DNA 4-Buchstaben (Mapping)
# Strategie: 2-Bit-Codierung der 19 Buchstaben
# 19 = nicht direkt 2^n, aber wir koennen es auf 4-Basen mappen

# Einfache Variante: Map basierend auf Haeufigkeit
freq = Counter(BURUMUT_FULL)
sorted_chars = sorted(freq.keys(), key=lambda c: (-freq[c], c))
base_map = {ch: 'ACGT'[i % 4] for i, ch in enumerate(sorted_chars)}

def to_dna(seq, mapping):
    return ''.join(mapping[ch] for ch in seq)

dna_seq = to_dna(BURUMUT_FULL, base_map)

print("="*70)
print("Q20.1: BURUMUT -> DNA (4-Buchstaben-Mapping)")
print("="*70)
print(f"BURUMUT: {BURUMUT_FULL}")
print(f"DNA:     {dna_seq}")
print(f"Laenge: {len(dna_seq)} Basen")
print(f"GC-Gehalt: {(dna_seq.count('G') + dna_seq.count('C'))/len(dna_seq)*100:.1f}%")
print(f"AT-Gehalt: {(dna_seq.count('A') + dna_seq.count('T'))/len(dna_seq)*100:.1f}%")

# 2. CpG-Island
print()
print("="*70)
print("Q20.2: CpG-Island-Suche")
print("="*70)
cpg_count = 0
for i in range(len(dna_seq) - 1):
    if dna_seq[i:i+2] == 'CG':
        cpg_count += 1
print(f"Anzahl 'CG' in DNA: {cpg_count}")
print(f"Erwartung bei Zufall: ~{len(dna_seq)*0.0625:.0f}")
# In Saeuger-DNA: CG ist unterrepraesentiert (Methylierung)
# In CpG-Inseln: CG ist haeufig

# 3. Hairpin-Suche (invers-repeats)
print()
print("="*70)
print("Q20.3: Hairpin / Stem-Loop-Suche")
print("="*70)
comp = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
hairpins = []
for i in range(len(dna_seq)):
    for j in range(i+6, min(i+30, len(dna_seq))):  # min loop = 4
        # Check if seq[i:j] could be a stem
        stem_len = min(j-i, len(dna_seq)-j)
        if stem_len >= 3:
            stem5 = dna_seq[i:i+stem_len]
            stem3 = dna_seq[j:j+stem_len]
            if all(stem5[k] == comp.get(stem3[stem_len-1-k], '?') for k in range(stem_len)):
                loop = dna_seq[i+stem_len:j]
                hairpins.append((i, j, stem5, loop, stem3))
print(f"Anzahl moeglicher Hairpins: {len(hairpins)}")
for h in hairpins[:5]:
    print(f"  Pos {h[0]}-{h[1]+len(h[4])}: 5'-{h[2]}...{h[3]}...{h[4]}-3'")

# 4. Wenn BURUMUT ein Protein ist: Wo ist das Start-Codon?
# In mRNA: AUG (Methionin) ist Start
# In BURUMUT sind die M-Positionen (Methionin):
m_positions = [i for i, c in enumerate(BURUMUT_FULL) if c == 'M']
print()
print("="*70)
print("Q20.4: Mögliche Start-Codons (Methionin)")
print("="*70)
print(f"Methionin (M) Positionen: {m_positions}")
# Wenn BURUMUT ein Protein mit einem Start-Methionin ist, sollte
# die erste Position ein M sein.
print(f"Erste Position BURUMUT[0] = {BURUMUT_FULL[0]}")
print(f"Wenn Protein mit M beginnt: BURUMUT[0] = M? {BURUMUT_FULL[0] == 'M'}")
# BURUMUT beginnt NICHT mit M. Falls Protein, fehlt der Start-M.

# 5. Falls BURUMUT eine mRNA-Projektion ist, suchen wir nach dem
# offenen Leserahmen
print()
print("="*70)
print("Q20.5: Offene Leserahmen (ORF) Suche")
print("="*70)
# Standard Stop-Codons: UAA, UAG, UGA
# In BURUMUT (Protein-Alphabet): O = Pyl (UAG) und U = Sec (UGA)
# Falls UAG/UGA echte Stops sind: BURUMUT hat 2+11 = 13 Stops
# Falls Sec/Pyl: kein Stop, ein einziges Polypeptid

# Wenn 2 UAG Stops und 11 UGA Sec:
# 2 Polypeptide: Pos 0-52 (bis UAG an Pos 52) und Pos 53-85
# und Pos 86-98 (nach UAG an Pos 86)

# Wenn alle UAG+UGA Sec/Pyl:
# Ein einziges Polypeptid von 99 AS

# Tatsaechlich: Wenn man die mRNA aus Q10 anschaut:
# UGA = Sec (11 Stops aber recodiert)
# UAG = Pyl (2 Stops aber recodiert)
# Kein echter Stop-Codon
# -> BURUMUT = ein einziges Polypeptid ohne Stop?

# Aber: In echten Sec-Proteinen gibt es einen TERMINAL-Stop nach der Sec.
# Wo ist er in BURUMUT?

# Wir suchen nach "ASX" am Ende (Stop-Analogon)
print(f"Letzte 5 Zeichen von BURUMUT: '{BURUMUT_FULL[-5:]}'")
