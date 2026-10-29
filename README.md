Claude




















Readme · MD
# 🛠️ MaintiDoc : Assistant documentaire multimodal pour la maintenance
 
MaintiDoc est un assistant destiné aux techniciens de maintenance. Il exploite des documents techniques (texte, tableaux, images) pour répondre à des questions avec des références vérifiables.
 
> Le système ne pilote aucun équipement et ne remplace pas un technicien habilité.
 
Projet réalisé dans le cadre d'un TP à HESTIM Engineering & Business School (Big Data & Intelligence Artificielle).
 
## 🎯 Objectif
 
Construire progressivement un assistant RAG agentique multimodal :
 
| Étape | Contenu | Statut |
|-------|---------|--------|
| 1 | RAG agentique multimodal | 🟡 En cours |
| 2 | Fine-tuning | ⬜ À venir |
| 3 | Orchestration agentique et MCP | ⬜ À venir |
| 4 | Client web, Telegram/Discord, sécurité et déploiement | ⬜ À venir |
 
### Avancement de l'étape 1
 
| # | Tâche | Statut |
|---|-------|--------|
| 1 | Sélection du document | ✅ Fait |
| 2 | Extraction, embeddings et stockage PGVector | ✅ Fait |
| 3 | Traitement des images (CLIP + descriptions) | ✅ Fait |
| 4 | Question-réponse avec un LLM open source (Qwen via Ollama) | ⬜ À faire |
| 5 | Interface Streamlit | 🟡 En cours |
| 6 | Orchestration agentique (LangChain) | ⬜ À faire |
 
## ✅ Fonctionnalités actuelles
 
- Extraction du texte, des tableaux et des images d'un PDF (PyMuPDF)
- Embeddings multilingues open source avec LlamaIndex
- Stockage des vecteurs et métadonnées dans PostgreSQL + pgvector
- Recherche sémantique des passages pertinents
- Images : vecteurs CLIP dans PGVector et descriptions textuelles générées (BLIP) indexées avec le texte
- Interface Streamlit pour poser des questions
## 🚧 À venir
 
- Génération de réponses sourcées avec un LLM open source (Qwen via Ollama)
- Agent LangChain (choix des outils, gestion du contexte)
## 🧰 Technologies
 
Python · LlamaIndex · PyMuPDF · Hugging Face (sentence-transformers, BLIP) · CLIP · PostgreSQL / pgvector · Streamlit · LangChain · Ollama
 
## 📁 Structure du projet
 
```
MaintiDoc/
├── data/            # PDF sources (document de travail : "Attention Is All You Need")
├── app.py           # Interface Streamlit
├── ingest.py        # Extraction du texte, des tableaux et des images
├── index.py         # Embeddings et indexation dans PGVector
├── image_index.py   # Traitement des images (CLIP + descriptions)
├── .gitignore
└── README.md
```
 
## ⚙️ Installation
 
### Prérequis
 
- Python 3.9+
- PostgreSQL avec l'extension pgvector (par exemple via Postgres.app)
### Étapes
 
```bash
# 1. Cloner le dépôt
git clone https://github.com/mahrouznada123/MaintiDoc.git
cd MaintiDoc
 
# 2. Environnement virtuel
python -m venv venv
source venv/bin/activate
 
# 3. Dépendances
python -m pip install pymupdf llama-index llama-index-embeddings-huggingface \
  llama-index-vector-stores-postgres sentence-transformers \
  psycopg2-binary streamlit pillow transformers torch
 
# 4. Base de données
createdb maintidoc
psql maintidoc -c "CREATE EXTENSION IF NOT EXISTS vector;"
```
 
## ▶️ Utilisation
 
1. Place ton PDF dans le dossier `data/` (par exemple `data/attention.pdf`).
2. Indexe le texte et les tableaux (bouton dans l'interface ou `python index.py`).
3. Indexe les images :
```bash
python image_index.py
```
 
4. Lance l'interface :
```bash
streamlit run app.py
```
 
5. Pose ta question dans l'interface.
## 👤 Auteure
 
**Nada**, élève ingénieure en Big Data & IA, HESTIM Engineering & Business School
GitHub : [@mahrouznada123](https://github.com/mahrouznada123)
 
