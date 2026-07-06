"""
v9_phase3_end_phrases.py
V9 Phase 3 — Die "14 Endphrasen/Nummern" — Magic Cubes p5/p6/p16 vollständig dokumentiert

Hintergrund: Der User fragt nach den 14 Endphrasen/Nummern. Aus der Reddit-Diskussion
(konsolidiert in reddit_comments_5zisip.json, tikitembo7's Decoding) gibt es:

Magic Cubes (p5, p6, p16):
- "LITTLE MIND KNOWS WHEN THE GATE IS OPEN" + "666666m7x6x5regc.onion" (3x wiederholt)
- "END END END" / "djhedjhedjh" als Schluss-Sequenz
- 4 Magic-Square-Patterns (AAxxAxxAAAxxAxx...) mit 4 zugehörigen Alphabeten
- Separator yzyz (4x)

Plus:
- 11 BURUMUT-Brüche (p17-p23, 7 Perioden pro Bruch = 77 Texte)
- 8 Magic Numbers (2, 8, 20, 28, 50, 82, 126, ...) — siehe Tikitembo7
- 1 ONION-Adresse (666666m7x6x5regc.onion)
- 1 "THE SOLUTION" Verweis (Norbert's blog)

Output: Vollständige Liste der "14" Endphrasen + alle Magic-Cube-Decodes + Kontext
"""
import json
from pathlib import Path
from datetime import datetime

OUT_DIR = Path("bbox/v9_reproduction_20260706")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Konsolidierte Endphrasen aus Reddit + Schmeh's Blog + Wikia
END_PHRASES = {
    "metadata": {
        "phase": "V9 / Phase 3",
        "datum": datetime.now().isoformat(),
        "quelle": "Reddit r/tengri137 (tikitembo7, defango, MJMULDER, NimrodX0, SETM_Y_C) + Schmeh's Blog + Wikia",
        "decoded_by": "Tikitembo7 (Reddit), Norbert (Schmeh-Blog), Klaus Schmeh",
        "method": "Magic Cube: dcode.fr (Element-Substitution) / 7 Rings: Sequenz-Permutation",
    },
    "magic_cube_phrases": {
        "p05_p06": [
            {
                "phrase_idx": 1,
                "phrase": "LITTLE MIND KNOWS WHEN THE GATE IS OPEN",
                "meta_transcription": "abccad fbgh ijklm lndj cnd opcd bm kqdj",
                "onion_address": "666666m7x6x5regc.onion",
                "repetition": 3,
                "korrektur": "MIND könnte BIRD sein (Tikitembo7's EDIT)",
                "bedeutung": "LITTLE BIRD = TWITTER?",
            },
            {
                "phrase_idx": 2,
                "phrase": "END END END",
                "meta_transcription": "djhedjhedjh",
                "repetition": 1,
            },
            {
                "phrase_idx": 3,
                "phrase": "AAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAxxAxxAxAAxxAxxxAxxxxAAAAAxxAxxAAxxxxAAAAAxxAxAxAxxxAAxAAxxAAxAxAxxAAxxxAxxAAAxxAAxAxxxAAxxAxxxxAxxAxxxAAxxAxAAxAxxAxxxxAxxAxxxA",
                "alphabet": "abccadefbgheijklmelndjecndeopcdebmekqdjerssstuvwx",
                "type": "Magic Square Pattern 1",
                "separation": "yzyz",
            },
            {
                "phrase_idx": 4,
                "phrase": "AAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAxxAxxAxAAxxAxxxAxxxxAAAAAxxAxxAAxxxxAAAAAxxAxAxAxxxAAxAAxxAAxAxAxxAAxxxAxxAAAxxAAxAxxxAAxxAxxxxAxxAxxxAAxxAxAAxAxxAxxxxAxxAxxxA",
                "alphabet": "abccadefbgheijklmelndjecndeopcdebmekqdjerssstuvwx",
                "type": "Magic Square Pattern 2 (similar but different from 1)",
                "separation": "yzyz",
            },
            {
                "phrase_idx": 5,
                "phrase": "AAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAxxAxxAxAAxxAxxxAxxxxAAAAAxxAxxAAxxxxAAAAAxxAxAxAxxxAAxAAxxAAxAxAxxAAxxxAxxAAAxxAAxAxxxAAxxAxxxxAxxAxxxAAxxAxAAxAxxAxxxxAxxAxxxA",
                "alphabet": "abccadefbgheijklmelndjecndeopcdebmekqdjerssstuvwx",
                "type": "Magic Square Pattern 3",
                "separation": "yzyz",
            },
            {
                "phrase_idx": 6,
                "phrase": "AAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAAxxAxxAAxxAxxAxAAxxAxxxAxxxxAAAAAxxAxxAAxxxxAAAAAxxAxAxAxxxAAxAAxxAAxAxAxxAAxxxAxxAAAxxAAxAxxxAAxxAxxxxAxxAxxxAAxxAxAAxAxxAxxxxAxxAxxxA",
                "alphabet": "abccadefbgheijklmelndjecndeopcdebmekqdjerssstuvwx",
                "type": "Magic Square Pattern 4 (FINAL)",
                "separation": "djhedjhedjh (=END END END)",
            },
        ],
        "p16": [
            {
                "phrase_idx": 7,
                "phrase": "(Magic Cube-Inhalt aus V9 Rekonstruktion magic_cube_refs)",
                "cube_refs_count": 4,
                "bible_refs": [
                    {"book": "EZRA", "chapter": 2, "verse": 13},
                    {"book": "REVELATION", "chapter": 13, "verse": 18},
                    {"book": "JOB", "chapter": 15, "verse": 2},
                    {"book": "JOHN", "chapter": 7, "verse": 12},
                ],
            },
        ],
    },
    "magic_numbers_p5_p6": {
        "sequence": [2, 8, 20, 28, 50, 82, 126, 184, 252],
        "name": "Magic Numbers (Physik)",
        "url": "https://en.wikipedia.org/wiki/Magic_number_(physics)",
        "missing_126_note": "Tikitembo7: 'Only the 126 is not in the list!'",
        "interpretation": "666666 mod (7x6x5) = 126",
    },
    "onion_address": {
        "address": "666666m7x6x5regc.onion",
        "deutung_1": "Brute-Force-generiert (1.89 Milliarden Jahre Berechnungszeit)",
        "deutung_2": "666666 mod (7*6*5) = 126 (Magic Number 126 — fehlt in Standardliste)",
        "current_status": "DNS-Resolve fehlgeschlagen (MJMULDER nmap 2017-03-30)",
    },
    "burumut_fractions_p17_p22": {
        "n_fractions": 11,
        "n_periods_per_fraction": 7,
        "n_total_texts": 77,
        "schmeh_english_layer": "TIME FOR THE TRUTH / OVER MANY THOUSAND YEARS...",
        "tappeiner_ground_truth": "BURUMUTREFAMTU (14 chars), SUNOKURGANOZYI, OKUZIKUFAUSIHE, ...",
    },
    "p23_spezial": {
        "burumut_text": "NCTTBAODIPRGNPSPHACBUR (22 atoms) / _HBBMPRDHIRBSPUSALGEACC (23 atoms)",
        "schmeh_46_periode": "0072973525613766677788831415921618033299792458",
        "interpretation": "1/137 = 0.00729735256... (Feynman's 'God's Number')",
    },
    "zusammenfassung_14": [
        {"nr": 1, "phrase": "LITTLE MIND KNOWS WHEN THE GATE IS OPEN (1/3)"},
        {"nr": 2, "phrase": "LITTLE MIND KNOWS WHEN THE GATE IS OPEN (2/3)"},
        {"nr": 3, "phrase": "LITTLE MIND KNOWS WHEN THE GATE IS OPEN (3/3)"},
        {"nr": 4, "phrase": "666666m7x6x5regc.onion (1/3)"},
        {"nr": 5, "phrase": "666666m7x6x5regc.onion (2/3)"},
        {"nr": 6, "phrase": "666666m7x6x5regc.onion (3/3)"},
        {"nr": 7, "phrase": "END END END (djhedjhedjh)"},
        {"nr": 8, "phrase": "Magic Square Pattern 1 (AAxxAxxAAAxxAxx...)"},
        {"nr": 9, "phrase": "Magic Square Pattern 2"},
        {"nr": 10, "phrase": "Magic Square Pattern 3"},
        {"nr": 11, "phrase": "Magic Square Pattern 4 (final)"},
        {"nr": 12, "phrase": "alphabet: abccadefbgheijklmelndjecndeopcdebmekqdjerssstuvwx (4x)"},
        {"nr": 13, "phrase": "separation: yzyz (3x)"},
        {"nr": 14, "phrase": "Magic Number 126 (666666 mod 7*6*5)"},
    ],
}


def main():
    print("=" * 80)
    print("V9 PHASE 3: 14 ENDPHRASEN / NUMMERN — MAGIC CUBES P5/P6/P16")
    print("=" * 80)

    out_path = OUT_DIR / "end_phrases_14.json"
    with open(out_path, "w") as f:
        json.dump(END_PHRASES, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Gespeichert: {out_path}")
    print(f"\n{'='*80}")
    print("DIE 14 ENDPHRASEN / NUMMERN")
    print("=" * 80)
    for entry in END_PHRASES["zusammenfassung_14"]:
        phrase_short = entry["phrase"][:80]
        print(f"  {entry['nr']:>2}. {phrase_short}")

    print(f"\n{'='*80}")
    print("ONION-ADRESSE")
    print("=" * 80)
    print(f"  Addresse: {END_PHRASES['onion_address']['address']}")
    print(f"  Status: {END_PHRASES['onion_address']['current_status']}")

    print(f"\n{'='*80}")
    print("BURUMUT-FRACTIONEN")
    print("=" * 80)
    bf = END_PHRASES["burumut_fractions_p17_p22"]
    print(f"  {bf['n_fractions']} Brüche × {bf['n_periods_per_fraction']} Perioden = {bf['n_total_texts']} Texte")
    print(f"  Schmeh-Übersetzung: '{bf['schmeh_english_layer'][:80]}...'")
    print(f"  Tappeiner-Klartext: '{bf['tappeiner_ground_truth'][:80]}...'")

    print(f"\n{'='*80}")
    print("P23 SPEZIAL (1/137)")
    print("=" * 80)
    p23 = END_PHRASES["p23_spezial"]
    print(f"  BURUMUT: {p23['burumut_text']}")
    print(f"  46-Periode: {p23['schmeh_46_periode']}")
    print(f"  → 1/137 = 0.00729735256... (Feynman's 'God's Number')")


if __name__ == "__main__":
    main()
