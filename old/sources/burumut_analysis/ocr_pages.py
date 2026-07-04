"""
OCR der Tengri-137 PDF-Seiten, weil PyMuPDF keinen Text extrahieren konnte.
"""
import fitz
import pytesseract
from PIL import Image
import io

pdf_path = "sources/Tengri-137.pdf"
doc = fitz.open(pdf_path)

# Erste die ersten Seiten in Bilder konvertieren und OCR anwenden
results = {}
for page_num in [22]:  # Seite 23 (0-indexed: 22)
    page = doc[page_num]
    # Pixmap (Rasterbild) mit hoher Aufloesung
    pix = page.get_pixmap(dpi=300)
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    text = pytesseract.image_to_string(img, lang="eng+deu")
    results[page_num + 1] = text
    print(f"=== SEITE {page_num+1} ===")
    print(text)
    print("="*70)

with open("sources/burumut_analysis/page_23_ocr.txt", "w", encoding="utf-8") as f:
    for k, v in results.items():
        f.write(f"=== SEITE {k} ===\n{v}\n\n")

print("OCR gespeichert in page_23_ocr.txt")