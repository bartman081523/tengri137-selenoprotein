"""
PHASE 1.5: TIEFERES GRABEN - DIE PHI-BRUCKE

Die erste Analyse ergab:
  Trigramm-Summen nahe Phi-Vielfachen (<1.0): 97/97 = 100%

Das ist zu gut, um Zufall zu sein. Wir muessen verstehen, warum.

Methoden:
1. Monte-Carlo-Verteilung der Trigramm-Summen bei zufaelligen 18-Zeichen-Alphabeten
2. Visualisierung der Phi-Approximation als Histogramm
3. Vergleich mit anderen irrationalen Zahlen (e, sqrt(2), sqrt(3), pi)
4. Suche nach einer algebraischen Bruecke zwischen BURUMUT-Buchstaben und phi
"""
import math
from collections import Counter
import random

# Konfiguration
BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

phi = (1 + math.sqrt(5)) / 2

def letter_to_num(s):
    return [ord(c) - ord('A') + 1 for c in s]

def trigram_sums(s):
    nums = letter_to_num(s)
    return [nums[i] + nums[i+1] + nums[i+2] for i in range(len(nums) - 2)]

print("="*70)
print("PHASE 1.5.1: MONTE CARLO - WIE OFT SIND TRIGRAMM-SUMMEN NAHE PHI?")
print("="*70)

# Wir generieren 10000 zufaellige Strings gleicher Laenge aus gleichem Alphabet
# und pruefen, wie oft die Trigramm-Summen nahe phi*n sind.

ALPHABET = sorted(set(BURUMUT_FULL))
N_SAMPLES = 10000
TOLERANCE = 1.0

observed_sums = trigram_sums(BURUMUT_FULL)
observed_count = sum(1 for s in observed_sums if abs(s - round(s/phi) * phi) < TOLERANCE)
print(f"Beobachtet in BURUMUT: {observed_count}/{len(observed_sums)} = {100*observed_count/len(observed_sums):.1f}%")

random_counts = []
for _ in range(N_SAMPLES):
    rseq = ''.join(random.choices(ALPHABET, k=len(BURUMUT_FULL)))
    rsums = trigram_sums(rseq)
    count = sum(1 for s in rsums if abs(s - round(s/phi) * phi) < TOLERANCE)
    random_counts.append(count)

mean_r = sum(random_counts) / N_SAMPLES
std_r = (sum((c - mean_r)**2 for c in random_counts) / N_SAMPLES) ** 0.5
print(f"Zufaellig (10000 Samples): Mittelwert {mean_r:.2f}, Std {std_r:.2f}")

if std_r > 0:
    z = (observed_count - mean_r) / std_r
    print(f"Z-Score: {z:.2f} (positiv = haeufiger als zufaellig)")
    p_val = sum(1 for c in random_counts if c >= observed_count) / N_SAMPLES
    print(f"p-Wert (haeufiger oder gleich): {p_val:.4f}")
print()

print("="*70)
print("PHASE 1.5.2: VERGLEICH MIT ANDEREN IRRATIONALEN ZAHLEN")
print("="*70)

irrationals = {
    'phi': phi,
    'pi': math.pi,
    'e': math.e,
    'sqrt(2)': math.sqrt(2),
    'sqrt(3)': math.sqrt(3),
    'sqrt(5)': math.sqrt(5),
    'Feigenbaum': 4.669201609,
    'ln(2)': math.log(2),
    'Catalan': 0.915965594,
    'Omega': 0.5671432904,
}

print(f"{'Konstante':12s} {'<0.1':>6s} {'<0.5':>6s} {'<1.0':>6s} {'<2.0':>6s}")
for name, c in irrationals.items():
    buckets = [0, 0, 0, 0]
    for s in observed_sums:
        diff = abs(s - round(s/c) * c)
        if diff < 0.1: buckets[0] += 1
        if diff < 0.5: buckets[1] += 1
        if diff < 1.0: buckets[2] += 1
        if diff < 2.0: buckets[3] += 1
    print(f"{name:12s} {buckets[0]:6d} {buckets[1]:6d} {buckets[2]:6d} {buckets[3]:6d}")
print()

print("="*70)
print("PHASE 1.5.3: WIE GROSS IST DIE ABWEICHUNG?")
print("="*70)
print(f"Trigramm-Summen-Werte und Abweichung zum naechsten phi*n:")
print()
print(f"{'Summe':>6s} {'phi*n':>10s} {'n':>5s} {'Diff':>10s}")
for s in observed_sums:
    n = round(s / phi)
    nearest_phi_n = n * phi
    diff = abs(s - nearest_phi_n)
    if diff < 2.0:  # nur die engen Treffer zeigen
        print(f"  {s:6d} {nearest_phi_n:10.4f} {n:5d} {diff:10.4f}")
print()

# Was wenn der Toleranz-Wert TOY eng gewaehlt ist?
print("Bei sehr enger Toleranz (0.1) - ist die 100% noch real?")
strict_count = sum(1 for s in observed_sums if abs(s - round(s/phi) * phi) < 0.1)
print(f"Toleranz 0.1: {strict_count}/{len(observed_sums)} = {100*strict_count/len(observed_sums):.1f}%")

strict_count_2 = sum(1 for s in observed_sums if abs(s - round(s/phi) * phi) < 0.01)
print(f"Toleranz 0.01: {strict_count_2}/{len(observed_sums)} = {100*strict_count_2/len(observed_sums):.1f}%")

# Bei Zufall
print()
print("Monte-Carlo bei Toleranz 0.01:")
strict_random = []
for _ in range(10000):
    rseq = ''.join(random.choices(ALPHABET, k=len(BURUMUT_FULL)))
    rsums = trigram_sums(rseq)
    count = sum(1 for s in rsums if abs(s - round(s/phi) * phi) < 0.01)
    strict_random.append(count)

mean_sr = sum(strict_random) / N_SAMPLES
print(f"Zufaellig: Mittelwert {mean_sr:.3f}, Max {max(strict_random)}, Min {min(strict_random)}")
print(f"Beobachtet (BURUMUT): {strict_count_2}")
print()

print("="*70)
print("PHASE 1.5.4: UAZ/AZB/ZBE - DIE SELBSTREFERENTIELLE SCHLEIFE")
print("="*70)
# Das Trigramm UAZ kommt 4x vor. Schauen wir die Positionen genauer an.
trigrams = [BURUMUT_FULL[i:i+3] for i in range(len(BURUMUT_FULL) - 2)]
positions = {}
for i, tg in enumerate(trigrams):
    if tg not in positions:
        positions[tg] = []
    positions[tg].append(i)

# Welche Trigramme wiederholen sich?
print("Trigramme mit >= 2 Vorkommen:")
for tg, pos in sorted(positions.items(), key=lambda x: -len(x[1])):
    if len(pos) >= 2:
        print(f"  {tg}: an Positionen {pos}")
print()

# Suchen wir das Muster UAZBE...
print("Suche nach UAZBE-Muster (zusammenhaengend):")
pattern = "UAZBE"
start = 0
while True:
    idx = BURUMUT_FULL.find(pattern, start)
    if idx == -1: break
    print(f"  Gefunden bei Position {idx}: ...{BURUMUT_FULL[idx:idx+15]}...")
    start = idx + 1
print()

print("="*70)
print("PHASE 1.5.5: PHI UND DER ALPHA-INTERFACE")
print("="*70)
# Beziehung zwischen phi und 137?
print(f"phi * 137 = {phi * 137:.6f}")
print(f"phi * 84 = {phi * 84:.6f}")
print(f"phi^2 = {phi**2:.6f}")
print(f"1/phi = {1/phi:.6f}")
print(f"137 / phi = {137/phi:.6f}")
print(f"137 - 84 = {137 - 84}")
print(f"84 = 2 * 42 = 2 * 6 * 7 = 12 * 7")
print()

# Berechne das Verhaeltnis BURUMUT-Summe zu phi*100
total_sum = sum(letter_to_num(BURUMUT_FULL))
print(f"BURUMUT-Gesamtsumme: {total_sum}")
print(f"phi * 250 = {phi * 250:.4f}")
print(f"phi * 260 = {phi * 260:.4f}")
print(f"BURUMUT-Summe / phi = {total_sum / phi:.4f}")
print(f"Naechstes phi*n: phi * 762 = {phi*762:.4f}")
print()

print("="*70)
print("PHASE 1.5.6: DAS GEHEIMNIS DER POSITION 34 - DER ERSTE 'Z'")
print("="*70)
# Position 34 in BURUMUT ist der erste 'Z'.
# 34 ist eine spezielle Zahl (Dreieckszahl T_8 = 36, F_9 = 34)
# 34 = 2 * 17 (Primzahl)
# Wir schauen, was vor und nach Position 34 steht.

print(f"BURUMUT (99 Zeichen): {BURUMUT_FULL}")
print(f"Position 34: '{BURUMUT_FULL[34]}' (Kontext: '{BURUMUT_FULL[30:40]}')")
print()
print("Alle Z-Positionen: 34, 42, 48, 57, 68, 76, 82, 92")
print("Differenzen: 8, 6, 9, 11, 8, 6, 10")
print("Median: 8, Mittelwert: 8.3")
print()

# Berechne die Fibonacciaehnlichkeit
fibs = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89]
print(f"Fibonacci-Zahlen bis 100: {fibs}")
print(f"Positionen, die Fibonacci-Zahlen sind: {[p for p in [34, 42, 48, 57, 68, 76, 82, 92] if p in fibs]}")
print()

print("="*70)
print("PHASE 1.5.7: DIE MAGISCHE KONSTANTE 666 / 137 = 4.86")
print("="*70)
print(f"666 / 137 = {666/137:.6f}")
print(f"666 / 110 = {666/110:.6f}")
print(f"666 / 100 = 6.66")
print(f"alpha^-1 * 4.86 = {137 * 4.86:.4f}")
print(f"alpha^-1 + phi = {137 + phi:.4f}")
print()

print("="*70)
print("PHASE 1.5.8: DAS BURUMUT-ALPHABET (18 Zeichen)")
print("="*70)
# BURUMUT hat 18 distinkte Zeichen (von 99 Gesamtzeichen).
# Wir untersuchen, ob 18 etwas Spezielles ist.
print(f"Alphabet-Groesse: {len(set(BURUMUT_FULL))}")
print(f"Alphabet: {sorted(set(BURUMUT_FULL))}")
print(f"  18 = 2 * 3^2")
print(f"  18 = 6 + 12 = 6 + 6 + 6")
print(f"  18 = 72 / 4")
print(f"  18 = 137 - 119 = 137 - 7 * 17")
print()

# Wenn wir jeden Buchstabe als 1-26 abbilden, dann ist die Summe / Anzahl:
nums = letter_to_num(BURUMUT_FULL)
mean_num = sum(nums) / len(nums)
print(f"Mittelwert der Buchstaben-Zahlen: {mean_num:.4f}")
print(f"Erwartet (13.5 fuer zufaellig 26 Buchstaben): 13.5")
print(f"13.5 * 99 = {13.5 * 99}")
print(f"Tatsaechliche Summe: {sum(nums)}")
print(f"Verhaeltnis tatsaechlich/erwartet: {sum(nums) / (13.5 * 99):.4f}")
print()

print("="*70)
print("PHASE 1.5 ENDE")
print("="*70)