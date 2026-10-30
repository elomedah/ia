"""TP 2 : métriques « LLM-as-a-judge » avec DeepEval (la RAG Triad du cours).

    RAG Triad (slide)         Métrique DeepEval
    Fidélité                  FaithfulnessMetric          (la réponse vient-elle du contexte ?)
    Pertinence de la réponse  AnswerRelevancyMetric       (répond-elle à la question ?)
    Pertinence du contexte    ContextualPrecisionMetric   (les bons chunks sont-ils en tête ?)
                              ContextualRecallMetric      (le contexte couvre-t-il la réponse attendue ?)

Choix du juge : de préférence un modèle DIFFÉRENT et plus fort que celui qui
génère (Gemini juge les réponses de qwen3:8b), pour limiter l'auto-complaisance.
Avec l'offre gratuite de Gemini, on espace les appels (paramètre `pause_s`).

On appelle metric.measure(test_case) cas par cas, en mode synchrone : c'est plus
lent que deepeval.evaluate(), mais robuste dans Colab et facile à déboguer.

Pour aller plus loin (alternatives à tester) :
- RAGAS (faithfulness, answer_relevancy, context_precision, context_recall) avec
  le même juge, et comparer les deux frameworks sur les mêmes réponses.
- Changer de juge (Ollama qwen3:8b contre Gemini) et mesurer l'écart de scores :
  le juge est lui-même une source de variance.
- Écrire une métrique sur mesure avec GEval (ex. « la réponse cite-t-elle une source ? »).
"""
from __future__ import annotations

import os
import time

os.environ.setdefault("DEEPEVAL_TELEMETRY_OPT_OUT", "YES")

METRIC_NAMES = ("faithfulness", "answer_relevancy", "contextual_precision", "contextual_recall")


def get_judge(provider: str = "auto", gemini_model: str = "gemini-3.1-flash-lite",
              ollama_model: str = "qwen3:8b", ollama_host: str = "http://localhost:11434"):
    """Renvoie un modèle juge DeepEval : Gemini si une clé existe (provider auto), sinon Ollama."""
    from deepeval.models import GeminiModel, OllamaModel

    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if provider == "gemini" or (provider == "auto" and key):
        if not key:
            raise RuntimeError("Juge Gemini demandé sans GEMINI_API_KEY.")
        return GeminiModel(model=gemini_model, api_key=key, temperature=0)
    return OllamaModel(model=ollama_model, base_url=ollama_host, temperature=0)


def build_metrics(judge, names=METRIC_NAMES) -> dict:
    from deepeval.metrics import (AnswerRelevancyMetric, ContextualPrecisionMetric,
                                  ContextualRecallMetric, FaithfulnessMetric)

    classes = {"faithfulness": FaithfulnessMetric, "answer_relevancy": AnswerRelevancyMetric,
               "contextual_precision": ContextualPrecisionMetric, "contextual_recall": ContextualRecallMetric}
    return {n: classes[n](model=judge, async_mode=False, include_reason=True, threshold=0.7) for n in names}


def judge_case(metrics: dict, question: str, answer: str, contexts: list[str], ground_truth: str,
               pause_s: float = 0.0, retries: int = 2) -> dict:
    """Calcule chaque métrique pour un cas ; renvoie {nom: score, nom_reason: raison}."""
    from deepeval.test_case import LLMTestCase

    # TODO : construire un LLMTestCase (input, actual_output, expected_output, retrieval_context) puis, pour chaque métrique, appeler measure() et récupérer score et reason ; en cas d'erreur, réessayer puis mettre None
    raise NotImplementedError("TODO : construire un LLMTestCase (input, actual_output, expected_output, r...")
