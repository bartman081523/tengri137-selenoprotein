"""
Q16 (NEU, vereinfacht): BURUMUT vs zufaellige Sequenzen
"""
import random
import statistics
from collections import Counter

BURUMUT_FULL = (
    "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
    "UAZBEHIMLAZANRUAZBENOMBA"
    "MZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
)

BURUMUT_FREQ = Counter(BURUMUT_FULL)
BURUMUT_CHARS = list(BURUMUT_FREQ.keys())
BURUMUT_WEIGHTS = list(BURUMUT_FREQ.values())

def gen_random_protein(n=99, seed=None):
    if seed is not None:
        random.seed(seed)
    return ''.join(random.choices(BURUMUT_CHARS, weights=BURUMUT_WEIGHTS, k=n))

print("="*70)
print("Q16.1: BURUMUT vs 5000 zufaellige Sequenzen")
print("="*70)

metrics = {
    'hydrophob': lambda seq: sum(1 for c in seq if c in 'AIVLFM') / len(seq),
    'helix_chars': lambda seq: sum(1 for c in seq if c in 'ALMEQK') / len(seq),
    'sheet_chars': lambda seq: sum(1 for c in seq if c in 'VIYFWL') / len(seq),
    'turn_chars': lambda seq: sum(1 for c in seq if c in 'GNPSD') / len(seq),
    'pro_count': lambda seq: seq.count('P'),
    'sec_density': lambda seq: seq.count('U') / len(seq),
}

n_trials = 5000
for metric_name, metric_fn in metrics.items():
    burumut_val = metric_fn(BURUMUT_FULL)
    rand_vals = [metric_fn(gen_random_protein(len(BURUMUT_FULL), seed=i)) for i in range(n_trials)]
    mean = sum(rand_vals) / n_trials
    std = statistics.stdev(rand_vals) if n_trials > 1 else 0
    if std > 0:
        z = (burumut_val - mean) / std
    else:
        z = 0
    p_val = sum(1 for v in rand_vals if v >= burumut_val) / n_trials
    print(f"  {metric_name:13s}: BURUMUT={burumut_val:.4f} | mean={mean:.4f} (std={std:.4f}) | z={z:+.2f} | p={p_val:.4f}")
