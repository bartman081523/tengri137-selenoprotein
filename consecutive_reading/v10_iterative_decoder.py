"""
v10_iterative_decoder.py
V10 Phase 2 — Iterative Glyph→Englisch-Decoder

Korrekte Strategie:
1. Tengri ist right-to-left (Wikia)
2. A=E: gleiche Glyphe für A und E (Wikia-Regel)
3. K=H: K=Glyph(H) (Wikia-Regel)
4. B=V: B=Glyph(V) (Wikia-Regel)
5. P=F: P=Glyph(F) (Wikia-Regel)
6. Schmeh-Plaintext ist Ground Truth (Wikia-Übersetzung)

Methode:
- Iterative Constraint-Satisfaction
- Starte mit Frequenz-Mapping
- Wende Wikia-Regeln als Constraints an
- Validiere gegen Schmeh-Plaintext
- Refine iterativ
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter
from itertools import permutations

OUT_DIR = Path("bbox/v10_decoder_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# V6 Heuristiken (aus glyphs_final.json)
V6_HEURISTICS = {
    "G01": "J", "G02": ")", "G03": "P", "G04": "F", "G05": "I",
    "G06": "E", "G07": "N", "G08": "H", "G09": "?", "G10": "?",
    "G11": "?", "G12": "S", "G13": "?", "G14": "?", "G15": "H",
    "G16": "?", "G17": "D", "G18": "F", "G19": "?", "G20": "?",
    "G21": "?", "G22": "?", "G23": "?", "G24": "?", "G25": "G25",
    "G26": "?", "G27": "?", "G28": "?", "G29": "?", "G30": "?",
}

# Wikia-Regeln (gleiche Glyphe für mehrere Buchstaben)
WIKIA_EQUIVALENCES = [
    ("A", "E"),  # A und E gleiche Rune
    ("K", "H"),  # K für H
    ("B", "V"),  # B für V
    ("P", "F"),  # P für F
]

# Mögliche Mapping-Kandidaten pro Glyph
# Basierend auf Heuristik + Frequenz + Wikia-Regeln
GLYPH_CANDIDATES = {
    "G01": ["J", "L", "Y", "C", "M"],  # J-Heuristik, 30 freq
    "G02": ["L", "Y", "B", "C", "J"],  # )-Heuristik, 17 freq (selten)
    "G03": ["P", "B", "F"],  # P-Heuristik, 73 freq
    "G05": ["I", "Y", "L"],  # I-Heuristik, 77 freq
    "G06": ["E", "A"],  # E-Heuristik, 40 freq + A=E-Regel
    "G07": ["N", "M"],  # N-Heuristik, 50 freq
    "G08": ["H", "K"],  # H-Heuristik, 11 freq + K=H-Regel
    "G09": ["O", "Q", "D"],  # 43 freq
    "G10": ["R", "L"],  # 52 freq
    "G11": ["U", "V", "W"],  # 17 freq
    "G14": ["S", "Z"],  # 39 freq
    "G17": ["D", "B", "V"],  # D-Heuristik, 17 freq + B=V-Regel
    "G18": ["F", "P"],  # F-Heuristik, 126 freq + P=F-Regel
    "G19": ["T", "L", "M"],  # 121 freq
    "G24": ["X", "Q", "Z"],  # sehr selten
    "G25": [" "],  # G25 ist Trenner (V6 Befund)
    "G29": ["A", "E", "O"],  # 106 freq
}


def load_v6_tokens():
    tokens = {}
    token_dir = Path("bbox/tokenstream_20260706_V6_v3_17glyphs")
    for p in range(1, 17):
        f = token_dir / f"p{p:02d}.json"
        if f.exists():
            data = json.load(open(f))
            tokens[f"p{p:02d}"] = data.get("tokens", [])
    return tokens


def load_wikia():
    return json.load(open("bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json"))["page_blocks"]


def decode_rtl(glyph_seq, mapping, separator=" "):
    """Decode right-to-left, G25 = separator"""
    result = []
    for g in reversed(glyph_seq):
        if g == "G25":
            if result and result[-1] != separator:
                result.append(separator)
        else:
            result.append(mapping.get(g, "?"))
    text = "".join(result).strip()
    # Cleanup: remove consecutive separators
    text = re.sub(r'\s+', ' ', text)
    return text


def score_against_plaintext(decoded, plaintext):
    """Score how well decoded matches Schmeh's plaintext"""
    # Convert both to word sets
    dec_words = set(w.upper() for w in re.findall(r'\b[A-Z]+\b', decoded.upper()))
    plain_words = set(w.upper() for w in re.findall(r'\b[A-Z]+\b', plaintext.upper()))

    if not dec_words:
        return 0.0

    # Score = intersection / union
    intersection = dec_words & plain_words
    return len(intersection) / len(dec_words) if dec_words else 0.0


def try_mapping(mapping, tokens, wikia):
    """Test mapping against all pages with Wikia plaintext"""
    total_score = 0.0
    n_pages = 0
    for page_id, page_tokens in tokens.items():
        if page_id in wikia:
            seq = [t.get("glyph_id", "?") for t in page_tokens]
            decoded = decode_rtl(seq, mapping)
            score = score_against_plaintext(decoded, wikia[page_id])
            total_score += score
            n_pages += 1
    return total_score / n_pages if n_pages else 0.0


def gen_mappings(constraints):
    """Generate all possible mappings respecting constraints"""
    # constraints: dict of {glyph: fixed_letter}
    # Variable glyphs are those not in constraints
    var_glyphs = [g for g in GLYPH_CANDIDATES if g not in constraints]
    var_letters_pool = set()
    for g in GLYPH_CANDIDATES:
        if g not in constraints:
            var_letters_pool.update(GLYPH_CANDIDATES[g])
    # Letters already used by constraints
    used_letters = set(constraints.values())
    available_letters = sorted(var_letters_pool - used_letters)
    # If too many or too few letters, skip
    if len(available_letters) < len(var_glyphs):
        return
    # Permutations of len(var_glyphs) letters from available_letters
    for perm in permutations(available_letters, len(var_glyphs)):
        m = dict(constraints)
        for g, l in zip(var_glyphs, perm):
            m[g] = l
        yield m


def main():
    print("=" * 80)
    print("V10 PHASE 2: ITERATIVE GLYPH→ENGLISCH DECODER")
    print("=" * 80)

    tokens = load_v6_tokens()
    wikia = load_wikia()

    print(f"\n  Pages with tokens: {list(tokens.keys())[:5]}...")
    print(f"  Pages with Wikia: {list(wikia.keys())[:5]}...")

    # Wikia "For beginners" Constraints (anwenden)
    print(f"\n{'='*80}")
    print("WIKIA-CONSTRAINTS (For beginners)")
    print("=" * 80)
    print("  A=E: G06 deckt A und E ab (gleiche Glyphe)")
    print("  K=H: G08 deckt K und H ab")
    print("  B=V: G17 deckt B und V ab (Heuristik D + Wikia-Regel)")
    print("  P=F: G18 deckt P und F ab")

    # Start: Wikia + Heuristik Constraints
    fixed = {
        "G06": "E",  # A=E: G06 deckt A und E
        "G08": "H",  # K=H: G08 deckt K und H
        "G17": "B",  # B=V: G17 deckt B und V (Heuristik D, aber B+V sind gleich)
        "G18": "F",  # P=F: G18 deckt P und F
        "G05": "I",  # Heuristik
        "G07": "N",  # Heuristik
    }

    print(f"\n  FIXED CONSTRAINTS: {fixed}")

    # Test initial mapping
    print(f"\n{'='*80}")
    print("INITIAL MAPPING TEST")
    print("=" * 80)
    p10_seq = [t.get("glyph_id", "?") for t in tokens["p10"]]
    p10_decoded = decode_rtl(p10_seq, fixed)
    print(f"\n  p10 decoded: {p10_decoded[:200]}")
    print(f"  p10 wikia:   {wikia['p10'][:200]}")
    print(f"  p10 score:   {score_against_plaintext(p10_decoded, wikia['p10']):.3f}")

    # Generiere alle Mappings (Wikia-Constraints)
    print(f"\n{'='*80}")
    print("BRUTE-FORCE: ALLE MAPPINGS TESTEN")
    print("=" * 80)
    print(f"  Fixed: {len(fixed)} Glyphen")
    print(f"  Variable: {len(GLYPH_CANDIDATES) - len(fixed)} Glyphen")
    print(f"  Teste alle Permutationen...")

    best_mapping = None
    best_score = 0.0
    n_tested = 0

    # Teste nur die vielversprechendsten Mappings (Top-Kandidaten pro Glyph)
    # Berechne Permutations-Budget
    var_glyphs = [g for g in GLYPH_CANDIDATES if g not in fixed]
    var_letters_pool = set()
    for g in var_glyphs:
        var_letters_pool.update(GLYPH_CANDIDATES[g])
    used = set(fixed.values())
    available = sorted(var_letters_pool - used)
    print(f"  Available letters: {len(available)} ({''.join(available)})")
    print(f"  Variable glyphs: {len(var_glyphs)}")

    # Zähle: permutations(len(available), len(var_glyphs))
    from math import perm
    n_perms = perm(len(available), len(var_glyphs))
    print(f"  Permutations: {n_perms:,}")

    # Zu viele Permutationen? Reduziere auf Top-2-Kandidaten pro Variable
    if n_perms > 100000:
        print("  → Zu viele Permutationen, teste nur Top-2-Kandidaten pro Variable")
        reduced_candidates = {g: GLYPH_CANDIDATES[g][:2] for g in var_glyphs}
        # Recompute
        var_letters_pool = set()
        for g in var_glyphs:
            var_letters_pool.update(reduced_candidates[g])
        available = sorted(var_letters_pool - used)
        print(f"  Reduced available: {len(available)}")
        n_perms = perm(len(available), len(var_glyphs))
        print(f"  Reduced permutations: {n_perms:,}")

    # Teste alle
    for mapping in gen_mappings(fixed):
        n_tested += 1
        if n_tested > 100000:
            print(f"  → Abbruch bei {n_tested} Tests")
            break
        score = try_mapping(mapping, tokens, wikia)
        if score > best_score:
            best_score = score
            best_mapping = dict(mapping)
            if n_tested < 100 or n_tested % 1000 == 0:
                print(f"  [{n_tested}] New best: {score:.3f}")
                # Print decoded p10
                p10_dec = decode_rtl(p10_seq, best_mapping)
                print(f"    p10: {p10_dec[:150]}")
                print(f"    wikia: {wikia['p10'][:150]}")

    print(f"\n{'='*80}")
    print(f"BESTES MAPPING (Score {best_score:.3f})")
    print("=" * 80)
    if best_mapping:
        for g in sorted(best_mapping.keys()):
            print(f"  {g} → '{best_mapping[g]}'")
        # Test alle Seiten
        for page_id in ["p01", "p07", "p08", "p10"]:
            if page_id in tokens:
                seq = [t.get("glyph_id", "?") for t in tokens[page_id]]
                decoded = decode_rtl(seq, best_mapping)
                print(f"\n  {page_id} decoded: {decoded[:200]}")
                if page_id in wikia:
                    print(f"  {page_id} wikia:   {wikia[page_id][:200]}")
                    print(f"  {page_id} score:   {score_against_plaintext(decoded, wikia[page_id]):.3f}")

        # Speichere
        out_path = OUT_DIR / "best_mapping.json"
        with open(out_path, "w") as f:
            json.dump({
                "metadata": {
                    "phase": "V10 / Brute-Force Mapping",
                    "datum": datetime.now().isoformat(),
                    "best_score": best_score,
                    "n_tested": n_tested,
                    "method": "Frequency + Wikia + V6 Heuristik Constraints",
                },
                "best_mapping": best_mapping,
                "n_pages_tested": len([p for p in tokens if p in wikia]),
            }, f, indent=2, ensure_ascii=False)
        print(f"\n✓ Best mapping: {out_path}")


if __name__ == "__main__":
    main()
