"""Étape 1 : ingestion et parsing.

Objectif : transformer des fichiers hétérogènes (Markdown, texte, PDF, HTML) en
texte propre accompagné de métadonnées (source, type, page).

Pour aller plus loin (alternatives à tester) :
- PDF complexes (tableaux, colonnes) : comparer pypdf avec pymupdf4llm ou Docling,
  qui produisent directement du Markdown et conservent mieux les tableaux.
- Ajouter un loader .docx avec python-docx, et mesurer l'effet sur le retrieval.
- Extraire des métadonnées supplémentaires (date de mise à jour, direction émettrice)
  pour filtrer la recherche (ex. « seulement les documents RH »).
"""
from __future__ import annotations

import re
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

SUPPORTED = {".md", ".txt", ".pdf", ".html", ".htm"}


@dataclass
class Document:
    text: str
    metadata: dict = field(default_factory=dict)


def clean_text(text: str) -> str:
    """Normalise les espaces sans casser la structure en paragraphes."""
    text = text.replace(" ", " ").replace("\r\n", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def load_text(path: Path) -> list[Document]:
    """Markdown et texte brut : lecture directe."""
    text = path.read_text(encoding="utf-8")
    return [Document(clean_text(text), {"source": path.name, "type": path.suffix.lstrip(".")})]


def remove_repeated_lines(pages: list[str], min_ratio: float = 0.6) -> list[str]:
    """Supprime les lignes (en-têtes, pieds de page) répétées sur la plupart des pages.

    Une ligne est considérée comme du bruit si, une fois les chiffres retirés
    (numéros de page), elle apparaît sur au moins `min_ratio` des pages.
    """
    if len(pages) < 2:
        return pages
    # TODO : repérer les lignes présentes sur au moins min_ratio des pages (en ignorant les chiffres) puis les retirer de chaque page
    raise NotImplementedError("TODO : repérer les lignes présentes sur au moins min_ratio des pages (en i...")


def load_pdf(path: Path) -> list[Document]:
    """PDF : un Document par page, en-têtes et pieds de page retirés."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [page.extract_text() or "" for page in reader.pages]
    pages = remove_repeated_lines(pages)
    return [Document(clean_text(t), {"source": path.name, "type": "pdf", "page": i + 1})
            for i, t in enumerate(pages) if t.strip()]


def load_html(path: Path) -> list[Document]:
    """HTML : ne garder que le contenu utile, titres convertis en Markdown."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    # TODO : supprimer nav/footer/script/style, garder <main> (ou <body>), convertir h1/h2/h3 en titres Markdown et li en puces
    raise NotImplementedError("TODO : supprimer nav/footer/script/style, garder <main> (ou <body>), conve...")
    title = soup.title.get_text(strip=True) if soup.title else path.stem
    return [Document(clean_text(text), {"source": path.name, "type": "html", "title": title})]


LOADERS = {".md": load_text, ".txt": load_text, ".pdf": load_pdf, ".html": load_html, ".htm": load_html}


def load_corpus(corpus_dir: str | Path) -> list[Document]:
    """Charge tous les fichiers supportés d'un dossier (ordre alphabétique)."""
    corpus_dir = Path(corpus_dir)
    docs: list[Document] = []
    for path in sorted(corpus_dir.iterdir()):
        loader = LOADERS.get(path.suffix.lower())
        if loader is None:
            continue
        docs.extend(loader(path))
    if not docs:
        raise FileNotFoundError(f"Aucun document supporté dans {corpus_dir} ({', '.join(sorted(SUPPORTED))})")
    return docs
