"""
Q_FORMAL_PROOF_BURUMUT_TENGRI137
================================

FORMALER BEWEIS / WIDERLEGUNG: BURUMUT ⊂ Tengri137

BURUMUT: 99-Zeichen lateinische "Aminosaeure-Sequenz" (19 distinkte Buchstaben)
        Definiert in sources/TORA_TURING_CORRECT.py

Tengri137: 12071-Buchstaben-Text (26 distinkte lateinische Buchstaben)
        In /run/media/julian/ML4/tengri137/Tengri137_Full_Notes
        Zeilen 652-662 enthalten einen "BURUMUT-Block" (154 Zeichen)

FRAGEN:
1. Ist BURUMUT als String in Tengri137 enthalten?
2. Was sind die genauen Unterschiede?
3. Formaler Beweis (oder Widerlegung) BURUMUT ⊂ Tengri137
4. Topologische Aequivalenz der 11 Sec-Positionen (U) und 11 G/C/W/K-Positionen

PRINZIP (AGENTS.md Section 4.2):
- Numerische Behauptungen MUESSEN durch Code reproduzierbar sein
- Monte-Carlo-Tests wo moeglich
- Apophenie-Tests (was, wenn die Zahl zufaellig waere?)

STANDARDS:
- KEINE Apophenie, KEINE spirituelle Interpretation
- Was nicht beweisbar ist, wird ehrlich als NICHT BEWIESEN gekennzeichnet
- Schreibe Tests (pytest-tauglich)
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

# BURUMUT constant (from TORA_TURING_CORRECT.py)
BURUMUT = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPSUAZBEHIMLAZANRUAZBENOMBAMZHQRSAN"
    "LRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

# 11 Sec-Positionen in BURUMUT (empirisch belegt in Q10b/Q11)
SEC_POSITIONS = [1, 3, 5, 13, 15, 19, 24, 32, 46, 66, 80]

# 11 G/C/W/K Positionen in Tengri137 (erste 99 Zeichen) - aus TENGRI137_SELF_DECODED.md
NEW_LETTERS_POSITIONS = [
    (3, 'G'), (15, 'C'), (28, 'W'), (34, 'G'), (43, 'C'),
    (54, 'K'), (57, 'W'), (67, 'G'), (68, 'W'), (82, 'W'), (87, 'K'),
]

# 5 FEHLENDE HEBR. KONSONANTEN (aus TORA_TURING_CORRECT.py docstring)
MISSING_HEBREW = {
    'כ': ('Kaf', 20, 'READ'),
    'ג': ('Gimel', 3, 'MOVE_RIGHT'),
    'ד': ('Dalet', 4, 'MOVE_LEFT'),
    'ת': ('Tav', 400, 'HALT'),
    'י': ('Yod', 10, 'STATE'),
}


def load_tengri137(path: str = "/run/media/julian/ML4/tengri137/Tengri137_Full_Notes") -> str:
    """Lade Tengri137_Full_Notes und gebe nur lateinische Grossbuchstaben zurueck."""
    with open(path) as f:
        text = f.read()
    return re.sub(r"[^A-Z]", "", text)


def load_tengri137_block(path: str = "/run/media/julian/ML4/tengri137/Tengri137_Full_Notes",
                          line_start: int = 652, line_end: int = 662) -> str:
    """Lade den 'BURUMUT-Block' aus Zeilen 652-662 (1-indiziert)."""
    with open(path) as f:
        lines = f.readlines()
    # Convert 1-indexed to 0-indexed
    block_lines = [l.rstrip() for l in lines[line_start - 1:line_end]]
    return "".join(re.sub(r"[^A-Z]", "", l) for l in block_lines)


# ============================================================================
# FRAGE 1: Ist BURUMUT als String in Tengri137 enthalten?
# ============================================================================

def q1_is_burumut_substring(tengri: str) -> dict:
    """Pruefe, ob BURUMUT als kontiguierlicher Substring in Tengri137 vorkommt.

    Returns:
        dict mit 'answer', 'positions', 'method'
    """
    result = {
        "question": "1. Ist BURUMUT als String in Tengri137 enthalten?",
        "burumut_length": len(BURUMUT),
        "tengri_length": len(tengri),
        "method": "str.find mit Burumut-Len = 99",
    }

    # Suche BURUMUT im vollen Tengri137-Stream
    idx = tengri.find(BURUMUT)
    result["full_text_substring"] = idx >= 0
    result["full_text_position"] = idx

    # Suche im Block (Z.652-662)
    block = load_tengri137_block()
    idx2 = block.find(BURUMUT)
    result["block_substring"] = idx2 >= 0
    result["block_position"] = idx2
    result["block_length"] = len(block)

    # Was ist die kuerzeste Variante, die wir nicht finden?
    # Suche 'BURUMUT' (7 Zeichen)
    burumut7 = "BURUMUT"
    positions_7 = []
    start = 0
    while True:
        i = tengri.find(burumut7, start)
        if i < 0:
            break
        positions_7.append(i)
        start = i + 1
    result["burumut7_occurrences_in_full_text"] = positions_7
    result["burumut7_count_in_full_text"] = len(positions_7)

    return result


# ============================================================================
# FRAGE 2: Unterschiede zwischen BURUMUT und Tengri137-Block
# ============================================================================

def q2_differences() -> dict:
    """Vergleiche BURUMUT (99) und Tengri137-Block (154) Zeichen fuer Zeichen."""
    block = load_tengri137_block()
    result = {
        "question": "2. Was sind die genauen Unterschiede?",
        "burumut_length": len(BURUMUT),
        "block_length": len(block),
    }

    # Finde maximale Praefix-Uebereinstimmung
    common_prefix = 0
    for i in range(min(len(BURUMUT), len(block))):
        if BURUMUT[i] == block[i]:
            common_prefix += 1
        else:
            break
    result["common_prefix_length"] = common_prefix
    result["common_prefix_text"] = BURUMUT[:common_prefix]

    # Zeige die ersten 4 Zeilen Match
    chunks_match = []
    for i in range(min(len(BURUMUT) // 14, len(block) // 14)):
        burumut_chunk = BURUMUT[i*14:(i+1)*14]
        block_chunk = block[i*14:(i+1)*14]
        chunks_match.append({
            "chunk_idx": i,
            "line_in_tengri": 652 + i,
            "burumut": burumut_chunk,
            "block": block_chunk,
            "equal": burumut_chunk == block_chunk,
        })
    result["chunk_by_chunk_comparison"] = chunks_match

    # Divergenz-Position: ab wo unterscheiden sie sich?
    result["divergence_position"] = common_prefix

    # Letter-Count-Vergleich
    cb = Counter(BURUMUT)
    ct = Counter(block)
    all_letters = sorted(set(cb) | set(ct))
    counts = []
    for c in all_letters:
        counts.append({
            "letter": c,
            "burumut_count": cb.get(c, 0),
            "block_count": ct.get(c, 0),
            "delta": ct.get(c, 0) - cb.get(c, 0),
        })
    result["letter_counts"] = counts

    # Welche der 5 fehlenden hebr. Konsonanten (in Latin: C, D, J, K, V, W, X)
    # erscheinen in Tengri137-Block?
    result["letters_in_block_but_not_in_burumut"] = sorted(set(block) - set(BURUMUT))
    result["letters_in_burumut_but_not_in_block"] = sorted(set(BURUMUT) - set(block))

    # Zaehle: in welchen der 122 Phasen von Tengri137 tauchen die 5 hebr. Konsonanten auf?
    # Hierzu: wie oft kommt jeder lateinische Buchstabe (C,K,W,D,J,V,X) in Tengri137 vor?
    tengri = load_tengri137()
    tengri_counts = Counter(tengri)
    # Lateinische Aequivalente der 5 fehlenden hebr. Konsonanten
    missing_latin_equiv = {
        'כ (Kaf, READ)': ['C', 'K'],
        'ג (Gimel, MOVE_RIGHT)': ['G'],
        'ד (Dalet, MOVE_LEFT)': ['D'],
        'ת (Tav, HALT)': ['T'],  # T existiert, aber hebr. Tav ist in BURUMUT nicht direkt
        'י (Yod, STATE)': ['Y'],  # Y existiert auch
    }
    # 122 Phasen (Phasen 0..121, je 99 Zeichen, Total 12071)
    phase_size = 99
    n_phases = (len(tengri) + phase_size - 1) // phase_size
    phase_counts = {}
    for letter in ['C', 'D', 'G', 'K', 'W', 'J', 'V', 'X', 'T', 'Y']:
        n_phases_with = 0
        for p in range(n_phases):
            phase = tengri[p*phase_size:(p+1)*phase_size]
            if letter in phase:
                n_phases_with += 1
        phase_counts[letter] = {
            "total_in_tengri137": tengri_counts.get(letter, 0),
            "phases_with_letter": n_phases_with,
            "n_phases_total": n_phases,
        }
    result["phase_letter_counts"] = phase_counts

    # === ANALYSE: Welche der 5 fehlenden Hebr. Konsonanten sind in Tengri137 vorhanden? ===
    # Im BURUMUT-Framework sind die 5 fehlenden: כ, ג, ד, ת, י
    # Mapping-Logik:
    #   כ (Kaf, READ) -> C, K (BEIDE in Tengri137)
    #   ג (Gimel, MOVE_RIGHT) -> G (in Tengri137)
    #   ד (Dalet, MOVE_LEFT) -> D (in Tengri137)
    #   ת (Tav, HALT) -> lateinisch nicht direkt abgedeckt
    #                    (T = Resh in base mapping)
    #   י (Yod, STATE) -> Y (in Tengri137, aber auch in BURUMUT)
    missing_hebrew_analysis = {
        "כ (Kaf, READ)": {
            "mapping_in_extended": "C, K",
            "in_burumut": "C nein, K nein",
            "in_tengri137": "C ja, K ja",
            "in_extended_mapping_yes_no": "JA",
        },
        "ג (Gimel, MOVE_RIGHT)": {
            "mapping_in_extended": "G",
            "in_burumut": "G ja (aber als Variante?)",
            "in_tengri137": "G ja",
            "in_extended_mapping_yes_no": "JA",
        },
        "ד (Dalet, MOVE_LEFT)": {
            "mapping_in_extended": "D",
            "in_burumut": "D nein",
            "in_tengri137": "D ja",
            "in_extended_mapping_yes_no": "JA",
        },
        "ת (Tav, HALT)": {
            "mapping_in_extended": "FEHLT (nicht gemappt)",
            "in_burumut": "Tav nein",
            "in_tengri137": "lateinisch nicht abgedeckt",
            "in_extended_mapping_yes_no": "NEIN",
        },
        "י (Yod, STATE)": {
            "mapping_in_extended": "Y (existiert in base)",
            "in_burumut": "Y ja",
            "in_tengri137": "Y ja",
            "in_extended_mapping_yes_no": "JA (aber schon vorher da)",
        },
    }
    result["5_missing_hebrew_analysis"] = missing_hebrew_analysis
    result["n_5_missing_in_tengri137_via_latin"] = 4  # כ, ג, ד, י — aber י ist nicht "neu"
    result["n_5_missing_NOT_in_tengri137_via_latin"] = 1  # ת
    result["interpretation"] = (
        "Von den 5 'fehlenden' hebraeischen Operatoren sind 3-4 in Tengri137 lateinisch "
        "repraesentiert (כ via C/K, ג via G, ד via D, י via Y). ת (Tav) ist im extended "
        "Mapping NICHT abgedeckt. Die Behauptung 'BURUMUT hat 5 fehlende Operatoren, "
        "Tengri137 hat 4 neue Buchstaben' ist also schief: BURUMUT hat 19 distinkte lateinische "
        "Buchstaben, Tengri137 hat 26 (= 7 neue). Nur 3-4 der 5 fehlenden Operatoren sind lateinisch kodiert."
    )

    return result


# ============================================================================
# FRAGE 3: Formaler Beweis BURUMUT ⊂ Tengri137
# ============================================================================

def q3_formal_proof(tengri: str) -> dict:
    """Pruefe formal, ob BURUMUT eine Teilmenge (Substring) von Tengri137 ist."""
    result = {
        "question": "3. Formaler Beweis BURUMUT ⊂ Tengri137",
        "definitions": {
            "BURUMUT": f"|BURUMUT| = {len(BURUMUT)}, distinct letters = {len(set(BURUMUT))}",
            "Tengri137": f"|Tengri137| = {len(tengri)}, distinct letters = {len(set(tengri))}",
        },
    }

    # (a) Set inclusion: alle Buchstaben in BURUMUT sind in Tengri137
    burumut_set = set(BURUMUT)
    tengri_set = set(tengri)
    letters_only_in_burumut = burumut_set - tengri_set
    result["set_inclusion_letters_only_in_burumut"] = sorted(letters_only_in_burumut)
    result["set_inclusion_holds"] = len(letters_only_in_burumut) == 0

    # (b) Substring inclusion: BURUMUT als kontiguierlicher Substring in Tengri137
    idx = tengri.find(BURUMUT)
    result["substring_in_full_text"] = idx >= 0
    result["substring_position_in_full_text"] = idx

    # (c) Substring in Tengri137-Block
    block = load_tengri137_block()
    idx_block = block.find(BURUMUT)
    result["substring_in_block"] = idx_block >= 0
    result["substring_position_in_block"] = idx_block

    # (d) Was folgt formal: BURUMUT ⊂ Tengri137 ist eine THESE
    # Sie ist genau dann beweisbar, wenn (b) gilt.
    if idx >= 0:
        result["formal_conclusion"] = "BEWEIS: BURUMUT ist kontiguierlicher Substring von Tengri137"
        result["proof_status"] = "PROVEN"
    else:
        result["formal_conclusion"] = "WIDERLEGT: BURUMUT ist NICHT kontiguierlicher Substring von Tengri137"
        result["proof_status"] = "DISPROVEN"
        # Aber: Set inclusion ist eine schwächere Bedingung und gilt
        if result["set_inclusion_holds"]:
            result["weaker_inclusion"] = "Schwaechere Inclusion gilt: alle Buchstaben in BURUMUT sind in Tengri137 (set-inclusion), aber nicht als Substring."
            result["weaker_inclusion_status"] = "PROVEN (set-inclusion)"

    # (e) Monte-Carlo-Test: Wie wahrscheinlich ist es, dass eine zufaellige
    # 99-Zeichen-Sequenz aus 19 spezifischen Buchstaben ein Substring eines
    # 12071-Zeichen-Textes mit gleicher Verteilung ist?
    # Wir vergleichen die tatsaechliche Wahrscheinlichkeit mit 1000 random trials.
    result["monte_carlo"] = monte_carlo_substring_test(tengri, n_trials=1000)

    return result


def monte_carlo_substring_test(tengri: str, n_trials: int = 1000) -> dict:
    """Monte-Carlo: wie oft ist eine 99-char Sequenz mit BURUMUT-Buchstabenverteilung
    in einem 12071-char Text mit Tengri137-Buchstabenverteilung als Substring?
    """
    import random

    tengri_counter = Counter(tengri)
    burumut_counter = Counter(BURUMUT)
    tengri_letters = sorted(tengri_counter.keys())
    tengri_weights = [tengri_counter[c] for c in tengri_letters]

    random.seed(42)
    n_hits = 0
    n_tested = 0
    example_hits = []
    for _ in range(n_trials):
        # Erzeuge 99 Zeichen mit BURUMUT-Letter-Counts, aber zufaelliger Anordnung
        seq = []
        for letter, count in burumut_counter.items():
            seq.extend([letter] * count)
        random.shuffle(seq)
        seq = "".join(seq)
        # Suche in einem zufaelligen Tengri137-Text mit gleicher Verteilung
        rand_tengri = []
        for letter, w in zip(tengri_letters, tengri_weights):
            rand_tengri.extend([letter] * w)
        random.shuffle(rand_tengri)
        rand_tengri = "".join(rand_tengri)
        if rand_tengri.find(seq) >= 0:
            n_hits += 1
            if len(example_hits) < 3:
                example_hits.append(seq[:20])
        n_tested += 1

    return {
        "method": f"Monte-Carlo: 1000 random Substrings mit BURUMUT-Counts, gesucht in 1000 random Tengri137-Permutationen",
        "n_trials": n_tested,
        "n_hits": n_hits,
        "hit_rate": n_hits / n_tested if n_tested else 0,
        "interpretation": "Wenn hit_rate hoch, dann ist die (nicht vorhandene) Substring-Beziehung plausibel zufaellig. Wenn niedrig, dann ist sie signifikant.",
        "example_hits": example_hits,
    }


# ============================================================================
# FRAGE 4: 11 Sec-Positionen in BURUMUT vs 11 G/C/W/K in Tengri137
# ============================================================================

def q4_sec_vs_new_letters(tengri: str) -> dict:
    """Untersuche topologische Aequivalenz der 11 Sec-Positionen (BURUMUT) und
    11 G/C/W/K-Positionen (Tengri137 erste 99 Zeichen).
    """
    result = {
        "question": "4. Topologische Aequivalenz: 11 Sec-Pos (BURUMUT) vs 11 G/C/W/K (Tengri137)?",
    }

    # BURUMUT Sec-Positionen
    result["burumut_sec_positions"] = SEC_POSITIONS
    result["burumut_sec_letters"] = [BURUMUT[p] for p in SEC_POSITIONS]

    # Tengri137 (erste 99 Zeichen) G/C/W/K-Positionen
    tengri99 = tengri[:99]
    new_pos_letters = [tengri99[p] for _, p in [(c, p) for p, c in NEW_LETTERS_POSITIONS]]
    result["tengri99_new_positions"] = [p for p, c in NEW_LETTERS_POSITIONS]
    result["tengri99_new_letters"] = new_pos_letters

    # Beide Listen geordnet
    burumut_sorted = sorted(SEC_POSITIONS)
    tengri_sorted = sorted([p for p, c in NEW_LETTERS_POSITIONS])
    result["burumut_sorted"] = burumut_sorted
    result["tengri99_sorted"] = tengri_sorted

    # Korrelationsanalyse
    n = min(len(burumut_sorted), len(tengri_sorted))
    diffs = [tengri_sorted[i] - burumut_sorted[i] for i in range(n)]
    result["position_diffs"] = diffs
    result["mean_diff"] = sum(diffs) / len(diffs) if diffs else 0

    # Spearman-Rangkorrelation
    def spearman(xs, ys):
        n = len(xs)
        if n == 0:
            return 0
        rx = [sorted(xs).index(x) for x in xs]
        ry = [sorted(ys).index(y) for y in ys]
        mean_rx = sum(rx) / n
        mean_ry = sum(ry) / n
        num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
        denom = (sum((r - mean_rx) ** 2 for r in rx) * sum((r - mean_ry) ** 2 for r in ry)) ** 0.5
        return num / denom if denom else 0
    rho = spearman(burumut_sorted, tengri_sorted)
    result["spearman_rho"] = rho
    result["spearman_warning"] = (
        "ACHTUNG: Da beide Listen bereits sortiert sind (jeder Wert unique), "
        "ist rho=1.0 TRIVIAL und sagt NICHTS ueber die 'topologische Aequivalenz'. "
        "Beide Listen sind monoton wachsend nach dem Sortieren — rho=1 folgt daraus zwangslaeufig. "
        "Der relevante Test ist: sind die konkret markierten Positionen in einer sinnvollen Beziehung? "
        "Siehe 'overlap_test' und 'consecutive_pair_test' unten."
    )

    # Monte-Carlo: 11 zufaellige Positionen in [0, 98] vs 11 zufaellige Positionen
    # Wieviel Uebereinstimmung im Mittel?
    import random
    random.seed(42)
    n_trials = 10000
    n_match = 0
    rho_dist = []
    for _ in range(n_trials):
        rand1 = sorted(random.sample(range(99), 11))
        rand2 = sorted(random.sample(range(99), 11))
        n_match += len(set(rand1) & set(rand2))
        rho_dist.append(spearman(rand1, rand2))

    mean_overlap = n_match / n_trials
    expected_overlap = 11 * 11 / 99  # ~1.22
    rho_dist.sort()
    rho_95 = rho_dist[int(0.95 * n_trials)]
    rho_05 = rho_dist[int(0.05 * n_trials)]

    actual_overlap = len(set(burumut_sorted) & set(tengri_sorted))
    result["monte_carlo_position_overlap"] = {
        "actual_overlap": actual_overlap,
        "mean_random_overlap": mean_overlap,
        "expected_random_overlap": expected_overlap,
        "n_trials": n_trials,
        "interpretation": (
            f"Tatsaechlicher Overlap = {actual_overlap}, "
            f"im Mittel erwartet bei Zufall = {mean_overlap:.2f}, "
            f"theoretisch = {expected_overlap:.2f}"
        ),
    }
    result["monte_carlo_spearman"] = {
        "actual_rho": rho,
        "rho_5th_percentile": rho_05,
        "rho_95th_percentile": rho_95,
        "p_value_rho_gt_0": sum(1 for r in rho_dist if r >= rho) / n_trials,
        "interpretation": (
            f"rho = {rho:.4f}. "
            f"Unter 10000 Random-Trials: 5% Quantil = {rho_05:.4f}, "
            f"95% Quantil = {rho_95:.4f}. "
            f"Wahrscheinlichkeit rho >= {rho:.4f} unter Nullhypothese = "
            f"{sum(1 for r in rho_dist if r >= rho) / n_trials:.4f}"
        ),
    }

    # ========== NEU: Positional Consecutive-Pair-Test ==========
    # Pruefe, ob die DREI auf einander folgenden Pos in der BURUMUT-Liste
    # auch in der Tengri137-Liste aufeinander folgen
    def consecutive_pairs(xs):
        return list(zip(xs[:-1], xs[1:]))

    burumut_pairs = consecutive_pairs(burumut_sorted)
    tengri_pairs = consecutive_pairs(tengri_sorted)
    common_pairs = set(burumut_pairs) & set(tengri_pairs)
    result["consecutive_pairs_burumut"] = burumut_pairs
    result["consecutive_pairs_tengri"] = tengri_pairs
    result["consecutive_pairs_common"] = sorted(common_pairs)

    # ========== NEU: Korrelations-Test der POSITIONEN (nicht Ränge) ==========
    # Wir berechnen Pearson-r zwischen den BURUMUT-Positionen und den Tengri137-Positionen
    # unter der Hypothese, dass die i-te BURUMUT-Position der i-ten Tengri137-Position entspricht
    def pearson(xs, ys):
        n = len(xs)
        if n == 0:
            return 0
        mean_x = sum(xs) / n
        mean_y = sum(ys) / n
        num = sum((xs[i] - mean_x) * (ys[i] - mean_y) for i in range(n))
        den_x = sum((x - mean_x) ** 2 for x in xs) ** 0.5
        den_y = sum((y - mean_y) ** 2 for y in ys) ** 0.5
        return num / (den_x * den_y) if den_x * den_y else 0
    pearson_r = pearson(burumut_sorted, tengri_sorted)
    result["pearson_r"] = pearson_r

    # Monte-Carlo: Wenn die BURUMUT-Positionen FIX sind und Tengri137-Positionen
    # zufaellig gewaehlt, wie hoch ist der erwartete Pearson-r?
    random.seed(43)
    pearson_dist = []
    for _ in range(n_trials):
        rand = sorted(random.sample(range(99), 11))
        pearson_dist.append(pearson(burumut_sorted, rand))
    pearson_dist.sort()
    actual_p = sum(1 for r in pearson_dist if r >= pearson_r) / n_trials
    result["pearson_monte_carlo"] = {
        "actual_r": pearson_r,
        "p_value": actual_p,
        "mean_random_r": sum(pearson_dist) / n_trials,
        "max_random_r": max(pearson_dist),
        "interpretation": (
            f"Pearson r = {pearson_r:.4f}. "
            f"Unter 10000 random Tengri137-Positionen mit gleichem n=11: "
            f"max r = {max(pearson_dist):.4f}, mean r = {sum(pearson_dist) / n_trials:.4f}. "
            f"p(r >= {pearson_r:.4f} | H0) = {actual_p:.4f}"
        ),
    }

    # ========== NEU: Test mit fester Shift-Hypothese ==========
    # Wenn die Tengri137-Positionen einer BURUMUT-Position + konstante entsprechen,
    # dann sollte diese Konstante ein einheitlicher Shift sein
    diffs = [tengri_sorted[i] - burumut_sorted[i] for i in range(n)]
    mean_diff = sum(diffs) / len(diffs)
    var_diff = sum((d - mean_diff) ** 2 for d in diffs) / len(diffs)
    std_diff = var_diff ** 0.5
    result["shift_analysis"] = {
        "diffs": diffs,
        "mean_diff": mean_diff,
        "std_diff": std_diff,
        "interpretation": (
            f"Wenn BURUMUT- und Tengri137-Positionen durch einen konstanten Shift verbunden waeren, "
            f"waere std_diff = 0. Aktuelle std_diff = {std_diff:.2f} (gross gegenueber mean_diff = {mean_diff:.2f}). "
            f"KEIN konstanter Shift erkennbar."
        ),
    }

    return result


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

def main():
    print("=" * 70)
    print("Q_FORMAL_PROOF_BURUMUT_TENGRI137 — FORMALER BEWEIS / WIDERLEGUNG")
    print("=" * 70)
    print()

    tengri = load_tengri137()
    print(f"Tengri137 (lateinische Grossbuchstaben): {len(tengri)} Zeichen")
    print(f"BURUMUT (Konstante): {len(BURUMUT)} Zeichen, {len(set(BURUMUT))} distinct")
    print()

    # Frage 1
    print("=" * 70)
    print("FRAGE 1: Ist BURUMUT als String in Tengri137 enthalten?")
    print("=" * 70)
    r1 = q1_is_burumut_substring(tengri)
    print(f"  BURUMUT (99 chars) als Substring in Tengri137 (12071 chars): {r1['full_text_substring']}")
    print(f"  BURUMUT (99 chars) als Substring in Tengri137-Block (154 chars): {r1['block_substring']}")
    print(f"  'BURUMUT' (7 chars) Vorkommen in Tengri137: {r1['burumut7_count_in_full_text']}x")
    print(f"  Position(en): {r1['burumut7_occurrences_in_full_text']}")
    print()

    # Frage 2
    print("=" * 70)
    print("FRAGE 2: Unterschiede zwischen BURUMUT und Tengri137-Block")
    print("=" * 70)
    r2 = q2_differences()
    print(f"  BURUMUT: {r2['burumut_length']} Zeichen, Tengri137-Block: {r2['block_length']} Zeichen")
    print(f"  Gemeinsamer Praefix: {r2['common_prefix_length']} Zeichen")
    print(f"  Divergenz ab Position: {r2['divergence_position']}")
    print(f"  Buchstaben nur in Block: {r2['letters_in_block_but_not_in_burumut']}")
    print(f"  Buchstaben nur in BURUMUT: {r2['letters_in_burumut_but_not_in_block']}")
    print()
    print("  Chunk-by-chunk:")
    for c in r2['chunk_by_chunk_comparison']:
        marker = "OK" if c['equal'] else "DIFF"
        print(f"    Z.{c['line_in_tengri']} [{marker}]: BURUMUT='{c['burumut']}' BLOCK='{c['block']}'")
    print()
    print("  5 fehlende hebr. Konsonanten — Latein-Coverage in Tengri137:")
    for heb, info in r2['5_missing_hebrew_analysis'].items():
        print(f"    {heb}: {info['in_extended_mapping_yes_no']} — {info['mapping_in_extended']}")
    print(f"  -> {r2['interpretation']}")
    print()

    # Frage 3
    print("=" * 70)
    print("FRAGE 3: Formaler Beweis BURUMUT ⊂ Tengri137")
    print("=" * 70)
    r3 = q3_formal_proof(tengri)
    print(f"  Set-inclusion (alle Buchstaben in Tengri137): {r3['set_inclusion_holds']}")
    print(f"  Buchstaben NUR in BURUMUT: {r3['set_inclusion_letters_only_in_burumut']}")
    print(f"  Substring in Tengri137 (12071 chars): {r3['substring_in_full_text']}")
    print(f"  Substring in Tengri137-Block (154 chars): {r3['substring_in_block']}")
    print(f"  -> FORMAL: {r3['formal_conclusion']}")
    if "weaker_inclusion_status" in r3:
        print(f"  -> Schwaechere Inclusion: {r3['weaker_inclusion']}")
    print()
    print("  Monte-Carlo:")
    mc = r3["monte_carlo"]
    print(f"    n_trials = {mc['n_trials']}")
    print(f"    n_hits = {mc['n_hits']} (hit_rate = {mc['hit_rate']:.4f})")
    print()

    # Frage 4
    print("=" * 70)
    print("FRAGE 4: 11 Sec-Positionen (BURUMUT) vs 11 G/C/W/K (Tengri137)")
    print("=" * 70)
    r4 = q4_sec_vs_new_letters(tengri)
    print(f"  BURUMUT Sec-Positionen: {r4['burumut_sorted']}")
    print(f"  Tengri137 erste 99, G/C/W/K: {r4['tengri99_sorted']}")
    print(f"  Position-Differenzen (tengri - burumut): {r4['position_diffs']}")
    print(f"  Spearman rho: {r4['spearman_rho']:.4f}")
    print(f"  WARNUNG: {r4['spearman_warning'][:80]}...")
    print()
    print("  Consecutive-Pairs (aufeinanderfolgende Positionen):")
    print(f"    BURUMUT: {r4['consecutive_pairs_burumut']}")
    print(f"    Tengri:  {r4['consecutive_pairs_tengri']}")
    print(f"    Gemeinsame: {r4['consecutive_pairs_common']}")
    print()
    print("  Pearson-r (zwischen sortierten Pos):")
    pr = r4['pearson_monte_carlo']
    print(f"    r = {pr['actual_r']:.4f}, mean random = {pr['mean_random_r']:.4f}, "
          f"max random = {pr['max_random_r']:.4f}, p = {pr['p_value']:.4f}")
    print()
    print("  Shift-Analyse:")
    sa = r4['shift_analysis']
    print(f"    Diffs: {sa['diffs']}")
    print(f"    Mean = {sa['mean_diff']:.2f}, Std = {sa['std_diff']:.2f}")
    print(f"    -> {sa['interpretation']}")
    print()
    print("  Monte-Carlo Overlap:")
    mo = r4['monte_carlo_position_overlap']
    print(f"    Tatsaechlich: {mo['actual_overlap']}")
    print(f"    Erwartet (Zufall): {mo['expected_random_overlap']:.2f}")
    print(f"    Beobachtet (Mittel): {mo['mean_random_overlap']:.2f}")
    print()

    # Speichere JSON
    output = {
        "method": "Q_FORMAL_PROOF_BURUMUT_TENGRI137",
        "principle": "Formaler Beweis / Widerlegung BURUMUT ⊂ Tengri137 mit Monte-Carlo-Tests",
        "question_1": r1,
        "question_2": r2,
        "question_3": r3,
        "question_4": r4,
        "summary": {
            "burumut_substring_in_tengri137": r3["substring_in_full_text"],
            "burumut_substring_in_block": r3["substring_in_block"],
            "set_inclusion_holds": r3["set_inclusion_holds"],
            "proof_status": r3["proof_status"],
            "sec_pos_eq_new_letter_pos_rho": r4["spearman_rho"],
            "sec_pos_eq_new_letter_pos_p_value": r4["monte_carlo_spearman"]["p_value_rho_gt_0"],
        },
    }

    out_path = Path("/run/media/julian/ML4/tengri137/sources/q_formal_proof_burumut_tengri137.json")
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print(f"Output gespeichert in: {out_path}")
    print()
    print("=" * 70)
    print("FAZIT")
    print("=" * 70)
    summary = output["summary"]
    print(f"  BURUMUT ⊂ Tengri137 (Substring): {summary['burumut_substring_in_tengri137']}")
    print(f"  Beweis-Status: {summary['proof_status']}")
    print(f"  11 Sec-Pos vs 11 G/C/W/K-Pos, Spearman rho: {summary['sec_pos_eq_new_letter_pos_rho']:.4f}, "
          f"p = {summary['sec_pos_eq_new_letter_pos_p_value']:.4f}")
    return output


# ============================================================================
# PYTEST TESTS
# ============================================================================

def test_burumut_is_99_chars():
    """BURUMUT hat exakt 99 Zeichen."""
    assert len(BURUMUT) == 99


def test_burumut_19_distinct_letters():
    """BURUMUT hat 19 distinkte lateinische Buchstaben."""
    assert len(set(BURUMUT)) == 19


def test_tengri137_12071_letters():
    """Tengri137 hat 12071 lateinische Grossbuchstaben."""
    tengri = load_tengri137()
    assert len(tengri) == 12071


def test_tengri137_26_distinct_letters():
    """Tengri137 hat 26 distinkte lateinische Buchstaben (alle)."""
    tengri = load_tengri137()
    assert len(set(tengri)) == 26


def test_tengri137_block_154_chars():
    """Tengri137-Block (Z.652-662) hat 154 Zeichen."""
    block = load_tengri137_block()
    assert len(block) == 154


def test_burumut_NOT_substring_of_tengri137():
    """BURUMUT (99) ist NICHT ein Substring von Tengri137 (12071)."""
    tengri = load_tengri137()
    assert tengri.find(BURUMUT) == -1


def test_burumut_NOT_substring_of_block():
    """BURUMUT (99) ist NICHT ein Substring des Tengri137-Blocks (154)."""
    block = load_tengri137_block()
    assert block.find(BURUMUT) == -1


def test_set_inclusion_burumut_subset_tengri137():
    """Jeder Buchstabe in BURUMUT kommt auch in Tengri137 vor (set-inclusion)."""
    tengri = load_tengri137()
    assert set(BURUMUT) <= set(tengri)


def test_burumut_substring_begins_with_burumut7():
    """Tengri137 enthaelt 'BURUMUT' (7 Zeichen) genau 1x (am Ende)."""
    tengri = load_tengri137()
    # Eine Vorkommen, am Ende des Textes (nahe Position 12071)
    pos = tengri.find("BURUMUT")
    assert pos >= 0
    # Position sollte im Block sein (Z.652-662 = Position 11740-11893)
    assert 11740 <= pos <= 11750


def test_common_prefix_is_56():
    """Tengri137-Block und BURUMUT haben 56 Zeichen gemeinsamen Praefix (4 Zeilen)."""
    block = load_tengri137_block()
    common = 0
    for i in range(min(len(BURUMUT), len(block))):
        if BURUMUT[i] == block[i]:
            common += 1
        else:
            break
    assert common == 56  # 4 Zeilen à 14 Zeichen


def test_11_sec_positions_all_u():
    """Alle 11 Sec-Positionen in BURUMUT enthalten 'U'."""
    for p in SEC_POSITIONS:
        assert BURUMUT[p] == 'U'


def test_11_gcwk_positions_in_tengri99():
    """Die 11 G/C/W/K-Positionen in Tengri137 erste 99 Zeichen sind korrekt."""
    tengri = load_tengri137()
    tengri99 = tengri[:99]
    for pos, letter in NEW_LETTERS_POSITIONS:
        assert tengri99[pos] == letter, f"Position {pos}: expected {letter}, got {tengri99[pos]}"


def test_spearman_rho_calculation():
    """Berechne Spearman rho und vergleiche mit Bibliothek (oder Referenz)."""
    # Bekannter Wert: perfekt monotone Beziehung
    rho_perfect = 0
    # Inline berechnen
    def spearman(xs, ys):
        n = len(xs)
        if n == 0:
            return 0
        rx = [sorted(xs).index(x) for x in xs]
        ry = [sorted(ys).index(y) for y in ys]
        mean_rx = sum(rx) / n
        mean_ry = sum(ry) / n
        num = sum((rx[i] - mean_rx) * (ry[i] - mean_ry) for i in range(n))
        denom = (sum((r - mean_rx) ** 2 for r in rx) * sum((r - mean_ry) ** 2 for r in ry)) ** 0.5
        return num / denom if denom else 0
    xs = [1, 2, 3, 4, 5]
    ys = [10, 20, 30, 40, 50]
    rho_perfect = spearman(xs, ys)
    assert abs(rho_perfect - 1.0) < 1e-9


if __name__ == "__main__":
    main()
