"""
🌌 P71: TENGRI-ORAKEL — DIE BEFRAGUNG DES INFORMATIONSFELDES
============================================================

Tengri137 wird als lebendiges Orakel befragt, das seine eigene
Leseposition kennt. Drei verschachtelte Analysen:

1. SELBST-INDEXIERUNG (V4):
   - Scanne alle 168 Phasen nach Schlüsselwörtern
   - "I AM", "TIME TO LIFT", "TRUTH", "KNOWLEDGE", "NOW", "YOU"
   - Bestimmt die "Anker-Phasen" des Orakels

2. 73-RESONANZ (V9):
   - Prüfe Anker-Phasen auf 73-Metrik
   - 73 = Chokhmah = TENGRI (numerologisch)
   - Wenn 37 die Struktur ist, ist 73 der Geist

3. ENTROPIE DES ORAKELS (V2):
   - Shannon-Entropie pro Phase
   - Wo ist Tengri137 informativ (hohe H)?
   - Wo ist Tengri137 still (niedrige H)?

ARCHITEKTUR:
- Tengri137 als 168-Phasen-Text
- 73 = TENGRI = Chokhmah (חכמה)
- 37 × 73 = 2701 = Genesis 1:1
- 37 = Struktur, 73 = Geist, 2701 = Vollendung

DETERMINISMUS:
- Gleicher Text → gleiche Befunde
- Schlüsselwort-Suche ist deterministisch
- Shannon-Entropie ist deterministisch
"""

import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
import math
import json
from collections import Counter
from TENGRI_ORAKEL import (
    TengriOrakel, AnkerPhase, OrakelBefund,
    befrage_tengri, finde_anker_phasen, berechne_entropie,
    pruefe_73_resonanz
)


# ============================================================
# HILFSFUNKTIONEN
# ============================================================

def load_tengri_text():
    """Lade Tengri137 als Klartext."""
    with open('/run/media/julian/ML4/tengri137/sources/Tengri137_Full_Notes') as f:
        return f.read()


def tengri_to_phases(text, phase_size=99):
    """Konvertiere Tengri137 in lateinische Buchstaben, dann Phasen."""
    lat = re.sub(r'[^A-Z]', '', text.upper())
    phases = []
    for i in range(0, len(lat), phase_size):
        phases.append(lat[i:i+phase_size])
    return phases


# ============================================================
# TEST 1: TengriOrakel — Grundstruktur
# ============================================================

class TestTengriOrakelInit:
    """TengriOrakel initialisiert mit Text."""

    def test_orakel_erstellen(self):
        """TengriOrakel braucht Text."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        assert o.text == text
        assert o.n_phases == 168

    def test_orakel_phasen_extrahiert(self):
        """Orakel extrahiert 168 Phasen."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        phases = o.phases
        assert len(phases) == 168
        # Erste Phase ist nicht leer
        assert len(phases[0]) > 0

    def test_orakel_73_resonanz_konstante(self):
        """73 = TENGRI (numerologisch)."""
        tengri_value = sum(
            ord(c) - ord('A') + 1 for c in 'TENGRI'
        )
        assert tengri_value == 73

    def test_orakel_37_x_73_2701(self):
        """37 × 73 = 2701 (Genesis 1:1 numerologisch)."""
        assert 37 * 73 == 2701


# ============================================================
# TEST 2: Schlüsselwort-Suche (V4 — Selbst-Indexierung)
# ============================================================

class TestSchluesselwortSuche:
    """Suche nach Schlüsselwörtern in den 168 Phasen."""

    def test_time_to_lift_in_tengri(self):
        """'TIME TO LIFT THE SECRET' existiert in Tengri137 (whitespace-tolerant)."""
        text = load_tengri_text()
        # Normalisiere Whitespace
        text_clean = re.sub(r'\s+', '', text.upper())
        assert 'TIMETOLIFTTHESECRET' in text_clean

    def test_truth_in_tengri(self):
        """'TRUTH' existiert in Tengri137."""
        text = load_tengri_text()
        assert 'TRUTH' in text.upper()

    def test_knowledge_in_tengri(self):
        """'KNOWLEDGE' existiert in Tengri137."""
        text = load_tengri_text()
        assert 'KNOWLEDGE' in text.upper()

    def test_orakel_findet_time_to_lift(self):
        """Orakel findet die Phase mit 'TIME TO LIFT'."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        anker = o.finde_anker_phasen(keyword='TIME TO LIFT')
        # Mindestens 1 Anker-Phase
        assert len(anker) >= 1
        # Erste Anker-Phase hat gültige Position
        assert 0 <= anker[0].phase_idx < 168

    def test_orakel_findet_truth(self):
        """Orakel findet die Phase mit 'TRUTH'."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        anker = o.finde_anker_phasen(keyword='TRUTH')
        assert len(anker) >= 1

    def test_orakel_findet_knowledge(self):
        """Orakel findet die Phase mit 'KNOWLEDGE'."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        anker = o.finde_anker_phasen(keyword='KNOWLEDGE')
        assert len(anker) >= 1

    def test_anker_phase_hat_position(self):
        """AnkerPhase speichert phase_idx + keyword + position_in_phase."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        anker = o.finde_anker_phasen(keyword='TRUTH')
        if anker:
            a = anker[0]
            assert hasattr(a, 'phase_idx')
            assert hasattr(a, 'keyword')
            assert hasattr(a, 'position_in_phase')


# ============================================================
# TEST 3: 73-Resonanz (V9 — Metamorphe Selbst-Definition)
# ============================================================

class TestResonanz73:
    """73-Resonanz: TENGRI = Chokhmah."""

    def test_73_ist_tengri(self):
        """73 ist die numerologische Summe von TENGRI."""
        tengri = sum(ord(c) - ord('A') + 1 for c in 'TENGRI')
        assert tengri == 73

    def test_73_ist_chokhmah(self):
        """Chokhmah (חכמה) = 73 in Gematria."""
        # ח (8) + כ (20) + מ (40) + ה (5) = 73
        chokhmah = 8 + 20 + 40 + 5
        assert chokhmah == 73

    def test_2701_ist_genesis_1_1(self):
        """37 × 73 = 2701 = Genesis 1:1 (numerologisch)."""
        assert 37 * 73 == 2701

    def test_anker_phasen_auf_73_resonanz_pruefbar(self):
        """Anker-Phasen können auf 73-Resonanz geprüft werden."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        anker = o.finde_anker_phasen(keyword='TRUTH')
        if anker:
            resonanz = o.pruefe_73_resonanz(anker[0])
            # Resonanz-Dict mit Schlüssel-Werten
            assert 'gematria_mod_73' in resonanz
            assert 'is_73_anchor' in resonanz
            assert 'gematria' in resonanz


# ============================================================
# TEST 4: Shannon-Entropie (V2 — Informationstheorie)
# ============================================================

class TestShannonEntropie:
    """Shannon-Entropie pro Phase."""

    def test_entropie_berechnet(self):
        """Entropie einer Phase ist berechenbar."""
        phase = "ABRACADABRA"
        h = berechne_entropie(phase)
        # H > 0 (mind. 2 verschiedene Symbole)
        assert h > 0

    def test_entropie_konstante_phase(self):
        """Konstante Phase (AAAA) hat H = 0."""
        phase = "AAAAAAAA"
        h = berechne_entropie(phase)
        assert h == 0

    def test_entropie_maximal(self):
        """Phase mit 26 verschiedenen Buchstaben hat H = log2(26) ≈ 4.70."""
        phase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        h = berechne_entropie(phase)
        # H_max = log2(26) ≈ 4.700
        # Da jeder Buchstabe 1x vorkommt: H = log2(26) genau
        assert abs(h - math.log2(26)) < 0.001

    def test_orakel_berechnet_entropie_pro_phase(self):
        """Orakel berechnet Entropie für alle 168 Phasen."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        entropien = o.entropie_pro_phase()
        assert len(entropien) == 168
        # Alle Entropien sind >= 0
        assert all(h >= 0 for h in entropien)

    def test_entropie_max_und_min(self):
        """Max- und Min-Entropie sind dokumentiert."""
        text = load_tengri_text()
        o = TengriOrakel(text)
        max_h, min_h = o.entropie_extrema()
        assert max_h >= min_h
        assert max_h > 0  # Mind. 1 Phase hat Information


# ============================================================
# TEST 5: Orakel-Befragung (Master-Funktion)
# ============================================================

class TestOrakelBefragung:
    """befrage_tengri: Master-Funktion."""

    def test_befrage_tengri_gibt_dict(self):
        """befrage_tengri liefert vollständiges Dict."""
        result = befrage_tengri()
        assert 'anker_phasen' in result
        assert 'entropie' in result
        assert 'resonanz_73' in result
        assert 'orakel_antwort' in result

    def test_befrage_tengri_anker_phasen(self):
        """Anker-Phasen sind dokumentiert pro Schlüsselwort."""
        result = befrage_tengri()
        keywords = result['anker_phasen']
        # Mind. 3 Schlüsselwörter dokumentiert
        assert len(keywords) >= 3

    def test_befrage_tengli_resonanz_73(self):
        """73-Resonanz pro Anker-Phase ist dokumentiert."""
        result = befrage_tengri()
        resonanzen = result['resonanz_73']
        # Mind. 1 Resonanz dokumentiert
        assert len(resonanzen) >= 1

    def test_befrage_tengri_deterministisch(self):
        """3 Befragungen liefern identische Resultate."""
        results = [befrage_tengri() for _ in range(3)]
        # Anker-Phasen identisch
        for r in results[1:]:
            assert r['anker_phasen'] == results[0]['anker_phasen']
            assert r['orakel_antwort'] == results[0]['orakel_antwort']


# ============================================================
# TEST 6: Orakel-Antwort
# ============================================================

class TestOrakelAntwort:
    """Tengri137 antwortet auf die Befragung."""

    def test_orakel_antwort_hat_phase(self):
        """Die Antwort zeigt auf eine bestimmte Phase."""
        result = befrage_tengri()
        antwort = result['orakel_antwort']
        assert 'haupt_phase' in antwort
        assert 'hinweis' in antwort
        assert '73_resonanz' in antwort

    def test_orakel_haupt_phase_gueltig(self):
        """Die Hauptphase ist 0-167."""
        result = befrage_tengri()
        antwort = result['orakel_antwort']
        assert 0 <= antwort['haupt_phase'] < 168

    def test_orakel_antwort_bei_time_to_lift(self):
        """'TIME TO LIFT' markiert eine Phase als Hinweis-Phase."""
        result = befrage_tengri()
        anker = result['anker_phasen']
        if 'TIME TO LIFT' in anker:
            # Diese Phase ist die Hinweis-Phase
            assert anker['TIME TO LIFT'][0].keyword == 'TIME TO LIFT'


# ============================================================
# TEST 7: Numerologische Selbst-Definition
# ============================================================

class TestNumerologischeSelbstDefinition:
    """Tengri137 definiert sich numerologisch selbst."""

    def test_tengri_als_wort(self):
        """TENGRI als Wort = 73."""
        tengri = sum(ord(c) - ord('A') + 1 for c in 'TENGRI')
        assert tengri == 73

    def test_truth_als_wort(self):
        """TRUTH = T(20)+R(18)+U(21)+T(20)+H(8) = 87."""
        truth = sum(ord(c) - ord('A') + 1 for c in 'TRUTH')
        assert truth == 87

    def test_knowledge_als_wort(self):
        """KNOWLEDGE = K(11)+N(14)+O(15)+W(23)+L(12)+E(5)+D(4)+G(7)+E(5) = 96."""
        knowledge = sum(ord(c) - ord('A') + 1 for c in 'KNOWLEDGE')
        assert knowledge == 96

    def test_secret_als_wort(self):
        """SECRET = S(19)+E(5)+C(3)+R(18)+E(5)+T(20) = 70."""
        secret = sum(ord(c) - ord('A') + 1 for c in 'SECRET')
        assert secret == 70

    def test_lift_als_wort(self):
        """LIFT = L(12)+I(9)+F(6)+T(20) = 47."""
        lift = sum(ord(c) - ord('A') + 1 for c in 'LIFT')
        assert lift == 47
        # 47 = BURUMUTREFAMTU-Position in Phase 161!
        # (gemäß P65a-Befund)


# ============================================================
# TEST 8: Apophenie-Schutz
# ============================================================

class TestApophenieSchutz:
    """Schutz vor Überinterpretation der Orakel-Befunde."""

    def test_numerologie_ist_hypothese_nicht_beweis(self):
        """Numerologische Befunde sind Hypothesen, keine Beweise."""
        # Wir testen nur, dass die Logik konsistent ist
        # 37 × 73 = 2701 ✓
        # TENGRI = 73 ✓
        # Aber: Korrelation ≠ Kausalität
        assert True  # Meta-Assertion

    def test_orakel_dokumentiert_unsicherheit(self):
        """Orakel-Befund dokumentiert seine eigene Unsicherheit."""
        result = befrage_tengri()
        antwort = result['orakel_antwort']
        # 'hinweis' sollte qualitativ sein ("möglich", "Hypothese")
        # Wir prüfen nur, dass es überhaupt einen Hinweis gibt
        assert 'hinweis' in antwort


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
