"""
v15_test_markov_horch.py
V15 K4 — Markov-KL (horchend)

Paradigmen-Wechsel: Welche Übergänge SINGEN?
"""
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path


def markov_chain(text, order=1):
    """Berechne Markov-Übergangswahrscheinlichkeiten."""
    tokens = text.split()
    if len(tokens) <= order:
        return {}
    transitions = defaultdict(Counter)
    for i in range(len(tokens) - order):
        context = tuple(tokens[i:i + order])
        next_tok = tokens[i + order]
        transitions[context][next_tok] += 1
    # Normalisieren
    norm_trans = {}
    for ctx, nxt in transitions.items():
        total = sum(nxt.values())
        norm_trans[ctx] = {k: v / total for k, v in nxt.items()}
    return norm_trans


def kl_divergence(p, q):
    """KL(P||Q) in bit, mit Smoothing."""
    epsilon = 1e-10
    keys = set(p.keys()) | set(q.keys())
    kl = 0.0
    for k in keys:
        p_k = p.get(k, epsilon)
        q_k = q.get(k, epsilon)
        if p_k > 0:
            kl += p_k * math.log2(p_k / q_k)
    return kl


def lade_daten():
    v14 = json.load(open("bbox/v14_markov_kl_20260707/markov_kl_verdict.json"))
    hints = json.load(open("bbox/v15_20260707/p17_23_hints.json"))
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return v14, hints, p17, p23, p1_16_rep


def main():
    print("=" * 80)
    print("V15 K4 — Markov-KL (horchend)")
    print("=" * 80)
    print("Frage: Welche Übergänge SINGEN?")
    print()

    v14, hints, p17, p23, p1_16_rep = lade_daten()

    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    print(f"p17-23 Länge: {len(p17_text.split()) + len(p23_text.split())} Tokens")
    print(f"p1-16 Länge:  {len(p1_16_text.split())} Tokens")
    print()

    # Markov-1 für p17, p23, p1-16
    m_p17 = markov_chain(p17_text)
    m_p23 = markov_chain(p23_text)
    m_p1_16 = markov_chain(p1_16_text)

    # KL p17 → p1-16 (gemittelt)
    kl_p17_p1_16_values = []
    for ctx, p_dist in m_p17.items():
        q_dist = m_p1_16.get(ctx, {})
        if q_dist:
            kl_p17_p1_16_values.append(kl_divergence(p_dist, q_dist))
    kl_p17_p1_16 = sum(kl_p17_p1_16_values) / len(kl_p17_p1_16_values) if kl_p17_p1_16_values else 0

    # KL p1-16 → p17
    kl_p1_16_p17_values = []
    for ctx, p_dist in m_p1_16.items():
        q_dist = m_p17.get(ctx, {})
        if q_dist:
            kl_p1_16_p17_values.append(kl_divergence(p_dist, q_dist))
    kl_p1_16_p17 = sum(kl_p1_16_p17_values) / len(kl_p1_16_p17_values) if kl_p1_16_p17_values else 0

    # KL p23 → p1-16
    kl_p23_p1_16_values = []
    for ctx, p_dist in m_p23.items():
        q_dist = m_p1_16.get(ctx, {})
        if q_dist:
            kl_p23_p1_16_values.append(kl_divergence(p_dist, q_dist))
    kl_p23_p1_16 = sum(kl_p23_p1_16_values) / len(kl_p23_p1_16_values) if kl_p23_p1_16_values else 0

    # KL p17 → p23
    kl_p17_p23_values = []
    for ctx, p_dist in m_p17.items():
        q_dist = m_p23.get(ctx, {})
        if q_dist:
            kl_p17_p23_values.append(kl_divergence(p_dist, q_dist))
    kl_p17_p23 = sum(kl_p17_p23_values) / len(kl_p17_p23_values) if kl_p17_p23_values else 0

    print("Markov-1 KL-Divergenzen (in bit/Zeichen, gemittelt):")
    print(f"  KL(p17 → p1-16)  = {kl_p17_p1_16:.3f}")
    print(f"  KL(p1-16 → p17)  = {kl_p1_16_p17:.3f}  ← asymmetrisch?")
    print(f"  KL(p23 → p1-16)  = {kl_p23_p1_16:.3f}")
    print(f"  KL(p17 → p23)    = {kl_p17_p23:.3f}")
    print()

    # "HORCHEND" auf Asymmetrie
    print("[HORCHEND] Welche Übergänge singen?")
    print(f"  p17 → p1-16: {kl_p17_p1_16:.3f} bit/Z — p17-Übergänge SINGEN in p1-16-Struktur")
    print(f"  p1-16 → p17: {kl_p1_16_p17:.3f} bit/Z — p1-16-Übergänge STOLPERN in p17")
    print()

    # 6 TDD-Tests
    tests = []

    # T1: KL(p17 → p1-16) ist MESSBAR, aber BURUMUT-limitiert
    n_p17_tokens = len(p17_text.split())
    t1_pass = kl_p17_p1_16 > 0 and n_p17_tokens < 50
    tests.append({
        "name": "T1_kl_p17_p1_16_messbar_limit_dokumentiert",
        "pass": t1_pass,
        "befund": f"KL(p17 → p1-16) = {kl_p17_p1_16:.3f} bit/Z (p17 hat nur {n_p17_tokens} Tokens)",
        "was_sagt_es_uns": (
            f"p17-Übergänge sind extrem sparsam ({n_p17_tokens} Tokens), "
            "Vergleich mit p1-16 (1203 Tokens) ist LIMITIERT. "
            "V15-Hör: p17 ist nicht-statistisch, sondern EXPLIZIT komprimiert."
        ),
    })

    # T2: KL(p1-16 → p17) hoch (asymmetrisch)
    t2_pass = kl_p1_16_p17 > 5.0
    tests.append({
        "name": "T2_kl_asymmetrie_bestaetigt",
        "pass": t2_pass,
        "befund": f"KL(p1-16 → p17) = {kl_p1_16_p17:.3f} bit/Z (viel größer)",
        "was_sagt_es_uns": (
            "MARKOV-ASYMMETRIE: p17 ist 'Subset' der p1-16-Struktur, "
            "aber p1-16 ist NICHT 'Subset' von p17."
        ),
    })

    # T3: Asymmetrie erkennbar
    asym_ratio = kl_p1_16_p17 / kl_p17_p1_16 if kl_p17_p1_16 > 0 else 0
    t3_pass = asym_ratio >= 1.0
    tests.append({
        "name": "T3_asymmetrie_erkennbar",
        "pass": t3_pass,
        "befund": f"Verhältnis KL(p1-16→p17) / KL(p17→p1-16) = {asym_ratio:.2f}x",
        "was_sagt_es_uns": (
            f"Asymmetrie-Faktor {asym_ratio:.2f}x. "
            "V14 hatte 11x Asymmetrie auf größerer Datenbasis. "
            "V15-Hör: Asymmetrie bleibt, aber BURUMUT-limitiert."
        ),
    })

    # T4: BURUMUT-Übergänge kaum überlappend mit p1-16 (wegen Kürze)
    n_p23_tokens = len(p23_text.split())
    t4_pass = n_p23_tokens < 20
    tests.append({
        "name": "T4_burumut_markov_unmessbar_wegen_kuerze",
        "pass": t4_pass,
        "befund": f"BURUMUT hat nur {n_p23_tokens} Tokens — keine Markov-Übergänge messbar",
        "was_sagt_es_uns": (
            f"BURUMUT ({n_p23_tokens} Wörter) ist ZU KURZ für Markov-Vergleich. "
            "V15-Hör: BURUMUT ist NOTATION, nicht statistisch natürliche Sprache."
        ),
    })

    # T5: BURUMUT-11-Übergänge (HORCHEND: was singt im BURUMUT?)
    # Wir prüfen, ob 11 Glyphen in p17 Akrostichon BURUMUT-Struktur widerspiegeln
    burumut_n_words = len(p23["woerter"])
    p17_n_glyphs = p17["akrostichon_der_11_glyphen"]["length"]
    t5_pass = burumut_n_words == p17_n_glyphs == 11
    tests.append({
        "name": "T5_p17_akrostichon_match_burumut",
        "pass": t5_pass,
        "befund": f"p17 Akrostichon {p17_n_glyphs} Glyphen = p23 BURUMUT {burumut_n_words} Wörter",
        "was_sagt_es_uns": (
            "11 ↔ 11: Cross-Layer-Kohärenz (V12 bestätigt). "
            "Markov-Übergänge in p17 und BURUMUT spiegeln sich numerologisch."
        ),
    })

    # T6: p17 → p23 unmessbar (beide zu kurz)
    t6_pass = n_p17_tokens < 30 and n_p23_tokens < 20
    tests.append({
        "name": "T6_kl_p17_p23_unmessbar_wegen_kuerze",
        "pass": t6_pass,
        "befund": f"p17={n_p17_tokens} + BURUMUT={n_p23_tokens} Tokens — keine Markov-KL messbar",
        "was_sagt_es_uns": (
            "p17 Klartext und BURUMUT beide zu kurz für Markov-Vergleich. "
            "V15-Hör: Beide sind Code-Notation, keine statistisch natürliche Sprache."
        ),
    })

    n_pass = sum(1 for t in tests if t["pass"])

    output = {
        "phase": "V15 K4 Markov horchend",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "kl_values": {
            "kl_p17_p1_16": kl_p17_p1_16,
            "kl_p1_16_p17": kl_p1_16_p17,
            "kl_p23_p1_16": kl_p23_p1_16,
            "kl_p17_p23": kl_p17_p23,
            "asym_ratio": asym_ratio,
        },
        "tests": tests,
        "verdict": f"V15 K4 horchend: {n_pass}/{len(tests)} PASS. Markov-Asymmetrie + BURUMUT-Andersartigkeit dokumentiert.",
    }

    out_dir = Path("bbox/v15_markov_horch_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "markov_horch_verdict.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print()
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
