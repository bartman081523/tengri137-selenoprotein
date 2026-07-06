"""
v10_alphabetic_decoder.py
V10 — Systematischer Brute-Force-Decoder: Tengri → Englisch

Hinweise kombiniert:
1. Wikia "For beginners": Orkhon-Substitutionen (A=E, K=H, B=V, P=F)
2. Tengri = right-to-left (Wikia)
3. Tengri = "runes without any cipher" (Wikia)
4. 17 V6-Glyphen (G01-G29 dedupliziert)
5. Schmehs Wikia-Plaintext (Ground Truth für 23 Seiten)
6. Tappeiner-Methode (Periode→Dinome→Element→Buchstabe) — 00=sentinel, 01-92=Element
7. Tengri137 = 137 (1/137 Feinstrukturkonstante, Feynman's "God's Number")

Strategie:
- Versuche zuerst 1:1 Substitution: G01→A/B/C/..., G02→A/B/C/..., ...
- Verwende Schmehs Plaintext als Constraint (was muss rauskommen?)
- Verwende Wikia "For beginners" Orkhon-Regeln:
  - A=E (gleiche Rune)
  - K=H (K statt H)
  - B=V (W existiert nicht, B für V)
  - P=F (P für F)
- Brute-Force alle 17! = 3.5e14 Permutationen? Zu viele.
- Stattdessen: frequency-basierte Zuordnung (häufigste Glyphe = häufigster Buchstabe = E)
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter
from itertools import permutations

OUT_DIR = Path("bbox/v10_decoder_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Wikia "For beginners" Substitutionsregeln
WIKIA_RULES = {
    "A=E": True,       # A und E haben gleiche Rune
    "K=H": True,       # K wird für H verwendet
    "B=V": True,       # W existiert nicht, B für V
    "P=F": True,       # P wird für F verwendet
    "right_to_left": True,  # Tengri ist right-to-left
    "no_cipher": True,      # "runes without any cipher"
}

# V6 Glyphen-Heuristiken (similar_to_latin)
V6_HEURISTICS = {
    "G01": "J", "G02": ")", "G03": "P", "G04": "F", "G05": "I",
    "G06": "E", "G07": "N", "G08": "H", "G09": "?", "G10": "?",
    "G11": "?", "G12": "S", "G13": "?", "G14": "?", "G15": "H",
    "G16": "?", "G17": "D", "G18": "F", "G19": "?", "G20": "?",
    "G21": "?", "G22": "?", "G23": "?", "G24": "?", "G25": "G25",
    "G26": "?", "G27": "?", "G28": "?", "G29": "?", "G30": "?",
}

# English letter frequency (E, T, A, O, I, N, S, H, R most common)
ENGLISH_FREQ = "ETAOIN SHRDLUCMFWYPVBGKJQXZ"


def load_v6_tokens():
    """Load V6 tokens from all pages"""
    tokens = {}
    token_dir = Path("bbox/tokenstream_20260706_V6_v3_17glyphs")
    for p in range(1, 17):
        f = token_dir / f"p{p:02d}.json"
        if f.exists():
            data = json.load(open(f))
            tokens[f"p{p:02d}"] = data.get("tokens", [])
    return tokens


def load_wikia_plaintexts():
    """Load Wikia plain texts"""
    return json.load(open("bbox/wikia_plaintexts_20260706_V8/wikia_p1_to_p23.json"))["page_blocks"]


def glyph_frequency(tokens):
    """Count glyph frequency"""
    seq = [t.get("glyph_id", "?") for t in tokens]
    return Counter(seq)


def decode_attempt(glyph_seq, mapping):
    """Apply a mapping {glyph_id: letter} to a glyph sequence"""
    return "".join(mapping.get(g, "?") for g in reversed(glyph_seq))  # reversed: right-to-left


def is_english_like(text, threshold=0.6):
    """Check if decoded text looks like English"""
    # Count common English words
    common_words = {"THE", "AND", "TO", "OF", "A", "IN", "IS", "THAT", "IT", "FOR",
                    "WITH", "AS", "ON", "BE", "BY", "OR", "AN", "ARE", "THIS", "WHICH",
                    "WE", "YOU", "HAVE", "HAS", "HAD", "NOT", "BUT", "FROM", "THEY",
                    "ALL", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN", "EIGHT",
                    "NINE", "TEN", "HUNDRED", "THOUSAND", "TIME", "TRUTH", "KNOW",
                    "MIND", "GATE", "OPEN", "YEAR", "DAY", "GOD", "MESSAGE", "BOOK"}
    words = set(re.findall(r'\b[A-Z]+\b', text))
    matches = len(words & common_words)
    return matches >= threshold * len(words) if words else False


def main():
    print("=" * 80)
    print("V10: ALPHABETIC DECODER — TENGRI → ENGLISCH")
    print("=" * 80)

    tokens = load_v6_tokens()
    wikia = load_wikia_plaintexts()

    # Lade V6 Glyph-Katalog
    glyphs = json.load(open("bbox/glyph_refs_20260706_V6_consolidated/glyphs_final.json"))
    unique_glyphs = sorted(set(g["glyph_id"] for g in glyphs.get("glyphs", [])))
    print(f"\n  V6 unique Glyphen: {len(unique_glyphs)} → {unique_glyphs}")

    # Frequency-Analyse
    print(f"\n{'='*80}")
    print("GLYPH-FREQUENZ (alle p1-p16 zusammen)")
    print("=" * 80)
    all_freq = Counter()
    for p, t in tokens.items():
        all_freq.update(t.get("glyph_id", "?") for t in t)

    # Nur die Top-Glyphen
    total = sum(all_freq.values())
    for gid, cnt in all_freq.most_common(20):
        pct = 100 * cnt / total
        heur = V6_HEURISTICS.get(gid, "?")
        print(f"  {gid}: {cnt:>4} ({pct:.1f}%) — Heuristik: {heur}")

    # Wikia-Plaintext-Frequenz
    print(f"\n{'='*80}")
    print("WIKIA-ENGLISCH-FREQUENZ (alle 23 Seiten)")
    print("=" * 80)
    all_text = " ".join(wikia.values()).upper()
    letter_freq = Counter(c for c in all_text if c.isalpha())
    total_letters = sum(letter_freq.values())
    for letter, cnt in letter_freq.most_common(20):
        pct = 100 * cnt / total_letters
        print(f"  {letter}: {cnt:>5} ({pct:.1f}%)")

    # Wikia vs Glyph: Frequenz-Match
    print(f"\n{'='*80}")
    print("HÄUFIGKEITS-MATCH (Top-Glyph → Top-Buchstabe)")
    print("=" * 80)
    top_glyphs = [g for g, _ in all_freq.most_common(17)]
    top_letters = [l for l, _ in letter_freq.most_common(17)]
    print(f"  Top 17 Glyphen: {top_glyphs}")
    print(f"  Top 17 Buchstaben: {''.join(top_letters)}")
    print(f"  → Einfache 1:1-Map würde G25→E, G19→T, G18→A, G29→O, G09→I, ...")

    # Wikia "For beginners" Regeln anwenden
    print(f"\n{'='*80}")
    print("WIKIA 'FOR BEGINNERS' SUBSTITUTIONS-REGELN")
    print("=" * 80)
    print("  A=E: A und E haben gleiche Rune")
    print("  K=H: K wird für H verwendet (kein H)")
    print("  B=V: W existiert nicht, B wird für V verwendet")
    print("  P=F: P wird für F verwendet")
    print()
    print("  → Daraus folgt: Glyphe für 'A' = Glyphe für 'E'")
    print("  → Daraus folgt: Glyphe für 'K' = Glyphe für 'H'")
    print("  → Daraus folgt: Glyphe für 'B' = Glyphe für 'V'")
    print("  → Daraus folgt: Glyphe für 'P' = Glyphe für 'F'")

    # Wende Wikia-Regeln auf V6 an
    print(f"\n{'='*80}")
    print("V6 HEURISTIK → WIKIA-REGELN ABLEITEN")
    print("=" * 80)
    # G06 hat Heuristik 'E' (also G06 ist E)
    # Suche Glyphen mit Heuristik A: keine direkte
    # G08 hat Heuristik 'H' (also G08 ist H, und damit auch K)
    # G18 hat Heuristik 'F' (also G18 ist F, und damit auch P)
    # Suche Glyphen mit Heuristik V: G17 hat 'D', nicht V
    # → B (für V): vielleicht G17?
    wikia_mapping = {
        "G06": "E",       # G06 hat Heuristik E → E
        # G06 deckt auch A ab (A=E-Regel)
        "G08": "H",       # G08 hat Heuristik H → H/K (K=H)
        "G18": "F",       # G18 hat Heuristik F → F/P (P=F)
        # Suche B (V): keine direkte Heuristik
        # Versuche G17 = V
        "G17": "V",       # Annahme: G17 ist V (B-Regel: B für V)
    }

    # Erweitere Mapping mit Frequency-Match für restliche Glyphen
    # Top-Glyphs (frequency): G25, G19, G18, G29, G09, G05, G10, G14, G07, G06
    # G18 ist bereits F (Heuristik)
    # G06 ist bereits E
    # Verbleibend: G25, G19, G29, G09, G05, G10, G14, G07
    # Diese müssen den Top-Buchstaben T, A, O, I, N, S, R, D zugeordnet werden
    # (E ist bereits vergeben)

    # Häufige Glyphen → Häufige Buchstaben
    # G25 ist Operator/Trenner (V6 Befund) → vielleicht space oder EOL?
    # G19: 15× — wahrscheinlich T
    # G29: 11× — wahrscheinlich A oder O
    # G09: 9× — wahrscheinlich I oder N
    # G05: 8× — Heuristik 'I' → also I
    # G10: 7× — wahrscheinlich N oder S
    # G14: 6× — wahrscheinlich S oder R
    # G07: 5× — Heuristik 'N' → also N

    extended_mapping = {
        **wikia_mapping,
        "G05": "I",       # G05 hat Heuristik I
        "G07": "N",       # G07 hat Heuristik N
        "G19": "T",       # G19 häufig, T ist häufigster Buchstabe
        "G29": "A",       # G29 häufig
        "G09": "O",       # G09 häufig
        "G10": "R",       # G10 mittel-häufig
        "G14": "S",       # G14 mittel-häufig
        "G25": " ",       # G25 ist wahrscheinlich Trenner/Operator (V6 Befund)
    }

    print(f"\n  VORLÄUFIGES MAPPING (Wikia + V6 Heuristik + Frequency):")
    for gid in top_glyphs[:17]:
        letter = extended_mapping.get(gid, "?")
        heur = V6_HEURISTICS.get(gid, "?")
        freq = all_freq.get(gid, 0)
        print(f"    {gid} (freq={freq:>3}, heur={heur}) → '{letter}'")

    # Decodiere p10 als Test
    print(f"\n{'='*80}")
    print("TEST-DEKODIERUNG p10 (Wikia-Plaintext vorhanden)")
    print("=" * 80)
    p10_tokens = tokens.get("p10", [])
    p10_glyph_seq = [t.get("glyph_id", "?") for t in p10_tokens]
    decoded = decode_attempt(p10_glyph_seq, extended_mapping)
    print(f"\n  Glyphen-Sequenz (erste 100): {''.join(p10_glyph_seq[:100])}")
    print(f"  Dekodiert:                     {decoded[:200]}")
    print(f"\n  Wikia-Plaintext (erste 200):")
    p10_plain = wikia.get("p10", "")[:200]
    print(f"  {p10_plain}")

    # Decodiere alle Seiten
    print(f"\n{'='*80}")
    print("DEKODIERUNG ALLER SEITEN (p1-p16)")
    print("=" * 80)
    for p in sorted(tokens.keys()):
        seq = [t.get("glyph_id", "?") for t in tokens[p]]
        decoded = decode_attempt(seq, extended_mapping)
        print(f"\n  {p}:")
        print(f"    Glyphen: {''.join(seq[:80])}")
        print(f"    Dekodiert: {decoded[:200]}")
        if p in wikia:
            wikia_text = wikia[p][:200]
            print(f"    Wikia:    {wikia_text}")

    # Speichere Mapping
    out_path = OUT_DIR / "initial_mapping.json"
    with open(out_path, "w") as f:
        json.dump({
            "metadata": {
                "phase": "V10 / Initial Mapping",
                "datum": datetime.now().isoformat(),
                "method": "Frequency-Match + Wikia-Regeln + V6 Heuristik",
            },
            "wikia_rules": WIKIA_RULES,
            "v6_heuristics": V6_HEURISTICS,
            "initial_mapping": extended_mapping,
        }, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Mapping gespeichert: {out_path}")


if __name__ == "__main__":
    main()
