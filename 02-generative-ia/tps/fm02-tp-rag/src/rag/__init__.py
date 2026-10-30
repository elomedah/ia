"""Mini-framework RAG pédagogique du module FM02 (IA générative).

Chaque étape du pipeline vu en cours a son module :

    loaders.py      étape 1  ingestion et parsing (md, txt, pdf, html)
    chunking.py     étape 2  découpage en chunks
    embeddings.py   étape 3  vectorisation (sentence-transformers)
    vectorstore.py  étape 4  stockage et recherche (ChromaDB)
    retriever.py    étape 5  récupération, reranking, recherche hybride
    prompts.py      étape 6  prompt RAG et règle d'or
    llm.py          étape 6  génération (Ollama, Gemini en secours)
    pipeline.py     assemblage des étapes
    tracing.py      observabilité (Langfuse, optionnel)
"""
from .config import RAGConfig, load_config

__all__ = ["RAGConfig", "load_config"]
