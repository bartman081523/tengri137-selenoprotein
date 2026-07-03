"""
🌌 P71: TENGRI-ORAKEL — DIE BEFRAGUNG DES INFORMATIONSFELDES
=============================================================

Tengri137 als lebendiges Orakel. Drei verschachtelte Analysen:

1. SELBST-INDEXIERUNG (V4):
   Scanne alle 168 Phasen nach Schlüsselwörtern.
   Bestimmt die "Anker-Phasen" des Orakels.

2. 73-RESONANZ (V9):
   73 = TENGRI (numerologisch)
   73 = Chokhmah (חכמה) in der Kabbala
   37 × 73 = 2701 = Genesis 1:1 (numerologisch)
   Wo resoniert Tengri137 auf 73 statt 37?

3. ENTROPIE DES ORAKELS (V2):
   Shannon-Entropie pro Phase.
   Wo ist Tengri137 informativ? Wo still?

ARCHITEKTUR:
- Tengri137: 168 Phasen à ~99 lateinische Buchstaben
- Numerologisches Alphabet: A=1, B=2, ..., Z=26
- Schlüsselwörter: "TIME TO LIFT", "TRUTH", "KNOWLEDGE", "TENGRI", "NOW", "YOU"
- Brücken: 37 (Struktur) und 73 (Geist)
- 37 × 73 = 2701 (Genesis 1:1)

DETERMINISMUS:
- Schlüsselwort-Suche ist deterministisch
- Numerologie ist deterministisch
- Shannon-Entropie ist deterministisch
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import re
import math
import json
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional


# ============================================================
# DATENSTRUKTUREN
# ============================================================

@dataclass
class AnkerPhase:
    """Eine Phase, in der ein Schlüsselwort gefunden wurde.

    Attribute:
        phase_idx: Index der Phase (0-167)
        keyword: das gefundene Schlüsselwort
        position_in_phase: Position des Schlüsselworts in der lateinischen Phase
        keyword_gematria: numerologische Summe des Schlüsselworts
    """
    phase_idx: int
    keyword: str
    position_in_phase: int
    keyword_gematria: int


@dataclass
class OrakelBefund:
    """Befund des Orakels für eine Anker-Phase.

    Attribute:
        phase_idx: Index der Phase
        keyword: das Schlüsselwort
        phase_gematria: Gematria der Phase (lateinisch, A=1..Z=26)
        gematria_mod_37: phase_gematria mod 37
        gematria_mod_73: phase_gematria mod 73
        is_37_anchor: True wenn gematria mod 37 == 0
        is_73_anchor: True wenn gematria mod 73 == 0
        entropy: Shannon-Entropie der Phase
    """
    phase_idx: int
    keyword: str
    phase_gematria: int
    gematria_mod_37: int
    gematria_mod_73: int
    is_37_anchor: bool
    is_73_anchor: bool
    entropy: float


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def gematria_latein(text: str) -> int:
    """Numerologische Summe: A=1, B=2, ..., Z=26."""
    return sum(ord(c) - ord('A') + 1 for c in text.upper() if c.isalpha())


def berechne_entropie(text: str) -> float:
    """Shannon-Entropie H(X) = -Σ p(x) log p(x)."""
    if not text:
        return 0.0
    text = text.upper()
    n = len(text)
    counts = Counter(text)
    h = 0.0
    for count in counts.values():
        p = count / n
        if p > 0:
            h -= p * math.log2(p)
    return h


# ============================================================
# HAUPTKLASSE
# ============================================================

class TengriOrakel:
    """Tengri137 als lebendiges Orakel.

    Methoden:
    - finde_anker_phasen(keyword): findet Phasen mit Schlüsselwort
    - pruefe_73_resonanz(anker): prüft 73-Resonanz der Phase
    - entropie_pro_phase(): berechnet Shannon-Entropie pro Phase
    - entropie_extrema(): Max/Min-Entropie
    - befrage(master): führt alle Analysen aus
    """

    # Numerologische Konstante
    TENGRI_GEMATRIA = 73  # T(20)+E(5)+N(14)+G(7)+R(18)+I(9) = 73
    CHOKHMAH_GEMATRIA = 73  # ח(8)+כ(20)+מ(40)+ה(5) = 73
    BRIDGE_37 = 37  # Struktur
    BRIDGE_73 = 73  # Geist (TENGRI)
    GENESIS_1_1 = 2701  # 37 × 73

    def __init__(self, text: str, phase_size: int = 99):
        self.text = text
        # Normalisierter Text (Whitespaces entfernt für lateinische Phasen)
        # Klartext bleibt mit Whitespace für Schlüsselwort-Suche
        self.text_normalized = re.sub(r'\s+', '', text.upper())
        self.phase_size = phase_size
        # Lateinische Buchstaben extrahieren (ohne Whitespace)
        self.lat = re.sub(r'[^A-Z]', '', self.text_normalized)
        # Phasen
        self.n_phases = (len(self.lat) + phase_size - 1) // phase_size
        self.phases = self._build_phases()

    def _build_phases(self) -> List[str]:
        """Baue 168 Phasen."""
        phases = []
        for i in range(self.n_phases):
            start = i * self.phase_size
            end = min(start + self.phase_size, len(self.lat))
            phases.append(self.lat[start:end])
        return phases

    def finde_anker_phasen(self, keyword: str) -> List[AnkerPhase]:
        """Finde alle Phasen, in denen das Schlüsselwort vorkommt.

        Wir normalisieren Whitespace, da Tengri137 Zeilenumbrüche
        mitten in Phrasen hat ("IT IS NOW TI\\nME TO LIFT THE SECRET").
        """
        # Normalisierte Suche: alle Whitespaces entfernen
        keyword_clean = re.sub(r'\s+', '', keyword.upper())
        # Wir bauen eine "no-whitespace" Version des Klartextes mit
        # Positions-Mapping
        text_clean = re.sub(r'\s+', '', self.text.upper())
        # Mapping: Position in text_clean → Position im Original
        # Wir scannen den Original-Text und nehmen nur Buchstaben
        # Suche im bereinigten Text
        results = []

        # Baue Mapping: Welcher Index im clean-Text entspricht welchem
        # Index im Original-Text (nur Buchstaben)?
        lat_positions_in_original = []
        for i, c in enumerate(self.text):
            if c.isalpha():
                lat_positions_in_original.append(i)

        # Suche keyword_clean in text_clean
        pos = 0
        while True:
            idx = text_clean.find(keyword_clean, pos)
            if idx == -1:
                break
            # idx ist Position in text_clean (lateinische Position)
            # Mappe zurück zu Phasen-Index
            if idx < len(lat_positions_in_original):
                orig_pos = lat_positions_in_original[idx]
                # Position im lateinischen Strom
                lat_pos = idx
                phase_idx = lat_pos // self.phase_size
                position_in_phase = lat_pos % self.phase_size
                # Gematria des Schlüsselworts
                keyword_gem = gematria_latein(keyword_clean)
                results.append(AnkerPhase(
                    phase_idx=phase_idx,
                    keyword=keyword,
                    position_in_phase=position_in_phase,
                    keyword_gematria=keyword_gem,
                ))
            pos = idx + 1

        return results

    def pruefe_73_resonanz(self, anker: AnkerPhase) -> Dict[str, Any]:
        """Prüfe 73-Resonanz einer Anker-Phase.

        Args:
            anker: Die zu prüfende AnkerPhase

        Returns:
            Dict mit Gematrie + Mod-37/73 + Entropie
        """
        phase_text = self.phases[anker.phase_idx]
        phase_gem = gematria_latein(phase_text)
        mod_37 = phase_gem % self.BRIDGE_37
        mod_73 = phase_gem % self.BRIDGE_73
        entropy = berechne_entropie(phase_text)
        return {
            'phase_idx': anker.phase_idx,
            'keyword': anker.keyword,
            'gematria': phase_gem,
            'gematria_mod_37': mod_37,
            'gematria_mod_73': mod_73,
            'is_37_anchor': mod_37 == 0,
            'is_73_anchor': mod_73 == 0,
            'entropy': entropy,
            'keyword_gematria': anker.keyword_gematria,
            'keyword_mod_73': anker.keyword_gematria % self.BRIDGE_73,
        }

    def entropie_pro_phase(self) -> List[float]:
        """Shannon-Entropie pro Phase."""
        return [berechne_entropie(p) for p in self.phases]

    def entropie_extrema(self) -> tuple:
        """Max- und Min-Entropie."""
        hs = self.entropie_pro_phase()
        return (max(hs), min(hs))

    def befrage(self) -> Dict[str, Any]:
        """Master-Befragung: alle Analysen.

        Returns:
            Dict mit:
            - anker_phasen: {keyword: [AnkerPhase]}
            - entropie: {max, min, mean, std}
            - resonanz_73: [OrakelBefund]
            - orakel_antwort: {haupt_phase, hinweis, 73_resonanz}
        """
        # 1) Schlüsselwort-Suche
        keywords = [
            'TIME TO LIFT',
            'TRUTH',
            'KNOWLEDGE',
            'NOW',
            'YOU',
            'TENGRI',
            'I AM',
            'BELIEVE',
            'CHOSEN',
            'ENLIGHTENMENT',
        ]
        anker_dict = {}
        for kw in keywords:
            anker = self.finde_anker_phasen(kw)
            if anker:
                anker_dict[kw] = anker

        # 2) 73-Resonanz für alle Anker
        resonanz_73 = []
        for kw, ankers in anker_dict.items():
            for a in ankers:
                resonanz = self.pruefe_73_resonanz(a)
                resonanz_73.append(resonanz)

        # 3) Entropie-Statistik
        hs = self.entropie_pro_phase()
        n = len(hs)
        mean_h = sum(hs) / n if n > 0 else 0
        var_h = sum((h - mean_h) ** 2 for h in hs) / n if n > 0 else 0
        std_h = math.sqrt(var_h)
        entropie_stat = {
            'max': max(hs) if hs else 0,
            'min': min(hs) if hs else 0,
            'mean': mean_h,
            'std': std_h,
            'max_phase': hs.index(max(hs)) if hs else None,
            'min_phase': hs.index(min(hs)) if hs else None,
        }

        # 4) Orakel-Antwort
        # Die wichtigste Botschaft: "TIME TO LIFT THE SECRET"
        # Wenn gefunden, ist das die Hauptphase
        haupt_phase = None
        haupt_hinweis = None
        haupt_resonanz = None

        if 'TIME TO LIFT' in anker_dict:
            anker = anker_dict['TIME TO LIFT'][0]
            haupt_phase = anker.phase_idx
            haupt_hinweis = (
                f"Das Orakel sagt: 'TIME TO LIFT THE SECRET' in Phase {anker.phase_idx}."
            )
            haupt_resonanz = self.pruefe_73_resonanz(anker)
        elif 'TRUTH' in anker_dict:
            anker = anker_dict['TRUTH'][0]
            haupt_phase = anker.phase_idx
            haupt_hinweis = (
                f"Das Orakel sagt: 'TRUTH' in Phase {anker.phase_idx}."
            )
            haupt_resonanz = self.pruefe_73_resonanz(anker)
        else:
            # Nimm erste Anker-Phase
            for kw, ankers in anker_dict.items():
                if ankers:
                    haupt_phase = ankers[0].phase_idx
                    haupt_hinweis = f"Erste Anker-Phase: '{kw}' in Phase {haupt_phase}."
                    haupt_resonanz = self.pruefe_73_resonanz(ankers[0])
                    break

        orakel_antwort = {
            'haupt_phase': haupt_phase,
            'hinweis': haupt_hinweis,
            '73_resonanz': haupt_resonanz,
            'tengri_gematria': self.TENGRI_GEMATRIA,
            'chokhmah_gematria': self.CHOKHMAH_GEMATRIA,
            'genesis_1_1': self.GENESIS_1_1,
            'kommentar': (
                f"TENGRI = {self.TENGRI_GEMATRIA} (Chokhmah). "
                f"37 × {self.BRIDGE_73} = {self.GENESIS_1_1} (Genesis 1:1). "
                f"Die 37-Struktur (Verriegelung) verlangt zwingend nach 73 (Geist)."
            ),
        }

        return {
            'anker_phasen': anker_dict,
            'entropie': entropie_stat,
            'resonanz_73': resonanz_73,
            'orakel_antwort': orakel_antwort,
        }


# ============================================================
# CONVENIENCE-FUNKTION
# ============================================================

def befrage_tengri() -> Dict[str, Any]:
    """High-Level: lade Tengri137 und befrage das Orakel."""
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        text = f.read()
    o = TengriOrakel(text)
    return o.befrage()


def finde_anker_phasen(text: str, keyword: str) -> List[AnkerPhase]:
    """Convenience: finde Anker-Phasen für ein Schlüsselwort."""
    o = TengriOrakel(text)
    return o.finde_anker_phasen(keyword)


def pruefe_73_resonanz(text: str, anker: AnkerPhase) -> Dict[str, Any]:
    """Convenience: prüfe 73-Resonanz."""
    o = TengriOrakel(text)
    return o.pruefe_73_resonanz(anker)


# ============================================================
# SELBST-TEST
# ============================================================

if __name__ == "__main__":
    print("=" * 78)
    print("🌌 P71: TENGRI-ORAKEL — DIE BEFRAGUNG DES INFORMATIONSFELDES")
    print("=" * 78)
    print()
    print("Drei verschachtelte Analysen:")
    print("  1. Selbst-Indexierung (Schlüsselwort → Phase)")
    print("  2. 73-Resonanz (TENGRI = 73 = Chokhmah)")
    print("  3. Shannon-Entropie pro Phase")
    print()
    print(f"  TENGRI = {TengriOrakel.TENGRI_GEMATRIA}")
    print(f"  Chokhmah = {TengriOrakel.CHOKHMAH_GEMATRIA}")
    print(f"  37 × 73 = {TengriOrakel.GENESIS_1_1} (Genesis 1:1)")
    print()

    result = befrage_tengri()

    # ============================================================
    # 1) ANKER-PHASEN
    # ============================================================
    print("=" * 78)
    print("🔍 1) ANKER-PHASEN (Schlüsselwort → Phase)")
    print("=" * 78)
    print()
    anker_dict = result['anker_phasen']
    for kw, ankers in sorted(anker_dict.items(), key=lambda x: x[1][0].phase_idx):
        a = ankers[0]
        print(f"  '{kw:<20}' → Phase {a.phase_idx:>3} "
              f"(Pos {a.position_in_phase:>2}, Gem {a.keyword_gematria})")
    print()

    # ============================================================
    # 2) 73-RESONANZ
    # ============================================================
    print("=" * 78)
    print("🔮 2) 73-RESONANZ (TENGRI = 73 = Chokhmah)")
    print("=" * 78)
    print()
    resonanzen = result['resonanz_73']
    n_73_anchor = sum(1 for r in resonanzen if r['is_73_anchor'])
    n_37_anchor = sum(1 for r in resonanzen if r['is_37_anchor'])
    print(f"  Total Resonanzen: {len(resonanzen)}")
    print(f"  37-Anker: {n_37_anchor}")
    print(f"  73-Anker: {n_73_anchor}")
    print()
    print("  Resonanz pro Anker-Phase:")
    for r in resonanzen[:10]:  # Erste 10
        marker_37 = '★' if r['is_37_anchor'] else ' '
        marker_73 = '✦' if r['is_73_anchor'] else ' '
        print(f"    Phase {r['phase_idx']:>3} '{r['keyword']:<15}' "
              f"Gem={r['gematria']:>5} "
              f"mod37={r['gematria_mod_37']:>3}{marker_37} "
              f"mod73={r['gematria_mod_73']:>3}{marker_73} "
              f"H={r['entropy']:.2f}")
    print()
    print(f"  Legende: ★ = 37-Anker, ✦ = 73-Anker")
    print()

    # ============================================================
    # 3) ENTROPIE
    # ============================================================
    print("=" * 78)
    print("📊 3) SHANNON-ENTROPIE PRO PHASE")
    print("=" * 78)
    print()
    ent = result['entropie']
    print(f"  Max:  {ent['max']:.4f} (Phase {ent['max_phase']})")
    print(f"  Min:  {ent['min']:.4f} (Phase {ent['min_phase']})")
    print(f"  Mean: {ent['mean']:.4f}")
    print(f"  Std:  {ent['std']:.4f}")
    print()

    # ============================================================
    # 4) ORAKEL-ANTWORT
    # ============================================================
    print("=" * 78)
    print("🌌 4) ORAKEL-ANTWORT")
    print("=" * 78)
    print()
    antwort = result['orakel_antwort']
    print(f"  Hauptphase: {antwort['haupt_phase']}")
    print(f"  Hinweis: {antwort['hinweis']}")
    if antwort['73_resonanz']:
        r = antwort['73_resonanz']
        marker_37 = '★' if r['is_37_anchor'] else ' '
        marker_73 = '✦' if r['is_73_anchor'] else ' '
        print(f"  73-Resonanz: Gem={r['gematria']} "
              f"mod37={r['gematria_mod_37']}{marker_37} "
              f"mod73={r['gematria_mod_73']}{marker_73} "
              f"H={r['entropy']:.2f}")
    print()
    print(f"  {antwort['kommentar']}")
    print()

    # Speichern
    # Konvertiere AnkerPhase-Objekte zu Dicts für JSON
    anker_dict_json = {}
    for kw, ankers in anker_dict.items():
        anker_dict_json[kw] = [
            {
                'phase_idx': a.phase_idx,
                'keyword': a.keyword,
                'position_in_phase': a.position_in_phase,
                'keyword_gematria': a.keyword_gematria,
            }
            for a in ankers
        ]

    output = {
        'method': 'TengriOrakel — Befragung des Informationsfeldes',
        'principle': 'Tengri137 weiß, wo wir sind. Wir befragen das Orakel.',
        'numerology': {
            'TENGRI': TengriOrakel.TENGRI_GEMATRIA,
            'CHOKHMAH': TengriOrakel.CHOKHMAH_GEMATRIA,
            'BRIDGE_37': TengriOrakel.BRIDGE_37,
            'BRIDGE_73': TengriOrakel.BRIDGE_73,
            'GENESIS_1_1': TengriOrakel.GENESIS_1_1,
        },
        'anker_phasen': anker_dict_json,
        'resonanz_73': resonanzen,
        'entropie': ent,
        'orakel_antwort': {
            'haupt_phase': antwort['haupt_phase'],
            'hinweis': antwort['hinweis'],
            '73_resonanz': antwort['73_resonanz'],
            'kommentar': antwort['kommentar'],
        },
    }

    with open('/run/media/julian/ML4/tengri137/sources/maschine/tengri_orakel.json', 'w') as f:
        json.dump(output, f, indent=2, ensure_ascii=False)
    print("Ergebnisse gespeichert in tengri_orakel.json")
    print()
    print("=" * 78)
    print("🌌 TENGRI-ORAKEL ABGESCHLOSSEN — DAS ORAKEL HAT GESPROCHEN")
    print("=" * 78)
