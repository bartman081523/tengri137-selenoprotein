#!/usr/bin/env python3
"""
phase3_cryptanalysis_v6.py — V6 Phase 3: Echte Cryptanalysis (CryptanalysisMind).

V6 PIVOT: Cryptanalysis auf dem ECHTEN Token-Stream (NICHT auf Inken-Strichen wie V5).
Berechnet Shannon-H, IoC, Zipf-α, N-Gramme pro Page und gesamt.

Output: bbox/cryptanalysis_20260706_V6/crypto_report.json
"""
import argparse
import json
import math
from collections import Counter
from pathlib import Path


def shannon_entropy(tokens: list) -> float:
    """H = -Σ p_i log2(p_i)"""
    if not tokens:
        return 0.0
    n = len(tokens)
    counts = Counter(tokens)
    h = 0.0
    for c in counts.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def index_of_coincidence(tokens: list) -> float:
    """IoC = Σ n_i(n_i-1) / N(N-1)"""
    n = len(tokens)
    if n < 2:
        return 0.0
    counts = Counter(tokens)
    return sum(c * (c - 1) for c in counts.values()) / (n * (n - 1))


def zipf_alpha(tokens: list) -> float:
    """Zipf'scher Exponent α via linearem Fit auf log(freq) vs log(rank)."""
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    freqs = sorted(counts.values(), reverse=True)
    n = len(freqs)
    if n < 2:
        return 0.0
    # Linearer Fit: log(freq) = -α * log(rank) + c
    log_ranks = [math.log(r + 1) for r in range(n)]
    log_freqs = [math.log(f) for f in freqs]
    # Least squares
    mean_x = sum(log_ranks) / n
    mean_y = sum(log_freqs) / n
    num = sum((log_ranks[i] - mean_x) * (log_freqs[i] - mean_y) for i in range(n))
    den = sum((log_ranks[i] - mean_x) ** 2 for i in range(n))
    if den == 0:
        return 0.0
    slope = num / den
    return -slope  # α = -slope


def bigrams(tokens: list) -> list:
    """Top-50 Bigramme (sortiert nach Frequenz)."""
    if len(tokens) < 2:
        return []
    bg = Counter()
    for i in range(len(tokens) - 1):
        bg[(tokens[i], tokens[i + 1])] += 1
    return bg.most_common(50)


def analyze_tokens(all_tokens: list) -> dict:
    """Cryptanalysis auf Token-Stream."""
    h = shannon_entropy(all_tokens)
    ioc = index_of_coincidence(all_tokens)
    alpha = zipf_alpha(all_tokens)
    bg = bigrams(all_tokens)

    # Glyph-Frequenzen
    counts = Counter(all_tokens)
    n_total = len(all_tokens)
    n_unique = len(counts)
    freqs = sorted(counts.items(), key=lambda x: -x[1])

    # Top-Token-Anteil (misst Ungleichverteilung)
    top_token_share = freqs[0][1] / n_total if freqs else 0

    return {
        "n_tokens_total": n_total,
        "n_tokens_unique": n_unique,
        "shannon_entropy": h,
        "ioc": ioc,
        "zipf_alpha": alpha,
        "top_token_share": top_token_share,
        "top_bigrams": [
            {"bigram": f"{a}-{b}", "count": c} for (a, b), c in bg[:20]
        ],
        "glyph_frequencies": [
            {"glyph_id": gid, "count": c, "share": c / n_total}
            for gid, c in freqs
        ],
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True,
                    help="bbox/tokenstream_20260706_V6_v2/")
    ap.add_argument("--out", type=Path, required=True,
                    help="bbox/cryptanalysis_20260706_V6/")
    ap.add_argument("--fliesstext-only", action="store_true",
                    help="Nur Fließtext-Pages (p01-p04, p07-p16)")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # 1. Fließtext-Pages
    fliesstext = ["p01", "p02", "p03", "p04", "p07", "p08", "p09", "p10",
                 "p11", "p12", "p13", "p14", "p15", "p16"]

    # 2. Token-Streams laden
    all_tokens = []
    per_page = {}
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        tokens = [t["glyph_id"] for t in d["tokens"]]
        per_page[pid] = tokens
        if args.fliesstext_only and pid not in fliesstext:
            continue
        all_tokens.extend(tokens)

    # 3. Gesamt-Analyse
    print(f"Analysiere {len(all_tokens)} Tokens (fliesstext_only={args.fliesstext_only})")
    result = analyze_tokens(all_tokens)
    result["fliesstext_only"] = args.fliesstext_only
    result["pages_included"] = [p for p in sorted(per_page.keys())
                                if not args.fliesstext_only or p in fliesstext]

    # 4. Per-Page-Analyse
    per_page_stats = {}
    for pid, tokens in per_page.items():
        if args.fliesstext_only and pid not in fliesstext:
            continue
        per_page_stats[pid] = {
            "n_tokens": len(tokens),
            "shannon_entropy": shannon_entropy(tokens),
            "ioc": index_of_coincidence(tokens),
            "zipf_alpha": zipf_alpha(tokens),
        }
    result["per_page"] = per_page_stats

    # 5. Vergleich mit V5 (falsifiziert)
    result["v5_comparison"] = {
        "v5_falsifiziert": True,
        "v5_h_war": 2.8706,
        "v5_ioc_war": 0.1606,
        "v5_alpha_war": 2.9281,
        "interpretation": (
            "V5 hat auf Inken-Strichen (16.797 Connected Components) gerechnet. "
            "V6 rechnet auf Glyphen-Tokens (~1690 für Fließtext-Pages). "
            "Falls V6-IoC ≈ 0.065 und V6-H ≈ 4.0, ist V5 als 'Font-Redundanz-Statistik' bestätigt."
        )
    }

    # 6. Englisch-Referenz
    result["english_reference"] = {
        "shannon_entropy": 4.14,
        "ioc": 0.067,
        "zipf_alpha": 1.0,
        "top_letter_freq": {"E": 0.127, "T": 0.091, "A": 0.082, "O": 0.075, "I": 0.070}
    }

    out_path = args.out / "crypto_report.json"
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False))

    # 7. Print
    print(f"\n=== V6 Cryptanalysis (echte Glyphen-Tokens) ===")
    print(f"  N Tokens:        {result['n_tokens_total']}")
    print(f"  N unique Glyphen: {result['n_tokens_unique']}")
    print(f"  Shannon H:        {result['shannon_entropy']:.4f}  (Englisch-Ref: 4.14)")
    print(f"  IoC:              {result['ioc']:.4f}  (Englisch-Ref: 0.067)")
    print(f"  Zipf α:           {result['zipf_alpha']:.4f}  (Englisch-Ref: 1.0)")
    print(f"  Top-Token share:  {result['top_token_share']:.3f}")
    print()
    print(f"Top-5 Glyphen:")
    for g in result["glyph_frequencies"][:5]:
        print(f"  {g['glyph_id']}: {g['count']:3d} ({g['share']*100:.1f}%)")
    print()
    print(f"Top-5 Bigramme:")
    for b in result["top_bigrams"][:5]:
        print(f"  {b['bigram']}: {b['count']}")
    print()
    print(f"V5 vs V6:")
    print(f"  V5 H (Striche):  {result['v5_comparison']['v5_h_war']:.4f}")
    print(f"  V6 H (Glyphen):  {result['shannon_entropy']:.4f}  → Differenz: {result['v5_comparison']['v5_h_war'] - result['shannon_entropy']:.4f}")
    print(f"  V5 IoC (Striche): {result['v5_comparison']['v5_ioc_war']:.4f}")
    print(f"  V6 IoC (Glyphen): {result['ioc']:.4f}  → Differenz: {result['v5_comparison']['v5_ioc_war'] - result['ioc']:.4f}")
    print()
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
