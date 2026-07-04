"""
Q14 (NEU): Welche 7 Buchstaben fehlen in BURUMUT?

BURUMUT-Alphabet: 19 distinkte Buchstaben (von 26)
Lateinisches Alphabet: 26 Buchstaben
Fehlen in BURUMUT: 7 Buchstaben

Welche 7?
"""
BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Welche Buchstaben fehlen?
all_letters = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
present = set(BURUMUT_FULL)
missing = sorted(all_letters - present)
present_sorted = sorted(present)

print("="*70)
print("Q14.1: Welche 7 Buchstaben fehlen in BURUMUT?")
print("="*70)
print(f"Vorhanden ({len(present_sorted)}): {present_sorted}")
print(f"Fehlend ({len(missing)}): {missing}")
print()

# Welche Aminosaeuren entsprechen den fehlenden Buchstaben?
amino_standard = {
    'A': 'Ala', 'R': 'Arg', 'N': 'Asn', 'D': 'Asp', 'C': 'Cys',
    'E': 'Glu', 'Q': 'Gln', 'G': 'Gly', 'H': 'His', 'I': 'Ile',
    'L': 'Leu', 'K': 'Lys', 'M': 'Met', 'F': 'Phe', 'P': 'Pro',
    'S': 'Ser', 'T': 'Thr', 'W': 'Trp', 'Y': 'Tyr', 'V': 'Val',
}
print("IUPAC-Standard-Aminosaeuren, die in BURUMUT fehlen:")
for letter in missing:
    name = amino_standard.get(letter, f"Platzhalter ({letter})")
    print(f"  {letter}: {name}")

# Andere wichtige Codes
print()
print("="*70)
print("Q14.2: Welche Codes haben 19 Symbole?")
print("="*70)

# 19-Buchstaben-Alphabete
codes_19 = {
    'DNA-Standard (A, C, G, T)': 4,
    'RNA-Standard (A, C, G, U)': 4,
    'Protein-Standard (20 AS)': 20,
    'Protein + B + Z (22 AS)': 22,
    'IUPAC-Nucleinsaeure-Code (15 Symbole)': 15,
    'IUPAC-Nucleinsaeure mit Luecken (18)': 18,
    'Morse-Code (Buchstaben + Zahlen)': 36,
    'Baudot (5-Bit)': 32,
    'Hexadezimal': 16,
    'Base64': 64,
    'Latein (ohne K, W, X)': 23,
    'BURUMUT (speziell?)': 19,
}

# 19 spezielle Codes?
# Suche in der Liste nach "19"
special_19 = [
    ('Bio-Alphabet', 'A, C, G, T (4) -> 19 nicht'),
    ('Trigramm-Alphabet', '32^3 = 32768 Symbole (zu viel)'),
    ('Genetisches Codesystem', '1-64 Codons'),
    ('Asx+Glx+Sec+Pyl+15 Standard', 4 + 20 = 24 (zu viel)'),
]

# Genau 19: Welche Systeme?
print("Alphabete/Code mit genau 19 Symbolen:")
print("  Base64 hat 64 Symbole (nicht 19)")
print("  Hexadezimal hat 16 (nicht 19)")
print("  Lateinisches Alphabet minus K, W, X = 23 (nicht 19)")
print("  Lateinisches Alphabet minus D, J, K, V, W, X, Y = 19")
print("  BURUMUT fehlen: C, D, F (fast), G (fast), J, K, V")
print(f"  Bestaetigung: {set('CDFGJKV') - set(BURUMUT_FULL)}")
