"""Étape 4 : stockage et recherche dans ChromaDB.

ChromaDB indexe les vecteurs avec HNSW ; on choisit la distance cosinus, cohérente
avec des embeddings normalisés. Chroma renvoie une DISTANCE (0 = identique) : on la
convertit en score de similarité (1 - distance) pour que « plus grand = meilleur ».

On fournit nous-mêmes les vecteurs (embedding_function=None) : cela garantit que
l'indexation et la requête utilisent le même Embedder.

Pour aller plus loin (alternatives à tester) :
- Filtrer par métadonnées : collection.query(..., where={"source": "02_politique_teletravail.md"}).
- Remplacer ChromaDB par FAISS (en mémoire) ou Qdrant (production, filtres riches)
  en gardant la même interface add_chunks / search.
- Monter Google Drive dans Colab et placer persist_dir sur le Drive pour ne pas
  ré-indexer à chaque session.
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .chunking import Chunk


@dataclass
class RetrievedChunk:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)
    score: float = 0.0          # similarité cosinus (ou score du reranker)
    rank: int = 0


class ChromaStore:
    def __init__(self, embedder, collection_name: str, persist_dir: str = "chroma_db"):
        import chromadb

        self.embedder = embedder
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection_name = collection_name
        self.collection = self._get_collection()

    def _get_collection(self):
        return self.client.get_or_create_collection(
            self.collection_name,
            configuration={"hnsw": {"space": "cosine"}},
            embedding_function=None,
        )

    def reset(self) -> None:
        """Vide la collection (à faire quand on change le chunking)."""
        try:
            self.client.delete_collection(self.collection_name)
        except Exception:
            pass
        self.collection = self._get_collection()

    def count(self) -> int:
        return self.collection.count()

    @staticmethod
    def _clean_meta(meta: dict) -> dict:
        """Chroma n'accepte que str, int, float, bool (pas de None ni de listes)."""
        return {k: v for k, v in meta.items() if isinstance(v, (str, int, float, bool))}

    def add_chunks(self, chunks: list[Chunk], batch_size: int = 128) -> int:
        """Vectorise et insère (upsert) les chunks par lots. Renvoie le nombre de chunks."""
        # TODO : par lots de batch_size, calculer les embeddings des textes puis collection.upsert(ids, embeddings, documents, metadatas)
        raise NotImplementedError("TODO : par lots de batch_size, calculer les embeddings des textes puis col...")

    def search(self, query: str, k: int = 3) -> list[RetrievedChunk]:
        """Renvoie les k chunks les plus proches de la question, du plus au moins similaire."""
        if self.count() == 0:
            raise RuntimeError("La collection est vide : lancez d'abord l'indexation.")
        # TODO : encoder la question, interroger la collection (n_results=k) puis construire des RetrievedChunk avec score = 1 - distance
        raise NotImplementedError("TODO : encoder la question, interroger la collection (n_results=k) puis co...")

    def all_chunks(self) -> list[RetrievedChunk]:
        """Tous les chunks indexés (utile pour BM25 en recherche hybride)."""
        res = self.collection.get(include=["documents", "metadatas"])
        return [RetrievedChunk(id=i, text=d, metadata=m or {}) for i, d, m in
                zip(res["ids"], res["documents"], res["metadatas"])]
