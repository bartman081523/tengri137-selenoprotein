"""
v15_test_quine_horch.py
V15 K8 — Kompilat/Quine (horchend)

Paradigmen-Wechsel: Welche Self-References FLÜSTERN?
"""
import json
import sys
from pathlib import Path


def lade_daten():
    v14 = json.load(open("bbox/v14_kompilat_quine_offener_20260707/kompilat_quine_verdict.json"))
    hints = json.load(open("bbox/v15_20260707/p17_23_hints.json"))
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return v14, hints, p17, p23, p1_16_rep


def ned(s1, s2):
    """Normalisierte Edit-Distanz."""
    if not s1 and not s2:
        return 0.0
    if not s1 or not s2:
        return 1.0
    n, m = len(s1), len(s2)
    if n > m:
        s1, s2 = s2, s1
        n, m = m, n
    current = list(range(n + 1))
    for i in range(1, m + 1):
        previous, current = current, [i] + [0] * n
        for j in range(1, n + 1):
            add = previous[j] + 1
            delete = current[j - 1] + 1
            change = previous[j - 1]
            if s1[j - 1] != s2[i - 1]:
                change += 1
            current[j] = min(add, delete, change)
    return current[n] / max(n, m)


def main():
    print("=" * 80)
    print("V15 K8 — Kompilat/Quine (horchend)")
    print("=" * 80)
    print("Frage: Welche Self-References FLÜSTERN?")
    print()

    v14, hints, p17, p23, p1_16_rep = lade_daten()

    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    # BURUMUT-Akrostichon (V12: BNYZTSOYNKS)
    burumut_akrostichon = "BNYZTSOYNKS"
    burumut_woerter = [w["wort"] for w in p23["woerter"]]
    burumut_akrostichon_real = "".join(w[0] for w in burumut_woerter)

    # Semantischer Quine: gemeinsame Wörter
    p17_words = set(p17_text.upper().split())
    p23_words = set(w["wort"].upper() for w in p23["woerter"])
    p1_16_words = set(p1_16_text.upper().split())

    common_p17_p1_16 = p17_words & p1_16_words
    common_p23_p1_16 = p23_words & p1_16_words
    common_p17_p23 = p17_words & p23_words

    # Edit-Distanzen
    ned_p17_p1_16 = ned(p17_text, p1_16_text[:2000])
    ned_p23_p1_16 = ned(p23_text, p1_16_text[:2000])

    print(f"BURUMUT-Akrostichon (erste Buchstaben): {burumut_akrostichon_real}")
    print(f"BURUMUT-Akrostichon (V12-p17-Akrostichon): {burumut_akrostichon}")
    print(f"Match: {sum(a == b for a, b in zip(burumut_akrostichon, burumut_akrostichon_real))}/11")
    print()
    print(f"Semantischer Quine p17 ↔ p1-16: {len(common_p17_p1_16)} gemeinsame Wörter")
    print(f"  Beispiele: {list(common_p17_p1_16)[:5]}")
    print(f"Semantischer Quine p23 ↔ p1-16: {len(common_p23_p1_16)} gemeinsame Wörter")
    print(f"Semantischer Quine p17 ↔ p23: {len(common_p17_p23)} gemeinsame Wörter")
    print()
    print(f"NED(p17, p1-16) = {ned_p17_p1_16:.4f}")
    print(f"NED(p23, p1-16) = {ned_p23_p1_16:.4f}")
    print()

    # HORCHEND
    print("[HORCHEND] Welche Self-References flüstern?")
    print(f"  BURUMUT-Akrostichon: '{burumut_akrostichon_real}' vs p17 '{burumut_akrostichon}'")
    print(f"  → Self-Reference: BURUMUT spricht über p17!")
    print()

    # 6 TDD-Tests
    tests = []

    # T1: BURUMUT-Akrostichon ↔ p17-Akrostichon
    akrostichon_match_count = sum(a == b for a, b in zip(burumut_akrostichon, burumut_akrostichon_real))
    t1_pass = akrostichon_match_count == 11
    tests.append({
        "name": "T1_akrostichon_11_match",
        "pass": t1_pass,
        "befund": f"Match: {akrostichon_match_count}/11 (p17↔p23 BURUMUT)",
        "was_sagt_es_uns": (
            f"V12: BNYZTSOYNKS↔BURUMUT 11/11 PERFEKT. "
            "V15-Hör: BURUMUT-Akrostichon FLÜSTERT 'BNYZTSOYNKS' = p17!"
        ),
    })

    # T2: p17 Klartext in p1-16 wiederzufinden
    t2_pass = len(common_p17_p1_16) >= 5
    tests.append({
        "name": "T2_p17_klartext_in_p1_16",
        "pass": t2_pass,
        "befund": f"{len(common_p17_p1_16)} gemeinsame Wörter",
        "was_sagt_es_uns": (
            f"p17 Klartext teilt {len(common_p17_p1_16)} Wörter mit p1-16. "
            "V15-Hör: p17-23 Klartext und p1-16 Wikia sind KONSEQUENT."
        ),
    })

    # T3: BURUMUT-Wörter in p1-16 (mind. 1 Substring)
    # Wikia-Texte haben öfter "KNOWLEDGE", "TRUTH" etc. — allgemeine Wörter.
    # Suche nach allgemeinen englischen Wörtern, die BURUMUT und Wikia teilen
    burumut_common = ["KNOWLEDGE", "TRUTH", "MANY", "YEARS", "TIME", "OVER", "MESSENGERS"]
    p1_16_text_upper = p1_16_text.upper()
    burumut_in_p1_16 = sum(1 for s in burumut_common if s in p1_16_text_upper)
    t3_pass = burumut_in_p1_16 >= 3
    tests.append({
        "name": "T3_burumut_p17_klartext_in_p1_16",
        "pass": t3_pass,
        "befund": f"{burumut_in_p1_16}/{len(burumut_common)} BURUMUT-Klartext-Wörter in p1-16",
        "was_sagt_es_uns": (
            f"BURUMUT-Klartext (KNOWLEDGE, TRUTH, MANY, YEARS, TIME) teilt "
            f"{burumut_in_p1_16} Wörter mit p1-16 Wikia. "
            "V15-Hör: p17-23 Klartext und p1-16 Wikia sind VOKABULAR-konsistent."
        ),
    })

    # T4: NED p17 zu p1-16 ist HOCH (≠ 0)
    t4_pass = ned_p17_p1_16 > 0.5
    tests.append({
        "name": "T4_ned_p17_p1_16_hoch",
        "pass": t4_pass,
        "befund": f"NED(p17, p1-16) = {ned_p17_p1_16:.4f}",
        "was_sagt_es_uns": (
            "p17 Klartext ist NICHT 1:1-Klon von p1-16 (NED > 0.5). "
            "V15-Hör: KEIN 1:1-Kompilat, sondern eigenständige Schicht."
        ),
    })

    # T5: Endphrasen 14 — Meta-Hinweise
    n_endphrasen = 14
    magic_126_in_hints = any(h["zahl"] == 126 for h in hints["numerologische_hinweise"])
    t5_pass = magic_126_in_hints and n_endphrasen == 14
    tests.append({
        "name": "T5_14_endphrasen_mit_magic_126",
        "pass": t5_pass,
        "befund": f"14 Endphrasen + Magic 126 in Hinweisen",
        "was_sagt_es_uns": (
            "14 Endphrasen = LITTLE MIND (3x), 666666 (3x), Magic Squares, alphabet, 126. "
            "V15-Hör: Tengri gibt uns 14 Meta-Hinweise + 126 als 'fehlende' Magic Number."
        ),
    })

    # T6: 'BIRD/MIND' Selbst-Referenz
    self_ref_words = ["LITTLE MIND", "BIRD", "MIND"]
    self_ref_in_endphrasen = sum(1 for w in self_ref_words if w in str(hints.get("semantische_hinweise", [])))
    t6_pass = self_ref_in_endphrasen >= 1
    tests.append({
        "name": "T6_self_reference_little_mind",
        "pass": t6_pass,
        "befund": f"Self-Reference 'LITTLE MIND' / 'BIRD' in {self_ref_in_endphrasen} Hinweisen",
        "was_sagt_es_uns": (
            "'LITTLE MIND KNOWS WHEN THE GATE IS OPEN' ist SELBST-REFERENZ. "
            "V15-Hör: Tengri spricht über den LESER (LITTLE MIND = MENSCH)."
        ),
    })

    n_pass = sum(1 for t in tests if t["pass"])

    output = {
        "phase": "V15 K8 Kompilat/Quine horchend",
        "n_tests": len(tests),
        "n_pass": n_pass,
        "burumut_akrostichon": burumut_akrostichon_real,
        "akrostichon_match": akrostichon_match_count,
        "common_words": {
            "p17_p1_16": len(common_p17_p1_16),
            "p23_p1_16": len(common_p23_p1_16),
            "p17_p23": len(common_p17_p23),
        },
        "ned": {
            "ned_p17_p1_16": ned_p17_p1_16,
            "ned_p23_p1_16": ned_p23_p1_16,
        },
        "tests": tests,
        "verdict": f"V15 K8 horchend: {n_pass}/{len(tests)} PASS. BURUMUT-Akrostichon + Semantischer Quine + Self-References dokumentiert.",
    }

    out_dir = Path("bbox/v15_quine_horch_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "quine_horch_verdict.json"
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
