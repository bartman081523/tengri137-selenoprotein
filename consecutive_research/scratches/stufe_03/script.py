"""
Stufe 3 — Latin-Tokens: Schmeh vs Vision.

Frage: Wo stimmen Vision und Schmeh überein, wo divergieren sie?

Methode:
  1) Sammle pro Region alle Tokens gruppiert nach Quelle
  2) conf-Verteilung der Vision-Tokens
  3) Region-für-Region-Vergleich
  4) Welche Wörter sind in Vision, welche nur in Schmeh
"""
import json
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path('/run/media/julian/ML4/tengri137/consecutive_research/docs')
with open(BASE / 'doc.json') as f:
    doc = json.load(f)

# Sammler
region_tokens = defaultdict(lambda: defaultdict(list))  # region_id -> {source: [texts]}
region_rt = {}  # region_id -> region_type
region_pid = {}  # region_id -> page_id

# Vision-Token-Detail
vision_details = []  # (pid, rid, text, conf, rt, bbox)

for p in doc['pages']:
    pid = p['page_id']
    for r in p['regions']:
        rid = r['region_id']
        rt = r.get('region_type', '?')
        region_rt[rid] = rt
        region_pid[rid] = pid
        for lt in r.get('latin_tokens', []):
            src = lt.get('source', '?')
            text = lt.get('text', '').strip()
            conf = lt.get('conf', 0)
            region_tokens[rid][src].append((text, conf))
            if src == 'vision':
                vision_details.append((pid, rid, text, conf, rt))

# === REPORT ===
print("=" * 80)
print("STUFE 3 — LATIN-TOKENS: SCHMEH vs VISION")
print("=" * 80)
print()

# 1) Vision-Token-Conf-Verteilung
print("=" * 80)
print("1) VISION-CONF-VERTEILUNG")
print("=" * 80)
conf_buckets = Counter()
for pid, rid, text, conf, rt in vision_details:
    if conf >= 0.9:
        bucket = "0.90-1.00 (sehr hoch)"
    elif conf >= 0.8:
        bucket = "0.80-0.89 (hoch)"
    elif conf >= 0.7:
        bucket = "0.70-0.79 (mittel)"
    else:
        bucket = "< 0.70 (niedrig)"
    conf_buckets[bucket] += 1
for b, c in conf_buckets.most_common():
    print(f"  {b:25s}: {c:3d}")
print(f"  TOTAL: {len(vision_details)} Vision-Tokens")
print()

# 2) Vision-Tokens pro Region-Type
print("=" * 80)
print("2) VISION-TOKENS PRO REGION-TYPE")
print("=" * 80)
v_rt = Counter()
for pid, rid, text, conf, rt in vision_details:
    v_rt[rt] += 1
for rt, c in v_rt.most_common():
    print(f"  {rt:25s}: {c:3d}")
print()

# 3) Vision-Tokens pro Page
print("=" * 80)
print("3) VISION-TOKENS PRO PAGE")
print("=" * 80)
v_page = Counter()
for pid, rid, text, conf, rt in vision_details:
    v_page[pid] += 1
for pid in sorted(v_page.keys()):
    print(f"  {pid}: {v_page[pid]:3d}")
print()

# 4) ALLE Vision-Tokens, sortiert nach conf
print("=" * 80)
print("4) ALLE VISION-TOKENS (sortiert nach conf)")
print("=" * 80)
sorted_v = sorted(vision_details, key=lambda x: -x[3])
for pid, rid, text, conf, rt in sorted_v:
    print(f"  {pid:4s} {rid:25s} conf={conf:.2f}  [{rt:18s}]  '{text[:80]}'")
print()

# 5) Region-Vergleich: Schmeh vs Vision (pro Region)
print("=" * 80)
print("5) REGION-VERGLEICH: Vision vs Schmeh in derselben Region")
print("=" * 80)
regions_with_both = []
regions_with_vision_only = []
regions_with_schmeh_only = []

for rid, sources in region_tokens.items():
    has_v = 'vision' in sources
    has_s = ('schmeh_hint' in sources) or ('schmeh_complete' in sources)
    if has_v and has_s:
        regions_with_both.append(rid)
    elif has_v:
        regions_with_vision_only.append(rid)
    elif has_s:
        regions_with_schmeh_only.append(rid)

print(f"Regionen mit Vision UND Schmeh:     {len(regions_with_both)}")
print(f"Regionen mit Vision NUR:             {len(regions_with_vision_only)}")
print(f"Regionen mit Schmeh NUR:             {len(regions_with_schmeh_only)}")
print()

# Detail-Vergleich für Regionen mit beiden
print("=" * 80)
print("6) DETAIL: Regionen mit Vision UND Schmeh (Top 20)")
print("=" * 80)
print(f"{'Region':<25}  {'Page':<5}  {'RT':<18}  Vision  |  Schmeh")
for rid in regions_with_both[:20]:
    pid = region_pid[rid]
    rt = region_rt[rid]
    v_texts = [t for t, c in region_tokens[rid].get('vision', [])]
    s_hints = [t for t, c in region_tokens[rid].get('schmeh_hint', [])]
    s_complete = [t for t, c in region_tokens[rid].get('schmeh_complete', [])]
    v_str = " | ".join(v_texts)[:60]
    s_str = " | ".join(s_hints + s_complete)[:60]
    print(f"  {rid:<23}  {pid:<5}  {rt:<18}  '{v_str}'  |  '{s_str}'")
print()

# 7) Übereinstimmungsanalyse
print("=" * 80)
print("7) WORT-ÜBEREINSTIMMUNG (Vision ↔ Schmeh)")
print("=" * 80)
# Sammle alle Vision-Wörter
vision_words = Counter()
schmeh_words = Counter()
for rid, sources in region_tokens.items():
    for t, c in sources.get('vision', []):
        for w in t.split():
            vision_words[w.strip('.,;:!?()"').upper()] += 1
    for src in ('schmeh_hint', 'schmeh_complete'):
        for t, c in sources.get(src, []):
            for w in t.split():
                schmeh_words[w.strip('.,;:!?()"').upper()] += 1

# Was ist in BEIDEN Quellen?
common = set(vision_words) & set(schmeh_words)
vision_only = set(vision_words) - set(schmeh_words)
schmeh_only = set(schmeh_words) - set(vision_words)

print(f"  Wörter in Vision UND Schmeh:  {len(common)}")
print(f"  Wörter NUR in Vision:          {len(vision_only)}")
print(f"  Wörter NUR in Schmeh:          {len(schmeh_only)}")
print()

print("  Top 20 Wörter in BEIDEN Quellen:")
for w in sorted(common, key=lambda x: -vision_words[x])[:20]:
    print(f"    {w:25s}  Vision: {vision_words[w]:3d}  Schmeh: {schmeh_words[w]:3d}")
print()

print("  Top 20 Vision-only Wörter:")
for w in sorted(vision_only, key=lambda x: -vision_words[x])[:20]:
    print(f"    {w:25s}  Vision: {vision_words[w]:3d}")
print()

print("  Top 20 Schmeh-only Wörter:")
for w in sorted(schmeh_only, key=lambda x: -schmeh_words[x])[:20]:
    print(f"    {w:25s}  Schmeh: {schmeh_words[w]:3d}")
print()

# JSON Export
out = {
    'vision_token_count': len(vision_details),
    'conf_distribution': dict(conf_buckets),
    'vision_per_rt': dict(v_rt),
    'vision_per_page': dict(v_page),
    'vision_tokens': [
        {'page': pid, 'region': rid, 'text': text, 'conf': conf, 'region_type': rt}
        for pid, rid, text, conf, rt in vision_details
    ],
    'regions_with_both': regions_with_both,
    'regions_with_vision_only': regions_with_vision_only,
    'regions_with_schmeh_only': regions_with_schmeh_only,
    'vision_words': dict(vision_words),
    'schmeh_words': dict(schmeh_words),
    'common_words': sorted(common),
    'vision_only_words': sorted(vision_only),
    'schmeh_only_words': sorted(schmeh_only),
}
with open(BASE.parent / 'scratches' / 'stufe_03' / 'latin_compare.json', 'w') as f:
    json.dump(out, f, indent=2, ensure_ascii=False)
print(f"Compare-JSON: scratches/stufe_03/latin_compare.json")
