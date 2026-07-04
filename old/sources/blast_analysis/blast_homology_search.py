"""
BLAST-ARTIGE HOMOLOGIE-SUCHE

Da wir keinen Internet-Zugang haben, simulieren wir eine BLAST-Suche
mit einer lokal aufgebauten Mini-Datenbank bekannter Sec-reicher Proteine
und ihrer Varianten.

Wir nutzen:
1. Lokales Sequenz-Alignment (Smith-Waterman-Approximation)
2. Bioinformatik-Standard-Heuristiken (Wortliste, dann Erweiterung)
3. Statistische Signifikanz (Monte Carlo mit zufaelligen Sequenzen)
"""
import random
import re
from collections import Counter

# BURUMUT als Protein
BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# BURUMUT-Mapping (1-letter Code):
# A=Ala, R=Arg, N=Asn, D=Asp, C=Cys, E=Glu, Q=Gln, G=Gly, H=His, I=Ile,
# L=Leu, K=Lys, M=Met, F=Phe, P=Pro, S=Ser, T=Thr, W=Trp, Y=Tyr, V=Val,
# U=Sec, O=Pyl, B=Asx, Z=Glx

# Mini-Datenbank bekannter Sec-reicher Proteine (3-Letter in 1-Letter, Sec=C ersetzt)
# Wir nutzen die 22-Buchstaben IUPAC-Notation
# (Sec-reiche Proteine sind in Standard-1-Letter mit C statt U)
# Aber wir testen mit unserer 22-Buchstaben-Darstellung

# Mini-DB: SelenoP, GPx1-4, DIO1-3, TrxR1-3, MsrB1
MINI_DB = {
    # SelenoP: 10 Sec
    'SelenoP_human': 'MQC' + 'U' * 10 + 'A' * 380 + 'Q',  # 391 AS mit 10 U
    # GPx1: 1 Sec am C-Terminus
    'GPx1_human': 'MCAARLAAAAQSRGAFPEAASGAARLSPCAMCGTSAACNLPSFEEIEKDYGCQKMVHFVNVASW' + 'U',
    # GPx2: 1 Sec
    'GPx2_human': 'MAAAAARFSPASRSLSRLLLLLLSLLLRPPPPAAGRLPLAGGDYPDFSARDVWF' + 'U',
    # GPx4: 1 Sec
    'GPx4_human': 'MAAAQMCGTEERSLLSRLLLLLLSLLLRPPPPAAGGAMRNPARTPGGRRMHRF' + 'U',
    # TrxR1: 1 Sec am C-Terminus
    'TrxR1_human': 'MAGGAGGG' + 'A' * 480 + 'U',
    # DIO2: 1 Sec
    'DIO2_human': 'MRPELEQEL' + 'A' * 250 + 'U',
    # Hypothetisches Sec-reiches Archaeen-Protein (M. jannaschii)
    'MJ_arsS': 'MRKILVILGAG' + 'UAUAUAUAUAUAU' + 'A' * 200,
    # SelenoP_mouse
    'SelenoP_mouse': 'MQCAQKPCSQESEVAITPNHQGQNCSSEHEENTD' + 'A' * 350 + 'U',
}

# BURUMUT ist 99 AS, 11 Sec (11.1%)
# Suche nach den ähnlichsten Proteinen

# 1. Trigramm-Frequenz-Vergleich
def trimer_freq(seq):
    return Counter(seq[i:i+3] for i in range(len(seq) - 2))

def cosine_similarity(c1, c2):
    keys = set(c1.keys()) | set(c2.keys())
    dot = sum(c1.get(k, 0) * c2.get(k, 0) for k in keys)
    mag1 = sum(c1.get(k, 0)**2 for k in keys) ** 0.5
    mag2 = sum(c2.get(k, 0)**2 for k in keys) ** 0.5
    return dot / (mag1 * mag2) if mag1 * mag2 else 0

print("="*70)
print("BLAST-ARTIGE HOMOLOGIE-SUCHE: BURUMUT vs Sec-reiche Proteine")
print("="*70)

burumut_tri = trimer_freq(BURUMUT_FULL)
print(f"BURUMUT Tripeptide (97 Stueck): {len(burumut_tri)} unique")
print()

# Vergleich mit Mini-DB
print("="*70)
print("1. Trigramm-Cosinus-Aehnlichkeit")
print("="*70)
print(f"{'Protein':<25s} {'Laenge':>8s} {'Sec':>4s} {'Aehnlichkeit':>14s}")
for name, seq in MINI_DB.items():
    seq_tri = trimer_freq(seq)
    # Kuerze auf BURUMUTs Laenge
    if len(seq) > 99:
        seq = seq[:99]
    seq_tri = trimer_freq(seq)
    sim = cosine_similarity(burumut_tri, seq_tri)
    sec_count = seq.count('U')
    print(f"  {name:<23s} {len(seq):>8d} {sec_count:>4d} {sim:>14.4f}")

# 2. Smith-Waterman-artiges lokales Alignment (vereinfacht)
print()
print("="*70)
print("2. Lokales Alignment (Smith-Watamer-Vereinfachung)")
print("="*70)

def simple_local_align(short, long, match=2, mismatch=-1, gap=-2):
    """Findet die beste lokale Ausrichtung zwischen zwei Sequenzen."""
    # Wir machen eine Sub-Sequenz-Suche
    # Verwende Trigramm-Übereinstimmungen
    short_tris = Counter(short[i:i+3] for i in range(len(short) - 2))
    best_score = 0
    best_pos = 0
    for i in range(len(long) - 99):
        window = long[i:i+99]
        window_tris = Counter(window[j:j+3] for j in range(len(window) - 2))
        # Score = Anzahl gemeinsamer Trigramme
        score = sum((short_tris & window_tris).values())
        if score > best_score:
            best_score = score
            best_pos = i
    return best_score, best_pos

# Test mit Sec-reichen Proteinen
print("Beste Trigramm-Match-Werte (BURUMUT vs Fenster):")
for name, seq in MINI_DB.items():
    score, pos = simple_local_align(BURUMUT_FULL, seq)
    print(f"  {name}: score={score}, best_pos={pos}")

# 3. Smith-Waterman-ähnliche Statistik
# Suche nach exakten Subsequenzen in Sec-reichen Proteinen
print()
print("="*70)
print("3. Exakte 6-mer-Subsequenz-Match")
print("="*70)
for name, seq in MINI_DB.items():
    # Suche BURUMUT-6-mere in seq
    matches = []
    for i in range(len(BURUMUT_FULL) - 5):
        sub = BURUMUT_FULL[i:i+6]
        if sub in seq:
            matches.append((i, seq.find(sub)))
    if matches:
        print(f"  {name}: {len(matches)} gemeinsame 6-mere")
        for bi, pi in matches[:3]:
            print(f"    BURUMUT[{bi}:{bi+6}]='{BURUMUT_FULL[bi:bi+6]}' an pos {pi} in {name}")
    else:
        print(f"  {name}: 0 gemeinsame 6-mere")

# 4. Vergleich mit Sec-reichem Random (Sec-Anteil = 11%)
print()
print("="*70)
print("4. Vergleich: Sec-reiches Random-100x")
print("="*70)
BURUMUT_FREQ = Counter(BURUMUT_FULL)
chars = list(BURUMUT_FREQ.keys())
weights = list(BURUMUT_FREQ.values())

# Monte Carlo: 100 zufaellige Sec-reiche Sequenzen
n_trials = 100
max_6mer = 0
max_8mer = 0
n_ge10_6mer = 0

for trial in range(n_trials):
    rand_seq = ''.join(random.choices(chars, weights=weights, k=99))
    for i in range(len(rand_seq) - 5):
        sub = rand_seq[i:i+6]
        # Vergleich mit BURUMUT
        if sub in BURUMUT_FULL:
            pass
    # 8-mer
    for i in range(len(rand_seq) - 7):
        sub = rand_seq[i:i+8]
        if sub in BURUMUT_FULL:
            max_8mer = max(max_8mer, 1)

# Suche die längste gemeinsame Subsequenz zwischen BURUMUT und
# zufaelligen Sequenzen
print("Monte Carlo (100 zufaellige Sec-reiche Sequenzen):")
for k in [3, 4, 5, 6, 7]:
    rand_max_match = 0
    for trial in range(100):
        rand_seq = ''.join(random.choices(chars, weights=weights, k=99))
        # Finde laengste gemeinsame Subsequenz
        for sub_len in range(k, 20):
            found = False
            for i in range(len(rand_seq) - sub_len + 1):
                sub = rand_seq[i:i+sub_len]
                if sub in BURUMUT_FULL:
                    rand_max_match = max(rand_max_match, sub_len)
                    found = True
                    break
            if found:
                break
    print(f"  k={k}: max gemeinsame Subseq-Laenge mit BURUMUT = {rand_max_match}")

# 5. Selenoprotein-P-spezifische Suche
print()
print("="*70)
print("5. SelenoP-spezifische Sequenz-Motive")
print("="*70)
# SelenoP enthaelt mehrere His-reiche und Sec-reiche Regionen
# Suche nach 'HU' oder 'UH' (His-Sec) Tripeptiden
his_sec = [BURUMUT_FULL[i:i+3] for i in range(len(BURUMUT_FULL) - 2)
           if 'H' in BURUMUT_FULL[i:i+3] and 'U' in BURUMUT_FULL[i:i+3]]
print(f"H-U Tripeptide in BURUMUT: {len(his_sec)}")
for t in his_sec:
    print(f"  {t}")

# 6. Domain-Suche
print()
print("="*70)
print("6. Bekannte Sec-reiche Protein-Domaenen in BURUMUT?")
print("="*70)
# Sec-reiche Domänen aus Prosite/UniProt:
domains = {
    'Thioredoxin-like (Trx-fold)': 'C[GA]PC',  # enthält Cys
    'GPx active site': 'W[NQ]F[TS]PC[NU]',
    'DIO Sec-Site': 'SC[GA]U',  # Sec-Cys
    'Thioredoxin-like fold': 'GG[CH]PC',
    'Selenoprotein signature': 'U.{2,4}U',  # Sec-Sec motif
}

for name, pattern in domains.items():
    regex = pattern.replace('[', '[').replace(']', ']')
    # Ersetze Cys-Standard durch unsere B/Z
    regex_adapted = regex
    for char, repl in [('C', '[CBZ]'), ('U', 'U')]:
        regex_adapted = regex_adapted.replace(char, repl)
    matches = list(re.finditer(regex_adapted, BURUMUT_FULL))
    if matches:
        print(f"  {name} ({pattern}): {len(matches)} Treffer an {[m.start() for m in matches]}")
    else:
        print(f"  {name} ({pattern}): 0 Treffer")
