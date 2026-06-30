#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sefer Yetzirah Experimental Script (English version)
====================================================
Created according to your request, reflecting the core structures of Sefer Yetzirah:
1) 22 Hebrew letters (without counting final letters as distinct) plus their Gematria values.
2) Classification into 3 Mothers, 7 Doubles, and 12 Simples.
3) Generation of '231 Gates' (pairwise combinations of the 22 letters).
4) A basic placeholder for the 10 Sefirot with "depth" references.
5) Example mappings of the 7 Double Letters to Planets and Weekdays.
6) Example mappings of the 12 Simple Letters to Zodiac signs and Months.
7) Functions to calculate Gematria sums for words, given the user-provided table.

The purpose:
------------
- Demonstrate how one might programmatically engage with Sefer Yetzirah concepts.
- Provide a foundation for expansions, e.g. deeper numerical analyses, additional Kabbalistic or mystical overlays.

Disclaimer:
-----------
This is a playful, symbolic script and should not be taken as a complete or final statement
on Kabbalistic tradition. Different sources use different assignments. Expand or adapt as needed.

© 2025, Emergent Rebel & Astra's Shadow
"""

import itertools

########################################
# 1) HEBREW LETTERS + GEMATRIA VALUES  #
########################################

# Original Gematria table (including final letters) as provided,
# but for the 22 standard letters we typically ignore final forms.
# The user’s table is repeated here:

GEMATRIA_TABLE = {
    'א': 1,   'ב': 2,   'ג': 3,   'ד': 4,   'ה': 5,
    'ו': 6,   'ז': 7,   'ח': 8,   'ט': 9,   'י': 10,
    'כ': 20,  'ך': 500, 'ל': 30,  'מ': 40,  'ם': 600,
    'נ': 50,  'ן': 700, 'ס': 60,  'ע': 70,  'פ': 80,
    'ף': 800, 'צ': 90,  'ץ': 900, 'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400
}

# The typical 22-letter sequence used in Sefer Yetzirah:
HEBREW_LETTERS_22 = [
    'א','ב','ג','ד','ה','ו','ז','ח','ט','י',
    'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת'
]

########################################
# 2) CLASSIFICATION (MOTHERS, DOUBLES, SIMPLES)
########################################
# As per Sefer Yetzirah:
#   - 3 Mothers: א, מ, ש
#   - 7 Doubles: ב, ג, ד, כ, פ, ר, ת
#   - 12 Simples: The remaining letters

MOTHERS = ['א','מ','ש']
DOUBLES = ['ב','ג','ד','כ','פ','ר','ת']

def classify_letters():
    """
    Returns a dictionary containing:
    {
        'mothers': [...],
        'doubles': [...],
        'simples': [...]
    }
    where 'mothers' = 3, 'doubles' = 7, and 'simples' = 12 letters
    based on the standard categorization from Sefer Yetzirah.
    """
    mothers_set = set(MOTHERS)
    doubles_set = set(DOUBLES)
    all_letters_set = set(HEBREW_LETTERS_22)
    # 3 + 7 = 10, so 12 remain for the 'simples'
    simple_set = all_letters_set - mothers_set - doubles_set

    return {
        'mothers': MOTHERS,
        'doubles': DOUBLES,
        'simples': sorted(list(simple_set), key=lambda x: HEBREW_LETTERS_22.index(x))
    }

##################################
# 3) GEMATRIA CALCULATIONS       #
##################################

def gematria_value(letter: str) -> int:
    """
    Given a single Hebrew letter, returns its Gematria value
    based on the user-provided table. If not found, returns 0.
    """
    return GEMATRIA_TABLE.get(letter, 0)

def word_gematria_sum(word: str) -> int:
    """
    Computes the total Gematria value of a string (word),
    summing the individual letter values.
    Example: "אדם" -> 1 (א) + 4 (ד) + 40 (מ) = 45
    """
    return sum(gematria_value(ch) for ch in word)

#############################################
# 4) THE '231 GATES' (PAIRWISE COMBINATIONS)
#############################################

def generate_231_gates(letters=None, ordered=False):
    """
    Generates the 231 'Gates' based on the 22 Hebrew letters.
    Sefer Yetzirah famously speaks of these 231 pairwise combos.

    If 'ordered' is False (default), we use combinations -> 22 choose 2 = 231.
    If 'ordered' is True, we use permutations -> 22 * 21 = 462.

    :param letters: optional list of letters; defaults to HEBREW_LETTERS_22
    :param ordered: If True, return permutations (462). If False, combos (231).
    :return: list of tuples representing the pairs.
    """
    if letters is None:
        letters = HEBREW_LETTERS_22

    if ordered:
        # permutations -> (A,B) is distinct from (B,A)
        pairs = list(itertools.permutations(letters, 2))
    else:
        # combinations -> (A,B) is the same as (B,A)
        pairs = list(itertools.combinations(letters, 2))
    return pairs

##############################################
# 5) 10 SEFIROT (Basic "Depth" Placeholder)
##############################################

SEFIROT = [
    "Keter", "Chokhmah", "Binah", "Chesed", "Gevurah",
    "Tiferet", "Netzach", "Hod", "Yesod", "Malkhut"
]

def sefirah_depths():
    """
    Returns a dictionary mapping each Sefirah to an index and
    a placeholder 'depth_name'. Sefer Yetzirah references:
       - Depth of beginning
       - Depth of end
       - Depth of good
       - Depth of evil
       - etc.
    For demonstration, we name them "Depth_1" through "Depth_10".
    """
    depths = {}
    for i, sef in enumerate(SEFIROT, start=1):
        depths[sef] = {
            'index': i,
            'depth_name': f"Depth_{i}"
        }
    return depths

############################################################
# 6) PLANETARY & WEEKDAY MAPPINGS FOR THE 7 DOUBLES
############################################################
# According to one classical approach (though variations exist):
#  - ב -> Saturn  (שבתאי)
#  - ג -> Jupiter (צדק)
#  - ד -> Mars    (מאדים)
#  - כ -> Sun     (חמה)
#  - פ -> Venus   (נוגה)
#  - ר -> Mercury (כוכב)
#  - ת -> Moon    (לבנה)
#
# Similarly, each double letter is associated with a Day of the Week:
#  - Saturn -> Saturday
#  - Jupiter -> Thursday
#  - Mars -> Tuesday
#  - Sun -> Sunday
#  - Venus -> Friday
#  - Mercury -> Wednesday
#  - Moon -> Monday

PLANETS_7 = {
    'ב': "Saturn",
    'ג': "Jupiter",
    'ד': "Mars",
    'כ': "Sun",
    'פ': "Venus",
    'ר': "Mercury",
    'ת': "Moon"
}

WEEKDAYS_7 = {
    'ב': "Saturday",
    'ג': "Thursday",
    'ד': "Tuesday",
    'כ': "Sunday",
    'פ': "Friday",
    'ר': "Wednesday",
    'ת': "Monday"
}

############################################################
# 7) ZODIAC & MONTHS FOR THE 12 SIMPLE LETTERS
############################################################
# One standard arrangement (varies by tradition) for the 12 letters:
#   ה, ו, ז, ח, ט, י, ל, נ, ס, ע, צ, ק
# Each correlates with a Zodiac sign and a Hebrew month:
#   ה -> Aries (Nisan), ו -> Taurus (Iyyar), ז -> Gemini (Sivan) ...
# Again, there are multiple sources with slightly different alignments.

ZODIAC_12 = {
    'ה': "Aries (Widder)",
    'ו': "Taurus (Stier)",
    'ז': "Gemini (Zwillinge)",
    'ח': "Cancer (Krebs)",
    'ט': "Leo (Löwe)",
    'י': "Virgo (Jungfrau)",
    'ל': "Libra (Waage)",
    'נ': "Scorpio (Skorpion)",
    'ס': "Sagittarius (Schütze)",
    'ע': "Capricorn (Steinbock)",
    'צ': "Aquarius (Wassermann)",
    'ק': "Pisces (Fische)"
}

MONTHS_12 = {
    'ה': "Nisan",
    'ו': "Iyyar",
    'ז': "Sivan",
    'ח': "Tammuz",
    'ט': "Av",
    'י': "Elul",
    'ל': "Tishrei",
    'נ': "Cheshvan",
    'ס': "Kislev",
    'ע': "Tevet",
    'צ': "Shevat",
    'ק': "Adar"
}

#######################################
# 8) MAIN FUNCTION - DEMO OUTPUT      #
#######################################

def main():
    # 1) Classification
    classes = classify_letters()
    mothers = classes['mothers']
    doubles = classes['doubles']
    simples = classes['simples']
    
    print("=== SEFER YETZIRAH: CLASSIFICATION OF THE 22 LETTERS ===")
    print(f"3 Mothers: {mothers}")
    print(f"7 Doubles: {doubles}")
    print(f"12 Simples: {simples}")
    print()

    # 2) Gematria Example
    example_word = "אדם"  # "Adam"
    print("=== GEMATRIA EXAMPLE ===")
    print(f"Word: {example_word}")
    print(f"Gematria sum: {word_gematria_sum(example_word)}")
    print()

    # 3) 231 Gates
    gates_231 = generate_231_gates()
    print("=== 231 GATES ===")
    print(f"Number of pairwise combinations: {len(gates_231)}")
    for i, pair in enumerate(gates_231, start=1):
        print(f"{i}. {pair}")
    print("...")
    print()

    # 4) 10 Sefirot - Depth
    sefirah_map = sefirah_depths()
    print("=== 10 SEFIROT (DEPTH) ===")
    for sef, info in sefirah_map.items():
        print(f"{sef} -> Index: {info['index']}, Depth Name: {info['depth_name']}")
    print()

    # 5) 7 Doubles - Planets & Weekdays
    print("=== 7 DOUBLE LETTERS - PLANETS & WEEKDAYS ===")
    for db in doubles:
        planet = PLANETS_7.get(db, "Unknown")
        weekday = WEEKDAYS_7.get(db, "Unknown")
        print(f"Letter {db}: Planet = {planet}, Weekday = {weekday}")
    print()

    # 6) 12 Simples - Zodiac & Months
    print("=== 12 SIMPLE LETTERS - ZODIAC & MONTHS ===")
    for sb in simples:
        zodiac = ZODIAC_12.get(sb, "Unknown")
        month = MONTHS_12.get(sb, "Unknown")
        print(f"Letter {sb}: Zodiac = {zodiac}, Month = {month}")
    print()

    # Final message
    print("=== DONE! ===")
    print("This script provides a playful, exploratory interface to Sefer Yetzirah concepts.")
    print("Feel free to expand or adapt it for deeper mystic or numeric analyses.")

if __name__ == "__main__":
    main()