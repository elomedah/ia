import pytest

from rag.config import RAGConfig
from rag.pipeline import RAGPipeline
from rag.prompts import IDK, build_user_prompt


def make_pipe(tmp_path, fake_embedder, fake_llm, **kw):
    cfg = RAGConfig(name="test", persist_dir=str(tmp_path / "db"), embedding_model="fake", **kw)
    return RAGPipeline(cfg, embedder=fake_embedder, llm=fake_llm)


def test_index_and_retrieve(tmp_path, fake_embedder, fake_llm, corpus_dir):
    pipe = make_pipe(tmp_path, fake_embedder, fake_llm, chunk_size=400, top_k=3)
    stats = pipe.index(corpus_dir)
    assert stats["n_chunks"] > 20
    chunks = pipe.retrieve("formulaire RH-07 arrêt maladie 48 heures")
    assert len(chunks) == 3
    assert chunks[0].metadata["source"] == "01_guide_conges_absences.md"
    assert chunks[0].score >= chunks[-1].score


def test_reindex_is_idempotent(tmp_path, fake_embedder, fake_llm, corpus_dir):
    pipe = make_pipe(tmp_path, fake_embedder, fake_llm)
    n = pipe.index(corpus_dir)["n_chunks"]
    assert pipe.index(corpus_dir)["status"] == "déjà indexé"
    assert pipe.index(corpus_dir, reset=True)["n_chunks"] == n


def test_ask_returns_answer_with_sources(tmp_path, fake_embedder, fake_llm, corpus_dir):
    pipe = make_pipe(tmp_path, fake_embedder, fake_llm)
    pipe.index(corpus_dir)
    res = pipe.ask("Quel est le plafond d'hôtel à Paris ?")
    assert res.answer and res.sources
    assert res.retrieval_s >= 0 and res.generation_s >= 0
    assert res.source_files


@pytest.mark.bonus
def test_hybrid_retrieval(tmp_path, fake_embedder, fake_llm, corpus_dir):
    pipe = make_pipe(tmp_path, fake_embedder, fake_llm, hybrid=True, top_k=3, fetch_k=10)
    pipe.index(corpus_dir)
    chunks = pipe.retrieve("ticket SEC-2")
    assert any(c.metadata["source"] == "03_charte_securite_si.md" for c in chunks)


def test_prompt_contains_rule_and_numbered_sources(tmp_path, fake_embedder, fake_llm, corpus_dir):
    pipe = make_pipe(tmp_path, fake_embedder, fake_llm)
    pipe.index(corpus_dir)
    chunks = pipe.retrieve("budget formation")
    prompt = build_user_prompt("budget formation", chunks)
    assert "[1] (source" in prompt and "QUESTION" in prompt
    from rag.prompts import SYSTEM_PROMPT
    assert IDK in SYSTEM_PROMPT


@pytest.mark.tp2
def test_reranker_reorders_candidates():
    from rag.retriever import CrossEncoderReranker
    from rag.vectorstore import RetrievedChunk

    class LengthModel:                       # faux cross-encoder : score = longueur du texte
        def predict(self, pairs):
            return [len(doc) for _, doc in pairs]

    rr = CrossEncoderReranker.__new__(CrossEncoderReranker)
    rr.model = LengthModel()
    cands = [RetrievedChunk(id=str(i), text="x" * n, rank=i + 1) for i, n in enumerate([5, 50, 20])]
    out = rr.rerank("q", cands, top_k=2)
    assert [c.id for c in out] == ["1", "2"]
    assert [c.rank for c in out] == [1, 2]
