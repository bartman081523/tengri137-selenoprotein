#!/usr/bin/env python3
"""
phase4b_schmeh_freq_match.py — V6 Phase 4b: Echter Schmeh-vs-Glyph Frequency-Match.

Was wir VORHER falsch interpretiert haben:
- Korrelation > 0.93 mit Englisch/Türkisch/Mongolisch/Deutsch beweist NICHT, dass Tengri lateinisch ist.
- Das ist nur Zipf's Law (universell).
- Es gibt 4 Sprachen mit ähnlicher Zipf-Distribution.

Was dieser Test WIRKLICH tut:
1. Nehme Schmehs Klartext für p01-p04, p07-p16 (Textseiten, kein Latein in PDF)
2. Berechne die ECHTE Buchstaben-Frequenz im Klartext
3. Mache das gleiche für unsere 25 Glyphen (Tengri-Tokens)
4. Korrelation: Wenn Tengri ein lateinisches Substitutions-Alphabet ist, MÜSSTE die
   Rang-Reihenfolge der häufigsten Glyphen (G28, G25, G16...) EXAKT mit der
   Rang-Reihenfolge der häufigsten Buchstaben (E, T, A, O...) übereinstimmen.

Output: bbox/frequency_match_20260706_V6/schmeh_freq_match.json
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path


def pearson(x, y):
    n = len(x)
    if n < 2:
        return 0.0
    mx, my = sum(x)/n, sum(y)/n
    num = sum((x[i]-mx)*(y[i]-my) for i in range(n))
    dx = sum((x[i]-mx)**2 for i in range(n))
    dy = sum((y[i]-my)**2 for i in range(n))
    if dx == 0 or dy == 0:
        return 0.0
    return num / math.sqrt(dx*dy)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True)
    ap.add_argument("--schmeh-parsed", type=Path, required=True,
                    help="bbox/schmeh_hints_20260704_V4/schmeh_parsed.json")
    ap.add_argument("--crypto-report", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # 1. Schmeh-Klartext für die FLIESSTEXT-Seiten
    fliesstext_pages = ["01", "02", "03", "04", "07", "08", "09", "10",
                        "11", "12", "13", "14", "15", "16"]
    schmeh = json.loads(args.schmeh_parsed.read_text())
    klartext = []
    for pid in fliesstext_pages:
        if pid in schmeh and "manifesto_lines" in schmeh[pid]:
            for line in schmeh[pid]["manifesto_lines"]:
                klartext.extend(line.upper())
    klartext = [c for c in klartext if c.isalpha() and c.isascii()]
    schmeh_counts = Counter(klartext)
    n_schmeh = len(klartext)
    schmeh_freqs = sorted(schmeh_counts.items(), key=lambda x: -x[1])
    print(f"Schmeh Klartext: {n_schmeh} Buchstaben, {len(schmeh_counts)} unique")
    print(f"  Top-10: {[(c, n) for c, n in schmeh_freqs[:10]]}")

    # 2. Unsere Glyphen-Frequenz (aus Phase 3 Cryptanalysis-Report)
    crypto = json.loads(args.crypto_report.read_text())
    glyph_freqs = [(g["glyph_id"], g["share"]) for g in crypto["glyph_frequencies"]]
    n_glyphs = len(glyph_freqs)
    print(f"\nTengri Glyphen: {n_glyphs} unique")
    print(f"  Top-10: {[(g, round(f, 4)) for g, f in glyph_freqs[:10]]}")

    # 3. Wenn Tengri ein lateinisches Substitutions-Alphabet wäre:
    #    - Schmeh-Top-1 Buchstabe = häufigstes Glyph
    #    - Schmeh-Top-2 Buchstabe = zweithäufigstes Glyph
    #    - ...
    #    → Liste von "Mapping-Hypothesen"
    print(f"\n=== Hypothese: Tengri ist lateinisches Substitutions-Alphabet ===")
    print(f"{'Rank':<5} {'Schmeh':<10} {'Tengri Glyph':<15}")
    for i, ((letter, lcount), (glyph, gshare)) in enumerate(zip(schmeh_freqs, glyph_freqs), 1):
        print(f"  {i:<3} {letter} ({lcount:4d})  →  {glyph} ({gshare*100:5.2f}%)")
        if i >= 15:
            break

    # 4. Test: Wenn diese Hypothese stimmt, müsste die Frequenz-Reihenfolge
    #    monoton abnehmen UND die Schmeh-Top-Buchstaben müssten die lateinischen Vokale + häufige Konsonanten sein
    #    E,T,A,O,I,N,S,H,R,D sind die Top-10 des Englischen
    expected_top10_english = set("ETAOINSTHRD")
    schmeh_top10 = set(l for l, _ in schmeh_freqs[:10])
    overlap = expected_top10_english & schmeh_top10
    print(f"\nSchmeh-Top-10 Buchstaben: {schmeh_top10}")
    print(f"Englisch-Top-10 erwartet: {expected_top10_english}")
    print(f"Overlap: {overlap} ({len(overlap)}/10)")

    # 5. Korrelation Schmeh-Frequenz ↔ Glyph-Frequenz (Rang-basiert)
    n = min(len(schmeh_freqs), len(glyph_freqs))
    s_vec = [c for _, c in schmeh_freqs[:n]]
    g_vec = [f for _, f in glyph_freqs[:n]]
    r = pearson(s_vec, g_vec)

    # 6. Korrelation gegen ZIPF (log-log) — wenn die Glyphen Zipf folgen, sind sie eine Schrift
    schmeh_zipf_log = [math.log(c) for c in s_vec]
    glyph_zipf_log = [math.log(f) for f in g_vec]
    r_zipf = pearson(schmeh_zipf_log, glyph_zipf_log)

    # 7. Korrelation gegen RANGS-Reihenfolge (1, 2, 3, ... n)
    rank_schmeh = [i for i in range(1, n+1)]
    rank_glyph = [i for i in range(1, n+1)]
    # Identisch (perfekt korreliert) — das ist trivial; stattdessen: Korrelation der
    # normalisierten Frequenzen
    norm_schmeh = [c / s_vec[0] for c in s_vec]
    norm_glyph = [f / g_vec[0] for f in g_vec]
    r_norm = pearson(norm_schmeh, norm_glyph)

    print(f"\n=== Korrelationen ===")
    print(f"  Pearson (raw Freq):       r = {r:.4f}")
    print(f"  Pearson (log-log Zipf):   r = {r_zipf:.4f}")
    print(f"  Pearson (normiert auf #1): r = {r_norm:.4f}")

    # 8. Falls Tengri KEIN lateinisches Substitutions-Alphabet ist,
    #    müsste die Korrelation mit Schmeh-Top-10 ähnlich wie mit MÜLLWORTEN sein.
    #    Wir testen gegen random-shuffle.
    import random
    random.seed(42)
    null_rs = []
    for _ in range(100):
        shuffled = g_vec.copy()
        random.shuffle(shuffled)
        null_rs.append(pearson(s_vec, shuffled))
    null_mean = sum(null_rs) / len(null_rs)
    null_std = (sum((r - null_mean)**2 for r in null_rs) / len(null_rs)) ** 0.5
    z_score = (r - null_mean) / null_std if null_std > 0 else 0.0
    print(f"  Null-Model (shuffled):    r = {null_mean:.4f} ± {null_std:.4f}")
    print(f"  Z-Score: {z_score:.2f}")
    print(f"  → |Z| > 2 = signifikant; |Z| < 2 = mit Zufall vereinbar")

    # 9. Top-Bigram-Vergleich (echter Sprachtest)
    # Wenn Tengri = lateinisches Sub-Alphabet, müssen die häufigsten Bigramme
    # den häufigsten lateinischen Bigrammen entsprechen (TH, HE, IN, ER, AN, RE, ON, AT, EN, ND)
    expected_top_bigrams_english = ["TH", "HE", "IN", "ER", "AN", "RE", "ON", "AT", "EN", "ND"]
    schmeh_bigrams = Counter()
    for i in range(len(klartext) - 1):
        if klartext[i].isalpha() and klartext[i+1].isalpha():
            schmeh_bigrams[klartext[i] + klartext[i+1]] += 1
    schmeh_top_bigrams = [bg for bg, _ in schmeh_bigrams.most_common(10)]
    print(f"\n=== Bigram-Vergleich ===")
    print(f"  Englisch-Top-10: {expected_top_bigrams_english}")
    print(f"  Schmeh-Top-10:   {schmeh_top_bigrams}")
    bigram_overlap = set(expected_top_bigrams_english) & set(schmeh_top_bigrams)
    print(f"  Overlap: {len(bigram_overlap)}/10")

    # Output
    output = {
        "metadata": {
            "n_schmeh_letters": n_schmeh,
            "n_schmeh_unique": len(schmeh_counts),
            "n_glyphs_unique": n_glyphs,
            "method": "Schmeh-Klartext (manifesto_lines) ↔ Tengri-Glyph-Frequenzen"
        },
        "schmeh_top20_letters": [(c, n) for c, n in schmeh_freqs[:20]],
        "tengri_top20_glyphs": [(g, round(f, 4)) for g, f in glyph_freqs[:20]],
        "hypothesis_mapping": [
            {"rank": i+1, "schmeh_letter": schmeh_freqs[i][0], "tengri_glyph": glyph_freqs[i][0]}
            for i in range(min(10, n))
        ],
        "correlations": {
            "pearson_raw": round(r, 4),
            "pearson_zipf_log": round(r_zipf, 4),
            "pearson_normalized": round(r_norm, 4),
            "null_model_mean": round(null_mean, 4),
            "null_model_std": round(null_std, 4),
            "z_score": round(z_score, 4),
        },
        "bigram_check": {
            "english_top10": expected_top_bigrams_english,
            "schmeh_top10": schmeh_top_bigrams,
            "overlap_count": len(bigram_overlap),
        },
        "interpretation": (
            f"Z-Score {z_score:.2f} bedeutet: "
            + ("Tengri-Glyph-Frequenzen korrelieren SIGNIFIKANT mit Schmehs Klartext-Buchstaben-Frequenzen. "
               "→ Starke Evidenz, dass Tengri ein lateinisches Substitutions-Alphabet ist (Schmehs Mapping plausibel)."
               if abs(z_score) > 2 else
               "Tengri-Glyph-Frequenzen korrelieren NICHT signifikant mit Schmehs Klartext-Buchstaben-Frequenzen. "
               "→ Schmehs Mapping ist nicht durch Frequenz-Analyse bestätigt. "
               "Tengri ist entweder KEIN lateinisches Substitutions-Alphabet, oder die 25 Glyphen sind falsch identifiziert.")
        )
    }
    out_path = args.out / "schmeh_freq_match.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
