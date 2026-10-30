"""TP 1 étape 4 : interface de chat avec Gradio.

Dans Colab :
    from app.app_gradio import build_app
    build_app(pipe).launch(share=True)     # share=True donne une URL publique temporaire

En ligne de commande (local) :
    python app/app_gradio.py --config config/tp1.yaml --corpus data/corpus

Pour aller plus loin (alternatives à tester) :
- Afficher la réponse en streaming (fonction génératrice qui fait yield).
- Ajouter un bouton « pouce bas » (flagging) et sauvegarder les mauvaises réponses
  pour enrichir le jeu de test du TP 2.
- Réécrire l'interface avec Streamlit (st.chat_input, st.chat_message) et comparer ;
  dans Colab, Streamlit demande un tunnel, d'où le choix de Gradio ici.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import gradio as gr

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from rag.config import load_config  # noqa: E402
from rag.pipeline import RAGAnswer, RAGPipeline  # noqa: E402


def format_answer(res: RAGAnswer) -> str:
    """Réponse + liste des sources consultées + temps de réponse, en Markdown."""
    # TODO : renvoyer la réponse suivie d'une section « Sources » (fichier, page, score) et des latences
    raise NotImplementedError("TODO : renvoyer la réponse suivie d'une section « Sources » (fichier, page...")


def build_app(pipe: RAGPipeline) -> gr.ChatInterface:
    def respond(message, history):
        return format_answer(pipe.ask(message))

    return gr.ChatInterface(
        fn=respond,
        title="Assistant documentaire Orbitale (RAG)",
        description=(f"Configuration **{pipe.cfg.name}** · chunks {pipe.cfg.chunking} {pipe.cfg.chunk_size} car. · "
                     f"top-k {pipe.cfg.top_k}{' + reranking' if pipe.cfg.rerank else ''}. "
                     "Corpus fictif : guides RH, télétravail, sécurité, frais, onboarding, support, formation."),
        examples=["Combien de jours de congés payés ai-je par an ?",
                  "Quel est le plafond pour une nuit d'hôtel à Paris ?",
                  "Comment signaler un courriel d'hameçonnage ?",
                  "Quelle est la mutuelle santé d'Orbitale ?"],
    )


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default=str(ROOT / "config" / "tp1.yaml"))
    ap.add_argument("--corpus", default=str(ROOT / "data" / "corpus"))
    ap.add_argument("--share", action="store_true")
    args = ap.parse_args()
    pipe = RAGPipeline(load_config(args.config))
    print(pipe.index(args.corpus))
    build_app(pipe).launch(share=args.share)
