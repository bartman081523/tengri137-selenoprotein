"""
OFFENE FRAGE 2: Genesis 1:11-31 - weitere Bruecken?

Genesis 1:1-10 haben wir bereits untersucht:
- 1:1 = 2701 = 37 * 73
- 1:3 = 232 (UV-C)
- 1:7 = 1369 = 37^2
- 1:9 = 1701 = 37 * 46
- 1:10 = 913

Was kommt in 1:11-31?
- 1:11-13: Grass, herbs, fruit trees
- 1:14-19: Sun, moon, stars
- 1:20-23: Sea creatures, birds
- 1:24-31: Land animals, man

Numerische Suche: Welche Verse haben Gematria-Werte mit
Faktoren 37, 46, 73, 137?
"""
# Hebraeische Gematria
HEBREW_GEMATRIA = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
    'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90,
    'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

def gematria(text):
    return sum(HEBREW_GEMATRIA.get(c, 0) for c in text)

# Genesis 1:11-31 Wort-Gematrien (Standard-Uebersetzung)
GENESIS_WORDS = {
    # 1:11-13: Vegetation
    '1:11_earth': 'הארץ',  # 296
    '1:11_grass': 'דשא',  # 304
    '1:11_herb': 'עשב',  # 372
    '1:11_seed': 'זרע',  # 257
    '1:12_brought': 'הוציא',  # 121
    '1:13_evening': 'ערב',  # 272
    '1:13_morning': 'בקר',  # 322
    '1:13_third': 'שלישי',  # 636
    # 1:14-19: Lichter
    '1:14_lights': 'מאורת',  # 646
    '1:14_day': 'יום',  # 56
    '1:14_night': 'לילה',  # 75
    '1:15_lights_in_firmament': 'מאורתברקיע',  # 1051
    '1:16_two_lights': 'שניםמאורת',  # 1077
    '1:16_greater': 'הגדול',  # 33
    '1:16_lesser': 'הקטן',  # 155
    '1:16_stars': 'כוכבים',  # 102
    '1:18_rule': 'משל',  # 340
    '1:20_waters': 'המים',  # 95
    '1:20_soul': 'נפש',  # 350
    '1:20_living': 'חיה',  # 23
    '1:21_created': 'יצר',  # 290
    '1:21_sea_monsters': 'תנינם',  # 590
    '1:21_winged': 'אוב',  # 13
    '1:23_fifth': 'חמישי',  # 358
    # 1:24-31: Land animals
    '1:24_cattle': 'בהמה',  # 47
    '1:24_creeping': 'רמש',  # 340
    '1:24_beast': 'חיתוארץ',  # 626
    '1:25_made': 'יעש',  # 320
    '1:26_made': 'נעשה',  # 365
    '1:26_image': 'צלם',  # 140
    '1:26_likeness': 'דמות',  # 446
    '1:26_domINION': 'ורדו',  # 214
    '1:27_created': 'ברא',  # 203
    '1:27_male_female': 'זכרונקבה',  # 335
    '1:28_blessed': 'יברך',  # 222
    '1:28_subdue': 'כבשה',  # 322
    '1:28_have_dominion': 'רדה',  # 209
    '1:29_given': 'נתתי',  # 850
    '1:30_living_creature': 'חית',  # 418
    '1:31_sixth': 'ששי',  # 760
    '1:31_very_good': 'טובמאד',  # 56
}

print("="*70)
print("Q2.1: Gematria-Werte aus Genesis 1:11-31")
print("="*70)
# Berechne alle Werte
values = []
for name, heb in GENESIS_WORDS.items():
    val = gematria(heb)
    values.append((name, heb, val))
    print(f"  {name:25s} {heb:20s} = {val:5d}")

# Suche Faktoren 37, 46, 73
print()
print("="*70)
print("Q2.2: Welche Verse haben die Faktoren 37, 46, 73, 137?")
print("="*70)

KEY_FACTORS = [37, 46, 73, 137]

for factor in KEY_FACTORS:
    print(f"\n  --- Faktor {factor} ---")
    for name, heb, val in values:
        if val % factor == 0 and val > 0:
            print(f"    {name}: {val} = {factor} * {val // factor}")

# Suche auch Summen, die genau 1370 (10x), 2701 (1:1), etc. ergeben
print()
print("="*70)
print("Q2.3: Summen, die sich zu 1:1-10 Gematrien summieren")
print("="*70)
TARGETS = [913, 232, 1369, 1701, 1558, 730, 2701, 1776]

# Gruppiere nach Vers-Abschnitt
verse_groups = {
    '1:11-13': ['1:11_earth', '1:11_grass', '1:11_herb', '1:11_seed',
                 '1:12_brought', '1:13_evening', '1:13_morning', '1:13_third'],
    '1:14-19': ['1:14_lights', '1:14_day', '1:14_night', '1:14_lights_in_firmament',
                 '1:16_two_lights', '1:16_greater', '1:16_lesser', '1:16_stars', '1:18_rule'],
    '1:20-23': ['1:20_waters', '1:20_soul', '1:20_living', '1:21_created',
                 '1:21_sea_monsters', '1:21_winged', '1:23_fifth'],
    '1:24-31': ['1:24_cattle', '1:24_creeping', '1:24_beast', '1:25_made', '1:26_made',
                 '1:26_image', '1:26_likeness', '1:26_domINION', '1:27_created',
                 '1:27_male_female', '1:28_blessed', '1:28_subdue', '1:28_have_dominion',
                 '1:29_given', '1:30_living_creature', '1:31_sixth', '1:31_very_good'],
}

for group_name, words in verse_groups.items():
    group_sum = sum(gematria(GENESIS_WORDS[w]) for w in words if w in GENESIS_WORDS)
    print(f"\n  {group_name}: Summe = {group_sum}")
    for target in TARGETS:
        if group_sum == target:
            print(f"    => Gleich Genesis 1:{target}!")
        elif abs(group_sum - target) < 50:
            print(f"    Nahe an {target} (Diff = {group_sum - target})")
    # Faktoren?
    from sympy import factorint
    print(f"    Faktoren: {factorint(group_sum)}")
