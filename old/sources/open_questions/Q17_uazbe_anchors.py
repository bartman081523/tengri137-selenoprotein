"""
Q17 (NEU): UAZBE als Doppel-Anker-Analyse

UAZBE = 5 Zeichen, kommt 4x in BURUMUT vor (an Pos 32, 46, 66, 80).
Jede UAZBE beginnt mit U (Sec) und enthaelt Z und B (unscharf).

Hypothese: UAZBE ist ein "Sec-Signal" der Zukunft.
- U (Sec) = die Sec-Aminosaeure
- A (Ala) = häufigster Protein-Rest (Helix-Begünstigung)
- Z (Glx) = unscharf (Gln oder Glu)
- B (Asx) = unscharf (Asn oder Asp)
- E (Glu) = negativ geladen

Bedeutung: UAZBE kodiert "Sec-Ala-Glx-Asx-Glu" als eine 5-AS-Signatur,
die in Sec-reichen Proteinen häufig vorkommt.

Wir testen: Wie oft kommt "UAZBE" in echten Sec-Proteinen vor?
Wir simulieren echte Sequenzen.
"""
import random
import re
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# 1. Suche nach UAZBE-ähnlichen Sub-Sequenzen in BURUMUT
print("="*70)
print("Q17.1: UAZBE-Sub-Sequenzen in BURUMUT")
print("="*70)
# Vollstaendige UAZBE-Positionen
positions = []
for i in range(len(BURUMUT_FULL)):
    if BURUMUT_FULL[i:i+5] == 'UAZBE':
        positions.append(i)
print(f"UAZBE-Positionen (5 Zeichen): {positions}")

# UAZ (erste 3 Zeichen)
for i in range(len(BURUMUT_FULL) - 2):
    if BURUMUT_FULL[i:i+3] == 'UAZ':
        print(f"  UAZ an Pos {i}: {BURUMUT_FULL[i:i+5]} ({BURUMUT_FULL[i:i+5] == 'UAZBE'})")

# AZB
print(f"\nAZB-Positionen: {[i for i in range(len(BURUMUT_FULL)-2) if BURUMUT_FULL[i:i+3] == 'AZB']}")

# ZBE
print(f"ZBE-Positionen: {[i for i in range(len(BURUMUT_FULL)-2) if BURUMUT_FULL[i:i+3] == 'ZBE']}")

# 2. Wie viele verschiedene 5-mer-Sequenzen hat BURUMUT?
print()
print("="*70)
print("Q17.2: 5-mer-Vielfalt in BURUMUT")
print("="*70)
five_mers = [BURUMUT_FULL[i:i+5] for i in range(len(BURUMUT_FULL)-4)]
five_freq = Counter(five_mers)
print(f"Anzahl unique 5-mere: {len(five_freq)}")
print(f"5-mer mit Haeufigkeit >= 2:")
for fm, n in sorted(five_freq.items(), key=lambda x: -x[1]):
    if n >= 2:
        print(f"  {fm}: {n}x")

# UAZBE sollte 4x vorkommen, andere 5-mere weniger
# Maximale Haeufigkeit pro 5-mer bei zufaelliger Sequenz?
n_trials = 5000
max_freq_dist = []
for trial in range(n_trials):
    rand_seq = ''.join(random.choices(set(BURUMUT_FULL), k=99))
    rand_five = Counter(rand_seq[i:i+5] for i in range(len(rand_seq)-4))
    if rand_five:
        max_freq_dist.append(max(rand_five.values()))

print(f"\nZufaellige 99-char-Sequenzen (n={n_trials}):")
print(f"  Haeufigstes 5-mer Haeufigkeit: Mittelwert = {sum(max_freq_dist)/n_trials:.2f}")
print(f"  Maximum beobachtet: {max(max_freq_dist)}")

# BURUMUT's 4-fache UAZBE - ist das ungewoehnlich?
print(f"\nBURUMUT hat 4x UAZBE (Maximal-Haeufigkeit = 4)")
if 4 > max(max_freq_dist) + 1:
    print(f"  -> UAZBE ist extrem ungewoehnlich oft wiederholt!")
else:
    print(f"  -> {max(max_freq_dist)} >= 4, koennte zufaellig sein")

# 3. UAZBE als Strukturmotiv in echten Proteinen
print()
print("="*70)
print("Q17.3: UAZBE-Motiv und seine Haeufigkeit")
print("="*70)
# Bedeutung von UAZBE als 5-mer:
# U = Sec (U)
# A = Ala (A)
# Z = Glx (Z = Gln oder Glu)
# B = Asx (B = Asn oder Asp)
# E = Glu (E)

# In Realitaet waere das "Sec-Ala-(Gln/Glu)-(Asn/Asp)-Glu"
# Was wenn Sec-Ala in der Sec-Helix-Position konserviert ist?
# In SECIS dirigiert ein Sec gefolgt von Ala + X + X + Glu

# Berechne: Wie oft kommt "UAXYE" (Sec-Ala-Glx-Asx-Glu) in echten Sec-Proteinen vor?
# Wir haben keine echten Sec-Proteinsequenzen lokal, daher:
# Monte Carlo Vergleich mit zufaelligen Sequenzen gleicher Laenge
n_trials = 5000
random_5mer_counts = []
for trial in range(n_trials):
    rand_seq = ''.join(random.choices(set(BURUMUT_FULL), k=99))
    cnt = sum(1 for i in range(len(rand_seq)-4) if rand_seq[i:i+5] == 'UAZBE')
    random_5mer_counts.append(cnt)

print(f"Monte Carlo: 5-mer UAZBE in 99-char zufaelligen Sequenzen")
print(f"  Mittelwert: {sum(random_5mer_counts)/n_trials:.4f}")
print(f"  Maximum: {max(random_5mer_counts)}")
print(f"  Anzahl mit >= 4 Vorkommen: {sum(1 for c in random_5mer_counts if c >= 4)}")
print(f"  BURUMUT hat: 4")

p_value = sum(1 for c in random_5mer_counts if c >= 4) / n_trials
print(f"\np-Wert fuer >= 4 Vorkommen in zufaelliger Sequenz: {p_value:.4f}")
