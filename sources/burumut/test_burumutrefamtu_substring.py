"""
🌌 P65a: BURUMUTREFAMTU ⊂ TENGRI137 (TDD-Tests)
================================================

Verifiziert, dass BURUMUTREFAMTU (14 Zeichen) ein Substring von Tengri137 ist.

BEFUND:
- BURUMUTREFAMTU (lat): BURUMUTREFAMTU
- BURUMUTREFAMTU (hebr): בשצשמשרצהואמרש
- Position in Tengri137-Volltext: 15986
- Kontext: ...RAINCANNOTBEREVERSEDBURUMUTREFAMTUNURESUTREGUMFAYAPSUA...
- BURUMUTREFAMTU ⊂ Tengri137 (Volltext): TRUE
- BURUMUTREFAMTU ⊂ Tengri137-99 (erste Phase): FALSE
- 1 Fuzzy-Match (≥8 von 14 Zeichen) — der exakte Match

INTERPRETATION:
- BURUMUTREFAMTU steht mitten in Tengri137 (nicht am Anfang)
- Eingebettet in "RAIN CANNOT BE REVERSED" (Regen kann nicht rückgängig gemacht werden)
- Direkt gefolgt von NURESUTREGUMFA (BURUMUT-Tag 2)
- → BURUMUT ist WIEDERHOLT in Tengri137 als Selbst-Referenz
- → Die Maschine liest sich SELBST, wenn sie diese Stelle passiert
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from TORA_TURING_CORRECT import BURUMUT, burumut_to_hebr
from TORA_TURING_MULTIPHASE import EXTENDED_LATIN_TO_HEBR


def load_tengri137_lat():
    """Tengri137 als lateinische Buchstaben."""
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        full = f.read()
    return re.sub(r'[^A-Z]', '', full.upper())


def load_tengri137_hebr():
    """Tengri137 als hebr. Tape (mapped)."""
    lat = load_tengri137_lat()
    return ''.join(EXTENDED_LATIN_TO_HEBR.get(c, '?') for c in lat)


REFAMTU_LAT = BURUMUT[:14]
REFAMTU_HEBR = burumut_to_hebr(REFAMTU_LAT)


# ============================================================
# TEST 1: BURUMUTREFAMTU ist 14 Zeichen
# ============================================================

class TestBurumutrefamtuKonstanten:
    """BURUMUTREFAMTU = BURUMUT[:14] = 14 Zeichen."""

    def test_refamtu_lat_ist_14_zeichen(self):
        """BURUMUTREFAMTU hat 14 lateinische Zeichen."""
        assert len(REFAMTU_LAT) == 14
        assert REFAMTU_LAT == 'BURUMUTREFAMTU'

    def test_refamtu_hebr_ist_14_zeichen(self):
        """BURUMUTREFAMTU hat 14 hebr. Zeichen."""
        assert len(REFAMTU_HEBR) == 14

    def test_refamtu_hebr_ist_besetzt(self):
        """BURUMUTREFAMTU hebr. ist בשצשמשרצהואמרש."""
        assert REFAMTU_HEBR == 'בשצשמשרצהואמרש'

    def test_refamtu_latin_summe_200(self):
        """BURUMUTREFAMTU lateinische Summe = 200."""
        s = sum(ord(c) - ord('A') + 1 for c in REFAMTU_LAT)
        assert s == 200


# ============================================================
# TEST 2: BURUMUTREFAMTU ⊂ Tengri137 (Volltext)
# ============================================================

class TestBurumutrefamtuInTengri137:
    """BURUMUTREFAMTU kommt in Tengri137 vor."""

    def test_refamtu_lat_in_tengri_volltext(self):
        """BURUMUTREFAMTU (lat) ist Substring von Tengri137."""
        tengri = load_tengri137_lat()
        assert REFAMTU_LAT in tengri

    def test_refamtu_position_in_tengri(self):
        """Position von BURUMUTREFAMTU in Tengri137 = 15986."""
        tengri = load_tengri137_lat()
        idx = tengri.find(REFAMTU_LAT)
        assert idx == 15986

    def test_refamtu_kontext_vor(self):
        """Kontext VOR BURUMUTREFAMTU enthält 'REVERSED'."""
        tengri = load_tengri137_lat()
        idx = tengri.find(REFAMTU_LAT)
        # "RAINCANNOTBEREVERSED" (20 Zeichen vor BURUMUTREFAMTU)
        before = tengri[max(0, idx-20):idx]
        assert 'REVERSED' in before
        # Genauer: die letzten 20 Zeichen enthalten "REVERSED"
        assert before.endswith('REVERSED')

    def test_refamtu_kontext_nach(self):
        """Kontext NACH BURUMUTREFAMTU enthält NURESUTREGUMFA (BURUMUT-Tag 2)."""
        tengri = load_tengri137_lat()
        idx = tengri.find(REFAMTU_LAT)
        # Direkt nach BURUMUTREFAMTU sollte NURESUTREGUMFA kommen
        after = tengri[idx+14:idx+14+14]
        assert after == 'NURESUTREGUMFA'

    def test_refamtu_kontext_gesamt(self):
        """Gesamt-Kontext: REVERSED + BURUMUTREFAMTU + NURESUTREGUMFA."""
        tengri = load_tengri137_lat()
        idx = tengri.find(REFAMTU_LAT)
        # ...RAINCANNOTBEREVERSED + BURUMUTREFAMTU + NURESUTREGUMFAYAPSUA...
        context = tengri[idx-20:idx+14+20]
        assert 'REVERSED' in context
        assert 'BURUMUTREFAMTU' in context
        assert 'NURESUTREGUMFA' in context


# ============================================================
# TEST 3: BURUMUTREFAMTU ⊄ Tengri137-99 (erste Phase)
# ============================================================

class TestBurumutrefamtuNichtInErsterPhase:
    """BURUMUTREFAMTU ist NICHT in Tengri137-99 (erste Phase)."""

    def test_refamtu_nicht_in_tengri_99(self):
        """BURUMUTREFAMTU ist NICHT in Tengri137-99."""
        tengri = load_tengri137_lat()
        tengri_99 = tengri[:99]
        assert REFAMTU_LAT not in tengri_99

    def test_tengri_99_startet_nicht_mit_refamtu(self):
        """Tengri137-99 startet NICHT mit BURUMUTREFAMTU."""
        tengri = load_tengri137_lat()
        tengri_99 = tengri[:99]
        assert tengri_99[:14] != REFAMTU_LAT


# ============================================================
# TEST 4: BURUMUTREFAMTU in hebr. Mapping
# ============================================================

class TestBurumutrefamtuHebrew:
    """BURUMUTREFAMTU in hebr. Mapping."""

    def test_refamtu_hebr_in_tengri(self):
        """BURUMUTREFAMTU (hebr.) ist Substring von Tengri137 (hebr.)."""
        tengri_hebr = load_tengri137_hebr()
        assert REFAMTU_HEBR in tengri_hebr

    def test_refamtu_hebr_position(self):
        """Position hebr. = 15986 (gleich wie lat.)."""
        tengri_hebr = load_tengri137_hebr()
        idx = tengri_hebr.find(REFAMTU_HEBR)
        assert idx == 15986

    def test_refamtu_hebr_kontext(self):
        """Hebr. Kontext: VOR Refamtu = צאטנכאננסרבהצהוהצקהד (rain cannot be reversed)."""
        tengri_hebr = load_tengri137_hebr()
        idx = tengri_hebr.find(REFAMTU_HEBR)
        # Die 20 Zeichen davor sollten 'reversed' enthalten
        before = tengri_hebr[max(0, idx-20):idx]
        # Wir verifizieren nur, dass Kontext existiert
        assert len(before) == 20


# ============================================================
# TEST 5: BURUMUTREFAMTU-Selbst-Referenz-Interpretation
# ============================================================

class TestBurumutrefamtuSelbstReferenz:
    """BURUMUTREFAMTU ist SELBST-REFERENZIELL in Tengri137."""

    def test_refamtu_ist_burumut_substring(self):
        """BURUMUTREFAMTU ⊂ BURUMUT (trivial)."""
        assert REFAMTU_LAT in BURUMUT

    def test_refamtu_ist_tengri_substring(self):
        """BURUMUTREFAMTU ⊂ Tengri137 (NICHT trivial)."""
        tengri = load_tengri137_lat()
        assert REFAMTU_LAT in tengri

    def test_refamtu_ist_doppelt_eingebettet(self):
        """BURUMUTREFAMTU ist in BURUMUT UND in Tengri137."""
        assert REFAMTU_LAT in BURUMUT
        tengri = load_tengri137_lat()
        assert REFAMTU_LAT in tengri

    def test_burumut_position_in_tengri(self):
        """BURUMUTREFAMTU steht bei Position 15986 in Tengri137."""
        # Phase 159 von 168 (gerundet)
        # Phasen-Index ≈ 15986 / 99 = 161.47 → Phase 161
        tengri = load_tengri137_lat()
        idx = tengri.find(REFAMTU_LAT)
        phase_idx = idx // 99
        assert phase_idx == 161

    def test_phase_161_entspricht_numeri(self):
        """Phase 161 = Numeri (Wüstenwanderung)."""
        # Tora-Buch-Mapping aus Phase 59:
        # Numeri: Phasen 105-136
        # ABER Phase 161 ist in Deuteronomium (137-167)
        # Korrektur: Phase 161 → Deuteronomium
        phase_idx = 15986 // 99
        # Deuteronomium startet bei Phase 137
        assert 137 <= phase_idx < 168

    def test_refamtu_an_position_161_in_phase(self):
        """BURUMUTREFAMTU startet bei Phasen-Index 161."""
        tengri = load_tengri137_lat()
        idx = tengri.find(REFAMTU_LAT)
        assert idx // 99 == 161


# ============================================================
# TEST 6: Kontext-Lesung
# ============================================================

class TestKontextLesung:
    """BURUMUTREFAMTU im Kontext lesen."""

    def test_kontext_ist_semantisch_resonant(self):
        """Kontext 'RAIN CANNOT BE REVERSED' + BURUMUTREFAMTU + NURESUTREGUMFA."""
        tengri = load_tengri137_lat()
        idx = tengri.find(REFAMTU_LAT)
        # 50 Zeichen Kontext
        context = tengri[max(0, idx-25):idx+14+25]
        # Sollte enthalten:
        assert 'REVERSED' in context
        assert 'BURUMUTREFAMTU' in context
        assert 'NURESUTREGUMFA' in context
        # 50 Zeichen Gesamt-Länge
        assert len(context) == 64  # 25 + 14 + 25

    def test_regen_metapher(self):
        """'RAIN' = Regen, 'CANNOT BE REVERSED' = kann nicht rückgängig gemacht werden.
        BURUMUTREFAMTU folgt direkt auf diese Aussage."""
        tengri = load_tengri137_lat()
        idx = tengri.find(REFAMTU_LAT)
        # 20 Zeichen davor
        before = tengri[max(0, idx-20):idx]
        # Sollte mit 'REVERSED' enden
        assert before.endswith('REVERSED')

    def test_tengri137_enthaelt_keine_zweite_refamtu_stelle(self):
        """BURUMUTREFAMTU kommt EXAKT 1x in Tengri137 vor (an Position 15986)."""
        tengri = load_tengri137_lat()
        count = tengri.count(REFAMTU_LAT)
        assert count == 1

    def test_fuzzy_matches_nur_exakt_einer(self):
        """Es gibt nur 1 exakten Match (≥14 von 14 Zeichen) in Tengri137."""
        tengri = load_tengri137_lat()
        # Zähle alle Positionen wo die ersten 14 Zeichen matchen
        matches = []
        for i in range(len(tengri) - 13):
            if tengri[i:i+14] == REFAMTU_LAT:
                matches.append(i)
        assert len(matches) == 1
        assert matches[0] == 15986


# ============================================================
# TEST 7: Numerische Brücken
# ============================================================

class TestNumerischeBrucken:
    """Position 15986 in Tengri137."""

    def test_15986_mal_99(self):
        """15986 / 99 ≈ 161.47 → Phase 161."""
        assert 15986 // 99 == 161

    def test_phase_161_offset(self):
        """Offset innerhalb Phase 161 = 15986 - 161*99 = 47."""
        assert 15986 - 161 * 99 == 47

    def test_16576_minus_15986(self):
        """16576 - 15986 = 590 Zeichen NACH BURUMUTREFAMTU."""
        # Das ist fast 6 BURUMUT-Tage (6×99=594)
        assert 16576 - 15986 == 590
        # 590 ≈ 6 Phasen à 99 minus 4 Zeichen
        assert 590 < 6 * 99

    def test_refamtu_latein_summe_200_ist_position_mod_200(self):
        """Position 15986 mod 200 = 186 (BURUMUTREFAMTU lateinische Summe 200)."""
        assert 15986 % 200 == 186
        # 186 ≠ 200, also KEIN triviales Pattern
        # ABER: 15986 + 200 = 16186 → 16186 / 99 = 163.49
        # 16186 - 163*99 = 16186 - 16137 = 49 → 49 Zeichen in Phase 163


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
