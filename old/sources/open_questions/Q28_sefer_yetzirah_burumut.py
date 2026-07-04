"""
Q28 (NEU): Sefer Yetzirah + BURUMUT
Sefer Yetzirah (Buch der Schöpfung) ist ein kabbalistischer Text,
der die 22 hebräischen Buchstaben als Grundlage der Schöpfung beschreibt.

Wir testen, ob BURUMUT eine numerische Entsprechung zu den
22 + 231 Gates von Sefer Yetzirah hat.
"""
HEBREW = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
    'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90,
    'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}
# 22 hebr. Konsonanten
HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
             'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']

BURUMUT = 'BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN'

# 1. BURUMUT in hebr. Buchstaben-Mapping
print("="*70)
print("Q28.1: BURUMUT <-> Hebräische Buchstaben (1-zu-1 Mapping)")
print("="*70)
heb_map = ''.join(HEBREW_22[ord(c) - ord('A')] for c in BURUMUT)
print(f"BURUMUT ({len(BURUMUT)} Zeichen):")
print(f"  {BURUMUT}")
print(f"Hebräisch-Mapping (A→א, B→ב, ...):")
print(f"  {heb_map}")
print()

# 2. Gematria der gemappten hebr. Buchstaben
print("="*70)
print("Q28.2: BURUMUT als hebr. Wort-Gematria")
print("="*70)
gematria_sum = sum(HEBREW[c] for c in heb_map)
print(f"BURUMUT → hebr. Σ = {gematria_sum}")
print(f"  = 2+21+18+21+13+21+20+18+5+6+1+13+20+21+... = {gematria_sum}")

# Vergleich mit wichtigen Zahlen
print(f"\nVergleich:")
print(f"  BURUMUT-Gematria: {gematria_sum}")
print(f"  22 × Gematria-Mittel = 22 × 100.5 = {22 * 100.5}")
print(f"  99 (BURUMUT-Laenge) × 16.5 = {99 * 16.5}")
print(f"  Ist BURUMUT-Gematria = 1232 (BURUMUT-Summe)? {gematria_sum == 1232}")

# 3. Sefer Yetzirah 22-Buchstaben-Permutationen
print()
print("="*70)
print("Q28.3: Sefer Yetzirah 231 Gates + BURUMUT")
print("="*70)
# 231 = 22*21/2 = 231 Gates (Paare von Buchstaben)
print(f"231 = 22 × 21 / 2 = 231 Gates (Sefer Yetzirah)")
print(f"BURUMUT hat 99 Zeichen, 99/3 = 33 Tripel")
print(f"33 Tripel × 3 = 99")
print(f"33 = 3 × 11 = 11 × 3 (Sec × Pil?)")
print(f"33 = Anzahl der Bones im Rueckgrat des Menschen!")

# 4. Vergleich BURUMUT-Mapping mit Genesis 1:1
print()
print("="*70)
print("Q28.4: BURUMUTREFAMTU vs Genesis 1:1 (hebr.)")
print("="*70)
BURUMUT_HEB = ''.join(HEBREW_22[ord(c) - ord('A')] for c in 'BURUMUTREFAMTU')
GEN_1_1 = 'בראשיתבראאלהיםאתהשמיםואתהארץ'
print(f"BURUMUTREFAMTU hebr.: {BURUMUT_HEB}")
print(f"Genesis 1:1 hebr.:    {GEN_1_1}")
print()
# Gematria-Vergleich
g_burumut = sum(HEBREW[c] for c in BURUMUT_HEB)
g_gen11 = sum(HEBREW[c] for c in GEN_1_1)
print(f"Gematria BURUMUTREFAMTU: {g_burumut}")
print(f"Gematria Genesis 1:1:    {g_gen11}")
print(f"Differenz: {g_gen11 - g_burumut}")
print(f"Verhältnis: {g_burumut / g_gen11:.4f}")

# 5. Sefer Yetzirah Permutationen auf BURUMUTREFAMTU
print()
print("="*70)
print("Q28.5: Permutationen von BURUMUTREFAMTU (hebr.)")
print("="*70)
unique_chars = set(BURUMUT_HEB)
print(f"Unique hebr. Buchstaben in BURUMUTREFAMTU: {len(unique_chars)}")
from collections import Counter
char_freq = Counter(BURUMUT_HEB)
for c, n in char_freq.most_common():
    print(f"  {c}: {n}x")

# Permutationen zaehlen
import math
perms = math.factorial(14)
# Aber mit Wiederholungen:
from sympy import factorial
n_perms = factorial(14)
for f in char_freq.values():
    n_perms //= factorial(f)
print(f"\nAnzahl Permutationen: {n_perms}")
print(f"  (zum Vergleich: 231 Gates = 22*21/2 = 231)")

# 6. 22 hebr. Buchstaben in BURUMUT?
print()
print("="*70)
print("Q28.6: Welche der 22 hebr. Buchstaben kommen in BURUMUT vor?")
print("="*70)
present = set(BURUMUT_HEB)
absent = set(HEBREW_22) - present
print(f"Vorhanden ({len(present)}): {sorted(present)}")
print(f"Abwesend ({len(absent)}): {sorted(absent)}")

# 7. 3 Mothers + 7 Doubles?
print()
print("="*70)
print("Q28.7: BURUMUT und die 3 Mothers + 7 Doubles (Sefer Yetzirah)")
print("="*70)
MOTHERS = ['א','מ','ש']
DOUBLES = ['ב','ג','ד','כ','פ','ר','ת']
print(f"3 Mothers: {MOTHERS}")
for m in MOTHERS:
    cnt = BURUMUT_HEB.count(m)
    print(f"  {m} (Mother): {cnt}x in BURUMUTREFAMTU")
print(f"\n7 Doubles: {DOUBLES}")
for d in DOUBLES:
    cnt = BURUMUT_HEB.count(d)
    print(f"  {d} (Double): {cnt}x in BURUMUTREFAMTU")
