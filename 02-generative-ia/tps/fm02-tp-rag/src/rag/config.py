"""Configuration d'un pipeline RAG.

Toute expérience (TP 1, Conf A, Conf B du TP 2) est décrite par un fichier YAML
dans config/. On ne change jamais un hyperparamètre « en dur » dans le code :
c'est ce qui rend les comparaisons reproductibles (slide « Git & reproductibilité »).
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field, fields
from pathlib import Path

import yaml


@dataclass
class RAGConfig:
    name: str = "tp1"

    # Étape 2 : chunking (tailles exprimées en CARACTÈRES)
    chunking: str = "fixed"          # "fixed" ou "markdown"
    chunk_size: int = 500
    chunk_overlap: int = 50

    # Étape 3 : embeddings (le même modèle pour indexer ET pour interroger)
    embedding_model: str = "BAAI/bge-m3"

    # Étape 4 : base vectorielle
    persist_dir: str = "chroma_db"

    # Étape 5 : récupération
    top_k: int = 3
    rerank: bool = False
    rerank_model: str = "BAAI/bge-reranker-v2-m3"
    fetch_k: int = 20                 # candidats envoyés au reranker
    hybrid: bool = False              # recherche vectorielle + BM25 (bonus)

    # Étape 6 : génération
    llm_provider: str = "auto"        # "auto", "ollama" ou "gemini"
    ollama_model: str = "qwen3:8b"
    ollama_host: str = "http://localhost:11434"
    gemini_model: str = "gemini-3.1-flash-lite"
    temperature: float = 0.0
    max_tokens: int = 512

    extra: dict = field(default_factory=dict)

    @property
    def collection_name(self) -> str:
        """Une collection par configuration de chunking : Conf A et Conf B ne se mélangent pas."""
        model = self.embedding_model.split("/")[-1].lower().replace(".", "-")
        raw = f"{self.name}-{self.chunking}-{self.chunk_size}-{self.chunk_overlap}-{model}"
        return "".join(c if c.isalnum() or c in "-_." else "-" for c in raw)[:60]

    def to_dict(self) -> dict:
        return asdict(self)


def load_config(path: str | Path, **overrides) -> RAGConfig:
    """Charge un YAML de config/ ; les clés inconnues vont dans `extra`."""
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    data.update(overrides)
    known = {f.name for f in fields(RAGConfig)}
    extra = {k: v for k, v in data.items() if k not in known}
    cfg = RAGConfig(**{k: v for k, v in data.items() if k in known})
    cfg.extra.update(extra)
    return cfg
