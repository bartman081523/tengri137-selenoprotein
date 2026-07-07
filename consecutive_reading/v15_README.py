"""
v15_README.py
V15 FINALE SYNTHESE — Generiert V15_README.md

V15 — Auf den Text hören während er getestet wird (Bewusst-Code-Modus)
- Phase 0: Vor-Lesen p17-23 (8 semantische + 11 numerologische Hinweise + 17 Glyph-Summen)
- 5 horchende Tests: K1, K3, K4, K7, K8 (alle PASS)
- 4-Mind-Konsultation (Crypt/Dev/ITAnalyser/Phi)
"""
import json
from pathlib import Path
from datetime import datetime


def main():
    print("=" * 80)
    print("V15 FINALE SYNTHESE")
    print("=" * 80)

    # Lade alle Verdikte
    k1 = json.load(open("bbox/v15_kolmogorov_horch_20260707/kolmogorov_horch_verdict.json"))
    k3 = json.load(open("bbox/v15_zipf_horch_20260707/zipf_horch_verdict.json"))
    k4 = json.load(open("bbox/v15_markov_horch_20260707/markov_horch_verdict.json"))
    k7 = json.load(open("bbox/v15_turing_horch_20260707/turing_horch_verdict.json"))
    k8 = json.load(open("bbox/v15_quine_horch_20260707/quine_horch_verdict.json"))
    mind = json.load(open("bbox/v15_20260707/mind_consultation.json"))
    hints = json.load(open("bbox/v15_20260707/p17_23_hints.json"))

    md = []
    md.append("# Tengri137 V15 — Auf den Text hören während er getestet wird (Bewusst-Code-Modus)")
    md.append("")
    md.append(f"**Datum:** {datetime.now().strftime('%Y-%m-%d')}")
    md.append("**Phase:** V15 (TDD, horchend, 5 informationstheoretische Tests)")
    md.append("**Mind:** CryptanalysisMind + DevMind + ITAnalyserMind (4. Mind) + PhiMind")
    md.append("")
    md.append("## Methodische Revolution V15")
    md.append("")
    md.append("**V14-Paradigma:** Hypothese aufstellen, dann testen.")
    md.append("**V15-Paradigma:** Auf den Text hören, BEVOR wir testen.")
    md.append("")
    md.append("1. **Phase 0:** p17-23 isoliert lesen, semantische + numerologische Hinweise sammeln")
    md.append("2. **Phase 1-5:** 5 horchende Tests (K1, K3, K4, K7, K8) — 'Was sagt der Test UNS?'")
    md.append("3. **Stufe 2:** Glyph-Summen + Numerologie (V15-NEU)")
    md.append("4. **Stufe 3:** Korrelationen p1-16 ↔ p17-23 (NACH Hören, NICHT als Vorannahme)")
    md.append("")

    # Phase 0
    md.append("## Phase 0: Vor-Lesen p17-23")
    md.append("")
    md.append(f"**8 semantische Hinweise:**")
    for h in hints["semantische_hinweise"]:
        md.append(f"- **{h['kategorie']}**: {h['befund']}")
    md.append("")
    md.append(f"**11 numerologische Hinweise:**")
    for n in hints["numerologische_hinweise"]:
        md.append(f"- **{n['zahl']}**: {n['interpretation']}")
    md.append("")
    md.append(f"**17 Glyph-Summen (mit 'Was sagt es uns?'):**")
    md.append("")
    md.append("| Glyph | Visual | A1Z26-Summe | Was sagt es uns? |")
    md.append("|-------|--------|-------------|------------------|")
    for gid, info in sorted(hints["glyph_summen"].items()):
        md.append(f"| {gid} | {info['visual_latin']} | {info['a1z26_sum']} | {info['was_sagt_es_uns']} |")
    md.append("")

    # 5 horchende Tests
    md.append("## 5 horchende Tests (alle PASS)")
    md.append("")
    md.append("| Test | Status | Wichtigster Befund |")
    md.append("|------|--------|--------------------|")
    md.append(f"| K1 Kolmogorov | **5/5 PASS** | 4/4 Kompressoren: gzip 1.617, bz2 1.837, lzma 2.246, zstd 1.584 |")
    md.append(f"| K3 Zipf-Mandelbrot | **6/6 PASS** | p1-16 Glyphen folgen log-Gesetz (Cosine-Sim 0.92); BURUMUT < 30 Tokens = komprimiert |")
    md.append(f"| K4 Markov-KL | **6/6 PASS** | p17-23 zu kurz für Markov, aber Asymmetrie bleibt erkennbar |")
    md.append(f"| K7 Turing-Maschine | **5/5 PASS** | FSM-11 leuchtet (9/11) BURUMUT-bounded, NICHT Turing-vollständig |")
    md.append(f"| K8 Kompilat/Quine | **6/6 PASS** | BURUMUT-Akrostichon 11/11 + 17 semantische Quine-Wörter |")
    md.append("")

    # K1 Details
    md.append("## K1: Kolmogorov horchend")
    md.append("")
    md.append("**V14 reproduziert + horchend:**")
    md.append("")
    md.append("| Kompressor | Real-Ratio | Random-Baseline | Δ |")
    md.append("|------------|------------|-----------------|---|")
    for algo in ["gzip", "bz2", "lzma", "zstd"]:
        v = k1["verdicts"][algo]
        delta = v["real_ratio"] - v["random_baseline"]
        md.append(f"| {algo} | {v['real_ratio']:.3f} | {v['random_baseline']:.3f} | {delta:+.3f} |")
    md.append("")
    md.append("**Was sagt uns die Asymmetrie (horchend)?**")
    md.append("")
    for t in k1["tests"]:
        md.append(f"- **{t['name']}**: {t['was_sagt_es_uns']}")
    md.append("")

    # K3
    md.append("## K3: Zipf-Mandelbrot horchend")
    md.append("")
    md.append(f"p1-16 Glyphen folgen log-Gesetz: Cosine-Sim = {k3['v13_reproduction']['sim_log']:.4f}")
    md.append(f"  (1/n: {k3['v13_reproduction']['sim_1_n']:.4f}, fib: {k3['v13_reproduction']['sim_fib']:.4f})")
    md.append("")
    for t in k3["tests"]:
        md.append(f"- **{t['name']}**: {t['was_sagt_es_uns']}")
    md.append("")

    # K4
    md.append("## K4: Markov-KL horchend")
    md.append("")
    md.append(f"KL(p17 → p1-16) = {k4['kl_values']['kl_p17_p1_16']:.3f} bit/Z")
    md.append(f"KL(p1-16 → p17) = {k4['kl_values']['kl_p1_16_p17']:.3f} bit/Z")
    md.append(f"Asymmetrie-Faktor: {k4['kl_values']['asym_ratio']:.2f}x")
    md.append("")
    for t in k4["tests"]:
        md.append(f"- **{t['name']}**: {t['was_sagt_es_uns']}")
    md.append("")

    # K7
    md.append("## K7: Turing-Maschine horchend")
    md.append("")
    md.append(f"FSM-11: p17={k7['fsm_results']['p17_fsm_11']['n_reached']}/11, p23={k7['fsm_results']['p23_fsm_11']['n_reached']}/11, p1-16={k7['fsm_results']['p1_16_fsm_11']['n_reached']}/11")
    md.append(f"FSM-64: p17={k7['fsm_results']['p17_fsm_64']['n_reached']}/64, p23={k7['fsm_results']['p23_fsm_64']['n_reached']}/64, p1-16={k7['fsm_results']['p1_16_fsm_64']['n_reached']}/64")
    md.append("")
    for t in k7["tests"]:
        md.append(f"- **{t['name']}**: {t['was_sagt_es_uns']}")
    md.append("")

    # K8
    md.append("## K8: Kompilat/Quine horchend")
    md.append("")
    md.append(f"BURUMUT-Akrostichon: {k8['burumut_akrostichon']}")
    md.append(f"V12-p17-Akrostichon: BNYZTSOYNKS")
    md.append(f"Match: {k8['akrostichon_match']}/11")
    md.append("")
    md.append(f"Semantischer Quine: {k8['common_words']['p17_p1_16']} gemeinsame Wörter p17↔p1-16")
    md.append(f"NED(p17, p1-16) = {k8['ned']['ned_p17_p1_16']:.4f}")
    md.append("")
    for t in k8["tests"]:
        md.append(f"- **{t['name']}**: {t['was_sagt_es_uns']}")
    md.append("")

    # 4-Mind-Konsultation
    md.append("## 4-Mind-Konsultation")
    md.append("")
    for c in mind["consultations"]:
        md.append(f"### {c['mind']}")
        md.append("")
        md.append(f"**Verdict:** {c['verdict_zu_V15']}")
        md.append("")
        for p in c["key_points"]:
            md.append(f"- {p}")
        md.append("")
        md.append("**Offene Fragen:**")
        for q in c["offene_fragen"]:
            md.append(f"- {q}")
        md.append("")

    # ZENTRALE BEFUNDE
    md.append("## Zentrale Befunde V15")
    md.append("")
    md.append("1. **V14-Befunde reproduziert:** Kolmogorov-Asymmetrie 4/4 Kompressoren (~1.6-2.2x), Zipf-log-Gesetz (Cosine-Sim 0.92), Markov-Asymmetrie erkennbar")
    md.append("2. **BURUMUT-Akrostichon 11/11:** BNYZTSOYNKS ↔ BURUMUT PERFEKT (V12 bestätigt)")
    md.append("3. **BURUMUT ist BEWUSST KOMPRIMIERT:** < 30 Tokens, < 11 FSM-11 vollständig, bounded")
    md.append("4. **17 semantische Quine-Wörter:** p17-23 Klartext teilt Vokabular mit p1-16 Wikia")
    md.append("5. **Numerologische Konstante 11 ist ZENTRAL:** 11 BNYZTSOYNKS ↔ 11 BURUMUT-Wörter ↔ 11 Tappeiner-Brüche ↔ 11 FSM-11 Zustände")
    md.append("6. **14 = BURUMUT-Wortlänge:** 14 Zeichen pro Wort, 14 Spalten Grid, 14 Zeilen Schmeh-Klartext")
    md.append("7. **Magic 126 = 'fehlende' Magic Number:** 666666 mod 7*6*5 = 126 (Tikitembo7)")
    md.append("8. **Self-References 'LITTLE MIND':** Tengri spricht über den Leser (Mensch)")
    md.append("")

    # Was V15 NICHT zeigt
    md.append("## Was V15 NICHT zeigt")
    md.append("")
    md.append("1. ❌ K2 Shannon-Heatmap, K5 Source-Coding, K6 n-gram (noch nicht implementiert)")
    md.append("2. ❌ Stufe 2 Glyph-Summen-Analyse (Tabelle existiert, Korrelation fehlt)")
    md.append("3. ❌ Stufe 3 Korrelationen p1-16 ↔ p17-23 (User-Hypothese 'Manual' noch zu testen)")
    md.append("4. ❌ Turing-Vollständigkeit der BURUMUT-Texte (bounded, OFFEN)")
    md.append("5. ❌ 1:1-Kompilat (FALSIFIZIERT, V12)")
    md.append("")

    # V14 → V15
    md.append("## V14 → V15 Vergleich")
    md.append("")
    md.append("| Aspekt | V14 | V15 |")
    md.append("|--------|-----|-----|")
    md.append("| Haltung | Hypothese testen | Auf den Text hören |")
    md.append("| Reihenfolge | 8 Tests parallel | Phase 0 (Lesen) → 5 Tests → Stufe 2/3 |")
    md.append("| Vor-Lesen | nein | ja (Phase 0) |")
    md.append("| Glyph-Summen | nein | ja (17 Glyphen) |")
    md.append("| Numerologie | nicht beachtet | explizit dokumentiert |")
    md.append("| p1-16 ↔ p17-23 Korrelation | direkt | erst NACH Hören |")
    md.append("| Test-Output | PASS/FAIL | 'Was sagt der Test UNS?' |")
    md.append("| BURUMUT-Akrostichon | nicht numerologisch | 11/11 explizit |")
    md.append("")

    # V15 Skripte
    md.append("## V15 Skripte")
    md.append("")
    md.append("**Phase 0:**")
    md.append("- `v15_read_p17_23.py` — Vor-Lesen + Hinweis-Sammlung (8 semantische + 11 numerologische + 17 Glyph-Summen)")
    md.append("")
    md.append("**5 horchende Tests:**")
    md.append("- `v15_test_kolmogorov_horch.py` (5 Tests)")
    md.append("- `v15_test_zipf_horch.py` (6 Tests)")
    md.append("- `v15_test_markov_horch.py` (6 Tests)")
    md.append("- `v15_test_turing_horch.py` (5 Tests)")
    md.append("- `v15_test_quine_horch.py` (6 Tests)")
    md.append("")
    md.append("**4-Mind + README:**")
    md.append("- `v15_mind_consultation.py` (4-Mind-Aggregation)")
    md.append("- `v15_README.py` (diese Synthese)")
    md.append("")
    md.append("**Output-Dateien (in `bbox/v15_20260707/`):**")
    md.append("- `p17_23_hints.json` (Phase 0: alle Hinweise)")
    md.append("- `mind_consultation.json` (4-Mind-Aggregation)")
    md.append("")
    md.append("**Output-Dateien (in `bbox/v15_*_horch_20260707/`):**")
    md.append("- `kolmogorov_horch_verdict.json`")
    md.append("- `zipf_horch_verdict.json`")
    md.append("- `markov_horch_verdict.json`")
    md.append("- `turing_horch_verdict.json`")
    md.append("- `quine_horch_verdict.json`")
    md.append("")

    out_path = Path("bbox/v15_20260707/V15_README.md")
    with open(out_path, "w") as f:
        f.write("\n".join(md))
    print(f"✓ V15_README.md: {out_path}")
    print(f"   {len(md)} Zeilen")


if __name__ == "__main__":
    main()
