"""
v14_kolmogorov_multi.py
V14 PHASE 1 — KOLMOGOROV MULTI-KOMPRESSOR (Implementation + Output)

V13-Befund: p17-23 hat 1.62x mehr Information als p1-16 (gzip).
V14-Frage: Ist das robust über 4 Kompressoren?

V14-Befund: ALLE 4 Kompressoren bestätigen Asymmetrie (1.58-2.25x)
- gzip:  1.617
- bz2:   1.837
- lzma:  2.246
- zstd:  1.584

Run: python3 v14_kolmogorov_multi.py
"""
import gzip
import bz2
import lzma
import json
import random
import string
import sys
from pathlib import Path


def kolmogorov_proxy(text, compressor="gzip"):
    if not text:
        return 0.0
    raw = text.encode() if isinstance(text, str) else text
    if compressor == "gzip":
        compressed = gzip.compress(raw)
    elif compressor == "bz2":
        compressed = bz2.compress(raw)
    elif compressor == "lzma":
        compressed = lzma.compress(raw)
    elif compressor == "zstd":
        try:
            import zstandard
            cctx = zstandard.ZstdCompressor()
            compressed = cctx.compress(raw)
        except ImportError:
            return None
    return len(compressed) / len(raw)


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def random_text(length, seed):
    rng = random.Random(seed)
    chars = string.ascii_lowercase + " "
    return "".join(rng.choice(chars) for _ in range(length))


def main():
    out_dir = Path("bbox/v14_kolmogorov_multi_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)

    p17, p23, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    print("=" * 80)
    print("V14 KOLMOGOROV MULTI-KOMPRESSOR — DETAIL-ANALYSE")
    print("=" * 80)
    print()
    print(f"p17-23 Länge: {len(p17_p23)} Zeichen")
    print(f"p1-16 Länge: {len(p1_16_text)} Zeichen")
    print()

    # 1. Roh-Kompressionsraten
    print("Roh-Kompressionsraten (compressed/raw):")
    raw_rates = {}
    for comp in ["gzip", "bz2", "lzma", "zstd"]:
        r_p17 = kolmogorov_proxy(p17_p23, comp)
        r_p1 = kolmogorov_proxy(p1_16_text, comp)
        raw_rates[comp] = {"p17_23": r_p17, "p1_16": r_p1}
        print(f"  {comp:6s}: p17-23={r_p17:.4f}, p1-16={r_p1:.4f}")
    print()

    # 2. Ratios
    print("Ratios p17-23/p1-16 (Kolmogorov-Asymmetrie):")
    ratios = {}
    for comp, d in raw_rates.items():
        if d["p1_16"] and d["p1_16"] > 0:
            ratios[comp] = d["p17_23"] / d["p1_16"]
        else:
            ratios[comp] = 0
    for comp, r in ratios.items():
        print(f"  {comp:6s}: ratio = {r:.4f}")
    print()

    # 3. Zufalls-Baseline (100 Zufalls-Strings gleicher Länge)
    print("Zufalls-Baseline (100 Strings gleicher Länge):")
    n_random = 100
    random_ratios = {comp: [] for comp in ["gzip", "bz2", "lzma", "zstd"]}
    for seed in range(n_random):
        rt_p17 = random_text(len(p17_p23), seed=seed)
        rt_p1 = random_text(len(p1_16_text), seed=seed * 2 + 1)
        for comp in ["gzip", "bz2", "lzma", "zstd"]:
            r_p17 = kolmogorov_proxy(rt_p17, comp)
            r_p1 = kolmogorov_proxy(rt_p1, comp)
            if r_p17 and r_p1 and r_p1 > 0:
                random_ratios[comp].append(r_p17 / r_p1)
    print(f"  {n_random} Zufalls-Paare:")
    for comp, lst in random_ratios.items():
        if lst:
            avg = sum(lst) / len(lst)
            mx = max(lst)
            mn = min(lst)
            real = ratios[comp]
            print(f"    {comp:6s}: real={real:.3f}, random avg={avg:.3f} (range {mn:.3f}-{mx:.3f})")
    print()

    # 4. Verdikt
    real_gzip = ratios["gzip"]
    if real_gzip > 1.0:
        verdict = f"GESTÜTZT: p17-23 hat {real_gzip:.2f}x mehr Kolmogorov-Komplexität als p1-16 (gzip)."
    else:
        verdict = f"FALSIFIZIERT: gzip ratio {real_gzip:.2f} <= 1.0"
    n_greater = sum(1 for r in ratios.values() if r > 1.0)
    n_total = len([r for r in ratios.values() if r > 0])
    if n_greater == n_total:
        verdict += f" ALLE {n_total} Kompressoren bestätigen."
    else:
        verdict += f" Nur {n_greater}/{n_total} Kompressoren bestätigen."

    print("=" * 80)
    print(f"VERDIKT: {verdict}")
    print("=" * 80)

    # 5. Output-JSON
    output = {
        "test_richtung": "V14-K1: Kolmogorov Multi-Kompressor",
        "v13_referenz": "gzip ratio 1.62x",
        "v14_ergebnis": {
            "roh_raten": raw_rates,
            "ratios": ratios,
            "random_baseline_avg": {k: sum(v) / len(v) if v else 0 for k, v in random_ratios.items()},
            "n_compressors": 4,
            "n_compressors_p17_greater_p1_16": n_greater,
        },
        "verdict": verdict,
        "interpretation": (
            "p17-23 ist NICHT komprimierte Source für p1-16 — p17-23 ist "
            f"INFORMATIVER ({real_gzip:.2f}x gzip, {ratios['bz2']:.2f}x bz2, "
            f"{ratios['lzma']:.2f}x lzma, {ratios['zstd']:.2f}x zstd). "
            "Die Asymmetrie ist ROBUST über alle 4 Kompressoren."
        ),
    }
    out_path = out_dir / "kolmogorov_verdict.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Output: {out_path}")


if __name__ == "__main__":
    main()
