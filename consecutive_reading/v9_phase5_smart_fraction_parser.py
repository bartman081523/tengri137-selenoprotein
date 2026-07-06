"""
v9_phase5_smart_fraction_parser.py
V9 Phase 5 — Smart Fraction Parser für p17-p23

Versteht die Schmeh-Faktorzerlegungs-Struktur:
- 30-Dash: num/den Separator (innerhalb einer Gruppe)
- 60-Dash: Gruppe-Separator (zwischen Brüchen)
- Innerhalb einer Gruppe: 2 Brüche (F1, F2)
- Insgesamt: 11 Brüche × 2 (num+den) = 22 Elemente

Beispiel p17 Gruppe 1:
  F1 num: 2^5 * 13 * 37 * 179 * 471077143
  30-dash
  F1 den: 23 * 53 * 2711 * 897232321
  F2 num: 307 * 1481 * 10873297429171343046
  60-dash (group end)
  F2 den: 7 * 17780871841855257950191971103144880245068986055043

Wait — looking at the data more carefully, the 60-dash is BEFORE the F2 den, so the F1 num+den come FIRST, then a 30-dash, then F2 num, then 60-dash, then F2 den. Actually the structure is:

F1 num / 30-dash / F1 den | F2 num / 30-dash / F2 den

But the 30-dashes count is 20 not 22 (11 fractions × 2). So 2 fractions are missing their 30-dash. Those are the "implicit" num/den transitions.

Let me just split on ANY dash separator and alternate num/den based on count parity.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from decimal import Decimal, getcontext
getcontext().prec = 200

OUT_DIR = Path("bbox/v9_reproduction_20260706")

PERIODIC = {
    1:'H', 2:'He', 3:'Li', 4:'Be', 5:'B', 6:'C', 7:'N', 8:'O', 9:'F', 10:'Ne',
    11:'Na', 12:'Mg', 13:'Al', 14:'Si', 15:'P', 16:'S', 17:'Cl', 18:'Ar', 19:'K', 20:'Ca',
    21:'Sc', 22:'Ti', 23:'V', 24:'Cr', 25:'Mn', 26:'Fe', 27:'Co', 28:'Ni', 29:'Cu', 30:'Zn',
    31:'Ga', 32:'Ge', 33:'As', 34:'Se', 35:'Br', 36:'Kr', 37:'Rb', 38:'Sr', 39:'Y', 40:'Zr',
    41:'Nb', 42:'Mo', 43:'Tc', 44:'Ru', 45:'Rh', 46:'Pd', 47:'Ag', 48:'Cd', 49:'In', 50:'Sn',
    51:'Sb', 52:'Te', 53:'I', 54:'Xe', 55:'Cs', 56:'Ba', 57:'La', 58:'Ce', 59:'Pr', 60:'Nd',
    61:'Pm', 62:'Sm', 63:'Eu', 64:'Gd', 65:'Tb', 66:'Dy', 67:'Ho', 68:'Er', 69:'Tm', 70:'Yb',
    71:'Lu', 72:'Hf', 73:'Ta', 74:'W', 75:'Re', 76:'Os', 77:'Ir', 78:'Pt', 79:'Au', 80:'Hg',
    81:'Tl', 82:'Pb', 83:'Bi', 84:'Po', 85:'At', 86:'Rn', 87:'Fr', 88:'Ra', 89:'Ac', 90:'Th',
    91:'Pa', 92:'U', 93:'Np', 94:'Pu', 95:'Am', 96:'Cm', 97:'Bk', 98:'Cf', 99:'Es', 100:'Fm',
    101:'Md', 102:'No', 103:'Lr', 104:'Rf', 105:'Db', 106:'Sg', 107:'Bh', 108:'Hs', 109:'Mt', 110:'Ds',
    111:'Rg', 112:'Cn', 113:'Nh', 114:'Fl', 115:'Mc', 116:'Lv', 117:'Ts', 118:'Og',
}


def parse_factor_expression(expr):
    if not expr:
        return None
    expr = expr.replace(" ", "").replace("\n", "")
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
            try:
                result *= int(part)
            except ValueError:
                return None
    return result


def get_period(num, den, max_period=80):
    if num == 0 or den == 0:
        return ""
    try:
        d = Decimal(num) / Decimal(den)
    except Exception:
        return ""
    s = str(d)
    if "." not in s:
        return ""
    decimals = s.split(".")[1]
    if len(decimals) < 2:
        return decimals
    for period_len in range(1, min(len(decimals)//2 + 1, max_period) + 1):
        candidate = decimals[:period_len]
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
    if len(period) % 2 == 1:
        period = "0" + period
    pairs = [period[i:i+2] for i in range(0, len(period), 2)]
    if n_atoms:
        pairs = pairs[:n_atoms]
    letters = []
    for p in pairs:
        try:
            n = int(p)
        except ValueError:
            letters.append("?")
            continue
        if n == 0:
            letters.append("_")
        elif 1 <= n <= 92:
            letters.append(PERIODIC[n][0])
        else:
            letters.append("?")
    return "".join(letters)


def parse_fractions_smart(text):
    """
    Smart parser: Each chunk (between 20+ dashes) has 1 or 2 expressions
    (separated by space within the chunk, not by newline).

    The pattern is:
    - Chunk 0: F1 num (alone, 1 expression)
    - Chunk 1: F1 den + F2 num (2 expressions, space-separated)
    - Chunk 2: F2 den + F3 num (2 expressions)
    - ...
    - Chunk 15: F10 num + F10 den (2 expressions)? No wait
    - Chunk N: 2 expressions
    - Last chunk: F11 den (alone, 1 expression)

    Total: ~17 chunks → 11 fractions × 2 = 22 expressions
    Remaining: 6 English translations + 1 magic square = 7 non-fraction chunks
    """
    # Split on 20+ dash sequence
    raw_chunks = re.split(r'-{20,}', text)
    chunks = [c.strip() for c in raw_chunks if c.strip()]

    # Each chunk has 1 or 2 expressions separated by spaces
    expressions = []
    for c in chunks:
        # Split on newline first, then merge
        lines = [l.strip() for l in c.split('\n') if l.strip()]
        # If chunk has only 1 line, it may have 2 expressions separated by spaces
        # If chunk has 2 lines, each is one expression
        if len(lines) == 1:
            # Try to split into 2 expressions: detect " * " pattern
            # Expressions typically end with a number (no *), then " * " or "  " separates
            line = lines[0]
            # Find positions where " " precedes a number (digit) after a *
            # Simple heuristic: find pattern of "X * Y" then "Z" where Z starts a new expression
            # For now: split on double space
            parts = re.split(r'\s\s+', line)
            if len(parts) == 2:
                expressions.extend(parts)
            else:
                expressions.append(line)
        else:
            expressions.extend(lines)

    # Now we have ~24-30 expressions. Filter non-fraction expressions (English, magic square)
    # Fractions contain "*" or "^" or are pure digits
    # English translations contain words
    fraction_exprs = []
    for e in expressions:
        # If it has letters outside math symbols, it's English
        # Otherwise it's a fraction expression
        # Remove spaces, check if it's " * " separated digits
        if re.search(r'\b[A-Z]{2,}\b', e) and not re.search(r'\^', e):
            # English text (e.g., "TIME FOR THE TRUTH")
            continue
        if 'A' in e and 'B' in e and 'C' in e and 'D' in e and not any(c.isdigit() for c in e):
            # Magic square (e.g., "UTMAFERTUMURUB...")
            continue
        fraction_exprs.append(e)

    # Now pair them: F1 num, F1 den, F2 num, F2 den, ...
    fractions = []
    for i in range(0, len(fraction_exprs) - 1, 2):
        fractions.append({"num": fraction_exprs[i], "den": fraction_exprs[i+1]})
    if len(fraction_exprs) % 2 == 1:
        fractions.append({"num": fraction_exprs[-1], "den": None})

    return fractions


def main():
    print("=" * 80)
    print("V9 PHASE 5: SMART FRACTION PARSER — KORREKTE p17-p23 DEKODIERUNG")
    print("=" * 80)

    knowledge = json.load(open("/run/media/julian/ML4/tengri137/original_sources/wikia/wikia_complete_knowledge.json"))

    decoded = {
        "metadata": {
            "phase": "V9 / Phase 5",
            "datum": datetime.now().isoformat(),
            "method": "Smart parser + dcode.fr atomic-number-substitution",
            "n_fractions_expected": 11,
        },
        "pages": {},
    }

    for page_key in ["017", "018", "019", "020", "021", "022", "023"]:
        if page_key not in knowledge:
            continue
        text = knowledge[page_key].get("plaintext", "")
        fractions = parse_fractions_smart(text)
        page_id = "p" + page_key.lstrip("0")

        decoded["pages"][page_id] = []
        for i, fr in enumerate(fractions):
            num_expr = fr["num"]
            den_expr = fr.get("den")
            entry = {
                "fraction_idx": i,
                "num_expr": num_expr[:80] if num_expr else None,
                "den_expr": den_expr[:80] if den_expr else None,
            }
            if not num_expr:
                continue
            try:
                num = parse_factor_expression(num_expr)
                entry["num_value"] = str(num)[:30] + "..." if num and len(str(num)) > 30 else str(num)
                if den_expr:
                    den = parse_factor_expression(den_expr)
                    entry["den_value"] = str(den)[:30] + "..." if den and len(str(den)) > 30 else str(den)
                    if num and den:
                        period = get_period(num, den)
                        if period:
                            entry["period"] = period
                            entry["n_period_digits"] = len(period)
                            entry["22_atoms"] = dinomes_to_letters(period, 22)
                            entry["23_atoms"] = dinomes_to_letters(period, 23)
                            entry["14_atoms"] = dinomes_to_letters(period, 14)
            except Exception as e:
                entry["error"] = str(e)
            decoded["pages"][page_id].append(entry)

    out_path = OUT_DIR / "burumut_decoded_smart.json"
    with open(out_path, "w") as f:
        json.dump(decoded, f, indent=2, ensure_ascii=False)

    # Vergleiche mit V7 Tappeiner-Ground-Truth
    tappeiner = json.load(open("bbox/burumut_20260707_V7/burumut_texts.json"))["burumut_texts"]

    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n{'='*80}")
    print("SMART-PARSE STATISTIK")
    print("=" * 80)
    for pg, entries in decoded["pages"].items():
        n_total = len(entries)
        n_with_period = sum(1 for e in entries if "period" in e)
        print(f"  {pg}: {n_total} fractions, {n_with_period} with valid period")

    print(f"\n{'='*80}")
    print("P17 — VERGLEICH MIT TAPPEINER GROUND TRUTH")
    print("=" * 80)
    p17 = decoded["pages"].get("p017", [])
    print(f"V9 Smart Parser: {len(p17)} fractions")
    print(f"V7 Tappeiner: {len(tappeiner)} fractions (mit 7 Perioden pro Bruch = 77 Texte)")
    print()
    for i, entry in enumerate(p17[:6]):
        period_short = entry.get('period', '?')[:40]
        atoms_22 = entry.get('22_atoms', '?')[:30]
        print(f"  [{i}] num={entry['num_expr'][:30]!r:<30} den={entry.get('den_expr', '?')[:30]!r:<30}")
        if 'period' in entry:
            print(f"      period ({entry['n_period_digits']}d): {period_short}...")
            print(f"      22 atoms: {atoms_22}")
        elif 'error' in entry:
            print(f"      ERROR: {entry['error']}")

    # p23 Spezial: 46-Periode-Check
    print(f"\n{'='*80}")
    print("P23 SPEZIAL: 46-PERIODE CHECK")
    print("=" * 80)
    p23 = decoded["pages"].get("p023", [])
    for i, entry in enumerate(p23):
        if 'period' in entry and entry['n_period_digits'] >= 40:
            print(f"  [{i}] {entry['n_period_digits']}d period (möglicher 46-Schmeh-Hinweis):")
            print(f"      period: {entry['period'][:60]}")
            print(f"      22 atoms: {entry['22_atoms']}")


if __name__ == "__main__":
    main()
