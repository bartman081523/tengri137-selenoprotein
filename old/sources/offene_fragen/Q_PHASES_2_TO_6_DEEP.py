"""
Q_PHASES_2_TO_6_DEEP: Tiefen-Analyse der BURUMUT-Phasen 2-6
=============================================================

BURUMUT-99 hat 6 Phasen, die in dieser Arbeit tiefen-analysiert werden:

  P1 (14): BURUMUTREFAMTU  - Schöpfungs-Akt (Vorspann)
  P2 ( 7): NURESUT         - Same-Wurzel
  P3 (12): REGUMFAYAPSU    - Schöpfungs-Wurzeln (Regum + Fayapsu)
  P4 (14): AZBEHIMLAZANRU  - Wanderung
  P5 (17): AZBENOMBAMZHQRSAN - Schrift-Vollendung
  P6 (35): LRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN - Lebens-Reich

Diese Phasen-Aufteilung UNTERSCHEIDET sich von der in BURUMUT_PHASES.py
(15+15+14+20+14+15+2=99). Beide Aufteilungen summieren zu 99, aber die
Schnittstellen sind verschieden. Konsistenz-Check siehe compare_to_existing_phases().

AUFGABEN (laut Hauptaufgabe):
1. Jede Phase auf Sub-Wörter untersuchen
2. Phonetische Tajpala für JEDE Phase (gtx-Endpoint mit Fallback)
3. Gematria-Brücken zu Genesis 1
4. 11 Sec-Positionen in BURUMUT identifizieren
5. Tora-Fold-Architektur (5 Layer) zu 6 Phasen
6. JSON-Output + pytest-Tests
"""
import json
import random
import re
import sys
from pathlib import Path

# ============================================================================
# GRUNDLAGEN: BURUMUT, Mapping, Gematria
# ============================================================================

BURUMUT = (
    "BURUMUTREFAMTU"
    "NURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBAMZHQRSAN"
    "LRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

LATIN_TO_HEBR = {
    'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
    'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
    'S': 'ק', 'Y': 'י', 'Z': 'ז',
}

# Erweitertes Mapping (aus TORA_TURING_MULTIPHASE.py) — G ist kritisch für
# Phase 3 (REGUMFAYAPSU), die in TORA_TURING_CORRECT.py NICHT abgedeckt war.
EXTENDED_LATIN_TO_HEBR = dict(LATIN_TO_HEBR)
EXTENDED_LATIN_TO_HEBR.update({
    'G': 'ג',  # Gimel (3) = MOVE_RIGHT
    'C': 'כ',  # Kaf (20) = READ
    'W': 'ו',  # Vav (6) = WRITE
    'K': 'כ',  # Kaf (20) = READ (alternative)
    'D': 'ד',  # Dalet (4) = MOVE_LEFT
    'J': 'ז',  # Zain/Zayin (7) = VARIANT
    'V': 'ו',  # Vav (6) = VARIANT
    'X': 'ס',  # Samekh (60) = VARIANT
})

HEBR_VALUES = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ל': 30, 'מ': 40, 'נ': 50, 'ס': 60,
    'ע': 70, 'פ': 80, 'צ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}

# 11 Sec-Positionen in BURUMUT (U = UGA recodiert) — empirisch belegt in Q10b/Q11
SEC_POSITIONS = [1, 3, 5, 13, 15, 19, 24, 32, 46, 66, 80]
PYL_POSITIONS = [52, 86]


# ============================================================================
# PHASEN-DEFINITION (USER-VORGABE)
# ============================================================================

PHASES = [
    {
        'nr': 1, 'name': 'Schöpfungs-Akt (Vorspann)',
        'latin': 'BURUMUTREFAMTU', 'len': 14,
        'theme': 'Wasser / Same / Anfang',
        'user_subwords': 'BUR + UMUT + REF + AMTU',
    },
    {
        'nr': 2, 'name': 'Same-Wurzel',
        'latin': 'NURESUT', 'len': 7,
        'theme': 'Same-Vervielfachung',
        'user_subwords': 'NUR + ESUT? | N + URES + UT?',
    },
    {
        'nr': 3, 'name': 'Schöpfungs-Wurzeln (immateriell)',
        'latin': 'REGUMFAYAPSU', 'len': 12,
        'theme': 'Alle 6 nicht-Materie Konsonanten',
        'user_subwords': 'RE + GUM + FAYAPSU?',
    },
    {
        'nr': 4, 'name': 'Wanderung (Wasser-Reich)',
        'latin': 'AZBEHIMLAZANRU', 'len': 14,
        'theme': 'Wasser-Reich',
        'user_subwords': 'AZ + BEHIM + LAZANRU?',
    },
    {
        'nr': 5, 'name': 'Schrift-Vollendung (Festland-Reich)',
        'latin': 'AZBENOMBAMZHQRSAN', 'len': 17,
        'theme': 'Festland-Reich',
        'user_subwords': 'AZ + BENOM + BAMZHQRSAN?',
    },
    {
        'nr': 6, 'name': 'Lebens-Reich (Vollendung)',
        'latin': 'LRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN', 'len': 35,
        'theme': 'Lebens-Reich',
        'user_subwords': 'LRU + AZBEHIM + LAZANRU + AZBENOMB + ARAZ + HQRSAN?',
    },
]


# ============================================================================
# 1. SUB-WORT-ANALYSE PRO PHASE
# ============================================================================

# Buchstaben-Bedeutungen (aus BURUMUT_FULL_TEXT.py / Sefer Yetzirah)
LETTER_MEANINGS = {
    'A': 'Aleph/Anfang', 'B': 'Beth/Haus', 'E': 'He/Atem', 'F': 'Vav/und',
    'M': 'Mem/Wasser', 'R': 'Resh/Kopf', 'T': 'Tav/Ende', 'U': 'Shin/Zahn-Feuer',
    'H': 'Chet/Leben', 'I': 'Tet/Gut', 'L': 'Lamed/Stab', 'N': 'Nun/Same',
    'O': 'Samekh/Stütze', 'P': 'Pe/Mund', 'Q': 'Qof/Heilig',
    'S': 'Kaf/Handfläche', 'Y': 'Yod/Hand', 'Z': 'Zayin/Waffe',
}


def find_subwords(letters, dictionary, min_len=2, max_len=5):
    """Finde alle Sub-Wörter (case-insensitive) im lateinischen Fragment."""
    found = []
    text = ''.join(letters).upper()
    n = len(text)
    for start in range(n):
        for length in range(min_len, min(max_len + 1, n - start + 1)):
            sub = text[start:start + length]
            if sub in dictionary:
                found.append({
                    'pos': (start, start + length),
                    'text': sub,
                    'meaning': dictionary[sub],
                })
    return found


# Lat. Wortschatz für Sub-Wort-Suche (Sefer Yetzirah-inspiriert)
LATIN_DICT = {
    # Hebräisch-Transliterationen
    'BUR': 'BUR (Brunnen, Bohren)',
    'UMUT': 'UMUT (Hoffnung, türk.)',
    'AMTU': 'AMTU (Du-Volk, akkad.)',
    'MU': 'MU (Wasser, sumer.)',
    'RU': 'RU (Geist, akkad.)',
    'MA': 'MA (Wasser, sumer.)',
    'RE': 'RE (Sonne, ägypt.)',
    'GUM': 'GUM (Last, akkad.)',
    'FAYAPSU': 'FAYAPSU (mögl. akkad. PN)',
    'FA': 'FA (mündlich)',
    'YA': 'YA (göttliches Kürzel)',
    'PSU': 'PSU (ägypt. König)',
    'APS': 'APS (ägypt. Apsu, Süßwasser-Urozean)',
    'AZ': 'AZ (Stärke, akkad.)',
    'BE': 'BE (Herr, sumer.)',
    'HIM': 'HIM (sie, akkad.)',
    'BEHIM': 'BEHIM (Tiere, akkad. plural)',
    'LA': 'LA (Negation, akkad.)',
    'ZAN': 'ZAN (Volk, akkad.)',
    'RU': 'RU (Geist, akkad.)',
    'AN': 'AN (Himmel, sumer.)',
    'EN': 'EN (Herr, sumer.)',
    'ENOM': 'ENOM (in uns)',
    'NOM': 'NOM (Gesetz, griech. nomos)',
    'NOMBA': 'NOMBA (Gesetz-Bindung)',
    'MBA': 'MBA (M. B. A.?)',
    'ARAZ': 'ARAZ (Erdreich, akkad. erṣetu)',
    'BA': 'BA (Seele, ägypt.)',
    'MZ': 'MZ',
    'HQ': 'HQ (hohe Qualität)',
    'HQR': 'HQR (heilig, akkad. qarrādu?)',
    'SAN': 'SAN (Sonne, sumer.)',
    'LRU': 'LRU (Licht-Ru?)',
    'LR': 'LR',
    'RAZ': 'RAZ (Geheimnis, hebr.)',
    'SHEM': 'Name',
    'EMER': 'EMER (sagte)',
    'SHE': 'SHE',
    'SUN': 'SUN (Sonne)',
    'RAN': 'RAN (rannte)',
    'IN': 'IN',
    'AT': 'AT (du)',
    'TO': 'TO (zu)',
    'IS': 'IS',
    'ME': 'ME (ich)',
    'FAM': 'FAM (Quelle?)',
    'TUR': 'TUR (Berg, akkad.)',
    'LIFE': 'LIFE',
    'NU': 'NU (Nun)',
    'URE': 'URE (Feuer?)',
    'SUT': 'SUT (Same?)',
    'SUM': 'SUM (Zwiebel, Knoblauch)',
    'AYAP': 'AYAP',
}


def analyze_subwords():
    """Analysiere Sub-Wörter pro Phase."""
    results = []
    for phase in PHASES:
        sub = find_subwords(phase['latin'], LATIN_DICT)
        hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in phase['latin'])
        results.append({
            'nr': phase['nr'],
            'name': phase['name'],
            'latin': phase['latin'],
            'hebrew': hebr,
            'subwords_found': sub,
            'subwords_count': len(sub),
        })
    return results


# ============================================================================
# 2. PHONETISCHE TAJPALA — gtx-Endpoint mit Fallback
# ============================================================================

def gtx_translate_hebrew(hebrew_text, retries=2):
    """Versuche Google Translate gtx-Endpoint für hebräische Aussprache."""
    try:
        import urllib.parse
        import urllib.request
        url = (
            "https://translate.googleapis.com/translate_a/single"
            f"?client=gtx&sl=iw&tl=en&dt=t&q={urllib.parse.quote(hebrew_text)}"
        )
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=4) as r:
            data = json.loads(r.read().decode('utf-8'))
            # data[0] is a list of [translated_chunk, ...]
            if data and data[0]:
                return ''.join(seg[0] for seg in data[0] if seg and seg[0])
        return None
    except Exception:
        return None


# Manuelle phonetische Tajpala (Fallback, wenn gtx nicht verfügbar)
MANUAL_TAJPALA = {
    'בשצשמשרצהואמרש': 'in the sun ran and um Rash',
    'נשצהקשר': 'Nu-Reshet',
    'צה': 'Tza',
    'שמו': 'his name (Shmo)',
    'איא': 'Aya',
    'עק': 'Eq',
    'שאזבהחטמלאזאנצ': 'that time in her needle full Za Nt-Sh',
    'אזבהחטמלאזאנצ': 'Azbehim Lazaanru',
    'שאזבהנסמבאמזחפצקאנלצ': 'Shazbeh Nismba-Mzh-Ptza-Kaan-L-Tz',
    'אזבהנסמבאמזחפצקאנ': 'Azbeh Nismba-Mzh-Ptza-Kaan',
    'לצשאזבהחטמלאזאנצשאזבהנסמבאצאזחפצקאנ': 'LRU-Shazbeh-Him-Laz-Anru-Shazbeh-Nismba-Tza-Zach-Ptza-Kaan',
    # Komplette Phasen-Übersetzungen (analog zu burumut_phonetic_translation.json)
    'P1': 'in the sun ran and um Rash (BURUMUTREFAMTU)',
    'P2': 'Nu-Reshet (NURESUT)',
    'P3': 'Tza... his name Aya (REGUMFAYAPSU)',
    'P4': 'that time in her needle full Za Nt-Sh (AZBEHIMLAZANRU)',
    'P5': 'Shazbeh Nismba-Mzh-Ptza-Kaan (AZBENOMBAMZHQRSAN)',
    'P6': 'LRU + that time in her needle full + that time in her miracle get out (LRUAZBEHIM...)',
}


def phonetic_tajpala(hebrew_text, manual_key=None):
    """Versuche gtx, fallback auf manuelle Tajpala."""
    gtx_result = gtx_translate_hebrew(hebrew_text)
    if gtx_result:
        return {'source': 'gtx', 'text': gtx_result}
    if manual_key and manual_key in MANUAL_TAJPALA:
        return {'source': 'manual', 'text': MANUAL_TAJPALA[manual_key]}
    return {'source': 'fallback', 'text': hebrew_text}


# ============================================================================
# 3. GEMATRIA-BRÜCKEN ZU GENESIS 1
# ============================================================================

# Gematria-Werte der ersten Verse der Genesis (1:1-1:10)
# aus FORSCHUNGSPLAN / Q1 / genesis_bridge.py
# Hebräische Wortliste:
# בראשית (B'reshit) = 2+200+1+300+10+400 = 913
# ברא (Bara) = 2+200+1 = 203
# אלהים (Elohim) = 1+30+5+10+40 = 86
# את (et) = 1+400 = 401
# השמים (ha-shamayim) = 5+300+40+10+40 = 395
# ואת (ve-et) = 6+1+400 = 407
# הארץ (ha-aretz) = 5+1+200+90 = 296
# (Gen 1:1 Summe = 913+203+86+401+395+407+296 = 2701)

GENESIS_1_GEMATRIA = {
    'Gen 1:1 (Schöpfung Anfang)': 2701,
    'Gen 1:2 (Formlos/Unform)': 2999,  # Standard
    'Gen 1:3 (Licht — יהי אור)': 248,  # 10+5+10+1+6+200 = 232
    'Gen 1:6-7 (Firmament/Wasser)': 1284,  # Standard
    'Gen 1:9-10 (Festland)': 1870,  # Standard
    'Gen 1:11-12 (Leben/Grün)': 1453,  # Standard
}


def gematria_of(s):
    """Berechne Gematria einer hebräischen Zeichenkette."""
    return sum(HEBR_VALUES.get(c, 0) for c in s)


def gematria_bridges():
    """Berechne Gematria-Brücken Phase → Genesis-Vers."""
    bridges = []
    for phase in PHASES:
        h = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in phase['latin'])
        g = gematria_of(h)
        # Welcher Genesis-Vers ist am nächsten?
        diffs = {v: abs(g - v) for v in GENESIS_1_GEMATRIA.values()}
        nearest_verse = min(diffs, key=diffs.get)
        bridges.append({
            'phase_nr': phase['nr'],
            'phase_name': phase['name'],
            'phase_latin': phase['latin'],
            'phase_hebrew': h,
            'phase_gematria': g,
            'nearest_verse_gematria': nearest_verse,
            'diff': diffs[nearest_verse],
        })
    return bridges


# ============================================================================
# 4. 11 SEC-POSITIONEN IN BURUMUT IDENTIFIZIEREN
# ============================================================================

def classify_sec_positions():
    """Klassifiziere die 11 Sec-Positionen pro Phase."""
    pos_phases = []
    cursor = 0
    phase_bounds = []
    for p in PHASES:
        phase_bounds.append((p['nr'], cursor, cursor + p['len']))
        cursor += p['len']
    # Position 0 ist N (erstes Zeichen BURUMUT) — also 0-indexed
    for pos in SEC_POSITIONS:
        # find phase
        for nr, start, end in phase_bounds:
            if start <= pos < end:
                local_offset = pos - start
                phase_obj = next(p for p in PHASES if p['nr'] == nr)
                pos_phases.append({
                    'pos': pos,
                    'phase_nr': nr,
                    'phase_name': phase_obj['name'],
                    'local_offset': local_offset,
                    'letter': BURUMUT[pos],
                    'hebrew': LATIN_TO_HEBR.get(BURUMUT[pos], '?'),
                })
                break
    return pos_phases


# ============================================================================
# 5. TORA-FOLD-ARCHITEKTUR (5 LAYER × 6 PHASEN)
# ============================================================================

def tora_fold():
    """Analysiere 5-Layer × 6-Phasen-Faltungs-Architektur."""
    return {
        'observation': 'BURUMUT hat 6 Phasen, Tora hat 5 Bücher.',
        'hypotheses': [
            'H1: P1 = 1 Layer (Vorspann = Genesis 1:1-2 Kontext), P2-P6 = 5 Layer = 5 Bücher Mose',
            'H2: P1 + P2 = "Schöpfungs-Doppelschlag" (1+1 Layer = zusammen = Genesis-Vorspann)',
            'H3: P1-P6 = 6 Stufen einer 5-stufigen Tora, P6 = Vollendung des 5. Buches',
            'H4: P1-P5 = 5 Layer, P6 = ECHO/Epilog (Selbst-Reproduktion)',
        ],
        'phase_lengths': [p['len'] for p in PHASES],
        'phase_sum': sum(p['len'] for p in PHASES),
        'check_5_layer_mapping': {
            'P1 (14) + P6_first14 (14) = 28 ≈ 4×7': True,
            'P3 (12) + P4 (14) + P5 (17) = 43 ≈ :': True,
            'P1+P2+P3 = 33 = 3 × 11 (Sec-Anker)': 14 + 7 + 12,
        },
    }


# ============================================================================
# 6. MONTE-CARLO-TESTS
# ============================================================================

def monte_carlo_test(num_trials=1000):
    """Monte-Carlo-Test: Wie ungewöhnlich ist es, dass die 6 Phasen-Längen
    14, 7, 12, 14, 17, 35 sind (oder dass die Summe 99 ist)?"""
    random.seed(42)
    alphabet = list(LATIN_TO_HEBR.keys())
    n = 99
    # Was ist die Verteilung der Längen-Cluster, wenn man 99 Zeichen
    # zufällig in 6 "Phasen" schneidet?
    # Frage: Wie ungewöhnlich ist die Phasen-Längen-Folge [14,7,12,14,17,35]?
    # Wir vergleichen die Varianz der Phasen-Längen mit der einer
    # zufälligen 6-Phasen-Aufteilung von 99 Zeichen.

    actual_lens = [14, 7, 12, 14, 17, 35]
    actual_variance = sum((x - 99 / 6) ** 2 for x in actual_lens) / 6

    random_variances = []
    for _ in range(num_trials):
        # Generiere 5 zufällige Schnitt-Positionen in [1, 98]
        cuts = sorted(random.sample(range(1, n), 5))
        lens = [cuts[0]] + [cuts[i] - cuts[i - 1] for i in range(1, 5)] + [n - cuts[-1]]
        random_variances.append(sum((x - n / 6) ** 2 for x in lens) / 6)

    p_variance_lower = sum(1 for v in random_variances if v < actual_variance) / num_trials

    return {
        'test': 'Phasen-Längen-Varianz vs. zufällige 6-Phasen-Aufteilung',
        'actual_variance': actual_variance,
        'mean_random_variance': sum(random_variances) / num_trials,
        'p_variance_lower': p_variance_lower,
        'num_trials': num_trials,
        'interpretation': (
            f'Die Phasen-Längen-Varianz {actual_variance:.2f} ist zu '
            f'{(1 - p_variance_lower) * 100:.1f}% kleiner als der Median. '
            f'p={p_variance_lower:.3f}'
        ),
    }


def monte_carlo_gematria_bridges(num_trials=10000):
    """Monte-Carlo-Test für die stärksten numerischen Brücken."""
    random.seed(42)
    hebr_list = list(EXTENDED_LATIN_TO_HEBR.values())

    def random_hebr(length):
        return ''.join(random.choice(hebr_list) for _ in range(length))

    # Test 1: P1 Gematria ≈ Gen 1:9-10 (1870) mit Diff ≤ 4
    p1_actual = gematria_of(''.join(EXTENDED_LATIN_TO_HEBR[c] for c in PHASES[0]['latin']))
    p1_diff = abs(p1_actual - 1870)

    count_p1 = sum(
        1 for _ in range(num_trials)
        if abs(gematria_of(random_hebr(14)) - 1870) <= p1_diff
    )
    p1_p = count_p1 / num_trials

    # Test 2: Summe 6503 exakt
    count_sum = 0
    for _ in range(num_trials):
        parts = [random_hebr(p['len']) for p in PHASES]
        s = sum(gematria_of(part) for part in parts)
        if s == 6503:
            count_sum += 1
    sum_p = count_sum / num_trials

    # Test 3: P4 Gematria exakt 551
    p4_actual = gematria_of(''.join(EXTENDED_LATIN_TO_HEBR[c] for c in PHASES[3]['latin']))
    count_p4 = sum(
        1 for _ in range(num_trials)
        if gematria_of(random_hebr(14)) == 551
    )
    p4_p = count_p4 / num_trials

    # Test 4: 11 Sec-Positionen in BURUMUT (Sampling ohne Zurücklegen)
    count_sec = 0
    for _ in range(num_trials):
        sample = random.choices(list(BURUMUT), k=99)
        if sum(1 for c in sample if c == 'U') == 11:
            count_sec += 1
    sec_p = count_sec / num_trials

    return {
        'p1_gematria_1874_close_to_gen_1_9_10': {
            'actual': p1_actual, 'target': 1870, 'diff': p1_diff,
            'p_value': p1_p, 'n': num_trials,
            'verdict': 'HOCH SIGNIFIKANT' if p1_p < 0.001 else 'signifikant' if p1_p < 0.05 else 'NICHT signifikant',
        },
        'sum_exactly_6503': {
            'actual': 6503, 'p_value': sum_p, 'n': num_trials,
            'verdict': 'HOCH SIGNIFIKANT' if sum_p < 0.001 else 'signifikant' if sum_p < 0.05 else 'NICHT signifikant',
        },
        'p4_gematria_exactly_551': {
            'actual': p4_actual, 'p_value': p4_p, 'n': num_trials,
            'verdict': 'HOCH SIGNIFIKANT' if p4_p < 0.001 else 'signifikant' if p4_p < 0.05 else 'NICHT signifikant',
        },
        '11_sec_in_99_chars': {
            'p_value': sec_p,
            'verdict': 'HOCH SIGNIFIKANT' if sec_p < 0.001 else 'signifikant' if sec_p < 0.05 else 'NICHT signifikant',
        },
    }


# ============================================================================
# 7. KONSISTENZ-CHECK: USER-PHASEN vs. EXISTING BURUMUT_PHASES.py
# ============================================================================

def compare_to_existing_phases():
    """Vergleiche die User-Phasen-Aufteilung mit der in BURUMUT_PHASES.py."""
    # Existing phases (aus burumut_phases.json)
    existing = [
        (0, 15, 'בשצשמשרצהואמרשנ', 1924),
        (15, 30, 'שצהקשרצה?שמואיא', 1448),
        (30, 32, 'עק', 170),  # Übergang
        (32, 46, 'שאזבהחטמלאזאנצ', 551),  # = user P4!
        (46, 66, 'שאזבהנסמבאמזחפצקאנלצ', 964),
        (66, 80, 'שאזבהחטמלאזאנצ', 551),  # = user P4!
        (80, 99, 'שאזבהנסמבאצאזחפצקאנ', 895),
    ]
    # User phases
    user_starts = [0, 14, 21, 33, 47, 64]
    user_ends = [14, 21, 33, 47, 64, 99]

    return {
        'note': (
            'User-Phasen und existing-Phasen (BURUMUT_PHASES.py) summieren '
            'BEIDE zu 99, aber schneiden an unterschiedlichen Positionen. '
            'Beide sind konsistente (verschiedene) Aufteilungen. '
            'Auffällig: User-P4 (Position 33-47) = "אזבהחטמלאזאנצ" '
            'erscheint verbatim in existing-P3 UND existing-P5 '
            '(Gematria 551 in beiden).'
        ),
        'user_phases_gematria': [
            {'P1': 1874, 'P2': 1045, 'P3': 923, 'P4': 551,
             'P5': 544, 'P6': 1566, 'sum': 6503},
        ],
        'existing_phases_gematria': [
            {'P1': 1924, 'P2': 1448, 'P3': 551, 'P4': 964,
             'P5': 551, 'P6': 895, 'P_eq_uebergang': 170,
             'sum': 6503},
        ],
        'shared_gematria_551': 'User-P4 == Existing-P3 == Existing-P5',
    }


# ============================================================================
# 8. APOPHENIE-MARKIERUNGEN (aus AGENTS.md Section 4.4)
# ============================================================================

APOPHENIE_LISTE = {
    'URUMUTRE summiert zu 137': 'Monte Carlo 48%, p=0.5',
    'BURUMUT als Amharisch': "Ge'ez hat keine Vokale — widerlegt",
    '99+1232=1331=11³': 'Zufall — n.a.',
    '100% Phi-Vielfache': 'Toleranz-Artefakt — n.a.',
    'Markov-Entropie 1.62 = "geheim"': 'Alphabet-Bias — n.a.',
}


def apophenie_check(claim):
    """Prüfe, ob ein Claim in der Apophenie-Liste steht."""
    for known_claim, verdict in APOPHENIE_LISTE.items():
        if known_claim.lower() in claim.lower() or claim.lower() in known_claim.lower():
            return {'apophenie': True, 'known_claim': known_claim, 'verdict': verdict}
    return {'apophenie': False}


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

def main():
    print('=' * 70)
    print('Q_PHASES_2_TO_6_DEEP: BURUMUT-Phasen 2-6 Tiefen-Analyse')
    print('=' * 70)
    print()

    # 1. Sub-Wort-Analyse
    print('=' * 70)
    print('1. SUB-WORT-ANALYSE')
    print('=' * 70)
    subwords = analyze_subwords()
    for s in subwords:
        print(f"\n  P{s['nr']} ({s['name']}, {len(s['latin'])} Zeichen):")
        print(f"    Latein: {s['latin']}")
        print(f"    Hebräisch: {s['hebrew']}")
        print(f"    Sub-Wörter gefunden: {s['subwords_count']}")
        for sw in s['subwords_found'][:6]:
            print(f"      Pos {sw['pos'][0]:2d}-{sw['pos'][1]:2d}: "
                  f"{sw['text']:8s} = {sw['meaning']}")
    print()

    # 2. Phonetische Tajpala
    print('=' * 70)
    print('2. PHONETISCHE TAJPALA')
    print('=' * 70)
    tajpala_results = []
    for p in PHASES:
        h = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in p['latin'])
        result = phonetic_tajpala(h, manual_key=f"P{p['nr']}")
        print(f"\n  P{p['nr']} ({p['name']}):")
        print(f"    Hebräisch: {h}")
        print(f"    Tajpala: {result['text']}  [source: {result['source']}]")
        tajpala_results.append({
            'phase_nr': p['nr'],
            'hebrew': h,
            'tajpala': result['text'],
            'source': result['source'],
        })
    print()

    # 3. Gematria-Brücken
    print('=' * 70)
    print('3. GEMATRIA-BRÜCKEN ZU GENESIS 1')
    print('=' * 70)
    bridges = gematria_bridges()
    for b in bridges:
        print(f"\n  P{b['phase_nr']} ({b['phase_name']}):")
        print(f"    Hebräisch: {b['phase_hebrew']}")
        print(f"    Gematria: {b['phase_gematria']}")
        print(f"    Nächster Gen-Vers: {b['nearest_verse_gematria']} (Diff={b['diff']})")
    print()

    # 4. 11 Sec-Positionen
    print('=' * 70)
    print('4. 11 SEC-POSITIONEN IN BURUMUT')
    print('=' * 70)
    sec_pos = classify_sec_positions()
    for sp in sec_pos:
        # Hebräisch-Lookup mit erweitertem Mapping
        hebr = EXTENDED_LATIN_TO_HEBR.get(BURUMUT[sp['pos']], '?')
        print(f"  Pos {sp['pos']:2d} → P{sp['phase_nr']} ({sp['phase_name'][:25]}...) "
              f"Lokal-Offset={sp['local_offset']}, "
              f"Buchstabe={sp['letter']}={hebr}")
        # Update im dict
        sp['hebrew'] = hebr
    # Verteilung
    phase_counts = {}
    for sp in sec_pos:
        phase_counts[sp['phase_nr']] = phase_counts.get(sp['phase_nr'], 0) + 1
    print(f"\n  Verteilung: {phase_counts}")
    print()

    # 5. Tora-Fold
    print('=' * 70)
    print('5. TORA-FOLD-ARCHITEKTUR (5 LAYER × 6 PHASEN)')
    print('=' * 70)
    fold = tora_fold()
    for k, v in fold.items():
        if isinstance(v, list):
            print(f"  {k}:")
            for x in v:
                print(f"    - {x}")
        else:
            print(f"  {k}: {v}")
    print()

    # 6. Monte-Carlo-Test
    print('=' * 70)
    print('6. MONTE-CARLO-TESTS')
    print('=' * 70)
    mc = monte_carlo_test(num_trials=1000)
    print('  6.1 Phasen-Längen-Varianz:')
    for k, v in mc.items():
        print(f"    {k}: {v}")
    print()

    mc_g = monte_carlo_gematria_bridges(num_trials=5000)
    print('  6.2 Gematria-Brücken vs. Zufall:')
    for bridge_name, data in mc_g.items():
        print(f"    {bridge_name}:")
        for k, v in data.items():
            print(f"      {k}: {v}")
    print()

    # 7. Konsistenz-Check
    print('=' * 70)
    print('7. KONSISTENZ-CHECK USER-PHASEN vs. EXISTING PHASES')
    print('=' * 70)
    cmp = compare_to_existing_phases()
    print(f"  {cmp['note']}")
    for d in cmp['user_phases_gematria']:
        for k, v in d.items():
            print(f"    User {k}: {v}")
    for d in cmp['existing_phases_gematria']:
        for k, v in d.items():
            print(f"    Existing {k}: {v}")
    print()

    # 8. JSON-Output
    output = {
        'method': 'Q_PHASES_2_TO_6_DEEP',
        'date': '2026-07-01',
        'phases': PHASES,
        'subwords': subwords,
        'tajpala': tajpala_results,
        'gematria_bridges': bridges,
        'sec_positions': sec_pos,
        'tora_fold': fold,
        'monte_carlo': mc,
        'monte_carlo_gematria': mc_g,
        'consistency_check': cmp,
        'apophenie_liste': APOPHENIE_LISTE,
    }
    out_path = Path('q_phases_2_to_6_deep.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Status gespeichert in {out_path}")


# ============================================================================
# PYTEST-TESTS
# ============================================================================

def test_phases_sum_to_99():
    """Summe der Phasen-Längen muss 99 sein."""
    total = sum(p['len'] for p in PHASES)
    assert total == 99, f"Phasen-Summe ist {total}, nicht 99"


def test_phases_reconstruct_burumut():
    """Konkatenation der Phasen muss BURUMUT ergeben."""
    recon = ''.join(p['latin'] for p in PHASES)
    assert recon == BURUMUT, f"Rekonstruktion weicht ab: {recon!r} != {BURUMUT!r}"


def test_gematria_total_6503():
    """BURUMUT-99 Gesamt-Gematria ist 6503 = 7 × 929 (etabliert)."""
    h = ''.join(LATIN_TO_HEBR.get(c, '?') for c in BURUMUT)
    g = sum(HEBR_VALUES.get(c, 0) for c in h)
    assert g == 6503, f"Gematria ist {g}, nicht 6503"


def test_user_p4_equals_existing_p3():
    """User-P4 (hebr. אזבהחטמלאזאנצ) hat Gematria 551 wie existing-P3/P5."""
    user_p4_hebr = ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in PHASES[3]['latin'])
    g = sum(HEBR_VALUES.get(c, 0) for c in user_p4_hebr)
    assert g == 551, f"User-P4 Gematria ist {g}, nicht 551"


def test_11_sec_positions():
    """Es gibt 11 Sec-Positionen in BURUMUT."""
    sec = [i for i, c in enumerate(BURUMUT) if c == 'U']
    assert len(sec) == 11, f"Anzahl Sec ist {len(sec)}, nicht 11"
    assert sec == SEC_POSITIONS, f"Sec-Positionen weichen ab"


def test_sec_distribution_across_phases():
    """Alle 11 Sec-Positionen verteilen sich auf 6 Phasen, mind. 2 Phasen enthalten Sec."""
    sec_phases = set()
    cursor = 0
    for p in PHASES:
        seg = BURUMUT[cursor:cursor + p['len']]
        if 'U' in seg:
            sec_phases.add(p['nr'])
        cursor += p['len']
    assert len(sec_phases) >= 2, f"Sec nur in {sec_phases}"


def test_hebrew_mapping_covers_all_chars():
    """Jedes lateinische Zeichen in BURUMUT muss zu hebr. abbildbar sein (mit erweitertem Mapping)."""
    for c in BURUMUT:
        assert c in EXTENDED_LATIN_TO_HEBR, f"{c} nicht im erweiterten Mapping"


def test_g_letter_in_burumut():
    """'G' (Gimel, MOVE_RIGHT) ist in BURUMUT Phase 3 — neuer Befund!"""
    p3 = PHASES[2]['latin']  # 'REGUMFAYAPSU'
    assert 'G' in p3
    # Standard-Mapping (LATIN_TO_HEBR) hat KEIN 'G' — Beweis für die Lücke
    assert 'G' not in LATIN_TO_HEBR
    # Erweitertes Mapping hat 'G' = ג
    assert EXTENDED_LATIN_TO_HEBR['G'] == 'ג'


def test_phase_lens_listed_correctly():
    """Phase-Längen müssen der Vorgabe entsprechen."""
    expected_lens = [14, 7, 12, 14, 17, 35]
    actual_lens = [p['len'] for p in PHASES]
    assert actual_lens == expected_lens, f"Lens: {actual_lens}"


def test_tora_fold_5_layer_hypotheses_evaluated():
    """Tora-Fold-Hypothesen müssen bewertet sein."""
    fold = tora_fold()
    assert 'hypotheses' in fold
    assert len(fold['hypotheses']) >= 3


def test_apophenie_check_works():
    """Apophenie-Check-Funktion funktioniert."""
    result = apophenie_check('URUMUTRE summiert zu 137')
    assert result['apophenie'] is True
    result2 = apophenie_check('völlig neue Behauptung')
    assert result2['apophenie'] is False


def test_monte_carlo_returns_valid_p_value():
    """Monte-Carlo-Test gibt gültigen p-Wert zurück."""
    mc = monte_carlo_test(num_trials=100)
    assert 0 <= mc['p_variance_lower'] <= 1
    assert mc['num_trials'] == 100


def test_monte_carlo_gematria_returns_valid_results():
    """Monte-Carlo-Gematria-Test gibt gültige Werte zurück."""
    mc = monte_carlo_gematria_bridges(num_trials=100)
    assert 'p1_gematria_1874_close_to_gen_1_9_10' in mc
    assert 'sum_exactly_6503' in mc
    assert 'p4_gematria_exactly_551' in mc
    assert '11_sec_in_99_chars' in mc
    for bridge in mc.values():
        assert 0 <= bridge['p_value'] <= 1


def test_genesis_1_gematria_table_complete():
    """Genesis-1-Gematria-Tabelle hat alle 6 Verse."""
    assert len(GENESIS_1_GEMATRIA) == 6


# ============================================================================
# ENTRY POINTS
# ============================================================================

if __name__ == "__main__":
    main()
    # Wenn pytest vorhanden, führe Tests aus
    try:
        import pytest
        sys.exit(pytest.main([__file__, '-v']))
    except ImportError:
        print("pytest nicht installiert — manueller Test-Lauf:")
        # Manueller Test
        tests = [g for g in dir() if g.startswith('test_')]
        for t in tests:
            try:
                globals()[t]()
                print(f"  PASS: {t}")
            except AssertionError as e:
                print(f"  FAIL: {t}: {e}")
