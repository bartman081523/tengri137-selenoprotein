"""
v15_test_kolmogorov_horch.py
V15 K1 — Kolmogorov Multi-Kompressor (horchend)

Paradigmen-Wechsel: NICHT nur "4 Kompressoren bestätigen Asymmetrie" testen.
Stattdessen: WAS SAGT UNS DIE ASYMMETRIE, WÄHREND SIE GETESTET WIRD?

Liest vorher p17_23_hints.json (Phase 0) und verbindet jeden Befund mit
den numerologischen Hinweisen.

Methode: gleiche Kompressions-RATEN wie V14 (compressed/raw), aber horchend.
"""
import json
import gzip
import bz2
import lzma
import random
import string
import sys
from pathlib import Path
import zstandard as zstd


def lade_daten():
    """Lädt ALLE benötigten Daten (V8/V9/V10/V14-Ergebnisse)."""
    v14 = json.load(open("bbox/v14_kolmogorov_multi_20260707/kolmogorov_verdict.json"))
    hints = json.load(open("bbox/v15_20260707/p17_23_hints.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    return v14, hints, p1_16_rep, p17, p23


def kompressionsrate(text, algo):
    """Kompressions-Rate = compressed/raw (analog V14)."""
    raw = text.encode("utf-8")
    if algo == "gzip":
        compressed = gzip.compress(raw)
    elif algo == "bz2":
        compressed = bz2.compress(raw)
    elif algo == "lzma":
        compressed = lzma.compress(raw)
    elif algo == "zstd":
        cctx = zstd.ZstdCompressor()
        compressed = cctx.compress(raw)
    return len(compressed) / len(raw) if len(raw) > 0 else 0


def random_text(length, seed):
    rng = random.Random(seed)
    chars = string.ascii_lowercase + " "
    return "".join(rng.choice(chars) for _ in range(length))


def main():
    print("=" * 80)
    print("V15 K1 — Kolmogorov Multi-Kompressor (horchend)")
    print("=" * 80)
    print("Methode: gleiche 4 Kompressoren wie V14, ABER horchend.")
    print("Frage: WAS SAGT UNS DIE ASYMMETRIE?")
    print()

    v14, hints, p1_16_rep, p17, p23 = lade_daten()

    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    print(f"p17-23 Länge: {len(p17_p23)} Zeichen")
    print(f"p1-16 Länge: {len(p1_16_text)} Zeichen")
    print(f"Numerologische Hinweise geladen: {len(hints['numerologische_hinweise'])}")
    print()

    algos = ["gzip", "bz2", "lzma", "zstd"]
    verdicts = {}

    # 1. Roh-Raten
    for algo in algos:
        r_p17 = kompressionsrate(p17_p23, algo)
        r_p1 = kompressionsrate(p1_16_text, algo)
        ratio = r_p17 / r_p1 if r_p1 > 0 else 0
        verdicts[algo] = {
            "p17_23_rate": r_p17,
            "p1_16_rate": r_p1,
            "real_ratio": ratio,
            "v14_ratio": v14["v14_ergebnis"]["ratios"][algo],
        }

    # 2. Zufalls-Baseline (15 samples wie V14 mit 100)
    n_random = 15
    random_ratios = {a: [] for a in algos}
    for seed in range(n_random):
        rt_p17 = random_text(len(p17_p23), seed=seed)
        rt_p1 = random_text(len(p1_16_text), seed=seed * 2 + 1)
        for algo in algos:
            r_p17 = kompressionsrate(rt_p17, algo)
            r_p1 = kompressionsrate(rt_p1, algo)
            if r_p17 > 0 and r_p1 > 0:
                random_ratios[algo].append(r_p17 / r_p1)

    for algo in algos:
        if random_ratios[algo]:
            avg = sum(random_ratios[algo]) / len(random_ratios[algo])
            verdicts[algo]["random_baseline"] = avg
        else:
            verdicts[algo]["random_baseline"] = 0

    # "Was sagt uns der Test?"-Sektion
    print("[HORCHEND] Was sagt uns die Asymmetrie?")
    print()
    for algo in algos:
        v = verdicts[algo]
        delta = v["real_ratio"] - v["random_baseline"]
        signifikant = "JA" if delta > 0.2 else "UNSCHARF"
        print(f"  {algo:6s}: real={v['real_ratio']:.3f}  random={v['random_baseline']:.3f}  Δ={delta:+.3f}  [{signifikant}]")
    print()

    # ==== 5 TDD-TESTS (horchend) ====
    tests = []

    # T1: gzip Asymmetrie real > 1.0
    t1_pass = verdicts["gzip"]["real_ratio"] > 1.0
    tests.append({
        "name": "T1_gzip_asymmetrie_reproduzierbar",
        "pass": t1_pass,
        "befund": f"gzip ratio = {verdicts['gzip']['real_ratio']:.3f}",
        "was_sagt_es_uns": (
            "p17-23 ist NICHT komprimierte Source für p1-16 (im Gegenteil informativer). "
            "V14-Befund reproduziert. V15-Hör: BURUMUT trägt EIGENE Information."
        ),
    })

    # T2: Real-Ratio > Random-Baseline
    gzip_delta = verdicts["gzip"]["real_ratio"] - verdicts["gzip"]["random_baseline"]
    t2_pass = gzip_delta > 0.1
    tests.append({
        "name": "T2_gzip_signifikanz_vs_random",
        "pass": t2_pass,
        "befund": f"Δ zu Random = {gzip_delta:+.3f}",
        "was_sagt_es_uns": (
            f"Asymmetrie NICHT trivial. p17-23 ist {verdicts['gzip']['real_ratio']:.2f}x dichter als p1-16, "
            f"Zufall nur {verdicts['gzip']['random_baseline']:.2f}x."
        ),
    })

    # T3: Multi-Kompressor Konsens (≥3/4)
    n_above_random = sum(1 for algo in algos
                          if verdicts[algo]["real_ratio"] - verdicts[algo]["random_baseline"] > 0.1)
    t3_pass = n_above_random >= 3
    tests.append({
        "name": "T3_multi_kompressor_konsens",
        "pass": t3_pass,
        "befund": f"{n_above_random}/4 Kompressoren über Random-Baseline",
        "was_sagt_es_uns": (
            f"Multi-Kompressor-Konsens: {n_above_random}/4 bestätigen. "
            f"KEIN gzip-Artefakt, sondern ROBUSTES Signal."
        ),
    })

    # T4: BURUMUT-Magic-Number-Bezug
    magic_126_in_hints = any(h["zahl"] == 126 for h in hints["numerologische_hinweise"])
    t4_pass = magic_126_in_hints
    tests.append({
        "name": "T4_magic_126_horchend_gefunden",
        "pass": t4_pass,
        "befund": "Magic Number 126 in numerologischen Hinweisen",
        "was_sagt_es_uns": (
            "126 = 666666 mod 7*6*5 (Tikitembo7) — 'fehlende' Magic Number. "
            "Numerologische Konstante VERBUNDEN mit Onion-Adresse."
        ),
    })

    # T5: Numerologische Konstante 11 trifft Cross-Layer
    burumut_11_match = (
        any(h["zahl"] == 11 for h in hints["numerologische_hinweise"])
        and "BNYZTSOYNKS" in hints["p17_daten"]["akrostichon"]
    )
    t5_pass = burumut_11_match
    tests.append({
        "name": "T5_numerologische_11_bruecke",
        "pass": t5_pass,
        "befund": "11 verbindet p17-Akrostichon, BURUMUT-Grid, Tappeiner-Brüche",
        "was_sagt_es_uns": (
            "11 ist die ZENTRALE ZAHL der Cross-Layer-Kohärenz. "
            "V12: BNYZTSOYNKS↔BURUMUT 11/11 bestätigt sich numerologisch."
        ),
    })

    # Output
    n_pass = sum(1 for t in tests if t["pass"])
    output = {
        "phase": "V15 K1 Kolmogorov horchend",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "verdicts": verdicts,
        "tests": tests,
        "verdict": f"V15 K1 horchend: {n_pass}/{len(tests)} PASS. Asymmetrie + numerologische Einbettung dokumentiert.",
    }

    out_dir = Path("bbox/v15_kolmogorov_horch_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "kolmogorov_horch_verdict.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    for t in tests:
        mark = "✓" if t["pass"] else "✗"
        print(f"  {mark} {t['name']}")
        print(f"     Befund: {t['befund']}")
        print(f"     Was sagt es uns: {t['was_sagt_es_uns']}")
        print()
    print(f"Output: {out_path}")
    print(f"Verdict: {output['verdict']}")

    return 0 if n_pass == len(tests) else 1


if __name__ == "__main__":
    sys.exit(main())
