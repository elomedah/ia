"""Étape 5 : récupération, reranking et recherche hybride.

- Recherche vectorielle simple : les top_k chunks les plus proches (Conf A du TP 2).
- Reranking (Conf B) : on récupère fetch_k candidats, puis un cross-encoder lit
  chaque paire (question, chunk) et les réordonne finement ; on garde les top_k.
- Recherche hybride (bonus) : fusion du classement vectoriel et du classement
  lexical BM25 par Reciprocal Rank Fusion (RRF). Utile pour les mots-clés exacts
  (identifiants comme « RH-07 » ou « SEC-2 »), que les embeddings captent mal.

Pour aller plus loin (alternatives à tester) :
- Reranker plus léger sur CPU : cross-encoder/mmarco-mMiniLMv2-L12-H384-v1.
- Faire varier fetch_k (10, 20, 50) : gain de qualité contre temps de reranking.
- Combiner hybride + reranking (Conf C) et la comparer à A et B dans le TP 2.
- Requêtes reformulées (multi-query, HyDE) générées par le LLM avant la recherche.
"""
from __future__ import annotations

import re
import unicodedata

from .config import RAGConfig
from .vectorstore import ChromaStore, RetrievedChunk


class CrossEncoderReranker:
    def __init__(self, model_name: str, device: str | None = None):
        from sentence_transformers import CrossEncoder

        self.model_name = model_name
        self.model = CrossEncoder(model_name, max_length=512, device=device)

    def rerank(self, query: str, candidates: list[RetrievedChunk], top_k: int) -> list[RetrievedChunk]:
        """Réordonne les candidats par score du cross-encoder et garde les top_k."""
        if not candidates:
            return []
        # TODO : scorer chaque paire (query, chunk.text) avec self.model.predict, trier par score décroissant, garder top_k et mettre à jour score et rank
        raise NotImplementedError("TODO : scorer chaque paire (query, chunk.text) avec self.model.predict, tr...")


def _tokenize(text: str) -> list[str]:
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text)


class BM25Index:
    """Index lexical BM25 sur les chunks déjà présents dans la base vectorielle."""

    def __init__(self, chunks: list[RetrievedChunk]):
        from rank_bm25 import BM25Okapi

        self.chunks = chunks
        self.bm25 = BM25Okapi([_tokenize(c.text) for c in chunks])

    def search(self, query: str, k: int) -> list[RetrievedChunk]:
        scores = self.bm25.get_scores(_tokenize(query))
        order = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
        return [RetrievedChunk(id=self.chunks[i].id, text=self.chunks[i].text, metadata=self.chunks[i].metadata,
                               score=float(scores[i]), rank=r) for r, i in enumerate(order, 1)]


def reciprocal_rank_fusion(rankings: list[list[RetrievedChunk]], k: int = 60) -> list[RetrievedChunk]:
    """RRF : score(d) = somme sur les classements de 1 / (k + rang(d))."""
    # TODO : (bonus) additionner 1 / (k + rang) pour chaque chunk dans chaque classement, puis trier par score décroissant
    raise NotImplementedError("TODO : (bonus) additionner 1 / (k + rang) pour chaque chunk dans chaque cl...")


class Retriever:
    def __init__(self, store: ChromaStore, cfg: RAGConfig, reranker: CrossEncoderReranker | None = None):
        self.store = store
        self.cfg = cfg
        self.reranker = reranker
        if cfg.rerank and reranker is None:
            self.reranker = CrossEncoderReranker(cfg.rerank_model)
        self._bm25: BM25Index | None = None

    def refresh_lexical_index(self) -> None:
        """À appeler après une (ré)indexation si la recherche hybride est activée."""
        self._bm25 = BM25Index(self.store.all_chunks()) if self.cfg.hybrid else None

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        cfg = self.cfg
        n_candidates = cfg.fetch_k if (cfg.rerank or cfg.hybrid) else cfg.top_k
        candidates = self.store.search(query, n_candidates)
        if cfg.hybrid:
            if self._bm25 is None:
                self.refresh_lexical_index()
            candidates = reciprocal_rank_fusion([candidates, self._bm25.search(query, n_candidates)])
        if cfg.rerank:
            return self.reranker.rerank(query, candidates, cfg.top_k)
        return candidates[:cfg.top_k]
