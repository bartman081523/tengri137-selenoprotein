"""
v10_concept_decoder.py
V10 Phase 4 — KONZEPT-Hypothese: 1 Glyph = 1 Konzept (= mehrere Wikia-Wörter)

Konsistente Befunde aus V6 + V8 + V10:
- 17 V6-Glyphen ≠ 26 lateinische Buchstaben
- 1 Glyph ≈ 7 lateinische Zeichen (Ratio 1:7)
- 1 Glyph ≈ 1.6 Wikia-Wörter
- G25 = Wort-Trenner (~22% der Glyphen)

Schlussfolgerung: Tengri ist eine PSEUDO-SCHRIFT (kein 1:1 lateinisches Mapping).
Jeder Glyph repräsentiert ein KONZEPT, das in mehreren lateinischen Wörtern ausgedrückt wird.

Methode (pragmatisch):
1. Segmentiere Wikia-Plaintext in 19 Konzepte pro p01 (= Glyphen-Anzahl ohne G25)
2. Erstelle Wort-Phrasen-Mapping (welche Wikia-Wörter pro Glyph)
3. Teste: sind die Phrasen über Seiten konsistent?
4. Wenn ja: wir haben eine echte "Übersetzung" gefunden (nicht 1:1, aber konsistent)

Beispiel:
- Glyphen-Sequenz p01: [G07] [G29] [G05] [G14] [G25] [G09] [G17] ... = 74 Glyphen
- Wikia-Plaintext p01: 122 Wörter / 74 Glyphen = 1.6 Wörter pro Glyph
- Mapping: G07 → "TENGRI IS THE", G29 → "SOURCE OF IMPORTANT", etc.
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter

OUT_DIR = Path("bbox/v10_decoder_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)


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


def segment_into_units(plaintext, n_units):
    """Segment Wikia plaintext into n_units roughly equal chunks (by word count)"""
    words = re.findall(r'\b[A-Z]+\b', plaintext.upper())
    if not words:
        return []
    words_per_unit = max(1, len(words) // n_units)
    units = []
    for i in range(n_units):
        start = i * words_per_unit
        end = start + words_per_unit if i < n_units - 1 else len(words)
        units.append(" ".join(words[start:end]))
    return units


def main():
    print("=" * 80)
    print("V10 PHASE 4: KONZEPT-HYPOTHESE — 1 GLYPH = 1 KONZEPT")
    print("=" * 80)

    tokens = load_v6_tokens()
    wikia = load_wikia()

    # p01 Detail-Analyse
    print(f"\n{'='*80}")
    print("P01: GLYPHEN vs WIKIA-WÖRTER (KONZEPT-SEGMENTIERUNG)")
    print("=" * 80)

    p01_seq = [t.get("glyph_id", "?") for t in tokens["p01"]]
    p01_wikia = wikia["p01"]

    # Zähle G25 (Trenner)
    n_g25 = sum(1 for g in p01_seq if g == "G25")
    n_concepts = len(p01_seq) - n_g25  # 92 - 18 = 74 Konzepte

    print(f"  Glyphen total: {len(p01_seq)}")
    print(f"  G25 (Trenner): {n_g25}")
    print(f"  Konzepte (= Glyphen ohne G25): {n_concepts}")
    print(f"  Wikia-Wörter: {len(re.findall(r'\\b[A-Z]+\\b', p01_wikia))}")

    # Segmentiere Wikia in 74 Konzepte
    units = segment_into_units(p01_wikia, n_concepts)
    print(f"  Konzepte segmentiert: {len(units)}")
    print(f"  Wörter pro Konzept: ~{len(re.findall(r'\\b[A-Z]+\\b', p01_wikia)) / n_concepts:.2f}")

    # Mapping Glyph → Konzept (für p01)
    print(f"\n  Glyph → Konzept (p01, ohne G25):")
    glyph_to_concept_p01 = {}
    for i, g in enumerate([g for g in p01_seq if g != "G25"]):
        if i < len(units):
            if g not in glyph_to_concept_p01:
                glyph_to_concept_p01[g] = []
            glyph_to_concept_p01[g].append(units[i])

    # Welche Glyphen sind mehrfach? Welche nur einmal?
    for g in sorted(glyph_to_concept_p01.keys(),
                    key=lambda x: -len(glyph_to_concept_p01[x])):
        concepts = glyph_to_concept_p01[g]
        if len(concepts) > 1:
            print(f"    {g} ({len(concepts)}×):")
            for c in concepts[:5]:
                print(f"      → {c[:80]}")

    # Test: Konsistenz über Seiten
    print(f"\n{'='*80}")
    print("KONSISTENZ-TEST: GLYPH-MAPPING ÜBER P01, P02, P03, P04")
    print("=" * 80)

    # Sammle alle Glyph→Konzept-Mappings über mehrere Seiten
    all_mappings = {}
    for page_id in ["p01", "p02", "p03", "p04"]:
        if page_id not in tokens or page_id not in wikia:
            continue
        seq = [t.get("glyph_id", "?") for t in tokens[page_id]]
        n_g25_p = sum(1 for g in seq if g == "G25")
        n_concepts_p = len(seq) - n_g25_p
        units_p = segment_into_units(wikia[page_id], n_concepts_p)
        for i, g in enumerate([g for g in seq if g != "G25"]):
            if i < len(units_p):
                if g not in all_mappings:
                    all_mappings[g] = []
                all_mappings[g].append((page_id, units_p[i]))

    # Drucke Glyphen mit mehreren Vorkommen über Seiten
    for g in sorted(all_mappings.keys(),
                    key=lambda x: -len(all_mappings[x])):
        if len(all_mappings[g]) > 1:
            entries = all_mappings[g]
            print(f"\n  {g} ({len(entries)} Vorkommen über Seiten):")
            for page_id, concept in entries[:6]:
                print(f"    {page_id}: {concept[:80]}")

    # Versuche eine "Übersetzung" zu generieren
    print(f"\n{'='*80}")
    print("P01 'ÜBERSETZUNG' (Glyphe → Wikia-Phrase)")
    print("=" * 80)

    # Erstelle Mapping aus p01
    glyph_to_phrase = {}
    for i, g in enumerate([g for g in p01_seq if g != "G25"]):
        if i < len(units):
            if g not in glyph_to_phrase:
                glyph_to_phrase[g] = units[i]
            else:
                # Kombiniere mehrfach-Vorkommen
                glyph_to_phrase[g] = f"{glyph_to_phrase[g]} | {units[i]}"

    # Decodiere p01
    p01_decoded = []
    for g in p01_seq:
        if g == "G25":
            p01_decoded.append(" | ")  # Satz-Trenner
        else:
            p01_decoded.append(glyph_to_phrase.get(g, "?")[:30])
    print(f"  p01 rekonstruiert:")
    print(f"  {' '.join(p01_decoded[:30])}")
    print(f"\n  p01 original (Wikia):")
    print(f"  {p01_wikia[:600]}")

    # Score: sind die Wort-Phrasen im Wikia?
    print(f"\n{'='*80}")
    print("WORT-PHRASEN-VERIFIKATION")
    print("=" * 80)
    wikia_p01_words = set(re.findall(r'\b[A-Z]+\b', p01_wikia))
    matched_words = set()
    for phrase in glyph_to_phrase.values():
        phrase_words = set(re.findall(r'\b[A-Z]+\b', phrase))
        matched_words.update(phrase_words & wikia_p01_words)
    print(f"  Wikia-Wörter in Mapping: {len(matched_words)} von {len(wikia_p01_words)} ({100*len(matched_words)/max(len(wikia_p01_words), 1):.1f}%)")
    print(f"  Matched: {sorted(matched_words)[:30]}")


if __name__ == "__main__":
    main()
