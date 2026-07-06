"""
v10_word_decoder.py
V10 Phase 3 — WORT-Hypothese: 1 Glyph = 1 Wort

Kritische Erkenntnis aus V10 Phase 2:
- 1 Glyph ≈ 1-2 Wörter (NICHT 1 Buchstabe)
- Tengri mp3 Spektrogramm: "EACH GLYPH IS A WORD" (angeblich)
- Wikia "For beginners": "runes without any cipher" — Orkhon runes, but konzept-basiert

Strategie:
- Jeder Glyph steht für ein WORT (oder Morphem)
- Verwende Schmehs Wikia-Wortliste als Ground-Truth-Wörterbuch
- Brute-Force Glyph → Wort
- Validiere gegen Schmehs Plaintext

Aber: 92 Glyphen × 125 Wörter = 11,500 Kombinationen pro Seite
- Zu viele für Brute-Force

Alternative:
- Verwende Wikia-Wortliste aus p01
- Häufigstes Wort = häufigster Glyph
- Teste Mappings konsistent über alle Seiten
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter
from itertools import permutations

OUT_DIR = Path("bbox/v10_decoder_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)

V6_HEURISTICS = {
    "G01": "J", "G02": ")", "G03": "P", "G05": "I", "G06": "E",
    "G07": "N", "G08": "H", "G17": "D", "G18": "F", "G25": "G25",
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


def extract_words(plaintext):
    """Extract words from Wikia plaintext"""
    # Wikia plaintext has words like "ONE THREE SEVEN"
    return re.findall(r'\b[A-Z]+\b', plaintext.upper())


def decode_as_words(glyph_seq, mapping, separator_glyph="G25"):
    """Decode right-to-left, G25 = word separator"""
    words = []
    current = []
    for g in reversed(glyph_seq):
        if g == separator_glyph:
            if current:
                word = mapping.get("".join(current), "?")
                words.append(word)
                current = []
        else:
            current.append(g)
    if current:
        word = mapping.get("".join(current), "?")
        words.append(word)
    return " ".join(words)


def main():
    print("=" * 80)
    print("V10 PHASE 3: WORT-HYPOTHESE — 1 GLYPH = 1 WORT")
    print("=" * 80)

    tokens = load_v6_tokens()
    wikia = load_wikia()

    # Sammle alle Wikia-Wörter über alle Seiten
    print(f"\n{'='*80}")
    print("WIKIA-WORTLISTE (alle 23 Seiten)")
    print("=" * 80)
    all_words = Counter()
    for page_id, text in wikia.items():
        words = extract_words(text)
        all_words.update(words)

    print(f"  Unique Wörter: {len(all_words)}")
    print(f"  Total Vorkommen: {sum(all_words.values())}")

    # Top 50 Wörter
    print(f"\n  Top 50 Wörter:")
    for word, cnt in all_words.most_common(50):
        print(f"    {word}: {cnt}")

    # Glyph-Frequenz
    print(f"\n{'='*80}")
    print("GLYPH-FREQUENZ (p1-p16, ohne G25)")
    print("=" * 80)
    glyph_freq = Counter()
    for page_id, page_tokens in tokens.items():
        for t in page_tokens:
            gid = t.get("glyph_id", "?")
            if gid != "G25":
                glyph_freq[gid] += 1
    print(f"  Top 17 Glyphen (ohne G25):")
    for g, c in glyph_freq.most_common(20):
        print(f"    {g}: {c}")

    # p01: 92 Glyphen vs 125 Wörter → 1.36 Wörter pro Glyph
    # Wenn 1 Glyph = 1 Wort, hätten wir 92 Wörter. Wikia hat 125.
    # Unterschied: 33 Wörter extra in Wikia (vielleicht Stoppwörter?)
    # Oder: G25 ist Wort-Trenner → 92 Glyphen - G25-Anzahl = tatsächliche Wörter

    # Zähle G25 pro Seite
    print(f"\n{'='*80}")
    print("G25 (TRENNER) PRO SEITE")
    print("=" * 80)
    for page_id in ["p01", "p02", "p07", "p10", "p11"]:
        if page_id in tokens:
            seq = [t.get("glyph_id", "?") for t in tokens[page_id]]
            n_total = len(seq)
            n_g25 = sum(1 for g in seq if g == "G25")
            n_words = n_g25 + 1 if n_g25 > 0 else n_total
            wikia_words = len(extract_words(wikia.get(page_id, "")))
            print(f"  {page_id}: {n_total} Glyphen, {n_g25} G25 → {n_words} Wörter (Wikia: {wikia_words})")

    # Versuche: Mapping G_X → Y aus Wort-Frequenz
    # Häufigster Glyph (ohne G25) = G18 (12%) → häufigstes englisches Wort "THE" (8%)
    # G19 (11.6%) → "TO" oder "OF"
    # G29 (10.1%) → "AND" (3.6%)
    # G05 (7.4%) → "A" (4.8%)? aber G05=I Heuristik

    # Häufigste Wikia-Wörter:
    # THE (1349), TO (564), A (497), OF (495), AND (451), IN (340), IS (266), ...

    # Mapping-Versuch
    print(f"\n{'='*80}")
    print("MAPPING-VERSUCH (Frequency + Heuristik)")
    print("=" * 80)
    word_mapping = {
        "G18": "THE",  # G18 = F-Heuristik, häufigstes Wort
        "G19": "TO",   # G19 = ?, häufig
        "G29": "AND",  # G29 = ?, häufig
        "G05": "A",    # G05 = I-Heuristik, A häufig
        "G07": "OF",   # G07 = N-Heuristik, OF häufig
        "G03": "IN",   # G03 = P-Heuristik
        "G10": "IS",   # G10 = ?
        "G09": "FOR",  # G09 = ?
        "G06": "THAT", # G06 = E-Heuristik
        "G14": "WITH", # G14 = ?
        "G01": "BE",   # G01 = J-Heuristik
        "G02": "NOT",  # G02 = )-Heuristik, selten
        "G11": "ON",   # G11 = ?
        "G17": "AT",   # G17 = D-Heuristik
        "G08": "FROM", # G08 = H-Heuristik
        "G24": "ALL",  # G24 = ?, sehr selten
    }

    # Test p01
    print(f"\n  Test p01 (erste 200 Zeichen):")
    p01_seq = [t.get("glyph_id", "?") for t in tokens["p01"]]
    p01_decoded = decode_as_words(p01_seq, word_mapping)
    p01_wikia = wikia.get("p01", "")
    print(f"    Decoded: {p01_decoded[:200]}")
    print(f"    Wikia:   {p01_wikia[:200]}")

    # Score
    decoded_words = set(p01_decoded.split())
    wikia_words_set = set(extract_words(p01_wikia))
    matches = decoded_words & wikia_words_set
    print(f"    Matches: {len(matches)}/{len(decoded_words)} = {len(matches)/max(len(decoded_words), 1):.2%}")
    print(f"    Matched: {sorted(matches)[:20]}")

    # Test p10
    print(f"\n  Test p10 (erste 200 Zeichen):")
    p10_seq = [t.get("glyph_id", "?") for t in tokens["p10"]]
    p10_decoded = decode_as_words(p10_seq, word_mapping)
    p10_wikia = wikia.get("p10", "")
    print(f"    Decoded: {p10_decoded[:200]}")
    print(f"    Wikia:   {p10_wikia[:200]}")

    decoded_words = set(p10_decoded.split())
    wikia_words_set = set(extract_words(p10_wikia))
    matches = decoded_words & wikia_words_set
    print(f"    Matches: {len(matches)}/{len(decoded_words)} = {len(matches)/max(len(decoded_words), 1):.2%}")
    print(f"    Matched: {sorted(matches)[:20]}")

    # Test p11
    print(f"\n  Test p11 (erste 200 Zeichen):")
    p11_seq = [t.get("glyph_id", "?") for t in tokens["p11"]]
    p11_decoded = decode_as_words(p11_seq, word_mapping)
    p11_wikia = wikia.get("p11", "")
    print(f"    Decoded: {p11_decoded[:200]}")
    print(f"    Wikia:   {p11_wikia[:200]}")

    decoded_words = set(p11_decoded.split())
    wikia_words_set = set(extract_words(p11_wikia))
    matches = decoded_words & wikia_words_set
    print(f"    Matches: {len(matches)}/{len(decoded_words)} = {len(matches)/max(len(decoded_words), 1):.2%}")
    print(f"    Matched: {sorted(matches)[:20]}")


if __name__ == "__main__":
    main()
