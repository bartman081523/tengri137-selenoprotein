#!/usr/bin/env python3
"""
phase4_frequency_match.py — V6 Phase 4: Frequency-Match-Test (CryptanalysisMind).

V6 PIVOT: Vergleicht Tengri-Glyph-Frequenzen mit Sprach-Referenz-Statistiken
(Englisch, Türkisch, Mongolisch, Deutsch) via Pearson-Korrelation.

Output: bbox/frequency_match_20260706_V6/freq_match.json
        {
          "english": {"pearson_r": 0.83, "rank_match_score": 0.71, "top_letters_match": [...]},
          "turkish": {...},
          ...
          "best_match": "english"
        }
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path


# Sprach-Referenz-Statistiken (Buchstabenhäufigkeiten)
LANG_FREQS = {
    "english": {
        "E": 0.1270, "T": 0.0906, "A": 0.0817, "O": 0.0751, "I": 0.0697,
        "N": 0.0675, "S": 0.0633, "H": 0.0609, "R": 0.0599, "D": 0.0425,
        "L": 0.0403, "C": 0.0278, "U": 0.0276, "M": 0.0241, "W": 0.0236,
        "F": 0.0223, "G": 0.0202, "Y": 0.0197, "P": 0.0193, "B": 0.0149,
        "V": 0.0098, "K": 0.0077, "J": 0.0015, "X": 0.0015, "Q": 0.0010,
        "Z": 0.0007,
    },
    "turkish": {
        "A": 0.1213, "I": 0.0985, "E": 0.0908, "N": 0.0796, "R": 0.0672,
        "L": 0.0592, "T": 0.0540, "K": 0.0463, "M": 0.0375, "D": 0.0370,
        "Y": 0.0335, "S": 0.0300, "B": 0.0284, "O": 0.0254, "U": 0.0251,
        "Ş": 0.0179, "H": 0.0126, "C": 0.0116, "Z": 0.0094, "G": 0.0085,
        "V": 0.0094, "Ç": 0.0085, "Ğ": 0.0067, "Ö": 0.0035, "İ": 0.0034,
        "Ü": 0.0034, "P": 0.0023, "F": 0.0023,
    },
    "german": {
        "E": 0.1740, "N": 0.0978, "I": 0.0755, "S": 0.0727, "R": 0.0700,
        "A": 0.0651, "T": 0.0615, "D": 0.0508, "H": 0.0476, "U": 0.0435,
        "L": 0.0344, "C": 0.0290, "G": 0.0300, "M": 0.0253, "O": 0.0251,
        "B": 0.0189, "W": 0.0189, "F": 0.0166, "K": 0.0121, "Z": 0.0113,
        "P": 0.0079, "V": 0.0067, "J": 0.0027, "Y": 0.0004, "X": 0.0004,
        "Q": 0.0002,
    },
    "mongolian_cyrillic": {
        "А": 0.1310, "Н": 0.0990, "Э": 0.0880, "О": 0.0810, "Т": 0.0750,
        "И": 0.0680, "Б": 0.0600, "Х": 0.0540, "С": 0.0490, "Г": 0.0460,
        "Д": 0.0420, "Е": 0.0380, "Л": 0.0340, "М": 0.0310, "Я": 0.0280,
        "П": 0.0250, "У": 0.0230, "В": 0.0210, "Й": 0.0190, "К": 0.0170,
        "Ы": 0.0150, "Ш": 0.0130, "Ь": 0.0110, "З": 0.0090, "Ч": 0.0070,
        "Ц": 0.0050, "Ё": 0.0030, "Ф": 0.0010,
    },
}


def pearson(x: list, y: list) -> float:
    """Pearson-Korrelations-Koeffizient."""
    n = len(x)
    if n < 2:
        return 0.0
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den_x = sum((x[i] - mean_x) ** 2 for i in range(n))
    den_y = sum((y[i] - mean_y) ** 2 for i in range(n))
    if den_x == 0 or den_y == 0:
        return 0.0
    return num / math.sqrt(den_x * den_y)


def rank_match_score(glyph_freqs: list, lang_freqs: dict) -> float:
    """Anteil der Top-K Glyphen, die in der gleichen Rang-Position wie die Top-K Buchstaben der Sprache sind."""
    # Top-K = n_glyphs (oder n_letters, je nachdem was kleiner ist)
    k = min(len(glyph_freqs), len(lang_freqs))
    if k == 0:
        return 0.0
    # Sort by freq desc
    sorted_glyphs = [g for g, _ in sorted(glyph_freqs, key=lambda x: -x[1])]
    sorted_letters = [l for l, _ in sorted(lang_freqs.items(), key=lambda x: -x[1])]
    # Top-K
    top_g = set(sorted_glyphs[:k])
    top_l = set(sorted_letters[:k])
    return len(top_g & top_l) / k


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True)
    ap.add_argument("--crypto-report", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # Token-Frequenzen sammeln
    fliesstext = ["p01", "p02", "p03", "p04", "p07", "p08", "p09", "p10",
                 "p11", "p12", "p13", "p14", "p15", "p16"]
    all_tokens = []
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        if pid not in fliesstext:
            continue
        all_tokens.extend(t["glyph_id"] for t in d["tokens"])

    counts = Counter(all_tokens)
    n_total = len(all_tokens)
    glyph_freqs = [(gid, c / n_total) for gid, c in counts.items()]

    print(f"Analyse: {n_total} Tokens, {len(glyph_freqs)} unique Glyphen\n")

    # Frequency-Match pro Sprache
    results = {}
    for lang, ref in LANG_FREQS.items():
        # Mappe Tengri-Glyphs (sortiert nach Frequenz) auf Sprach-Buchstaben (sortiert nach Frequenz)
        sorted_glyphs = sorted(glyph_freqs, key=lambda x: -x[1])
        sorted_letters = sorted(ref.items(), key=lambda x: -x[1])
        n = min(len(sorted_glyphs), len(sorted_letters))
        # Vektoren für Pearson
        g_vec = [g[1] for g in sorted_glyphs[:n]]
        l_vec = [l[1] for l in sorted_letters[:n]]
        r = pearson(g_vec, l_vec)
        rms = rank_match_score(glyph_freqs, ref)
        # Top-5 Vergleich
        top5_g = [(g, round(f, 4)) for g, f in sorted_glyphs[:5]]
        top5_l = [(l, round(f, 4)) for l, f in sorted_letters[:5]]
        results[lang] = {
            "pearson_r": round(r, 4),
            "rank_match_score": round(rms, 4),
            "top5_tengri": top5_g,
            "top5_lang": top5_l,
        }
        print(f"  {lang:20s}: pearson={r:+.4f}, rank_match={rms:.2%}")
        print(f"    Tengri top5: {top5_g}")
        print(f"    Lang   top5: {top5_l}")

    # Best match
    best = max(results.items(), key=lambda x: x[1]["pearson_r"])
    print(f"\nBest match: {best[0]} (pearson_r = {best[1]['pearson_r']:.4f})")

    # Output
    output = {
        "metadata": {
            "n_tokens": n_total,
            "n_unique_glyphs": len(glyph_freqs),
            "fliesstext_pages": len(fliesstext),
            "method": "Pearson-Korrelation sortierter Frequenz-Vektoren + Rank-Match"
        },
        "language_correlations": results,
        "best_match": {
            "language": best[0],
            "pearson_r": best[1]["pearson_r"],
            "interpretation": (
                f"Die Tengri-Glyph-Frequenzen korrelieren am stärksten mit {best[0]} "
                f"(r={best[1]['pearson_r']:.4f}). "
                f"Das stützt die Hypothese, dass Tengri ein Substitutions-Alphabet für diese Sprache ist."
                if best[1]["pearson_r"] > 0.5
                else f"Keine starke Korrelation mit einer getesteten Sprache. "
                     f"Best match: {best[0]} mit r={best[1]['pearson_r']:.4f}. "
                     f"Tengri könnte ein nicht-lateinisches Alphabet oder ein Silbensystem sein."
            )
        }
    }
    out_path = args.out / "freq_match.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
