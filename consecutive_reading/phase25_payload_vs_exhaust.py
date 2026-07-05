"""
phase25_payload_vs_exhaust.py
V7 Phase 25 — Payload vs. Exhaust Test (Anti-Apophenia Edition)

Hypothese: 11 Schlusswörter (Periode 7) enthalten mehr türkische/mongolische
Substrings als die 55 inneren Perioden (Perioden 1-6).

KORREKTE Methodik (gegen Apophenia):
- NICHT absolute Treffer zählen (innere Perioden haben mehr Daten)
- PRO-PHRASE-Trefferrate: (Anzahl TR/MN-Substrings) / (Wortlänge)
- Vergleich: 11 Schlusswörter vs 55 innere Perioden
- Statistischer Test: Mann-Whitney U (verschiedene Gruppengrößen)

Quellen für türkische/mongolische Wörter:
1. Echte türkische Wortstämme (Liste von gängigen TR-Wurzeln)
2. Echte mongolische Wortstämme (Liste von gängigen MN-Wurzeln)
3. Substrings müssen in echten TR/MN-Wörtern vorkommen
"""
import json
from pathlib import Path
from collections import Counter
import re
import urllib.request
import urllib.parse
import time

OUT = Path("bbox/burumut_20260707_V7")
OUT_NEW = Path("bbox/burumut_lexical_20260707_V7")
OUT_NEW.mkdir(parents=True, exist_ok=True)

# 1. Lade BURUMUT-Texte
with open(OUT / "burumut_texts.json") as f:
    d = json.load(f)

schluss = []
innere = []
for bnr, texts in d["burumut_texts"].items():
    n = len(texts)
    for i, t in enumerate(texts):
        if '?' not in t:
            if i == n - 1:  # Letzte Periode
                schluss.append(t)
            else:
                innere.append(t)

print(f"11 Schlusswörter: {len(schluss)}")
print(f"55 innere Perioden: {len(innere)}")
print(f"Total: {len(schluss) + len(innere)} (statt 66 — Datenanomalie)")

# 2. Echte türkische/mongolische Wortstämme
# Diese Liste basiert auf linguistischem Wissen, NICHT auf Apophenia
# Sie umfasst Wörter, die in einem echten Türkisch/Mongolisch-Wörterbuch vorkommen
TR_MN_WORDS = [
    # Türkische Wurzeln (echte Wörter)
    'ATA', 'ANA', 'OGUL', 'KIZ', 'ERKEK', 'KADIN',
    'EV', 'ODA', 'KAPI', 'PENCERE', 'MASA',
    'SU', 'TOPRAK', 'ATES', 'HAVA', 'DUMAN',
    'GUNES', 'AY', 'YILDIZ', 'GOK', 'BULUT', 'YAGMUR', 'KAR', 'RUZGAR',
    'DAG', 'TEPE', 'OV', 'NEHIR', 'GOL', 'DENIZ',
    'AGAC', 'ORMAN', 'CAYIR', 'YESIL', 'CICEK',
    'KURT', 'AYI', 'Geyik', 'KUS', 'BALIK', 'YILAN',
    'AT', 'OKUZ', 'DEVE', 'KOYUN', 'KEKI', 'KOPEK', 'KEDI',
    'YOL', 'KOPRU', 'SEHIR', 'KOY',
    'OGLAN', 'COCUK', 'INSAN', 'MILL',
    'SAGLIK', 'HASTA', 'ILAC', 'HEKIM',
    'KILIC', 'KALKAN', 'OK', 'YAY',
    'KURGAN', 'BALBAL', 'TAMGA',
    'KARA', 'AK', 'KIRMIZI', 'SARI', 'YESIL', 'MAVI', 'BEYAZ',
    'BUYUK', 'KUCUK', 'UZUN', 'KISA', 'YUKSEK', 'ALCAK',
    'YAKIN', 'UZAK', 'ESKI', 'YENI', 'GUZEL', 'CIKIN',
    'IYI', 'KOTU', 'DOGRU', 'YANLIS',
    'GEL', 'GIT', 'BIL', 'GOR', 'DUY', 'KOKLA', 'TAT',
    'YEMEK', 'ICMEK', 'UYUMAK', 'CALISMAK', 'OYNAMAK',
    'YASAMAK', 'OLMEK', 'DOGMAK',
    'YAP', 'AL', 'VER', 'SAT', 'AL',
    'DE', 'SOYLE', 'KONUS', 'YAZ', 'OKU',
    'BEG', 'BEK', 'HAN', 'KAGAN', 'YABGU', 'TUDUN',
    'KAM', 'BAGAN', 'BAGA',
    'TURK', 'TURAN', 'OZ', 'TURK',
    'KUR', 'YAP', 'INSA', 'TAMIR',
    'TAM', 'DOLU', 'BOS',
    'SABAH', 'AKSAM', 'GECE', 'OGLE',
    'BUGUN', 'DUN', 'YARIN',
    'BURADA', 'ORADA', 'NEREDE',
    'BEN', 'SEN', 'O', 'BIZ', 'SIZ', 'ONLAR',
    # Mongolische Wurzeln
    'NOYAN', 'NOION', 'BEISE', 'DARHAN',
    'TUMEN', 'MINGAN', 'JUN', 'ARBAN',
    'SARAN', 'GER', 'BARK',
    'MORIN', 'UNAGAN', 'TAHAR',
    'TSETSEG', 'BUD', 'CHULUUN',
    'NARAN', 'SARA', 'BORHAN',
    'TUUL', 'URAN', 'MONGOL',
    'TENGRI', 'BURHAN', 'BOGD',
    'NAIMAN', 'MERKIT', 'KEREY', 'KATAKIN',
    'NAADAM', 'BUKHE',
    'SUM', 'BAGA',
]

# Bereinige und erstelle Set
TR_MN_SET = set()
for w in TR_MN_WORDS:
    TR_MN_SET.add(w.upper())

# Filtere zu kurze und zu lange
TR_MN_SET = {w for w in TR_MN_SET if 3 <= len(w) <= 10}
print(f"\nTR/MN-Wortliste: {len(TR_MN_SET)} Wörter")

# 3. N-Gramm-Extraktion pro Phrase
def extract_ngrams(text, min_len=3, max_len=7):
    ngrams = []
    for n in range(min_len, max_len + 1):
        for i in range(len(text) - n + 1):
            ngrams.append(text[i:i+n])
    return ngrams

# 4. Für jede Phrase: zähle TR/MN-Substrings + sammle Beispiele
def count_tr_hits(text, word_set, min_len=3, max_len=7):
    ngrams = extract_ngrams(text, min_len, max_len)
    hits = []
    for ng in ngrams:
        if ng in word_set:
            hits.append(ng)
    return hits

print("\n" + "="*80)
print("PRO-PHRASE-TREFFERRATE")
print("="*80)

schluss_hits_per_phrase = []
schluss_examples = {}
for w in schluss:
    hits = count_tr_hits(w, TR_MN_SET)
    rate = len(hits) / len(w) if len(w) > 0 else 0
    schluss_hits_per_phrase.append((w, len(hits), rate, hits))
    schluss_examples[w] = hits
    print(f"  [SCHLUSS] {w}: {len(hits)} Treffer, Rate={rate:.3f}, Hits={hits}")

innere_hits_per_phrase = []
for w in innere:
    hits = count_tr_hits(w, TR_MN_SET)
    rate = len(hits) / len(w) if len(w) > 0 else 0
    innere_hits_per_phrase.append((w, len(hits), rate, hits))
    if hits:
        print(f"  [INNERE] {w}: {len(hits)} Treffer, Rate={rate:.3f}, Hits={hits}")

print()
print(f"Analyse innere Perioden: {len(innere_hits_per_phrase)} Phrasen")
print(f"  Davon mit Treffern: {sum(1 for _, _, _, h in innere_hits_per_phrase if h)}")
print(f"  Total Treffer: {sum(len(h) for _, _, _, h in innere_hits_per_phrase)}")
print(f"  Mittlere Treffer pro Phrase: {sum(len(h) for _, _, _, h in innere_hits_per_phrase)/len(innere_hits_per_phrase):.2f}")

# 5. Statistischer Vergleich
print("\n" + "="*80)
print("STATISTISCHER VERGLEICH: Schluss vs. Innere")
print("="*80)
schluss_total_hits = sum(len(h) for _, _, _, h in schluss_hits_per_phrase)
schluss_total_chars = sum(len(w) for w, _, _, _ in schluss_hits_per_phrase)
schluss_avg_rate = schluss_total_hits / schluss_total_chars

innere_total_hits = sum(len(h) for _, _, _, h in innere_hits_per_phrase)
innere_total_chars = sum(len(w) for w, _, _, _ in innere_hits_per_phrase)
innere_avg_rate = innere_total_hits / innere_total_chars

print(f"\nSchlusswörter:")
print(f"  Total Zeichen: {schluss_total_chars}")
print(f"  Total TR/MN-Treffer: {schluss_total_hits}")
print(f"  Trefferrate pro Zeichen: {schluss_avg_rate:.4f} ({100*schluss_avg_rate:.2f}%)")
print(f"  Mittlere Treffer pro Phrase: {schluss_total_hits/len(schluss_hits_per_phrase):.2f}")

print(f"\nInnere Perioden:")
print(f"  Total Zeichen: {innere_total_chars}")
print(f"  Total TR/MN-Treffer: {innere_total_hits}")
print(f"  Trefferrate pro Zeichen: {innere_avg_rate:.4f} ({100*innere_avg_rate:.2f}%)")
print(f"  Mittlere Treffer pro Phrase: {innere_total_hits/len(innere_hits_per_phrase):.2f}")

if innere_avg_rate > 0:
    ratio = schluss_avg_rate / innere_avg_rate
    print(f"\nRATIO: Schlusswörter sind {ratio:.1f}x reicher an TR/MN-Substrings pro Zeichen")
else:
    print(f"\nRATIO: Innere haben 0 Treffer pro Zeichen (undefiniert)")

# 6. Mann-Whitney U-Test
try:
    from scipy.stats import mannwhitneyu
    schluss_rates = [rate for _, _, rate, _ in schluss_hits_per_phrase]
    innere_rates = [rate for _, _, rate, _ in innere_hits_per_phrase]
    stat, p_value = mannwhitneyu(schluss_rates, innere_rates, alternative='greater')
    print(f"\nMann-Whitney U Test (Schluss > Innere):")
    print(f"  U = {stat}")
    print(f"  p-value = {p_value:.4f}")
    if p_value < 0.05:
        print(f"  → SIGNIFIKANT: Schlusswörter enthalten statistisch mehr TR/MN-Substrings")
    else:
        print(f"  → NICHT SIGNIFIKANT: Kein Unterschied zwischen Schichten")
except ImportError:
    print("\nKein scipy verfügbar — Mann-Whitney Test übersprungen")

# 7. Speichere Ergebnisse
results = {
    "metadata": {
        "phase": "V7 / Phase 25",
        "datum": "2026-07-05",
        "methode": "Pro-Phrase-Trefferrate statt absolute Treffer (Anti-Apophenia)",
        "n_tr_mn_words": len(TR_MN_SET),
        "n_schluss": len(schluss),
        "n_innere": len(innere),
    },
    "schlusswoerter": [
        {"wort": w, "n_hits": h, "rate": r, "hits": ht}
        for w, h, r, ht in schluss_hits_per_phrase
    ],
    "innere_perioden": [
        {"wort": w, "n_hits": h, "rate": r, "hits": ht}
        for w, h, r, ht in innere_hits_per_phrase if ht
    ],
    "statistik": {
        "schluss_total_hits": schluss_total_hits,
        "schluss_total_chars": schluss_total_chars,
        "schluss_avg_rate": schluss_avg_rate,
        "innere_total_hits": innere_total_hits,
        "innere_total_chars": innere_total_chars,
        "innere_avg_rate": innere_avg_rate,
        "ratio": schluss_avg_rate / innere_avg_rate if innere_avg_rate > 0 else None,
    },
}
with open(OUT_NEW / "payload_vs_exhaust.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
print(f"\n✓ Gespeichert: {OUT_NEW}/payload_vs_exhaust.json")
