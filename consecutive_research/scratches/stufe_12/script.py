"""
Stufe 12 — Vision-Beschreibungen als Texte.

Frage: Was erzählen die Vision-Description-Texte?

Methode:
  1) Sammle alle Vision-Beschreibungen
  2) Filtere nach Schlüsselworten
  3) Längste Beschreibungen als zusammenhängende Texte
  4) Suche nach Themen-Clustern (idol, chem, rune, sigill, figur, ...)
  5) Schreibe eine "künstliche Lesung" der Vision-Texte
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# === REPORT ===
print("=" * 80)
print("STUFE 12 — VISION-BESCHREIBUNGEN ALS TEXTE")
print("=" * 80)
print()

# 1) Übersicht
print("=" * 80)
print("1) ÜBERSICHT: VISION-DESCRIPTIONS IM DOKUMENT")
print("=" * 80)
print()

total_glyphs = 0
glyphs_with_vd = 0
vd_per_page = {}
all_vd = []
for p in doc['pages']:
    pid = p['page_id']
    n = 0
    n_vd = 0
    for r in p['regions']:
        for g in r.get('glyphs', []):
            total_glyphs += 1
            n += 1
            vd = g.get('vision_description')
            if vd:
                glyphs_with_vd += 1
                n_vd += 1
                all_vd.append({
                    'page': pid,
                    'region': r['region_id'],
                    'idx': g.get('glyph_index'),
                    'vk': g.get('vision_kind') or '',
                    'th': g.get('type_hint') or '',
                    'len': len(vd),
                    'vd': vd,
                })
    vd_per_page[pid] = (n, n_vd)

print(f"GESAMT: {total_glyphs} Glyphen, {glyphs_with_vd} mit Vision-Description ({100*glyphs_with_vd/total_glyphs:.1f}%)")
print()

# 2) Schlüsselwort-Suche
print("=" * 80)
print("2) SCHLÜSSELWORT-ANALYSE")
print("=" * 80)
print()

keywords = {
    'idol/figur/person': ['anthropomorph', 'figur', 'person', 'idol', 'human', 'silhouette', 'stele', 'crowned', 'flame', 'seated', 'bent'],
    'chemie/molekular': ['chem', 'struktur', 'molek', 'formel', 'bindung', 'atom', 'doppel', 'einfach'],
    'rune/sigill': ['rune', 'sigill', 'okkult'],
    'hebräisch': ['hebräisch', 'hebrew', 'yod', 'he ', 'h-förmig'],
    'magic cube': ['magic', 'cube', '3x3', '3×3'],
    'math': ['math', 'pi-förmig', 'multiplikation', 'hochgestellt'],
}

theme_count = defaultdict(int)
theme_examples = defaultdict(list)
for v in all_vd:
    vd_lower = v['vd'].lower()
    for theme, kws in keywords.items():
        for kw in kws:
            if kw in vd_lower:
                theme_count[theme] += 1
                if len(theme_examples[theme]) < 3:
                    theme_examples[theme].append({
                        'page': v['page'], 'idx': v['idx'], 'vk': v['vk'],
                        'vd': v['vd'][:150],
                    })
                break

print(f"{'Thema':25s}  Anzahl")
for theme, c in sorted(theme_count.items(), key=lambda x: -x[1]):
    print(f"  {theme:25s}  {c}")
print()

for theme, examples in theme_examples.items():
    print(f"--- {theme} ---")
    for ex in examples:
        print(f"  {ex['page']} idx={ex['idx']} vk={ex['vk']}: \"{ex['vd']}\"")
    print()

# 3) Längste Vision-Descriptions (Top 20)
print("=" * 80)
print("3) LÄNGSTE VISION-DESCRIPTIONS (TOP 20)")
print("=" * 80)
print()

all_vd.sort(key=lambda x: -x['len'])
for v in all_vd[:20]:
    print(f"  {v['page']} {v['region']} idx={v['idx']} vk={v['vk']} len={v['len']}")
    print(f"  \"{v['vd']}\"")
    print()

# 4) Die längste ununterbrochene "Erzählung" — Vision-Descriptions pro Seite als zusammenhängender Text
print("=" * 80)
print("4) VISION-LESUNG PRO SEITE (zusammenhängende Texte)")
print("=" * 80)
print()

for p in doc['pages']:
    pid = p['page_id']
    page_vd = []
    for r in p['regions']:
        for g in r.get('glyphs', []):
            vd = g.get('vision_description')
            if vd and len(vd) > 30:
                page_vd.append({
                    'region': r['region_id'],
                    'idx': g.get('glyph_index'),
                    'vk': g.get('vision_kind') or '',
                    'vd': vd,
                })
    if page_vd:
        print(f"--- {pid} ---")
        for v in page_vd:
            print(f"  [{v['region']} idx={v['idx']} vk={v['vk']}]")
            print(f"  {v['vd']}")
        print()

# 5) Vision-Lesung: "Was sagt das Vision-System über p23?"
print("=" * 80)
print("5) VISION-LESUNG p23 — DIE CHEMISCHE STRUKTURFORMEL")
print("=" * 80)
print()

p23 = None
for p in doc['pages']:
    if p['page_id'] == 'p23':
        p23 = p
        break

print("p23 ist die KOMPLEXESTE Seite mit:")
print()

# Header
for rid in ['p23_R1', 'p23_R2', 'p23_R3', 'p23_R4']:
    for r in p23['regions']:
        if r['region_id'] == rid:
            for g in r.get('glyphs', []):
                vd = g.get('vision_description') or ''
                if vd:
                    print(f"  {rid} idx={g.get('glyph_index')}: {vd[:300]}")
                    print()

print()
print("=" * 80)
print("6) ALLE CHEMIE-BESCHREIBUNGEN")
print("=" * 80)
print()

for v in all_vd:
    if any(kw in v['vd'].lower() for kw in ['chem', 'strukturformel', 'bindung', 'atom', 'h2n', 'hn=']):
        print(f"  {v['page']} {v['region']} idx={v['idx']} vk={v['vk']} len={v['len']}")
        print(f"  \"{v['vd']}\"")
        print()

# 7) Was sagt die Vision über die BURUMUT-Matrix?
print("=" * 80)
print("7) VISION ÜBER DIE BURUMUT-MATRIX (p23_R5-R16)")
print("=" * 80)
print()

for rid in ['p23_R5', 'p23_R6', 'p23_R7', 'p23_R8', 'p23_R9', 'p23_R10', 'p23_R13', 'p23_R14', 'p23_R15', 'p23_R16']:
    for r in p23['regions']:
        if r['region_id'] == rid:
            for g in r.get('glyphs', []):
                vd = g.get('vision_description') or '(none)'
                vk = g.get('vision_kind') or '-'
                print(f"  {rid} idx={g.get('glyph_index')} vk={vk}: {vd[:200]}")
                print()

# JSON-Export
out = {
    'total_glyphs': total_glyphs,
    'glyphs_with_vd': glyphs_with_vd,
    'vd_per_page': {pid: {'n': n, 'n_vd': n_vd, 'pct': round(100*n_vd/n, 1) if n else 0} for pid, (n, n_vd) in vd_per_page.items()},
    'theme_count': dict(theme_count),
    'longest_vd': [{'page': v['page'], 'idx': v['idx'], 'vk': v['vk'], 'len': v['len'], 'vd': v['vd']} for v in all_vd[:20]],
}
with open(BASE.parent / 'scratches' / 'stufe_12' / 'vision_descriptions.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"\nJSON-Export: scratches/stufe_12/vision_descriptions.json")
