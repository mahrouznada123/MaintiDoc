import fitz  # PyMuPDF
import os


PDF_PATH = "data/attention.pdf"
IMG_DIR = "data/images"
os.makedirs(IMG_DIR, exist_ok=True)


def extract_chunks(pdf_path=PDF_PATH):
    """Retourne une liste de blocs {text, page, type} (texte et tableaux)."""
    doc = fitz.open(pdf_path)
    chunks = []  # texte + métadonnées

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

    return chunks


# Utilisé par index.py : from ingest import chunks
chunks = extract_chunks()


if __name__ == "__main__":
    n_text = sum(c["type"] == "text" for c in chunks)
    n_tab = sum(c["type"] == "table" for c in chunks)
    print(f"{n_text} blocs de texte, {n_tab} tableaux extraits")