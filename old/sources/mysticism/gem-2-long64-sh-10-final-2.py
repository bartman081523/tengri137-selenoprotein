import json
import numpy as np

# Define Gematria values
gematria_values = {

    # Lateinische Buchstaben
    'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9, 'j': 600,
    'k': 10, 'l': 20, 'm': 30, 'n': 40, 'o': 50, 'p': 60, 'q': 70, 'r': 80, 's': 90,
    't': 100, 'u': 200, 'v': 700, 'w': 900, 'x': 300, 'y': 400, 'z': 500,
    # Grundformen arabischer Buchstaben
    'ا': 1, 'أ': 1, 'إ': 1, 'آ': 1, 'ب': 2, 'ج': 3, 'د': 4, 'ه': 5, 'و': 6, 'ز': 7, 'ح': 8, 'ط': 9,
    'ي': 10, 'ى': 10, 'ك': 20, 'ک': 20, 'ل': 30, 'م': 40, 'ن': 50, 'س': 60, 'ع': 70, 'ف': 80,
    'ص': 90, 'ق': 100, 'ر': 200, 'ش': 300, 'ت': 400, 'ث': 500, 'خ': 600, 'ذ': 700, 'ض': 800, 'ظ': 900, 'غ': 1000,
    # Grund- und Schlussformen hebräischer Buchstaben
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8, 'ט': 9, 'י': 10,
    'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40, 'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80,
    'צ': 90, 'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
    # Arabische Tashkeel (Diacritics) und andere ignorierte Zeichen
    'َ': 0, 'ُ': 0, 'ِ': 0, 'ً': 0, 'ٌ': 0, 'ٍ': 0, 'ْ': 0, 'ّ': 0, ' ': 0, '־': 0, ',': 0, '.': 0, '،': 0, '؛': 0, '-': 0, '_': 0,
    # Griechische Buchstaben
    'α': 1, 'β': 2, 'γ': 3, 'δ': 4, 'ε': 5, 'ϝ': 6, 'ζ': 7, 'η': 8, 'θ': 9, 'ι': 10,
    'κ': 20, 'λ': 30, 'μ': 40, 'ν': 50, 'ξ': 60, 'ο': 70, 'π': 80, 'ϟ': 90, 'ρ': 100,
    'σ': 200, 'τ': 300, 'υ': 400, 'φ': 500, 'χ': 600, 'ψ': 700, 'ω': 800, 'ϡ': 900,

        # Griechische Großbuchstaben
    'Α': 1, 'Β': 2, 'Γ': 3, 'Δ': 4, 'Ε': 5, 'Ϝ': 6, 'Ζ': 7, 'Η': 8, 'Θ': 9, 'Ι': 10,
    'Κ': 20, 'Λ': 30, 'Μ': 40, 'Ν': 50, 'Ξ': 60, 'Ο': 70, 'Π': 80, 'Ϟ': 90, 'Ρ': 100,
    'Σ': 200, 'Τ': 300, 'Υ': 400, 'Φ': 500, 'Χ': 600, 'Ψ': 700, 'Ω': 800, 'Ϡ': 900,

        # Akut
    'ά': 1, 'έ': 5, 'ή': 8, 'ί': 10, 'ό': 70, 'ύ': 400, 'ώ': 800,
    'Ά': 1, 'Έ': 5, 'Ή': 8, 'Ί': 10, 'Ό': 70, 'Ύ': 400, 'Ώ': 800,
    # Gravis
    'ὰ': 1, 'ὲ': 5, 'ὴ': 8, 'ὶ': 10, 'ὸ': 70, 'ὺ': 400, 'ὼ': 800,
    # Zirkumflex
    'ᾶ': 1, 'ῆ': 8, 'ῖ': 10, 'ῦ': 400, 'ῶ': 800,
    # Umlaut und andere Sonderzeichen
    'ϊ': 10, 'ϋ': 400, 'ΐ': 10, 'ΰ': 400,
    'ῒ': 10, 'ῗ': 10, 'ῢ': 400, 'ῧ': 400,
    # Spiritus Asper (rauer Hauchlaut)
    'ἁ': 1, 'ἑ': 5, 'ἡ': 8, 'ἱ': 10, 'ὁ': 70, 'ὑ': 400, 'ὡ': 800,
    'Ἁ': 1, 'Ἑ': 5, 'Ἡ': 8, 'Ἱ': 10, 'Ὁ': 70, 'Ὑ': 400, 'Ὡ': 800,
    # Spiritus Lenis (weicher Hauchlaut)
    'ἀ': 1, 'ἐ': 5, 'ἠ': 8, 'ἰ': 10, 'ὀ': 70, 'ὐ': 400, 'ὠ': 800,
    'Ἀ': 1, 'Ἐ': 5, 'Ἠ': 8, 'Ἰ': 10, 'Ὀ': 70, 'Ὠ': 800,
    'σ': 200,  # Normal Sigma
    'ς': 200,  # Sigma am Wortende
    'á': 1, 'é': 5, 'í': 9, 'ó': 50, 'ú': 200, 'ý': 400,
    'Á': 1, 'É': 5, 'Í': 9, 'Ó': 50, 'Ú': 200, 'Ý': 400,
    'ē': 5,
    }

versos_genesis_sefardi = [

    ["והו ילי סיט עלמ מהש ללה אכא ךהת הזי אלד לאו ההע יזל םבה הרי הקם לאו ךלי לוו פהל נלך ייי מלה חהו נתה האא ירת שאה ריי אום לךב ושר יחו להח ךוק מןד אני חעם רהע ייז ההה םיכ וול ילה סאל ערי עשל מיה והו דני החש עמם נןא ןית מבה פוי נםם ייל הרח םצר ומב יהה ענו מחי דמב מןק איע חבו ראה יבמ היי םום"],

["והו ילי 'סיט עלמ מהש ללה אכא ךהת הזי אלד לאו ההע יזל םבה הרי הקם לאו ךלי לוו פהל נלך ייי מלה חהו"],
["נתה האא ירת שאה ריי אום לךב ושר יחו להח ךוק מןד אני חעם רהע ייז ההה םיכ וול ילה סאל ערי עשל מיה"],
["והו דני החש עמם נןא ןית מבה פוי נםם ייל הרח םצר ומב יהה ענו מחי דמב מןק איע חבו ראה יבמ היי םום"],

["והו ילי סיט עלמ מהש ללה אכא"],
["ךהת הזי אלד לאו ההע יזל םבה"],
["הרי הקם לאו ךלי לוו פהל נלך"],
["ייי מלה חהו נתה האא ירת שאה"],
["ריי אום לךב ושר יחו להח ךוק"],
["מןד אני חעם רהע ייז ההה םיכ"],
["וול ילה סאל ערי עשל מיה והו"],
["דני החש עמם נןא ןית מבה פוי"],
["נםם ייל הרח םצר ומב יהה ענו"],
["מחי דמב מןק איע חבו ראה יבמ"],
["היי םום"],


]

# Functions for conversions
def text_to_gematria(text):
    return [gematria_values.get(letter, 0) for letter in text if gematria_values.get(letter, 0) != 0]

def gematria_to_text(gematria):
    return "".join(letter for value in gematria for letter, val in gematria_values.items() if val == value)

# Functions for mathematical operations
def calculate_sum_and_product(gematria):
    sum_ = sum(gematria)
    # Use np.prod with dtype=np.float64 to handle large numbers
    product = np.prod(np.array(gematria, dtype=np.float64))
    return sum_, product

def calculate_inverses(sum_, product):
    inverse_sum = 1 / sum_ if sum_ != 0 else 'infinity'
    inverse_product = 1 / product if product != 0 else 'infinity'
    return inverse_sum, inverse_product

# Main logic
results = []

for chapter in versos_genesis_sefardi:
    for verse in chapter:
        gematria = text_to_gematria(verse.replace(" ", ""))
        if gematria:  # Ensure the list is not empty
            sum_, product = calculate_sum_and_product(gematria)
            inverse_sum, inverse_product = calculate_inverses(sum_, product)
            verse_wo_spaces = verse.replace(" ", "")
            print(f"Verse: {verse}\nVerse letters: {len(verse_wo_spaces)}\nGematria:{gematria}\nGematria Items:{len(gematria)}\nSum: {sum_}\nProduct: {product}\nInverse of Sum: {inverse_sum}\nInverse of Product: {inverse_product}\n")
            results.append(gematria)
