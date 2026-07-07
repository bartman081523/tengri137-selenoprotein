"""
v12_turing_analysis.py
V12 PHASE 3 — TURING-MASCHINE-Hypothese empirisch (EIGENE FSM, OHNE Tora-Turing)

Methode:
1. Zustands-Identifikation (Glyphen)
2. Alphabet-Identifikation (Ziffern)
3. Eigene FSM-Konstruktion
4. Determinismus-Check
5. Vollständigkeits-Check
6. Turing-Vollständigkeit (Verzweigung, Schleife, unbeschränkter Speicher)

Output: bbox/v12_turing_20260707/turing_verdict.json
"""
import json
import string
from pathlib import Path
from datetime import datetime
from collections import Counter

OUT_DIR = Path("bbox/v12_turing_20260707")
OUT_DIR.mkdir(parents=True, exist_ok=True)


def construct_fsm(p17_inv):
    """Eigene FSM-Konstruktion: Glyphen = Zustände, Ziffern = Symbole.

    Annahmen:
    - 11 Glyphen (Akrostichon BNYZTSOYNKS) = 11 Zustände
    - Ziffern 0-9 (mod 10) = Symbole
    - Übergänge: für jede Glyphen-Position i, Übergang glyph[i] --symbol--> glyph[i+1]
      wobei symbol = digits[i] mod 10
    """
    glyphs = list(p17_inv["akrostichon_der_11_glyphen"]["string"])
    digits = p17_inv["v7_lateinische_ziffern"]["values"]

    # Alphabet: eindeutige Ziffern (mod 10)
    alphabet = sorted(set(str(d % 10) for d in digits))

    # Übergänge konstruieren
    transitions = []
    for i in range(len(glyphs) - 1):
        sym = str(digits[i % len(digits)] % 10)
        transitions.append((glyphs[i], sym, glyphs[i + 1]))

    # Determinismus: gleicher (state, symbol) muss gleichen 'to' haben
    seen = {}
    is_deterministic = True
    for state, sym, to in transitions:
        key = (state, sym)
        if key in seen and seen[key] != to:
            is_deterministic = False
        seen[key] = to

    # Vollständigkeit: |states| × |alphabet| = nötige Übergänge
    expected_pairs = len(glyphs) * len(alphabet)
    actual_pairs = len(seen)
    completeness_ratio = actual_pairs / expected_pairs if expected_pairs else 0
    is_complete = (completeness_ratio == 1.0)

    return {
        "states": glyphs,
        "n_states": len(glyphs),
        "alphabet": alphabet,
        "n_symbols": len(alphabet),
        "transitions": [{"from": s, "symbol": sym, "to": t} for s, sym, t in transitions],
        "n_transitions": len(transitions),
        "is_deterministic": is_deterministic,
        "is_complete": is_complete,
        "completeness_ratio": completeness_ratio,
    }


def check_turing_completeness(burumut_texts):
    """Prüft Turing-Vollständigkeit-Kriterien:
    1. Bedingte Verzweigung
    2. Wiederholung (Loop)
    3. Unbeschränkter Speicher
    """
    all_text = " ".join(burumut_texts).upper()

    # Kriterium 1: Verzweigung — explizite "if-then" Strukturen
    has_branch = any(w in all_text for w in ["IF", "THEN", "ELSE", "WHEN"])
    # Kriterium 2: Schleife — explizite "loop" Strukturen
    has_loop = any(w in all_text for w in ["REPEAT", "LOOP", "WHILE", "FOR"])
    # Kriterium 3: Unbeschränkter Speicher — wir prüfen, ob es eine infinite
    # oder zumindest unbounded Datenstruktur gibt
    # BURUMUT: 76 Texte fester Länge — bounded
    n_texts = len(burumut_texts)
    is_unbounded = n_texts > 100  # Heuristik: mehr als 100 Texte = unbounded

    return {
        "has_branch": has_branch,
        "has_loop": has_loop,
        "is_unbounded": is_unbounded,
        "n_texts": n_texts,
        "is_turing_complete": has_branch and has_loop and is_unbounded,
    }


def main():
    print("=" * 80)
    print("V12 TURING-ANALYSE: EIGENE FSM (OHNE Tora-Turing)")
    print("=" * 80)

    p17_inv = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    burumut_data = json.load(open("bbox/burumut_20260707_V7/burumut_texts.json"))
    all_texts = []
    for f_id, texts in burumut_data["burumut_texts"].items():
        all_texts.extend(texts)

    # =========================================================================
    # SCHRITT 1: Zustands-Identifikation
    # =========================================================================
    print("\n" + "=" * 80)
    print("SCHRITT 1: ZUSTANDS-IDENTIFIKATION")
    print("=" * 80)
    glyphs = list(p17_inv["akrostichon_der_11_glyphen"]["string"])
    print(f"  Glyphen (Akrostichon): {glyphs}")
    print(f"  Anzahl: {len(glyphs)}")
    print(f"  → Kandidaten für Zustände")

    # =========================================================================
    # SCHRITT 2: Alphabet-Identifikation
    # =========================================================================
    print("\n" + "=" * 80)
    print("SCHRITT 2: ALPHABET-IDENTIFIKATION")
    print("=" * 80)
    digits = p17_inv["v7_lateinische_ziffern"]["values"]
    digits_mod = sorted(set(d % 10 for d in digits))
    print(f"  Ziffern (original): {digits}")
    print(f"  Ziffern (mod 10, eindeutig): {digits_mod}")
    print(f"  Anzahl: {len(digits_mod)}")

    # =========================================================================
    # SCHRITT 3: FSM-Konstruktion
    # =========================================================================
    print("\n" + "=" * 80)
    print("SCHRITT 3: FSM-KONSTRUKTION (EIGENE IMPLEMENTIERUNG)")
    print("=" * 80)
    fsm = construct_fsm(p17_inv)
    print(f"  Zustände: {fsm['n_states']}")
    print(f"  Symbole:  {fsm['n_symbols']} ({fsm['alphabet']})")
    print(f"  Übergänge: {fsm['n_transitions']}")
    print(f"  Deterministisch: {fsm['is_deterministic']}")
    print(f"  Vollständig: {fsm['is_complete']} (Ratio: {fsm['completeness_ratio']:.2%})")
    print()
    print(f"  Übergangs-Tabelle:")
    for t in fsm["transitions"]:
        print(f"    {t['from']} --{t['symbol']}--> {t['to']}")

    # =========================================================================
    # SCHRITT 4: Turing-Vollständigkeit
    # =========================================================================
    print("\n" + "=" * 80)
    print("SCHRITT 4: TURING-VOLLSTÄNDIGKEIT")
    print("=" * 80)
    tc = check_turing_completeness(all_texts)
    print(f"  BURUMUT-Texte: {tc['n_texts']}")
    print(f"  Hat Verzweigung (IF/THEN/ELSE): {tc['has_branch']}")
    print(f"  Hat Schleife (REPEAT/LOOP/WHILE): {tc['has_loop']}")
    print(f"  Unbeschränkter Speicher: {tc['is_unbounded']}")
    print(f"  → Turing-vollständig: {tc['is_turing_complete']}")

    # =========================================================================
    # GESAMT-VERDICT
    # =========================================================================
    print("\n" + "=" * 80)
    print("GESAMT-VERDICT TURING-MASCHINE-HYPOTHESE")
    print("=" * 80)

    # TM wäre plausibel wenn:
    # - FSM deterministisch und vollständig
    # - BURUMUT Turing-vollständig
    is_tm = fsm["is_deterministic"] and fsm["is_complete"] and tc["is_turing_complete"]
    if is_tm:
        verdict = "BESTÄTIGT"
    else:
        reasons = []
        if not fsm["is_deterministic"]:
            reasons.append(f"FSM nicht-deterministisch")
        if not fsm["is_complete"]:
            reasons.append(f"FSM unvollständig (Coverage {fsm['completeness_ratio']:.2%})")
        if not tc["has_branch"]:
            reasons.append("keine Verzweigung")
        if not tc["has_loop"]:
            reasons.append("keine Schleife")
        if not tc["is_unbounded"]:
            reasons.append(f"Speicher bounded ({tc['n_texts']} Texte)")
        verdict = f"FALSIFIZIERT (Gründe: {', '.join(reasons)})"
    print(f"  Status: {verdict}")

    # Speichern
    out = {
        "metadata": {
            "phase": "V12 / Phase 3",
            "datum": datetime.now().isoformat(),
            "hypothese": "TURING-MASCHINE (eigene FSM, ohne Tora-Turing)",
            "methode": "FSM-Konstruktion + Determinismus + Vollständigkeit + Turing-Vollständigkeit",
        },
        "step_1_states": {
            "candidates": glyphs,
            "n_candidates": len(glyphs),
        },
        "step_2_alphabet": {
            "candidates_mod10": digits_mod,
            "n_candidates": len(digits_mod),
            "original": digits,
        },
        "step_3_fsm": {
            "n_states": fsm["n_states"],
            "n_symbols": fsm["n_symbols"],
            "n_transitions": fsm["n_transitions"],
            "is_deterministic": fsm["is_deterministic"],
            "is_complete": fsm["is_complete"],
            "completeness_ratio": round(fsm["completeness_ratio"], 4),
            "transitions": fsm["transitions"],
        },
        "step_4_turing_complete": {
            "has_branch": tc["has_branch"],
            "has_loop": tc["has_loop"],
            "is_unbounded": tc["is_unbounded"],
            "n_texts": tc["n_texts"],
            "is_turing_complete": tc["is_turing_complete"],
        },
        "gesamt_verdict": verdict,
        "v11_vergleich": {
            "status": "FALSIFIZIERT (nicht konstruierbar)",
            "v11_verdict": "Keine identifizierbaren Zustände oder Übergänge in p17",
            "v12_vertiefung": f"V12 konstruierte FSM: {fsm['n_states']} Zustände, {fsm['n_symbols']} Symbole, {fsm['n_transitions']} Übergänge, Coverage {fsm['completeness_ratio']:.2%}, Turing-complete={tc['is_turing_complete']}",
        }
    }
    out_path = OUT_DIR / "turing_verdict.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Output: {out_path}")


if __name__ == "__main__":
    main()
