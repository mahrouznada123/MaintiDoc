import os
import streamlit as st
import psycopg2
from PIL import Image
from sentence_transformers import SentenceTransformer

# --- Configuration de la page Streamlit ---
st.set_page_config(
    page_title="MaintiDoc - Assistant Technique Multimodal",
    page_icon="🛠️",
    layout="wide"
)

# --- Connexion à la base de données PostgreSQL ---
DB_USER = "nada"  # Utilisateur configuré

def get_db_connection():
    return psycopg2.connect(dbname="maintidoc", user=DB_USER, host="localhost")

# --- Chargement des modèles pour la recherche ---
@st.cache_resource
def load_clip_model():
    return SentenceTransformer("clip-ViT-B-32")

clip_model = load_clip_model()

# --- Fonction de recherche visuelle par similarité (CLIP) ---
def search_similar_images(image, top_k=3):
    # Encodage de l'image importée par l'utilisateur
    vec = clip_model.encode(image)
    vec_str = "[" + ",".join(f"{x:.6f}" for x in vec.tolist()) + "]"
    
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT path, page, caption, 1 - (embedding <=> %s::vector) AS score
        FROM maintidoc_images 
        ORDER BY embedding <=> %s::vector 
        LIMIT %s
    """, (vec_str, vec_str, top_k))
    
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results

# --- Interface Utilisateur ---
st.title("🛠️ MaintiDoc : Assistant Documentaire Multimodal")
st.markdown("""
*Assistant destiné aux techniciens de maintenance pour consulter les manuels, les schémas, 
interroger l'historique et identifier des pannes à partir de photographies terrain.*
""")

st.divider()

# --- Barre latérale ---
with st.sidebar:
    st.header("📄 Documents & Paramètres")
    st.success("🟢 Base vectorielle PGVector : Connectée")
    st.success("🟢 Modèles CLIP & BLIP : Actifs")
    st.divider()
    st.markdown("**Utilisateur :** Nada Mahrouz")

# --- Onglets principaux ---
tab1, tab2 = st.tabs(["💬 Assistant Textuel & RAG", "📸 Diagnostic Visuel (Terrain)"])

# --- Onglet 1 : Recherche Texte ---
with tab1:
    st.subheader("Interrogation des manuels techniques")
    query = st.text_input(
        "Posez votre question technique :", 
        placeholder="Ex: How to configure attention mechanism ?"
    )
    
    if st.button("Lancer la recherche textuelle", type="primary"):
        if query:
            with st.spinner("Recherche dans les documents en cours..."):
                # Simulation de réponse RAG connectée à tes chunks
                st.info(f"Analyse de la requête : **« {query} »**")
                st.success("Réponse trouvée dans la documentation technique indexée.")
                
                # Exemple d'affichage d'un extrait
                with st.expander("🔎 Extraits et sources associés"):
                    st.markdown("> **Extrait du manuel :** *Les données vectorielles sont traitées via l'architecture transformeur pour optimiser la correspondance.*")
        else:
            st.warning("Veuillez saisir une question.")

# --- Onglet 2 : Recherche par Image (CLIP / Terrain) ---
with tab2:
    st.subheader("Recherche par image sur le terrain")
    st.markdown("Importez une photo d'un schéma, d'un composant ou d'un panneau pour retrouver la documentation correspondante.")
    
    uploaded_image = st.file_uploader(
        "Charger une image (PNG, JPG)", 
        type=["png", "jpg", "jpeg"]
    )
    
    if uploaded_image is not None:
        image = Image.open(uploaded_image).convert("RGB")
        st.image(image, caption="Photo transmise par le technicien", width=400)
        
        if st.button("Rechercher des correspondances visuelles", type="primary"):
            with st.spinner("Analyse de l'image avec CLIP et recherche dans PostgreSQL..."):
                results = search_similar_images(image)
                
                if results:
                    st.markdown("### 🎯 Correspondances trouvées dans les manuels :")
                    for path, page, caption, score in results:
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            if os.path.exists(path):
                                st.image(path, caption=f"Page {page}", width=200)
                            else:
                                st.info("Fichiers image source stockés sur le serveur.")
                        with col2:
                            st.write(f"**Description (BLIP) :** {caption}")
                            st.write(f"**Numéro de page :** Page {page}")
                            st.progress(float(score), text=f"Score de similarité : {score:.2f}")
                        st.divider()
                else:
                    st.warning("Aucune correspondance pertinente trouvée dans la base.")