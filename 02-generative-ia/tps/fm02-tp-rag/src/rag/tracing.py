"""Observabilité avec Langfuse (optionnelle).

Si LANGFUSE_PUBLIC_KEY et LANGFUSE_SECRET_KEY sont définies (compte gratuit sur
https://cloud.langfuse.com), chaque appel du pipeline produit une trace :
retrieval, reranking et génération, avec latence et nombre de tokens.
Sans clés, les fonctions de ce module ne font rien : le code tourne à l'identique.

Variables d'environnement : LANGFUSE_PUBLIC_KEY, LANGFUSE_SECRET_KEY,
LANGFUSE_BASE_URL (ex. https://cloud.langfuse.com, ou l'URL de votre instance).

Pour aller plus loin (alternatives à tester) :
- Arize Phoenix (open source, basé sur OpenTelemetry) comme alternative à Langfuse.
- Envoyer les scores DeepEval du TP 2 dans Langfuse (create_score) pour les voir
  à côté de chaque trace.
"""
from __future__ import annotations

import contextlib
import functools
import os


def enabled() -> bool:
    return bool(os.environ.get("LANGFUSE_PUBLIC_KEY") and os.environ.get("LANGFUSE_SECRET_KEY"))


def observe(name: str | None = None, as_type: str | None = None):
    """Décorateur : trace la fonction dans Langfuse si activé, sinon ne fait rien.

    L'activation est vérifiée à chaque appel : on peut donc définir les clés dans
    le notebook après l'import du module. Les entrées et sorties ne sont pas
    capturées automatiquement (on les renseigne avec update_span) pour éviter de
    sérialiser des objets volumineux comme le pipeline lui-même.
    """
    def decorator(func):
        traced = None

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal traced
            if not enabled():
                return func(*args, **kwargs)
            if traced is None:
                try:
                    from langfuse import observe as lf_observe
                except ImportError:
                    return func(*args, **kwargs)
                opts = {"name": name or func.__name__, "capture_input": False, "capture_output": False}
                if as_type:
                    opts["as_type"] = as_type
                traced = lf_observe(**opts)(func)
            return traced(*args, **kwargs)
        return wrapper
    return decorator


def update_span(**kwargs) -> None:
    """Renseigne input, output ou metadata de l'observation en cours."""
    if not enabled():
        return
    try:
        from langfuse import get_client
        get_client().update_current_span(**kwargs)
    except Exception:
        pass


def update_generation(**kwargs) -> None:
    """Ajoute modèle et tokens à l'observation de type « generation » en cours."""
    if not enabled():
        return
    try:
        from langfuse import get_client
        get_client().update_current_generation(**kwargs)
    except Exception:
        pass


def tags(tag_list: list[str], metadata: dict | None = None):
    """Contexte qui étiquette toutes les traces créées à l'intérieur (ex. ["conf_a"])."""
    if not enabled():
        return contextlib.nullcontext()
    try:
        from langfuse import propagate_attributes
        return propagate_attributes(tags=tag_list, metadata={k: str(v) for k, v in (metadata or {}).items()})
    except Exception:
        return contextlib.nullcontext()


def flush() -> None:
    if enabled():
        try:
            from langfuse import get_client
            get_client().flush()
        except Exception:
            pass
