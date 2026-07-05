"""
phase13_search_fractions.py
V7 Phase 4e — Suche den Bruch, dessen Periode Jims 96-Ziffern-Folge ergibt

Jim's Periode: 632363457043807793324372132263547716431677165613166310576111312132280631213437717135722379222722
"""
import sys
sys.setrecursionlimit(100000)

JIM = "632363457043807793324372132263547716431677165613166310576111312132280631213437717135722379222722"
JIM_LEN = len(JIM)
print(f"Jim Periode: {JIM_LEN} Ziffern")

# 1/n Periodenlänge: ord_n(10)
# Wir suchen n mit Periode genau JIM_LEN
# n muss teilerfremd zu 10 sein (sonst endet der Bruch)
# Mögliche Kandidaten

def find_period(num, den, max_digits=300):
    seen = {}
    digits = []
    rem = num % den
    while rem != 0 and rem not in seen and len(digits) < max_digits:
        seen[rem] = len(digits)
        rem *= 10
        d = rem // den
        rem = rem % den
        digits.append(d)
    if rem in seen:
        return ''.join(str(x) for x in digits[seen[rem]:])
    return None

# Suche 1/n mit Periode 96
print("\nSuche 1/n mit Periode 96...")
found = []
for n in range(7, 100000):
    if n % 2 == 0 or n % 5 == 0:
        continue
    p = find_period(1, n)
    if p and len(p) == 96:
        # Prüfe Übereinstimmung
        match = p == JIM
        if match:
            print(f"  EXAKT: 1/{n}")
            found.append((1, n, p, "EXACT"))
        else:
            # Nur erste 30 Ziffern prüfen
            if p[:30] == JIM[:30]:
                print(f"  PARTIAL: 1/{n}: {p[:60]}")
                found.append((1, n, p, "PARTIAL"))

# Auch a/n für kleine a
print("\nSuche a/n (a=2,3,5,7) mit Periode 96...")
for a in [2, 3, 5, 7, 11, 13]:
    for n in range(7, 100000):
        if n % 2 == 0 or n % 5 == 0:
            continue
        p = find_period(a, n)
        if p and len(p) == 96 and p == JIM:
            print(f"  EXAKT: {a}/{n}")
            found.append((a, n, p, "EXACT"))

if not found:
    print("Keine einfache 1/n oder a/n gefunden.")
    print("Möglicherweise ist der Bruch komplexer (z.B. 1/(p*q) oder p1*...*pn / q1*...*qm)")
