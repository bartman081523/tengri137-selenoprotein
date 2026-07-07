"""
v14_test_kolmogorov_multi.py
V14 PHASE 1 — KOLMOGOROV MIT 4 KOMPRESSOREN (TDD)

Hypothese (V13): p17-23 hat 1.62x mehr Information als p1-16 (gzip).
V14-Erweiterung: Ist das robust über Kompressoren?
- gzip, bz2, lzma, zstd parallel
- Verhältnis K(p17-23)/K(p1-16) für jeden

Run: python3 v14_test_kolmogorov_multi.py
"""
import json
import gzip
import bz2
import lzma
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
    else:
        return None
    return len(compressed) / len(raw)


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def test_kompressionsverhaeltnis_gzip():
    p17, p23, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    r_gzip_p17 = kolmogorov_proxy(p17_p23, "gzip")
    r_gzip_p1 = kolmogorov_proxy(p1_16_text, "gzip")
    ratio = r_gzip_p17 / r_gzip_p1 if r_gzip_p1 > 0 else 0
    print(f"  gzip: p17-23={r_gzip_p17:.4f}, p1-16={r_gzip_p1:.4f}, ratio={ratio:.3f}")
    assert ratio > 1.0, f"gzip: ratio {ratio:.3f} <= 1.0 (V13 nicht bestätigt)"


def test_kompressionsverhaeltnis_bz2():
    p17, p23, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    r_bz2_p17 = kolmogorov_proxy(p17_p23, "bz2")
    r_bz2_p1 = kolmogorov_proxy(p1_16_text, "bz2")
    ratio = r_bz2_p17 / r_bz2_p1 if r_bz2_p1 > 0 else 0
    print(f"  bz2: p17-23={r_bz2_p17:.4f}, p1-16={r_bz2_p1:.4f}, ratio={ratio:.3f}")
    assert ratio > 1.0, f"bz2: ratio {ratio:.3f} <= 1.0"


def test_kompressionsverhaeltnis_lzma():
    p17, p23, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    r_lzma_p17 = kolmogorov_proxy(p17_p23, "lzma")
    r_lzma_p1 = kolmogorov_proxy(p1_16_text, "lzma")
    ratio = r_lzma_p17 / r_lzma_p1 if r_lzma_p1 > 0 else 0
    print(f"  lzma: p17-23={r_lzma_p17:.4f}, p1-16={r_lzma_p1:.4f}, ratio={ratio:.3f}")
    assert ratio > 1.0, f"lzma: ratio {ratio:.3f} <= 1.0"


def test_kompressionsverhaeltnis_zstd():
    p17, p23, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    r_zstd_p17 = kolmogorov_proxy(p17_p23, "zstd")
    r_zstd_p1 = kolmogorov_proxy(p1_16_text, "zstd")
    if r_zstd_p17 is None or r_zstd_p1 is None:
        print(f"  zstd: nicht verfügbar (skip)")
        return
    ratio = r_zstd_p17 / r_zstd_p1 if r_zstd_p1 > 0 else 0
    print(f"  zstd: p17-23={r_zstd_p17:.4f}, p1-16={r_zstd_p1:.4f}, ratio={ratio:.3f}")
    assert ratio > 1.0, f"zstd: ratio {ratio:.3f} <= 1.0"


def test_informationsasymmetrie_konsistent():
    """Wenn alle 4 Kompressoren p17-23 > p1-16 zeigen: robuste Asymmetrie."""
    p17, p23, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p17_p23 = p17_text + " " + p23_text
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    ratios = {}
    for comp in ["gzip", "bz2", "lzma", "zstd"]:
        r1 = kolmogorov_proxy(p17_p23, comp)
        r2 = kolmogorov_proxy(p1_16_text, comp)
        if r1 is not None and r2 is not None and r2 > 0:
            ratios[comp] = r1 / r2
    print(f"  Ratios: {ratios}")
    n_greater = sum(1 for r in ratios.values() if r > 1.0)
    n_total = len(ratios)
    print(f"  {n_greater}/{n_total} Kompressoren zeigen p17-23 > p1-16")
    assert n_greater == n_total, f"Nur {n_greater}/{n_total} zeigen Asymmetrie"


def main():
    print("=" * 80)
    print("V14 KOLMOGOROV MULTI-KOMPRESSOR — TDD (5 Tests)")
    print("=" * 80)
    print()
    print("Hypothese: p17-23 hat 1.62x mehr Information als p1-16 (V13, gzip).")
    print("V14-Test: Ist das robust über 4 Kompressoren?")
    print()
    tests = [
        ("test_kompressionsverhaeltnis_gzip", test_kompressionsverhaeltnis_gzip),
        ("test_kompressionsverhaeltnis_bz2", test_kompressionsverhaeltnis_bz2),
        ("test_kompressionsverhaeltnis_lzma", test_kompressionsverhaeltnis_lzma),
        ("test_kompressionsverhaeltnis_zstd", test_kompressionsverhaeltnis_zstd),
        ("test_informationsasymmetrie_konsistent", test_informationsasymmetrie_konsistent),
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
    print(f"V14 KOLMOGOROV: {passed} PASS, {failed} FAIL")
    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
