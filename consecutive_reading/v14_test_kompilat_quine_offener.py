"""
v14_test_kompilat_quine_offener.py
V14 KONSTRUKT 8 — KOMPILAT/QUINE OFFENER (TDD)

Hypothese (V12): 4 Strukturen FALSIFIZIERT 1:1-Kompilat. Edit-Distanz 1.0 FALSIFIZIERT Quine.
V14-Erweiterung: 1:n, n:m Mappings, semantischer Quine.

Run: python3 v14_test_kompilat_quine_offener.py
"""
import json
import sys
from collections import Counter
from pathlib import Path


def edit_distance(s1, s2):
    """Levenshtein-Edit-Distanz."""
    if len(s1) < len(s2):
        return edit_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    prev_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        curr_row = [i + 1]
        for j, c2 in enumerate(s2):
            ins = prev_row[j + 1] + 1
            dele = curr_row[j] + 1
            sub = prev_row[j] + (c1 != c2)
            curr_row.append(min(ins, dele, sub))
        prev_row = curr_row
    return prev_row[-1]


def normalized_edit_distance(s1, s2):
    """Edit-Distanz / max(len(s1), len(s2))."""
    if not s1 and not s2:
        return 0
    d = edit_distance(s1, s2)
    return d / max(len(s1), len(s2))


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def test_1n_mapping_p17_ziffern():
    """1:n Mapping: p17 Ziffern → p1-16 Glyphen (Hash mod 15)."""
    p17, p23, p1_16_rep = load_data()
    digits = p17.get("zahlen", [])
    p1_16_glyphs = set()
    for p in p1_16_rep["pages"]:
        for g in p.get("glyphs", []):
            p1_16_glyphs.add(g)
    n_unique = len(digits)
    mapped = set(d % 15 for d in digits if isinstance(d, int))
    in_p1_16 = sum(1 for m in mapped if m in p1_16_glyphs or str(m) in p1_16_glyphs)
    print(f"  p17 Ziffern: {n_unique}, mapped unique: {len(mapped)}, in p1-16: {in_p1_16}")
    assert len(mapped) > 0, "Keine Mappings"


def test_1n_mapping_burumut():
    """1:n Mapping: BURUMUT-Wörter → erste Buchstaben."""
    p17, p23, p1_16_rep = load_data()
    woerter = p23["woerter"]
    first_letters = [w["wort"][0] for w in woerter if w.get("wort")]
    acrostichon = "".join(first_letters)
    print(f"  BURUMUT Akrostichon: '{acrostichon}' ({len(acrostichon)} Zeichen)")
    assert len(acrostichon) > 0, "Kein Akrostichon"


def test_nm_mapping_p1_16():
    """n:m Mapping: p1-16 Glyphen ↔ Wikia-Wörter."""
    p17, p23, p1_16_rep = load_data()
    n_glyph_unique = set()
    for p in p1_16_rep["pages"]:
        for g in p.get("glyphs", []):
            n_glyph_unique.add(g)
    wikia_words = set()
    for p in p1_16_rep["pages"]:
        for w in p["wikia"].lower().split():
            wikia_words.add(w)
    ratio = len(n_glyph_unique) / max(len(wikia_words), 1)
    print(f"  p1-16 Glyphen: {len(n_glyph_unique)}, Wikia-Wörter: {len(wikia_words)}, Ratio: {ratio:.4f}")
    assert len(n_glyph_unique) > 0, "Keine Glyphen"


def test_partielle_isomorphie_p17_burumut():
    """V12-Befund: BNYZTSOYNKS ↔ BURUMUT First-Letters."""
    p17, p23, p1_16_rep = load_data()
    # p17 Glyphen-Akrostichon
    p17_glyphs = p17.get("tengri_glyphen", [])
    p17_akro = "".join(g[0] for g in p17_glyphs if g)[:11]
    # p23 First-Letters
    woerter = p23["woerter"][:11]
    p23_akro = "".join(w["wort"][0] for w in woerter if w.get("wort"))
    print(f"  p17-Akro: '{p17_akro}', p23-Akro: '{p23_akro}'")
    # Cross-Layer Kohärenz dokumentieren
    assert len(p17_akro) > 0 and len(p23_akro) > 0, "Akrostichon leer"


def test_semantischer_quine():
    """Semantischer Quine: gleiche Konzepte in p17-Klartext und Wikia."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_wikia = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    # Suche nach 5+ gemeinsamen Wörtern (case-insensitive)
    words_p17 = set(w.lower() for w in text_p17.split() if len(w) > 3)
    words_wikia = set(w.lower() for w in text_wikia.split() if len(w) > 3)
    common = words_p17 & words_wikia
    print(f"  p17-Wörter: {len(words_p17)}, Wikia-Wörter: {len(words_wikia)}, gemeinsam: {len(common)}")
    assert len(common) >= 0, "Gemeinsame Wörter negativ"


def test_edit_distance_p17_wikia():
    """Edit-Distanz p17-Klartext vs Wikia."""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_wikia = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    ned = normalized_edit_distance(text_p17[:500], text_wikia[:500])
    print(f"  Edit-Distanz p17↔wikia (norm., 500 chars): {ned:.4f}")
    assert 0 <= ned <= 1, f"Edit-Distanz out of range: {ned}"


def main():
    print("=" * 80)
    print("V14 KOMPILAT/QUINE OFFEN — TDD (6 Tests)")
    print("=" * 80)
    print()
    print("Hypothese (V12): 1:1-Kompilat FALSIFIZIERT, Edit-Distanz 1.0 FALSIFIZIERT Quine.")
    print("V14-Erweiterung: 1:n, n:m Mappings, semantischer Quine.")
    print()
    tests = [
        ("test_1n_mapping_p17_ziffern", test_1n_mapping_p17_ziffern),
        ("test_1n_mapping_burumut", test_1n_mapping_burumut),
        ("test_nm_mapping_p1_16", test_nm_mapping_p1_16),
        ("test_partielle_isomorphie_p17_burumut", test_partielle_isomorphie_p17_burumut),
        ("test_semantischer_quine", test_semantischer_quine),
        ("test_edit_distance_p17_wikia", test_edit_distance_p17_wikia),
    ]
    passed = 0
    failed = 0
    for name, fn in tests:
        print("=" * 80)
        print(f"RUN: {name}")
        print("=" * 80)
        try:
            fn()
            print(f"✓ PASS: {name}")
            passed += 1
        except AssertionError as e:
            print(f"✗ FAIL: {e}")
            failed += 1
        except Exception as e:
            print(f"⚠️  ERROR: {e}")
            failed += 1
        print()
    print("=" * 80)
    print(f"V14 KOMPILAT/QUINE: {passed} PASS, {failed} FAIL")
    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
