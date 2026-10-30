# TP 2 · Rapport comparatif Conf A / Conf B

## 1. Protocole

| Élément | Valeur |
|---|---|
| Corpus | Orbitale (7 fichiers : md, txt, pdf, html) |
| Jeu de test | 15 questions (répartition par type : …) |
| Modèle d'embedding | BAAI/bge-m3 (identique pour A et B) |
| LLM générateur | … (température 0) |
| Juge | … |
| Conf A | chunks fixes 500 car., chevauchement 50, top-k 3 |
| Conf B | chunks fixes 200 car., chevauchement 30, top-k 5, reranking bge-reranker-v2-m3 sur 20 candidats |
| Nombre d'exécutions | … |

## 2. Résultats

_Coller ici `eval/results/summary.md` et le graphique du notebook._

## 3. Analyse des écarts

_Au moins 3 questions où A et B divergent : chunks récupérés, cause probable (chunk coupé, mauvais classement, contexte bruité, réponse non fidèle), lien avec la configuration._

## 4. Coût

_Latence médiane (recherche et génération), effet du reranking, tokens envoyés au LLM._

## 5. Recommandation

_Configuration recommandée pour ce corpus et pourquoi, en 5 lignes, chiffres à l'appui._

## 6. Limites et pistes

_Taille du jeu de test, une seule exécution, biais du juge, ce que vous testeriez ensuite (conf C, top-k, autre juge)._
