import unicodedata

def strip_diacritics(text):
    """
    Entfernt Diakritika von Unicode-Zeichen, um den Basisbuchstaben zu erhalten.
    """
    return ''.join(char for char in unicodedata.normalize('NFD', text)
                   if unicodedata.category(char) != 'Mn')

def hebrew_letter_to_value(letter):
    """
    Konvertiert einen einzelnen Buchstaben in seinen Gematria-Wert, ignoriert Leerzeichen
    und Nicht-Buchstaben-Zeichen.
    """
    # Dein vorhandenes Wörterbuch bleibt unverändert
    values = {
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
    'כ': 20, 'ך': 500, 'ל': 30, 'מ': 40, 'ם': 600, 'נ': 50, 'ן': 700, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 800,
    'צ': 90, 'ץ': 900, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,

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

    # Stelle sicher, dass Diakritika entfernt werden, bevor auf das Wörterbuch zugegriffen wird
    letter_no_diacritics = strip_diacritics(letter)

    if letter_no_diacritics in values:
        return values[letter_no_diacritics.lower()]
    elif letter.strip() == "":  # Ignoriere Leerzeichen und leere Zeilen
        return 0
    else:
        # Anstatt einen Fehler zu werfen, gib 0 zurück für Zeichen, die nicht im Wörterbuch gefunden werden
        # Dies verhindert das Programmabbruch bei unbekannten Zeichen
        # Optional: Protokolliere unbekannte Zeichen für die Überprüfung
        print(f"Warnung: Unbekanntes Zeichen '{letter}' ignoriert.")
        return 0


def calculate_gematria(text):
    """Calculate the Gematria value of a given Hebrew text, ignoring spaces and non-Hebrew characters."""
    return sum(hebrew_letter_to_value(letter) for letter in text if letter.strip() != "")

def main():
    print("Geben Sie hebräischen, arabischen oder englischen Text ein (tippen Sie 'END' auf einer neuen Zeile, um zu beenden):")

    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)

    hebrew_text = ''.join(lines)
    try:
        gematria_value = calculate_gematria(hebrew_text)
        print(f"Der Gematria-Wert des eingegebenen Textes ist: {gematria_value}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    main()
