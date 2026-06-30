#!/usr/bin/env python3
"""
uni_13732.py: LOOK-ELSEWHERE TEST FOR mu = 178 + 610*e
Experiment ID: uni-13732

HYPOTHESIS:
    Proton/electron mass ratio mu = 178 + 610*e
    where 610 = F_15 (15th Fibonacci number)
    and   178 = 2 * F_11 = 2 * 89

    Claimed precision: ~0.4 PPM

ANTITHESIS (Steelman):
    The formula A + B*e with A,B integers has two free parameters.
    Given the density of integers near mu ~ 1836, it is statistically
    inevitable that some (A,B) pair lands within 0.4 PPM.
    The Fibonacci label is applied post-hoc after finding the match.

METHOD (identical to uni_13700b/13744):

    PART 1 — CANDIDATE SPACE:
    Test ALL formulas of the form A + B*e where:
      A in [0..2000], B in [0..1000]
    This is the honest search space — every formula of equal or lesser
    complexity to (178, 610).
    Count how many hit within 0.4 PPM of mu_real.

    PART 2 — FIBONACCI SPECIALNESS:
    Is 610 special AS a Fibonacci number, or just as an integer?
    Test: restrict to A + B*e where B is a Fibonacci number.
    How many Fibonacci-B candidates hit within 0.4 PPM?

    PART 3 — MONTE CARLO p-VALUE:
    Draw 100,000 random targets from [1800, 1900] (plausible mu range).
    For each, find best-fitting A + B*e with A in [0..2000], B in [0..1000].
    p-value = fraction of random targets hit within 0.4 PPM.

    PART 4 — FIBONACCI p-VALUE:
    Same Monte Carlo but restricted to Fibonacci B values.

VERDICT (pre-registered):
    p < 0.001 AND only 1 candidate in full space -> STRONG
    p < 0.01  AND few candidates                 -> MODERATE
    p >= 0.05 OR many candidates                 -> WEAK / curve-fitting
"""

import numpy as np
from scipy.constants import proton_mass, electron_mass, e as E_const
import math

E        = math.e
MU_REAL  = proton_mass / electron_mass   # 1836.15267343...
THRESHOLD_PPM = 0.4
N_MC     = 100_000
TARGET_RANGE = (1800.0, 1900.0)

np.random.seed(42)

# Fibonacci numbers up to 2000
def fibonacci_up_to(n):
    fibs = [1, 1]
    while True:
        next_f = fibs[-1] + fibs[-2]
        if next_f > n:
            break
        fibs.append(next_f)
    return set(fibs)

FIBS = fibonacci_up_to(2000)

print("=" * 72)
print("EXPERIMENT UNI-13732: LOOK-ELSEWHERE TEST FOR mu = 178 + 610*e")
print("=" * 72)

formula_val = 178 + 610 * E
formula_ppm = abs(formula_val - MU_REAL) / MU_REAL * 1e6

print(f"\n[CONSTANTS]")
print(f"  mu_real          = {MU_REAL:.10f}")
print(f"  e (Euler)        = {E:.10f}")
print(f"  178 + 610*e      = {formula_val:.10f}")
print(f"  Formula error    = {formula_ppm:.4f} PPM")
print(f"  610 is Fibonacci : {610 in FIBS}")
print(f"  178 = 2*89       : {178 == 2*89}, 89 is Fibonacci: {89 in FIBS}")

# ── PART 1: Full candidate space ──────────────────────────────────────────────
print(f"\n{'─'*72}")
print("PART 1: FULL CANDIDATE SPACE  A + B*e,  A in [0..2000], B in [0..1000]")
print(f"{'─'*72}")

A_MAX = 2000
B_MAX = 1000

# Vectorized search
A_vals = np.arange(0, A_MAX + 1, dtype=float)
B_vals = np.arange(0, B_MAX + 1, dtype=float)

hits_full = []
best_ppm_full = float('inf')
best_formula = None

for B in range(B_MAX + 1):
    vals = A_vals + B * E
    ppms = np.abs(vals - MU_REAL) / MU_REAL * 1e6
    mask = ppms <= THRESHOLD_PPM
    for A in A_vals[mask]:
        ppm = abs((A + B*E) - MU_REAL) / MU_REAL * 1e6
        hits_full.append((int(A), B, ppm))
        if ppm < best_ppm_full:
            best_ppm_full = ppm
            best_formula = (int(A), B)

total_candidates = (A_MAX + 1) * (B_MAX + 1)
print(f"  Total candidates searched : {total_candidates:,}")
print(f"  Hits within {THRESHOLD_PPM} PPM        : {len(hits_full)}")
print(f"  Best match                : A={best_formula[0]}, B={best_formula[1]}")
print(f"  Best match value          : {best_formula[0] + best_formula[1]*E:.8f}")
print(f"  Best match error          : {best_ppm_full:.4f} PPM")

if len(hits_full) <= 20:
    print(f"\n  All hits:")
    for A, B, ppm in sorted(hits_full, key=lambda x: x[2]):
        fib_a = A in FIBS
        fib_b = B in FIBS
        print(f"    {A} + {B}*e  =  {A+B*E:.8f}  ({ppm:.4f} PPM)"
              f"  [A Fib:{fib_a}, B Fib:{fib_b}]")
else:
    print(f"\n  Top 10 hits:")
    for A, B, ppm in sorted(hits_full, key=lambda x: x[2])[:10]:
        fib_b = B in FIBS
        print(f"    {A} + {B}*e  ({ppm:.4f} PPM)  [B Fibonacci: {fib_b}]")

# ── PART 2: Fibonacci-restricted space ───────────────────────────────────────
print(f"\n{'─'*72}")
print("PART 2: FIBONACCI-RESTRICTED  A + F*e  where F is a Fibonacci number")
print(f"{'─'*72}")

fib_list = sorted(FIBS)
hits_fib = []
for F in fib_list:
    for A in range(A_MAX + 1):
        val = A + F * E
        ppm = abs(val - MU_REAL) / MU_REAL * 1e6
        if ppm <= THRESHOLD_PPM:
            hits_fib.append((A, F, ppm))

fib_candidates = len(fib_list) * (A_MAX + 1)
print(f"  Fibonacci numbers up to {B_MAX}  : {len(fib_list)}  {sorted(FIBS)[:15]}...")
print(f"  Total Fibonacci candidates    : {fib_candidates:,}")
print(f"  Hits within {THRESHOLD_PPM} PPM           : {len(hits_fib)}")
if hits_fib:
    for A, F, ppm in sorted(hits_fib, key=lambda x: x[2]):
        print(f"    {A} + {F}*e  ({ppm:.4f} PPM)")

# ── PART 3: Monte Carlo p-value (full space) ──────────────────────────────────
print(f"\n{'─'*72}")
print(f"PART 3: MONTE CARLO p-VALUE  ({N_MC:,} random targets from {TARGET_RANGE})")
print(f"{'─'*72}")

# Precompute B*e values
Be_vals = np.array([B * E for B in range(B_MAX + 1)])

random_targets = np.random.uniform(TARGET_RANGE[0], TARGET_RANGE[1], N_MC)
hits_mc = 0

for target in random_targets:
    # For each B, best A is round(target - B*e)
    A_best = np.round(target - Be_vals).clip(0, A_MAX)
    vals = A_best + Be_vals
    ppms = np.abs(vals - target) / target * 1e6
    if np.min(ppms) <= THRESHOLD_PPM:
        hits_mc += 1

p_value_full = hits_mc / N_MC

print(f"  Random targets hitting <= {THRESHOLD_PPM} PPM : {hits_mc}/{N_MC}")
print(f"  p-value (full space)             : {p_value_full:.4f}")

# ── PART 4: Monte Carlo p-value (Fibonacci B only) ────────────────────────────
print(f"\n{'─'*72}")
print(f"PART 4: MONTE CARLO p-VALUE — FIBONACCI B ONLY")
print(f"{'─'*72}")

FBe_vals = np.array([F * E for F in fib_list])
hits_mc_fib = 0

for target in random_targets:
    A_best = np.round(target - FBe_vals).clip(0, A_MAX)
    vals = A_best + FBe_vals
    ppms = np.abs(vals - target) / target * 1e6
    if np.min(ppms) <= THRESHOLD_PPM:
        hits_mc_fib += 1

p_value_fib = hits_mc_fib / N_MC

print(f"  Random targets hitting <= {THRESHOLD_PPM} PPM : {hits_mc_fib}/{N_MC}")
print(f"  p-value (Fibonacci B only)       : {p_value_fib:.4f}")

# ── PART 5: Is 610 special? ───────────────────────────────────────────────────
print(f"\n{'─'*72}")
print("PART 5: IS B=610 SPECIAL AMONG ALL B IN [0..1000]?")
print(f"{'─'*72}")

# For each B, find best A and compute PPM
best_per_B = []
for B in range(B_MAX + 1):
    A_opt = round(MU_REAL - B * E)
    if 0 <= A_opt <= A_MAX:
        val = A_opt + B * E
        ppm = abs(val - MU_REAL) / MU_REAL * 1e6
        best_per_B.append((ppm, A_opt, B))

best_per_B.sort()
rank_610 = next((i+1 for i, (_, _, B) in enumerate(best_per_B) if B == 610), None)

print(f"  Rank of B=610 among all B in [0..1000] by PPM precision: #{rank_610}")
print(f"  Top 10 B values by precision:")
for i, (ppm, A, B) in enumerate(best_per_B[:10]):
    fib = "← Fibonacci" if B in FIBS else ""
    print(f"    #{i+1}: B={B:4d}, A={A:4d},  {A}+{B}*e = {ppm:.4f} PPM  {fib}")

# ── VERDICT ───────────────────────────────────────────────────────────────────
print(f"\n{'='*72}")
print("VERDICT")
print(f"{'='*72}")

print(f"""
  Hypothesis: mu = 178 + 610*e  (claimed: 0.4 PPM, Fibonacci structure)
  Actual error: {formula_ppm:.4f} PPM

  PART 1 — Full space hits within {THRESHOLD_PPM} PPM : {len(hits_full)}
  PART 2 — Fibonacci-B hits within {THRESHOLD_PPM} PPM: {len(hits_fib)}
  PART 3 — p-value (full A+B*e space)  : {p_value_full:.4f}
  PART 4 — p-value (Fibonacci B only)  : {p_value_fib:.4f}
  PART 5 — Rank of B=610               : #{rank_610} of {B_MAX+1}
""")

if p_value_full >= 0.05:
    grade = "C — WEAK"
    conclusion = (f"p={p_value_full:.4f}. The form A+B*e with integer A,B "
                  f"saturates the target range. {len(hits_full)} candidates hit "
                  f"within {THRESHOLD_PPM} PPM. This is curve-fitting.")
elif p_value_full >= 0.01:
    grade = "B — MARGINAL"
    conclusion = f"p={p_value_full:.4f}. Borderline. LEE cannot be excluded."
else:
    if len(hits_full) == 1:
        grade = "A — STRONG (but see caveats)"
        conclusion = (f"p={p_value_full:.4f}. Only 1 candidate hits. "
                      f"Statistically unusual. Fibonacci label still needs "
                      f"independent justification.")
    else:
        grade = "B — MODERATE"
        conclusion = (f"p={p_value_full:.4f} but {len(hits_full)} candidates hit. "
                      f"Not uniquely Fibonacci.")

print(f"  Grade     : {grade}")
print(f"  Conclusion: {conclusion}")
print(f"""
  NOTE ON FIBONACCI LABELING:
  The Fibonacci property of 610 is only meaningful if:
  (a) The formula was predicted to involve Fibonacci numbers BEFORE
      searching, not after finding 610 and then noting it is F_15.
  (b) Fibonacci-B formulas are significantly rarer than arbitrary-B.
  The p-value comparison between Part 3 and Part 4 tests this directly.
""")
print("=" * 72)
