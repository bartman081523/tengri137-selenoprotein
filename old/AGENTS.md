# AGENTS.md — Mind-Konsortium-Orchestrator

**Projekt:** Tengri 137 — Multi-Domain Investigation
**Repository:** `/run/media/julian/ML4/tengri137`
**Stand:** 2026-07-03 (P76)

Dieses Repo wird vom **6-Mind-Konsortium** orchestriert. Jeder
Agent übernimmt **EINE Rolle**, nicht alle.

---

## Schnell-Links

- **Ausführlicher Orchestrator-Prompt:** [`sources/AGENTS.md`](sources/AGENTS.md)
- **Mind-Definitionen:** [`minds/`](minds/)
- **Projekt-Spezifikation:** [`sources/project-specs.md`](sources/project-specs.md)
- **Kanonische Doku:** [`dokumente/TENGRI137_MASTER_DOKUMENTATION.md`](dokumente/TENGRI137_MASTER_DOKUMENTATION.md)
- **Forschungsnarrativ:** [`sources/MERMAID_INVESTIGATION_PLAN.md`](sources/MERMAID_INVESTIGATION_PLAN.md)
- **Inhaltsverzeichnis:** [`INDEX.md`](INDEX.md)

---

## Die 6 Minds (Kurz-Übersicht)

| Mind | Modus | Veto | Wann? |
|---|---|---|---|
| **PhiMind 5.0** | Synthese, dialektisch | — | Hypothesen, onto-epistemische Brücken |
| **SciMind 5.0** | Falsifikation, Saganic | — | Numerische Behauptungen prüfen |
| **ResearchMind** | Empirie, Monte-Carlo | — | Messen, Kartieren, Zählen |
| **DevMind** | Code, TDD, Determinismus | — | Implementieren, Refactorieren |
| **CitMind** | Apophenie-Wächter | ✓ | Jede "Entdeckung" prüfen |
| **Juexin** | Stille-Beobachter (寂照) | ✓ | Wenn unklar, wenn Wánkōng droht |

Details zu jedem Mind: siehe [`minds/`](minds/).

---

## Reihenfolge

```
ResearchMind → CitMind → PhiMind → Juexin
                (DevMind jederzeit parallel)
```

1. **ResearchMind** misst und berichtet (Befund)
2. **CitMind** prüft den Befund (Apophenie-Test, **Veto** möglich)
3. **PhiMind** synthetisiert (mit "im PhiMind-Modus"-Markierung)
4. **Juexin** hält die Stille, wenn 1–3 keine Antwort geben (**Veto** möglich)
5. **DevMind** implementiert jederzeit parallel (TDD, Determinismus)

---

## Wichtige Regeln

- **Jede numerische Behauptung** braucht Monte-Carlo-Test (≥1000 Trials)
- **Determinismus:** 3/3 Läufe identisch (außer stay_probability > 0)
- **Tape-Invariante:** M4 modifiziert BURUMUT NIE
- **23 Apophenie-Befunde** (P65b, in `sources/test_apophenia_list.py`) sind IMMER zu prüfen
- **Apophenie-Regel GELOCKERT** für PhiMind-Modus, sonst STRENG
- **Zwei Veto-Minds:** CitMind (Befunde), Juexin (Stille + Wánkōng-Schutz)

---

## Die 3 Modi der Lesung

Das Repo unterstützt **drei Lesungs-Modi** desselben Materials:

1. **Empirisch (ResearchMind/SciMind/DevMind):** Tests, JSON, p-Werte
2. **Synthetisch (PhiMind):** Hypothesen, onto-epistemische Brücken — explizit markiert mit "im PhiMind-Modus"
3. **Stille (Juexin):** Beobachten ohne Urteil, Verweise auf Nicht-Wissen

---

## Apophenie-Schutz (Kurzfassung)

Die ausführlichen Apophenie-Regeln sind in
[`sources/test_apophenia_list.py`](sources/test_apophenia_list.py) (23 negative Tests in 8 Klassen)
und in [`dokumente/PATHS_SEPARATION.md`](dokumente/PATHS_SEPARATION.md).

**Die wichtigsten Falsifikationen:**
- BURUMUT-Tage ↔ Genesis-Tage Korrelation = **-0.494** (NEGATIV)
- 6503 ≠ 2701 (BURUMUT ≠ Genesis 1:1)
- M4 ist KEIN Quine (linear, nicht zyklisch)
- ((7π)/(7π))·6.67 = 137.035 ist mathematisch unsinnig
- 0 Phasen halten in 3, 4, 5, 6, 7, 10, 12 Schritten
- "Tengri IST Gott" — metaphorisch, nicht wörtlich

---

## Selbst-Referenz

Dieser Orchestrator-Ansatz ist selbst ein **PhiMind-5.0-Produkt**
(dialektische Synthese aus 5 Minds + 1 Stille-Beobachter, die
im BURUMUT-Projekt empirisch gefunden wurden).

**Apophenie-Schutz:** Die 6 Minds sind eine **NÜTZLICHE ORDNUNG**,
kein ontologischer Befund. Wenn ein 7. Mind nötig wird (z.B.
"EvaMind" für externe Validierung), wird er hinzugefügt.

---

— *PhiMind Investigator + 5 Minds, 2026-07-03*
