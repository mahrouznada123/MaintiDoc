import os
import fitz  # PyMuPDF
import psycopg2
import os
os.environ["TRANSFORMERS_NO_ADVISORY_WARNINGS"] = "1"
os.environ["HF_HUB_DISABLE_TELEMETRY"] = "1"

# Contourner le verrouillage de torch.load() dans transformers >= 4.49
import transformers.utils.import_utils
transformers.utils.import_utils.check_torch_load_is_safe = lambda *args, **kwargs: True
from PIL import Image
from sentence_transformers import SentenceTransformer
from transformers import BlipProcessor, BlipForConditionalGeneration
from llama_index.core import Document, VectorStoreIndex, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

PDF_PATH = "data/attention.pdf"
IMG_DIR = "data/images"
DB_USER = "nada"   # résultat de `whoami`
os.makedirs(IMG_DIR, exist_ok=True)

# ---------- 1. Récupérer les images ----------
doc = fitz.open(PDF_PATH)
images = []  # (chemin, page)

for page_num, page in enumerate(doc, start=1):
    found = False
    # a) images intégrées au PDF
    for i, img in enumerate(page.get_images(full=True)):
        pix = fitz.Pixmap(doc, img[0])
        if pix.n > 4:
            pix = fitz.Pixmap(fitz.csRGB, pix)
        if pix.width < 100 or pix.height < 100:
            continue
        path = f"{IMG_DIR}/page{page_num}_img{i}.png"
        pix.save(path)
        images.append((path, page_num))
        found = True
    # b) sinon, rendu de la page si elle contient une figure (dessins vectoriels)
    if not found and "Figure" in page.get_text():
        path = f"{IMG_DIR}/page{page_num}_render.png"
        page.get_pixmap(dpi=110).save(path)
        images.append((path, page_num))

print(f"{len(images)} image(s) à traiter")

# ---------- 2. Modèles ----------
clip = SentenceTransformer("clip-ViT-B-32")  # vecteurs de 512 dimensions
blip_proc = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
blip = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def caption(img):
    inputs = blip_proc(img, return_tensors="pt")
    out = blip.generate(**inputs, max_new_tokens=40)
    return blip_proc.decode(out[0], skip_special_tokens=True)

def to_pg(vec):
    return "[" + ",".join(f"{x:.6f}" for x in vec.tolist()) + "]"

# ---------- 3. Table PGVector pour les images (CLIP) ----------
conn = psycopg2.connect(dbname="maintidoc", user=DB_USER, host="localhost")
cur = conn.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS maintidoc_images (
        id SERIAL PRIMARY KEY,
        path TEXT, page INT, caption TEXT,
        embedding vector(512)
    )
""")
cur.execute("DELETE FROM maintidoc_images")  # évite les doublons si on relance

# ---------- 4. Index texte existant (pour y ajouter les descriptions) ----------
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)
vector_store = PGVectorStore.from_params(
    database="maintidoc", host="localhost", port=5432,
    user=DB_USER, password="", table_name="maintidoc_chunks", embed_dim=384,
)
text_index = VectorStoreIndex.from_vector_store(vector_store)

# ---------- 5. Traitement ----------
for path, page_num in images:
    img = Image.open(path).convert("RGB")
    desc = caption(img)
    emb = clip.encode(img)
    cur.execute(
        "INSERT INTO maintidoc_images (path, page, caption, embedding) VALUES (%s,%s,%s,%s::vector)",
        (path, page_num, desc, to_pg(emb)),
    )
    text_index.insert(Document(
        text=f"Image (page {page_num}) : {desc}",
        metadata={"page": page_num, "type": "image", "source": "attention.pdf", "image_path": path},
    ))
    print(f"✅ page {page_num} : {desc}")

conn.commit()

# ---------- 6. Test : recherche d'image par texte avec CLIP ----------
q = to_pg(clip.encode("diagram of the Transformer architecture"))
cur.execute("""
    SELECT path, page, caption, 1 - (embedding <=> %s::vector) AS score
    FROM maintidoc_images ORDER BY embedding <=> %s::vector LIMIT 3
""", (q, q))
print("\nTest de recherche :")
for row in cur.fetchall():
    print(row)

cur.close()
conn.close()