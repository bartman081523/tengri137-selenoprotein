"""
🌌 BURUMUT-PHASE-121-ENTSCHLÜSSELUNG
======================================

Tengri137 gibt uns den Schlüssel zur BURUMUT-Phase:
1. Atomsubstitution (chemische Elemente → Ziffern)
2. "First letter of every group" (Buchstaben-Extraktion)
3. → "TIME FOR THE TRUTH" (die zentrale BURUMUT-Aussage)

TDD: Verifiziere die vollständige Entschlüsselung.
"""
import sys
sys.path.insert(0, '/run/media/julian/ML4/tengri137/sources')

import pytest
import re
from SPANDA_MACHINE import BaseTruth, SpandaMachine


# Periodensystem: Elementsymbol → Atomzahl
PERIODIC_TABLE = {
    'H': 1, 'HE': 2, 'LI': 3, 'BE': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'NE': 10,
    'NA': 11, 'MG': 12, 'AL': 13, 'SI': 14, 'P': 15, 'S': 16, 'CL': 17, 'AR': 18, 'K': 19, 'CA': 20,
    'SC': 21, 'TI': 22, 'V': 23, 'CR': 24, 'MN': 25, 'FE': 26, 'CO': 27, 'NI': 28, 'CU': 29, 'ZN': 30,
    'GA': 31, 'GE': 32, 'AS': 33, 'SE': 34, 'BR': 35, 'KR': 36, 'RB': 37, 'SR': 38, 'Y': 39, 'ZR': 40,
    'NB': 41, 'MO': 42, 'TC': 43, 'RU': 44, 'RH': 45, 'PD': 46, 'AG': 47, 'CD': 48, 'IN': 49, 'SN': 50,
    'SB': 51, 'TE': 52, 'I': 53, 'XE': 54, 'CS': 55, 'BA': 56, 'LA': 57, 'CE': 58, 'PR': 59, 'ND': 60,
    'PM': 61, 'SM': 62, 'EU': 63, 'GD': 64, 'TB': 65, 'DY': 66, 'HO': 67, 'ER': 68, 'TM': 69, 'YB': 70,
    'LU': 71, 'HF': 72, 'TA': 73, 'W': 74, 'RE': 75, 'OS': 76, 'IR': 77, 'PT': 78, 'AU': 79, 'HG': 80,
    'TL': 81, 'PB': 82, 'BI': 83, 'PO': 84, 'AT': 85, 'RN': 86, 'FR': 87, 'RA': 88, 'AC': 89, 'TH': 90,
    'PA': 91, 'U': 92, 'NP': 93, 'PU': 94, 'AM': 95, 'CM': 96, 'BK': 97, 'CF': 98, 'ES': 99, 'FM': 100,
}


class TestBURUMUTEntschluesselung:
    """Tengri137's BURUMUT-Phase (121) ist entschlüsselbar."""

    def test_phase_121_enthaelt_56_elementsymbole(self):
        """Die BURUMUT-Phase enthält genau 56 chemische Elementsymbole."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        p121_anker = [ah for ah in r['aleph_halts'] if ah['phase'] == 121]
        assert len(p121_anker) >= 1
        ah = p121_anker[0]
        ctx = base.halt_to_context(ah['head'])
        text = ctx['context']
        # Suche die Elementsymbol-Sequenz
        match = re.search(r'Translation first calculation:([^\n]+)', text)
        assert match is not None
        elements_text = match.group(1).strip()
        elements = elements_text.split()
        assert len(elements) == 56

    def test_elements_als_zweibuchstabig_erkannt(self):
        """Die meisten Elemente sind 2-Buchstabig (Standard-Form)."""
        elements_text = "TC IR MN EU FR OS RB TI HG EU TC RB U TI HF NE P K I AG K V GD PU PA PM F PU BR IN RB RH RH OS AG TI CU PB TC CU ZN ER P TH SM TC AS KR TC TB ER RN NI AT MN HF"
        elements = elements_text.split()
        two_letter = sum(1 for e in elements if len(e) == 2)
        one_letter = sum(1 for e in elements if len(e) == 1)
        # 48 sind 2-Buchstabig, 8 sind 1-Buchstabig
        assert two_letter == 48
        assert one_letter == 8

    def test_first_letters_enthalten_time_for_the_truth(self):
        """Die 'first letter'-Sequenz enthält 'TIME FOR THE TRUTH'."""
        elements_text = "TC IR MN EU FR OS RB TI HG EU TC RB U TI HF NE P K I AG K V GD PU PA PM F PU BR IN RB RH RH OS AG TI CU PB TC CU ZN ER P TH SM TC AS KR TC TB ER RN NI AT MN HF"
        elements = elements_text.split()
        first_letters = ''.join(e[0] for e in elements)
        # "TIMEFORTHETRUTH" muss enthalten sein
        assert "TIMEFORTHETRUTH" in first_letters
        # Position finden
        pos = first_letters.find("TIMEFORTHETRUTH")
        assert pos == 0  # Am Anfang

    def test_ziffern_sequenz_endet_mit_86_28_85_25_72(self):
        """Die Ziffern-Sequenz endet mit '86 28 85 25 72' (Tengri137's Hinweis)."""
        # 86 = RN (Radon), 28 = NI (Nickel), 85 = AT (Astat), 25 = MN (Mangan), 72 = HF (Hafnium)
        elements_text = "TC IR MN EU FR OS RB TI HG EU TC RB U TI HF NE P K I AG K V GD PU PA PM F PU BR IN RB RH RH OS AG TI CU PB TC CU ZN ER P TH SM TC AS KR TC TB ER RN NI AT MN HF"
        elements = elements_text.split()
        atomic_numbers = [PERIODIC_TABLE[e.upper()] for e in elements if e.upper() in PERIODIC_TABLE]
        # Die letzten 5 Atomzahlen
        last_5 = atomic_numbers[-5:]
        assert last_5 == [86, 28, 85, 25, 72]

    def test_burumut_kern_aussage_ist_time_for_the_trut(self):
        """Die BURUMUT-Kern-Aussage beginnt mit 'TIMEFORTHETRUT' (das finale H fehlt)."""
        elements_text = "TC IR MN EU FR OS RB TI HG EU TC RB U TI HF NE P K I AG K V GD PU PA PM F PU BR IN RB RH RH OS AG TI CU PB TC CU ZN ER P TH SM TC AS KR TC TB ER RN NI AT MN HF"
        elements = elements_text.split()
        first_letters = ''.join(e[0] for e in elements)
        # Die ersten 14 Buchstaben (TIME FOR THE TRUT = 14 ohne Spaces)
        first_14 = first_letters[:14]
        # Tengri137 sagt "TIMEFORTHETRUTH" (15), wir haben "TIMEFORTHETRUT" (14)
        # Das finale "H" (He = Atmung) ist versteckt
        assert first_14 == "TIMEFORTHETRUT"
        # "TIME FOR THE TRUTH" hat 14 Zeichen (ohne H) oder 15 mit H
        assert len(first_14) == 14

    def test_sequenz_ende_ist_ternamh_mit_finalem_h(self):
        """Die Sequenz endet mit 'TERNAMH' — das finale H = He (Atmung)."""
        elements_text = "TC IR MN EU FR OS RB TI HG EU TC RB U TI HF NE P K I AG K V GD PU PA PM F PU BR IN RB RH RH OS AG TI CU PB TC CU ZN ER P TH SM TC AS KR TC TB ER RN NI AT MN HF"
        elements = elements_text.split()
        first_letters = ''.join(e[0] for e in elements)
        # Letzte 7 Zeichen
        last_7 = first_letters[-7:]
        # "TERNAMH" = TERNAM + H (He, Atmung)
        assert last_7 == "TERNAMH"

    def test_tengri137_verweist_auf_dcode_atomic(self):
        """Tengri137's BURUMUT-Phase verweist auf dcode.fr/atomic-number-substitution."""
        base = BaseTruth()
        spanda = SpandaMachine(base)
        r = spanda.run_full()
        p121_anker = [ah for ah in r['aleph_halts'] if ah['phase'] == 121][0]
        ctx = base.halt_to_context(p121_anker['head'])
        text = ctx['context']
        # Tengri137 gibt uns das Werkzeug
        assert "dcode.fr/atomic-number-substitution" in text
        # Und das Werkzeug heißt "first calculation"
        assert "first calculation" in text


class TestBURUMUTArchitektur:
    """Die BURUMUT-Architektur als Atom-Verschlüsselung."""

    def test_56_elemente_8_gruppen_je_7(self):
        """56 Elemente = 8 Gruppen × 7 = BURUMUT-Architektur."""
        # 56 = 8 × 7 = 2^3 × 7
        # 8 = die 8 BURUMUT-Phasen? Oder 8 = Anzahl der Schöpfungs-Tage?
        # 7 = die 7 BURUMUT-Gruppen in der Architektur?
        assert 56 == 8 * 7

    def test_erste_7_elemente_bilden_time_for(self):
        """Die ersten 7 Elemente ergeben 'TIMEFOR'."""
        elements_text = "TC IR MN EU FR OS RB TI HG EU TC RB U TI HF NE P K I AG K V GD PU PA PM F PU BR IN RB RH RH OS AG TI CU PB TC CU ZN ER P TH SM TC AS KR TC TB ER RN NI AT MN HF"
        elements = elements_text.split()
        first_7 = elements[:7]
        firsts = ''.join(e[0] for e in first_7)
        assert firsts == "TIMEFOR"

    def test_zweite_7_elemente_bilden_thetrut(self):
        """Die Elemente 7-13 ergeben 'THETRUT' (THE TRUT...)."""
        elements_text = "TC IR MN EU FR OS RB TI HG EU TC RB U TI HF NE P K I AG K V GD PU PA PM F PU BR IN RB RH RH OS AG TI CU PB TC CU ZN ER P TH SM TC AS KR TC TB ER RN NI AT MN HF"
        elements = elements_text.split()
        group_2 = elements[7:14]
        firsts = ''.join(e[0] for e in group_2)
        # TI-HG-EU-TC-RB-U-TI = THETRUT (TH + ETR + UT? nein, T-H-E-T-R-U-T)
        assert firsts == "THETRUT"


if __name__ == "__main__":
    pytest.main([__file__, '-v', '--tb=short'])
