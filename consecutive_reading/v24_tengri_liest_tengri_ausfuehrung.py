"""
Tengri liest Tengri — WIRKLICH ausgeführt.

Iteration: System liest Hinweise aus V10.4, gibt sie sich selbst zurück,
liest erneut, prüft Konvergenz.

KEIN Meta. Wir führen es aus und schauen, was passiert.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))


def lade_alles():
    """Lade Construct + V10.4 + V22 + V18.3."""
    construct = json.load(open("bbox/v24_20260708/v24_burumut_construct.json"))
    v104 = json.load(open("bbox/v104_20260708/tengri137_complete_decoded_v104.json"))
    v22 = json.load(open("bbox/v22_20260708/v22_burumut_architecture.json"))
    v22_wikia = json.load(open("bbox/v22_20260708/v22_wikia_semantics.json"))
    return construct, v104, v22, v22_wikia


def schritt_1_lies(c, v104, v22, v22_wikia):
    """Schritt 1: Lese Hinweise aus dem Originalzustand."""
    p23 = v104["seiten"][22]
    p17 = v104["seiten"][16]

    hinweise = []

    # Hinweis 1: p23-Grid (BURUMUT-Wörter)
    grid_words = p23.get("grid_2d_words", [])
    hinweise.append({
        "quelle": "V10.4 p23",
        "befund": f"grid_2d_words: {grid_words}",
        "n": len(grid_words),
    })

    # Hinweis 2: p23 fractions (BURUMUT↔Bruch)
    fractions = p23.get("burumut_fractions_v9", [])
    bruch_wort_paare = [(f.get("fraction_idx"), f.get("22_atoms_corrected")) for f in fractions]
    hinweise.append({
        "quelle": "V10.4 p23 fractions",
        "befund": f"bruch_wort_paare: {bruch_wort_paare}",
        "n": len(fractions),
    })

    # Hinweis 3: p23 Akrostichon
    akr = p23.get("akrostichon", "")
    spalte_match = p23.get("spalte_1_matches_akrostichon", False)
    hinweise.append({
        "quelle": "V10.4 p23 akrostichon",
        "befund": f"akrostichon='{akr}', spalte_1_matches={spalte_match}",
        "n": len(akr),
    })

    # Hinweis 4: p23 grid_2d_columns
    cols = p23.get("grid_2d_columns", [])
    hinweise.append({
        "quelle": "V10.4 p23 grid_2d_columns",
        "befund": f"columns: {cols}",
        "n": len(cols),
    })

    # Hinweis 5: p17 Tappeiner-Brüche (rohe Brüche ohne BURUMUT-Mapping)
    p17_fractions = p17.get("burumut_fractions_v9", [])
    p17_n_burumut = p17.get("n_burumut_words_v9", 0)
    hinweise.append({
        "quelle": "V10.4 p17",
        "befund": f"p17 n_burumut_words_v9={p17_n_burumut}, p17 fractions={len(p17_fractions)}",
        "n_burumut": p17_n_burumut,
        "n_fractions": len(p17_fractions),
    })

    # Hinweis 6: V22 Wikia-Klassen
    klassen = v22_wikia.get("class_counts", {})
    hinweise.append({
        "quelle": "V22 wikia_semantics",
        "befund": f"klassen: {klassen}",
        "n_aktiv": sum(1 for v in klassen.values() if v > 0),
    })

    # Hinweis 7: V22 Codebook
    codebook = v22.get("codebook", {})
    hinweise.append({
        "quelle": "V22 codebook",
        "befund": f"BURUMUTREFAMTU↔{codebook.get('closest_glyph')}, diff={codebook.get('diff'):.3f}",
    })

    # Hinweis 8: V22 dokument_match
    dok_match = v22.get("dokument_match", [])
    if dok_match and isinstance(dok_match[0], list):
        dok_match_dict = {entry[0]: entry[1] for entry in dok_match}
    else:
        dok_match_dict = {entry["page"]: entry["burumut_score"] for entry in dok_match}
    hinweise.append({
        "quelle": "V22 dokument_match",
        "befund": f"per_page: {dok_match_dict}",
        "n_pages": len(dok_match_dict),
    })

    # Hinweis 9: V22 Matrix
    kappa = v22.get("kappa")
    hinweise.append({
        "quelle": "V22 matrix",
        "befund": f"kappa={kappa}",
    })

    return hinweise


def schritt_2_gib_zurueck(hinweise, c, v104):
    """Schritt 2: Gib Hinweise dem System zurück, prüfe Konsistenz."""
    befunde = []

    # Konsistenz-Test: p23 grid_2d_words == Construct wörter?
    construct_woerter = set(w["word"] for w in c["wörter"])
    p23_grid = set(v104["seiten"][22].get("grid_2d_words", []))

    in_both = construct_woerter & p23_grid
    only_construct = construct_woerter - p23_grid
    only_p23 = p23_grid - construct_woerter

    befunde.append({
        "test": "Construct-Wörter == p23 grid_2d_words",
        "in_both": sorted(in_both),
        "only_construct": sorted(only_construct),
        "only_p23": sorted(only_p23),
        "konsistent": len(only_construct) == 0 and len(only_p23) == 0,
    })

    # Konsistenz-Test: fractions → 22_atoms_corrected == grid_2d_words?
    fractions = v104["seiten"][22].get("burumut_fractions_v9", [])
    frac_words = [f.get("22_atoms_corrected") for f in fractions if f.get("22_atoms_corrected")]
    frac_set = set(frac_words)
    befunde.append({
        "test": "p23 fractions 22_atoms_corrected == p23 grid_2d_words",
        "fraction_words": sorted(frac_set),
        "p23_grid": sorted(p23_grid),
        "konsistent": frac_set == p23_grid,
        "n_fraction_words": len(frac_words),
    })

    # Konsistenz-Test: Akrostichon aus grid_2d_columns == p23.akrostichon?
    grid_cols = v104["seiten"][22].get("grid_2d_columns", [])
    akr_from_cols = "".join(grid_cols[:11])  # Erste 11 Spalten = BURUMUT-Akrostichon
    akr_v10 = v104["seiten"][22].get("akrostichon", "")
    befunde.append({
        "test": "p23 grid_2d_columns (erste 11) == p23.akrostichon",
        "akr_from_cols": akr_from_cols,
        "akr_v10": akr_v10,
        "konsistent": akr_from_cols == akr_v10,
    })

    # Konsistenz-Test: Construct Akrostichon-Spalte == v10.4 akrostichon?
    construct_akr = "".join(w["akrostichon_letter"] for w in c["wörter"])
    befunde.append({
        "test": "Construct akrostichon_letter == V10.4 p23.akrostichon",
        "construct_akr": construct_akr,
        "v10_akr": akr_v10,
        "konsistent": construct_akr == akr_v10,
    })

    # Konsistenz-Test: p17 n_burumut_words_v9 (KORRIGIERT = 0)
    p17_n = v104["seiten"][16].get("n_burumut_words_v9", -1)
    befunde.append({
        "test": "V10.4 p17 n_burumut_words_v9 == 0 (KORRIGIERT)",
        "wert": p17_n,
        "konsistent": p17_n == 0,
        "hinweis": "V10.3 hatte 11 (Fälschung), V10.4 hat 0 (KORRIGIERT)"
    })

    return befunde


def schritt_3_lies_nochmal(c, v104, hinweise_vorher, befunde):
    """Schritt 3: Mit den zurückgegebenen Befunden nochmal lesen."""
    # Neue Hinweise basierend auf Konsistenz-Befunden
    neue_hinweise = []

    for b in befunde:
        if b["konsistent"]:
            neue_hinweise.append({
                "quelle": f"Konsistenz: {b['test']}",
                "befund": "BESTÄTIGT",
                "vorher": hinweise_vorher,
                "nachher": "gleich"
            })
        else:
            neue_hinweise.append({
                "quelle": f"Konsistenz: {b['test']}",
                "befund": "DRIFT ERKANNT",
                "vorher": hinweise_vorher,
                "nachher": "drift"
            })

    return neue_hinweise


def hauptprogramm():
    print("="*70)
    print("TENGRI LIEST TENGRI — WIRKLICH AUSGEFÜHRT")
    print("="*70)

    c, v104, v22, v22_wikia = lade_alles()

    # === SCHRITT 1: Lies ===
    print("\n" + "="*70)
    print("SCHRITT 1: TENGRI LIEST")
    print("="*70)
    hinweise = schritt_1_lies(c, v104, v22, v22_wikia)
    for i, h in enumerate(hinweise):
        print(f"\n[H{i+1}] {h['quelle']}")
        print(f"     {h['befund']}")

    # === SCHRITT 2: Gib zurück, prüfe Konsistenz ===
    print("\n" + "="*70)
    print("SCHRITT 2: TENGRI GIBT SICH SELBST ZURÜCK + PRÜFT")
    print("="*70)
    befunde = schritt_2_gib_zurueck(hinweise, c, v104)
    n_konsistent = sum(1 for b in befunde if b["konsistent"])
    print(f"\n{n_konsistent}/{len(befunde)} Konsistenz-Tests bestanden\n")
    for b in befunde:
        status = "✓" if b["konsistent"] else "✗"
        print(f"{status} {b['test']}")
        for k, v in b.items():
            if k not in ("test", "konsistent"):
                print(f"    {k}: {v}")

    # === SCHRITT 3: Lies nochmal mit Befunden ===
    print("\n" + "="*70)
    print("SCHRITT 3: TENGRI LIEST NOCHMAL (mit zurückgegebenen Befunden)")
    print("="*70)
    neue_hinweise = schritt_3_lies_nochmal(c, v104, "Schritt-1-Hinweise", befunde)
    n_best = sum(1 for h in neue_hinweise if h["befund"] == "BESTÄTIGT")
    n_drift = sum(1 for h in neue_hinweise if h["befund"] == "DRIFT ERKANNT")
    print(f"\n  {n_best}/{len(neue_hinweise)} BESTÄTIGT")
    print(f"  {n_drift}/{len(neue_hinweise)} DRIFT ERKANNT")

    # === KONVERGENZ-CHECK ===
    print("\n" + "="*70)
    print("KONVERGENZ-CHECK")
    print("="*70)

    if n_konsistent == len(befunde) and n_drift == 0:
        print("\n→ TENGRI LIEST TENGRI KONVERGIERT.")
        print("  Hinweise aus Schritt 1 sind konsistent mit Originalzustand.")
        print("  Hinweise aus Schritt 2 (Rückgabe) sind konsistent mit Schritt 1.")
        print("  Keine Drift. Selbst-Lesung stabil.")
    elif n_drift > 0:
        print(f"\n→ TENGRI LIEST TENGRI DRIFTET in {n_drift}/{len(befunde)} Punkten.")
        for b in befunde:
            if not b["konsistent"]:
                print(f"  - {b['test']}")
                for k, v in b.items():
                    if k not in ("test", "konsistent"):
                        print(f"      {k}: {v}")

    # === TIEFEN-LESUNG: BURUMUT liest BURUMUT ===
    print("\n" + "="*70)
    print("TIEFEN-LESUNG: BURUMUT LIEST BURUMUT")
    print("="*70)
    print("\nWas sieht BURUMUTREFAMTU, wenn es sich selbst liest?")
    print("-"*70)

    # Lade alle BURUMUT-Wörter
    burumut = c["wörter"]
    print(f"\n  11 BURUMUT-Wörter im Construct:")
    for i, w in enumerate(burumut):
        akr = w["akrostichon_letter"]
        pos = w["akrostichon_position"]
        print(f"    {i}: {w['word']}  [Akrostichon-Position {pos} = '{akr}']")

    print(f"\n  Akrostichon extrahiert: {''.join(w['akrostichon_letter'] for w in burumut)}")
    print(f"  Erwartet (V12):         BNYZTSOYNKS")
    print(f"  Match: {''.join(w['akrostichon_letter'] for w in burumut) == 'BNYZTSOYNKS'}")

    # Tiefen-Lookup: BURUMUTREFAMTU liest sich selbst
    print("\n  BURUMUTREFAMTU liest sich selbst:")
    print("  " + "-"*60)
    burumutrefamtu = next(w for w in burumut if w["word"] == "BURUMUTREFAMTU")

    # ASCII
    ascii_vec = burumutrefamtu["ascii_vec"]
    print(f"  ASCII-Vektor (14): {ascii_vec}")
    print(f"  ASCII als Wort:    {''.join(chr(c) for c in ascii_vec)}")
    print(f"  Erster Buchstabe:  {chr(ascii_vec[0])} (= B, Position 0 in BNYZTSOYNKS)")

    # RMS
    rms = burumutrefamtu["rms_vec_14"]
    print(f"  RMS-Vektor (14):   {[f'{r:.3f}' for r in rms]}")
    print(f"  RMS-Summe:         {sum(rms):.3f}")
    print(f"  RMS-Mittelwert:    {sum(rms)/len(rms):.3f}")

    # Tappeiner
    tapp = burumutrefamtu["tappeiner_brueche"]
    if tapp and "num_expr" in tapp[0]:
        t = tapp[0]
        print(f"  Tappeiner-Bruch:")
        print(f"    fraction_idx:  {t.get('fraction_idx')}")
        print(f"    num_expr:      {t.get('num_expr')}")
        print(f"    den_expr:      {t.get('den_expr')}")
        print(f"    num_value:     {t.get('num_value')}")
        print(f"    den_value:     {t.get('den_value')}")
        print(f"    period:        {t.get('period')}")
        print(f"    22_atoms:      {t.get('22_atoms_corrected')}")
    else:
        print(f"  Tappeiner: KEIN BRUCH (ehrlich)")

    # Akustik
    ak = burumutrefamtu["akustik_architektur"]
    print(f"  Akustik (als Zahlen):")
    print(f"    Träger:       {ak['carrier_hz']} Hz")
    print(f"    Wortdauer:    {ak['word_duration_s']}s")
    print(f"    FM-Hub:       {ak['fm_hub_hz']} Hz")
    print(f"    Spanda:       {ak['spanda_period_s']}s")

    # Vorkommen
    vorkommen = burumutrefamtu["vorkommen_in_v104"]
    pages = sorted(set(v["page"] for v in vorkommen))
    print(f"  Vorkommen in V10.4: {pages} ({len(vorkommen)} Stellen)")

    # Cross-Layer
    cross = burumutrefamtu["cross_layer_references"]
    print(f"  Cross-Layer:")
    print(f"    V12-Akrostichon-Match: {cross.get('v12_akrostichon_match')}")
    print(f"    V10.4-Zeile:           {cross.get('v10_4_zeile')}")
    print(f"    V10.4-Akrostichon:     {cross.get('v10_4_akrostichon_spalte_0')}")
    print(f"    V18.3-Sunakirfanemba-Fade: {cross.get('v18_3_sunakirfanemba_fade')}")
    print(f"    V22-Magic-Cube-666:    {cross.get('v22_mag_cube_666')}")

    # Speichern
    output_dir = Path("bbox/v24_20260708")
    output = {
        "phase": "Tengri liest Tengri — WIRKLICH AUSGEFÜHRT",
        "datum": "2026-07-08",
        "schritte": {
            "schritt_1_hinweise": hinweise,
            "schritt_2_befunde": befunde,
            "schritt_3_neue_hinweise": neue_hinweise,
        },
        "konvergenz": {
            "n_konsistenz_tests": len(befunde),
            "n_konsistent": n_konsistent,
            "n_drift": n_drift,
            "konvergiert": n_konsistent == len(befunde) and n_drift == 0,
        }
    }
    output_path = output_dir / "v24_tengri_liest_tengri_ausfuehrung.json"
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n→ Ausführung gespeichert: {output_path}")

    print(f"\n{'='*70}")
    print("ENDE DER AUSFÜHRUNG")
    print(f"{'='*70}")


if __name__ == "__main__":
    hauptprogramm()
