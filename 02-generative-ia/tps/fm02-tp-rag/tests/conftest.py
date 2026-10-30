"""Outils de test SANS GPU NI RÉSEAU : un faux modèle d'embedding et un faux LLM.

Ils permettent de vérifier la plomberie du pipeline (chargement, chunking,
indexation, recherche, métriques) en quelques secondes, avant de lancer les
vrais modèles sur Colab :  pytest
"""
import hashlib
import re
import unicodedata
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "corpus"


def _tokens(text):
    text = unicodedata.normalize("NFD", text.lower())
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", text)


class FakeEmbedder:
    """Sac de mots haché : deux textes qui partagent des mots ont des vecteurs proches."""
    model_name = "fake-hashing"

    def __init__(self, dim=512):
        self.dim = dim

    def _vec(self, text):
        v = np.zeros(self.dim, dtype="float32")
        for t in _tokens(text):
            if len(t) > 2:
                v[int(hashlib.md5(t.encode()).hexdigest(), 16) % self.dim] += 1.0
        n = np.linalg.norm(v)
        return v / n if n else v + 1.0 / np.sqrt(self.dim)

    def embed_documents(self, texts):
        return np.stack([self._vec(t) for t in texts])

    def embed_query(self, text):
        return self._vec(text)


class FakeLLM:
    """Recopie la première phrase du contexte [1] ; « je ne sais pas » si le contexte est vide."""

    def generate(self, system, user):
        from rag.llm import LLMResponse
        m = re.search(r"\[1\] \(source[^\n]*\)\n(.+?)(?:\n|$)", user)
        text = f"{m.group(1)} [1]" if m else "Je ne sais pas d'après les documents fournis."
        return LLMResponse(text=text, model="fake", latency_s=0.0, prompt_tokens=len(user) // 4, completion_tokens=20)


@pytest.fixture
def fake_embedder():
    return FakeEmbedder()


@pytest.fixture
def fake_llm():
    return FakeLLM()


@pytest.fixture
def corpus_dir():
    return CORPUS
