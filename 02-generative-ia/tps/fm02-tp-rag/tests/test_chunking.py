import pytest

from rag.chunking import chunk_documents, fixed_size_chunks, markdown_chunks
from rag.config import RAGConfig
from rag.loaders import load_corpus

TEXT = ("Phrase numéro un du test. " * 40).strip()


def test_fixed_size_respects_size():
    chunks = fixed_size_chunks(TEXT, 200, 30)
    assert len(chunks) > 1
    assert all(len(c) <= 200 for c in chunks)


def test_fixed_size_overlap():
    chunks = fixed_size_chunks(TEXT, 200, 50)
    # la fin d'un chunk se retrouve au début du suivant
    assert chunks[0][-20:].split()[-1] in chunks[1][:80]


def test_fixed_size_covers_all_text():
    chunks = fixed_size_chunks(TEXT, 150, 0)
    assert "".join(c.replace(" ", "") for c in chunks) == TEXT.replace(" ", "")


def test_invalid_overlap():
    with pytest.raises(ValueError):
        fixed_size_chunks(TEXT, 100, 100)


def test_markdown_chunks_keep_section_title():
    text = "# Titre\nIntro.\n## Congés\nVingt-cinq jours.\n## RTT\nDix jours."
    pieces = markdown_chunks(text, 300, 0)
    assert ("Congés", "Congés\nVingt-cinq jours.") in pieces


@pytest.mark.parametrize("strategy", ["fixed", "markdown"])
def test_chunk_documents_ids_unique(corpus_dir, strategy):
    cfg = RAGConfig(chunking=strategy, chunk_size=300, chunk_overlap=30)
    chunks = chunk_documents(load_corpus(corpus_dir), cfg)
    assert len({c.id for c in chunks}) == len(chunks)
    assert all(c.metadata["source"] for c in chunks)
