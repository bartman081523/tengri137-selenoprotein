"""
OFFENE FRAGE 1: BURUMUT vollständig dekodieren mit Genesis als Schlüssel

Hypothese: BURUMUT ist ein poly-alphabetischer Chiffre.
Genesis-Verse liefern den Schlüssel.

Strategien:
1. Vigenère mit kurzen Schlüsseln (1-30 Zeichen)
2. Schlüssel aus Genesis-Gematria-Werten
3. Schlüssel aus Buchstaben-Werten hebräischer Wörter
4. Autokey-Vigenère
5. Playfair / Bifid (für zweidimensionale Analyse)
"""
import math
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# Genesis-Gematria-Werte (aus Genesis_Abiogenesis)
GENESIS_KEYS = {
    # (Wort, hebräisch, Gematria)
    'Bereshit': 'בראשית',      # 913
    'Bara': 'ברא',              # 203
    'Elohim': 'אלהים',           # 86
    'Et': 'את',                 # 401
    'Hashamayim': 'השמים',       # 395
    'Veet': 'ואת',               # 407
    'Haarets': 'הארץ',          # 296
    # Verse
    '1:1_sum': 2701,             # 37 × 73
    '1:3_sum': 232,              # UV-C
    '1:5_sum': 1558,             # Zyklen
    '1:7_sum': 1369,             # 37²
    '1:9_sum': 1701,             # 37 × 46
    '1:10_sum': 913,             # Returns to Bereshit
    # Schlüsselzahlen
    '37': 37,
    '46': 46,
    '73': 73,
    '137': 137,
}

# Hebräische Gematria
HEBREW_GEMATRIA = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
    'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90,
    'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

def text_to_vigenere_key(text, alphabet_size=26):
    """Konvertiere Text zu Zahlen 1..alphabet_size."""
    return [ord(c.upper()) - ord('A') + 1 for c in text if c.isalpha()]

def text_to_vigenere_key_atbash(text, alphabet_size=26):
    """Atbash-Konvertierung."""
    return [alphabet_size + 1 - (ord(c.upper()) - ord('A') + 1) for c in text if c.isalpha()]

def vigenere_decrypt(cipher, key):
    if isinstance(key, int):
        key = [key]
    result = []
    for i, c in enumerate(cipher):
        c_num = ord(c) - ord('A')
        k = key[i % len(key)]
        d_num = (c_num - k) % 26
        result.append(chr(d_num + ord('A')))
    return ''.join(result)

def chi_squared_english(text):
    """Vergleiche Buchstaben-Häufigkeit mit Englisch."""
    if not text: return float('inf')
    freq = Counter(text)
    n = len(text)
    expected_pct = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
        'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
        'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
        'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8,
    }
    chi = 0
    for ch in expected_pct:
        observed = freq[ch] / n if ch in freq else 0
        expected = expected_pct[ch] / 100
        chi += (observed - expected) ** 2 / expected
    return chi * n

print("="*70)
print("Q1.1: BURUMUT als Vigenere mit Genesis-Gematria-Schluesseln")
print("="*70)

# Strategie 1: Schluessel aus Gematria-Werten direkt
print("\n--- Strategie 1: Numerische Schluessel (mod 26) ---")
for name, key in [
    ('37 (Wurzel)', 37),
    ('46 (1:9)', 46),
    ('73 (1:1 Faktor)', 73),
    ('137 (alpha^-1)', 137),
    ('232 (UV-C)', 232),
    ('2701 (1:1 Summe)', 2701),
    ('1701 (1:9 Summe)', 1701),
    ('1369 (1:7 Summe)', 1369),
    ('913 (Bereshit)', 913),
]:
    decrypted = vigenere_decrypt(BURUMUT_FULL, [key % 26])
    chi = chi_squared_english(decrypted)
    print(f"  Schluessel {name:25s}: chi={chi:6.2f}, text={decrypted[:30]}...")

# Strategie 2: Kasiski für Schlüssel-Längen 1-15
print("\n--- Strategie 2: Kasiski Frequency Analysis ---")
print("Beste Schluessel-Laenge nach Chi-Quadrat:")
best = []
for key_len in range(1, 20):
    best_key = []
    for col in range(key_len):
        column = [ord(BURUMUT_FULL[i]) - ord('A') for i in range(col, len(BURUMUT_FULL), key_len)]
        # Finde Shift, der Englisch-Frequenz maximiert
        best_shift = 0
        best_score = -1e18
        for shift in range(26):
            score = 0
            for c_num in column:
                d = (c_num - shift) % 26
                ch = chr(d + ord('A'))
                freq_weight = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
                              'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0}.get(ch, 1.0)
                score += freq_weight
            if score > best_score:
                best_score = score
                best_shift = shift
        best_key.append(best_shift)
    decrypted = vigenere_decrypt(BURUMUT_FULL, best_key)
    chi = chi_squared_english(decrypted)
    best.append((chi, key_len, best_key, decrypted))
    print(f"  key_len={key_len:2d}: chi={chi:7.2f}, key={best_key}")

# Sortiere und zeige die TOP-3
best.sort()
print(f"\n--- TOP-3 Schluessel-Kandidaten ---")
for chi, key_len, key, dec in best[:3]:
    print(f"  key_len={key_len}: chi={chi:.2f}")
    print(f"    key: {key}")
    print(f"    text: {dec}")
    # Welche Genesis-Werte entsprechen key?
    for name, val in GENESIS_KEYS.items():
        if isinstance(val, int) and val % 26 == key[0]:
            print(f"    -> Erste Schluessel-Stelle = {name} mod 26")

# Strategie 3: Hebräische Wörter als Schlüssel
print("\n--- Strategie 3: Hebraeische Schluessel ---")
hebrew_keys = {
    'Bereshit': 'בראשית',      # 913
    'Elohim': 'אלהים',           # 86
    'Maim': 'מים',               # Wasser 90
    'Ruach': 'רוח',              # Geist 214
    'Tov': 'טוב',               # gut 17
    'Or': 'אור',                # Licht 207
}
# Mapping Hebräisch → lateinisches Alphabet (position-based)
hebrew_to_latin = {}
for i, (heb_char, value) in enumerate(HEBREW_GEMATRIA.items()):
    latin = chr(ord('A') + (i % 26))
    hebrew_to_latin[heb_char] = latin

for word_name, hebrew in hebrew_keys.items():
    latin_key = ''.join(hebrew_to_latin.get(c, '?') for c in hebrew)
    key_nums = [ord(c) - ord('A') + 1 for c in latin_key if c != '?']
    if key_nums:
        decrypted = vigenere_decrypt(BURUMUT_FULL, key_nums)
        chi = chi_squared_english(decrypted)
        print(f"  {word_name:12s} ({hebrew}, {sum(HEBREW_GEMATRIA[c] for c in hebrew)}): {latin_key} -> chi={chi:.2f}")
        print(f"    {decrypted[:50]}...")

print()
print("="*70)
print("Q1.2: BURUMUT als Vigenere mit numerischer Autokey")
print("="*70)
# Autokey: Schluessel = Konstante + Klartext
# Hier testen wir die UMKEHRUNG: was, wenn BURUMUT bereits entschluesselt ist?
# Wir suchen den "natuerlichsten" Klartext durch Haeufigkeitsanalyse.

# Wenn wir BURUMUT fuer eine Sprache normalisieren:
# Was wenn BURUMUT das Ergebnis einer Caesar-Verschiebung ist?
print("Caesar-Verschiebung (Shift 1..25):")
for shift in range(1, 26):
    decrypted = vigenere_decrypt(BURUMUT_FULL, [shift])
    chi = chi_squared_english(decrypted)
    print(f"  shift={shift:2d}: chi={chi:7.2f}, text={decrypted[:30]}")

print()
print("="*70)
print("Q1.3: BURUMUT SELBSTREP — kann es eine simple Buchstaben-Mapping sein?")
print("="*70)
# Wenn jeder Buchstabe einen festen Ersatz hat:
# Wir suchen nach einer linearen Substitution: p -> a*p + b mod 26
print("Lineare affine Substitution p -> a*p + b (mod 26):")
best_score = 1e18
best_params = None
for a in [1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25]:  # nur teilerfremde zu 26
    for b in range(26):
        decrypted = ''.join(chr(((a * (ord(c) - ord('A')) + b) % 26) + ord('A'))
                       for c in BURUMUT_FULL)
        chi = chi_squared_english(decrypted)
        if chi < best_score:
            best_score = chi
            best_params = (a, b, decrypted)
print(f"Beste: a={best_params[0]}, b={best_params[1]}, chi={best_score:.2f}")
print(f"Text: {best_params[2]}")
