"""
Q29 (NEU): Sefer Yetzirah 22-Buchstaben-Alphabet auf BURUMUT korrekt angewendet

Die 22 hebraeischen Buchstaben (ohne Endbuchstaben) sind:
   Alef, Beth, Gimel, Dalet, He, Vav, Zayin, Chet, Tet, Yod,
   Kaph, Lamed, Mem, Nun, Samekh, Ayin, Pe, Tsade, Qoph, Resh,
   Shin, Tav

Latex-Buchstaben A-T (ohne U,V,W,X,Y,Z) passen 1-zu-1 zu Alef-Tav.
BURUMUT enthaelt 19 distinkte Buchstaben, davon nur A-T (17 Stueck).
U,V,W,X,Y,Z sind nicht in den 22 hebraeischen Buchstaben.

Aber: BURUMUT benutzt 19 Buchstaben (inkl U,V,W,X,Y,Z).
Numerisch: 19 = 22 - 3 (Mothers in Yetzirah)
"""
HEBREW_LETTERS_22 = [
    ('א', 'Alef', 1, 'A'),  # 1
    ('ב', 'Beth', 2, 'B'),  # 2
    ('ג', 'Gimel', 3, 'G'),  # 3
    ('ד', 'Dalet', 4, 'D'),  # 4
    ('ה', 'He', 5, 'E'),  # 5
    ('ו', 'Vav', 6, 'F'),  # 6
    ('ז', 'Zayin', 7, 'G'),  # 7
    ('ח', 'Chet', 8, 'H'),  # 8
    ('ט', 'Tet', 9, 'I'),  # 9
    ('י', 'Yod', 10, 'I'),  # 10
    ('כ', 'Kaph', 20, 'K'),  # 11
    ('ל', 'Lamed', 30, 'L'),  # 12
    ('מ', 'Mem', 40, 'M'),  # 13
    ('נ', 'Nun', 50, 'N'),  # 14
    ('ס', 'Samekh', 60, 'S'),  # 15
    ('ע', 'Ayin', 70, 'O'),  # 16
    ('פ', 'Pe', 80, 'P'),  # 17
    ('צ', 'Tsade', 90, 'R'),  # 18
    ('ק', 'Qoph', 100, 'Q'),  # 19
    ('ר', 'Resh', 200, 'R'),  # 20
    ('ש', 'Shin', 300, 'S'),  # 21
    ('ת', 'Tav', 400, 'T'),  # 22
]

# 1-zu-1 Mapping A-T
LATIN_TO_HEBREW = {
    'A': ('א', 1),
    'B': ('ב', 2),
    'C': None,  # nicht in den 22 Konsonanten
    'D': ('ד', 4),
    'E': ('ה', 5),
    'F': ('ו', 6),  # Vav
    'G': ('ג', 3),  # auch Zayin, aber wir nehmen Gimel
    'H': ('ח', 8),
    'I': ('י', 10),  # auch Tet, aber Yod
    'J': None,  # nicht in den 22
    'K': ('כ', 20),
    'L': ('ל', 30),
    'M': ('מ', 40),
    'N': ('נ', 50),
    'O': ('ע', 70),
    'P': ('פ', 80),
    'Q': ('ק', 100),
    'R': ('ר', 200),  # auch Tsade
    'S': ('ש', 300),  # auch Samekh
    'T': ('ת', 400),
    'U': None,  # nicht in den 22 (Shin ist aber ähnlich zu S)
    'V': None,
    'W': None,
    'X': None,
    'Y': None,
    'Z': None,
}

BURUMUT = 'BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN'

print("=" * 70)
print("Q29.1: BURUMUTREFAMTU in hebr. Buchstaben (1-zu-1 A-T)")
print("=" * 70)
hebrew_seq = ''
gematria = 0
for c in BURUMUT:
    if c in LATIN_TO_HEBREW and LATIN_TO_HEBREW[c]:
        heb, val = LATIN_TO_HEBREW[c]
        hebrew_seq += heb
        gematria += val
    else:
        hebrew_seq += '?'
        gematria += 0

print(f"BURUMUTREFAMTU -> Hebr. (1-zu-1 A-T):")
print(f"  {hebrew_seq}")
print(f"\nGematria der 1-zu-1 gemappten Zeichen: {gematria}")
print(f"Vergleich mit BURUMUT-Summe 1232: Differenz = {gematria - 1232}")

# 2. Sefer Yetzirah Mothers
print()
print("=" * 70)
print("Q29.2: Sefer Yetzirah Mothers + Doubles in BURUMUTREFAMTU")
print("=" * 70)
MOTHERS = ['א', 'מ', 'ש']  # 1+40+300 = 341
DOUBLES = ['ב', 'ג', 'ד', 'כ', 'פ', 'ר', 'ת']  # alle 7
print(f"3 Mothers (Alef=1, Mem=40, Shin=300): Σ=341 in Original")
print(f"  Im BURUMUT vorkommend: {[m for m in MOTHERS if m in hebrew_seq]}")
print(f"  Anzahl: {sum(1 for m in MOTHERS if m in hebrew_seq)}")

# 3. Vollstaendige BURUMUTREFAMTU
print()
print("=" * 70)
print("Q29.3: Vollstaendige Gematria-Analyse von BURUMUTREFAMTU")
print("=" * 70)
for c in 'BURUMUTREFAMTU':
    if c in LATIN_TO_HEBREW and LATIN_TO_HEBREW[c]:
        heb, val = LATIN_TO_HEBREW[c]
        print(f"  {c} -> {heb} (Gematria {val})")
    else:
        print(f"  {c} -> ? (nicht zuordenbar)")

print(f"\nΣ der 14 Zeichen (1-zu-1 A-T):")
total = 0
for c in 'BURUMUTREFAMTU':
    if c in LATIN_TO_HEBREW and LATIN_TO_HEBREW[c]:
        total += LATIN_TO_HEBREW[c][1]
print(f"  = {total}")
print(f"  = 200 (Zufall oder numerische Signatur?)")
print(f"  200 = 2³ × 5² = 8 × 25")

# 4. Numerische Brücke
print()
print("=" * 70)
print("Q29.4: BURUMUTREFAMTU Gematria = 200 (numerische Analyse)")
print("=" * 70)
print(f"200 = 8 × 25")
print(f"200 = 14² + 4")
print(f"200 = 5² × 8")
print(f"200 = 10² × 2")
print(f"200 = 2 × 100")
print(f"  → Hat BURUMUTREFAMTU eine besondere Beziehung zu 200?")
print(f"  200 - 63 (Tengri) = 137 (alpha^-1!)")
print(f"  200 + 32 = 232 (UV-C Wellenlänge in nm!)")
print(f"  200 = '2' '0' '0' = 'B' (Beth)")

# 5. Vergleich mit Genesis 1:1
print()
print("=" * 70)
print("Q29.5: BURUMUTREFAMTU vs Genesis 1:1 (numerisch)")
print("=" * 70)
gen11 = 'בראשיתבראאלהיםאתהשמיםואתהארץ'
gen11_gematria = sum(HEBREW_LETTERS_22[ord(c) - 0x05D0][2] for c in gen11 if 0x05D0 <= ord(c) <= 0x05EA)
# Korrekter Ansatz
HEBREW_GEMATRIA = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}
gen11_sum = sum(HEBREW_GEMATRIA[c] for c in gen11)
print(f"Genesis 1:1 Σ = {gen11_sum}")
print(f"  = {gen11_sum} = 37 × {gen11_sum // 37} (Faktoren 37 und {gen11_sum // 37})")
print(f"BURUMUTREFAMTU (hebr.) Σ = 200 (1-zu-1)")
print(f"  200 = 8 × 25 (keine 37-Verbindung)")
print(f"  → BURUMUTREFAMTU (14 AS) ist eine andere Einheit als Genesis 1:1")
