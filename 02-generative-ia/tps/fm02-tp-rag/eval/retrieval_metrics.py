"""TP 2 : métriques déterministes (sans LLM juge).

Elles sont gratuites, instantanées et reproductibles : à calculer AVANT les
métriques « LLM-as-a-judge », qui sont lentes, coûteuses et elles-mêmes bruitées.

- hit@k           : au moins une source attendue figure-t-elle dans les k chunks ?
- source_recall   : part des sources attendues retrouvées (questions multi-documents)
- mrr             : 1 / rang du premier chunk issu d'une source attendue
- keyword_score   : part des mots-clés attendus présents dans la réponse
- answer_correct  : réponse jugée correcte (mots-clés présents, ou « je ne sais pas »
                    pour une question hors corpus)

Pour aller plus loin (alternatives à tester) :
- Annoter les chunks attendus (et pas seulement les fichiers) pour un recall plus fin.
- Ajouter nDCG@k, qui tient compte de la position de chaque chunk pertinent.
- Comparer keyword_score au jugement du LLM : où divergent-ils, et pourquoi ?
"""
from __future__ import annotations

import re
import unicodedata


def normalize(text: str) -> str:
    """Minuscules, sans accents, espaces normalisés (y compris insécables)."""
    text = unicodedata.normalize("NFD", (text or "").replace(" ", " ").replace(" ", " ").lower())
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", text).strip()


def hit_at_k(retrieved_sources: list[str], expected: list[str]) -> float | None:
    # TODO : renvoyer None si aucune source attendue (question hors corpus), sinon 1.0 si au moins une source attendue est retrouvée, 0.0 sinon
    raise NotImplementedError("TODO : renvoyer None si aucune source attendue (question hors corpus), sin...")


def source_recall(retrieved_sources: list[str], expected: list[str]) -> float | None:
    # TODO : part des sources attendues présentes parmi les sources retrouvées (None si aucune source attendue)
    raise NotImplementedError("TODO : part des sources attendues présentes parmi les sources retrouvées (...")


def mrr(retrieved_sources_ranked: list[str], expected: list[str]) -> float | None:
    """retrieved_sources_ranked : la source de chaque chunk, dans l'ordre (doublons possibles)."""
    # TODO : 1 / rang (à partir de 1) du premier chunk dont la source est attendue ; 0.0 si aucun ; None si aucune source attendue
    raise NotImplementedError("TODO : 1 / rang (à partir de 1) du premier chunk dont la source est attend...")


def is_idk(answer: str) -> bool:
    return "je ne sais pas" in normalize(answer)


def keyword_score(answer: str, groups: list[str]) -> float:
    """Chaque groupe accepte des variantes séparées par « | » (ex. "1 500|1500")."""
    if not groups:
        return 1.0
    ans = normalize(answer)
    found = sum(any(normalize(alt) in ans for alt in g.split("|")) for g in groups)
    return found / len(groups)


def answer_correct(case: dict, answer: str) -> float:
    if case.get("type") == "hors-corpus" or not case.get("expected_sources"):
        return 1.0 if is_idk(answer) else 0.0
    if is_idk(answer):
        return 0.0
    return 1.0 if keyword_score(answer, case.get("expected_keywords", [])) == 1.0 else 0.0
