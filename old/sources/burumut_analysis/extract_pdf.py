"""
Tengri-137 Original-PDF-Extraktion.

Wir verwenden PyMuPDF, um den vollstaendigen Text aus dem PDF zu extrahieren
und gezielt nach der BURUMUTREFAMTU-Sequenz und Seite 23 zu suchen.
"""
import fitz  # PyMuPDF
import re

pdf_path = "sources/Tengri-137.pdf"
doc = fitz.open(pdf_path)
print(f"Anzahl Seiten: {doc.page_count}")
print(f"PDF-Titel: {doc.metadata.get('title', 'n/a')}")
print(f"PDF-Autor: {doc.metadata.get('author', 'n/a')}")
print(f"Erstellungsdatum: {doc.metadata.get('creationDate', 'n/a')}")
print()

# Speichere den vollstaendigen Text aller Seiten in eine Textdatei
all_text = []
for page_num in range(doc.page_count):
    page = doc[page_num]
    text = page.get_text("text")
    all_text.append(f"=== SEITE {page_num + 1} ===\n{text}\n")

combined = "\n".join(all_text)
with open("sources/burumut_analysis/tengri137_full_text.txt", "w", encoding="utf-8") as f:
    f.write(combined)
print(f"Vollstaendiger Text gespeichert in tengri137_full_text.txt")
print(f"Gesamtzahl Zeichen: {len(combined)}")
print()

# Suche nach "BURUMUT"
print("="*70)
print("SUCHE NACH 'BURUMUT'")
print("="*70)
burumut_positions = []
for page_num in range(doc.page_count):
    page_text = doc[page_num].get_text("text")
    if "BURUMUT" in page_text.upper() or "burumut" in page_text.lower():
        # Suche alle Vorkommen
        for m in re.finditer(r"(?i)BURUMUT", page_text):
            burumut_positions.append((page_num + 1, m.start(), page_text[max(0,m.start()-100):m.start()+300]))
print(f"Anzahl Vorkommen von BURUMUT: {len(burumut_positions)}")
for page, pos, ctx in burumut_positions[:10]:
    print(f"\n--- Seite {page}, Position {pos} ---")
    print(f"Kontext: {ctx!r}")
print()

# Suche nach Seite 23
print("="*70)
print("SUCHE NACH SEITE 23 (Pages 21-25)")
print("="*70)
for page_num in [20, 21, 22, 23, 24]:  # 0-indexed
    if page_num < doc.page_count:
        page = doc[page_num]
        text = page.get_text("text")
        print(f"\n--- SEITE {page_num+1} ---")
        print(text[:3000])
        print("...")
print()

print("="*70)
print("PDF-EXTRAKTION ABGESCHLOSSEN")
print("="*70)