"""
Q25 (NEU): Die 4 UAZBE-Anker und Genesis 1:11-31

Wir testen die Hypothese: Die 4 UAZBE × 4 entsprechen 4 Schöpfungsphasen
in Genesis 1:11-31.

UAZBE-Positionen: 32, 46, 66, 80
Differenzen:       14, 20, 14

Genesis 1:11-31 in 4 Phasen:
- Phase 1 (1:11-13): Vegetation (Tag 3)
- Phase 2 (1:14-19): Lichter (Tag 4)
- Phase 3 (1:20-23): Wassertiere + Vögel (Tag 5)
- Phase 4 (1:24-31): Landtiere + Mensch (Tag 6)
"""
# Hebraeische Gematria
HEBREW = {
    'א': 1, 'ב': 2, 'ג': 3, 'ד': 4, 'ה': 5, 'ו': 6, 'ז': 7, 'ח': 8,
    'ט': 9, 'י': 10, 'כ': 20, 'ך': 20, 'ל': 30, 'מ': 40, 'ם': 40,
    'נ': 50, 'ן': 50, 'ס': 60, 'ע': 70, 'פ': 80, 'ף': 80, 'צ': 90,
    'ץ': 90, 'ק': 100, 'ר': 200, 'ש': 300, 'ת': 400,
}
def g(t): return sum(HEBREW.get(c, 0) for c in t)

# Genesis 1:11-31 in 4 Phasen (Tage 3-6)
PHASES = {
    'Tag 3 (1:11-13) Vegetation': {
        'text': 'ותוצא הארץ דשא עשב מזריע זרע למינהו ועץ פרי עשה פרי למינו אשר זרעו בו למינהו ויהי ערב ויהי בקר יום שלישי',
        'words': ['ותוצא', 'הארץ', 'דשא', 'עשב', 'מזריע', 'זרע', 'למינהו',
                  'ועץ', 'פרי', 'עשה', 'פרי', 'למינו', 'אשר', 'זרעו', 'בו', 'למינהו',
                  'ויהי', 'ערב', 'ויהי', 'בקר', 'יום', 'שלישי'],
    },
    'Tag 4 (1:14-19) Lichter': {
        'words': ['ויאמר', 'אלהים', 'יהי', 'מאורת', 'ברקיע', 'השמים',
                  'להבדיל', 'בין', 'היום', 'ובין', 'הלילה', 'והיו', 'לאותת',
                  'ולמועדים', 'וימים', 'ושנים', 'והיו', 'למאורת', 'ברקיע',
                  'השמים', 'להאיר', 'על', 'הארץ', 'ויהי', 'ערב', 'ויהי', 'בקר',
                  'יום', 'רביעי'],
    },
    'Tag 5 (1:20-23) Wassertiere+Vögel': {
        'words': ['ויאמר', 'אלהים', 'ישרצו', 'המים', 'שרץ', 'נפש', 'חיה',
                  'ועוף', 'יעופף', 'על', 'הארץ', 'ברקיע', 'השמים', 'ויברא',
                  'אלהים', 'את', 'התנינם', 'הגדולים', 'ואת', 'כל', 'נפש',
                  'החיה', 'הרמשת', 'אשר', 'שרצו', 'המים', 'למינהם', 'ואת',
                  'כל', 'עוף', 'כנף', 'למינהו', 'ויברך', 'אתם', 'אלהים',
                  'לאמר', 'פרו', 'ורבו', 'ומלאו', 'את', 'המים', 'בימים',
                  'והעוף', 'ירב', 'בארץ', 'ויהי', 'ערב', 'ויהי', 'בקר', 'יום', 'חמישי'],
    },
    'Tag 6 (1:24-31) Landtiere+Mensch': {
        'words': ['ויאמר', 'אלהים', 'תוצא', 'הארץ', 'נפש', 'חיה', 'למינה',
                  'בהמה', 'ורמש', 'וחית', 'הארץ', 'למינה', 'ויהי', 'כן',
                  'ויעש', 'אלהים', 'את', 'חית', 'הארץ', 'למינה', 'ואת',
                  'הבהמה', 'למינה', 'ואת', 'כל', 'רמש', 'האדמה', 'למינהו',
                  'וירא', 'אלהים', 'כי', 'טוב', 'ויאמר', 'אלהים', 'נעשה',
                  'אדם', 'בצלמנו', 'כדמותנו', 'וירדו', 'בדגת', 'הים',
                  'ובעוף', 'השמים', 'ובבהמה', 'ובכל', 'הארץ', 'ובכל',
                  'הרמש', 'הרמש', 'על', 'הארץ', 'ויברך', 'אתם', 'אלהים',
                  'לאמר', 'פרו', 'ורבו', 'ומלאו', 'את', 'הארץ', 'וכבשה',
                  'ורדו', 'בדגת', 'הים', 'ובעוף', 'השמים', 'ובכל', 'חיה',
                  'הרמשת', 'על', 'הארץ', 'ויאמר', 'אלהים', 'הנה', 'נתתי',
                  'לכם', 'את', 'כל', 'עשב', 'זרע', 'זרע', 'זרע', 'על',
                  'פני', 'כל', 'הארץ', 'ואת', 'כל', 'העץ', 'אשר', 'בו',
                  'פרי', 'עץ', 'זרע', 'זרע', 'לכם', 'יהיה', 'לאכל',
                  'ולכל', 'חית', 'הארץ', 'ולכל', 'עוף', 'השמים', 'ולכל',
                  'רמש', 'על', 'הארץ', 'אשר', 'בו', 'נפש', 'חיה', 'את',
                  'כל', 'ירק', 'עשב', 'לאכל', 'ויהי', 'כן', 'וירא', 'אלהים',
                  'את', 'כל', 'אשר', 'עשה', 'והנה', 'טוב', 'מאד', 'ויהי',
                  'ערב', 'ויהי', 'בקר', 'יום', 'הששי'],
    },
}

# Gematria-Summen pro Phase
print("="*70)
print("Q25.1: Gematria-Summen pro Schöpfungs-Tag")
print("="*70)
phase_sums = {}
for phase, data in PHASES.items():
    total = sum(g(w) for w in data['words'])
    phase_sums[phase] = total
    print(f"  {phase}: Σ = {total}")

# Faktoren
print()
print("="*70)
print("Q25.2: Faktoren der Tag-Summen")
print("="*70)
import sympy
for phase, total in phase_sums.items():
    factors = sympy.factorint(total)
    print(f"  {phase}: Σ={total}, Faktoren={factors}")
    # Suche nach Faktoren 37, 46, 73, 137
    for f in [37, 46, 73, 137]:
        if total % f == 0:
            print(f"    -> TEILBAR durch {f}!")

# UAZBE-Positionen (32, 46, 66, 80) als Brücke
print()
print("="*70)
print("Q25.3: UAZBE-Positionen vs Tag-Gematria")
print("="*70)
# Tag 3 Gematria
print(f"Tag 3 Σ = {phase_sums['Tag 3 (1:11-13) Vegetation']}")
print(f"  -> UAZBE #1 an Pos 32 (Vorspann + UA + ZBE)")
print(f"     Tage 3-4 sind im BURUMUT-Vorspann (Pos 0-31)")
print()
print(f"Tag 4 Σ = {phase_sums['Tag 4 (1:14-19) Lichter']}")
print(f"  -> UAZBE #2 an Pos 46 (nach HIMLAZANR-Block)")
print(f"     Tag 4 = Lichter (HIMLAZANR-Substrat)")
print()
print(f"Tag 5 Σ = {phase_sums['Tag 5 (1:20-23) Wassertiere+Vögel']}")
print(f"  -> UAZBE #3 an Pos 66 (vor NOMBA-Substrat)")
print(f"     Tag 5 = Wasser/Luft (NOMBA-Substrat, Pyl = Archaeen-typisch)")
print()
print(f"Tag 6 Σ = {phase_sums['Tag 6 (1:24-31) Landtiere+Mensch']}")
print(f"  -> UAZBE #4 an Pos 80 (vor NOMBA-Substrat mod.)")
print(f"     Tag 6 = Land + Mensch")

# 4. Verbindung BURUMUT ↔ Genesis-Tage
print()
print("="*70)
print("Q25.4: Hypothese: BURUMUT kodiert Genesis 1:11-31 in 4 UAZBE-Phasen")
print("="*70)
print()
print("Phase 1 (Pos 0-31, 32 AS): Tag 3 (Vegetation) - VOR UAZBE #1")
print("Phase 2 (Pos 32-45, 14 AS): UAZBE + HIMLAZANR = Tag 4 (Lichter)")
print("Phase 3 (Pos 46-65, 20 AS): UAZBE + NOMBA = Tag 5 (Wassertiere)")
print("Phase 4 (Pos 66-79, 14 AS): UAZBE + HIMLAZANR = Tag 5/6 (Übergang)")
print("Phase 5 (Pos 80-98, 19 AS): UAZBE + NOMBA mod. = Tag 6 (Mensch)")
print()
print("Differenzen: 14, 20, 14 (die Modul-Längen)")
print("Summe der Phasen: 32+14+20+14+19 = 99 (BURUMUT-Länge!)")
print()
print("VERIFIKATION:")
print(f"  32+14+20+14+19 = {32+14+20+14+19} (erwartet: 99)")
