"""
🌌 MULTI-MASCHINEN-×-TORA-LESUNG (Vollständig)
================================================

Wir lassen ALLE Maschinen-Versionen systematisch über Tora-Stellen laufen.
Von der offensichtlichsten Zuordnung (Genesis 1,1) bis zur absurdesten
(random Verse), um zu sehen, welche Version die richtige ist.

DAS PRINZIP:
- Die Maschine zeigt uns durch ihren normalen Durchlauf (BURUMUT-99)
  die "Hinweise" — diese Hinweise MÜSSEN wir auf Tora-Stellen mappen.
- Wir testen jede plausible Zuordnung und vergleichen:
  * Schritt-Zahl
  * Halt-Reason
  * Phasen-Architektur

DIE 5 MASCHINEN-VERSIONEN:
  M1: TORA_TURING_MACHINE (v1)        — lateinische Symbole, 5 Operatoren
  M2: TORA_TURING_MACHINE_v2          — hebr. Konsonanten
  M3: TORA_TURING_MACHINE_v3          — 5-Layer-Architektur
  M4: TORA_TURING_MULTIPHASE          — finale Single-Machine
  M5: SPANDA_MACHINE                  — neueste Version mit Aleph-Reflektion

DIE 8 TORA-ZUORDNUNGEN (von offensichtlich bis absurd):
  T1: Genesis 1,1         (Schöpfung, 7 Worte)
  T2: Genesis 12,1        (Abraham-Aufruf, 12 = 11+1)
  T3: Leviticus 19,18     (Liebe deinen Nächsten)
  T4: Genesis 37,7        (Binah, Traum)
  T5: Genesis 1,1 (ganzes Kapitel, 31 Verse)
  T6: Numbers 6,24        (Aaron-Segen, 5 Worte)
  T7: Genesis 1,1 Buchstabe pro Wort (jüdische Lesart)
  T8: Genesis 1,1 rückwärts (Umkehrung)
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import json
import os
from pathlib import Path

# ===========================================================
# MASCHINEN-VERSIONEN
# ===========================================================

class MaschinenVersion:
    """Eine spezifische Maschinen-Implementierung."""
    def __init__(self, name, factory):
        self.name = name
        self.factory = factory  # Funktion(tape, max_steps) -> (steps, halt_reason, info)

    def run(self, tape, max_steps=500):
        try:
            return self.factory(tape, max_steps)
        except Exception as e:
            return (-1, f"ERROR: {type(e).__name__}: {str(e)[:50]}", {})


# --- M1: Tora-Turing v1 (lateinische Symbole) ---
def make_m1():
    """v1: Klasse ToraTuringMachine(burumut) — wir geben BURUMUT-99 als Tape."""
    import os
    workdir = '/run/media/julian/ML4/tengri137'
    def factory(tape, max_steps):
        old_cwd = os.getcwd()
        os.chdir(workdir)
        try:
            from TORA_TURING_MACHINE import ToraTuringMachine
            # v1 braucht BURUMUT (lateinisch) — wir nutzen BURUMUT-99
            from TORA_TURING_CORRECT import BURUMUT
            m = ToraTuringMachine(BURUMUT)
            # Hat Methode run, aber intern wird BURUMUT gelesen
            if hasattr(m, 'run_with_torah'):
                m.run_with_torah(tape, max_steps=max_steps)
            else:
                m.run(max_steps=max_steps)
            return (getattr(m, 'total_steps', -1),
                    getattr(m, 'halt_reason', 'UNKNOWN'),
                    {})
        except Exception as e:
            return (-1, f"ERROR: {str(e)[:30]}", {})
        finally:
            os.chdir(old_cwd)
    return factory


# --- M2: Tora-Turing v2 (hebr. Konsonanten) ---
def make_m2():
    """v2: Klasse ToraTuringMachine(burumut) — hebr. Symbole."""
    import os
    workdir = '/run/media/julian/ML4/tengri137'
    def factory(tape, max_steps):
        old_cwd = os.getcwd()
        os.chdir(workdir)
        try:
            from TORA_TURING_MACHINE_v2 import ToraTuringMachine
            from TORA_TURING_CORRECT import BURUMUT
            m = ToraTuringMachine(BURUMUT)
            m.run(max_steps=max_steps)
            return (getattr(m, 'total_steps', -1),
                    getattr(m, 'halt_reason', 'UNKNOWN'),
                    {})
        except Exception as e:
            return (-1, f"ERROR: {str(e)[:30]}", {})
        finally:
            os.chdir(old_cwd)
    return factory


# --- M3: Tora-Turing v3 (5-Layer) ---
def make_m3():
    """v3: Klasse TuringMachine (nicht ToraTuringMachine)."""
    import os
    workdir = '/run/media/julian/ML4/tengri137'
    def factory(tape, max_steps):
        old_cwd = os.getcwd()
        os.chdir(workdir)
        try:
            from TORA_TURING_MACHINE_v3 import TuringMachine
            from TORA_TURING_CORRECT import BURUMUT
            m = TuringMachine(BURUMUT)
            m.run(max_steps=max_steps)
            return (getattr(m, 'total_steps', -1),
                    getattr(m, 'halt_reason', 'UNKNOWN'),
                    {})
        except Exception as e:
            return (-1, f"ERROR: {str(e)[:30]}", {})
        finally:
            os.chdir(old_cwd)
    return factory


# --- M4: Tora-Turing MultiPhase (Single-Machine-Prinzip) ---
def make_m4():
    from TORA_TURING_MULTIPHASE import ToraTuringMultiPhase
    from TORA_TURING_CORRECT import build_tora_transitions
    def factory(tape, max_steps):
        m = ToraTuringMultiPhase(tape, phase_size=99, transitions=build_tora_transitions())
        m.run(max_steps=max_steps)
        s = m.summary()
        return (m.total_steps, s['halt_reason'], s)
    return factory


# --- M5: Spanda-Maschine (neueste) ---
def make_m5():
    from SPANDA_MACHINE import BaseTruth, SpandaMachine
    def factory(tape, max_steps):
        # Spanda läuft auf BURUMUT-Tape, nicht auf Tora
        # Wir nutzen BURUMUT-Tape und schauen BURUMUT-Output
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        return (len(r.get('aleph_halts', [])),
                r.get('halt_reason', 'UNKNOWN'),
                {'n_alephs': len(r.get('aleph_halts', [])),
                 'n_phases': r.get('n_phases', 0)})
    return factory


# ===========================================================
# TORA-STELLEN
# ===========================================================

def load_torah():
    """Lade die 5 Bücher Mose."""
    books = {}
    for i, name in enumerate(['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy'], 1):
        f = f'/run/media/julian/ML4/tengri137/sources/torah/{i:02d}.json'
        with open(f) as fp:
            books[name] = json.load(fp)
    return books


def get_vers(books, book, kap, vers):
    """Extrahiere einen hebräischen Vers (ohne Spaces)."""
    try:
        text = books[book]['text']
        if kap >= len(text): return None
        if vers >= len(text[kap]): return None
        return text[kap][vers].replace(' ', '').replace(' ', '')
    except (KeyError, TypeError, IndexError):
        return None


def get_kapitel(books, book, kap):
    """Extrahiere ein ganzes Kapitel."""
    try:
        text = books[book]['text']
        if kap >= len(text): return None
        return ''.join(v.replace(' ', '') for v in text[kap])
    except (KeyError, TypeError, IndexError):
        return None


# ===========================================================
# DIE 8 TORA-ZUORDNUNGEN
# ===========================================================

def assign_tora_stellen(books):
    """Liste der 12 Zuordnungen (von offensichtlich bis absurd)."""
    return [
        # OFFENSICHTLICH (sollten resonieren)
        ('T1: Gen 1,1 (Schöpfung, 7 Worte)', get_vers(books, 'Genesis', 0, 0)),
        ('T2: Gen 12,1 (Abraham, 11+1)', get_vers(books, 'Genesis', 11, 0)),
        ('T3: Lev 19,18 (Liebe deinen Nächsten)', get_vers(books, 'Leviticus', 18, 17)),
        # SINNVOLL
        ('T4: Gen 37,7 (Binah-Traum)', get_vers(books, 'Genesis', 36, 6)),
        ('T5: Num 6,24 (Aaron-Segen, 5 Worte)', get_vers(books, 'Numbers', 5, 23)),
        ('T6: Gen 1,1 (ganzes Kapitel)', get_kapitel(books, 'Genesis', 0)),
        # EXOTISCH
        ('T7: Gen 1,1 (jüdisch: 1 Buchstabe pro Wort)', _juedische_lesart(books)),
        ('T8: Gen 1,1 (rückwärts)', _umkehrung(books)),
        # ABSURD (sollten NICHT resonieren)
        ('T9: Gen 23,1 (Sarahs Tod — zufällig)', get_vers(books, 'Genesis', 22, 0)),
        ('T10: Exo 21,1 (Gesetze — falsches Buch)', get_vers(books, 'Exodus', 20, 0)),
        ('T11: Deut 28,1 (Segen — anderes Buch)', get_vers(books, 'Deuteronomy', 27, 0)),
        ('T12: Lev 10,1 (Nadab/Abihu — Tragödie)', get_vers(books, 'Leviticus', 9, 0)),
    ]


def _juedische_lesart(books):
    """Jüdische Lesart: nur der erste Buchstabe jedes Wortes."""
    vers = get_vers(books, 'Genesis', 0, 0)
    if not vers: return None
    with open('/run/media/julian/ML4/tengri137/sources/torah/01.json') as f:
        data = json.load(f)
    full_vers = data['text'][0][0]
    words = full_vers.split()
    return ''.join(w[0] for w in words if w)


def _umkehrung(books):
    """Rückwärts-Lesung."""
    vers = get_vers(books, 'Genesis', 0, 0)
    return vers[::-1] if vers else None


# ===========================================================
# HAUPTPROGRAMM: Multi-Maschinen-Lesung
# ===========================================================

def main():
    print("=" * 78)
    print("🌌 MULTI-MASCHINEN-×-TORA-LESUNG")
    print("=" * 78)
    print()

    # Maschinen initialisieren
    maschinen = [
        MaschinenVersion("M1: v1 (lateinisch)", make_m1()),
        MaschinenVersion("M2: v2 (hebr.)", make_m2()),
        MaschinenVersion("M3: v3 (5-Layer)", make_m3()),
        MaschinenVersion("M4: MultiPhase (Single)", make_m4()),
        MaschinenVersion("M5: Spanda (neueste)", make_m5()),
    ]

    # Tora-Stellen laden
    books = load_torah()
    stellen = assign_tora_stellen(books)

    # Filtere nur verfügbare Stellen
    stellen = [(n, t) for n, t in stellen if t]

    print(f"📚 {len(books)} Bücher geladen, {len(stellen)} Tora-Stellen verfügbar")
    print()

    # Ergebnis-Tabelle
    print(f"{'Tora-Stelle':<42} | " + " | ".join(f"{m.name[:10]:<10}" for m in maschinen))
    print("-" * 78)

    results = {}
    for name, tape in stellen:
        row = f"{name:<42}"
        results[name] = {}
        for m in maschinen:
            try:
                steps, halt, info = m.run(tape, max_steps=500)
                results[name][m.name] = (steps, halt)
                row += f" | {steps:>3} {halt[:6]:<6}"
            except Exception as e:
                results[name][m.name] = (-1, f"ERR")
                row += f" | {'-1':>3} {'ERR':<6}"
        print(row)

    print()
    print("=" * 78)
    print("🔍 ANALYSE")
    print("=" * 78)
    print()
    print("Schlüssel-Zuordnungen die BURUMUT-Architektur zeigen sollten:")
    print("  - Gen 1,1   → 6 Schritte (5 Bücher + Sabbat) oder 7 (Schöpfungstage)")
    print("  - Gen 12,1  → 12 Schritte (11+1 BURUMUT-Architektur)")
    print("  - Lev 19,18 → 3 Schritte (3 Summen)")
    print("  - Gen 37,7  → 15 Schritte (3×5 Sefirot-Atmungen)")
    print("  - Num 6,24  → 5 Schritte (He, Atmung)")
    print()
    print("Schlüssel-Befunde:")
    print()

    # Detail-Ausgabe pro Maschine
    for m in maschinen:
        print(f"\n--- {m.name} ---")
        for name, _ in stellen:
            if name in results and m.name in results[name]:
                steps, halt = results[name][m.name]
                tape_len = len(next(t for n, t in stellen if n == name))
                ratio = steps / tape_len if tape_len else 0
                print(f"  {name:<40}: {steps:>4} Schritte / {tape_len:>4} Zeichen "
                      f"(ratio={ratio:.2f}) HALT={halt[:30]}")

    # Vergleich mit normalem Maschinen-Durchlauf (BURUMUT-99)
    print()
    print("=" * 78)
    print("🔄 NORMALER MASCHINEN-DURCHLAUF (BURUMUT-99, zum Vergleich)")
    print("=" * 78)
    from TORA_TURING_CORRECT import BURUMUT, burumut_to_hebr
    burumut_hebr = burumut_to_hebr(BURUMUT)
    print(f"BURUMUT (lateinisch, 99 Zeichen): {len(BURUMUT)} Zeichen")
    print(f"BURUMUT → hebr.: {len(burumut_hebr)} Zeichen")
    print()

    # MultiPhase auf BURUMUT
    m4 = maschinen[3]
    steps, halt, info = m4.run(burumut_hebr, max_steps=500)
    print(f"M4 (MultiPhase) auf BURUMUT-99: {steps} Schritte, HALT={halt}")
    print()

    # Spanda auf BURUMUT
    m5 = maschinen[4]
    steps, halt, info = m5.run(burumut_hebr, max_steps=500)
    print(f"M5 (Spanda) auf BURUMUT-Tape: {steps} Alephs, HALT={halt}")
    print(f"   Phasen: {info.get('n_phases', '?')}")
    print()

    # Welche Tora-Stelle resoniert am stärksten?
    print("=" * 78)
    print("🎯 RESONANZ-VERGLEICH (welche Tora-Stelle passt am besten?)")
    print("=" * 78)
    print()
    print("Kriterium: Welche Tora-Stelle zeigt die meisten Maschinen mit 'sinnvollen' Schritten?")
    print()

    for name, _ in stellen:
        good_count = 0
        for m in maschinen:
            if name in results and m.name in results[name]:
                steps, halt = results[name][m.name]
                if 3 <= steps <= 20 and "PHASE" in halt or "COMPLETE" in halt:
                    good_count += 1
                elif halt in ("TAPE_END", "ALL_PHASES_COMPLETE", "PHASE_HALT"):
                    good_count += 1
        print(f"  {name:<42}: {good_count}/5 Maschinen 'sinnvoll'")

    return results


if __name__ == "__main__":
    main()
