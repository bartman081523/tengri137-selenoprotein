#!/usr/bin/env python3
"""
phase5b_abjad_test.py — V6 Phase 5b: Abjad-Hypothese + Wort-Segmentierung.

Aus Phase 5:
- G25 ist "Hub" (zentral, vielfältige Nachbarn)
- X-G25-X trilaterale Muster: 6 Varianten in Top-50
- Gaps > 80px sind Wortgrenzen (353 gefunden)

Jetzt:
1. Segmentiere Token-Streams in "Wörter" via Gap > 80px
2. Pro Wort: Berechne Konsonanten-Gerüst (alle Glyphen ohne G25)
3. Test: Sind die "Wurzeln" (konsonantische Gerüste) wiederholend?
   → Wenn ja, ist Tengri ein Abjad

Output: bbox/ngram_xeno_20260706_V6/abjad_test.json
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


VOWEL = "G25"  # Hypothese: G25 ist Vokal-Träger (Schwa)


def segment_words(tokens_with_pos, gap_threshold=80):
    """Segmentiere Token-Sequenz in Wörter basierend auf horizontalem Gap."""
    words = []
    cur = [tokens_with_pos[0]]
    for i in range(1, len(tokens_with_pos)):
        prev = tokens_with_pos[i-1]
        cur_tok = tokens_with_pos[i]
        # Gap = x_von_cur - (x+breite von prev)
        gap = cur_tok["x"] - (prev["x"] + prev["w"])
        if gap > gap_threshold:
            words.append(cur)
            cur = [cur_tok]
        else:
            cur.append(cur_tok)
    if cur:
        words.append(cur)
    return words


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--pages", type=str, default="p01,p02,p03,p04,p07,p08,p09,p10,p11,p12,p13,p14,p15,p16")
    ap.add_argument("--gap-threshold", type=int, default=80)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    pages = args.pages.split(",")
    page_data = {}
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        page_data[pid] = d["tokens"]

    # Alle Wörter sammeln
    all_words = []
    per_page_words = {}
    for pid in pages:
        if pid not in page_data:
            continue
        # Sortiere nach y, dann x (Lesereihenfolge)
        toks = sorted(page_data[pid], key=lambda t: (t["y"], t["x"]))
        words = segment_words(toks, args.gap_threshold)
        per_page_words[pid] = words
        for w in words:
            word_glyphs = [t["glyph_id"] for t in w]
            all_words.append({
                "page": pid,
                "glyphs": word_glyphs,
                "n_chars": len(word_glyphs),
                "kons_frame": "".join(g for g in word_glyphs if g != VOWEL),
            })

    print(f"=== Wort-Segmentierung (Gap > {args.gap_threshold}px) ===")
    n_words = len(all_words)
    n_chars_total = sum(w["n_chars"] for w in all_words)
    print(f"Total Wörter: {n_words}")
    print(f"Total Glyphen in Wörtern: {n_chars_total}")
    print(f"Mittlere Wortlänge: {n_chars_total/n_words:.2f}")
    word_lens = Counter(w["n_chars"] for w in all_words)
    print(f"Wortlängen-Verteilung: {dict(sorted(word_lens.items()))}")

    # === Konsonanten-Gerüst-Analyse ===
    print(f"\n=== Abjad-Test: Konsonanten-Gerüste ({VOWEL} als Vokal) ===")
    frames = Counter(w["kons_frame"] for w in all_words if w["kons_frame"])
    print(f"Unique Konsonanten-Gerüste: {len(frames)}")
    print(f"Top-20 häufigste Gerüste (Wurzel-Kandidaten):")
    for frame, n in frames.most_common(20):
        print(f"  '{frame}': {n} mal")

    # Wiederholungs-Rate
    total_wiederholt = sum(n for n in frames.values() if n > 1)
    print(f"\nGerüste mit > 1 Vorkommen: {sum(1 for n in frames.values() if n > 1)}")
    print(f"  → {total_wiederholt} Wörter haben ein wiederholtes Wurzel-Muster")
    print(f"  → Wiederholungs-Rate: {total_wiederholt/n_words*100:.1f}% der Wörter")

    # === Konsonanten-Inventar ===
    all_kons = "".join(w["kons_frame"] for w in all_words)
    kons_counts = Counter(all_kons)
    print(f"\nKonsonanten-Inventar (Häufigkeit):")
    for g, n in kons_counts.most_common():
        print(f"  {g}: {n} ({n/len(all_kons)*100:.1f}%)")

    # === G25-Position im Wort (Anfang, Mitte, Ende, allein) ===
    g25_position = Counter()
    for w in all_words:
        glyphs = w["glyphs"]
        if glyphs == [VOWEL]:
            g25_position["alone"] += 1
        elif glyphs[0] == VOWEL and glyphs[-1] == VOWEL:
            g25_position["both"] += 1
        elif glyphs[0] == VOWEL:
            g25_position["start"] += 1
        elif glyphs[-1] == VOWEL:
            g25_position["end"] += 1
        else:
            g25_position["middle"] += 1
    print(f"\nG25-Position im Wort:")
    for pos, n in g25_position.most_common():
        print(f"  {pos}: {n} Wörter")

    # === Top-10 längste und kürzeste "Wörter" ===
    print(f"\n=== Beispiele ===")
    print(f"Beispiel-Wörter (zufällig, max 15):")
    for w in all_words[:15]:
        print(f"  p{w['page']} ({w['n_chars']} Glyphen): {''.join(w['glyphs'])}")

    # Output
    output = {
        "metadata": {
            "n_words": n_words,
            "n_chars_total": n_chars_total,
            "mean_word_length": round(n_chars_total / n_words, 2),
            "gap_threshold_px": args.gap_threshold,
            "vowel_hypothesis": VOWEL,
            "method": "Xenosemantische Segmentierung + Abjad-Gerüst-Test",
        },
        "word_length_distribution": dict(sorted(word_lens.items())),
        "consonant_frames": {
            "n_unique": len(frames),
            "n_repeated": sum(1 for n in frames.values() if n > 1),
            "top20": [{"frame": f, "count": n} for f, n in frames.most_common(20)],
            "repetition_rate": round(total_wiederholt / n_words, 4),
        },
        "consonant_inventory": {
            "counts": dict(kons_counts),
            "n_unique": len(kons_counts),
        },
        "g25_position": dict(g25_position),
        "interpretation": (
            f"Wenn Konsonanten-Gerüste sich wiederholen und ein fixes Inventar haben: "
            f"Abjad-Hypothese wahrscheinlich. "
            f"Unique Gerüste: {len(frames)} (von {n_words} Wörtern). "
            f"Repetition-Rate: {total_wiederholt/n_words*100:.1f}%. "
            f"Top-Konsonanten: {kons_counts.most_common(5)}"
        )
    }
    out_path = args.out / "abjad_test.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
