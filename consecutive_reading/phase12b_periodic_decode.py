"""
phase12b_periodic_decode.py
V7 Phase 4c — Periodensystem-Decoder (optimiert)
"""
import json
from pathlib import Path
from fractions import Fraction

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
    s = s.strip().replace(' ', '').replace('^', '**')
    factors = [f for f in s.split('*') if f]
    result = 1
    for f in factors:
        result *= int(eval(f))
    return result

def find_period_fast(num, den, max_digits=200):
    """Optimierte Perioden-Suche mit Set statt Dict"""
    seen = set()
    digits = []
    remainder = num % den
    while remainder != 0 and remainder not in seen and len(digits) < max_digits:
        seen.add(remainder)
        remainder *= 10
        digit = remainder // den
        remainder = remainder % den
        digits.append(digit)
    if remainder == 0:
        return ''.join(str(d) for d in digits), 0  # endender Dezimal
    return ''.join(str(d) for d in digits), len(seen) - 1

def decode_period(period):
    text = []
    pairs_used = []
    for i in range(0, len(period)-1, 2):
        pair = int(period[i:i+2])
        if pair in PERIODIC:
            elem = PERIODIC[pair]
            text.append(elem[0])
            pairs_used.append((pair, elem))
        else:
            text.append("?")
            pairs_used.append((pair, "?"))
    return ''.join(text), pairs_used

# === TEST: Schmehs Hinweis (Beispiel aus Web) ===
# "EVERYTHING THAT EXISTS IS BASED ON A MATHEMATICAL TRUTH"
# Jim's Kommentar: 28-Ziffern-Periode ergibt 14 Buchstaben
# Periode: 63 23 63 45 70 43 80 77 93 32 43 72 13 22 63 54 77 16 43 16 77 16 56 13 63 105 76 11

print("=" * 70)
print("TEST 1: Web-Beispiel (Jim's Kommentar)")
print("=" * 70)
example_period = "63" + "23" + "63" + "45" + "70" + "43" + "80" + "77" + "93" + "32" + "43" + "72" + "13" + "22" + "63" + "54" + "77" + "16" + "43" + "16" + "77" + "16" + "56" + "13" + "63" + "105" + "76" + "11"
print(f"Periode: {example_period}")
text, pairs = decode_period(example_period)
print(f"Decoded: {text}")

# === TEST 2: Verifiziere Tappeiners p17 ===
# Wir wissen: p17 hat 14 Faktorzerlegungen
# Aber Schmehs Lesung L=R könnte falsch sein — lass uns eine p17-Gleichung testen
print("\n" + "=" * 70)
print("TEST 2: Schmehs p17 Gleichung 1")
print("=" * 70)
L = parse_factorization("2^5 * 13 * 37 * 179 * 471077143")
R = parse_factorization("23 * 53 * 2711 * 897232321")
print(f"L = {L}")
print(f"R = {R}")
print(f"L == R: {L == R}")

# Wenn L != R, dann ist Schmehs Lesung falsch
# ABER: Tappeiner hat die Rechnungen geknackt — er hatte die RICHTIGEN Brüche
# Vielleicht ist die Reihenfolge in Schmehs Lesung falsch
# Wir brauchen die visuellen Glyphen, nicht Schmehs Transkription
