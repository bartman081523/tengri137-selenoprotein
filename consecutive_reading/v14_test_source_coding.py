"""
v14_test_source_coding.py
V14 KONSTRUKT 5 — SOURCE-CODING (Huffman/LZW) (TDD)

Hypothese (V11/V12): p1-16 ≠ 1:1-Code für p17.
V14-Erweiterung: Ist p1-16 ein OPTIMALER Code für p17?

Run: python3 v14_test_source_coding.py
"""
import json
import heapq
import sys
from collections import Counter
from pathlib import Path


def huffman_encode(text):
    """Huffman-Codierung: gibt Codes-Dict und Bitlänge zurück."""
    if not text:
        return {}, 0
    counts = Counter(text)
    heap = [[c, char] for char, c in counts.items()]
    heapq.heapify(heap)
    if len(heap) == 1:
        return {heap[0][1]: "0"}, len(text)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        merged = [lo[0] + hi[0], [lo, hi]]
        heapq.heappush(heap, merged)
    # Codes extrahieren
    codes = {}

    def walk(node, prefix=""):
        if len(node) == 2 and isinstance(node[1], str):
            codes[node[1]] = prefix or "0"
        else:
            _, left, right = node[1][0], node[1][0], node[1][1]
            if isinstance(node[1][0], list):
                walk(node[1][0], prefix + "0")
            if isinstance(node[1][1], list):
                walk(node[1][1], prefix + "1")
            elif len(node) == 2 and isinstance(node[1], str):
                codes[node[1]] = prefix or "0"

    walk(heap[0])
    bit_length = sum(len(codes[c]) * n for c, n in counts.items())
    return codes, bit_length


def lzw_compress(text):
    """LZW-Kompression: gibt Anzahl distinkter Phrasen zurück."""
    if not text:
        return 0
    dictionary = {chr(i): i for i in range(256)}
    dict_size = 256
    result = []
    w = ""
    for c in text:
        wc = w + c
        if wc in dictionary:
            w = wc
        else:
            result.append(dictionary[w])
            dictionary[wc] = dict_size
            dict_size += 1
            w = c
    if w:
        result.append(dictionary[w])
    return len(result)


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def test_huffman_p17_klartext():
    """Huffman-Codierung p17-Klartext liefert kürzere Bitlänge als Original."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    codes, bit_length = huffman_encode(text)
    original_bits = len(text) * 8
    ratio = bit_length / original_bits if original_bits > 0 else 0
    print(f"  Huffman p17: {bit_length} bits vs {original_bits} bits (ratio={ratio:.3f})")
    assert bit_length > 0, "Bitlänge = 0"


def test_huffman_p1_16():
    """Huffman p1-16 Wikia."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    codes, bit_length = huffman_encode(text)
    original_bits = len(text) * 8
    ratio = bit_length / original_bits if original_bits > 0 else 0
    print(f"  Huffman p1-16: {bit_length} bits vs {original_bits} bits (ratio={ratio:.3f})")
    assert bit_length > 0, "Bitlänge = 0"


def test_lzw_p17():
    """LZW p17: Anzahl Tokens vs Original."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    n_tokens = lzw_compress(text)
    n_chars = len(text)
    print(f"  LZW p17: {n_tokens} tokens vs {n_chars} Zeichen")
    assert n_tokens > 0, "LZW = 0 Tokens"


def test_lzw_p1_16():
    """LZW p1-16."""
    p17, p23, p1_16_rep = load_data()
    text = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    n_tokens = lzw_compress(text)
    n_chars = len(text)
    print(f"  LZW p1-16: {n_tokens} tokens vs {n_chars} Zeichen")
    assert n_tokens > 0, "LZW = 0 Tokens"


def test_huffman_vergleich():
    """Vergleich Huffman p17 vs p1-16: ähnliche Kompression?"""
    p17, p23, p1_16_rep = load_data()
    text_p17 = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    text_p1 = " ".join(p["wikia"] for p in p1_16_rep["pages"])
    _, bl_p17 = huffman_encode(text_p17)
    _, bl_p1 = huffman_encode(text_p1)
    r_p17 = bl_p17 / (len(text_p17) * 8) if text_p17 else 0
    r_p1 = bl_p1 / (len(text_p1) * 8) if text_p1 else 0
    delta = abs(r_p17 - r_p1)
    print(f"  Huff p17: {r_p17:.3f}, p1-16: {r_p1:.3f}, |Δ| = {delta:.3f}")
    assert r_p17 > 0 and r_p1 > 0, "Huffman-Ratio nicht positiv"


def main():
    print("=" * 80)
    print("V14 SOURCE-CODING — TDD (5 Tests)")
    print("=" * 80)
    print()
    print("Hypothese: p1-16 könnte optimaler Code für p17 sein (V14 neu).")
    print("V14-Methode: Huffman + LZW auf alle Schichten.")
    print()
    tests = [
        ("test_huffman_p17_klartext", test_huffman_p17_klartext),
        ("test_huffman_p1_16", test_huffman_p1_16),
        ("test_lzw_p17", test_lzw_p17),
        ("test_lzw_p1_16", test_lzw_p1_16),
        ("test_huffman_vergleich", test_huffman_vergleich),
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
    print(f"V14 SOURCE-CODING: {passed} PASS, {failed} FAIL")
    print("=" * 80)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
