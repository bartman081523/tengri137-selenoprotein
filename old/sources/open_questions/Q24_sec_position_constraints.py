"""
Q24 (NEU): Sec-Insertion-Positions-Beschraenkungen in BURUMUT

BURUMUT hat 11 U an spezifischen Positionen: 1, 3, 5, 13, 15, 19, 24, 32, 46, 66, 80
Davon sind 4 (an Pos 32, 46, 66, 80) an UAZBE-Ankern.

Frage: Was beschraenkt die Sec-Positionen?
- Sind sie zufaellig verteilt?
- Folgen sie einem Muster (z.B. Periodizitaet)?
- Korrelieren sie mit Sekundaerstruktur?

Wir testen:
1. Auto-Korrelation der Sec-Positionen
2. Distanz-zum-vorherigen-Sec
3. Sekundaerstruktur-Vorhersage um Sec-Positionen
"""
import math
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# 1. Sec-Positionen
sec_pos = [i for i, c in enumerate(BURUMUT_FULL) if c == 'U']
uazbe_pos = [32, 46, 66, 80]
print("="*70)
print("Q24.1: Sec-Positions-Analyse")
print("="*70)
print(f"Sec-Positionen in BURUMUT: {sec_pos}")
print(f"UAZBE-Positionen:          {uazbe_pos}")
print(f"Sec an UAZBE: {sorted([p for p in sec_pos if p in uazbe_pos])}")
print()

# 2. Distanzen zwischen Sec
print("="*70)
print("Q24.2: Distanzen zwischen aufeinanderfolgenden Sec")
print("="*70)
distances = [sec_pos[i+1] - sec_pos[i] for i in range(len(sec_pos) - 1)]
print(f"Distanzen: {distances}")
print(f"Mittelwert: {sum(distances)/len(distances):.2f}")
print(f"Median: {sorted(distances)[len(distances)//2]}")
print(f"Min/Max: {min(distances)}/{max(distances)}")
print()

# 3. Suche nach Periodizitaet
print("="*70)
print("Q24.3: Periodizitaets-Test (Fourier-Analyse)")
print("="*70)
# Konvertiere Sec-Positionen in eine binaere Sequenz
binary_sec = [1 if i in sec_pos else 0 for i in range(len(BURUMUT_FULL))]
print(f"Binaere Sec-Sequenz: {''.join(str(b) for b in binary_sec)}")

# Auto-Korrelation fuer verschiedene lags
print("Auto-Korrelation der Sec-Positionen:")
for lag in [1, 2, 3, 4, 5, 7, 10, 14, 20]:
    # Berechne Pearson-Korrelation
    n = len(binary_sec) - lag
    a = binary_sec[:n]
    b = binary_sec[lag:lag+n]
    mean_a = sum(a) / n
    mean_b = sum(b) / n
    cov = sum((a[i] - mean_a) * (b[i] - mean_b) for i in range(n))
    var_a = sum((a[i] - mean_a)**2 for i in range(n))
    var_b = sum((b[i] - mean_b)**2 for i in range(n))
    if var_a > 0 and var_b > 0:
        corr = cov / (var_a * var_b) ** 0.5
    else:
        corr = 0
    print(f"  lag={lag:2d}: {corr:+.4f}")

# 4. Sec-Clustering
print()
print("="*70)
print("Q24.4: Sec-Clustering-Analyse")
print("="*70)
# Wir suchen nach Clustern von Sec-Positionen
# Ein "Cluster" = mehrere Sec in einem 10-AS-Fenster
clusters = []
for i in range(len(sec_pos) - 1):
    cluster_size = 1
    for j in range(i+1, len(sec_pos)):
        if sec_pos[j] - sec_pos[j-1] <= 5:  # max 5 AS zwischen Secs
            cluster_size += 1
        else:
            break
    if cluster_size >= 2:
        clusters.append((sec_pos[i], cluster_size))
print(f"Sec-Cluster (>= 2 Secs, max Abstand 5): {len(clusters)}")
for c in clusters[:10]:
    print(f"  Start: {c[0]}, Groesse: {c[1]}")

# 5. Vergleich: Sec-Positionen vs Zufall
print()
print("="*70)
print("Q24.5: Sind Sec-Positionen zufaellig?")
print("="*70)
import random
random.seed(42)
n_trials = 10000
random_5mer_count = 0
# Vergleiche: In 99 Zeichen mit 11 Sec, was ist die Wahrscheinlichkeit,
# dass 4 davon an spezifizierten Positionen sind?
from math import comb
total = comb(99, 11)
# Exakt 4 an spezifizierten 4 Positionen
matching = comb(4, 4) * comb(95, 7)
p_value = matching / total
print(f"P(4 Sec an spezifizierten 4 Positionen) = {p_value:.6e}")
print(f"= {p_value:.3e} (äquivalent zu p=8.77e-5 aus Q9)")

# 6. 11 Sec auf 99 Positionen - statistisch ungewoehnlich?
# Wenn Secs zufaellig waeren, waere die erwartete Anzahl pro Position = 11/99 = 0.111
# Tatsaechlich: 4 an UAZBE-Positionen, 7 an anderen
# Chi-squared Test
expected_per_pos = 11 / 99
chi_sq = sum((binary_sec[i] - expected_per_pos)**2 / expected_per_pos
             for i in range(len(binary_sec)))
print(f"\nChi-squared Test (Sec vs Erwartung): {chi_sq:.4f}")
print(f"  (Hoeher = ungleichmaessiger)")
print(f"  Bei 11 Sec in 99 Pos ist die erwartete Varianz natuerlich hoch")

# 7. Konsequenz fuer Sec-Insertion-Mechanismus
print()
print("="*70)
print("Q24.6: Welcher Sec-Insertion-Mechanismus passt?")
print("="*70)
# 1. Eukaryotisch: SECIS-Element dirigiert ALLE Sec downstream
#    3 SECIS-Elemente in BURUMUT-mRNA
# 2. Prokaryotisch (E. coli): SelB erkennt spezifische mRNA-Haarnadel
#    am UGA-Codon. Wenn BURUMUT prokaryotisch waere, braucht es
#    kein SECIS, sondern eine mRNA-Struktur am UGA.
# 3. Archaeal: SECIS-artige Strukturen, aber selten
#
# In BURUMUT: 3 SECIS-Elemente, eukaryotisch-ähnlich
# → BURUMUT ist möglicherweise von einem EUKARYOTISCHEN
#   Biosystem codiert (nicht prokaryotisch, nicht archaeal)
