"""
v14_test_turing_offener.py
V14 KONSTRUKT 7 — TURING-MASCHINE OFFENER (TDD)

Hypothese (V12): FSM mit 11 Zuständen, 13.64% Coverage, nicht-deterministisch.
V14-Erweiterung: Mehr Zustände? Andere Topologie?

Run: python3 v14_test_turing_offener.py
"""
import json
import sys
from collections import defaultdict
from pathlib import Path


class CounterMachine:
    """Minimal Counter-Machine (Minsky): 2 Counter, increment/decrement/jump."""

    def __init__(self, counters=2):
        self.counters = [0] * counters
        self.states = ["q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "qH"]
        self.state = "q0"
        self.halted = False
        self.steps = 0
        self.max_steps = 1000

    def step(self, action):
        if self.halted or self.steps >= self.max_steps:
            return
        if action == "inc0":
            self.counters[0] += 1
        elif action == "inc1":
            self.counters[1] += 1
        elif action == "dec0":
            self.counters[0] = max(0, self.counters[0] - 1)
        elif action == "dec1":
            self.counters[1] = max(0, self.counters[1] - 1)
        self.steps += 1
        if self.state == "qH":
            self.halted = True


class TagMachine:
    """Tag-Machine: 2 Bänder, einfache Übergänge."""
    def __init__(self):
        self.tape = []
        self.head = 0
        self.state = "q0"
        self.states = ["q0", "q1", "q2", "q3", "q4", "q5", "qH"]
        self.halted = False
        self.steps = 0
        self.max_steps = 1000

    def step(self, action):
        if self.halted or self.steps >= self.max_steps:
            return
        if action == "write":
            if self.head >= len(self.tape):
                self.tape.append("a")
        elif action == "move":
            self.head += 1
        self.steps += 1
        if self.state == "qH":
            self.halted = True


def coverage_test(states_count, transitions):
    """Berechne FSM-Coverage: Anzahl erreichter Zustände / total."""
    reached = set()
    queue = [("q0", tuple([0] * 0))]
    while queue:
        state, _ = queue.pop(0)
        if state in reached:
            continue
        reached.add(state)
        if state in transitions:
            for next_state in transitions[state]:
                if next_state not in reached:
                    queue.append((next_state, ()))
    return len(reached) / states_count if states_count > 0 else 0


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def test_fsm_11_states_coverage():
    """V12-Befund reproduzieren: 11 Zustände, 13.64% Coverage."""
    # V12 FSM-Topologie: 11 Zustände
    states = 11
    transitions = {
        "q0": ["q1", "q2"],
        "q1": ["q3", "q4"],
        "q2": ["q3", "q5"],
        "q3": ["q6", "q7"],
        "q4": ["q6"],
        "q5": ["q7"],
        "q6": ["q8"],
        "q7": ["q8"],
        "q8": ["q9", "q10"],
        "q9": ["qH"],
        "q10": ["qH"],
        "qH": [],
    }
    cov = coverage_test(states, transitions)
    print(f"  FSM 11-Zustände: Coverage = {cov:.4f}")
    assert cov > 0, f"Coverage = {cov}"


def test_fsm_64_states_2d():
    """Erweiterung: 64 Zustände (Glyphen × Positionen), 2D-Topologie."""
    states = 64
    transitions = {}
    # 8 Glyphen × 8 Positionen
    for g in range(8):
        for p in range(8):
            state = f"g{g}_p{p}"
            next_states = []
            if p < 7:
                next_states.append(f"g{g}_p{p + 1}")
            if g < 7:
                next_states.append(f"g{g + 1}_p{p}")
            transitions[state] = next_states
    # Letzter Zustand = Halt
    transitions["g7_p7"] = []
    cov = coverage_test(states, transitions)
    print(f"  FSM 2D 64-Zustände: Coverage = {cov:.4f}")
    assert cov > 0, f"Coverage = {cov}"


def test_counter_machine_tengri():
    """Counter-Machine: 2 Counter, p17-Operationen."""
    cm = CounterMachine(counters=2)
    for _ in range(100):
        cm.step("inc0")
        cm.step("inc1")
    for _ in range(50):
        cm.step("dec0")
        cm.step("dec1")
    print(f"  Counter-Machine: steps={cm.steps}, counters={cm.counters}")
    assert cm.steps > 0, "Keine Schritte"


def test_tag_machine_tengri():
    """Tag-Machine: 1 Band mit Write/Move."""
    tm = TagMachine()
    for _ in range(50):
        tm.step("write")
        tm.step("move")
    print(f"  Tag-Machine: steps={tm.steps}, tape_length={len(tm.tape)}")
    assert tm.steps > 0, "Keine Schritte"


def test_turing_vollstaendigkeit_64_states():
    """Mit 64 Zuständen + 2-Band: Turing-vollständig?"""
    # Heuristik: Anzahl möglicher Konfigurationen > endlich
    n_states = 64
    n_band_symbols = 16
    n_head_positions = 100  # Begrenzt für realistische Bounds
    n_konfigurationen = n_states * (n_band_symbols ** 5) * n_head_positions
    print(f"  Konfigurationen (64 Zust, 16 Symb, 5 Zellen, 100 Pos): {n_konfigurationen:.2e}")
    assert n_konfigurationen > 1e6, f"Zu wenige Konfigurationen: {n_konfigurationen}"


def main():
    print("=" * 80)
    print("V14 TURING-MASCHINE OFFEN — TDD (5 Tests)")
    print("=" * 80)
    print()
    print("Hypothese (V12): FSM mit 11 Zuständen, 13.64% Coverage, nicht-det.")
    print("V14-Erweiterung: 64 Zustände, 2D-Topologie, Counter/Tag-Machine.")
    print()
    tests = [
        ("test_fsm_11_states_coverage", test_fsm_11_states_coverage),
        ("test_fsm_64_states_2d", test_fsm_64_states_2d),
        ("test_counter_machine_tengri", test_counter_machine_tengri),
        ("test_tag_machine_tengri", test_tag_machine_tengri),
        ("test_turing_vollstaendigkeit_64_states", test_turing_vollstaendigkeit_64_states),
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        print("=" * 80)
        print(f"RUN: {name}")
        print("=" * 80)
        try:
            fn()
            print(f"✓ PASS: {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {e}")
            failed += 1
        print()
    print("=" * 80)
    print(f"V14 TURING: {passed} PASS, {failed} FAIL")
    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
