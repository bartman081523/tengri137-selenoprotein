"""
phase12_periodic_decode.py
V7 Phase 4b — Periodensystem-Decoder für Tengri 137

Methode: Tappeiner-Decodierung
1. Bruch aus Schmehs Lesung
2. Reduziere zu irreduziblen Bruch
3. Berechne periodische Dezimal-Expansion
4. Paare Ziffern, map zu Elementen
5. Erster Buchstabe jedes Elements = Klartext-Buchstabe
"""
import json
from pathlib import Path
from fractions import Fraction

# Periodensystem (1-118)
PERIODIC = {
    1:'H', 2:'He', 3:'Li', 4:'Be', 5:'B', 6:'C', 7:'N', 8:'O', 9:'F', 10:'Ne',
    11:'Na', 12:'Mg', 13:'Al', 14:'Si', 15:'P', 16:'S', 17:'Cl', 18:'Ar', 19:'K', 20:'Ca',
    21:'Sc', 22:'Ti', 23:'V', 24:'Cr', 25:'Mn', 26:'Fe', 27:'Co', 28:'Ni', 29:'Cu', 30:'Zn',
    31:'Ga', 32:'Ge', 33:'As', 34:'Se', 35:'Br', 36:'Kr', 37:'Rb', 38:'Sr', 39:'Y', 40:'Zr',
    41:'Nb', 42:'Mo', 43:'Tc', 44:'Ru', 45:'Rh', 46:'Pd', 47:'Ag', 48:'Cd', 49:'In', 50:'Sn',
    51:'Sb', 52:'Te', 53:'I', 54:'Xe', 55:'Cs', 56:'Ba', 57:'La', 58:'Ce', 59:'Pr', 60:'Nd',
    61:'Pm', 62:'Sm', 63:'Eu', 64:'Gd', 65:'Tb', 66:'Dy', 67:'Ho', 68:'Er', 69:'Tm', 70:'Yb',
    71:'Lu', 72:'Hf', 73:'Ta', 74:'W', 75:'Re', 76:'Os', 77:'Ir', 78:'Pt', 79:'Au', 80:'Hg',
    81:'Tl', 82:'Pb', 83:'Bi', 84:'Po', 85:'At', 86:'Rn', 87:'Fr', 88:'Ra', 89:'Ac', 90:'Th',
    91:'Pa', 92:'U', 93:'Np', 94:'Pu', 95:'Am', 96:'Cm', 97:'Bk', 98:'Cf', 99:'Es', 100:'Fm',
    101:'Md', 102:'No', 103:'Lr', 104:'Rf', 105:'Db', 106:'Sg', 107:'Bh', 108:'Hs', 109:'Mt', 110:'Ds',
    111:'Rg', 112:'Cn', 113:'Nh', 114:'Fl', 115:'Mc', 116:'Lv', 117:'Ts', 118:'Og',
}

def parse_factorization(s):
    """Parse '2^5 * 13 * 37' -> integer"""
    s = s.strip().replace(' ', '').replace('^', '**')
    factors = [f for f in s.split('*') if f]
    result = 1
    for f in factors:
        result *= int(eval(f))
    return result

def reduce_fraction(num, den):
    """Reduce to lowest terms (remove 2 and 5 from denominator)"""
    f = Fraction(num, den)
    # Entferne 2er und 5er
    while f.denominator % 2 == 0:
        f = Fraction(f.numerator * 5, f.denominator * 5)
    while f.denominator % 5 == 0:
        f = Fraction(f.numerator * 2, f.denominator * 2)
    return f.numerator, f.denominator

def find_period(num, den, max_digits=200):
    """Find repeating decimal period of num/den"""
    # Long division
    quotient = num // den
    remainder = num % den
    digits = []
    seen = {}
    while remainder != 0 and remainder not in seen and len(digits) < max_digits:
        seen[remainder] = len(digits)
        remainder *= 10
        digit = remainder // den
        remainder = remainder % den
        digits.append(digit)
    if remainder in seen:
        period_start = seen[remainder]
        period = digits[period_start:]
        return ''.join(str(d) for d in period), period_start
    return ''.join(str(d) for d in digits), 0

def decode_period(period):
    """Decode period to plaintext using periodic table"""
    pairs = []
    text = []
    for i in range(0, len(period)-1, 2):
        pair = int(period[i:i+2])
        if pair in PERIODIC:
            elem = PERIODIC[pair]
            pairs.append(f"{pair}={elem}")
            text.append(elem[0])  # first letter
        else:
            pairs.append(f"{pair}=?")
            text.append("?")
    return ''.join(text), pairs

# === TEST MIT SCHMEHS LESUNG ===
# p17 Gleichungen (aus Tengri137_Full_Notes)
p17_equations = [
    ("2^5 * 13 * 37 * 179 * 471077143", "23 * 53 * 2711 * 897232321"),
    # 14 Gleichungen insgesamt
]

print("=" * 70)
print("TAPPEINER-DECODER TEST: p17")
print("=" * 70)

for i, (left, right) in enumerate(p17_equations, 1):
    L = parse_factorization(left)
    R = parse_factorization(right)
    print(f"\nGleichung {i}: {left} = {right}")
    print(f"  L = {L}, R = {R}")
    print(f"  L == R: {L == R}")

    # Tappeiner: 1 Gleichung = 1 Bruch
    # Aber L = R sollte gelten (Faktorzerlegung)
    if L != R:
        print(f"  WARNUNG: L != R, Schmehs Lesung könnte falsch sein")

    # Versuche beide: L/R und R/L
    for num_str, den_str, label in [(L, R, "L/R"), (R, L, "R/L")]:
        num_red, den_red = reduce_fraction(num_str, den_str)
        period, start = find_period(num_red, den_red)
        if period and len(period) >= 2:
            text, pairs = decode_period(period)
            print(f"  {label}: {num_red}/{den_red}, period_start={start}, period={period[:60]}{'...' if len(period) > 60 else ''}")
            print(f"    Plaintext: {text}")
        else:
            print(f"  {label}: keine Periode gefunden")

# === TEST: Schmehs Hinweis ===
# 'TIME FOR THE TRUTH' (19 chars) als erste Zeile
# Wir brauchen einen Bruch mit 38-Ziffern-Periode, der 'TIME FOR THE TRUTH' ergibt
print("\n" + "=" * 70)
print("VERIFIKATION: Erwarteter Klartext 'TIME FOR THE TRUTH'")
print("=" * 70)
expected = "TIMEFORTHETRUTH"
print(f"  Erwartet: {expected} ({len(expected)} Zeichen)")

# Welche 2er-Paare ergeben T,I,M,E,F,O,R,T,H,E,T,R,U,T,H?
required_pairs = []
for c in expected:
    # Suche Element mit erstem Buchstaben c
    matches = [(n, e) for n, e in PERIODIC.items() if e[0] == c]
    if matches:
        # Nimm das häufigste/erste
        required_pairs.append(matches[0])
    else:
        required_pairs.append((None, None))

print(f"  Benötigte Paare: {required_pairs}")
print(f"  Periode: {''.join(str(p[0]) for p in required_pairs if p[0])}")
