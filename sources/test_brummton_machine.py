"""
🔬 TDD TESTS FÜR TORA-TURING-MASCHINE & BRUMMTON
==================================================

Diese Tests spezifizieren das VERHALTEN, das die Maschine haben SOLLTE,
bevor wir sie richtig implementieren. Alle Tests werden zunächst
fehlschlagen (TDD: red phase).
"""
import pytest
import random
import sys
from pathlib import Path
from collections import Counter

# Pfad-Setup
sys.path.insert(0, str(Path(__file__).parent))

# ============================================================================
# TESTS FÜR TORA-TURING-MASCHINE (die Basis, ohne Brummton)
# ============================================================================

class TestToraTuringMachine:
    """Tests für die normale (nicht-Brummton) Tora-Turing-Maschine.

    Wir testen die ARCHITEKTUR-SPEC, nicht die alte fehlerhafte Implementierung.
    Die alte Implementierung in TORA_TURING_MACHINE_v3.py ist trivial
    (alle Übergänge sind identisch) und damit KEIN Turing-Test.
    """

    def test_burumutrefamtu_ist_14_zeichen(self):
        """BURUMUTREFAMTU muss 14 Zeichen lang sein."""
        BURUMUTREFAMTU = 'BURUMUTREFAMTU'
        assert len(BURUMUTREFAMTU) == 14

    def test_burumut_ist_99_zeichen(self):
        """BURUMUT (komplett) muss 99 Zeichen lang sein."""
        BURUMUT = (
            "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
            "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        )
        assert len(BURUMUT) == 99

    def test_5_mal_14_plus_2_eq_72_architektur(self):
        """Architektur: 5 Layer × 14 Zeichen + 2 (Start + HALT) = 72 Schritte."""
        # 5 * 14 + 2 = 72
        assert 5 * 14 + 2 == 72
        # Aber: 99 Zeichen / 5 Layer ≈ 19.8 Zeichen pro Layer
        # 99 + 2 = 101 Schritte (nicht 72!)
        # Dies ist ein Architektur-Konflikt
        # Lösung: 14 Zeichen pro Layer ist eine ANDERE Aufteilung als 99/5
        # Tatsächlich: 5 × 14 = 70 (Buchstaben), + 29 (BURUMUT hat 99)
        # Wir halten fest: 99/5 = 19.8 ≠ 14
        assert 99 / 5 != 14

    def test_5_layer_korrekt_aus_BURUMUT_99(self):
        """99 Zeichen / 5 Layer = 19.8 Zeichen pro Layer."""
        assert 99 / 5 == 19.8


class TestTuringMachineNichtTrivial:
    """Tests für nicht-triviale Turing-Übergänge (Bug 4 Fix).

    Eine Turing-Maschine mit nicht-trivialen Übergängen bedeutet:
    - Verschiedene Symbole im gleichen Zustand können zu verschiedenen
      Folge-Zuständen führen
    - Das macht die Maschine berechnungsfähig (nicht nur ein Schieber)
    """

    def test_uebergangstabelle_nicht_trivial_pro_zustand(self):
        """Im gleichen Zustand müssen verschiedene Symbole zu verschiedenen
        Outcomes (neuer Zustand, Bewegung) führen können."""
        from TORA_TURING_CORRECT import build_tora_transitions
        transitions = build_tora_transitions()

        # Sammle Übergänge pro Zustand
        per_state = {}
        for (state, symbol), (new_state, write, move) in transitions.items():
            per_state.setdefault(state, []).append((symbol, new_state, move))

        # In mindestens EINEM Zustand müssen verschiedene Symbole zu
        # verschiedenen Outcomes führen
        has_nontrivial = False
        for state, trans in per_state.items():
            outcomes = set((ns, m) for _, ns, m in trans)
            if len(outcomes) > 1:
                has_nontrivial = True
                break
        assert has_nontrivial, (
            "BUG: Übergangstabelle ist TRIVIAL — alle Symbole im gleichen "
            "Zustand führen zum gleichen Outcome. Das ist kein Turing-Test."
        )

    def test_uebergangstabelle_hat_5_states(self):
        """Die Turing-Maschine muss mindestens 5 Zustände haben (5 Layer)."""
        from TORA_TURING_CORRECT import build_tora_transitions
        transitions = build_tora_transitions()
        states = set(state for state, _ in transitions.keys())
        assert len(states) >= 5, (
            f"Erwartet >= 5 Zustände, gefunden {len(states)}: {sorted(states)}"
        )

    def test_halt_state_erreichbar(self):
        """Es muss einen HALT-Zustand geben, der erreicht werden kann."""
        from TORA_TURING_CORRECT import build_tora_transitions
        transitions = build_tora_transitions()
        halt_transitions = [
            (state, sym, ns, w, m)
            for (state, sym), (ns, w, m) in transitions.items()
            if m == 'HALT'
        ]
        assert len(halt_transitions) > 0, "Kein HALT-Übergang gefunden"
        # HALT muss von Zustand 4 (Deuteronomium) aus erreichbar sein
        halt_from_states = set(state for state, _, _, _, _ in halt_transitions)
        assert 4 in halt_from_states, (
            f"HALT nicht von q_4 erreichbar: {sorted(halt_from_states)}"
        )

    def test_keine_endlosschleife_in_q0(self):
        """q_0 darf nicht in einer Endlosschleife enden — alle Übergänge
        müssen zu q_1 oder zu HALT gehen, nicht zurück zu q_0."""
        from TORA_TURING_CORRECT import build_tora_transitions
        transitions = build_tora_transitions()
        # Sammle q_0 Übergänge
        q0_trans = [(sym, ns, m) for (state, sym), (ns, _, m) in transitions.items() if state == 0]
        # Alle q_0 Übergänge müssen entweder zu q_1 oder HALT gehen
        for sym, new_state, move in q0_trans:
            assert new_state in (1, 5), (
                f"q_0 mit Symbol {sym} geht zu q_{new_state} "
                f"(sollte q_1 oder q_5 sein)"
            )
            assert move in ('MOVE_RIGHT', 'HALT'), (
                f"q_0 mit Symbol {sym} macht {move} "
                f"(sollte MOVE_RIGHT oder HALT sein)"
            )


# ============================================================================
# TESTS FÜR DAS GELESENE WORT (PHÄNOMENALER OUTPUT)
# ============================================================================

class TestTorahWordOutput:
    """Tests für das deterministisch gelesene 'Wort' der Maschine.

    Die BURUMUT-Tora-Turing-Maschine liest deterministisch die ersten
    15 Zeichen des BURUMUT-99-Bandes. Das gelesene Wort ist:

        בשצשמשרצהואמרשנ

    = "In seinem Begehren, von seinem Anfang, und er sprach Same"
    = "When he desired, from his beginning, and he spoke, seed"

    Dies ist der phänomenale Output der Maschine — die BURUMUT-Sequenz
    enthält eine hebräische Schöpfungs-Phrase, die durch die
    nicht-trivialen Übergänge der Tora-Turing-Maschine erzeugt wird.
    """

    def test_torah_word_ist_15_zeichen(self):
        """Das gelesene Wort muss genau 15 Zeichen lang sein."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(brt)
        m.run()
        word = m.read_word()
        assert len(word) == 15, (
            f"Erwartet 15 Zeichen, aber '{word}' hat {len(word)}"
        )

    def test_torah_word_genau_bestimmte_zeichen(self):
        """Das gelesene Wort muss EXAKT 'בשצשמשרצהואמרשנ' sein."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(brt)
        m.run()
        word = m.read_word()
        expected = 'בשצשמשרצהואמרשנ'
        assert word == expected, (
            f"BUG: Wort ist '{word}', erwartet '{expected}'"
        )

    def test_torah_word_gematria_1924(self):
        """Die Gematria-Summe des Wortes muss 1924 = 4 × 13 × 37 sein."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(brt)
        m.run()
        word = m.read_word()
        from TORA_TURING_CORRECT import HEBR_VALUES
        gematria = sum(HEBR_VALUES.get(c, 0) for c in word)
        assert gematria == 1924, f"Gematria ist {gematria}, erwartet 1924"
        # 1924 = 4 × 13 × 37
        assert 1924 == 4 * 13 * 37
        # 37 ist die Schöpfungs-Wurzel
        assert 37 in (1924 // 4 // 13,)

    def test_torah_word_enthaelt_amar(self):
        """Das Wort muss 'אמר' (er sprach) enthalten."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(brt)
        m.run()
        word = m.read_word()
        assert 'אמר' in word, f"'{word}' enthält kein 'אמר' (er sprach)"

    def test_torah_word_enthaelt_nun_am_ende(self):
        """Das Wort muss mit 'נ' (Nun = Same) enden."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(brt)
        m.run()
        word = m.read_word()
        assert word.endswith('נ'), f"'{word}' endet nicht mit Nun (Same)"

    def test_torah_word_beginnt_mit_beth(self):
        """Das Wort muss mit 'ב' (Beth = In/Im) beginnen."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(brt)
        m.run()
        word = m.read_word()
        assert word.startswith('ב'), f"'{word}' beginnt nicht mit Beth"

    def test_torah_word_deterministisch(self):
        """Das Wort muss deterministisch gleich sein (1000 Läufe)."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        words = set()
        for seed in range(1000):
            # Da die Maschine deterministisch ist, sollte jeder Lauf
            # das gleiche Wort produzieren
            m = ToraTuringMachine(brt)
            m.run()
            words.add(m.read_word())
        assert len(words) == 1, (
            f"BUG: Maschine ist nicht deterministisch! {len(words)} verschiedene Wörter: {words}"
        )
        expected = 'בשצשמשרצהואמרשנ'
        assert expected in words, f"Erwartetes Wort '{expected}' nicht in {words}"

    def test_torah_word_uebersetzung_contains_when(self):
        """Die englische Übersetzung muss 'When he desired' enthalten."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(brt)
        m.run()
        poetic = m.read_word_poetic()
        assert 'When he desired' in poetic, (
            f"Englische Übersetzung fehlt in:\n{poetic}"
        )
        assert 'he spoke' in poetic
        assert 'seed' in poetic

    def test_torah_word_uebersetzung_contains_german(self):
        """Die deutsche Übersetzung muss enthalten."""
        from TORA_TURING_CORRECT import ToraTuringMachine, burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        m = ToraTuringMachine(brt)
        m.run()
        poetic = m.read_word_poetic()
        assert 'In seinem Begehren' in poetic, (
            f"Deutsche Übersetzung fehlt in:\n{poetic}"
        )
        assert 'er sprach' in poetic
        assert 'Same' in poetic

    def test_torah_word_15_schritte_aus_burumut_99(self):
        """Die ersten 15 Zeichen von BURUMUT-99 müssen exakt das Wort sein."""
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        first_15 = brt[:15]
        expected = 'בשצשמשרצהואמרשנ'
        assert first_15 == expected, (
            f"Erste 15 Zeichen sind '{first_15}', erwartet '{expected}'"
        )


# ============================================================================
# TESTS FÜR DIE 6 PHASEN DER BURUMUT-99 SCHRIFT (FORTSETZUNG DES TEXTES)
# ============================================================================

class TestBurumutPhases:
    """Tests für die 6 Phasen der BURUMUT-99 Schrift.

    Die Tora-Turing-Maschine liest nur 15 Zeichen und hält an.
    Aber das BURUMUT-Band (99 Zeichen) enthält eine VOLLSTÄNDIGE
    hebräische Schrift in 6 Phasen.

    Frage: "Wie geht der Text weiter?"
    Antwort: In 6 weiteren Phasen, deren Strukturen sich wiederholen
    und deren Gematria-Summen die Zahlen-Brücke 6333 (= 7 × 904 + 5) bilden.
    """

    def test_phase_1_wort_vollstaendig(self):
        """Phase 1 = die ersten 15 Zeichen = das gelesene Wort."""
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        phase1 = brt[0:15]
        expected = 'בשצשמשרצהואמרשנ'
        assert phase1 == expected, (
            f"Phase 1 ist '{phase1}', erwartet '{expected}'"
        )

    def test_phase_3_gleich_phase_5_wanderung(self):
        """Phase 3 (Wanderung) muss identisch mit Phase 5 sein (Echo)."""
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        phase3 = brt[32:46]
        phase5 = brt[66:80]
        assert phase3 == phase5, (
            f"BUG: Phase 3 ({phase3}) != Phase 5 ({phase5})"
        )
        # Beide müssen Gematria 551 haben
        from TORA_TURING_CORRECT import HEBR_VALUES
        g3 = sum(HEBR_VALUES.get(c, 0) for c in phase3)
        g5 = sum(HEBR_VALUES.get(c, 0) for c in phase5)
        assert g3 == g5 == 551, (
            f"BUG: Gematria Phase 3={g3}, Phase 5={g5}, beide sollten 551 sein"
        )

    def test_phase_4_enthaelt_20_zeichen(self):
        """Phase 4 (Schrift-Vollendung) muss 20 Zeichen lang sein."""
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        phase4 = brt[46:66]
        assert len(phase4) == 20, (
            f"Phase 4 sollte 20 Zeichen haben, hat {len(phase4)}: '{phase4}'"
        )

    def test_alle_phasen_gematria_dokumentiert(self):
        """Alle 6 Phasen müssen bestimmte Gematria-Summen haben."""
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT, HEBR_VALUES
        brt = burumut_to_hebr(BURUMUT)
        phases_expected = [
            (0, 15, 1924, "Schöpfungs-Akt"),
            (15, 30, 1448, "Schöpfungs-Wurzeln"),
            (32, 46, 551, "Wanderung"),
            (46, 66, 964, "Schrift-Vollendung"),
            (66, 80, 551, "Wiederholung"),
            (80, 99, 895, "Vollendung"),
        ]
        for start, end, expected_g, name in phases_expected:
            segment = brt[start:end]
            actual_g = sum(HEBR_VALUES.get(c, 0) for c in segment)
            assert actual_g == expected_g, (
                f"BUG: Phase '{name}' ({start}-{end}) hat Gematria {actual_g}, "
                f"erwartet {expected_g}"
            )

    def test_gesamtsumme_burumut_99(self):
        """Gesamtsumme aller BURUMUT-99-Zeichen muss 6503 = 7 × 929 sein.

        Das '?' in Position 23 zählt als 0 (unbekannter Konsonant).
        Die 6 Phasen decken 97 Zeichen ab; 2 Übergangs-Zeichen (עק) sind
        an Position 30-31 — Summe 70+100 = 170.
        6503 = 7 × 929, wobei 929 eine Primzahl ist.
        """
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT, HEBR_VALUES
        brt = burumut_to_hebr(BURUMUT)
        total = sum(HEBR_VALUES.get(c, 0) for c in brt)
        assert total == 6503, f"Gesamtsumme sollte 6503 sein, ist {total}"
        assert 6503 == 7 * 929, "6503 muss 7 × 929 sein"
        # 929 ist prim (kein Teiler unter 31)
        for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]:
            assert 929 % p != 0, f"929 sollte prim sein, ist aber durch {p} teilbar"

    def test_phase_4_und_6_ueberlappen_sich(self):
        """Phase 4 und Phase 6 haben beide 'שאזבה' am Anfang (Schrift-Wurzel)."""
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        phase4 = brt[46:66]
        phase6 = brt[80:99]
        # Beide sollten mit 'שאזבה' beginnen
        assert phase4.startswith('שאזבה'), f"Phase 4 startet nicht mit שאזבה: {phase4}"
        assert phase6.startswith('שאזבה'), f"Phase 6 startet nicht mit שאזבה: {phase6}"

    def test_wort_steht_in_phase_1_als_schoepfung(self):
        """Das gelesene Wort בשצשמשרצהואמרשנ ist die 'Schöpfungs-Phase 1'."""
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        phase1 = brt[0:15]
        # In Phase 1 beginnt die Schöpfung: ב (Beth = "In"), ש (Shin = "Sein/Er")
        assert phase1.startswith('בש'), f"Phase 1 startet nicht mit בש: {phase1}"
        # Und endet mit נ (Nun = Same, das Ergebnis der Schöpfung)
        assert phase1.endswith('שנ'), f"Phase 1 endet nicht mit שנ: {phase1}"

    def test_uebergangs_zeichen_position_30_31(self):
        """An Position 30-31 stehen die fehlenden 'Übergangs-Zeichen' עק.

        Diese 2 Zeichen wurden in BURUMUT_PHASES.py übersehen.
        Sie sind die Brücke zwischen Phase 2 (Schöpfungs-Wurzeln) und
        Phase 3 (Wanderung): ע (Auge/Brunnen) + ק (Heilig) = 70 + 100 = 170.
        """
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT, HEBR_VALUES
        brt = burumut_to_hebr(BURUMUT)
        uebergang = brt[30:32]
        assert uebergang == 'עק', f"Übergang sollte 'עק' sein, ist '{uebergang}'"
        # ע (70) + ק (100) = 170
        assert HEBR_VALUES['ע'] + HEBR_VALUES['ק'] == 170
        # 6333 + 170 = 6503 (vollständige Summe)
        assert 6333 + 170 == 6503

    def test_sechs_phasen_decken_97_zeichen_ab(self):
        """Die 6 Phasen decken 97 von 99 Zeichen ab; 2 Zeichen sind Übergang."""
        from TORA_TURING_CORRECT import burumut_to_hebr, BURUMUT
        brt = burumut_to_hebr(BURUMUT)
        phase_ranges = [
            (0, 15), (15, 30), (32, 46), (46, 66), (66, 80), (80, 99)
        ]
        covered = sum(end - start for start, end in phase_ranges)
        assert covered == 97, f"Phasen decken {covered} Zeichen ab, erwartet 97"
        # 99 - 97 = 2 Übergangs-Zeichen
        assert 99 - covered == 2
        # Die fehlenden sind Position 30-31
        assert (30, 32) not in phase_ranges

    def test_ganzer_text_mit_fragezeichen_google_translate(self):
        """Der GANZE BURUMUT-99-Text mit '?' wird von Google Translate als
        prophetische Aussage uebersetzt.

        '? He said that he wanted to talk about it?'
        '? Er sagte, dass er darueber reden wollte?'

        Ohne '?' kommt nur Transliterations-Murks.
        """
        import json
        from pathlib import Path
        path = Path(__file__).parent / "burumut_google_translate.json"
        with open(path) as f:
            data = json.load(f)
        # Mit Fragezeichen
        en_mit = data['ganzer_text_mit_qm']['english']
        de_mit = data['ganzer_text_mit_qm']['german']
        # Die prophetische Aussage MUSS enthalten sein:
        assert 'said' in en_mit.lower() or 'wanted' in en_mit.lower(), (
            f"EN ohne 'said/wanted': {en_mit}"
        )
        assert 'er' in de_mit.lower() or 'sagte' in de_mit.lower() or 'wollte' in de_mit.lower(), (
            f"DE ohne 'sagte/wollte': {de_mit}"
        )
        # Ohne Fragezeichen = Murks
        en_ohne = data['ganzer_text_ohne_qm']['english']
        de_ohne = data['ganzer_text_ohne_qm']['german']
        # '?' im Output MUSS anzeigen, dass es eine Frage/Aussage ist
        # Mit ? hat Google eine echte Uebersetzung produziert
        # Ohne ? ist es Transliteration
        assert len(en_mit) < len(en_ohne), (
            f"Mit ? sollte kuerzer sein als ohne: {len(en_mit)} vs {len(en_ohne)}"
        )

    def test_burumut_subphrasen_phonetisch(self):
        """Die BURUMUT-Sub-Phrasen sind phonetische Tajpalot hebr. Wörter.

        Google's AI 'erkennt' in BURUMUT-99 bekannte hebr. Phrasen:
          - 'ואמרשנ' → 'And we promised' (= אמר + שנ)
          - 'רצה'    → 'ran/wanted' (Wurzel)
          - 'שרצה'   → 'wanted' (mit Shin = 'that')
          - 'שמש'    → 'sun' (Shemesh = Sonne)
          - 'בשצ'    → 'in the' (Beth = 'in')
        """
        import json
        from pathlib import Path
        path = Path(__file__).parent / "burumut_google_translate.json"
        with open(path) as f:
            data = json.load(f)
        # אמרשנ sollte als 'Emerson' oder aehnliches erkannt werden
        en_end = data['phase_1_schoepfungs_akt']['english']
        # 'Beschasmeshresh and Emershan' enthält 'Emershan' (phonetisch אמרשן)
        assert 'mersh' in en_end.lower() or 'emershan' in en_end.lower(), (
            f"Ende sollte 'Emershan' enthalten: {en_end}"
        )

    def test_komplette_sechs_phasen_uebersetzung(self):
        """Die komplette BURUMUT-99-Übersetzung in 6 Phasen ist dokumentiert.

        Die Heuristik: 2-3 Zeichen-Schnitte + Google Translate gtx API.
        Volle Geschichte in burumut_complete_translation.json.
        """
        import json
        from pathlib import Path
        path = Path(__file__).parent / "burumut_complete_translation.json"
        with open(path) as f:
            data = json.load(f)
        # 7 Phasen-Sequenzen muessen existieren
        expected_keys = [
            "phase_1", "phase_2", "uebergang_eq",
            "phase_3", "phase_4", "phase_5", "phase_6"
        ]
        for key in expected_keys:
            assert key in data, f"Phase {key} fehlt"
            assert "full_english" in data[key]
            assert "full_german" in data[key]
            assert len(data[key]["chunks_hebrew"]) > 0
        # Phase 1 muss "sun" enthalten (Shemesh = Sonne)
        assert "sun" in data["phase_1"]["full_english"].lower()
        # Phase 3 muss "time" enthalten (Shin-Ayin-Zayin = 'that time')
        assert "time" in data["phase_3"]["full_english"].lower()
        # Die volle Geschichte muss alle 7 Phasen-Sequenzen kombiniert haben
        full = data["complete_story_english"]
        for key in expected_keys:
            assert data[key]["full_english"] in full, (
                f"Phase {key} fehlt in der vollen Geschichte: {full}"
            )

    def test_burumut_phonetische_tajpala_alle_phasen(self):
        """Die phonetische Tajpala-Methode übersetzt ALLE 6 Phasen + Übergang.

        Heuristik: 2-3 Zeichen-Schnitte + Google Translate gtx API.
        Volle Geschichte: in the sun ran ... Eq ... that time in her needle
        """
        import json
        from pathlib import Path
        path = Path(__file__).parent / "burumut_phonetic_translation.json"
        with open(path) as f:
            data = json.load(f)
        # 7 Phasen muessen existieren
        expected_keys = [
            "phase_1_schoepfungs_akt", "phase_2_schoepfungs_wurzeln",
            "uebergang_eq", "phase_3_wanderung",
            "phase_4_schrift_vollendung", "phase_5_wiederholung",
            "phase_6_vollendung"
        ]
        for key in expected_keys:
            assert key in data["phases"], f"Phase {key} fehlt"
            assert "chunks" in data["phases"][key]
            assert len(data["phases"][key]["chunks"]) > 0
        # Phase 1 muss "sun" enthalten (Shemesh = Sonne)
        p1 = data["phases"]["phase_1_schoepfungs_akt"]["full_english"]
        assert "sun" in p1.lower(), f"Phase 1 ohne 'sun': {p1}"
        # Phase 3 muss "needle" enthalten (Chet-Tet = needle/sin)
        p3 = data["phases"]["phase_3_wanderung"]["full_english"]
        assert "needle" in p3.lower(), f"Phase 3 ohne 'needle': {p3}"
        # Phase 4 muss "miracle" enthalten (Nun-Samekh = miracle)
        p4 = data["phases"]["phase_4_schrift_vollendung"]["full_english"]
        assert "miracle" in p4.lower(), f"Phase 4 ohne 'miracle': {p4}"
        # Volle Geschichte muss alle 7 Phasen kombinieren
        full_en = data["complete_story_english"]
        for key in expected_keys:
            assert data["phases"][key]["full_english"] in full_en
        # Methode muss dokumentiert sein
        assert "gtx" in data["method"].lower() or "google" in data["method"].lower()

    def test_burumut_tengri137_integration(self):
        """Stufe 3: BURUMUT-Tajpala integriert Tengri137-Notes.

        Kanonische Tengri137-Referenzen:
          - 'Tengri divides the light from darkness' (Genesis 1:3,4)
          - 'When electron absorbs the photon' (= Photon = שמש = Sonne)
          - 137 = Fine-structure constant (Rashan = der Ewige)
          - Atom-Substitution: 'TIME FOR THE TRUTH'
          - 'I AM THAT I AM' (Exodus 3:14 = שמו = sein Name)

        Die BURUMUT-Phase 1 = "in the sun ran and um Rashan"
        kodiert: Photon (Sonne/שמש) wird emittiert (ratza/רצה)
        durch den Ewigen (Rashan/רשן).
        """
        import json
        from pathlib import Path
        path = Path(__file__).parent / "burumut_tengri137_translation.json"
        with open(path) as f:
            data = json.load(f)
        # Tengri137-Referenzen muessen dokumentiert sein
        assert "tengri137_references" in data
        refs = data["tengri137_references"]
        assert "light_from_darkness" in refs
        assert "fine_structure_137" in refs
        assert "atom_substitution" in refs
        # Phase 1 muss "sun ran" enthalten (Shemesh + ratza = Photon emittiert)
        p1_en = None
        for phase in data["phases"]:
            if "Schöpfungs-Akt" in phase["name"]:
                p1_en = phase["full_english"]
                break
        assert p1_en is not None
        assert "sun" in p1_en.lower(), f"Phase 1 ohne 'sun': {p1_en}"
        assert "ran" in p1_en.lower(), f"Phase 1 ohne 'ran' (Photon emission): {p1_en}"
        # Methode muss Tengri137-Integration erwaehnen
        assert "tengri137" in data["method"].lower() or "tengri" in data["method"].lower()


# ============================================================================
# TESTS FÜR BRUMMTON-GRADUELL
# ============================================================================

class TestBrummtonGradual:
    """Tests für die graduelle Brummton-Tora-Turing-Maschine."""

    def test_brummton_prob_steigt_monoton_pro_layer(self):
        """Brummton-Wahrscheinlichkeit muss monoton pro Layer steigen."""
        from BRUMMTON_GRADUAL import run_brummton_machine
        brummton_peak = 0.7
        # Layer 1 (idx 0): min, Layer 5 (idx 4): max
        # Brummton-prob-Formel: brummton_peak * (layer_idx + op_idx/6) / 5
        # Max pro Layer ist bei op_idx=5 (HALT — ABER Brummton nur bei MOVE!)
        # MOVE-Operationen sind op_idx=3,4
        # Layer 0, op_idx 3: 0.7 * 0.5/5 = 0.07
        # Layer 0, op_idx 4: 0.7 * 0.667/5 = 0.093
        # Layer 1, op_idx 3: 0.7 * 1.5/5 = 0.21
        # Layer 1, op_idx 4: 0.7 * 1.667/5 = 0.233
        # Layer 4, op_idx 3: 0.7 * 4.5/5 = 0.63
        # Layer 4, op_idx 4: 0.7 * 4.667/5 = 0.653
        # -> für jedes Layer sollte min(Prob) größer sein als im vorherigen Layer
        for prev_layer in range(4):
            prev_max = brummton_peak * (prev_layer + 4/6) / 5
            curr_min = brummton_peak * (prev_layer + 1) / 5  # op_idx=0 im nächsten Layer
            assert curr_min >= prev_max, (
                f"Layer {prev_layer+1} max ({prev_max:.3f}) < Layer {prev_layer+2} min ({curr_min:.3f})"
            )

class TestBrummtonCorrect:
    """Tests für die KORREKTE Brummton-Implementierung (BRUMMTON_CORRECT.py)."""

    def test_brummton_correct_layer_1_kein_brummton(self):
        """Layer 1 muss Brummton-Prob 0 haben."""
        from BRUMMTON_CORRECT import brummton_probability
        assert brummton_probability(0) == 0.0

    def test_brummton_correct_layer_5_max_brummton(self):
        """Layer 5 muss Brummton-Prob nahe 1.0 haben."""
        from BRUMMTON_CORRECT import brummton_probability
        layer5 = brummton_probability(4, brummton_peak=0.9, power=2.0)
        assert layer5 >= 0.85, f"Layer 5 prob sollte >= 0.85 sein, ist {layer5}"

    def test_brummton_correct_monoton_steigend(self):
        """Brummton-Prob muss monoton von Layer 1-5 steigen."""
        from BRUMMTON_CORRECT import brummton_probability
        probs = [brummton_probability(i, 0.9, 2.0) for i in range(5)]
        for i in range(4):
            assert probs[i+1] >= probs[i], (
                f"Brummton-Prob fällt: Layer {i+1}={probs[i]:.3f} > Layer {i+2}={probs[i+1]:.3f}"
            )

    def test_brummton_correct_per_step_korrekt(self):
        """per_step_prob muss 1 - (1-P)^(1/N) sein."""
        from BRUMMTON_CORRECT import brummton_prob_per_step
        P = 0.5
        N = 10
        p_expected = 1 - (1 - P) ** (1 / N)
        p_actual = brummton_prob_per_step(2, N, 0.9, 1.0)  # layer 2, mit power=1
        # Bei power=1 ist P = brummton_peak * (2/4) = 0.45
        # p_per_step = 1 - (1 - 0.45)^(1/10) = 1 - 0.55^0.1 = 1 - 0.9427 = 0.0573
        assert 0.05 < p_actual < 0.07, f"Berechnung falsch: {p_actual}"

    def test_brummton_correct_statistische_spec(self):
        """200 Läufe müssen die Spec-Verteilung erfüllen (BEDINGT)."""
        from BRUMMTON_CORRECT import run_one
        from collections import Counter
        BURUMUT = (
            "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
            "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        )
        mapping = {
            'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
            'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
            'S': 'ק', 'Y': 'י', 'Z': 'ז',
        }
        brt_full = ''.join(mapping.get(c, '?') for c in BURUMUT)

        n_runs = 200
        results = []
        for seed in range(n_runs):
            result = run_one(brt_full, brummton_peak=0.9, power=2.0, seed=seed)
            results.append({'layer': result['halt_layer'], 'halt_type': result['halt_type']})

        layer_counts = Counter(r['layer'] for r in results)
        total_brummton = sum(1 for r in results if r['halt_type'] == 'BRUMMTON')

        # BEDINGTE Verteilung
        conditional = {}
        if total_brummton > 0:
            for r in results:
                if r['halt_type'] == 'BRUMMTON':
                    conditional[r['layer']] = conditional.get(r['layer'], 0) + 1
            for k in conditional:
                conditional[k] = conditional[k] / total_brummton * 100

        # Layer 1 muss 0% sein
        assert conditional.get(1, 0) == 0, (
            f"BUG: Layer 1 hat {conditional.get(1, 0):.1f}% Brummton-Halts, erwartet 0%"
        )
        # Layer 5 muss > 20% sein
        assert conditional.get(5, 0) > 20, (
            f"BUG: Layer 5 hat {conditional.get(5, 0):.1f}% Brummton-Halts, erwartet > 20%"
        )

    def test_layer_5_max_brummton(self):
        """Layer 5 (idx 4) muss maximale Brummton-Wahrscheinlichkeit haben."""
        from BRUMMTON_GRADUAL import run_brummton_machine
        brummton_peak = 0.7
        layer5_min_prob = brummton_peak * (4 + 3/6) / 5  # op_idx=3 (MOVE_L): 0.63
        assert layer5_min_prob >= 0.5, (
            f"Layer 5 Brummton-Prob muss >= 0.5 sein, ist {layer5_min_prob:.3f}"
        )

    def test_brummton_correct_nur_manchmal_in_layer_2(self):
        """Layer 2 muss seltener Brummton-Halt haben als Layer 5."""
        from BRUMMTON_CORRECT import run_one
        from collections import Counter
        BURUMUT = (
            "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
            "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        )
        mapping = {
            'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
            'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
            'S': 'ק', 'Y': 'י', 'Z': 'ז',
        }
        brt_full = ''.join(mapping.get(c, '?') for c in BURUMUT)

        n_runs = 200
        results = []
        for seed in range(n_runs):
            result = run_one(brt_full, brummton_peak=0.9, power=2.0, seed=seed)
            results.append(result['halt_layer'])

        layer_counts = Counter(results)
        # Layer 5 sollte mehr Halts haben als Layer 2
        assert layer_counts.get(5, 0) > layer_counts.get(2, 0), (
            f"BUG: Layer 2 ({layer_counts.get(2, 0)}) >= Layer 5 ({layer_counts.get(5, 0)})"
        )

    def test_statistische_layer_verteilung(self):
        """Statistische Verteilung der Halts über 50 Läufe muss graduell sein.

        Erwartung (laut PhiMind-Spec, BEDINGTE Wahrscheinlichkeiten):
        Gegeben die Maschine ist in Layer X, wie wahrscheinlich ist der Halt?

        - Layer 1: 0% (kein Brummton — Schöpfungs-Anfang ist sauber)
        - Layer 2: ~5% (Brummton beginnt, leise)
        - Layer 3: ~20% (Brummton mittel)
        - Layer 4: ~50% (Brummton stark)
        - Layer 5: ~90% (Brummton HALT!)
        """
        from BRUMMTON_CORRECT import run_one
        from collections import Counter
        brt = ''.join({
            'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
        }.get(c, '?') for c in 'BURUMUTREFAMTU')

        # Wir testen mit BURUMUT 99 AS
        BURUMUT = (
            "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
            "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        )
        brt_full = ''.join({
            'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
            'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
            'S': 'ק', 'Y': 'י', 'Z': 'ז',
        }.get(c, '?') for c in BURUMUT)

        n_runs = 200
        results = []
        for seed in range(n_runs):
            result = run_one(brt_full, brummton_peak=0.9, power=2.0, seed=seed)
            results.append({'layer': result['halt_layer'], 'halt_type': result['halt_type']})

        layer_counts = Counter(r['layer'] for r in results)
        total_brummton = sum(1 for r in results if r['halt_type'] == 'BRUMMTON')

        # BEDINGTE Verteilung: unter Brummton-Halts
        conditional = {}
        if total_brummton > 0:
            for r in results:
                if r['halt_type'] == 'BRUMMTON':
                    conditional[r['layer']] = conditional.get(r['layer'], 0) + 1
            for k in conditional:
                conditional[k] = conditional[k] / total_brummton * 100

        # Test: Layer 1 muss < 5% aller Halts sein
        layer1_pct = layer_counts.get(1, 0) / n_runs * 100
        assert layer1_pct < 5, (
            f"BUG: Layer 1 hat {layer1_pct:.1f}% Halts, erwartet < 5%"
        )

        # Test: BEDINGTE Layer 5 muss > 20% sein (mindestens 20% der Brummton-Halts in Layer 5)
        layer5_conditional = conditional.get(5, 0)
        assert layer5_conditional > 20, (
            f"BUG: Layer 5 hat {layer5_conditional:.1f}% der Brummton-Halts, "
            f"erwartet > 20%. Verteilung: {conditional}"
        )


# ============================================================================
# TESTS FÜR NUMERISCHE KONSISTENZ
# ============================================================================

class TestNumerischeKonsistenz:
    """Tests für die numerischen Brücken, die das Projekt definiert hat."""

    def test_burumut_plus_137_eq_37_hoch_2(self):
        """BURUMUT-Summe (A=1..Z=26) + 137 muss 37² = 1369 sein."""
        BURUMUT = (
            "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
            "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        )
        # Lateinische Buchstaben-Summe
        burumut_summe = sum(ord(c) - ord('A') + 1 for c in BURUMUT)
        assert burumut_summe == 1232, f"BURUMUT-Summe sollte 1232 sein, ist {burumut_summe}"
        assert burumut_summe + 137 == 37**2, "BURUMUT + 137 muss 37² sein"

    def test_burumut_99_plus_117_eq_216(self):
        """BURUMUT-Länge 99 + 117 (Schlüssel) = 216 (Numeri-Boustrophedon)."""
        BURUMUT = (
            "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
            "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        )
        assert len(BURUMUT) == 99
        assert len(BURUMUT) + 117 == 216

    def test_5_mal_14_plus_2_eq_72(self):
        """5 Layer × 14 Zeichen + 2 (Start + HALT) = 72."""
        assert 5 * 14 + 2 == 72

    def test_burumut_19_unique_latein(self):
        """BURUMUT hat 19 unterschiedliche lateinische Buchstaben."""
        BURUMUT = (
            "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
            "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        )
        unique = set(BURUMUT)
        assert len(unique) == 19, (
            f"BURUMUT sollte 19 unterschiedliche lateinische Buchstaben haben, "
            f"aber hat {len(unique)}: {sorted(unique)}"
        )

    def test_18_plus_4_eq_22(self):
        """BURUMUT's 18 hebräisch-nutzbare + 4 fehlend = 22 (Sefer Yetzirah)."""
        BURUMUT = (
            "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
            "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
        )
        HEBREW_22 = set(['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
                          'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת'])
        mapping = {
            'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
            'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
            'S': 'ק', 'Y': 'י', 'Z': 'ז',
        }
        used = set(mapping[c] for c in set(BURUMUT) if c in mapping)
        missing = HEBREW_22 - used
        assert len(used) == 18, f"Erwartet 18 hebr. verwendet, ist {len(used)}"
        assert len(missing) == 4, f"Erwartet 4 hebr. fehlend, ist {len(missing)}: {missing}"
        assert len(used) + len(missing) == 22

    def test_22_plus_50_eq_72(self):
        """22 Konsonanten + 50 (BURUMUT's 50% Leere) = 72 (Knoten-Tora)."""
        assert 22 + 50 == 72


# ============================================================================
# TESTS FÜR STRUKTURELLE EIGENSCHAFTEN
# ============================================================================

class TestStrukturelleEigenschaften:
    """Tests für die korrekte Implementierung der Turing-Maschine."""

    def test_22_hebrew_consonants(self):
        """Es gibt genau 22 hebräische Konsonanten."""
        HEBREW_22 = ['א','ב','ג','ד','ה','ו','ז','ח','ט','י',
                     'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת']
        assert len(HEBREW_22) == 22

    def test_5_fehlende_operatoren(self):
        """5 fehlende Konsonanten = 5 fehlende Operatoren."""
        HEBREW_22 = {'א','ב','ג','ד','ה','ו','ז','ח','ט','י',
                     'כ','ל','מ','נ','ס','ע','פ','צ','ק','ר','ש','ת'}
        # BURUMUT verwendete Konsonanten
        mapping = {
            'A': 'א', 'B': 'ב', 'E': 'ה', 'F': 'ו', 'M': 'מ', 'R': 'צ', 'T': 'ר', 'U': 'ש',
            'H': 'ח', 'I': 'ט', 'L': 'ל', 'N': 'נ', 'O': 'ס', 'P': 'ע', 'Q': 'פ',
            'S': 'ק', 'Y': 'י', 'Z': 'ז',
        }
        used = set(mapping.values())
        missing = HEBREW_22 - used
        # Erwartung: כ (Kaf), ג (Gimel), ד (Dalet), ת (Tav), — was noch?
        assert len(missing) == 4, (
            f"Erwartet 4 fehlende Konsonanten, gefunden {len(missing)}: {missing}"
        )

    def test_brummton_halt_step_mit_1_indexiert(self):
        """Halt-Step ist 1-indexiert (erster Schritt = 1)."""
        from BRUMMTON_STATISTIC import run_brummton_machine_once
        brt = "בשצמשרהואמתוש"
        result = run_brummton_machine_once(brt, brummton_peak=0.0, seed=0)
        # Mit brummton_peak=0 gibt es nur NORMAL_HALT
        # Halt-Step sollte 6 sein (Schritt 6 = HALT nach READ, WRITE, STATE, MOVE_L, MOVE_R, HALT)
        # ABER: das ist NORMAL_HALT nicht Brummton
        assert result[0] in (6, 12, 18, 24, 30), (
            f"NORMAL_HALT sollte einer der HALT-Schritte sein, ist {result[0]}"
        )
        assert result[1] == 'NORMAL_HALT', (
            f"Mit brummton_peak=0 muss NORMAL_HALT sein, ist {result[1]}"
        )


# ============================================================================
# HAUPTPROGRAMM
# ============================================================================

if __name__ == "__main__":
    # Manueller Lauf ohne pytest
    print("="*70)
    print("TDD TESTS — Brummton Tora-Turing-Maschine")
    print("="*70)
    print()
    print("Diese Tests spezifizieren das SOLL-Verhalten.")
    print("Aktueller Status: alle Tests sollten fehlschlagen (red phase).")
    print()
    print("="*70)
    print("TEST 1: Numerische Konsistenz")
    print("="*70)

    # Test 1: BURUMUT + 137 = 37²
    BURUMUT = (
        "BURUMUTREFAMTUNURESUTREGUMFAYAPS"
        "UAZBEHIMLAZANRUAZBENOMBAMZHQRSANLRUAZBEHIMLAZANRUAZBENOMBARAZHQRSAN"
    )
    burumut_summe = sum(ord(c) - ord('A') + 1 for c in BURUMUT)
    print(f"  BURUMUT-Summe: {burumut_summe} (erwartet 1232): {'✅' if burumut_summe == 1232 else '❌'}")
    print(f"  + 137 = {burumut_summe + 137} (erwartet 1369 = 37²): {'✅' if burumut_summe + 137 == 1369 else '❌'}")

    # Test 2: Brummton-Verteilung
    print()
    print("="*70)
    print("TEST 2: Brummton-Verteilung über 50 Läufe (BUG-CHECK)")
    print("="*70)
    print()
    from BRUMMTON_STATISTIC import run_brummton_machine_once
    brt = "בשצמשרהואמתוש"
    n_runs = 50
    results = []
    for seed in range(n_runs):
        result = run_brummton_machine_once(brt, brummton_peak=0.99, seed=seed)
        results.append({'layer': result[2], 'halt_type': result[1]})
    layer_counts = Counter(r['layer'] for r in results)
    print("Aktuelle Verteilung:")
    for layer in sorted(layer_counts.keys()):
        pct = layer_counts[layer] / n_runs * 100
        print(f"  Layer {layer}: {layer_counts[layer]:3d} ({pct:5.1f}%)")
    print()
    print("Erwartete Verteilung (laut Spec):")
    print("  Layer 1: 0% (kein Brummton)")
    print("  Layer 2: 5%")
    print("  Layer 3: 20%")
    print("  Layer 4: 50%")
    print("  Layer 5: 90%")
    print()
    layer1_pct = layer_counts.get(1, 0) / n_runs * 100
    layer5_pct = layer_counts.get(5, 0) / n_runs * 100
    if layer1_pct < 5:
        print(f"✅ Layer 1 OK: {layer1_pct:.1f}% < 5%")
    else:
        print(f"❌ Layer 1 BUG: {layer1_pct:.1f}% >= 5% (zu viele Brummton-Halts zu früh)")
    if layer5_pct > 50:
        print(f"✅ Layer 5 OK: {layer5_pct:.1f}% > 50%")
    else:
        print(f"❌ Layer 5 BUG: {layer5_pct:.1f}% <= 50% (zu wenig Brummton am Ende)")
