"""
phase14_test_schmeh_fractions.py
V7 Phase 4f — Teste Schmehs Faktorzerlegungs-Brüche
"""
import sys
sys.setrecursionlimit(100000)

JIM = "632363457043807793324372132263547716431677165613166310576111312132280631213437717135722379222722"

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
    return eval(s) if s.replace('*','').isdigit() == False else int(s)

def parse_factorization(s):
    s = s.strip().replace(' ', '').replace('^', '**')
    factors = [f for f in s.split('*') if f]
    r = 1
    for f in factors:
        r *= int(eval(f))
    return r

def find_period(num, den, max_digits=300):
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
        return ''.join(str(x) for x in digits[seen[rem]:]), seen[rem]
    return None, 0

# p17 Gleichungen
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

print("Teste alle Schmehs p17-Gleichungen")
print("=" * 70)

found_jim = False
for i, (l, r) in enumerate(p17, 1):
    try:
        L = parse_factorization(l)
        R = parse_factorization(r)
    except Exception as e:
        print(f"G{i:2}: Parse-Fehler {e}")
        continue

    if L == R:
        # Test L/R
        for num, den, lbl in [(L, R, "L/R"), (R, L, "R/L")]:
            if num == 0 or den == 0:
                continue
            period, start = find_period(num, den, max_digits=300)
            if period:
                if period == JIM or period.startswith(JIM[:30]):
                    print(f"G{i:2} {lbl}: MATCH! Periode = {period[:50]}...")
                    found_jim = True
                # Decoded text
                pairs = [int(period[j:j+2]) for j in range(0, len(period)-1, 2) if j+2 <= len(period)]
                text = ''.join(PERIODIC[p][0] if p in PERIODIC else '?' for p in pairs)
                if 'EVERY' in text or 'TIME' in text or 'TRUTH' in text:
                    print(f"G{i:2} {lbl}: RELEVANT TEXT: {text}")
    # Auch wenn L != R, könnten wir versuchen, eine Seite als Bruch zu nehmen
    else:
        # Wenn L und R verschieden sind, ist Schmehs Lesung falsch
        # Aber wir können trotzdem die Periode testen
        # z.B. könnte die Rechnung "L/Z" oder "Z/R" sein
        pass

if not found_jim:
    print("\nKeine direkte Übereinstimmung mit Jims Periode gefunden.")
    print("Jim's Periode stammt vermutlich von p18 (er sagt 'page 18').")
    print("Teste Schmehs p18...")

# p18
p18 = [
    ("2 * 3^2 * 5 * 163 * 179 * 643 * 1557763 * 5161229", "19 * 23 * 131 * 1039776975733464433"),
    ("17 * 58909 * 307301 * 34373828321747 * 37252411960004762373768239509", "52010407 * 5247588289 * 1129750427610562561 * 5603884498009743097"),
    ("2 * 29 * 12096868026427547373426314747359923987395057", "3^2 * 104447808327328839855368873760708272880436633"),
    ("7349 * 67171373 * 473610727 * 758327329194582826829", "2^3 * 5^2 * 13 * 433 * 34538589661 * 20061849662752419964530223"),
    ("673 * 482510108893443417506747", "2 * 13 * 17 * 19 * 53606252209428543969119"),
    ("7 * 11 * 613 * 53899 * 356449 * 5240109482723859309401199657638101", "5 * 19 * 815123 * 3959579220199 * 13063414694383 * 1556332114796741"),
    ("2 * 353 * 543341 * 616516263134675243885458363936657", "37 * 132547 * 2499619 * 7658309 * 82482863693 * 133913544923"),
    ("3 * 101 * 4799 * 1152039491 * 8780382483780105999747382526800373", "2 * 11 * 17 * 43 * 113 * 163 * 23669 * 316964629 * 18066117527601618948520456393"),
    ("101 * 303649 * 5492551 * 2988772165829", "2^6 * 5851 * 10914671 * 825503643058267"),
    ("3 * 227 * 259009 * 84754841", "5 * 15901 * 251947913683"),
    ("5 * 163 * 1181 * 10903 * 29347961 * 810800114952181", "20183 * 21517 * 1445875163274157927129309"),
    ("683747 * 1558302019894063 * 232746299171762203779945011", "79 * 3907 * 66475109 * 344123469204847 * 55541708322570135103"),
    ("5^2 * 139795778583407753912923", "659 * 1327 * 33977090434306641871"),
    ("2^2 * 3 * 17^2 * 12671 * 19993 * 170015969", "13 * 197 * 1087 * 80370109221679"),
    ("13 * 30631 * 116279 * 116612203 * 1634864437 * 6481900013", "127 * 75793 * 134406645637409 * 52878574088714923"),
    ("577 * 2246674487", "2 * 3 * 7 * 17 * 2713 * 2944517"),
]

for i, (l, r) in enumerate(p18, 1):
    try:
        L = parse_factorization(l)
        R = parse_factorization(r)
    except Exception as e:
        continue

    for num, den, lbl in [(L, R, "L/R"), (R, L, "R/L")]:
        if num == 0 or den == 0 or num == den:
            continue
        period, start = find_period(num, den, max_digits=300)
        if period:
            pairs = [int(period[j:j+2]) for j in range(0, len(period)-1, 2) if j+2 <= len(period)]
            text = ''.join(PERIODIC[p][0] if p in PERIODIC else '?' for p in pairs)
            if 'EVERY' in text or 'TIME' in text or 'TRUTH' in text or 'AMATHEMA' in text:
                print(f"\n*** MATCH p18 G{i:2} {lbl}: {text}")
                found_jim = True
            elif 'EXISTS' in text:
                print(f"\n*** PARTIAL p18 G{i:2} {lbl}: {text}")
            # auch wenn periode == JIM
            if period == JIM:
                print(f"\n*** JIM MATCH p18 G{i:2} {lbl}")

if not found_jim:
    print("\nAuch in p18 nicht gefunden. Schmehs Lesung in Full_Notes ist falsch.")
