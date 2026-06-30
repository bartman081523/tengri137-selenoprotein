"""
Q28b: Sefer Yetzirah + BURUMUT (korrigiert)
"""
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

# 1. Mapping
def to_hebrew(s):
    out = []
    for c in s:
        idx = ord(c) - ord('A')
        if 0 <= idx < 22:
            out.append(HEBREW_22[idx])
        else:
            out.append('?')
    return ''.join(out)

print("="*70)
print("Q28b.1: BURUMUT <-> Hebräische Buchstaben (Mapping A=א..T=ת)")
print("="*70)
heb = to_hebrew(BURUMUT)
print(f"BURUMUT ({len(BURUMUT)} Zeichen):")
print(f"  {BURUMUT}")
print(f"Hebräisch:")
print(f"  {heb}")
print(f"Nicht-zuordbare Buchstaben in BURUMUT (C, D, J, K, V, W, X):")
unmappable = [c for c in BURUMUT if c in 'CDJKVWX']
print(f"  {Counter(unmappable)}")

# 2. Gematria
print()
print("="*70)
print("Q28b.2: BURUMUT als hebr. Wort-Gematria")
print("="*70)
# U=21 -> ש(300). R=18 -> צ(90). Das Problem: viele BURUMUT-Buchstaben > T.
# Daher: U->ש(300), R->צ(90), M->מ(40) - sehr unbalanciert

# Korrekter Ansatz: BURUMUT-Buchstaben A-T direkt zu A=1..T=20 zuordnen
# U,V,W,X,Y,Z haben keine saubere Zuordnung in 22-Buchstaben-System

gematria_sum = sum(HEBREW[c] for c in heb if c in HEBREW)
print(f"BURUMUT (mit Mappings A=א..T=ת): Σ = {gematria_sum}")
print(f"  = {gematria_sum} (inkl. hohe Werte für U=ש(300), R=צ(90))")
print(f"  Vergleich ohne U/R/W/Y (die > T):")
no_high = [c for c in BURUMUT if c not in 'URWY']
heb_no_high = to_hebrew(''.join(no_high))
g2 = sum(HEBREW[c] for c in heb_no_high if c in HEBREW)
print(f"  BURUMUT ohne U/R/W/Y: Σ = {g2}")
print(f"  Vergleich mit BURUMUT-Summe 1232: {g2 == 1232}")

# 3. 3 Mothers + 7 Doubles in BURUMUT
print()
print("="*70")
print("Q28b.3: BURUMUT und Sefer Yetzirah Mothers/Doubles")
print("="*70)
MOTHERS = ['א','מ','ש']  # A, M, S
DOUBLES = ['ב','ג','ד','כ','פ','ר','ת']  # B, G, D, K, P, R, T
print(f"3 Mothers (Alef, Mem, Shin) → A, M, S")
for m in MOTHERS:
    cnt = BURUMUT.count(m)
    print(f"  {m} = '{BURUMUT[BURUMUT.index(m)] if m in BURUMUT else '?'}' : {cnt}x")
print(f"\n7 Doubles (Beth, Gimel, Dalet, Kaph, Pe, Resh, Tav) → B, G, D, K, P, R, T")
for d in DOUBLES:
    cnt = BURUMUT.count(d)
    print(f"  {d} : {cnt}x")

# 4. Was wenn die 7 Doubles die UAZBE-Region markieren?
print()
print("="*70)
print("Q28b.4: 7 Doubles + BURUMUT")
print("="*70)
# B, G, D, K, P, R, T sind die 7 Doubles
# BURUMUT enthaelt: B(7x), D(0), G(1), K(0), P(1), R(10x), T(3x)
# Fehlend in BURUMUT: D, K
# Vorhanden: B(7), G(1), P(1), R(10), T(3) = 22x
print(f"BURUMUT enthaelt 5/7 Doubles (B, G, P, R, T)")
print(f"Fehlend in BURUMUT: D, K (Dalet, Kaph)")
print(f"D und K = 'Dunkelheit' und 'Ahnlichkeit' im Hebraeischen")

# Was wenn die 7 Doubles die 7 Planeten repraesentieren?
# Sonne, Mond, Mars, Merkur, Jupiter, Venus, Saturn
print(f"\nD (Dalet) = 'Tur' = Saturn in Sefer Yetzirah")
print(f"K (Kaph) = 'Kokab' = Merkur in Sefer Yetzirah")
print(f"  -> BURUMUT enthaelt 5/7 Planeten! Merkur und Saturn fehlen.")

# 5. Numerische Konsistenz mit 7 Planeten + 12 Tierkreiszeichen
print()
print("="*70)
print("Q28b.5: 7+12 Struktur (Planeten+Zodiak)")
print("="*70)
# 7 Planeten + 12 Sternzeichen = 19 (BURUMUT-Alphabet!)
print(f"7 Planeten + 12 Tierkreiszeichen = 19 = BURUMUT-Alphabet!")
print(f"-> BURUMUT-Alphabet = 22 hebr. Konsonanten - 3 Mothers = 19 Simples")
print(f"   (Mothers א, מ, ש sind in BURUMUT = A, M, S vorhanden)")
print(f"-> Aber: A, M, S sind nicht 'Mothers' in BURUMUT-Sequenz")
