import json

import pytest

from eval.run_benchmark import evaluate_config, markdown_table, summarize
from rag.config import RAGConfig
from rag.pipeline import RAGPipeline

pytestmark = pytest.mark.tp2


def test_benchmark_end_to_end_without_judge(tmp_path, fake_embedder, fake_llm, corpus_dir):
    testset = [json.loads(l) for l in open(corpus_dir.parents[1] / "eval" / "testset.jsonl", encoding="utf-8")]
    summaries = []
    for name, size, k in [("a", 500, 3), ("b", 200, 5)]:
        cfg = RAGConfig(name=name, chunk_size=size, chunk_overlap=30, top_k=k, persist_dir=str(tmp_path / "db"),
                        embedding_model="fake")
        pipe = RAGPipeline(cfg, embedder=fake_embedder, llm=fake_llm)
        pipe.index(corpus_dir)
        rows = evaluate_config(pipe, testset, verbose=False)
        assert len(rows) == len(testset)
        s = summarize(rows)
        assert 0.0 <= s["hit@k"] <= 1.0
        summaries.append(s)
    assert "| config |" in markdown_table(summaries)
