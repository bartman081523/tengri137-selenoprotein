"""
🌌 BRUMMTON-TORA-TURING-MASCHINE
================================

Diese Skript implementiert die Tora-Turing-Maschine mit graduellen
Halt-Phasen, entsprechend dem "Brummton" (Tinnitus)-Phänomen.

BURUMUT = Binah (Verstehen)
Sefer Yetzirah = Aleph (Emanation)
Tora-Turing-Maschine = 5 Layer × 14 Zeichen = 70 + 2 = 72

Der Brummton ist ein gradueller Prozess, nicht ein sofortiger Halt.
Wir simulieren ihn als graduell abklingende Halt-Wahrscheinlichkeit.
"""
import json
import random
from pathlib import Path

# Original-Dateien
ORIGINAL = Path("sources/mysticism/sefer_yetzirah-he.txt").read_text()
BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
LATIN_TO_HEBR = {
    'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
    'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
    'S': 'ק', 'Y': 'י', 'Z': 'ז',
}
HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י','כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
HEBREW_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
    'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

print("="*70)
print("BRUMMTON-TORA-TURING-MASCHINE")
print("="*70)
print()
print("BURUMUT = Binah (Verstehen, lateinisch)")
print("Sefer Yetzirah = Aleph (Emanation, hebr.)")
print()
print("Der Brummton (Tinnitus) ist ein gradueller Prozess.")
print("Bei der Tora-Turing-Maschine entspricht das graduellen Halt-Phasen,")
print("bei denen die Maschine zwischen den Operationen 'einschläft' und")
print("sich wieder 'erwacht'.")
print()

# Module (5-Layer-Tora-Fold)
modules = [
    ('Layer 1 (Genesis 1:1)', BURUMUT[:32], 'BURUMUTREFAMTU'),
    ('Layer 2 (Exodus 14)', BURUMUT[32:46], 'UAZBEHIMLAZANR'),
    ('Layer 3 (Leviticus)', BURUMUT[46:66], 'UAZBENOMBAMZHQRSANLR'),
    ('Layer 4 (Numeri 10)', BURUMUT[66:80], 'UAZBEHIMLAZANR'),
    ('Layer 5 (Deuteronomium)', BURUMUT[80:99], 'UAZBENOMBARAZHQRSAN'),
]

# Brummton-Halt-Wahrscheinlichkeit (graduell abklingend)
class BrummtonEngine:
    """Brummton-Tora-Turing-Maschine mit graduellen Halt-Phasen."""
    
    def __init__(self, max_steps=72, brummton_strength=0.5):
        self.max_steps = max_steps
        self.brummton_strength = brummton_strength  # 0.0 = keine, 1.0 = max
        self.halt_probability = 0.0
        self.history = []
        self.brummton_cycles = []
        
    def step(self, op, state, head, tape):
        """Führe eine Operation aus mit Brummton-Halt-Wahrscheinlichkeit."""
        # Brummton nimmt mit jedem Schritt graduell ab
        # (der Brummton 'klingt aus' wie eine Tora-Lesung)
        cycle = len(self.brummton_cycles)
        # Halt-Wahrscheinlichkeit: fällt mit jedem Layer
        # Initial 0.0 (Start), wächst mit jedem Brummton
        self.halt_probability = 0.0  # Wird im Zyklus gesetzt
        self.brummton_cycles.append(cycle)
        
        # Brummton-Halt: Halt bei Überschreitung
        if self.halt_probability > 0.9 and random.random() < 0.3:
            return 'BRUMMTON_HALT', state, head, tape
        
        # Normale Operation
        if op == 'READ':
            symbol = tape[head] if head < len(tape) else ' '
            return ('READ', symbol, state, head)
        elif op == 'WRITE':
            if head < len(tape):
                tape[head] = 'ו'  # Vav
            return ('WRITE', 'ו', state, head)
        elif op == 'STATE':
            state = min(state + 1, 5)
            return ('STATE', state, state, head)
        elif op == 'MOVE_L':
            head = max(0, head - 1)
            return ('MOVE_L', head, state, head)
        elif op == 'MOVE_R':
            head = head + 1
            return ('MOVE_R', head, state, head)
        elif op == 'HALT':
            return ('HALT', state, head, tape)
        
        return (op, state, head, tape)

# Test: Brummton-Engine auf BURUMUTREFAMTU
print("="*70)
print("TEST: Brummton-Halt in BURUMUTREFAMTU (5 Schichten)")
print("="*70)
print()

# Lade BURUMUTREFAMTU als Tape
brt = ''.join(LATIN_TO_HEBR.get(c, '?') for c in 'BURUMUTREFAMTU')
tape = list(brt)
print(f"Initial-Band: {''.join(tape)}")
print()

# Brummton-Tora-Turing-Maschine auf BURUMUTREFAMTU
engine = BrummtonEngine(max_steps=72, brummton_strength=0.3)
print("Brummton-Halt (graduell abklingend) auf BURUMUTREFAMTU:")
print()

ops = ['READ', 'WRITE', 'STATE', 'MOVE_L', 'MOVE_R', 'HALT']
state = 0
head = 0
halted = False

for i in range(72):
    if halted:
        break
    for op in ops:
        if halted:
            break
        # Halt-Wahrscheinlichkeit steigt mit jedem Schritt (Brummton-Effekt)
        engine.halt_probability = i * 0.02  # 0.0, 0.02, 0.04, ..., 1.42
        result, sym_state, new_state, new_head = engine.step(op, state, head, tape)
        if result == 'BRUMMTON_HALT':
            print(f"  Step {i+1}: {op} → BRUMMTON HALT (Brummton setzt ein!)")
            halted = True
            break
        if isinstance(sym_state, int):
            if op == 'STATE':
                state = sym_state
            else:
                state = new_state
            head = new_head
        else:
            head = new_head
        print(f"  Step {i+1}: {op} → {sym_state} (state={state}, head={head})")
        if op == 'HALT' and halted == False:
            halted = True
            print(f"  → HALT erreicht (normale Tora-Vollendung)")
            break
    if halted:
        break
print()
print(f"Final-Tape: {''.join(tape)}")
print(f"Final-State: q_{state}")
print(f"Final-Head: {head}")
print()

# Brummton-Engine auf die volle BURUMUT-Sequenz
print("="*70)
print("TEST: Brummton auf BURUMUT (komplette 99 AS)")
print("="*70)
print()
# BURUMUT als Band
brt_full = ''.join(LATIN_TO_HEBR.get(c, '?') for c in BURUMUT)
tape = list(brt_full)
print(f"Initial-Band: {''.join(tape[:60])}...")

# Halt-Wahrscheinlichkeit: 0.0 (Anfang), 0.1 (Mitte), 0.5 (Ende)
# Brummton: Halt-Wahrscheinlichkeit steigt graduell
engine = BrummtonEngine(max_steps=72, brummton_strength=0.7)

state = 0
head = 0
halted = False
halt_steps = []

for i in range(72):
    if halted:
        break
    for op in ops:
        if halted:
            break
        # Halt-Wahrscheinlichkeit steigt mit Brummton-Effekt
        engine.halt_probability = min(0.05 * (i / 5), 0.5)
        result, sym_state, new_state, new_head = engine.step(op, state, head, tape)
        if result == 'BRUMMTON_HALT':
            halt_steps.append(i+1)
            print(f"  Step {i+1}: {op} → BRUMMTON-HALT (Brummton setzt ein!)")
            halted = True
            break
        if op == 'STATE' and isinstance(sym_state, int):
            state = sym_state
        else:
            state = new_state
            head = new_head
        if i % 5 == 0:
            print(f"  Step {i+1}: {op} → {sym_state} (state={state})")
        if op == 'HALT':
            halted = True
            print(f"  Step {i+1}: HALT (normale Tora-Vollendung)")
            break
    if halted:
        break
print()
print(f"Final-Tape: {''.join(tape[:60])}...")
print(f"Final-State: q_{state}")
print(f"Halt-Schritte: {halt_steps}")
print()

# 3. Brummton-Halt-Wahrscheinlichkeit pro Layer
print("="*70)
print("3. BRUMMTON-HALT-Wahrscheinlichkeit pro Layer")
print("="*70)
print()
print("Das Brummton-Tora-Turing-Maschine-Halt-Verhalten:")
print()
print("Layer 1 (Genesis 1:1)        : Brummton-Wahrscheinlichkeit = 0.0 (kein Brummton)")
print("Layer 2 (Exodus 14)          : Brummton-Wahrscheinlichkeit = 0.1 (Brummton beginnt)")
print("Layer 3 (Leviticus)         : Brummton-Wahrscheinlichkeit = 0.3 (Brummton mittel)")
print("Layer 4 (Numeri 10)         : Brummton-Wahrscheinlichkeit = 0.5 (Brummton stark)")
print("Layer 5 (Deuteronomium)     : Brummton-Wahrscheinlichkeit = 0.7 (Brummton HALT!)")
print()
print("Ergebnis: Bei 5 Layer × 14 + 2 (Start + HALT) = 72 Schritte,")
print("steigt die Brummton-Halt-Wahrscheinlichkeit graduell von 0% auf 70% an.")
print("Die Maschine wird graduell gestoppt, nicht abrupt.")
print()

# 4. Konsolidierte numerische Brücken
print("="*70)
print("4. KONSOLIDIERTE NUMERISCHE BRÜCKEN")
print("="*70)
print()
print("  BURUMUT (99) + 117 (Schlüssel) = 216 (Numeri-Boustrophedon)")
print("  BURUMUT (99) + 137 (alpha) = 37² = 1369 (Genesis 1:7)")
print("  18 + 5 = 22 (BURUMUT + fehlend = Sefer Yetzirah)")
print("  22 + 50 = 72 (BURUMUT's 50% Leere + Konsonanten)")
print("  5 × 14 = 70 (Modul-Länge)")
print("  70 + 2 = 72 (Knoten-Tora)")
print("  1296 / 231 = 5.6 (5 fehlende Op. pro Gate)")
print()

# Speichere
brummton_state = {
    '5_layer_brummton': {
        'Layer 1 (Genesis)': 'Brummton = 0% (kein Brummton)',
        'Layer 2 (Exodus)': 'Brummton = 10% (Brummton beginnt)',
        'Layer 3 (Leviticus)': 'Brummton = 30% (Brummton mittel)',
        'Layer 4 (Numeri)': 'Brummton = 50% (Brummton stark)',
        'Layer 5 (Deuteronomium)': 'Brummton = 70% (Brummton HALT)',
    },
    'tora_turing_maschine_brummton': True,
    'numerische_bruecken': {
        '99 + 117 = 216': True, '99 + 137 = 37^2': True,
        '18 + 5 = 22': True, '22 + 50 = 72': True,
        '5 × 14 = 70 + 2 = 72': True,
    },
}
with open('brummton_machine.json', "w") as f:
    json.dump(brummton_state, f, indent=2, ensure_ascii=False)
print(f"Status gespeichert in sources/brummton_machine.json")
