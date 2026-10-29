"""Étape 3 : vectorisation avec sentence-transformers.

Règle critique (slide « Vectorisation ») : le modèle utilisé pour indexer les chunks
doit être EXACTEMENT celui utilisé pour encoder la question.

Modèle par défaut : BAAI/bge-m3 (multilingue, 1 024 dimensions, 8 192 tokens),
rapide sur le GPU T4 de Colab, plus lent sur CPU.

Pour aller plus loin (alternatives à tester) :
- intfloat/multilingual-e5-small : 5 fois plus léger, idéal sur CPU ; attention, il
  attend les préfixes « query: » et « passage: » (gérés automatiquement ci-dessous).
- sentence-transformers/all-MiniLM-L6-v2 : modèle anglais du cours, à comparer sur
  ce corpus français pour constater l'effet de la langue.
- Embeddings servis par Ollama (ex. nomic-embed-text) pour tout faire tourner via Ollama.
- Consulter le classement MTEB pour choisir un modèle selon la langue et la taille.
"""
from __future__ import annotations

import numpy as np


class Embedder:
    """Fine enveloppe autour de SentenceTransformer, avec vecteurs normalisés (cosinus)."""

    def __init__(self, model_name: str, device: str | None = None, batch_size: int = 32):
        from sentence_transformers import SentenceTransformer

        if device is None:
            try:
                import torch
                device = "cuda" if torch.cuda.is_available() else "cpu"
            except ImportError:
                device = "cpu"
        self.model_name = model_name
        self.device = device
        self.batch_size = batch_size
        self.model = SentenceTransformer(model_name, device=device)
        self.is_e5 = "e5" in model_name.lower()

    @property
    def dimension(self) -> int:
        return len(self.embed_query("test"))

    def embed_documents(self, texts: list[str]) -> np.ndarray:
        # TODO : encoder les textes avec self.model.encode (normalize_embeddings=True) ; pour un modèle e5, préfixer chaque texte par "passage: "
        raise NotImplementedError("TODO : encoder les textes avec self.model.encode (normalize_embeddings=Tru...")

    def embed_query(self, text: str) -> np.ndarray:
        # TODO : encoder la question avec le même modèle (préfixe "query: " pour e5), normalize_embeddings=True
        raise NotImplementedError("TODO : encoder la question avec le même modèle (préfixe 'query: ' pour e5)...")
