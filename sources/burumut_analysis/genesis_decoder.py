"""
GENESIS-DECODER fuer BURUMUT

Hypothese: BURUMUT ist ein Poly-Alphabet-Chiffre mit Genesis-basiertem
Schluessel. Wir testen systematisch alle Schluessel-Laengen 1-30 mit
verschiedenen Genesis-Wort-Gematrien.

Wenn BURUMUT ein verschluesselter Text ist (Klartext-Alphabet A=1, ..., Z=26),
dann sollte ein Vigenere-Decoder Buchstaben mit normaler englischer oder
hebraeischer Haeufigkeitsverteilung liefern.
"""
import math
from collections import Counter
import itertools

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

HEBREW_GEMATRIA = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
    'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90,
    'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

# Genesis 1:1 Gematria-Summe = 2701 = 37 x 73
# Genesis 1:9 = 1701 = 37 x 46
# Wir versuchen Vigenere-Decoder mit verschiedenen Schluesseln:
# Schluessel-Werte aus:
#  - Wort-Gematrien aus Genesis 1:1-10
#  - Numerische Ableitungen (37, 46, 73, 137, 232, 2701, 1701, 1369, 913)
#  - Buchstaben-Werte direkt

def chi_squared_english(text):
    """Berechne chi-squared vs. englische Buchstaben-Verteilung."""
    if not text: return float('inf')
    freq = Counter(text)
    n = len(text)
    expected_pct = {
        'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 'N': 6.7,
        'S': 6.3, 'H': 6.1, 'R': 6.0, 'D': 4.3, 'L': 4.0, 'C': 2.8,
        'U': 2.8, 'M': 2.4, 'W': 2.4, 'F': 2.2, 'G': 2.0, 'Y': 2.0,
        'P': 1.9, 'B': 1.5, 'V': 1.0, 'K': 0.8, 'J': 0.15, 'X': 0.15,
        'Q': 0.10, 'Z': 0.07,
    }
    chi = 0
    for ch in expected_pct:
        observed = freq[ch] / n if ch in freq else 0
        expected = expected_pct[ch] / 100
        chi += (observed - expected) ** 2 / expected
    return chi * n  # normalised chi-squared


def viginere_decrypt(cipher, key):
    """Klassische Vigenere-Entschluesselung."""
    result = []
    for i, c in enumerate(cipher):
        k = key[i % len(key)]
        # Konvertiere zu Zahl
        c_num = ord(c) - ord('A')
        if isinstance(k, str):
            k_num = ord(k) - ord('A')
        else:
            k_num = k
        d_num = (c_num - k_num) % 26
        result.append(chr(d_num + ord('A')))
    return ''.join(result)


# Baseline: Was bekommt man fuer zufaellige Schluessel?
print("="*70)
print("BASELINE: BURUMUT als unverarbeitetes Rauschen")
print("="*70)
baseline_chi = chi_squared_english(BURUMUT_FULL)
print(f"BURUMUT chi-squared vs. englisch: {baseline_chi:.2f}")
print(f"BURUMUT Buchstaben-Verteilung: {dict(Counter(BURUMUT_FULL).most_common(10))}")
print()

print("="*70)
print("PHASE A: VIGENERE-DECODER mit Genesis-Schluesseln")
print("="*70)

genesis_keys = {
    '37 (Frequenz)': 37 % 26,
    '46 (Genesis 1:9)': 46 % 26,
    '73 (Genesis 1:1)': 73 % 26,
    '137 (Feinstruktur)': 137 % 26,
    '232 (UV-C)': 232 % 26,
    '913 (Bereshit)': 913 % 26,
    '46 direkt': 20,
    '37 direkt': 11,
    '37 mod 26 + 1 (A=1)': 12,
}

for name, key in genesis_keys.items():
    decrypted = viginere_decrypt(BURUMUT_FULL, [key])
    chi = chi_squared_english(decrypted)
    print(f"Schluessel {name:30s}: {decrypted[:40]}... (chi={chi:.2f})")

print()
print("="*70)
print("PHASE B: POLY-VIGENERE mit kurzen Schluesseln (Laenge 4-7)")
print("="*70)
# Versuche systematisch Schluessel-Laengen
# Ein 'guter' Schluessel wuerde die chi-squared minimieren

def best_key_for_length(text, key_len, alphabet_size=26):
    """Finde den wahrscheinlichsten Schluessel einer gegebenen Laenge
    via Frequency-Analyse jeder Spalte (Kasiski-Examination)."""
    columns = [[] for _ in range(key_len)]
    for i, c in enumerate(text):
        c_num = ord(c) - ord('A')
        columns[i % key_len].append(c_num)
    # Bestimme den wahrscheinlichsten Shift fuer jede Spalte
    key = []
    for col in columns:
        # Finde best shift s.t. decrypted col has highest match with English freq
        best_shift = 0
        best_score = -1e18
        for shift in range(alphabet_size):
            score = 0
            for c_num in col:
                d_num = (c_num - shift) % alphabet_size
                ch = chr(d_num + ord('A'))
                # English frequency weight
                freq_weight = {'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0,
                              'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0}.get(ch, 1.0)
                score += freq_weight
            if score > best_score:
                best_score = score
                best_shift = shift
        key.append(best_shift)
    return key

print("Kasiski-Examination: beste Schluessel-Laenge nach Chi-Quadrat:")
for key_len in range(2, 16):
    best_key = best_key_for_length(BURUMUT_FULL, key_len)
    decrypted = viginere_decrypt(BURUMUT_FULL, best_key)
    chi = chi_squared_english(decrypted)
    print(f"  key_len={key_len:2d}: chi={chi:.2f}, key={best_key}, text={decrypted[:30]}...")

print()
print("="*70)
print("PHASE C: BURUMUT SELBSTREP — ist es ein PALINDROM?")
print("="*70)
# BURUMUTREFAMTU... rückwärts lesen?
reverse_burumut = BURUMUT_FULL[::-1]
print(f"BURUMUT:        {BURUMUT_FULL[:60]}...")
print(f"BURUMUT reverse: {reverse_burumut[:60]}...")

# Inverse Buchstaben (A↔Z, B↔Y, ...)
def atbash(s):
    return ''.join(chr(ord('Z') - (ord(c) - ord('A'))) for c in s)

print(f"Atbash:         {atbash(BURUMUT_FULL)[:60]}...")

# Was, wenn BURUMUT ein ROT-13 ist?
print(f"ROT-13:         {viginere_decrypt(BURUMUT_FULL, [13])[:60]}...")

print()
print("="*70)
print("PHASE D: BURUMUT UND DIE STRUKTUR-VORHERSAGE")
print("="*70)
# Wir wissen: R_28 = 1111111111111111111111111111 = Tengri-Faktor 1
# BURUMUT enthaelt 99 Zeichen. 99 = 9 x 11, also 9 * 11
# Aber R_28 hat 28 Ziffern. Verbindung?

# Wenn wir BURUMUT als SUMME der Zahlen 1..26 interpretieren, kommt 1232 raus
# 1232 / 28 = 44 - das ist die Tengri-Zahl!

nums = [ord(c) - ord('A') + 1 for c in BURUMUT_FULL]
total = sum(nums)
print(f"BURUMUT-Summe: {total}")
print(f"  / 28 = {total / 28}")
print(f"  / 99 = {total / 99}")
print(f"  Rest mod 28: {total % 28}")
print(f"  Rest mod 99: {total % 99}")
print(f"  Rest mod 137: {total % 137}")
print(f"  Rest mod 46: {total % 46}")
print()

# Was wenn BURUMUT aus 11 Genesen-Strophen (jeweils 9 Zeichen = 99 / 11) besteht?
# Wenn ja, ist die 11-Verteilung signifikant
verse_lens = []
i = 0
while i < len(BURUMUT_FULL):
    # Suche naechste UAZBE-Position
    next_uazbe = BURUMUT_FULL.find('UAZBE', i)
    if next_uazbe == -1:
        verse_lens.append(len(BURUMUT_FULL) - i)
        break
    verse_lens.append(next_uazbe - i)
    i = next_uazbe + 5
print(f"BURUMUT-Subsequenz-Laengen (zwischen UAZBE): {verse_lens}")
print(f"  Summe: {sum(verse_lens)}")
print(f"  Mittelwert: {sum(verse_lens) / len(verse_lens):.2f}")
print()

print("="*70)
print("GENESIS-DECODER BEENDET")
print("="*70)