"""Assemblage du pipeline RAG : indexation puis question-réponse.

    pipe = RAGPipeline(load_config("config/tp1.yaml"))
    pipe.index("data/corpus")
    res = pipe.ask("Combien de jours de congés ?")
    print(res.answer, res.sources)

Les composants lourds (modèle d'embedding, reranker, LLM) peuvent être injectés :
le TP 2 partage ainsi le même Embedder et le même LLM entre Conf A et Conf B.

Pour aller plus loin (alternatives à tester) :
- Mémoire de conversation : reformuler la question avec l'historique avant la
  recherche (« condense question »), pour gérer « et pour les RTT ? ».
- Réécrire ce pipeline avec LangChain (Chroma, HuggingFaceEmbeddings, ChatOllama)
  et comparer la lisibilité, la flexibilité et les résultats.
- Mettre en cache les réponses aux questions déjà posées.
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path

from . import tracing
from .chunking import chunk_documents, chunk_stats
from .config import RAGConfig
from .loaders import load_corpus
from .prompts import SYSTEM_PROMPT, build_user_prompt
from .vectorstore import ChromaStore, RetrievedChunk


@dataclass
class RAGAnswer:
    question: str
    answer: str
    sources: list[RetrievedChunk] = field(default_factory=list)
    model: str = ""
    retrieval_s: float = 0.0
    generation_s: float = 0.0
    prompt_tokens: int | None = None
    completion_tokens: int | None = None

    @property
    def contexts(self) -> list[str]:
        return [c.text for c in self.sources]

    @property
    def source_files(self) -> list[str]:
        seen = []
        for c in self.sources:
            s = c.metadata.get("source")
            if s and s not in seen:
                seen.append(s)
        return seen


class RAGPipeline:
    def __init__(self, cfg: RAGConfig, embedder=None, llm=None, reranker=None):
        from .embeddings import Embedder
        from .retriever import Retriever

        self.cfg = cfg
        self.embedder = embedder or Embedder(cfg.embedding_model)
        self.store = ChromaStore(self.embedder, cfg.collection_name, cfg.persist_dir)
        self.retriever = Retriever(self.store, cfg, reranker=reranker)
        self._llm = llm

    @property
    def llm(self):
        if self._llm is None:
            from .llm import get_llm
            self._llm = get_llm(self.cfg)
        return self._llm

    def index(self, corpus_dir: str | Path, reset: bool = False) -> dict:
        """Charge, découpe et indexe le corpus. Ne réindexe pas si la collection est déjà pleine."""
        if reset:
            self.store.reset()
        if self.store.count() > 0:
            self.retriever.refresh_lexical_index()
            return {"status": "déjà indexé", "n_chunks": self.store.count(), "collection": self.cfg.collection_name}
        docs = load_corpus(corpus_dir)
        chunks = chunk_documents(docs, self.cfg)
        t0 = time.perf_counter()
        self.store.add_chunks(chunks)
        self.retriever.refresh_lexical_index()
        return {"status": "indexé", "n_documents": len(docs), **chunk_stats(chunks),
                "indexing_s": round(time.perf_counter() - t0, 2), "collection": self.cfg.collection_name}

    @tracing.observe(name="retrieval", as_type="retriever")
    def retrieve(self, question: str) -> list[RetrievedChunk]:
        chunks = self.retriever.retrieve(question)
        tracing.update_span(input=question, output=[{"id": c.id, "score": round(c.score, 4)} for c in chunks])
        return chunks

    @tracing.observe(name="generation", as_type="generation")
    def generate(self, question: str, chunks: list[RetrievedChunk]):
        user = build_user_prompt(question, chunks)
        resp = self.llm.generate(SYSTEM_PROMPT, user)
        tracing.update_generation(input=user, output=resp.text, model=resp.model,
                                  usage_details={"input": resp.prompt_tokens or 0, "output": resp.completion_tokens or 0})
        return resp

    @tracing.observe(name="rag-ask")
    def ask(self, question: str) -> RAGAnswer:
        """Question -> recherche -> prompt -> réponse ancrée, avec mesures de latence."""
        # TODO : chronométrer self.retrieve puis self.generate et construire un RAGAnswer complet (réponse, sources, modèle, latences, tokens)
        raise NotImplementedError("TODO : chronométrer self.retrieve puis self.generate et construire un RAGA...")
        tracing.update_span(input=question, output=result.answer,
                            metadata={"config": self.cfg.name, "sources": result.source_files})
        return result
