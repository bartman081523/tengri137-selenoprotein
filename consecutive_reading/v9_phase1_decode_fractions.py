"""
v9_phase1_decode_fractions.py
V9 Phase 1 — Vollständige BURUMUT-Dekodierung aller p17-p23 Faktorzerlegungen

Methode: dcode.fr atomic-number-substitution
- Berechne Bruch = numerator / denominator
- Periode extrahieren (sich wiederholende Ziffern)
- Periode in 2-Ziffer-Dinome aufteilen (00-99)
- 00 = sentinel, 01-92 = Periodensystem-Elemente (1=H, 2=He, ..., 92=U)
- Element-Symbol → erster Buchstabe = BURUMUT-Zeichen

Input: bbox/v9_reproduction_20260706/wikia_v9_knowledge.json
Output: bbox/v9_reproduction_20260706/burumut_decoded.json
"""
import json
from pathlib import Path
from datetime import datetime
import re
from decimal import Decimal, getcontext
getcontext().prec = 200  # High precision for long periods

# Element symbols (1-92)
ELEMENTS = {
    1: "H", 2: "He", 3: "Li", 4: "Be", 5: "B", 6: "C", 7: "N", 8: "O",
    9: "F", 10: "Ne", 11: "Na", 12: "Mg", 13: "Al", 14: "Si", 15: "P",
    16: "S", 17: "Cl", 18: "Ar", 19: "K", 20: "Ca", 21: "Sc", 22: "Ti",
    23: "V", 24: "Cr", 25: "Mn", 26: "Fe", 27: "Co", 28: "Ni", 29: "Cu",
    30: "Zn", 31: "Ga", 32: "Ge", 33: "As", 34: "Se", 35: "Br", 36: "Kr",
    37: "Rb", 38: "Sr", 39: "Y", 40: "Zr", 41: "Nb", 42: "Mo", 43: "Tc",
    44: "Ru", 45: "Rh", 46: "Pd", 47: "Ag", 48: "Cd", 49: "In", 50: "Sn",
    51: "Sb", 52: "Te", 53: "I", 54: "Xe", 55: "Cs", 56: "Ba", 57: "La",
    58: "Ce", 59: "Pr", 60: "Nd", 61: "Pm", 62: "Sm", 63: "Eu", 64: "Gd",
    65: "Tb", 66: "Dy", 67: "Ho", 68: "Er", 69: "Tm", 70: "Yb", 71: "Lu",
    72: "Hf", 73: "Ta", 74: "W", 75: "Re", 76: "Os", 77: "Ir", 78: "Pt",
    79: "Au", 80: "Hg", 81: "Tl", 82: "Pb", 83: "Bi", 84: "Po", 85: "At",
    86: "Rn", 87: "Fr", 88: "Ra", 89: "Ac", 90: "Th", 91: "Pa", 92: "U"
}


def parse_factor_expression(expr):
    """Parse '2^5 * 13 * 37 * 179 * 471077143' into number"""
    if not expr:
        return None
    # Remove whitespace
    expr = expr.replace(" ", "").replace("\n", "")
    # Split by *
    parts = expr.split("*")
    result = 1
    for part in parts:
        part = part.strip()
        if not part:
            continue
        if "^" in part:
            base, exp = part.split("^")
            result *= int(base) ** int(exp)
        else:
            result *= int(part)
    return result


def get_period(numerator, denominator, max_period=80):
    """Extract period of decimal expansion numerator/denominator"""
    if denominator == 0 or numerator == 0:
        return ""
    # Use Decimal for high precision
    try:
        d = Decimal(numerator) / Decimal(denominator)
    except Exception:
        return ""
    s = str(d)
    if "." not in s:
        return ""
    decimals = s.split(".")[1]
    # Find period: smallest repeating block
    if len(decimals) < 2:
        return decimals
    for period_len in range(1, min(len(decimals)//2 + 1, max_period) + 1):
        candidate = decimals[:period_len]
        # Check if it repeats
        is_periodic = True
        # Allow 2-3 non-repeating prefix digits
        prefix_len = 0
        for p_len in [0, 1, 2, 3]:
            test = decimals[p_len:]
            if len(test) < period_len * 2:
                continue
            if all(test[i:i+period_len] == candidate for i in range(0, min(len(test), period_len * 4), period_len)):
                prefix_len = p_len
                break
        # Simple check: first 6 repetitions
        is_repeating = True
        for rep in range(1, 6):
            start = rep * period_len
            if start + period_len > len(decimals):
                break
            if decimals[start:start + period_len] != candidate:
                is_repeating = False
                break
        if is_repeating:
            return candidate
    return ""


def dinomes_to_letters(period, n_atoms=None):
    """Convert period (string of digits) to letters via element symbols.

    Rules (per Schmeh):
    - Take period in groups of 2 digits (00-99)
    - If n_atoms is set, take only first n_atoms pairs
    - 00 = ignore (sentinel or space)
    - 01-92 = element symbol, take first letter
    - 93-99 = ignore (too heavy)
    """
    # Pad period to even length
    if len(period) % 2 == 1:
        period = "0" + period

    letters = []
    pairs = [period[i:i+2] for i in range(0, len(period), 2)]
    if n_atoms:
        pairs = pairs[:n_atoms]
    for p in pairs:
        try:
            n = int(p)
        except ValueError:
            letters.append("?")
            continue
        if n == 0:
            letters.append("_")  # sentinel
        elif 1 <= n <= 92:
            letters.append(ELEMENTS[n][0])
        else:
            letters.append("?")
    return "".join(letters)


def main():
    print("=" * 80)
    print("V9 PHASE 1: BURUMUT-DEKODIERUNG ALLER FAKTORZERLEGUNGEN")
    print("=" * 80)

    knowledge = json.load(open("bbox/v9_reproduction_20260706/wikia_v9_knowledge.json"))
    fractions = knowledge["fractions"]

    decoded = {
        "metadata": {
            "phase": "V9 / Phase 1",
            "datum": datetime.now().isoformat(),
            "method": "dcode.fr atomic-number-substitution (00=sentinel, 01-92=element first letter)",
        },
        "pages": {},
    }

    for page_id, pairs in fractions.items():
        decoded["pages"][page_id] = []
        for i, pair in enumerate(pairs):
            num_expr = pair["num"]
            den_expr = pair["den"]
            result = {
                "pair_idx": i,
                "num_expr": num_expr,
                "den_expr": den_expr,
            }
            if not num_expr:
                continue
            try:
                num = parse_factor_expression(num_expr)
                result["num_value"] = str(num)
                if den_expr:
                    den = parse_factor_expression(den_expr)
                    result["den_value"] = str(den)
                    if den and den != 0:
                        period = get_period(num, den)
                        result["period"] = period
                        if period:
                            # Try 22, 23, 14, 15 atoms (Wikia mentions 22/23, Tappeiner 14/15)
                            result["22_atoms"] = dinomes_to_letters(period, 22)
                            result["23_atoms"] = dinomes_to_letters(period, 23)
                            result["14_atoms"] = dinomes_to_letters(period, 14)
                            result["15_atoms"] = dinomes_to_letters(period, 15)
                            result["n_period_digits"] = len(period)
                else:
                    # Single number (no denominator) - check if it's a period itself
                    result["single_value"] = str(num)
                    period_str = str(num)
                    if len(period_str) >= 22:
                        result["22_atoms"] = dinomes_to_letters(period_str, 22)
                        result["23_atoms"] = dinomes_to_letters(period_str, 23)
            except Exception as e:
                result["error"] = str(e)
            decoded["pages"][page_id].append(result)

    # Save
    out_path = Path("bbox/v9_reproduction_20260706/burumut_decoded.json")
    with open(out_path, "w") as f:
        json.dump(decoded, f, indent=2, ensure_ascii=False)

    # Print sample
    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n{'='*80}")
    print("BEISPIELE (erste 3 Paare pro Seite):")
    for pg in sorted(decoded["pages"].keys()):
        print(f"\n=== {pg} ===")
        for entry in decoded["pages"][pg][:3]:
            if "error" in entry:
                print(f"  [{entry['pair_idx']}] ERROR: {entry['error']}")
                continue
            if "period" in entry:
                print(f"  [{entry['pair_idx']}] {entry['num_expr'][:40]} / {entry['den_expr'][:30]}")
                print(f"     period ({entry['n_period_digits']}d): {entry['period']}")
                print(f"     22 atoms: {entry.get('22_atoms', '?')}")
                print(f"     23 atoms: {entry.get('23_atoms', '?')}")
                print(f"     14 atoms: {entry.get('14_atoms', '?')}")
                print(f"     15 atoms: {entry.get('15_atoms', '?')}")
            else:
                print(f"  [{entry['pair_idx']}] {entry.get('num_expr', '?')[:40]}")


if __name__ == "__main__":
    main()
