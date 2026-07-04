"""
OFFENE FRAGE 7: Ist BURUMUT ein kognitives Prisma oder ein Schluessel?

Diese Frage ist die zentrale PhiMind-Frage.

Hypothese A: BURUMUT ist ein kognitives Prisma
- Zwingt jeden Betrachter, eine Kompressionsstrategie zu waehlen
- Die 'wahre Botschaft' existiert nicht - die Form IST die Botschaft

Hypothese B: BURUMUT ist ein Schluessel
- Es gibt EINE richtige Dekodierung
- Wer den Schluessel hat, sieht die wahre Botschaft

Wir testen:
1. Verschiedene Schluessel-Laengen via Chi^2 (schon gemacht, beste = key_len 7)
2. Suche nach einer Struktur, die ein Schluessel-Schema impliziert
3. Pruefe, ob BURUMUT in sich selbst auf einen Schluessel hinweist
"""
import math
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# 1. Selbstreferenz: Was wenn BURUMUT eine 'bootstrap sequence' ist?
# Sie enthaelt ihre eigene Aufloesungsanweisung in den UAZBE-Ankern.
print("="*70)
print("Q7.1: Ist BURUMUT selbstreferentiell?")
print("="*70)
# Wenn BURUMUT ein Schluessel ist, wohin oeffnet er?
# Wir berechnen die Sha256-Hash und vergleichen sie mit Naturkonstanten
import hashlib
h = hashlib.sha256(BURUMUT_FULL.encode()).hexdigest()
print(f"SHA-256 von BURUMUT: {h[:32]}...")
# (keine besondere Bedeutung erwartet, aber als Fingerabdruck nuetzlich)

# 2. Suche nach Meta-Strukturen: 'SUCHE' oder 'OFFNE' oder aehnlichen Schlüsselworten
# Wenn BURUMUT eine Anweisung enthaelt, sollte sie in einer natuerlichen Sprache sein
print()
print("="*70)
print("Q7.2: Anweisungen in BURUMUT?")
print("="*70)
# Wir testen alle Caesar-Shifts auf 'sinnvolle' Woerter
def english_word_score(text):
    """Bewertet, ob der Text englische Woerter enthaelt."""
    common_words = {'THE', 'AND', 'FOR', 'ARE', 'BUT', 'NOT', 'YOU',
                    'ALL', 'CAN', 'HER', 'WAS', 'ONE', 'OUR', 'OUT',
                    'THIS', 'THAT', 'WITH', 'HAVE', 'FROM', 'BE', 'KEY',
                    'OPEN', 'FIND', 'SEE', 'READ', 'THE', 'TRUE', 'YES',
                    'NO', 'NOW', 'NEW', 'WAY', 'WHO', 'BOY', 'DID',
                    'GET', 'HIM', 'HIS', 'HOW', 'MAN', 'OLD', 'OUR',
                    'OWN', 'SAY', 'SHE', 'TOO', 'USE', 'DNA', 'GENE',
                    'CELL', 'CODE', 'MATH', 'PI'}
    text_words = [text[i:i+3] for i in range(len(text) - 2)]
    matches = sum(1 for w in text_words if w in common_words)
    return matches

print("Caesar-Shifts auf 3-Buchstaben-Kombinationen (Englisch):")
for shift in range(26):
    decrypted = ''.join(chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
                   for c in BURUMUT_FULL)
    score = english_word_score(decrypted)
    if score > 0:
        print(f"  shift={shift:2d}: score={score}, text={decrypted[:30]}")

# 3. Sagt BURUMUT seine Laenge?
# 99 = BURUMUT-Summe / 28
# 28 = R_28/9 = Tengri-Faktor
# 99 - 28 = 71
# 99 - 71 = 28 -> Rekursion!
print()
print("="*70)
print("Q7.3: Rekursive Struktur in BURUMUT?")
print("="*70)
print(f"  BURUMUT-Laenge = 99")
print(f"  BURUMUT-Summe  = 1232")
print(f"  1232 / 28 = 44.0  (44 = Tengri-Zahl)")
print(f"  99 - 71 = 28 (71 = ?)")
print(f"  1232 - 1108 = 124 = ?")
print(f"  99 + 1232 = 1331 = 11^3  <-- ZUFALL?")

# 4. Die 99-Zahl als magische Konstante
print()
print("="*70)
print("Q7.4: BURUMUT-Laenge 99 in der Physik")
print("="*70)
# 99 ist nicht prominent in der Physik, aber:
# - Anzahl der natuerlichen Elemente bis Es (99)
# - Einsteinium = Es = Element 99
# - 99 = 100 - 1 = eine 'Teiler-Defizit'-Zahl
print(f"  99 = 9 * 11")
print(f"  99 = 3^2 * 11")
print(f"  Element 99 = Einsteinium (Es)")
print(f"  Einsteinium ist nach Einstein benannt")
print(f"  Hat Verbindungen zu Alpha-Zerfall und Transuranen")

# 5. Was sagt die Sequenz ueber SELBST?
print()
print("="*70)
print("Q7.5: BURUMUT als selbstreferentielles Dokument")
print("="*70)
# Was wenn die ersten Buchstaben der UAZBE-Bloecke eine Botschaft ergeben?
# Block 0 (Vorspann): B-U-R-U-M
# Block 1 (HIMLAZANR): H-I-M-L-A
# Block 2 (NOMBAMZHQRSANLR): N-O-M-B-A
# Block 3 (NOMBARAZHQRSAN): N-O-M-B-A

# Wenn wir die ersten Buchstaben jedes Blockes nehmen:
initials = ['B', 'H', 'N', 'N']
print(f"  Initial-Buchstaben der Bloecke: {initials}")
# BURUMUT-HIMLAZANR-?
# Was wenn die Mittelpunkte eine Bedeutung haben?
print()
print("  Was wenn die UAZBE-Schleife ein 'rekursiver Restart' ist,")
print("  weil die Sequenz sich nicht von selbst versteht, sondern nur durch")
print("  eine Kontext-Aktivierung (Genesis, Protein-Kontext, etc.)?")

# 6. Die 'wahre Botschaft' - was wenn sie 137 ist?
print()
print("="*70)
print("Q7.6: Wenn die 'wahre Botschaft' 137 ist, wo erscheint sie?")
print("="*70)
# Suche nach 137 in der Matrix
# Wenn die Botschaft 137 waere, sollte sie irgendwo im BURUMUT-Buchstaben-
# Werten erscheinen.

# Alphabet-Index: B=2, U=21, R=18, ...
# Teste, ob die Summe einer 3-er-Gruppe 137 ergibt:
for i in range(0, len(BURUMUT_FULL) - 2):
    a, b, c = [ord(x) - ord('A') + 1 for x in BURUMUT_FULL[i:i+3]]
    if a + b + c == 137:
        print(f"  3-Gramm an Pos {i} ({BURUMUT_FULL[i:i+3]}): {a}+{b}+{c} = 137!")
# Oder mit 4-Buchstaben, 5-Buchstaben, etc.
# Oder mit 4, 5, 6, ...
for k in [4, 5, 6, 7, 8]:
    for i in range(0, len(BURUMUT_FULL) - k + 1):
        s = sum(ord(x) - ord('A') + 1 for x in BURUMUT_FULL[i:i+k])
        if s == 137:
            print(f"  {k}-Gramm an Pos {i} ({BURUMUT_FULL[i:i+k]}): Summe = 137!")
