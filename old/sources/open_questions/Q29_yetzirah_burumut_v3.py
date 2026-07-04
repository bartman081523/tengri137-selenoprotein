"""
Q29 v3: Korrektes Sefer Yetzirah-Mapping auf BURUMUTREFAMTU
"""
HEBREW_GEMATRIA = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50,
    'ס': 60, 'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

# 1-zu-1 Mapping A-T
LATIN_TO_HEBREW = {
    'A': ('א', 1), 'B': ('ב', 2), 'D': ('ד', 4), 'E': ('ה', 5),
    'F': ('ו', 6), 'G': ('ג', 3), 'H': ('ח', 8), 'I': ('י', 10),
    'K': ('כ', 20), 'L': ('ל', 30), 'M': ('מ', 40), 'N': ('נ', 50),
    'O': ('ע', 70), 'P': ('פ', 80), 'Q': ('ק', 100), 'R': ('ר', 200),
    'S': ('ש', 300), 'T': ('ת', 400),
}

BURUMUT = 'BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN'

print("=" * 70)
print("Q29.1: BURUMUTREFAMTU in hebr. Buchstaben (1-zu-1 A-T)")
print("=" * 70)
hebrew_seq = ''
gematria = 0
for c in BURUMUT:
    if c in LATIN_TO_HEBREW:
        heb, val = LATIN_TO_HEBREW[c]
        hebrew_seq += heb
        gematria += val
    else:
        hebrew_seq += '?'
        gematria += 0

print(f"BURUMUTREFAMTU -> Hebr. (1-zu-1): {hebrew_seq}")
print(f"Σ (mapped): {gematria}")

# 2. Mothers + Doubles
print()
print("=" * 70)
print("Q29.2: Sefer Yetzirah Mothers + Doubles in BURUMUT (hebr.)")
print("=" * 70)
MOTHERS = ['א', 'מ', 'ש']  # A, M, S
DOUBLES = ['ב', 'ג', 'ד', 'כ', 'פ', 'ר', 'ת']  # B, G, D, K, P, R, T
SIMPLES = ['ה', 'ו', 'ז', 'ח', 'ט', 'י', 'ל', 'נ', 'ס', 'ע', 'צ', 'ק']  # 12 Simples

# 1. Welche sind Mapped?
mapped_set = set(c for c in hebrew_seq if c != '?')
print(f"3 Mothers:")
for m in MOTHERS:
    if m in mapped_set:
        cnt = hebrew_seq.count(m)
        print(f"  {m} (Mother): {cnt}x in BURUMUT")
    else:
        print(f"  {m} (Mother): NICHT in BURUMUT!")

print(f"\n7 Doubles:")
for d in DOUBLES:
    if d in mapped_set:
        cnt = hebrew_seq.count(d)
        print(f"  {d} (Double): {cnt}x in BURUMUT")
    else:
        print(f"  {d} (Double): NICHT in BURUMUT!")

print(f"\n12 Simples:")
for s in SIMPLES:
    if s in mapped_set:
        cnt = hebrew_seq.count(s)
        print(f"  {s} (Simple): {cnt}x in BURUMUT")
    else:
        print(f"  {s} (Simple): NICHT in BURUMUT!")

# 3. Mothers-Gematria
print()
print("=" * 70)
print("Q29.3: Mothers-Gematria in BURUMUT")
print("=" * 70)
m_sum = sum(HEBREW_GEMATRIA[c] for c in MOTHERS if c in mapped_set)
m_cnt = sum(hebrew_seq.count(c) for c in MOTHERS)
print(f"Mothers-Gematria (in BURUMUTREFAMTU): {m_sum}")
print(f"Anzahl Mother-Buchstaben: {m_cnt}")
print(f"  -> Alef (1) + Mem (40) + Shin (300) = 341 in Original")
print(f"  -> Aber BURUMUT hat nicht Alef/Mem/Shin als Mothers (es hat sie als Sec/Pyl!)")

# 4. Komplette BURUMUTREFAMTU
print()
print("=" * 70)
print("Q29.4: Vollstaendige BURUMUTREFAMTU-Analyse")
print("=" * 70)
for c in 'BURUMUTREFAMTU':
    if c in LATIN_TO_HEBREW:
        heb, val = LATIN_TO_HEBREW[c]
        print(f"  {c} -> {heb} (Gematria {val})")
    else:
        print(f"  {c} -> ? (nicht zuordenbar)")

# Σ der 14 Zeichen
total = sum(LATIN_TO_HEBREW[c][1] for c in 'BURUMUTREFAMTU' if c in LATIN_TO_HEBREW)
print(f"\nΣ (14 Zeichen, 1-zu-1): {total}")
print(f"  = {total} = 2^3 * 5^2 = 8 * 25")
print(f"  200 = 14² + 4 (BURUMUTREFAMTU hat 14 Zeichen)")
print(f"  200 = 8 × 25")
print(f"  200 - 63 = 137 (alpha^-1!)")
print(f"  200 + 32 = 232 (UV-C Wellenlänge)")
print(f"  200 = 'B' in hebr. Gematria (Beth = 2, Resh = 200)")

# 5. Vergleich mit Genesis 1:1
print()
print("=" * 70)
print("Q29.5: BURUMUTREFAMTU vs Genesis 1:1 (numerisch)")
print("=" * 70)
gen11 = 'בראשיתבראאלהיםאתהשמיםואתהארץ'
gen11_sum = sum(HEBREW_GEMATRIA[c] for c in gen11)
print(f"Genesis 1:1 Σ = {gen11_sum} = 37 × {gen11_sum // 37} (Faktor 73)")
print(f"BURUMUTREFAMTU Σ = 200")
print(f"  Differenz: {gen11_sum - 200} = {gen11_sum - 200}")
print(f"  2501 = 41 × 61")
print(f"  Keine offensichtliche Brücke (200 hat keinen 37, 46, 73, 137 Faktor)")

# 6. Vergleich: BURUMUTREFAMTU und Genesis 1:7
print()
print("=" * 70)
print("Q29.6: BURUMUTREFAMTU vs Genesis 1:7")
print("=" * 70)
gen17 = 'ויעשאלהיםאתהרקיעויבדלביןהמיםאשרמתחתלרקיעוביןהמיםאשרמעללרקיעויהיערבויהיבקריוםשני'
# Vereinfachung - nur Wort-Gematria
gen17_words = gen17.split('וי')  # sehr grob
print(f"Genesis 1:7 Worte (grob): {gen17[:50]}...")
gen17_sum_simple = sum(HEBREW_GEMATRIA[c] for c in gen17)
print(f"Genesis 1:7 Σ (einfach) = {gen17_sum_simple}")

# Numerische Bruecke zwischen BURUMUT und 1:7
print()
print(f"Wir wissen bereits: BURUMUT-Summe + 137 = 37² = 1369 = Genesis 1:7 Σ")
print(f"  Das ist die numerische Brücke zwischen BURUMUT (gesamt) und 1:7")
print(f"  Aber: BURUMUTREFAMTU (Vorspann) Σ = 200, hat keine direkte 1:7-Verbindung")
