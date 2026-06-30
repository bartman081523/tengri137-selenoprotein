import math
from collections import Counter

HEBREW = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}
HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
             'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']

BURUMUT = 'BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN'

def to_hebrew(s):
    out = []
    for c in s:
        idx = ord(c) - ord('A')
        if 0 <= idx < 22:
            out.append(HEBREW_22[idx])
        else:
            out.append('?')
    return ''.join(out)

print("=" * 70)
print("Q28c.1: BURUMUT <-> Hebraeische Buchstaben")
print("=" * 70)
heb = to_hebrew(BURUMUT)
print(f"BURUMUT ({len(BURUMUT)} Zeichen):")
print(f"  {BURUMUT}")
print(f"Hebraeisch:")
print(f"  {heb}")

# Mothers und Doubles
MOTHERS = ['א', 'מ', 'ש']  # A, M, S
DOUBLES = ['ב', 'ג', 'ד', 'כ', 'פ', 'ר', 'ת']  # B, G, D, K, P, R, T

print()
print("=" * 70)
print("Q28c.2: Sefer Yetzirah Mothers + Doubles in BURUMUT")
print("=" * 70)
print("3 Mothers (Alef, Mem, Shin):")
for m in MOTHERS:
    cnt = BURUMUT.count(m)
    print(f"  {m} : {cnt}x")

print("\n7 Doubles (Beth, Gimel, Dalet, Kaph, Pe, Resh, Tav):")
for d in DOUBLES:
    cnt = BURUMUT.count(d)
    print(f"  {d} : {cnt}x")

print()
print("Beobachtung: BURUMUT enthaelt 5/7 Doubles (B, G, P, R, T)")
print("Fehlend: D, K (Dalet, Kaph)")

# 22 - 3 Mothers = 19 Simples
# 19 = BURUMUT-Alphabet-Groesse
print()
print("=" * 70)
print("Q28c.3: 22 Konsonanten = Mothers (3) + Doubles (7) + Simples (12)")
print("=" * 70)
# Aber BURUMUT hat 19 distinct, nicht 12
print("Aber BURUMUT hat 19 distinct (nicht 12 Simples)")
print()
print("Was wenn 19 = 22 - 3 (Mothers) = Simples + Doubles?")
print("  12 Simples + 7 Doubles = 19!")
print("  -> BURUMUT enthaelt ALLE Simples + ALLE Doubles!")

# Verifizieren
simples_set = set(HEBREW_22) - set(MOTHERS) - set(DOUBLES)
print(f"\nSimples (12): {sorted(simples_set)}")
burumut_hebrew_set = set(heb.replace('?', ''))
print(f"\nIn BURUMUT vorhandene hebr. Buchstaben: {sorted(burumut_hebrew_set)}")
print(f"Anzahl: {len(burumut_hebrew_set)}")

# Welche fehlen?
missing = set(HEBREW_22) - burumut_hebrew_set
print(f"\nFehlend: {sorted(missing)}")
