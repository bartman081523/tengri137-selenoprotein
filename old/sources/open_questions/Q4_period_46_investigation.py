"""
OFFENE FRAGE 4: Welche Periode ist wirklich 46?

Tengri behauptet mehrfach:
- 'eine Periode von exakt 46' (in Tengri137_Full_Notes)
- '1/47 hat Periode 46' (T137-math)

Aber:
- 1/47 = 0.0212765957446808510638297872340425531914893617021... (Periode 46)
- Tengri's eigene Berechnung: 
  (2*23*499*19214759967251*55150662460749672076915609) / 
  (3*11*47*139*2531*549797184491917*11111111111111111111111)
  = 0.0072973525613766677788831415921618033299792458 (Periode 46)
  
Numerator: 2*23*499*19214759967251*55150662460749672076915609
Denominator: 3*11*47*139*2531*549797184491917*11111111111111111111111

Wir testen:
1. Welche echte 46-stellige Periode steckt dahinter?
2. Ist die Sequenz '046'/'047'/'776'/'677' in der Wiederholung?
3. Welche Repunit-Faktorisierung beschreibt 1/alpha genauer?
"""
import math
from sympy import factorint, isprime, gcd
import sympy

# 1. Was hat Periode 46?
# Die zyklische Periode von 1/n ist gleich ord_n(10).
# Tengri behauptet 46.
# Suche alle n mit Periode 46:
print("="*70)
print("Q4.1: Welche Zahlen haben Periode 46 in 1/n?")
print("="*70)

def order_mod_10(n):
    """Findet k = ord_n(10), d.h. die kleinste k mit 10^k ≡ 1 (mod n)."""
    if n in (2, 5):
        return None
    if gcd(10, n) != 1:
        return None
    k = 1
    val = 10 % n
    while val != 1:
        val = (val * 10) % n
        k += 1
    return k

# Tengri's Aussage: Periode 46
# Bekannte Zahlen mit Periode 46:
print("Suche Zahlen mit dezimaler Periode 46 (kleine Beispiele):")
test_values = [47, 239 * 281, 909091, 4649, 121499449]
for n in test_values:
    period = order_mod_10(n)
    print(f"  {n}: Periode {period}")

# Finde alle kleinen Primzahlen mit Periode 46
print("\nKleine Primzahlen mit Periode 46:")
for n in range(2, 100000):
    if isprime(n) and order_mod_10(n) == 46:
        print(f"  {n}")
        break  # erste

# 2. Tengri's exakte Berechnung
print()
print("="*70)
print("Q4.2: Tengri's exakte Berechnung verifizieren")
print("="*70)
n_tengri = 2*23*499*19214759967251*55150662460749672076915609
d_tengri = 3*11*47*139*2531*549797184491917*11111111111111111111111

print(f"Numerator (N): {n_tengri}")
print(f"  Factorization: {factorint(n_tengri)}")
print(f"Denominator (D): {d_tengri}")
print(f"  Factorization: {factorint(d_tengri)}")

# Berechne N/D
q, r = divmod(n_tengri, d_tengri)
print(f"\nN / D = {q} (Ganzzahl-Anteil)")
print(f"Rest: {r}")
print(f"Dezimal: {n_tengri / d_tengri}")
print()

# Welche Periode hat N/D?
# Die dezimale Periode von N/D = lcm(ord_N(10), ord_D(10)) wenn gcd(N,D)=1
import math
def lcm(a, b):
    return a * b // math.gcd(a, b)

period_N = order_mod_10(n_tengri)
period_D = order_mod_10(d_tengri)
print(f"Periode von 1/N: {period_N}")
print(f"Periode von 1/D: {period_D}")
if period_N and period_D:
    full_period = lcm(period_N, period_D)
    print(f"Volle Periode von N/D: lcm({period_N}, {period_D}) = {full_period}")

# Tatsächliche Periode empirisch:
frac = n_tengri / d_tengri
s = str(frac)
if '0.' in s:
    decimal_part = s.split('0.')[1]
    print(f"\nDezimal-Darstellung (erste 80 Zeichen): 0.{decimal_part[:80]}...")

# 3. Suche die '046'-Sequenz in der Wiederholung
print()
print("="*70)
print("Q4.3: Suche 0.00729735256... in den Wiederholungen")
print("="*70)
# Berechne 1/alpha mit hoher Praezision
mpmath = __import__('mpmath')
mpmath.mp.dps = 100
alpha_inv = mpmath.mpf('137.035999084')  # CODATA 2018
alpha = 1 / alpha_inv
print(f"alpha = 1/137.035999084 = {mpmath.nstr(alpha, 80)}")

# Die dekodierte Sequenz: 0.0072973525613766677788831415921618033299792458
# Suche diese Sequenz in der Repunit-Struktur
print()
print("Suche die Tengri-Sequenz '00729735256' in 1/alpha:")
target = "00729735256"
alpha_str = mpmath.nstr(alpha, 200)
if target in alpha_str:
    pos = alpha_str.index(target)
    print(f"  Gefunden an Position {pos}: ...{alpha_str[max(0,pos-5):pos+len(target)+20]}...")
else:
    print(f"  NICHT direkt gefunden")
    # Suche Varianten
    for variant in ['0072973525', '073525613', '73252561']:
        if variant in alpha_str:
            print(f"  Variante '{variant}' gefunden in 1/alpha")

# 4. 46 Stellen von 1/alpha
print()
print("="*70)
print("Q4.4: Welche Repunit-Repraesentation liefert die 46-stellige Periode?")
print("="*70)
# 1/47 hat Periode 46, aber ist 0.02127..., nicht 0.00729...
# Was wenn Tengri die 46 Stellen der Repunit R_46 verwendet?
# R_46 = (10^46 - 1) / 9 = 111...1 (46x EINSEN)
# R_46 Faktoren:
R46_factors = factorint(10**46 - 1)
print(f"R_46 = (10^46 - 1) Faktoren: {dict(list(R46_factors.items())[:10])}")
# Welche dieser Faktoren koennte Tengri's Zaehler sein?

# Oder: Tengri's Berechnung liefert eine 46-stellige Periode einer Repunit
# Tengri's Zaehler-Faktoren:
print(f"\nTengri's Zaehler-Faktoren:")
for f in [2, 23, 499, 19214759967251, 55150662460749672076915609]:
    is_p = isprime(f)
    print(f"  {f} (prim: {is_p})")

print()
print(f"Tengri's Nenner-Faktoren:")
for f in [3, 11, 47, 139, 2531, 549797184491917, 11111111111111111111111]:
    is_p = isprime(f)
    print(f"  {f} (prim: {is_p})")

# Welcher Faktor ist 11111111111111111111111?
# Das ist R_22 = 22 EINSEN
print(f"\n11111111111111111111111 = R_22 (22 EINSEN)? {str(11111111111111111111111) == '1' * 22}")
