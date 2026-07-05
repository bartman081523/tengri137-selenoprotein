"""
phase12c_full_test.py
V7 Phase 4d — Teste alle 14 p17-Gleichungen aus Schmehs Lesung
"""
from fractions import Fraction
import sys
sys.setrecursionlimit(100000)

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

def parse(s):
    s = s.strip().replace(' ', '').replace('^', '**')
    factors = [f for f in s.split('*') if f]
    r = 1
    for f in factors:
        r *= int(eval(f))
    return r

def find_period(num, den, max_digits=100):
    seen = {}
    digits = []
    rem = num % den
    while rem != 0 and rem not in seen and len(digits) < max_digits:
        seen[rem] = len(digits)
        rem *= 10
        d = rem // den
        rem = rem % den
        digits.append(d)
    if rem in seen:
        period_start = seen[rem]
        period = digits[period_start:]
        return ''.join(str(x) for x in period), period_start, len(period)
    return ''.join(str(x) for x in digits), 0, len(digits)

def decode(p):
    t = []
    for i in range(0, len(p)-1, 2):
        pair = int(p[i:i+2])
        t.append(PERIODIC[pair][0] if pair in PERIODIC else '?')
    return ''.join(t)

# p17 Gleichungen aus Schmehs Lesung
p17 = [
    ("2^5 * 13 * 37 * 179 * 471077143", "23 * 53 * 2711 * 897232321"),
    ("307 * 1481 * 10873297429171343046161 * 19193689163997857327327", "7 * 17780871841855257950191971103144880245068986055043"),
    ("2 * 11 * 31 * 13859 * 368409682534592182127348765844882931423", "25649821274850734656854890069058197080762302797"),
    ("20824027389475657 * 652793699238832001551", "2 * 17 * 1621 * 32297 * 111623 * 91673033412247294680889"),
    ("5 * 61 * 103 * 113867495484484178331304153088007990064363783", "17 * 179 * 3467 * 3219088991 * 264850496551597978818922424250101"),
    ("7^2 * 51749 * 163247627663 * 326153710690401658818517", "6932277120159617 * 85395751599324144689923657"),
    ("2 * 3 * 5 * 997 * 6798111767 * 39981184788031", "37 * 21503 * 10258109 * 6747307626687311"),
    ("2^2 * 3 * 11 * 521 * 1951 * 3373 * 8521 * 184669", "7 * 53 * 709 * 3627657461137709"),
    ("2 * 3^3 * 55751765473057", "61 * 317 * 443 * 470896109"),
    ("2 * 3 * 5 * 13 * 157 * 8663 * 68813 * 21019979", "23 * 83 * 11949331 * 45067390603"),
    ("2 * 105557 * 125788337 * 153880609", "431 * 563 * 3257 * 167597 * 41337883"),
    ("2^2 * 5 * 7^2 * 461 * 96681715401559", "109 * 1741 * 308405893609031"),
    ("7196993 * 63653689179445812751", "9928974360853 * 116017446409097"),
    ("2^5 * 3^2 * 151 * 929 * 2851 * 71777 * 17179879599815040097271", "139 * 103800937 * 239135080477 * 55157555001341549"),
    ("2663 * 527321833009330157320330830319", "2 * 986094191 * 3121883712968346492645571"),
    ("3 * 4351757 * 21485973838025664080646395598811170316033", "2 * 187926408429986714056114267608550013734737954283"),
]

print("=" * 80)
print("Vollständige p17-Verifizierung")
print("=" * 80)

valid = 0
for i, (l, r) in enumerate(p17, 1):
    try:
        L = parse(l)
        R = parse(r)
        is_eq = L == R
        if is_eq:
            valid += 1
        print(f"G{i:2}: L==R: {is_eq}  (L={L if L < 10**15 else 'big'}, R={R if R < 10**15 else 'big'})")
    except Exception as e:
        print(f"G{i:2}: ERROR {e}")

print(f"\n{valid}/{len(p17)} Gleichungen sind konsistent (L == R)")

# Auch: Suche nach der ersten, die einen lesbaren Text ergibt
print("\n" + "=" * 80)
print("Teste Periode für gültige Gleichungen")
print("=" * 80)

for i, (l, r) in enumerate(p17, 1):
    try:
        L = parse(l)
        R = parse(r)
        if L != R:
            continue
        # Beide Richtungen testen
        for num, den, lbl in [(L, R, "L/R"), (R, L, "R/L")]:
            period, start, plen = find_period(num, den, max_digits=200)
            if plen > 0:
                text = decode(period)
                print(f"G{i:2} {lbl}: period_len={plen}, decoded={text[:50]}{'...' if len(text) > 50 else ''}")
    except Exception as e:
        pass  # skip
