#!/usr/bin/env python3
"""
phase5_ngram_xeno.py — V6 Phase 5: N-Gramm- und Kontaktanalyse (Xenosemantisch).

Epoché: KEIN lateinisches Substitutions-Bias. Wir analysieren Tengri als
eigenständiges 17-State-System mit folgenden Attack-Vektoren:

1. G25-Kontaktanalyse (Bigramm + Trigramm): Spacer? Suffix? Prefix?
2. Trilaterale Wurzeln: Wiederholen sich Tripel (Abjad-Hypothese)?
3. Positions-Glyphen: Welche Glyphen kommen NUR am Anfang/Ende vor?
4. Cluster-Segmentierung: Lassen sich Wortgrenzen statistisch detektieren?
   (Variation in Glyphen-Größe oder Lücken?)
5. Repetitions-Analyse: G25+G25 (Verdopplung)?

Output: bbox/ngram_xeno_20260706_V6/ngram_report.json
        + PNG-Visualisierungen
"""
import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


def shannon(tokens):
    n = len(tokens)
    if n == 0:
        return 0.0
    counts = Counter(tokens)
    h = 0.0
    for c in counts.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--pages", type=str, default="01,02,03,04,07,08,09,10,11,12,13,14,15,16")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    pages = ["p" + p for p in args.pages.split(",")]
    page_data = {}
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        page_data[pid] = d["tokens"]

    # All tokens across fliesstext pages
    all_tokens = []
    per_page_seq = {}
    for pid in pages:
        if pid in page_data:
            toks = [t["glyph_id"] for t in page_data[pid]]
            per_page_seq[pid] = toks
            all_tokens.extend(toks)

    n_total = len(all_tokens)
    counts = Counter(all_tokens)
    print(f"Substrat: {n_total} tokens, {len(counts)} unique")

    # === Attack 1: G25-Kontaktanalyse ===
    G25 = "G25"  # Das dominante Token (21.3%)
    print(f"\n=== ATTACK 1: G25-Kontaktanalyse ===")
    print(f"G25 Anteil: {counts.get(G25, 0)/n_total*100:.2f}%")

    bigrams = Counter()
    trigrams = Counter()
    for i in range(len(all_tokens) - 1):
        bigrams[(all_tokens[i], all_tokens[i+1])] += 1
    for i in range(len(all_tokens) - 2):
        trigrams[(all_tokens[i], all_tokens[i+1], all_tokens[i+2])] += 1

    # Bigramme mit G25
    g25_left = Counter()  # X+G25
    g25_right = Counter()  # G25+X
    g25_doubled = 0  # G25+G25
    for (a, b), c in bigrams.items():
        if a == G25 and b == G25:
            g25_doubled = c
        elif a == G25:
            g25_right[b] += c
        elif b == G25:
            g25_left[a] += c

    print(f"\nG25 + G25 (Verdopplung): {g25_doubled} mal")
    print(f"Top-10 G25→X (Suffix-Hypothese): {g25_right.most_common(10)}")
    print(f"Top-10 X→G25 (Prefix-Hypothese): {g25_left.most_common(10)}")

    # === Attack 2: Trilaterale Wurzeln ===
    print(f"\n=== ATTACK 2: Trilaterale Wurzeln (Top-20 Trigramm) ===")
    for (a, b, c), n in trigrams.most_common(20):
        print(f"  {a}-{b}-{c}: {n}")

    # Trilaterale Wurzeln: gleicher Anfangs- und Endbuchstabe
    root_candidates = defaultdict(int)
    for (a, b, c), n in trigrams.most_common(50):
        if a == c:  # X-Y-X (wie semitische Wurzeln)
            root_candidates[(a, b, c)] += n
    print(f"\nTrilaterale Wurzeln (X-Y-X) in Top-50: {dict(root_candidates)}")

    # === Attack 3: Positions-Glyphen (Anfang/Ende) ===
    print(f"\n=== ATTACK 3: Positions-Glyphen (Anfang/Ende der Page-Sequenzen) ===")
    start_counts = Counter()
    end_counts = Counter()
    for pid, toks in per_page_seq.items():
        if toks:
            start_counts[toks[0]] += 1
            end_counts[toks[-1]] += 1
    print(f"\nHäufigste Page-Starts: {start_counts.most_common(10)}")
    print(f"Häufigste Page-Ends:  {end_counts.most_common(10)}")

    # === Attack 4: Cluster-Segmentierung ===
    print(f"\n=== ATTACK 4: Cluster-Segmentierung (Glyphen-Größe als Wort-Indikator) ===")
    # Wir haben die bbox-Daten nochmal
    page_tokens_full = {}
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        if pid in pages:
            page_tokens_full[pid] = d["tokens"]

    # Größen (w*h) pro Token
    sizes = []
    gaps_x = []  # horizontal gap zum nächsten Token
    for pid, toks in page_tokens_full.items():
        # Sortiere nach y, dann x
        sorted_toks = sorted(toks, key=lambda t: (t["y"], t["x"]))
        for t in sorted_toks:
            sizes.append(t["w"] * t["h"])
        for i in range(len(sorted_toks) - 1):
            a, b = sorted_toks[i], sorted_toks[i+1]
            if abs(a["y"] - b["y"]) < 20:  # gleiche Zeile
                gap = b["x"] - (a["x"] + a["w"])
                gaps_x.append(gap)

    print(f"Token-Größen: min={min(sizes)}, max={max(sizes)}, mean={np.mean(sizes):.0f}, median={np.median(sizes):.0f}")
    print(f"Horizontal-Gaps: min={min(gaps_x)}, max={max(gaps_x)}, mean={np.mean(gaps_x):.1f}, median={np.median(gaps_x):.1f}")

    # Gap-Verteilung
    gap_buckets = Counter()
    for g in gaps_x:
        if g < 0:
            gap_buckets["overlap"] += 1
        elif g < 5:
            gap_buckets["0-5"] += 1
        elif g < 10:
            gap_buckets["5-10"] += 1
        elif g < 20:
            gap_buckets["10-20"] += 1
        elif g < 40:
            gap_buckets["20-40"] += 1
        elif g < 80:
            gap_buckets["40-80"] += 1
        else:
            gap_buckets[">80 (Wortgrenze?)"] += 1
    print(f"\nGap-Verteilung: {dict(gap_buckets)}")

    # === Attack 5: G25-Verdopplung + Sequenz-Analyse ===
    print(f"\n=== ATTACK 5: G25-Sequenz-Analyse ===")
    # Suche alle maximalen G25-Sequenzen
    max_run = 0
    cur_run = 0
    runs = []
    for t in all_tokens:
        if t == G25:
            cur_run += 1
        else:
            if cur_run > 0:
                runs.append(cur_run)
            max_run = max(max_run, cur_run)
            cur_run = 0
    if cur_run > 0:
        runs.append(cur_run)
    run_counts = Counter(runs)
    print(f"Maximale G25-Sequenz: {max_run}")
    print(f"G25-Run-Verteilung: {dict(run_counts)}")

    # Output
    output = {
        "metadata": {
            "n_tokens": n_total,
            "n_unique": len(counts),
            "method": "Xenosemantische N-Gramm- und Kontaktanalyse (Epoché: kein lateinischer Bias)",
        },
        "attack_1_g25_contact": {
            "g25_share": round(counts.get(G25, 0) / n_total, 4),
            "g25_doubled": g25_doubled,
            "g25_right_top10": g25_right.most_common(10),
            "g25_left_top10": g25_left.most_common(10),
            "hypothesis": (
                "Wenn G25 nie verdoppelt und nur rechts vielfältig: Suffix/Spacer-Hypothese. "
                "Wenn G25 links vielfältig: Prefix. "
                f"Tatsächlich: Verdopplung={g25_doubled}, Right-Top={g25_right.most_common(3)}, Left-Top={g25_left.most_common(3)}"
            )
        },
        "attack_2_triliteral_roots": {
            "top20_trigrams": [
                {"trigram": f"{a}-{b}-{c}", "count": n} for (a, b, c), n in trigrams.most_common(20)
            ],
            "x_y_x_roots": {f"{a}-{b}-{c}": n for (a, b, c), n in root_candidates.items()},
        },
        "attack_3_position_glyphs": {
            "page_starts_top10": start_counts.most_common(10),
            "page_ends_top10": end_counts.most_common(10),
        },
        "attack_4_cluster_segmentation": {
            "token_sizes": {
                "min": int(min(sizes)), "max": int(max(sizes)),
                "mean": round(float(np.mean(sizes)), 1),
                "median": int(np.median(sizes)),
            },
            "gap_distribution": {k: v for k, v in gap_buckets.items()},
            "word_break_hypothesis": (
                "Wenn viele Gaps > 80px: vermutete Wortgrenzen. "
                "Wenn Verteilung bimodal: klare Segmentierung. "
                f"Tatsächlich: {dict(gap_buckets)}"
            )
        },
        "attack_5_g25_runs": {
            "max_run": max_run,
            "run_distribution": {str(k): v for k, v in sorted(run_counts.items())},
        },
        "interpretation": "Siehe einzelne Hypothesen-Felder pro Attack-Vector.",
    }
    out_path = args.out / "ngram_report.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")

    # === Visualisierung: G25-Kontakt-Heatmap ===
    # Bigramm-Matrix (17x17) zeichnen
    glyphs_sorted = sorted(counts.keys(), key=lambda g: -counts[g])
    n_g = len(glyphs_sorted)
    cell_size = 30
    canvas = Image.new("RGB", (n_g * cell_size + 100, n_g * cell_size + 50), "white")
    draw = ImageDraw.Draw(canvas)
    draw.text((5, 5), f"Bigramm-Matrix (Zeile gefolgt von Spalte), Top-Token: G25 (Zeile 1)", fill="black")

    for i, g_row in enumerate(glyphs_sorted):
        for j, g_col in enumerate(glyphs_sorted):
            count = bigrams.get((g_row, g_col), 0)
            if count > 0:
                # Farbskala: 0=weiß, max=dunkelrot
                intensity = min(255, int(count * 5))
                color = (255, 255 - intensity, 255 - intensity)
                draw.rectangle([
                    50 + j * cell_size, 30 + i * cell_size,
                    50 + (j+1) * cell_size, 30 + (i+1) * cell_size
                ], fill=color, outline="gray")
                if count > 5:
                    draw.text((50 + j * cell_size + 8, 30 + i * cell_size + 8),
                              str(count), fill="black")

    # Labels
    for i, g in enumerate(glyphs_sorted):
        draw.text((5, 30 + i * cell_size + 5), g, fill="blue")
        draw.text((50 + i * cell_size + 5, 30 + n_g * cell_size + 5), g, fill="blue")

    canvas.save(args.out / "bigram_heatmap.png")
    print(f"Wrote {args.out / 'bigram_heatmap.png'}")


if __name__ == "__main__":
    main()
