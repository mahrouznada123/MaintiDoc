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

## ✅ Fonctionnalités actuelles

- Extraction du texte, des tableaux et des images d'un PDF (PyMuPDF)
- Embeddings open source avec LlamaIndex
- Stockage des vecteurs et métadonnées dans PostgreSQL + pgvector
- Recherche sémantique des passages pertinents
- Interface Streamlit pour poser des questions

## 🚧 À venir

- Traitement des images avec CLIP et descriptions textuelles
- Génération de réponses avec un LLM open source (Qwen via Ollama)
- Agent LangChain (choix des outils, gestion du contexte)

## 🧰 Technologies

Python · LlamaIndex · PyMuPDF · Hugging Face (sentence-transformers) · PostgreSQL / pgvector · Streamlit · LangChain · Ollama

## 📁 Structure du projet

```
MaintiDoc/
├── data/          # PDF sources (document de travail : "Attention Is All You Need")
├── app.py         # Interface Streamlit
├── ingest.py      # Extraction du texte, des tableaux et des images
├── index.py       # Embeddings et indexation dans PGVector
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
  psycopg2-binary streamlit pillow

# 4. Base de données
createdb maintidoc
psql maintidoc -c "CREATE EXTENSION IF NOT EXISTS vector;"
```

## ▶️ Utilisation

1. Place ton PDF dans le dossier `data/`.
2. Lance l'interface :

```bash
streamlit run app.py
```

3. Clique sur **Indexation de tous les PDF**, puis pose ta question.

## 👤 Auteure

**Nada**, élève ingénieure en Big Data & IA, HESTIM Engineering & Business School
GitHub : [@mahrouznada123](https://github.com/mahrouznada123)