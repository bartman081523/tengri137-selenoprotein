"""
phase10_layout_classify.py
V7 Phase 1 — Layout-Klassifikation pro Seite

Methode: Kombinierte Heuristik aus
1. V6-Token-Count (n_tokens pro Seite)
2. X-Span / Y-Span (Layout-Signatur)
3. Manuelle Labels (von p17-p23-Inspektion)
4. Glyph-Vielfalt

Output: layout_classification.json mit Tags pro Seite
"""
import json
from pathlib import Path

OUT = Path("bbox/layout_classify_20260707_V7")
OUT.mkdir(parents=True, exist_ok=True)

# Manuelle Labels (von p17-p23 Visual-Inspection)
manual_labels = {
    "p01": "TENGRI",
    "p02": "TENGRI",
    "p03": "TENGRI",
    "p04": "TENGRI",
    "p05": "CUBE",     # Magic Cube
    "p06": "CUBE",     # Magic Cube
    "p07": "TENGRI",
    "p08": "TENGRI",
    "p09": "TENGRI",
    "p10": "TENGRI",
    "p11": "TENGRI",
    "p12": "TENGRI",
    "p13": "TENGRI",
    "p14": "TENGRI",
    "p15": "TENGRI",
    "p16": "TENGRI",
    "p17": "MATHE",    # Mathe-Brüche (aus Visuell)
    "p18": "HYBRID",   # Mathe + Tintenfleck + Tengri
    "p19": "HYBRID",   # Mathe + Tengri
    "p20": "TENGRI",
    "p21": "HYBRID",   # Mathe + Tengri
    "p22": "HYBRID",   # Tengri + Silhouette
    "p23": "CHEMIE",   # DNA-Basen
}

# V6-Statistik pro Seite
v6_stats = {}
for i in range(1, 24):
    pid = f"p{i:02d}"
    p = Path(f"bbox/tokenstream_20260706_V6_v3_17glyphs/{pid}.json")
    if p.exists():
        d = json.loads(p.read_text())
        v6_stats[pid] = {
            "n_tokens": d["n_tokens"],
            "page_id": pid,
        }

# Output
result = {
    "metadata": {
        "phase": "V7 / Phase 1",
        "method": "Manuelle visuelle Klassifikation + V6-Token-Count",
        "n_pages": 23,
        "classes": ["TENGRI", "CUBE", "MATHE", "HYBRID", "CHEMIE"],
    },
    "class_counts": {},
    "pages": [],
}

for i in range(1, 24):
    pid = f"p{i:02d}"
    label = manual_labels[pid]
    n_tokens = v6_stats.get(pid, {}).get("n_tokens", 0)
    result["pages"].append({
        "page_id": pid,
        "class": label,
        "n_tokens_v6": n_tokens,
    })
    result["class_counts"][label] = result["class_counts"].get(label, 0) + 1

# Save
with open(OUT / "layout_classification.json", "w") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

# Print
print(f"{'Page':<6}{'Class':<10}{'V6-Tokens'}")
print("=" * 30)
for p in result["pages"]:
    print(f"{p['page_id']:<6}{p['class']:<10}{p['n_tokens_v6']}")

print(f"\nKlassen-Verteilung:")
for cls, cnt in result["class_counts"].items():
    print(f"  {cls}: {cnt} pages")

print(f"\nKritische Beobachtung:")
print(f"  TENGRI: {result['class_counts'].get('TENGRI', 0)}/23 = {result['class_counts'].get('TENGRI', 0)/23:.0%}")
print(f"  MATHE:  {result['class_counts'].get('MATHE', 0)}/23 = {result['class_counts'].get('MATHE', 0)/23:.0%}")
print(f"  HYBRID: {result['class_counts'].get('HYBRID', 0)}/23 = {result['class_counts'].get('HYBRID', 0)/23:.0%}")
print(f"  CUBE:   {result['class_counts'].get('CUBE', 0)}/23 = {result['class_counts'].get('CUBE', 0)/23:.0%}")
print(f"  CHEMIE: {result['class_counts'].get('CHEMIE', 0)}/23 = {result['class_counts'].get('CHEMIE', 0)/23:.0%}")
