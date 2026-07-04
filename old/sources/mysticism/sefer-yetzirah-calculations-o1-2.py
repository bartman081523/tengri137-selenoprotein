#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Grand Unified Kabbalistic Script
================================

Purpose:
--------
This Python script merges multiple Kabbalistic constructs:
1) 22 Hebrew letters (standard forms) with:
   - Original Hebrew names (e.g. Aleph -> "אלף")
   - Gematria sums of each letter's name

2) Sefirot with Hebrew names (e.g. Keter -> כתר) + Gematria sums.

3) Generation of 231 Gates (pairs of letters) with:
   - Combined gematria sums of each pair
   - Basic "geometrical" manipulations (ratios, differences, etc.)

4) A placeholder mechanism for 72 Triplets, referencing the "72 Names of G-d."
   - Each triplet is assigned a gematria sum.
   - Potential expansions for ratio or difference calculations.

5) A function to "append 'אל'/'אלף'/'על'/etc." suffixes to words,
   to see how gematria changes ("al/el" suffix concept from some
   Kabbalah secret circles references).

6) A small cameo for "cryptocalypse2," "Raziel," and other potential expansions.

Disclaimers and Known Placeholders:
-----------------------------------
- The approach is playful and experimental. True Kabbalistic depth can't be
  fully captured in a single script.
- The "72 Triplets" are often enumerated from Exodus 14:19-21 (three verses,
  72 letters each). We do a placeholder array here for demonstration only.
- "Geometric calculations" can mean many things; we interpret them here
  as numeric manipulations on pairs/triplets (ratios, differences).
- This script is not an authoritative commentary on Raziel or any advanced
  Kabbalah text. It's a creative sandbox.

Enjoy exploring, expanding, or hacking it for deeper secrets. cryptocalypse2
might be a code name for your own expansions or a next-level puzzle.
"""

import itertools

###############################################################################
# 1) HEBREW LETTERS: Original Names, Gematria Table, Basic Info
###############################################################################

# Provided Gematria Table (including final letters).
# We'll treat final letters (ך ם ן ף ץ) as separate for summation
# but NOT as part of the main 22 standard letters in Sefer Yetzirah classification.

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

# Original Hebrew spelled-out names for these letters:
# (Popular tradition might differ in exact spellings.)
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
    'נ': 'نون',   # NUN (some write נון)
    'ס': 'סמך',   # SAMEKH
    'ע': 'עין',   # AYIN
    'פ': 'פה',    # PE
    'צ': 'צדי',   # TSADI (various spellings)
    'ק': 'קוף',   # QOF
    'ר': 'ריש',   # RESH
    'ש': 'שין',   # SHIN
    'ת': 'תיו',   # TAV
}

def gematria_value(letter: str) -> int:
    """
    Returns the gematria value of a single letter (including finals).
    If the letter is not found, returns 0.
    """
    return GEMATRIA_TABLE.get(letter, 0)

def gematria_sum_of_word(word: str) -> int:
    """
    Returns the sum of gematria values for each character in 'word'.
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
# The 10 Sefirot (Keter, Chokhmah, Binah, Chesed, Gevurah, Tiferet, Netzach, Hod, Yesod, Malkhut)

SEFIROT_INFO = [
    ("Keter", "כתר"),
    ("Chokhmah", "חכמה"),
    ("Binah", "בינה"),
    ("Chesed", "חסד"),
    ("Gevurah", "גבורה"),
    ("Tiferet", "תפארת"),
    ("Netzach", "נצח"),
    ("Hod", "הוד"),
    ("Yesod", "יסוד"),
    ("Malkhut", "מלכות")
]

def sefirah_gematria(sefirah_hebrew: str) -> int:
    """
    Returns the gematria sum of the Hebrew name of the sefirah.
    Example: 'כתר' -> 20 + 400 + 200 = 620
    """
    return gematria_sum_of_word(sefirah_hebrew)

###############################################################################
# 3) CLASSIFY LETTERS: 3 Mothers, 7 Doubles, 12 Simples
###############################################################################
# As in Sefer Yetzirah
MOTHERS = ['א','מ','ש']
DOUBLES = ['ב','ג','ד','כ','פ','ר','ת']  # 7
# The remaining 12 will be the Simples
def classify_letters_sy():
    """
    Return dict with 'mothers', 'doubles', 'simples' from the standard 22 letters.
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
    Given a gate (a pair of letters), e.g. ('א','ב'), compute
    the SUM of their gematria values OR spelled-out name gematria.
    There's more than one approach. We'll do basic letter-sum here.
    """
    # Approach 1: sum of the letter's direct gematria
    # e.g. ('א','ב') -> 1 + 2 = 3
    return sum(gematria_value(g) for g in gate)

def gate_name_ratio(gate) -> float:
    """
    A 'geometrical' or numeric ratio approach, for demonstration:
    We'll sum gematria of spelled-out names for each letter,
    then do a ratio letter1_name_sum / letter2_name_sum if letter2 != 0.
    If second is zero, return 0.
    """
    # For example, if gate = ('א','ב'):
    # 'א' => spelled-out name = 'אלף' => gem sum
    # 'ב' => spelled-out name = 'בית' => gem sum
    # ratio => gem_sum(אלף) / gem_sum(בית)
    sum1 = letter_name_gematria(gate[0])
    sum2 = letter_name_gematria(gate[1])
    if sum2 == 0:
        return 0
    return sum1 / sum2

###############################################################################
# 5) 72 TRIPLETS (Placeholder) + RATIO EXAMPLES
###############################################################################
# The "72 Triplets" are typically derived from Exodus 14:19-21 in Kabbalah.
# We won't parse the biblical text here, but create a placeholder list for demonstration.

PLACEHOLDER_72_TRIPLETS = [
"והו", "ילי", "סיט", "עלמ", "מהש", "ללה", "אכא", "ךהת", "הזי", "אלד", "לאו", "ההע", "יזל", "םבה", "הרי", "הקם", "לאו", "ךלי", "לוו", "פהל", "נלך", "ייי", "מלה", "חהו", "נתה", "האא", "ירת", "שאה", "ריי", "אום", "לךב", "ושר", "יחו", "להח", "ךוק", "מןד", "אני", "חעם", "רהע", "ייז", "ההה", "םיכ", "וול", "ילה", "סאל", "ערי", "עשל", "מיה", "והו", "דני", "החש", "עמם", "נןא", "ןית", "מבה", "פוי", "נםם", "ייל", "הרח", "םצר", "ומב", "יהה", "ענו", "מחי", "דמב", "מןק", "איע", "חבו", "ראה", "יבמ", "היי", "םום"
]
# A real system might parse the actual verse sets. For now, we do a short placeholder.

def triplet_gematria(triplet: str) -> int:
    """
    Sum gematria of a 3-letter name (placeholder approach).
    """
    return gematria_sum_of_word(triplet)

def ratio_triplets(t1: str, t2: str) -> float:
    """
    Example ratio among triplets' gematria sums.
    """
    g1 = triplet_gematria(t1)
    g2 = triplet_gematria(t2)
    if g2 == 0:
        return 0
    return g1 / g2

###############################################################################
# 6) Adding "al"/"el" Suffix to Words for Gematria Shifts
###############################################################################
# One concept in certain Kabbalistic texts is adding suffixes like "אל" or "על"
# to transform or expand a word's gematria. We'll do a small function:

def add_suffix_gematria(base_word: str, suffix: str) -> int:
    """
    Returns the gematria sum of base_word + suffix.
    Example: add_suffix_gematria("גיל","אל") -> sum of ג+י+ל + א+ל
    """
    combined = base_word + suffix  # purely string concatenation
    return gematria_sum_of_word(combined)

###############################################################################
# 7) Example "Geometrical" Calculations with 231 Gates
###############################################################################
# We interpret "geometrical" loosely as numeric manipulations: sums, differences, ratios.

def gates_numeric_analysis(gates):
    """
    For each pair (gate), compute:
     - basic sum of letter gematria,
     - ratio of spelled-out name gematria,
     - difference of spelled-out name gematria.
    Returns a list of dicts so you can further investigate patterns.
    """
    results = []
    for gate in gates:
        letter1, letter2 = gate
        basic_sum = gematria_of_gate(gate)
        ratio_nm = gate_name_ratio(gate)
        # difference in spelled-out name sums
        diff_nm = letter_name_gematria(letter1) - letter_name_gematria(letter2)
        results.append({
            'gate': gate,
            'basic_sum': basic_sum,
            'ratio_name_sum': ratio_nm,
            'diff_name_sum': diff_nm
        })
    return results

###############################################################################
# 8) MAIN DEMO
###############################################################################

def main():
    print("=== GRAND UNIFIED KABBALISTIC SCRIPT DEMO ===\n")

    # 1) Print letter names + gematria
    print("1) HEBREW LETTERS & THEIR NAME'S GEMATRIA:")
    for lt in STANDARD_22_LETTERS:
        nm = HEBREW_LETTER_NAMES.get(lt,"")
        nm_g = letter_name_gematria(lt)
        lt_value = gematria_value(lt)
        print(f"Letter: {lt} (Value: {lt_value}), Name: {nm}, Name Gematria: {nm_g}")
    print()

    # 2) Print Sefirot + gematria
    print("2) SEFIROT & GEMATRIA:")
    for eng, heb in SEFIROT_INFO:
        sg = sefirah_gematria(heb)
        print(f"{eng} / {heb} => Gematria: {sg}")
    print()

    # 3) 231 Gates: Summaries
    gates = generate_231_gates(ordered=False)
    print("3) 231 GATES STATS:")
    print(f"Total gates (combinations): {len(gates)}\n")
    # Let's just show the gematria sum for the first 10 gates, plus a ratio or two:
    for i, gate in enumerate(gates[:231], start=1):
        gate_sum = gematria_of_gate(gate)
        name_ratio = gate_name_ratio(gate)
        print(f"{i}. Gate {gate} => Basic Gematria Sum: {gate_sum}, Ratio of Names: {name_ratio:.2f}")
    print()

    # 4) "Geometrical" analysis on gates
    print("4) SIMPLE GATES 'GEOMETRICAL' ANALYSIS (First 5):")
    analysis = gates_numeric_analysis(gates[:231])
    for item in analysis:
        g = item['gate']
        bs = item['basic_sum']
        rn = item['ratio_name_sum']
        df = item['diff_name_sum']
        print(f"Gate {g}: basic_sum={bs}, ratio_name_sum={rn:.2f}, diff_name_sum={df}")
    print()

    # 5) 72 Triplets (Placeholder) ratio example
    print("5) 72 TRIPLETS (PLACEHOLDER) RATIO EXAMPLE:")
    if len(PLACEHOLDER_72_TRIPLETS) >= 2:
        t1 = PLACEHOLDER_72_TRIPLETS[0]
        t2 = PLACEHOLDER_72_TRIPLETS[1]
        r = ratio_triplets(t1, t2)
        print(f"Triplets: {t1}, {t2} => Ratio: {r:.2f}")
    else:
        print("Not enough placeholder triplets to compare.")
    print()

    # 6) Adding suffix 'אל' to an example word
    base_word = "אדם"
    suffix = "אל"
    combined_g = add_suffix_gematria(base_word, suffix)
    print("6) ADD SUFFIX 'אל':")
    print(f"Base word: {base_word} => Gematria: {gematria_sum_of_word(base_word)}")
    print(f"Suffix: {suffix} => Gematria: {gematria_sum_of_word(suffix)}")
    print(f"Combined Gematria: {combined_g}")

    print("=== DEMO COMPLETE ===")
    print("Feel free to expand or adapt any part of this script for deeper or specialized analyses.")

if __name__ == "__main__":
    main()
