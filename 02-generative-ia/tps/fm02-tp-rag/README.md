# FM02 · TP RAG · Kit de démarrage

Kit de démarrage des deux TP du module **IA Générative** (M2 Lead Developer Full Stack, ENSITECH) : un chatbot RAG sur une documentation d'entreprise (TP 1), puis son évaluation comparative (TP 2).

**Ce qui est fourni** : l'arborescence, le corpus, la configuration, les squelettes de code, les notebooks Colab, les tests et 5 questions du jeu de test.
**Ce que vous écrivez** : les fonctions marquées `TODO` (elles lèvent `NotImplementedError` tant qu'elles ne sont pas écrites), la justification du chunking, 10 questions de test et les deux rapports.

| Fichier | À compléter | TP |
|---|---|---|
| `src/rag/loaders.py` | `remove_repeated_lines`, nettoyage HTML dans `load_html` | 1 |
| `src/rag/chunking.py` | `fixed_size_chunks` | 1 |
| `src/rag/embeddings.py` | `embed_documents`, `embed_query` | 1 |
| `src/rag/vectorstore.py` | `add_chunks`, `search` | 1 |
| `src/rag/prompts.py` | `format_context` | 1 |
| `src/rag/llm.py` | `OllamaLLM.generate` | 1 |
| `src/rag/pipeline.py` | `ask` | 1 |
| `app/app_gradio.py` | `format_answer` | 1 |
| `config/tp1.yaml` + ce README | justification du chunking | 1 |
| `src/rag/retriever.py` | `CrossEncoderReranker.rerank` (+ bonus `reciprocal_rank_fusion`) | 2 |
| `eval/retrieval_metrics.py` | `hit_at_k`, `source_recall`, `mrr` | 2 |
| `eval/llm_judge.py` | `judge_case` | 2 |
| `eval/run_benchmark.py` | boucle de `evaluate_config`, `summarize` | 2 |
| `eval/testset.jsonl` | 10 questions supplémentaires | 2 |

Avancez étape par étape : `python -m pytest -m "not tp2 and not bonus"` vérifie le TP 1, `python -m pytest` vérifie tout (TP 2 et bonus inclus) et indique les fonctions qui restent à écrire.

## Justification du chunking (TP 1, à compléter)

_Stratégie, taille, chevauchement retenus, et 3 à 5 arguments chiffrés._

## Arborescence

```
fm02-tp-rag/
├── README.md
├── requirements.txt            # TP 1
├── requirements-eval.txt       # TP 2 (DeepEval, Langfuse, pandas)
├── .env.example                # modèle de fichier de clés (jamais commité)
├── pytest.ini
├── config/
│   ├── tp1.yaml                # configuration du chatbot (chunking justifié)
│   ├── conf_a.yaml             # TP 2 : chunks 500, top-k 3
│   ├── conf_b.yaml             # TP 2 : chunks 200, top-k 5 + reranking
│   └── conf_c.yaml             # pour aller plus loin : sections + hybride + reranking
├── data/corpus/                # documentation interne fictive d'Orbitale (md, txt, pdf, html)
├── src/rag/                    # le pipeline, une étape du cours par module
│   ├── config.py               # dataclass RAGConfig + lecture YAML
│   ├── loaders.py              # étape 1 : ingestion et parsing
│   ├── chunking.py             # étape 2 : chunking fixe ou par sections
│   ├── embeddings.py           # étape 3 : sentence-transformers
│   ├── vectorstore.py          # étape 4 : ChromaDB (cosinus)
│   ├── retriever.py            # étape 5 : top-k, reranking, hybride BM25
│   ├── prompts.py              # étape 6 : prompt RAG et règle d'or
│   ├── llm.py                  # étape 6 : Ollama, Gemini en secours
│   ├── pipeline.py             # assemblage : index() et ask()
│   └── tracing.py              # Langfuse (optionnel)
├── app/app_gradio.py           # interface de chat
├── eval/
│   ├── testset.jsonl           # jeu de test (Ground Truth)
│   ├── retrieval_metrics.py    # métriques déterministes
│   ├── llm_judge.py            # RAG Triad avec DeepEval
│   ├── run_benchmark.py        # comparaison de configurations
│   └── results/                # CSV et tableau Markdown générés
├── notebooks/
│   ├── TP1_chatbot_RAG.ipynb
│   └── TP2_evaluation_RAG.ipynb
├── reports/
│   ├── TP1_exemples_QR.md
│   └── TP2_rapport_comparatif.md
├── tests/                      # pytest, sans GPU (faux embedder et faux LLM)
└── tools/make_pdf.py           # régénère le PDF du corpus
```

## Démarrer sur Google Colab

1. **Forkez** ce dépôt sur votre compte GitHub (ou importez le zip dans Colab).
2. Ouvrez `notebooks/TP1_chatbot_RAG.ipynb` dans Colab : *Fichier > Ouvrir un notebook > GitHub*.
3. *Exécution > Modifier le type d'exécution > **GPU T4*** (gratuit). Le notebook installe Ollama et télécharge `qwen3:8b` (environ 5 Go).
4. Exécutez l'étape 0 (installation), puis suivez les étapes dans l'ordre.

**Sans GPU** (quota épuisé, poste trop léger) : créez une clé gratuite sur [Google AI Studio](https://aistudio.google.com), ajoutez-la dans les secrets Colab sous le nom `GEMINI_API_KEY` ; le pipeline bascule automatiquement sur Gemini (`llm_provider: auto`). Le corpus étant fictif, on peut l'envoyer à une API ; ne le faites jamais avec des données réelles confidentielles.

**En local** (si votre machine le permet) : `pip install -r requirements-eval.txt`, installez [Ollama](https://ollama.com), `ollama pull qwen3:8b`, copiez `.env.example` en `.env`.

**Tests rapides sans GPU** : `python -m pytest`. Les tests utilisent un faux modèle d'embedding et un faux LLM : ils vérifient la plomberie (chargement, chunking, indexation, recherche, métriques) en quelques secondes.

## Le corpus

Documentation interne **fictive** de l'entreprise Orbitale (domaine `orbitale.example`) : congés, télétravail, sécurité informatique, notes de frais (PDF), onboarding (HTML), FAQ du support, formation. Les formats et les pièges sont volontaires : en-têtes répétés dans le PDF, menu et pied de page dans le HTML, tableaux, identifiants exacts (`RH-07`, `SEC-2`), informations réparties sur plusieurs documents.

## TP 1 · Chatbot RAG (séance 1, 2 h 30)

Consignes : charger le corpus et implémenter un chunking **justifié** ; vectoriser avec sentence-transformers et indexer dans ChromaDB ; connecter la recherche au LLM ; créer une interface Gradio.

Livrable : dépôt GitHub avec ce README complété (section « Justification du chunking »), le code et `reports/TP1_exemples_QR.md` (5 questions-réponses testées).

## TP 2 · Évaluation et comparaison (séance 2, 2 h 30)

Consignes : jeu de test de **15 questions** avec Ground Truth ; comparer **Conf A** (chunks 500, top-k 3) et **Conf B** (chunks 200, top-k 5 + reranking) ; scores déterministes et DeepEval, traces Langfuse ; rapport comparatif.

```bash
python eval/run_benchmark.py --configs config/conf_a.yaml config/conf_b.yaml --judge auto --pause 4
python eval/run_benchmark.py --configs config/conf_a.yaml config/conf_b.yaml --judge none   # sans juge, rapide
```

Livrables : `eval/testset.jsonl`, `eval/results/`, `reports/TP2_rapport_comparatif.md` avec une recommandation argumentée.

## Pour aller plus loin

Chaque module de `src/` se termine par une liste « Pour aller plus loin » : alternatives à tester et à comparer avec vos mesures. Quelques pistes :
- **Ingestion** : `pymupdf4llm` ou Docling pour les PDF à tableaux.
- **Chunking** : découpage en tokens, chunking sémantique, LangChain `RecursiveCharacterTextSplitter`.
- **Embeddings** : `multilingual-e5-small` (léger) contre `bge-m3` ; un modèle anglais sur ce corpus français.
- **Récupération** : `conf_c.yaml` (recherche hybride BM25 + reranking), variation de `fetch_k`, requêtes reformulées.
- **Génération** : comparer `qwen3:8b`, `llama3.1:8b`, `mistral:7b` ; sortie JSON structurée.
- **Évaluation** : RAGAS en plus de DeepEval, changement de juge, trois exécutions par configuration.
- **Framework** : réécrire le pipeline avec LangChain ou LlamaIndex et comparer.

## Règles

- Aucune clé d'API dans le code ni dans Git : secrets Colab ou fichier `.env`.
- Tout changement d'hyperparamètre passe par un fichier de `config/`, versionné.
- Commits réguliers et parlants (« TP2 : ajout du reranking, +0,12 de MRR »).
