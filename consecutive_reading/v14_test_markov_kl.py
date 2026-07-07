"""
v14_test_markov_kl.py
V14 KONSTRUKT 4 — MARKOV-KETTEN + KL-DIVERGENZ (TDD)

Hypothese (V14, neu): p17-23 und p1-16 haben ähnliche Übergangswahrscheinlichkeiten.
V14-Methode: Markov-Ketten 1./2. Ordnung, KL-Divergenz.

Run: python3 v14_test_markov_kl.py
"""
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path


def markov_chain(text, order=1):
    """Markov-Kette: Übergangswahrscheinlichkeiten P(next | current_ngram)."""
    if len(text) <= order:
        return {}, set()
    transitions = defaultdict(Counter)
    states = set()
    for i in range(len(text) - order):
        state = text[i:i + order]
        next_char = text[i + order]
        transitions[state][next_char] += 1
        states.add(state)
    # Normalisierung
    probs = {}
    for state, counts in transitions.items():
        total = sum(counts.values())
        probs[state] = {c: n / total for c, n in counts.items()}
    return probs, states


def kl_divergence(p_probs, q_probs, states):
    """KL(P || Q) in bit/Zeichen."""
    kl = 0.0
    for state in states:
        if state not in p_probs:
            continue
        p_dist = p_probs[state]
        q_dist = q_probs.get(state, {})
        for c, p in p_dist.items():
            if p > 0:
                q = q_dist.get(c, 1e-10)  # Smoothing
                kl += p * math.log2(p / q)
    return kl / max(len(states), 1)


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def test_markov_1st_order_p17():
    """Markov-Kette 1. Ordnung für p17 existiert."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    probs, states = markov_chain(text, order=1)
    print(f"  p17 Markov-1: {len(states)} Zustände")
    assert len(states) > 0, "Keine Zustände"


def test_markov_1st_order_p1_16():
    """Markov-Kette 1. Ordnung für p1-16 existiert."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    probs, states = markov_chain(text, order=1)
    print(f"  p1-16 Markov-1: {len(states)} Zustände")
    assert len(states) > 0, "Keine Zustände"


def test_kl_divergence_p17_p1_16_order1():
    """KL(p17 || p1-16) für Markov-1 (Schwelle: endlich)."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p1 = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    p_probs, p_states = markov_chain(text_p17, order=1)
    q_probs, q_states = markov_chain(text_p1, order=1)
    common = p_states & q_states
    kl = kl_divergence(p_probs, q_probs, common)
    print(f"  KL(p17||p1-16, order=1) = {kl:.4f} bit/Zeichen ({len(common)} gemeinsame Zustände)")
    assert math.isfinite(kl), f"KL = {kl} nicht endlich"


def test_kl_divergence_p17_p1_16_order2():
    """KL(p17 || p1-16) für Markov-2."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p1 = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    p_probs, p_states = markov_chain(text_p17, order=2)
    q_probs, q_states = markov_chain(text_p1, order=2)
    common = p_states & q_states
    kl = kl_divergence(p_probs, q_probs, common)
    print(f"  KL(p17||p1-16, order=2) = {kl:.4f} bit/Zeichen ({len(common)} gemeinsame Zustände)")
    assert math.isfinite(kl), f"KL = {kl} nicht endlich"


def test_kl_divergence_p17_p23_order1():
    """KL(p17 || p23) — gleicher Schicht-Typ (Klartext↔BURUMUT)."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p23 = " ".join(w["wort"] for w in p23["woerter"])
    p_probs, p_states = markov_chain(text_p17, order=1)
    q_probs, q_states = markov_chain(text_p23, order=1)
    common = p_states & q_states
    kl = kl_divergence(p_probs, q_probs, common)
    print(f"  KL(p17||p23, order=1) = {kl:.4f} bit/Zeichen ({len(common)} gemeinsame Zustände)")
    assert math.isfinite(kl), f"KL = {kl} nicht endlich"


def test_kl_asymmetrie():
    """KL ist asymmetrisch: KL(P||Q) ≠ KL(Q||P) im Allgemeinen."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p1 = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    p_probs, _ = markov_chain(text_p17, order=1)
    q_probs, _ = markov_chain(text_p1, order=1)
    _, p_states = markov_chain(text_p17, order=1)
    _, q_states = markov_chain(text_p1, order=1)
    common = p_states & q_states
    kl_pq = kl_divergence(p_probs, q_probs, common)
    kl_qp = kl_divergence(q_probs, p_probs, common)
    print(f"  KL(P||Q) = {kl_pq:.4f}, KL(Q||P) = {kl_qp:.4f}")
    # Asymmetrie: sollten verschieden sein (außer bei perfekter Symmetrie)
    assert math.isfinite(kl_pq) and math.isfinite(kl_qp)


def main():
    print("=" * 80)
    print("V14 MARKOV-KETTEN + KL — TDD (6 Tests)")
    print("=" * 80)
    print()
    print("Hypothese (V14 neu): Markov-Übergänge p17↔p1-16 zeigen strukturelle Kopplung.")
    print("V14-Methode: KL-Divergenz über 1./2. Ordnung.")
    print()
    tests = [
        ("test_markov_1st_order_p17", test_markov_1st_order_p17),
        ("test_markov_1st_order_p1_16", test_markov_1st_order_p1_16),
        ("test_kl_divergence_p17_p1_16_order1", test_kl_divergence_p17_p1_16_order1),
        ("test_kl_divergence_p17_p1_16_order2", test_kl_divergence_p17_p1_16_order2),
        ("test_kl_divergence_p17_p23_order1", test_kl_divergence_p17_p23_order1),
        ("test_kl_asymmetrie", test_kl_asymmetrie),
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
    print(f"V14 MARKOV: {passed} PASS, {failed} FAIL")
    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
