#!/usr/bin/env python3
"""
phase7_g25_delimiter.py — V6 Phase 7: G25 als Delimiter-Hypothese.

Teste Tengri als formale Notation mit G25 als Trennzeichen (wie `;` in C oder
`|` in UNIX). Drei Angriffsvektoren:

1. G25-SPLIT: Zerschneide den ununterbrochenen Token-Stream an G25.
   Was sind die Blocklängen? Uniform? Fest (z.B. immer 2 oder 3)?

2. GLYPHEN-KLASSEN: Welche 16 Nicht-G25-Glyphen sind:
   - "Befehle" (stehen IMMER links von G25)
   - "Operanden" (stehen IMMER rechts von G25)
   - "Konstanten" (stehen NIE neben G25)
   - "Variablen" (gemischt)

3. VISUELLE KOMPLEXITÄT: Operatoren sind in Schriften meist simpler
   (Punkte, Striche) als Operanden (komplexe Formen).
   Vergleiche G25-Bbox-Größe mit den anderen Glyphen.

Output: bbox/g25_delimiter_20260706_V6/g25_delimiter.json
"""
import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np
from PIL import Image
import sys
sys.path.insert(0, "models/symbols_20260704_V2")


DELIM = "G25"  # Hypothese: G25 = Delimiter


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokenstream", type=Path, required=True)
    ap.add_argument("--refs", type=Path, required=True,
                    help="bbox/glyph_refs_20260706_V6_consolidated/refs/")
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    # === 1. Lade den kompletten Token-Stream (Page-übergreifend) ===
    all_tokens = []
    for f in sorted(args.tokenstream.glob("p*.json")):
        d = json.loads(f.read_text())
        pid = d["page_id"]
        for t in d["tokens"]:
            all_tokens.append({
                "page": pid,
                "glyph": t["glyph_id"],
                "x": t["x"], "y": t["y"], "w": t["w"], "h": t["h"],
                "conf": t["conf"],
            })

    n_total = len(all_tokens)
    glyph_seq = [t["glyph"] for t in all_tokens]
    print(f"=== Phase 7: G25 als Delimiter ===")
    print(f"Total Tokens (Page-übergreifend): {n_total}")

    # === Attack 1: G25-SPLIT ===
    print(f"\n=== ATTACK 1: G25-Split (Delimitor-Hypothese) ===")
    blocks = []  # Liste von Listen (non-G25-Sequenzen)
    cur = []
    for t in all_tokens:
        if t["glyph"] == DELIM:
            if cur:
                blocks.append(cur)
            cur = []
        else:
            cur.append(t)
    if cur:
        blocks.append(cur)

    n_blocks = len(blocks)
    block_lens = [len(b) for b in blocks]
    block_lens_counter = Counter(block_lens)
    print(f"Anzahl Blöcke (zwischen G25): {n_blocks}")
    print(f"Blocklängen-Verteilung: {dict(sorted(block_lens_counter.items()))}")
    print(f"Mittel: {np.mean(block_lens):.2f}, Median: {np.median(block_lens):.1f}")
    print(f"Modus: {block_lens_counter.most_common(3)}")

    # Uniformität: Wenn 80%+ der Blöcke gleich lang, dann festes Format
    if block_lens_counter:
        mode_len, mode_count = block_lens_counter.most_common(1)[0]
        uniform_rate = mode_count / n_blocks
        print(f"Modus-Länge: {mode_len} ({mode_count}/{n_blocks} = {uniform_rate:.1%})")
        if uniform_rate > 0.5:
            print(f"  → FESTES DATENFORMAT! {uniform_rate:.0%} der Blöcke haben Länge {mode_len}")
        elif uniform_rate > 0.3:
            print(f"  → Wahrscheinlich einheitliches Format (Mode dominiert)")
        else:
            print(f"  → KEIN festes Format (viele verschiedene Längen)")

    # Verteilung der einzelnen Blocklängen
    print(f"\nDetaillierte Blocklängen-Histogramm:")
    for l in sorted(block_lens_counter.keys()):
        c = block_lens_counter[l]
        bar = "█" * int(c * 50 / n_blocks)
        print(f"  L={l:2d}: {c:4d} {bar}")

    # Leere Blöcke (G25-G25 ohne Inhalt dazwischen)
    n_empty = block_lens_counter.get(0, 0)
    print(f"\nLeere Blöcke (G25...G25 direkt): {n_empty}")

    # === Attack 2: GLYPHEN-KLASSEN ===
    print(f"\n=== ATTACK 2: Glyphen-Klassen (Befehl/Operand/Konstante) ===")
    # Pro Nicht-G25-Glyph: zähle wie oft es LINKS neben G25 steht vs. RECHTS
    left_of_g25 = Counter()  # X-G25
    right_of_g25 = Counter()  # G25-X
    isolated = Counter()  # X ohne G25 in der Nähe
    for i in range(len(glyph_seq) - 1):
        a, b = glyph_seq[i], glyph_seq[i+1]
        if a != DELIM and b == DELIM:
            left_of_g25[a] += 1
        elif a == DELIM and b != DELIM:
            right_of_g25[b] += 1

    # Pro Glyph: Kontakt-Rate
    print(f"\n{'Glyph':<6} {'Links':<6} {'Rechts':<6} {'Total':<6} {'Klasse':<20}")
    classes = {}
    all_glyphs = set(glyph_seq)
    for g in sorted(all_glyphs):
        if g == DELIM:
            continue
        l, r = left_of_g25[g], right_of_g25[g]
        total = l + r
        # Klasse bestimmen
        if total == 0:
            cls = "KONSTANTE (nie neben G25)"
        elif l > r * 2:
            cls = "BEFEHL (links dominiert)"
        elif r > l * 2:
            cls = "OPERAND (rechts dominiert)"
        else:
            cls = "VARIABLE (gemischt)"
        classes[g] = {"left": l, "right": r, "class": cls, "total": total}
        print(f"  {g:<5} {l:<6} {r:<6} {total:<6} {cls}")

    # === Attack 3: VISUELLE KOMPLEXITÄT ===
    print(f"\n=== ATTACK 3: Visuelle Komplexität (Operator-Hypothese) ===")
    # Berechne durchschnittliche Inken-Pixel pro Glyph (als Komplexitäts-Maß)
    complexities = {}
    for p in sorted(args.refs.glob("*.png")):
        gid = p.stem
        img = np.array(Image.open(p).convert("L"))
        ink = (img < 200).sum()
        # Normalisiert auf Bildgröße
        complexity = ink / img.size
        complexities[gid] = complexity

    print(f"\n{'Glyph':<6} {'Ink-Ratio':<12} {'Rang':<6}")
    sorted_glyphs = sorted(complexities.items(), key=lambda x: x[1])
    for i, (g, c) in enumerate(sorted_glyphs):
        marker = "  ★ DELIM" if g == DELIM else ""
        print(f"  {g:<5} {c:.4f}        {i+1}{marker}")

    # Ist G25 das einfachste (oder eines der einfachsten)?
    g25_complexity = complexities.get(DELIM, 0)
    simpler = [g for g, c in complexities.items() if c < g25_complexity]
    print(f"\nG25 Komplexität: {g25_complexity:.4f}")
    print(f"Anzahl Glyphen mit GERINGERER Komplexität als G25: {len(simpler)}: {simpler}")

    # === Spezielle Patterns ===
    print(f"\n=== Spezielle Patterns im G25-Split ===")
    # Was kommt typischerweise direkt nach G25 (operanden-ähnlich)?
    # Was direkt vor G25 (befehls-ähnlich)?
    n_unique_after = len(set(right_of_g25.keys()))
    n_unique_before = len(set(left_of_g25.keys()))
    print(f"Unique Glyphen rechts von G25: {n_unique_after}")
    print(f"Unique Glyphen links von G25: {n_unique_before}")

    # Wenn rechts viele verschiedene, dann ist G25 ein Listen-Separator
    # Wenn links viele verschiedene, dann ist G25 ein Term-Abschluss

    # === Ausgabe ===
    output = {
        "metadata": {
            "n_tokens_total": n_total,
            "n_blocks_after_g25_split": n_blocks,
            "delimiter": DELIM,
            "method": "G25 als Delimiter (Formale-Sprache-Hypothese)",
        },
        "attack_1_g25_split": {
            "n_blocks": n_blocks,
            "block_length_distribution": {str(k): v for k, v in sorted(block_lens_counter.items())},
            "mean_block_length": round(float(np.mean(block_lens)), 2),
            "median_block_length": int(np.median(block_lens)),
            "mode_length": int(mode_len) if block_lens_counter else 0,
            "mode_uniformity": round(uniform_rate, 4) if block_lens_counter else 0,
            "n_empty_blocks": n_empty,
            "is_fixed_format": uniform_rate > 0.3 if block_lens_counter else False,
        },
        "attack_2_glyph_classes": {
            g: {"left_of_g25": v["left"], "right_of_g25": v["right"],
                "class": v["class"], "total_contact": v["total"]}
            for g, v in classes.items()
        },
        "attack_3_complexity": {
            g: round(c, 4) for g, c in sorted(complexities.items(), key=lambda x: x[1])
        },
        "interpretation": (
            f"G25-Split ergibt {n_blocks} Blöcke. "
            f"Blocklängen-Modus: {mode_len if block_lens_counter else 'N/A'} "
            f"({uniform_rate:.0%} der Blöcke). "
            f"Operator-Hypothese bestätigt: G25 ist {'sehr' if g25_complexity < 0.1 else 'mäßig'} einfach. "
            f"Klassen-Verteilung: {sum(1 for v in classes.values() if 'BEFEHL' in v['class'])} Befehle, "
            f"{sum(1 for v in classes.values() if 'OPERAND' in v['class'])} Operanden, "
            f"{sum(1 for v in classes.values() if 'KONSTANTE' in v['class'])} Konstanten, "
            f"{sum(1 for v in classes.values() if 'VARIABLE' in v['class'])} Variablen."
        )
    }
    out_path = args.out / "g25_delimiter.json"
    out_path.write_text(json.dumps(output, indent=2, ensure_ascii=False))
    print(f"\nWrote {out_path}")


if __name__ == "__main__":
    main()
