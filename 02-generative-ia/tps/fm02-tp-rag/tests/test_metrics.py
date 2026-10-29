import pytest
from eval.retrieval_metrics import answer_correct, hit_at_k, keyword_score, mrr, normalize, source_recall

pytestmark = pytest.mark.tp2


def test_normalize():
    assert normalize("Délai  de 48 heures") == "delai de 48 heures"


def test_hit_recall_mrr():
    ranked = ["b.md", "a.md", "a.md"]
    assert hit_at_k(ranked, ["a.md"]) == 1.0
    assert hit_at_k(ranked, ["z.md"]) == 0.0
    assert hit_at_k(ranked, []) is None
    assert source_recall(ranked, ["a.md", "c.md"]) == 0.5
    assert mrr(ranked, ["a.md"]) == 0.5
    assert mrr(ranked, ["z.md"]) == 0.0


def test_keywords_and_correctness():
    case = {"type": "factuel", "expected_sources": ["x"], "expected_keywords": ["1 500|1500", "HT"]}
    assert keyword_score("Le budget est de 1500 € HT.", case["expected_keywords"]) == 1.0
    assert answer_correct(case, "Le budget est de 1 500 euros HT [1].") == 1.0
    assert answer_correct(case, "Je ne sais pas d'après les documents fournis.") == 0.0
    oos = {"type": "hors-corpus", "expected_sources": [], "expected_keywords": ["je ne sais pas"]}
    assert answer_correct(oos, "Je ne sais pas d'après les documents fournis.") == 1.0
