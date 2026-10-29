"""TP 2 : benchmark comparatif de configurations RAG.

    python eval/run_benchmark.py --configs config/conf_a.yaml config/conf_b.yaml
    python eval/run_benchmark.py --configs config/conf_a.yaml config/conf_b.yaml --judge none   # sans LLM juge
    python eval/run_benchmark.py --configs config/conf_a.yaml --limit 3                          # essai rapide

Pour chaque configuration : indexation dans sa propre collection, puis pour chaque
question du jeu de test : recherche, génération, métriques déterministes,
métriques DeepEval (optionnelles), latence et tokens. Résultats dans eval/results/ :
    details_<conf>.csv   une ligne par question (avec les raisons du juge)
    summary.csv          une ligne par configuration (moyennes)
    summary.md           tableau prêt à coller dans le rapport

Pour aller plus loin (alternatives à tester) :
- Lancer chaque configuration 3 fois et rapporter moyenne et écart type :
  la génération et le juge ne sont pas parfaitement déterministes.
- Ajouter conf_c.yaml (hybride + reranking) au benchmark.
- Faire varier un seul paramètre à la fois (top_k = 3, 5, 8) pour isoler son effet.
"""
from __future__ import annotations

import argparse
import csv
import json
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from rag import tracing  # noqa: E402
from rag.config import RAGConfig, load_config  # noqa: E402
from rag.pipeline import RAGPipeline  # noqa: E402
from eval.retrieval_metrics import answer_correct, hit_at_k, keyword_score, mrr, source_recall  # noqa: E402

DET_METRICS = ("hit@k", "source_recall", "mrr", "keyword_score", "answer_correct")
LLM_METRICS = ("faithfulness", "answer_relevancy", "contextual_precision", "contextual_recall")


def load_testset(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def evaluate_config(pipe: RAGPipeline, testset: list[dict], judge_metrics: dict | None = None,
                    pause_s: float = 0.0, verbose: bool = True) -> list[dict]:
    """Exécute toutes les questions avec une configuration et renvoie une ligne de résultats par question."""
    rows = []
    with tracing.tags([pipe.cfg.name], metadata={"top_k": pipe.cfg.top_k, "chunk_size": pipe.cfg.chunk_size,
                                                 "rerank": pipe.cfg.rerank}):
        for case in testset:
            # TODO : interroger le pipeline, calculer les 5 métriques déterministes à partir des sources des chunks, ajouter latences et tokens, puis les métriques du juge si judge_metrics est fourni
            raise NotImplementedError("TODO : interroger le pipeline, calculer les 5 métriques déterministes à pa...")
            rows.append(row)
            if verbose:
                print(f"[{pipe.cfg.name}] {case['id']} correct={row['answer_correct']} "
                      f"hit={row['hit@k']} sources={row['retrieved_sources']}")
    return rows


def _mean(values) -> float | None:
    vals = [v for v in values if isinstance(v, (int, float))]
    return round(statistics.mean(vals), 3) if vals else None


def summarize(rows: list[dict]) -> dict:
    """Moyenne de chaque métrique (les None, ex. hit@k hors corpus, sont ignorés)."""
    # TODO : moyenne de chaque métrique déterministe et LLM, latence médiane et maximale, tokens moyens
    raise NotImplementedError("TODO : moyenne de chaque métrique déterministe et LLM, latence médiane et ...")


def write_csv(rows: list[dict], path: Path) -> None:
    keys = [k for k in dict.fromkeys(k for r in rows for k in r) if not k.startswith("_")]
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def markdown_table(summaries: list[dict]) -> str:
    keys = [k for k in summaries[0] if k not in ("n",)]
    head = "| " + " | ".join(keys) + " |\n|" + "---|" * len(keys) + "\n"
    body = "".join("| " + " | ".join("" if s.get(k) is None else str(s.get(k)) for k in keys) + " |\n"
                   for s in summaries)
    return head + body


def main(argv=None):
    ap = argparse.ArgumentParser(description="Benchmark de configurations RAG")
    ap.add_argument("--configs", nargs="+", default=[str(ROOT / "config/conf_a.yaml"), str(ROOT / "config/conf_b.yaml")])
    ap.add_argument("--testset", default=str(ROOT / "eval/testset.jsonl"))
    ap.add_argument("--corpus", default=str(ROOT / "data/corpus"))
    ap.add_argument("--out", default=str(ROOT / "eval/results"))
    ap.add_argument("--judge", choices=["auto", "gemini", "ollama", "none"], default="auto")
    ap.add_argument("--pause", type=float, default=0.0, help="pause (s) entre deux appels au juge (quota gratuit)")
    ap.add_argument("--limit", type=int, default=None, help="n'évaluer que les N premières questions")
    ap.add_argument("--reset", action="store_true", help="réindexer même si la collection existe")
    args = ap.parse_args(argv)

    from rag.embeddings import Embedder
    from rag.llm import get_llm

    cfgs: list[RAGConfig] = [load_config(p) for p in args.configs]
    testset = load_testset(args.testset)[: args.limit]
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    embedders: dict[str, Embedder] = {}
    llm = get_llm(cfgs[0])                      # même LLM pour toutes les configurations : seule la récupération varie
    judge_metrics = None
    if args.judge != "none":
        from eval.llm_judge import build_metrics, get_judge
        judge_metrics = build_metrics(get_judge(args.judge, ollama_model=cfgs[0].ollama_model,
                                                ollama_host=cfgs[0].ollama_host))

    summaries = []
    for cfg in cfgs:
        if cfg.embedding_model not in embedders:
            embedders[cfg.embedding_model] = Embedder(cfg.embedding_model)
        pipe = RAGPipeline(cfg, embedder=embedders[cfg.embedding_model], llm=llm)
        print(f"\n=== {cfg.name} === {pipe.index(args.corpus, reset=args.reset)}")
        t0 = time.perf_counter()
        rows = evaluate_config(pipe, testset, judge_metrics, pause_s=args.pause)
        write_csv(rows, out / f"details_{cfg.name}.csv")
        s = summarize(rows)
        s["run_s"] = round(time.perf_counter() - t0, 1)
        summaries.append(s)

    write_csv(summaries, out / "summary.csv")
    (out / "summary.md").write_text(markdown_table(summaries), encoding="utf-8")
    tracing.flush()
    print("\n" + markdown_table(summaries))
    return summaries


if __name__ == "__main__":
    main()
