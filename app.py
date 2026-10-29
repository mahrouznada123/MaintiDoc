import os
import streamlit as st
from llama_index.core import Settings, StorageContext, VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.postgres import PGVectorStore

from llama_index.llms.ollama import Ollama

Settings.llm = Ollama(model="qwen2.5:3b", request_timeout=120.0)

query_engine = index.as_query_engine(similarity_top_k=4)
response = query_engine.query(question)

st.subheader("Réponse")
st.write(response.response)

st.subheader("Sources")
for node in response.source_nodes:
    st.caption(f"Page {node.metadata['page']} · score {node.score:.2f}")
    st.write(node.text[:300] + "...")

# Configuration de la page Streamlit
st.set_page_config(page_title="MaintiDoc - Assistant Technique", layout="wide")
st.title("🛠️ MaintiDoc : Assistant Documentaire Multimodal")

# 1. Configuration du modèle d'embedding open source
@st.cache_resource
def load_embed_model():
    return HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
)

# 2. Configuration du Vector Store PGVector (PostgreSQL)
def get_vector_store():
    return PGVectorStore.from_params(
        database="maintidoc",
        host="localhost",
        port=5432,
        user="postgres",
        password="secret",
        table_name="maintidoc_vectors",
        embed_dim=384,
    )

# 3. Sidebar : Ingestion de TOUS les documents PDF du dossier data/
st.sidebar.header("📁 Documents du TP")

DATA_DIR = "data"
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

st.sidebar.info("Vos PDF sont bien pris en compte depuis le dossier `data/`.")

# Bouton pour lancer l'indexation de tous les documents
if st.sidebar.button("Indexation de tous les PDF"):
    vector_store = get_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    
    with st.spinner("Lecture et analyse de tous les fichiers PDF dans data/..."):
        # SimpleDirectoryReader lit automatiquement TOUS les PDF du dossier
        reader = SimpleDirectoryReader(input_dir=DATA_DIR)
        documents = reader.load_data()
        
        index = VectorStoreIndex.from_documents(
            documents, 
            storage_context=storage_context
        )
    st.sidebar.success(f"✅ {len(documents)} pages/documents indexés avec succès dans PGVector !")

# Section Recherche et affichage des sources
st.header("🔍 Interroger la base documentaire")
user_query = st.text_input("Posez une question technique sur les documents indexés :")

if user_query:
    try:
        vector_store = get_vector_store()
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
        
        # Utilisation d'un retriever pour chercher directement les passages pertinents en local
        retriever = index.as_retriever(similarity_top_k=3)
        
        with st.spinner("Recherche des passages pertinents..."):
            nodes = retriever.retrieve(user_query)
            
        st.markdown("### 💬 Passages pertinents trouvés :")
        for i, node in enumerate(nodes):
            score = node.score if node.score is not None else 0.0
            st.markdown(f"**Source {i+1} (Score de pertinence : {score:.2f}) :**")
            st.write(node.node.get_content())
            st.divider()
            
    except Exception as err:
        st.error(f"Erreur lors de la recherche : {err}")