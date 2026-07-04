#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grand Unified Kabbalistic Script (Final Update)
===============================================
Purpose:
--------
This Python script merges multiple Kabbalistic constructs from Sefer Yetzirah:
1) 22 Hebrew letters (standard forms) with:
   - Original Hebrew names (e.g. "אלף" for א)
   - Gematria sums of each letter's name
   - Classification into 3 Mothers, 7 Doubles, 12 Simples

2) Sefirot (10 emanations) with Hebrew names (e.g. כתר for Keter) + gematria sums.

3) Generation of 231 Gates (pairs of letters) with:
   - Combined gematria sums for each pair
   - Basic numeric manipulations (ratios, differences, etc.)

4) A placeholder mechanism for 72 Triplets (referencing the "72 Names")
   - Each triplet is assigned a gematria sum (placeholder array)

5) A function to "append 'אל'/'על' suffix" to words,
   to see how gematria changes (some expansions from Kabbalistic texts).

6) A function that performs the exact geometric calculations
   referencing the 216 vs. 231 arrangement in Sefer Yetzirah:
   - 216 (6^3) => often linked to the six directions sealed thrice
   - 231 => number of 2-letter combinations from 22 letters

7) Proper definitions of all functions, including gates_numeric_analysis(),
   to avoid NameErrors.

Disclaimers:
------------
This script is an experimental sandbox demonstrating numeric manipulations
in a Kabbalistic context, not an authoritative commentary on Sefer Yetzirah.
"""

import itertools

###############################################################################
# 1) HEBREW LETTERS: Original Names, Gematria Table, Basic Info
###############################################################################

# Main Gematria Table (including final letters).
# In Sefer Yetzirah classification, final letters are not separate from the 22 standard.
GEMATRIA_TABLE = {
    'א': 1,   'ב': 2,   'ג': 3,   'ד': 4,   'ה': 5,
    'ו': 6,   'ז': 7,   'ח': 8,   'ט': 9,   'י': 10,
    'כ': 20,  'ך': 500, 'ל': 30,  'מ': 40,  'ם': 600,
    'נ': 50,  'ן': 700, 'ס': 60,  'ע': 70,  'פ': 80,
    'ף': 800, 'צ': 90,  'ץ': 900, 'ק': 100, 'ר': 200,
    'ש': 300, 'ת': 400
}

# The 22 standard letters used in Sefer Yetzirah:
STANDARD_22_LETTERS = [
    'א','ב','ג','ד','ה','ו','ז','ח','ט','י',
    'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת'
]

# Original Hebrew spelled-out names for these letters
HEBREW_LETTER_NAMES = {
    'א': 'אלף',   # ALEPH
    'ב': 'בית',   # BET
    'ג': 'גימל',  # GIMEL
    'ד': 'דלת',   # DALET
    'ה': 'הא',    # HE
    'ו': 'ואו',   # VAV
    'ז': 'זין',   # ZAYIN
    'ח': 'חית',   # CHET
    'ט': 'טית',   # TET
    'י': 'יוד',   # YOD
    'כ': 'כף',    # KAF
    'ל': 'למד',   # LAMED
    'מ': 'מם',    # MEM
    'נ': 'نون',   # NUN (variant spelling)
    'ס': 'סמך',   # SAMEKH
    'ע': 'עין',   # AYIN
    'פ': 'פה',    # PE
    'צ': 'צדי',   # TSADI
    'ק': 'קוף',   # QOF
    'ר': 'ריש',   # RESH
    'ש': 'שין',   # SHIN
    'ת': 'תיו',   # TAV
}

def gematria_value(letter: str) -> int:
    """Returns the gematria value of a single letter (including finals)."""
    return GEMATRIA_TABLE.get(letter, 0)

def gematria_sum_of_word(word: str) -> int:
    """
    Returns the sum of gematria values for each character in 'word'.
    Example: gematria_sum_of_word("אדם") => 1 + 4 + 40 = 45
    """
    return sum(gematria_value(ch) for ch in word)

def letter_name_gematria(letter: str) -> int:
    """
    For a single letter (e.g. 'א'), compute gematria of its spelled-out name (e.g. 'אלף').
    """
    name = HEBREW_LETTER_NAMES.get(letter, "")
    return gematria_sum_of_word(name)

###############################################################################
# 2) SEFIRAH NAMES & GEMATRIA
###############################################################################
# The 10 Sefirot:
#   Keter   - כתר
#   Chokhmah- חכמה
#   Binah   - בינה
#   Chesed  - חסד
#   Gevurah - גבורה
#   Tiferet - תפארת
#   Netzach - נצח
#   Hod     - הוד
#   Yesod   - יסוד
#   Malkhut - מלכות

SEFIROT_INFO = [
    ("Keter",   "כתר"),
    ("Chokhmah","חכמה"),
    ("Binah",   "בינה"),
    ("Chesed",  "חסד"),
    ("Gevurah", "גבורה"),
    ("Tiferet", "תפארת"),
    ("Netzach", "נצח"),
    ("Hod",     "הוד"),
    ("Yesod",   "יסוד"),
    ("Malkhut", "מלכות")
]

def sefirah_gematria(sefirah_hebrew: str) -> int:
    """
    Returns the gematria sum of the Hebrew name of a sefirah.
    Example: 'כתר' => 20 + 400 + 200 = 620
    """
    return gematria_sum_of_word(sefirah_hebrew)

###############################################################################
# 3) CLASSIFY LETTERS: 3 Mothers, 7 Doubles, 12 Simples
###############################################################################
# As per Sefer Yetzirah
MOTHERS = ['א','מ','ש']                # 3
DOUBLES = ['ב','ג','ד','כ','פ','ר','ת'] # 7
# The remaining 12 letters are the Simples.

def classify_letters_sy():
    """
    Return a dict with 'mothers', 'doubles', 'simples'
    from the standard 22 letters.
    """
    all_set = set(STANDARD_22_LETTERS)
    mothers_set = set(MOTHERS)
    doubles_set = set(DOUBLES)
    simple_set = all_set - mothers_set - doubles_set

    return {
        'mothers': sorted(MOTHERS, key=STANDARD_22_LETTERS.index),
        'doubles': sorted(DOUBLES, key=STANDARD_22_LETTERS.index),
        'simples': sorted(list(simple_set), key=STANDARD_22_LETTERS.index)
    }

###############################################################################
# 4) 231 GATES: Pairs of the 22 Letters
###############################################################################
def generate_231_gates(ordered=False):
    """
    Generates the '231 Gates' from the 22 standard letters.
    By default (ordered=False), we get 231 combinations: 22 choose 2 = 231.
    If ordered=True, permutations -> 462 pairs.
    """
    if ordered:
        return list(itertools.permutations(STANDARD_22_LETTERS, 2))
    else:
        return list(itertools.combinations(STANDARD_22_LETTERS, 2))

def gematria_of_gate(gate) -> int:
    """
    Given a gate (a pair of letters), e.g. ('א','ב'),
    returns the sum of their standard gematria values.
    """
    return sum(gematria_value(g) for g in gate)

def gate_name_ratio(gate) -> float:
    """
    Returns a ratio of spelled-out name gematria:
        ratio = gematria(letter1_name) / gematria(letter2_name) if not zero
    Example: gate=('א','ב')
      'אלף' => gem sum
      'בית' => gem sum
      ratio => sum(אלף)/sum(בית)
    """
    sum1 = letter_name_gematria(gate[0])
    sum2 = letter_name_gematria(gate[1])
    return (sum1 / sum2) if sum2 != 0 else 0

###############################################################################
# 5) 72 TRIPLETS (Placeholder) + RATIO EXAMPLES
###############################################################################
PLACEHOLDER_72_TRIPLETS = [
    # Example array (placeholder) referencing 72 Names from Exodus 14:19-21
    "והו", "ילי", "סיט", "עלמ", "מהש", "ללה", "אכא", "ךהת", "הזי", "אלד", "לאו", "ההע",
    "יזל", "םבה", "הרי", "הקם", "לאו", "ךלי", "לוו", "פהל", "נלך", "ייי", "מלה", "חהו",
    "נתה", "האא", "ירת", "שאה", "ריי", "אום", "לךב", "ושר", "יחו", "להח", "ךוק", "מןד",
    "אני", "חעם", "רהע", "ייז", "ההה", "םיכ", "וול", "ילה", "סאל", "ערי", "עשל", "מיה",
    "והו", "דני", "החש", "עמם", "נןא", "ןית", "מבה", "פוי", "נםם", "ייל", "הרח", "םצר",
    "ומב", "יהה", "ענו", "מחי", "דמב", "מןק", "איע", "חבו", "ראה", "יבמ", "היי", "םום"
]

def triplet_gematria(triplet: str) -> int:
    """
    Sum gematria of a 3-letter triplet.
    """
    return gematria_sum_of_word(triplet)

def ratio_triplets(t1: str, t2: str) -> float:
    """
    Compute ratio of gematria sums for two triplets.
    """
    g1 = triplet_gematria(t1)
    g2 = triplet_gematria(t2)
    if g2 == 0:
        return 0.0
    return g1 / g2

###############################################################################
# 6) Adding Suffix to Words for Gematria Shifts
###############################################################################
def add_suffix_gematria(base_word: str, suffix: str) -> int:
    """
    Returns gematria sum of (base_word + suffix).
    Example: add_suffix_gematria("אדם","אל")
             => gematria_sum_of_word("אדםאל")
    """
    combined = base_word + suffix
    return gematria_sum_of_word(combined)

###############################################################################
# 7) EXACT GEOMETRIC CALCULATION: 216 vs 231 in Sefer Yetzirah
###############################################################################
def sefer_yetzirah_geometry():
    """
    Demonstrates the numeric interplay between 216 (6^3) and 231
    from Sefer Yetzirah:

    - 231 => # of 'Gates' formed by combining 22 letters two by two.
    - 216 => 6^3, referencing 'six directions thrice-sealed' or
             a 'cosmic cube' concept in Kabbalistic geometry.

    We show their difference (231 - 216) and ratio (231/216),
    plus a short explanation referencing the 6 directions and
    22 letter combos.
    """
    gates_count = len(generate_231_gates(ordered=False))  # 231
    number_216 = 216

    diff_231_216 = gates_count - number_216  # 15
    ratio_231_216 = gates_count / number_216

    explanation = (
        "\nIn Sefer Yetzirah:\n"
        " - 231 'Gates' are derived from combining the 22 letters two by two.\n"
        " - 216 (6^3) often represents the six directions (up, down, east, west,\n"
        "   north, south) in a triple expansion (or 72 triplets x 3 letters).\n"
        "Sefer Yetzirah alludes to both numbers, linking geometry of letters\n"
        "with the dimensions of space.\n"
        f"Difference: 231 - 216 = {diff_231_216}\n"
        f"Ratio: 231 / 216 = {ratio_231_216:.4f}\n"
    )

    return {
        'number_231': gates_count,
        'number_216': number_216,
        'difference': diff_231_216,
        'ratio': ratio_231_216,
        'explanation': explanation
    }

###############################################################################
# 8) MISSING FUNCTION FROM BEFORE: gates_numeric_analysis()
###############################################################################
def gates_numeric_analysis(gates):
    """
    For each pair (gate), compute:
     - basic_sum: sum of letter gematria (letter1 + letter2),
     - ratio_name_sum: ratio of spelled-out name gematria (letter1_name / letter2_name),
     - diff_name_sum: difference in spelled-out name gematria (letter1_name - letter2_name).

    Returns a list of dictionaries, each describing these metrics
    so you can investigate deeper patterns or numeric relationships.
    """
    results = []
    for gate in gates:
        letter1, letter2 = gate
        basic_sum = gematria_of_gate(gate)
        ratio_nm = gate_name_ratio(gate)
        diff_nm = letter_name_gematria(letter1) - letter_name_gematria(letter2)
        results.append({
            'gate': gate,
            'basic_sum': basic_sum,
            'ratio_name_sum': ratio_nm,
            'diff_name_sum': diff_nm
        })
    return results

###############################################################################
# 9) MAIN DEMO
###############################################################################
def main():
    print("=== GRAND UNIFIED KABBALISTIC SCRIPT DEMO (with 216 vs 231) ===\n")

    #
    # 1) Print letter names + gematria
    #
    print("1) HEBREW LETTERS & THEIR NAME'S GEMATRIA:")
    for lt in STANDARD_22_LETTERS:
        lt_value = gematria_value(lt)
        nm = HEBREW_LETTER_NAMES.get(lt, "")
        nm_g = letter_name_gematria(lt)
        print(f"Letter: {lt} (Value: {lt_value}), Name: {nm}, Name Gematria: {nm_g}")
    print()

    #
    # 2) Print Sefirot + gematria
    #
    print("2) SEFIROT & GEMATRIA:")
    for eng, heb in SEFIROT_INFO:
        sg = sefirah_gematria(heb)
        print(f"{eng} / {heb} => Gematria: {sg}")
    print()

    #
    # 3) 231 Gates: Summaries
    #
    gates = generate_231_gates(ordered=False)
    print("3) 231 GATES STATS:")
    print(f"Total gates (combinations): {len(gates)}\n")

    # Show first 5 gates for brevity
    for i, gate in enumerate(gates[:5], start=1):
        gate_sum = gematria_of_gate(gate)
        name_ratio = gate_name_ratio(gate)
        print(f"{i}. Gate {gate} => Basic Sum: {gate_sum}, Name Ratio: {name_ratio:.2f}")
    print()

    #
    # 4) 'GEOMETRICAL' ANALYSIS FOR GATES (First 5)
    #
    print("4) SAMPLE GATES 'GEOMETRICAL' ANALYSIS (First 5):")
    subset_analysis = gates_numeric_analysis(gates[:5])
    for idx, item in enumerate(subset_analysis, start=1):
        g = item['gate']
        bs = item['basic_sum']
        rn = item['ratio_name_sum']
        df = item['diff_name_sum']
        print(f"{idx}. Gate {g}: basic_sum={bs}, ratio_name_sum={rn:.2f}, diff_name_sum={df}")
    print()

    #
    # 5) 72 Triplets (Placeholder) ratio example
    #
    print("5) 72 TRIPLETS (PLACEHOLDER) RATIO EXAMPLE:")
    if len(PLACEHOLDER_72_TRIPLETS) >= 2:
        t1 = PLACEHOLDER_72_TRIPLETS[0]
        t2 = PLACEHOLDER_72_TRIPLETS[1]
        r = ratio_triplets(t1, t2)
        print(f"Triplets: {t1}, {t2} => Ratio: {r:.2f}")
    else:
        print("Not enough placeholder triplets to compare.")
    print()

    #
    # 6) Adding suffix 'אל' to an example word
    #
    base_word = "אדם"
    suffix = "אל"
    combined_g = add_suffix_gematria(base_word, suffix)
    print("6) ADD SUFFIX 'אל':")
    print(f"Base word: {base_word} => Gematria: {gematria_sum_of_word(base_word)}")
    print(f"Suffix: {suffix} => Gematria: {gematria_sum_of_word(suffix)}")
    print(f"Combined Gematria: {combined_g}")
    print()

    #
    # 7) EXACT GEOMETRIC CALCULATION: 216 vs 231 in Sefer Yetzirah
    #
    print("7) 216 VS 231 IN SEFER YETZIRAH:")
    geo_res = sefer_yetzirah_geometry()
    print(f"231 Gates => {geo_res['number_231']}")
    print(f"216 => {geo_res['number_216']}")
    print(f"Difference => {geo_res['difference']}")
    print(f"Ratio => {geo_res['ratio']:.4f}")
    print(geo_res['explanation'])

    print("=== DEMO COMPLETE ===")
    print("Feel free to expand or adapt this script for specialized analyses.\n")

if __name__ == "__main__":
    main()
