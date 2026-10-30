"""Étape 2 : chunking.

Deux stratégies vues en cours :
- "fixed"    : taille fixe en caractères avec chevauchement (overlap), en coupant
               de préférence sur une fin de phrase ou un espace ;
- "markdown" : découpage par sections (titres Markdown), puis taille fixe si une
               section dépasse chunk_size. Chaque chunk garde le titre de sa section.

Trop petits, les chunks perdent leur contexte ; trop grands, ils diluent le signal
sémantique et coûtent des tokens. C'est exactement ce que mesure le TP 2.

Pour aller plus loin (alternatives à tester) :
- Comparer avec RecursiveCharacterTextSplitter de LangChain (langchain-text-splitters).
- Raisonner en tokens plutôt qu'en caractères (tokenizer du modèle d'embedding) :
  bge-m3 accepte 8 192 tokens, multilingual-e5-small seulement 512.
- Chunking sémantique : couper là où la similarité entre phrases consécutives chute.
- Préfixer chaque chunk par le titre du document (« contextual chunk headers »).
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .config import RAGConfig
from .loaders import Document


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict = field(default_factory=dict)


def _cut_position(text: str, start: int, end: int) -> int:
    """Cherche une coupure « propre » dans la seconde moitié de la fenêtre [start, end)."""
    if end >= len(text):
        return len(text)
    window = text[start:end]
    half = len(window) // 2
    for sep in ("\n\n", "\n", ". ", " ; ", " "):
        pos = window.rfind(sep, half)
        if pos != -1:
            return start + pos + len(sep)
    return end


def fixed_size_chunks(text: str, size: int, overlap: int) -> list[str]:
    """Découpe `text` en morceaux d'au plus `size` caractères, avec `overlap` caractères
    de recouvrement entre deux morceaux consécutifs.
    """
    if size <= 0:
        raise ValueError("size doit être > 0")
    if not 0 <= overlap < size:
        raise ValueError("overlap doit être dans [0, size)")
    text = text.strip()
    if not text:
        return []
    # TODO : avancer par fenêtres de `size` caractères, couper proprement avec _cut_position, puis repartir `overlap` caractères avant la fin du morceau
    raise NotImplementedError("TODO : avancer par fenêtres de `size` caractères, couper proprement avec _...")


HEADING = re.compile(r"^(#{1,6})\s+(.+)$", re.MULTILINE)


def split_markdown_sections(text: str) -> list[tuple[str, str]]:
    """Renvoie une liste (titre de section, contenu). Le texte avant le premier titre a un titre vide."""
    sections, last_title, last_pos = [], "", 0
    for m in HEADING.finditer(text):
        body = text[last_pos:m.start()].strip()
        if body:
            sections.append((last_title, body))
        last_title, last_pos = m.group(2).strip(), m.end()
    body = text[last_pos:].strip()
    if body:
        sections.append((last_title, body))
    return sections


def markdown_chunks(text: str, size: int, overlap: int) -> list[tuple[str, str]]:
    """Découpe par sections Markdown puis, si besoin, en taille fixe. Renvoie (section, texte)."""
    out = []
    for title, body in split_markdown_sections(text):
        prefix = f"{title}\n" if title else ""
        for piece in fixed_size_chunks(body, max(size - len(prefix), size // 2), overlap):
            out.append((title, prefix + piece))
    return out


def chunk_documents(docs: list[Document], cfg: RAGConfig) -> list[Chunk]:
    """Applique la stratégie de cfg.chunking à tous les documents.

    Chaque chunk reçoit un identifiant stable « source::page::index » et hérite
    des métadonnées du document (source, type, page...).
    """
    chunks: list[Chunk] = []
    for doc in docs:
        src = doc.metadata.get("source", "doc")
        page = doc.metadata.get("page", 0)
        if cfg.chunking == "markdown":
            pieces = markdown_chunks(doc.text, cfg.chunk_size, cfg.chunk_overlap)
        elif cfg.chunking == "fixed":
            pieces = [("", t) for t in fixed_size_chunks(doc.text, cfg.chunk_size, cfg.chunk_overlap)]
        else:
            raise ValueError(f"Stratégie de chunking inconnue : {cfg.chunking}")
        for i, (section, text) in enumerate(pieces):
            meta = {**doc.metadata, "chunk_index": i, "section": section}
            chunks.append(Chunk(id=f"{src}::{page}::{i}", text=text, metadata=meta))
    return chunks


def chunk_stats(chunks: list[Chunk]) -> dict:
    """Statistiques utiles pour justifier un choix de chunking dans le README."""
    lengths = sorted(len(c.text) for c in chunks)
    if not lengths:
        return {"n_chunks": 0}
    return {
        "n_chunks": len(lengths),
        "min": lengths[0],
        "median": lengths[len(lengths) // 2],
        "max": lengths[-1],
        "mean": round(sum(lengths) / len(lengths), 1),
    }
