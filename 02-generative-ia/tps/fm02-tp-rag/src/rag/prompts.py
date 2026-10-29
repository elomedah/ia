"""Étape 6a : composition du prompt RAG (slide « Synthèse & génération ancrée »).

Règle d'or : si le contexte ne contient pas la réponse, le modèle doit répondre
explicitement « Je ne sais pas d'après les documents fournis ».

Pour aller plus loin (alternatives à tester) :
- Demander une sortie structurée (JSON : answer, sources, confidence) avec le
  paramètre format d'Ollama, puis la valider avec Pydantic.
- Ajouter 1 ou 2 exemples (few-shot) de bonne réponse citée.
- Placer les chunks les plus pertinents au début ET à la fin du contexte
  (effet « lost in the middle ») et mesurer l'effet sur la fidélité.
"""
from __future__ import annotations

from .vectorstore import RetrievedChunk

IDK = "Je ne sais pas d'après les documents fournis."

SYSTEM_PROMPT = f"""Tu es l'assistant documentaire interne d'Orbitale.
Tu réponds en français, de façon concise et exacte, UNIQUEMENT à partir du CONTEXTE fourni.
Règles :
1. N'utilise aucune connaissance extérieure au CONTEXTE.
2. Cite tes sources entre crochets avec leur numéro, par exemple [1] ou [2][3].
3. Si le CONTEXTE ne permet pas de répondre, réponds exactement : « {IDK} »
4. N'invente jamais de chiffre, de délai ou de nom de formulaire."""


def format_context(chunks: list[RetrievedChunk]) -> str:
    """Numérote les chunks [1], [2]... et indique leur source (et page pour un PDF)."""
    # TODO : produire un bloc par chunk : "[n] (source: <fichier>, p. <page>)" puis le texte du chunk ; blocs séparés par une ligne vide
    raise NotImplementedError("TODO : produire un bloc par chunk : '[n] (source: <fichier>, p. <page>)' p...")


def build_user_prompt(question: str, chunks: list[RetrievedChunk]) -> str:
    return (f"CONTEXTE :\n{format_context(chunks)}\n\n"
            f"QUESTION : {question}\n\n"
            f"RÉPONSE (cite les sources) :")
