"""
Q10 (NEU): BURUMUT -> DNA Rückübersetzung

Wenn BURUMUT ein Protein ist, dann können wir die zugehörige
DNA-Sequenz zurückrechnen. Allerdings:
- BURUMUT enthält Selenocystein (U), das über UGA-Codon eingebaut wird
- B (Asx) und Z (Glx) sind unscharf - sie können Asn/Asp bzw. Gln/Glu sein
- O (Pyl, Pyrrolysine) wird über UAG eingebaut

Wir berechnen die wahrscheinlichsten DNA-Codons für jede Aminosäure
und vergleichen die Konsensus-Sequenz mit bekannten Genomen.
"""
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Standard Codon-Tabelle (mRNA → Aminosäure)
# Wir verwenden E. coli codon-usage für die häufigsten Codons
CODON_TABLE = {
    'A': ['GCU', 'GCC', 'GCA', 'GCG'],   # Ala
    'R': ['CGU', 'CGC', 'CGA', 'CGG', 'AGA', 'AGG'],
    'N': ['AAU', 'AAC'],
    'D': ['GAU', 'GAC'],
    'C': ['UGU', 'UGC'],
    'E': ['GAA', 'GAG'],
    'Q': ['CAA', 'CAG'],
    'G': ['GGU', 'GGC', 'GGA', 'GGG'],
    'H': ['CAU', 'CAC'],
    'I': ['AUU', 'AUC', 'AUA'],
    'L': ['UUA', 'UUG', 'CUU', 'CUC', 'CUA', 'CUG'],
    'K': ['AAA', 'AAG'],
    'M': ['AUG'],
    'F': ['UUU', 'UUC'],
    'P': ['CCU', 'CCC', 'CCA', 'CCG'],
    'S': ['UCU', 'UCC', 'UCA', 'UCG', 'AGU', 'AGC'],
    'T': ['ACU', 'ACC', 'ACA', 'ACG'],
    'W': ['UGG'],
    'Y': ['UAU', 'UAC'],
    'V': ['GUU', 'GUC', 'GUA', 'GUG'],
    'U': ['UGA'],   # Sec - recodierter Stop
    'O': ['UAG'],   # Pyl - recodierter Stop
    'B': ['AAU', 'AAC', 'GAU', 'GAC'],  # Asn ODER Asp
    'Z': ['CAA', 'CAG', 'GAA', 'GAG'],  # Gln ODER Glu
}

# E. coli Codon-Häufigkeiten (für jedes Codon)
ECOLI_CODON_FREQ = {
    'A': {'GCU': 0.27, 'GCC': 0.25, 'GCA': 0.23, 'GCG': 0.25},
    'R': {'CGU': 0.36, 'CGC': 0.36, 'CGA': 0.07, 'CGG': 0.07, 'AGA': 0.07, 'AGG': 0.04},
    'N': {'AAU': 0.49, 'AAC': 0.51},
    'D': {'GAU': 0.63, 'GAC': 0.37},
    'C': {'UGU': 0.45, 'UGC': 0.55},
    'E': {'GAA': 0.68, 'GAG': 0.32},
    'Q': {'CAA': 0.34, 'CAG': 0.66},
    'G': {'GGU': 0.34, 'GGC': 0.40, 'GGA': 0.13, 'GGG': 0.13},
    'H': {'CAU': 0.57, 'CAC': 0.43},
    'I': {'AUU': 0.49, 'AUC': 0.39, 'AUA': 0.11},
    'L': {'UUA': 0.14, 'UUG': 0.13, 'CUU': 0.13, 'CUC': 0.10, 'CUA': 0.04, 'CUG': 0.46},
    'K': {'AAA': 0.74, 'AAG': 0.26},
    'M': {'AUG': 1.0},
    'F': {'UUU': 0.57, 'UUC': 0.43},
    'P': {'CCU': 0.18, 'CCC': 0.13, 'CCA': 0.20, 'CCG': 0.49},
    'S': {'UCU': 0.17, 'UCC': 0.15, 'UCA': 0.14, 'UCG': 0.15, 'AGU': 0.16, 'AGC': 0.25},
    'T': {'ACU': 0.19, 'ACC': 0.40, 'ACA': 0.17, 'ACG': 0.25},
    'W': {'UGG': 1.0},
    'Y': {'UAU': 0.59, 'UAC': 0.41},
    'V': {'GUU': 0.28, 'GUC': 0.20, 'GUA': 0.15, 'GUG': 0.37},
}

# Eukaryont (Mensch) Codon-Häufigkeiten
HUMAN_CODON_FREQ = {
    'A': {'GCU': 0.27, 'GCC': 0.40, 'GCA': 0.23, 'GCG': 0.11},
    'R': {'CGU': 0.09, 'CGC': 0.19, 'CGA': 0.13, 'CGG': 0.21, 'AGA': 0.21, 'AGG': 0.21},
    'N': {'AAU': 0.47, 'AAC': 0.53},
    'D': {'GAU': 0.46, 'GAC': 0.54},
    'C': {'UGU': 0.46, 'UGC': 0.54},
    'E': {'GAA': 0.42, 'GAG': 0.58},
    'Q': {'CAA': 0.27, 'CAG': 0.73},
    'G': {'GGU': 0.16, 'GGC': 0.34, 'GGA': 0.25, 'GGG': 0.25},
    'H': {'CAU': 0.42, 'CAC': 0.58},
    'I': {'AUU': 0.36, 'AUC': 0.47, 'AUA': 0.17},
    'L': {'UUA': 0.07, 'UUG': 0.13, 'CUU': 0.13, 'CUC': 0.20, 'CUA': 0.07, 'CUG': 0.41},
    'K': {'AAA': 0.43, 'AAG': 0.57},
    'M': {'AUG': 1.0},
    'F': {'UUU': 0.46, 'UUC': 0.54},
    'P': {'CCU': 0.29, 'CCC': 0.32, 'CCA': 0.28, 'CCG': 0.11},
    'S': {'UCU': 0.19, 'UCC': 0.22, 'UCA': 0.15, 'UCG': 0.05, 'AGU': 0.15, 'AGC': 0.24},
    'T': {'ACU': 0.25, 'ACC': 0.36, 'ACA': 0.28, 'ACG': 0.11},
    'W': {'UGG': 1.0},
    'Y': {'UAU': 0.44, 'UAC': 0.56},
    'V': {'GUU': 0.18, 'GUC': 0.24, 'GUA': 0.12, 'GUG': 0.46},
}

def backtranslate(seq, codon_freq):
    """Konvertiere Protein-Sequenz zu DNA-Sequenz mit haeufigstem Codon."""
    dna = ''
    for aa in seq:
        if aa in codon_freq:
            # Waehle das haeufigste Codon
            codons = codon_freq[aa]
            best_codon = max(codons, key=codons.get)
            dna += best_codon
        elif aa == 'B':
            # Asx: mittlere Frequenz aus Asn und Asp
            for c in codon_freq.get('N', {}): dna += c[0]
            for c in codon_freq.get('D', {}): dna += c[0]
        elif aa == 'Z':
            for c in codon_freq.get('Q', {}): dna += c[0]
            for c in codon_freq.get('E', {}): dna += c[0]
        elif aa == 'U':
            dna += 'UGA'  # Sec
        elif aa == 'O':
            dna += 'UAG'  # Pyl
        else:
            dna += 'NNN'
    return dna

print("="*70)
print("Q10.1: BURUMUT -> DNA Rueckuebersetzung")
print("="*70)

# E. coli Version
dna_ecoli = backtranslate(BURUMUT_FULL, ECOLI_CODON_FREQ)
print(f"E. coli Codon-Verwendung:")
print(f"  DNA-Laenge: {len(dna_ecoli)} Basen")
print(f"  DNA-Sequenz (erste 99):")
for i in range(0, min(len(dna_ecoli), 99), 33):
    print(f"    {i:3d}: {dna_ecoli[i:i+33]}")
print()

# Human Version
dna_human = backtranslate(BURUMUT_FULL, HUMAN_CODON_FREQ)
print(f"Menschlicher Codon-Verwendung:")
print(f"  DNA-Laenge: {len(dna_human)} Basen")
print(f"  DNA-Sequenz (erste 99):")
for i in range(0, min(len(dna_human), 99), 33):
    print(f"    {i:3d}: {dna_human[i:i+33]}")
print()

# Beide vergleichen
print("="*70)
print("Q10.2: Vergleich E.coli vs Mensch")
print("="*70)
diffs = sum(1 for a, b in zip(dna_ecoli, dna_human) if a != b)
print(f"Unterschiedliche Basen: {diffs}/{len(dna_ecoli)} = {diffs/len(dna_ecoli)*100:.1f}%")

# GC-Gehalt
def gc_content(seq):
    g = seq.count('G')
    c = seq.count('C')
    return (g + c) / len(seq) * 100 if seq else 0

print(f"GC-Gehalt (E.coli): {gc_content(dna_ecoli):.1f}%")
print(f"GC-Gehalt (Mensch): {gc_content(dna_human):.1f}%")
print(f"E.coli-Durchschnitt: ~50.8%")
print(f"Mensch-Durchschnitt: ~52.5%")

# Suche nach auffaelligen Mustern
print()
print("="*70)
print("Q10.3: Struktur der rueckuebersetzten DNA")
print("="*70)

# Stop-Codons in der Sequenz?
stops = ['TAA', 'TAG', 'TGA']  # DNA-Schreibweise
for i in range(0, len(dna_ecoli) - 2, 3):
    codon = dna_ecoli[i:i+3]
    if codon in stops:
        print(f"  Stop-Codon an Position {i//3}: {codon}")

# Aber: Sec braucht UGA. Wenn UGA als Sec recodiert wird,
# ist es KEIN Stop im Protein-Kontext.
# Schauen wir, wo UGA (Sec) vorkommt
uga_pos = []
for i in range(0, len(dna_ecoli) - 2, 3):
    if dna_ecoli[i:i+3] == 'TGA':  # DNA-Codon = UGA in RNA
        uga_pos.append(i // 3)
print(f"\nUGA (Sec-Codon) Positionen: {uga_pos}")
print(f"  BURUMUT hat 11 Sec, wir erwarten 11 UGA")

# Aber: BURUMUT hat auch Pyl (O), das ist UAG in mRNA
# Schauen wir UAG
uag_pos = []
for i in range(0, len(dna_ecoli) - 2, 3):
    if dna_ecoli[i:i+3] == 'TAG':
        uag_pos.append(i // 3)
print(f"\nUAG (Pyl-Codon) Positionen: {uag_pos}")
print(f"  BURUMUT hat 2 O, wir erwarten 2 UAG")

# UAA?
uaa_pos = []
for i in range(0, len(dna_ecoli) - 2, 3):
    if dna_ecoli[i:i+3] == 'TAA':
        uaa_pos.append(i // 3)
print(f"\nUAA (echter Stop) Positionen: {uaa_pos}")
print(f"  Wenn vorhanden: realer Stop-Codon")
