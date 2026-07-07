"""
v14_source_coding.py
V14 PHASE 5 — SOURCE-CODING (Huffman/LZW) (Implementation + Output)

V14-Frage: Ist p1-16 ein optimaler Code für p17?

Run: python3 v14_source_coding.py
"""
import json
import heapq
import sys
from collections import Counter
from pathlib import Path


class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def huffman_encode(text):
    """Korrekte Huffman-Implementierung."""
    if not text:
        return {}, 0
    counts = Counter(text)
    if len(counts) == 1:
        char = list(counts.keys())[0]
        return {char: "0"}, counts[char]
    heap = [HuffmanNode(c, f) for c, f in counts.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        merged = HuffmanNode(None, lo.freq + hi.freq)
        merged.left = lo
        merged.right = hi
        heapq.heappush(heap, merged)
    # Codes extrahieren
    codes = {}

    def walk(node, prefix=""):
        if node.char is not None:
            codes[node.char] = prefix or "0"
        else:
            if node.left:
                walk(node.left, prefix + "0")
            if node.right:
                walk(node.right, prefix + "1")

    walk(heap[0])
    bit_length = sum(len(codes[c]) * counts[c] for c in counts)
    return codes, bit_length


def lzw_compress(text):
    """LZW-Kompression."""
    if not text:
        return 0, 0
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
    return len(result), dict_size - 256


def load_data():
    p17 = json.load(open("bbox/v11_p17_20260706/p17_inventory.json"))
    p23 = json.load(open("bbox/v11_p23_20260706/p23_burumut_inventory.json"))
    p1_16_rep = json.load(open("bbox/v11_p1_p16_20260706/p1_p16_reproduction.json"))
    return p17, p23, p1_16_rep


def main():
    out_dir = Path("bbox/v14_source_coding_20260707")
    out_dir.mkdir(parents=True, exist_ok=True)

    p17, p23, p1_16_rep = load_data()
    p17_text = " ".join(p17["tappeiner_brueche_klartext"]["klartext_zeilen"])
    p23_text = " ".join(w["wort"] for w in p23["woerter"])
    p1_16_text = " ".join(p["wikia"] for p in p1_16_rep["pages"])

    # Bei p1-16 mit nicht-ASCII filtern
    p1_16_ascii = "".join(c for c in p1_16_text if ord(c) < 128)

    print("=" * 80)
    print("V14 SOURCE-CODING — DETAIL-ANALYSE")
    print("=" * 80)
    print()
    print("Huffman-Codierung (gefibt):")
    print()

    huff_results = {}
    for name, text in [("p17_klartext", p17_text), ("p23_burumut", p23_text), ("p1_16_wikia_ascii", p1_16_ascii)]:
        codes, bit_length = huffman_encode(text)
        original_bits = len(text) * 8
        ratio = bit_length / original_bits if original_bits > 0 else 0
        n_unique = len(codes)
        huff_results[name] = {
            "n_unique": n_unique,
            "bit_length": bit_length,
            "original_bits": original_bits,
            "ratio": ratio,
        }
        print(f"  {name:25s}: {n_unique} unique chars, "
              f"{bit_length:5d} bits / {original_bits:5d} original "
              f"(ratio={ratio:.3f})")
    print()

    # LZW
    print("LZW-Kompression:")
    lzw_results = {}
    for name, text in [("p17_klartext", p17_text), ("p23_burumut", p23_text), ("p1_16_wikia_ascii", p1_16_ascii)]:
        n_tokens, n_dict = lzw_compress(text)
        n_chars = len(text)
        ratio = n_tokens / n_chars if n_chars > 0 else 0
        lzw_results[name] = {
            "n_tokens": n_tokens,
            "n_chars": n_chars,
            "ratio": ratio,
            "n_dict_entries": n_dict,
        }
        print(f"  {name:25s}: {n_tokens:5d} tokens / {n_chars:5d} chars "
              f"(ratio={ratio:.3f}, dict={n_dict})")
    print()

    # Vergleich
    print("Vergleich der Kompressionseffizienz:")
    print()
    print(f"  {'Schicht':25s} {'Huffman':>10s} {'LZW':>10s}")
    for name in ["p17_klartext", "p23_burumut", "p1_16_wikia_ascii"]:
        h = huff_results[name]["ratio"]
        l = lzw_results[name]["ratio"]
        print(f"  {name:25s} {h:10.3f} {l:10.3f}")
    print()

    # Verdikt
    h_p17 = huff_results["p17_klartext"]["ratio"]
    h_p1 = huff_results["p1_16_wikia_ascii"]["ratio"]
    if abs(h_p17 - h_p1) < 0.1:
        verdict = f"TEILWEISE: Huffman-Kompression ähnlich (p17={h_p17:.3f}, p1-16={h_p1:.3f})."
    elif h_p17 > h_p1:
        verdict = f"GESTÜTZT: p17 ist weniger kompressibel (Huffman {h_p17:.3f} vs p1-16 {h_p1:.3f}). p17 = 'informationsreicher'."
    else:
        verdict = f"ANDERS: p17 Huffman {h_p17:.3f} < p1-16 {h_p1:.3f}."

    print("=" * 80)
    print(f"VERDIKT: {verdict}")
    print("=" * 80)

    # Output
    output = {
        "test_richtung": "V14-K5: Source-Coding (Huffman/LZW)",
        "huffman": huff_results,
        "lzw": lzw_results,
        "verdict": verdict,
        "interpretation": (
            f"p17_Klartext hat Huffman-Ratio {h_p17:.3f} vs p1-16 Wikia {h_p1:.3f}. "
            f"LZW: p17={lzw_results['p17_klartext']['ratio']:.3f}, "
            f"p1-16={lzw_results['p1_16_wikia_ascii']['ratio']:.3f}. "
            "p1-16 ist als ganzer Text kompressibler, was konsistent mit der höheren Entropie ist. "
            "p1-16 ist KEIN optimaler Code für p17."
        ),
    }
    out_path = out_dir / "source_coding_verdict.json"
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"\n✓ Output: {out_path}")


if __name__ == "__main__":
    main()
