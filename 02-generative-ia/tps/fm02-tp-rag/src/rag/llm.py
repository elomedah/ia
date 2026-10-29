"""Étape 6b : génération avec un LLM.

Deux fournisseurs derrière la même interface `generate(system, user)` :
- Ollama : le LLM du cours, qui tourne dans Colab sur le GPU T4 (ou en local) ;
- Gemini : API cloud de secours quand aucun GPU n'est disponible.
  ATTENTION : l'offre gratuite peut réutiliser les données envoyées. Ne jamais y
  envoyer de données personnelles ou confidentielles (ici, le corpus est fictif).

provider="auto" essaie Ollama, puis Gemini si une clé GEMINI_API_KEY est définie.

Pour aller plus loin (alternatives à tester) :
- Comparer plusieurs modèles Ollama : qwen3:8b, llama3.1:8b, mistral:7b (même code).
- Streaming de la réponse dans l'interface Gradio (stream=True).
- Tout LLM exposant une API compatible OpenAI (vLLM, Groq, LM Studio) peut être
  ajouté en écrivant une troisième classe avec la même méthode generate().
"""
from __future__ import annotations

import os
import re
import time
from dataclasses import dataclass


@dataclass
class LLMResponse:
    text: str
    model: str
    latency_s: float
    prompt_tokens: int | None = None
    completion_tokens: int | None = None


THINK = re.compile(r"<think>.*?</think>", re.DOTALL)


def strip_thinking(text: str) -> str:
    """Retire un éventuel raisonnement <think>...</think> (modèles Qwen3, DeepSeek-R1)."""
    return THINK.sub("", text or "").strip()


class OllamaLLM:
    def __init__(self, model: str, host: str = "http://localhost:11434", temperature: float = 0.0,
                 max_tokens: int = 512):
        import ollama

        self.client = ollama.Client(host=host)
        self.model, self.host = model, host
        self.temperature, self.max_tokens = temperature, max_tokens

    def is_available(self) -> bool:
        """Le serveur répond-il et le modèle est-il téléchargé ?"""
        try:
            names = {m.model for m in self.client.list().models}
        except Exception:
            return False
        return self.model in names or f"{self.model}:latest" in names

    def generate(self, system: str, user: str) -> LLMResponse:
        # TODO : appeler self.client.chat avec un message system et un message user, options temperature et num_predict, think=False ; renvoyer un LLMResponse (texte nettoyé, latence, prompt_eval_count, eval_count)
        raise NotImplementedError("TODO : appeler self.client.chat avec un message system et un message user,...")


class GeminiLLM:
    def __init__(self, model: str, api_key: str | None = None, temperature: float = 0.0,
                 max_tokens: int = 512, max_retries: int = 5):
        from google import genai

        api_key = api_key or os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
        if not api_key:
            raise RuntimeError("Aucune clé GEMINI_API_KEY : créez-en une sur https://aistudio.google.com")
        self.client = genai.Client(api_key=api_key)
        self.model, self.temperature, self.max_tokens = model, temperature, max_tokens
        self.max_retries = max_retries

    def generate(self, system: str, user: str) -> LLMResponse:
        from google.genai import errors, types

        config = types.GenerateContentConfig(system_instruction=system, temperature=self.temperature,
                                             max_output_tokens=self.max_tokens)
        t0 = time.perf_counter()
        for attempt in range(self.max_retries):
            try:
                resp = self.client.models.generate_content(model=self.model, contents=user, config=config)
                break
            except errors.APIError as exc:
                # 429 = quota de l'offre gratuite dépassé : on attend puis on réessaie
                if exc.code in (429, 500, 503) and attempt < self.max_retries - 1:
                    time.sleep(min(60, 5 * 2 ** attempt))
                    continue
                raise
        latency = time.perf_counter() - t0
        usage = resp.usage_metadata
        return LLMResponse(text=(resp.text or "").strip(), model=f"gemini/{self.model}", latency_s=latency,
                           prompt_tokens=getattr(usage, "prompt_token_count", None),
                           completion_tokens=getattr(usage, "candidates_token_count", None))


def get_llm(cfg) -> OllamaLLM | GeminiLLM:
    """Choisit le LLM selon cfg.llm_provider ("auto", "ollama" ou "gemini")."""
    provider = cfg.llm_provider
    if provider in ("auto", "ollama"):
        llm = OllamaLLM(cfg.ollama_model, cfg.ollama_host, cfg.temperature, cfg.max_tokens)
        if llm.is_available():
            return llm
        if provider == "ollama":
            raise RuntimeError(f"Ollama ne répond pas sur {cfg.ollama_host} ou le modèle {cfg.ollama_model} "
                               f"n'est pas téléchargé (ollama pull {cfg.ollama_model}).")
        print(f"[llm] Ollama indisponible ({cfg.ollama_model}) : bascule sur Gemini ({cfg.gemini_model}).")
    return GeminiLLM(cfg.gemini_model, temperature=cfg.temperature, max_tokens=cfg.max_tokens)
