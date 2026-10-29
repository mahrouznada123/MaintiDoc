import fitz  # PyMuPDF
import os

PDF_PATH = "data/attention.pdf"
IMG_DIR = "data/images"
os.makedirs(IMG_DIR, exist_ok=True)

doc = fitz.open(PDF_PATH)
chunks = []   # texte + métadonnées
images = []   # chemins des images extraites

for page_num, page in enumerate(doc, start=1):
    # Texte
    text = page.get_text()
    if text.strip():
        chunks.append({"text": text, "page": page_num, "type": "text"})

    # Tableaux
    for t in page.find_tables().tables:
        rows = t.extract()
        table_txt = "\n".join(" | ".join(str(c) for c in r) for r in rows)
        chunks.append({"text": table_txt, "page": page_num, "type": "table"})

    # Images
    for i, img in enumerate(page.get_images(full=True)):
        pix = fitz.Pixmap(doc, img[0])
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        path = f"{IMG_DIR}/page{page_num}_img{i}.png"
        pix.save(path)
        images.append({"path": path, "page": page_num})

print(f"{len(chunks)} blocs texte/tableau, {len(images)} images")