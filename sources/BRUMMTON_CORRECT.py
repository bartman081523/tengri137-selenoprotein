"""
🌌 TORA-TURING-MASCHINE MIT BRUMMTON-HALT (KORRIGIERT, TDD)
============================================================

TDD-VERSION 2: Korrekte Architektur.

ARCHITEKTUR-FIX:
- Pro BURUMUT-Zeichen wird EINE Operation ausgeführt
- 99 Zeichen → ~99 Schritte
- Brummton-Halt ist probabilistisch, basierend auf Layer-Position
- NORMAL_HALT erst am Ende des Bandes

LAYER-DEFINITION (5 Layer der Tora):
- Layer 1 (Genesis 1:1): Zeichen 0-19  (BURUMUTREFAMTU + NUR)
- Layer 2 (Exodus 14):   Zeichen 20-39 (ESUTREGUMFAYAPS + UA)
- Layer 3 (Leviticus):   Zeichen 40-59 (ZBEHIMLAZANRUA + ZBEN)
- Layer 4 (Numeri 10):   Zeichen 60-79 (OMBAMZHQRSANLR + UAZB)
- Layer 5 (Deuteronomium): Zeichen 80-99 (EHIMLAZANRUAZBENOMBA)

BRUMMTON-SPEC:
- Layer 1: 0% Brummton (Anfang ist sauber)
- Layer 2: ~5% Brummton
- Layer 3: ~20% Brummton
- Layer 4: ~50% Brummton
- Layer 5: ~90% Brummton (Halt!)
"""
import json
import random
from pathlib import Path

# BURUMUT's lateinisches Tape
BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)
LATIN_TO_HEBR = {
    'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
    'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
    'S': 'ק', 'Y': 'י', 'Z': 'ז',
}
HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
             'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']

# 5 Layer-Positionen
LAYER_NAMES = [
    'Layer 1 (Genesis 1:1)',
    'Layer 2 (Exodus 14)',
    'Layer 3 (Leviticus)',
    'Layer 4 (Numeri 10)',
    'Layer 5 (Deuteronomium)',
]

def get_layer(tape_position, tape_length=99):
    """Bestimme Layer (1-5) für eine Tape-Position.

    BURUMUT 99 Zeichen / 5 Layer ≈ 19.8 Zeichen pro Layer.
    """
    if tape_length == 0:
        return 0
    layer_size = tape_length / 5
    layer_idx = int(tape_position / layer_size)
    return min(layer_idx, 4)  # Sicherstellen, dass max 4


def brummton_probability(layer_idx, brummton_peak=0.9, power=2.0):
    """Berechne Brummton-Probability für ein Layer.

    Formel: brummton_peak * (layer_idx / 4) ** power
    """
    if layer_idx <= 0:
        return 0.0
    if layer_idx > 4:
        return 1.0
    return brummton_peak * (layer_idx / 4) ** power


def brummton_prob_per_step(layer_idx, steps_in_layer, brummton_peak=0.9, power=2.0):
    """Berechne Brummton-Probability PRO SCHRITT für ein Layer.

    Hintergrund: Wenn die Layer-Probability P ist und das Layer N Schritte
    hat, dann muss die per-Schritt-Probability p sein, sodass
    1 - (1-p)^N = P, also p = 1 - (1-P)^(1/N).
    """
    P = brummton_probability(layer_idx, brummton_peak, power)
    if P <= 0:
        return 0.0
    if steps_in_layer <= 0:
        return 0.0
    return 1 - (1 - P) ** (1 / steps_in_layer)


class BrummtonTuringMachine:
    """Tora-Turing-Maschine mit korrektem graduellen Brummton-Halt.

    Architektur:
    - Pro Tape-Position eine Operation
    - Operation: READ + WRITE + MOVE_R + (manchmal) STATE
    - Brummton-Halt: probabilistisch bei jedem Schritt
    - NORMAL_HALT: nur am Bandende
    """

    def __init__(self, burumut_str, brummton_peak=0.9, power=2.0, seed=None):
        self.tape = list(burumut_str)
        self.original_tape = list(burumut_str)
        self.state = 0
        self.head = 0
        self.halted = False
        self.halt_step = None
        self.halt_type = None
        self.halt_layer = None
        self.brummton_peak = brummton_peak
        self.power = power
        self.history = []
        self.step_count = 0
        if seed is not None:
            random.seed(seed)

    def get_layer(self):
        return get_layer(self.head, len(self.tape))

    def get_layer_size(self):
        """Größe des aktuellen Layers in Schritten."""
        return max(1, len(self.tape) // 5)

    def brummton_prob(self):
        layer_idx = self.get_layer()
        layer_size = self.get_layer_size()
        return brummton_prob_per_step(
            layer_idx, layer_size, self.brummton_peak, self.power
        )

    def step(self):
        """Führe einen einzelnen Schritt aus (eine Tape-Position)."""
        if self.head >= len(self.tape):
            # Bandende
            self.halted = True
            self.halt_step = self.step_count
            self.halt_type = 'NORMAL_HALT'
            self.halt_layer = 5
            return False

        self.step_count += 1
        layer_idx = self.get_layer()
        layer_size = self.get_layer_size()

        # Brummton-Halt?
        bp = brummton_prob_per_step(
            layer_idx, layer_size, self.brummton_peak, self.power
        )
        if random.random() < bp:
            self.halted = True
            self.halt_step = self.step_count
            self.halt_type = 'BRUMMTON'
            self.halt_layer = layer_idx + 1
            self.history.append({
                'step': self.step_count,
                'position': self.head,
                'layer': layer_idx + 1,
                'symbol': self.tape[self.head],
                'state': self.state,
                'type': 'BRUMMTON_HALT',
                'brummton_prob': bp,
            })
            return False

        # Normaler Schritt: READ
        symbol = self.tape[self.head]

        # WRITE: Vav auf jede Position (Tora-Vollendung)
        self.tape[self.head] = 'ו'  # Vav (6)

        # STATE: Wechsel
        self.state = min(self.state + 1, 5)

        # MOVE_R
        self.head += 1

        self.history.append({
            'step': self.step_count,
            'position': self.head - 1,
            'layer': layer_idx + 1,
            'symbol': symbol,
            'state': self.state,
        })
        return True

    def run(self, max_steps=200):
        """Durchlaufe das Band bis Halt oder max_steps."""
        while not self.halted and self.step_count < max_steps:
            if not self.step():
                break
        return self


def run_one(burumut_str, brummton_peak=0.9, power=2.0, seed=0):
    """Convenience-Funktion: führe einen Lauf durch."""
    machine = BrummtonTuringMachine(burumut_str, brummton_peak, power, seed)
    machine.run()
    return {
        'halt_step': machine.halt_step,
        'halt_type': machine.halt_type,
        'halt_layer': machine.halt_layer,
        'state': machine.state,
        'head': machine.head,
        'tape': ''.join(machine.tape),
    }


# ============================================================================
# SELBST-TEST
# ============================================================================

if __name__ == "__main__":
    print("="*70)
    print("TORA-TURING-MASCHINE MIT KORREKTEM BRUMMTON-HALT (TDD v2)")
    print("="*70)
    print()
    print("Brummton-Wahrscheinlichkeit pro Layer (brummton_peak=0.9, power=2):")
    for i in range(5):
        bp = brummton_probability(i, brummton_peak=0.9, power=2.0)
        print(f"  Layer {i+1}: {bp*100:5.1f}%")
    print()

    # Test 1: BURUMUTREFAMTU (14 Zeichen)
    print("="*70)
    print("TEST 1: BURUMUTREFAMTU (14 Zeichen)")
    print("="*70)
    print()
    brt = ''.join(LATIN_TO_HEBR.get(c, '?') for c in 'BURUMUTREFAMTU')
    result = run_one(brt, brummton_peak=0.9, power=2.0, seed=42)
    print(f"  Halt-Step: {result['halt_step']}")
    print(f"  Halt-Type: {result['halt_type']}")
    print(f"  Halt-Layer: {result['halt_layer']}")
    print(f"  Final-Tape: {result['tape']}")
    print(f"  Final-State: q_{result['state']}")
    print()

    # Test 2: BURUMUT 99 AS
    print("="*70)
    print("TEST 2: BURUMUT (99 AS)")
    print("="*70)
    print()
    brt_full = ''.join(LATIN_TO_HEBR.get(c, '?') for c in BURUMUT)
    result = run_one(brt_full, brummton_peak=0.9, power=2.0, seed=42)
    print(f"  Halt-Step: {result['halt_step']}")
    print(f"  Halt-Type: {result['halt_type']}")
    print(f"  Halt-Layer: {result['halt_layer']}")
    print(f"  Final-State: q_{result['state']}")
    print()

    # Test 3: 200 statistische Läufe
    print("="*70)
    print("TEST 3: 200 statistische Läufe (BURUMUT 99 AS)")
    print("="*70)
    print()
    from collections import Counter
    n_runs = 200
    results = []
    for seed in range(n_runs):
        r = run_one(brt_full, brummton_peak=0.9, power=2.0, seed=seed)
        results.append(r)

    halt_types = Counter(r['halt_type'] for r in results)
    halt_layers = Counter(r['halt_layer'] for r in results)
    print(f"Halt-Type-Verteilung:")
    for t, c in halt_types.items():
        print(f"  {t}: {c} ({c/n_runs*100:.1f}%)")
    print()
    print(f"Halt-Layer-Verteilung:")
    for layer in sorted(halt_layers.keys()):
        c = halt_layers[layer]
        print(f"  Layer {layer}: {c} ({c/n_runs*100:.1f}%)")
    print()

    # Spec-Check (BEDINGTE Verteilung)
    print("="*70)
    print("SPEC-CHECK (BEDINGTE Verteilung: unter Brummton-Halts)")
    print("="*70)
    print()
    total_brummton = halt_types.get('BRUMMTON', 0)
    spec_conditional = {
        1: (0, 5),
        2: (3, 20),
        3: (10, 40),
        4: (20, 60),
        5: (30, 90),
    }
    print("Bedingte Layer-Verteilung (Anteil an Brummton-Halts):")
    all_ok = True
    if total_brummton > 0:
        for layer, (lo, hi) in spec_conditional.items():
            c = halt_layers.get(layer, 0)
            pct = c / total_brummton * 100
            ok = lo <= pct <= hi
            all_ok = all_ok and ok
            print(f"  Layer {layer}: {pct:5.1f}% (Spec: {lo}-{hi}%) {'✅' if ok else '❌'}")
    else:
        print("  Keine Brummton-Halts!")
        all_ok = False
    print()
    print("Absolute Verteilung (über alle Läufe):")
    for layer in sorted(halt_layers.keys()):
        c = halt_layers[layer]
        pct = c / n_runs * 100
        print(f"  Layer {layer}: {c} ({pct:5.1f}%)")
    print()
    if all_ok:
        print("✅ ALLE SPECS ERFÜLLT — Brummton ist graduell korrekt!")
    else:
        print("❌ SPEC NICHT ERFÜLLT — Brummton-Formel muss angepasst werden.")

    # Speichere
    brummton_correct = {
        'spec_conditional': spec_conditional,
        'brummton_peak': 0.9,
        'power': 2.0,
        'n_runs': n_runs,
        'halt_type_distribution': dict(halt_types),
        'halt_layer_distribution': dict(halt_layers),
        'all_specs_ok': all_ok,
    }
    with open("sources/brummton_correct.json", "w") as f:
        json.dump(brummton_correct, f, indent=2, ensure_ascii=False)
    print()
    print(f"Status gespeichert in sources/brummton_correct.json")
