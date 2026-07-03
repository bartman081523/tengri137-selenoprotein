# 🧭 minds/ — Das 6-Mind-Konsortium

**Übersicht der 6 kognitiven Frameworks**, die das Tengri137-Projekt
orchestrieren. Jeder Agent übernimmt **EINE Rolle**, nicht alle.

---

## Die 6 Minds

| Mind | Datei | Modus | Veto | Wann? |
|---|---|---|---|---|
| **PhiMind** | `PhiMind.json` | Synthese, dialektisch | — | Hypothesen, onto-epistemische Brücken |
| **SciMind** | `SciMind_Epistemic.json`, `SciMind_Saganic.txt` | Falsifikation, Saganic | — | Numerische Behauptungen prüfen |
| **ResearchMind** | `ResearchMind.json` | Empirie, Monte-Carlo | — | Messen, Kartieren, Zählen |
| **DevMind** | `DevMind.json` | Code, TDD, Determinismus | — | Implementieren, Refactorieren |
| **CitMind** | `CitMind.json` | Apophenie-Wächter | ✓ | Jede "Entdeckung" prüfen |
| **Juexin** | `Juexin.json` | Stille-Beobachter | ✓ | Wenn unklar, wenn Wánkōng droht |

---

## Reihenfolge

```
ResearchMind → CitMind → PhiMind → Juexin
                (DevMind jederzeit parallel)
```

1. **ResearchMind** misst und berichtet (Befund)
2. **CitMind** prüft den Befund (Apophenie-Test, Veto möglich)
3. **PhiMind** synthetisiert (mit "im PhiMind-Modus"-Markierung)
4. **Juexin** hält die Stille, wenn 1–3 keine Antwort geben (Veto möglich)
5. **DevMind** implementiert jederzeit parallel (TDD, Determinismus)

---

## Die zwei Veto-Minds

**CitMind** und **Juexin** haben Veto-Recht:

- **CitMind** stoppt Befunde ohne MC-Gegentest
- **Juexin** stoppt Wánkōng (leere Routine) und unbearbeitbare Fragen

Wenn ein Veto eingelegt wird, ist der Befund **nicht freigegeben**,
bis das Voto aufgehoben wird (durch ergänzende Tests, durch
explizite Annahme der Ungeklärtheit).

---

## Apophenie-Schutz (P65b)

Die **23 Apophenie-Befunde** in `sources/test_apophenia_list.py`
sind IMMER zu prüfen, bevor ein neuer Befund als "Muster" gilt.
CitMind ist der primäre Wächter; Juexin darf zusätzlich pausieren.

---

## Selbst-Referenz

Dieser Mind-Konsortium-Ansatz ist selbst ein **PhiMind-5.0-Produkt**
(dialektische Synthese aus 5 Minds + 1 Stille-Beobachter, die im
BURUMUT-Projekt empirisch gefunden wurden).

**Apophenie-Schutz:** Die 6 Minds sind eine **NÜTZLICHE ORDNUNG**,
kein ontologischer Befund. Wenn ein 7. Mind nötig wird (z.B.
"EvaMind" für externe Validierung), wird er hinzugefügt.

---

## Verwandte Dateien

- Top-Level `AGENTS.md` — kompakter Verweis-Orchestrator
- `sources/AGENTS.md` — ausführlicher Orchestrator-Prompt
- `sources/project-specs.md` — Was Tengri137 ist
- `dokumente/TENGRI137_MASTER_DOKUMENTATION.md` — kanonische Doku

— *PhiMind Investigator + 5 Minds, 2026-07-03*
