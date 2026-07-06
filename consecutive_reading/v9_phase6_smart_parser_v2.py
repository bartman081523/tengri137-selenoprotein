"""
v9_phase6_smart_parser_v2.py
V9 Phase 6 — Smart Fraction Parser v2 (korrekte Aufteilung)

Versteht die Schmeh-Faktorzerlegungs-Struktur:
- Jeder Chunk (zwischen 20+ dashes) enthält 1 oder 2 Expressions
- Expressions in einem Chunk sind durch Whitespace getrennt
- Trennstelle: " <Zahl>" wo das vorherige Zeichen NICHT '*' ist
  (d.h. das " * " zwischen Faktoren bleibt, aber " " zwischen Expressions bricht)
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
    91:'Pa', 92:'U',
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


def parse_chunk_expressions(chunk_text):
    """Split a chunk into 1 or 2 expressions.
    Boundary: space NOT between digits AND NOT after '*' (since '* <num>' is part of expression).
    The pattern is: <num>( * <num>)* <space> <digit_start_of_new_expr>
    """
    # Find positions where a space is followed by a digit and the char before is NOT '*'
    # We can use lookbehind: split on " " preceded by something other than '*'
    parts = re.split(r'(?<=[^*]) (?=\d)', chunk_text)
    return [p.strip() for p in parts if p.strip()]


def parse_fractions_smart(text):
    """Parse p17-p23 factorizations correctly."""
    # Step 1: Split on 20+ dash sequence
    raw_chunks = re.split(r'-{20,}', text)
    chunks = [c.strip() for c in raw_chunks if c.strip()]

    # Step 2: For each chunk, extract 1-2 expressions
    expressions = []
    for c in chunks:
        # First split on newlines (some chunks have multi-line content)
        sub_chunks = re.split(r'\n+', c)
        for sc in sub_chunks:
            sc = sc.strip()
            if not sc:
                continue
            parts = parse_chunk_expressions(sc)
            expressions.extend(parts)

    # Step 3: Filter non-fraction expressions (English, magic square)
    fraction_exprs = []
    for e in expressions:
        # English text (multiple uppercase words)
        if re.search(r'\b[A-Z]{2,}\s+[A-Z]{2,}', e):
            continue
        # Magic square (long single-word without digits, mostly letters)
        if not any(c.isdigit() for c in e) and len(e) > 30 and e.isalpha():
            continue
        fraction_exprs.append(e)

    # Step 4: Pair them as (num, den)
    fractions = []
    for i in range(0, len(fraction_exprs) - 1, 2):
        fractions.append({"num": fraction_exprs[i], "den": fraction_exprs[i+1]})
    if len(fraction_exprs) % 2 == 1:
        fractions.append({"num": fraction_exprs[-1], "den": None})

    return fractions


def main():
    print("=" * 80)
    print("V9 PHASE 6: SMART FRACTION PARSER V2 — KORREKTE DEKODIERUNG")
    print("=" * 80)

    knowledge = json.load(open("/run/media/julian/ML4/tengri137/original_sources/wikia/wikia_complete_knowledge.json"))

    decoded = {
        "metadata": {
            "phase": "V9 / Phase 6",
            "datum": datetime.now().isoformat(),
            "method": "Smart parser v2 + dcode.fr",
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
                if num is not None:
                    entry["num_value"] = str(num)[:30] + ("..." if len(str(num)) > 30 else "")
                if den_expr:
                    den = parse_factor_expression(den_expr)
                    if den is not None:
                        entry["den_value"] = str(den)[:30] + ("..." if len(str(den)) > 30 else "")
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

    out_path = OUT_DIR / "burumut_decoded_v2.json"
    with open(out_path, "w") as f:
        json.dump(decoded, f, indent=2, ensure_ascii=False)

    # Vergleiche mit V7 Tappeiner-Ground-Truth
    tappeiner = json.load(open("bbox/burumut_20260707_V7/burumut_texts.json"))["burumut_texts"]

    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n{'='*80}")
    print("STATISTIK")
    print("=" * 80)
    for pg, entries in decoded["pages"].items():
        n_total = len(entries)
        n_with_period = sum(1 for e in entries if "period" in e)
        print(f"  {pg}: {n_total} fractions, {n_with_period} with valid period")

    print(f"\n{'='*80}")
    print("P17 ERSTE 6 FRACTIONS (VALIDIERUNG GEGEN TAPPEINER)")
    print("=" * 80)
    p17 = decoded["pages"].get("p17", [])
    for i, entry in enumerate(p17[:6]):
        num = entry.get('num_expr', '?')[:30]
        den = entry.get('den_expr', '?')[:30] if entry.get('den_expr') else 'None'
        print(f"\n  [{i}]")
        print(f"      num: {num!r}")
        print(f"      den: {den!r}")
        if 'period' in entry:
            print(f"      period ({entry['n_period_digits']}d): {entry['period'][:50]}")
            print(f"      22 atoms: {entry['22_atoms']}")
        elif 'error' in entry:
            print(f"      ERROR: {entry['error']}")

    # p23 Spezial
    print(f"\n{'='*80}")
    print("P23 SPEZIAL")
    print("=" * 80)
    p23 = decoded["pages"].get("p23", [])
    for i, entry in enumerate(p23):
        if 'period' in entry:
            print(f"  [{i}] {entry['n_period_digits']}d period: {entry['period'][:60]}")
            print(f"      22 atoms: {entry['22_atoms']}")


if __name__ == "__main__":
    main()
