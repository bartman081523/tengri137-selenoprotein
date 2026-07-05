#!/usr/bin/env python3
"""
phase6_word_topology.py — V6 Phase 6: Wort-Topologie + OCP-Test.

Drei Angriffsvektoren:

ALPHA: Lexikalischer Zipf-Test + Affix-Isolierung
  - Wie viele der 394 Wörter sind unique?
  - Konsonanten-Gerüste (Stripping G25)
  - Affix-Kandidaten (Präfix/Suffix-Detection)

BETA: OCP-Test (Obligatory Contour Principle)
  - In echten Abjads verdoppeln sich Konsonanten NICHT (B-B-X ist tabu)
  - In Tengri: Verdopplung von Nicht-G25-Glyphen?
  - G18-G18-G18 wurde gefunden → CODE/Maschinenschrift, kein Abjad

GAMMA: G25-Kontext-Kollaps
  - Welche Glyphen stehen neben langen G25-Ketten (G25+G25+, G25³+, G25⁴)?
  - Wenn immer dieselben: mantrisch/multiplikator-funktion

Output: bbox/word_topology_20260706_V6/word_topology.json
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path


VOWEL = "G25"  # Hypothese


def segment_words(tokens_with_pos, gap_threshold=80):
    words = []
    cur = [tokens_with_pos[0]]
    for i in range(1, len(tokens_with_pos)):
        prev = tokens_with_pos[i-1]
        cur_tok = tokens_with_pos[i]
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
    ap.add_argument("--gap-threshold", type=int, default=80)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Lade Token-Streams
    all_words = []
    per_page = defaultdict(list)
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        toks = sorted(d["tokens"], key=lambda t: (t["y"], t["x"]))
        if not toks:
            continue
        words = segment_words(toks, args.gap_threshold)
        for w in words:
            word = {
                "page": pid,
                "glyphs": [t["glyph_id"] for t in w],
                "n_chars": len(w),
            }
            word["kons_frame"] = "".join(g for g in word["glyphs"] if g != VOWEL)
            word["g25_count"] = sum(1 for g in word["glyphs"] if g == VOWEL)
            word["kons_count"] = word["n_chars"] - word["g25_count"]
            all_words.append(word)
            per_page[pid].append(word)

    n_total = len(all_words)
    print(f"=== ALPHA: Lexikalische Inventur ===")
    print(f"Total Wörter: {n_total}")

    # === ALPHA.1: Unique Wörter (voller String) ===
    word_strs = ["-".join(w["glyphs"]) for w in all_words]
    word_counts = Counter(word_strs)
    n_unique_words = len(word_counts)
    n_unique_repeated = sum(1 for w, c in word_counts.items() if c > 1)

    print(f"\nUnique Wörter (voller String): {n_unique_words}")
    print(f"Wiederholte Wörter (>1 Vorkommen): {n_unique_repeated}")
    print(f"Lexikalische Diversität: {n_unique_words/n_total:.2%}")

    # Wortlängen-Verteilung
    word_lens = Counter(w["n_chars"] for w in all_words)
    print(f"\nWortlängen-Verteilung: {dict(sorted(word_lens.items()))}")

    # Top-20 häufigste Wörter
    print(f"\nTop-20 häufigste Wörter (voller String):")
    for word, c in word_counts.most_common(20):
        print(f"  '{word}': {c} mal")

    # === ALPHA.2: Konsonanten-Gerüste ===
    frames = Counter(w["kons_frame"] for w in all_words if w["kons_frame"])
    n_unique_frames = len(frames)
    print(f"\n=== Konsonanten-Gerüste (ohne G25) ===")
    print(f"Unique Gerüste: {n_unique_frames}")
    print(f"Gerüste mit >1 Vorkommen: {sum(1 for n in frames.values() if n > 1)}")
    print(f"\nTop-20 häufigste Gerüste:")
    for frame, c in frames.most_common(20):
        # Decode für Lesbarkeit
        readable = "·".join(frame[i:i+2] for i in range(0, len(frame), 2)) if len(frame) > 2 else frame
        print(f"  '{readable}': {c} mal")

    # === ALPHA.3: Affix-Kandidaten ===
    # Was steht IMMER am Anfang (Präfix-Kandidat)?
    first_glyph = Counter(w["glyphs"][0] for w in all_words if w["glyphs"])
    # Was steht IMMER am Ende (Suffix-Kandidat)?
    last_glyph = Counter(w["glyphs"][-1] for w in all_words if w["glyphs"])

    print(f"\n=== Affix-Kandidaten ===")
    print(f"Häufigste erste Glyphen: {first_glyph.most_common(10)}")
    print(f"Häufigste letzte Glyphen:  {last_glyph.most_common(10)}")

    # Was steht direkt vor G25 (in Mitte)?
    pre_g25 = Counter()
    post_g25 = Counter()
    for w in all_words:
        for i, g in enumerate(w["glyphs"]):
            if g == VOWEL:
                if i > 0:
                    pre_g25[w["glyphs"][i-1]] += 1
                if i < len(w["glyphs"]) - 1:
                    post_g25[w["glyphs"][i+1]] += 1

    print(f"\nVor G25 (Suffix-Kandidat): {pre_g25.most_common(10)}")
    print(f"Nach G25 (Prefix-Kandidat): {post_g25.most_common(10)}")

    # === BETA: OCP-Test ===
    print(f"\n=== BETA: OCP-Test (Obligatory Contour Principle) ===")
    # Suche Verdopplungen von Nicht-G25-Glyphen in Wörtern
    non_g25_doubles = Counter()
    triple_doubles = Counter()  # X-Y-X
    for w in all_words:
        glyphs = w["glyphs"]
        for i in range(len(glyphs) - 1):
            a, b = glyphs[i], glyphs[i+1]
            if a == b and a != VOWEL:
                non_g25_doubles[a] += 1
        for i in range(len(glyphs) - 2):
            a, b, c = glyphs[i], glyphs[i+1], glyphs[i+2]
            if a == c and a != VOWEL:
                triple_doubles[(a, b)] += 1

    print(f"Verdopplungen von Nicht-G25 (z.B. G18-G18): {dict(non_g25_doubles)}")
    print(f"Symmetric-Verdopplungen X-Y-X (Nicht-G25):")
    for (a, b), c in triple_doubles.most_common(10):
        print(f"  {a}-{b}-{a}: {c} mal")

    # Wenn G25 raus wäre, was wäre die Häufigkeit von Konsonant-Verdopplung?
    non_g25_doubles_total = sum(non_g25_doubles.values())
    n_total_pairs = sum(len(w["glyphs"]) - 1 for w in all_words)
    print(f"\nVerdopplungs-Rate (Nicht-G25): {non_g25_doubles_total}/{n_total_pairs} = {non_g25_doubles_total/n_total_pairs*100:.2f}%")

    # === GAMMA: G25-Kontext-Kollaps ===
    print(f"\n=== GAMMA: G25-Kontext-Kollaps ===")
    # Finde alle langen G25-Ketten
    long_chains_2 = []  # G25-G25
    long_chains_3 = []  # G25-G25-G25
    long_chains_4 = []  # G25-G25-G25-G25
    for w in all_words:
        glyphs = w["glyphs"]
        i = 0
        while i < len(glyphs):
            if glyphs[i] == VOWEL:
                # Finde Run
                start = i
                while i < len(glyphs) and glyphs[i] == VOWEL:
                    i += 1
                run_len = i - start
                # Kontext davor und danach
                pre = glyphs[start-1] if start > 0 else None
                post = glyphs[i] if i < len(glyphs) else None
                entry = (pre, post, start, i, glyphs)
                if run_len == 2:
                    long_chains_2.append(entry)
                elif run_len == 3:
                    long_chains_3.append(entry)
                elif run_len >= 4:
                    long_chains_4.append(entry)
            else:
                i += 1

    print(f"\nG25-G25 (Doppel): {len(long_chains_2)} Vorkommen")
    if long_chains_2:
        pre2 = Counter(e[0] for e in long_chains_2 if e[0])
        post2 = Counter(e[1] for e in long_chains_2 if e[1])
        print(f"  Vor G25-G25 (Top-5): {pre2.most_common(5)}")
        print(f"  Nach G25-G25 (Top-5): {post2.most_common(5)}")

    print(f"\nG25-G25-G25 (Tripel): {len(long_chains_3)} Vorkommen")
    if long_chains_3:
        pre3 = Counter(e[0] for e in long_chains_3 if e[0])
        post3 = Counter(e[1] for e in long_chains_3 if e[1])
        print(f"  Vor G25³: {pre3.most_common(5)}")
        print(f"  Nach G25³: {post3.most_common(5)}")

    print(f"\nG25-G25-G25-G25+ (Quadrupel): {len(long_chains_4)} Vorkommen")
    for entry in long_chains_4[:5]:
        pre, post, s, e, glyphs = entry
        print(f"  Wort: {''.join(glyphs)} (G25-Run @ {s}-{e}, pre={pre}, post={post})")

    # === Bigramm-Analyse: Top-30 Bigramme (volles Wort) ===
    print(f"\n=== Bigramm-Top-30 (volle Wort-Token) ===")
    bigrams = Counter()
    for w in all_words:
        glyphs = w["glyphs"]
        for i in range(len(glyphs) - 1):
            bigrams[(glyphs[i], glyphs[i+1])] += 1
    for (a, b), c in bigrams.most_common(30):
        marker = " ★" if a == VOWEL and b == VOWEL else ""
        print(f"  {a}-{b}: {c}{marker}")

    # Output
    output = {
        "metadata": {
            "n_total_words": n_total,
            "n_unique_full_words": n_unique_words,
            "n_repeated_words": n_unique_repeated,
            "lexical_diversity": round(n_unique_words / n_total, 4),
            "n_unique_consonant_frames": n_unique_frames,
            "method": "Wort-Topologie (Alpha) + OCP-Test (Beta) + G25-Kontext (Gamma)",
        },
        "alpha_lexicon": {
            "top20_full_words": [{"word": w, "count": c} for w, c in word_counts.most_common(20)],
            "top20_consonant_frames": [{"frame": f, "count": c} for f, c in frames.most_common(20)],
            "word_length_distribution": dict(sorted(word_lens.items())),
        },
        "alpha_affixes": {
            "first_glyph_top10": first_glyph.most_common(10),
            "last_glyph_top10": last_glyph.most_common(10),
            "pre_g25_top10": pre_g25.most_common(10),
            "post_g25_top10": post_g25.most_common(10),
        },
        "beta_ocp": {
            "non_g25_doubles": dict(non_g25_doubles),
            "x_y_x_symmetric": {f"{a}-{b}-{a}": c for (a, b), c in triple_doubles.most_common(20)},
            "non_g25_double_rate_pct": round(non_g25_doubles_total / n_total_pairs * 100, 2),
            "interpretation": (
                "Wenn OCP-Rate ≈ 0%: Echtes Abjad (Konsonanten-Verdopplung tabu). "
                "Wenn OCP-Rate > 5%: Code/formal/maschinell. "
                f"Tatsächlich: {non_g25_doubles_total/n_total_pairs*100:.2f}%"
            )
        },
        "gamma_g25_context": {
            "chain_2": {
                "count": len(long_chains_2),
                "pre_top5": Counter(e[0] for e in long_chains_2 if e[0]).most_common(5),
                "post_top5": Counter(e[1] for e in long_chains_2 if e[1]).most_common(5),
            },
            "chain_3": {
                "count": len(long_chains_3),
                "pre_top5": Counter(e[0] for e in long_chains_3 if e[0]).most_common(5),
                "post_top5": Counter(e[1] for e in long_chains_3 if e[1]).most_common(5),
            },
            "chain_4plus": {
                "count": len(long_chains_4),
                "examples": [{"word": "".join(e[4]), "pre": e[0], "post": e[1]} for e in long_chains_4[:5]],
            },
        },
        "bigrams_top30": [
            {"bigram": f"{a}-{b}", "count": c, "is_g25_run": a == VOWEL and b == VOWEL}
            for (a, b), c in bigrams.most_common(30)
        ],
        "interpretation": (
            f"Lexikalische Diversität: {n_unique_words/n_total:.2%}. "
            f"Top-Wort-Häufigkeit: {word_counts.most_common(1)[0][1] if word_counts else 0}. "
            f"OCP-Rate: {non_g25_doubles_total/n_total_pairs*100:.2f}%. "
            f"G25-Doppel-Kontext: pre={Counter(e[0] for e in long_chains_2 if e[0]).most_common(3)}, "
            f"post={Counter(e[1] for e in long_chains_2 if e[1]).most_common(3)}."
        )
    }
    out_path = args.out / "word_topology.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
