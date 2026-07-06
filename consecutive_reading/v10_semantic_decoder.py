"""
v10_semantic_decoder.py
V10 Phase 5 — SEMANTISCHE Übersetzung: Glyph → Wort-Sinn

Befund aus V10 Phase 4:
- 1 Glyph = ~1 Wikia-Wort
- Aber: gleicher Glyph mappt zu verschiedenen Wikia-Wörtern
- Daher: Mapping ist SEMANTISCH (Wort-Sinn), nicht 1:1 (Buchstabe-zu-Buchstabe)

Beispiel:
- G05 (13× in p01) → IS, A, MINDS, FAITH, YOU
  → G05 = Verb "sein" oder Pronomen-Konzept
- G19 (10×) → SOULS, RE, THOSE, YOU, EVERYTHING
  → G19 = Possessiv/Person-Bezug
- G29 (9×) → WHO, ASK, SEEK, TRUTH, AND
  → G29 = Frage/Suche-Wort

Methode:
1. Sammle ALLE Wikia-Wörter pro Glyph über alle Seiten
2. Berechne "Wortfeld" (semantisches Feld) pro Glyph
3. Erstelle semantisches Mapping Glyph → Wortfeld
4. Teste mit p10 (komplexe Seite mit 1/137, AMRAM, LEVI, ISHMAEL)
"""
import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

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
    """Segment Wikia plaintext into n_units chunks by word count"""
    words = re.findall(r'\b[A-Z]+\b', plaintext.upper())
    if not words or n_units == 0:
        return []
    words_per_unit = max(1, len(words) // n_units)
    remainder = len(words) % n_units
    units = []
    for i in range(n_units):
        # Add 1 to first 'remainder' units to balance
        extra = 1 if i < remainder else 0
        start = i * words_per_unit + min(i, remainder)
        end = start + words_per_unit + extra
        units.append(" ".join(words[start:end]))
    return units


def main():
    print("=" * 80)
    print("V10 PHASE 5: SEMANTISCHE ÜBERSETZUNG GLYPH → WORT-SINN")
    print("=" * 80)

    tokens = load_v6_tokens()
    wikia = load_wikia()

    # Sammle Glyph → Wikia-Wörter über ALLE Seiten
    print(f"\n{'='*80}")
    print("SAMMLE GLYPH → WIKIA-WÖRTER ÜBER ALLE P1-P16")
    print("=" * 80)

    glyph_words = defaultdict(list)
    for page_id in sorted(tokens.keys()):
        if page_id not in wikia:
            continue
        seq = [t.get("glyph_id", "?") for t in tokens[page_id]]
        n_g25 = sum(1 for g in seq if g == "G25")
        n_concepts = len(seq) - n_g25
        units = segment_into_units(wikia[page_id], n_concepts)

        for i, g in enumerate([g for g in seq if g != "G25"]):
            if i < len(units):
                unit_words = re.findall(r'\b[A-Z]+\b', units[i])
                glyph_words[g].extend(unit_words)

    # Drucke für jeden Glyphen die Top-Wörter
    print(f"\n  GLYPH-WORTFELDER (Top 10 Wörter pro Glyph):")
    glyph_semantic = {}
    for g in sorted(glyph_words.keys(), key=lambda x: -len(glyph_words[x])):
        counter = Counter(glyph_words[g])
        top = counter.most_common(15)
        print(f"\n  {g} ({sum(counter.values())} total words, {len(counter)} unique):")
        for word, cnt in top:
            print(f"    {word}: {cnt}")

        # Extrahiere semantisches Feld
        glyph_semantic[g] = [w for w, _ in counter.most_common(5)]

    # Test mit p10 (komplexeste Seite)
    print(f"\n{'='*80}")
    print("TEST-DEKODIERUNG P10 (komplexeste Seite mit 1/137)")
    print("=" * 80)

    p10_seq = [t.get("glyph_id", "?") for t in tokens["p10"]]
    p10_wikia = wikia["p10"]

    # Segmentiere Wikia
    n_g25_p10 = sum(1 for g in p10_seq if g == "G25")
    n_concepts_p10 = len(p10_seq) - n_g25_p10
    units_p10 = segment_into_units(p10_wikia, n_concepts_p10)

    # Versuche Glyph → Wikia-Concept Mapping
    p10_decoded = []
    for g in p10_seq:
        if g == "G25":
            p10_decoded.append(" / ")
        else:
            # Mappe Glyph → Top-3 Wikia-Wörter aus semantischem Feld
            if g in glyph_semantic:
                p10_decoded.append(f"({g}:{','.join(glyph_semantic[g][:2])})")
            else:
                p10_decoded.append(f"({g}:?)")

    print(f"\n  Glyphen → semantisches Mapping:")
    print(f"  {' '.join(p10_decoded[:60])}")

    # Besser: verwende p10-spezifisches Mapping
    print(f"\n  P10 Wikia-Phrasen (zur Validierung):")
    for i, u in enumerate(units_p10[:20]):
        print(f"    [{i}] {u[:80]}")

    # Test: Welche Wikia-Phrasen pro Glyph in p10?
    p10_glyph_to_phrase = {}
    for i, g in enumerate([g for g in p10_seq if g != "G25"]):
        if i < len(units_p10):
            p10_glyph_to_phrase.setdefault(g, []).append(units_p10[i])

    print(f"\n  Glyph → Phrase in P10:")
    for g in sorted(p10_glyph_to_phrase.keys(),
                    key=lambda x: -len(p10_glyph_to_phrase[x])):
        phrases = p10_glyph_to_phrase[g]
        if len(phrases) > 1:
            print(f"    {g} ({len(phrases)}×):")
            for p in phrases[:3]:
                print(f"      → {p[:80]}")

    # Speichere Glyph-Semantic-Mapping
    out_path = OUT_DIR / "glyph_semantic_mapping.json"
    with open(out_path, "w") as f:
        json.dump({
            "metadata": {
                "phase": "V10 / Semantic Mapping",
                "datum": datetime.now().isoformat(),
                "method": "Word-frequency aggregation per glyph across all pages",
            },
            "glyph_semantic": {g: {"top_words": [w for w, _ in Counter(glyph_words[g]).most_common(20)],
                                    "n_occurrences": sum(Counter(glyph_words[g]).values()),
                                    "n_unique": len(Counter(glyph_words[g]))}
                               for g in glyph_words},
        }, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Glyph-Semantic-Mapping: {out_path}")


if __name__ == "__main__":
    main()
