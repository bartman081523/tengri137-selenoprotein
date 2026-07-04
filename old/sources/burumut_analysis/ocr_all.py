"""
OCR aller Tengri-137 Seiten.
"""
import fitz
import pytesseract
from PIL import Image
import io

pdf_path = "sources/Tengri-137.pdf"
doc = fitz.open(pdf_path)

results = {}
for page_num in range(doc.page_count):
    page = doc[page_num]
    pix = page.get_pixmap(dpi=300)
    img_bytes = pix.tobytes("png")
    img = Image.open(io.BytesIO(img_bytes))
    text = pytesseract.image_to_string(img, lang="eng+deu")
    results[page_num + 1] = text

with open("sources/burumut_analysis/tengri137_all_pages_ocr.txt", "w", encoding="utf-8") as f:
    for k, v in results.items():
        f.write(f"=== SEITE {k} ===\n{v}\n\n")

print("Alle Seiten OCR gespeichert.")