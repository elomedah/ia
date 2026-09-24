# Parcours Big Data et intelligence artificielle

Bienvenue dans ce parcours consacré à la conception et à la mise en production de solutions d'intelligence artificielle. Vous apprendrez à exploiter des modèles génératifs, à construire des agents capables d'utiliser des outils, puis à organiser, déployer et suivre vos services IA.

Les cours et travaux pratiques vous accompagnent progressivement, des bases du machine learning à un projet d'application complet. La visualisation des données vous aidera à explorer les résultats et à les rendre compréhensibles pour les utilisateurs.

## Programme

Les durées ci-dessous sont exprimées en heures. Les références et durées non fournies sont indiquées comme restant à préciser.

| Module | Référence | Durée | Description |
| --- | --- | ---: | --- |
| IA générative | À préciser | 14 h | Comprendre les modèles génératifs, formuler des instructions et enrichir les réponses avec des données documentaires grâce au RAG. |
| Agents IA | RNCP40573-BC04B-FM03 | 14 h | Concevoir des agents qui utilisent des outils et enchaînent des actions pour assister un utilisateur ou automatiser des tâches. |
| Pipelines MLOps | RNCP40573-BC04B-FM04 | 7 h | Structurer les étapes de préparation, d'entraînement et d'évaluation, suivre les expériences et orchestrer des workflows reproductibles. |
| Data Visualisation | RNCP40573-BC04B-FM05 | 14 h | Explorer les données, choisir des représentations adaptées et présenter les résultats pour faciliter leur interprétation. |
| Déploiement de services IA | RNCP40573-BC04B-FM06 | 14 h | Exposer un modèle via une API, conteneuriser le service et surveiller son fonctionnement ainsi que la qualité des prédictions. |
| Projet d’implémentation de modèles Big Data et IA | RNCP40573-BC04B-FM07 | À préciser | Mobiliser les acquis du parcours pour concevoir, réaliser et présenter une solution répondant à un besoin métier. |

## Se repérer dans le dépôt

| Répertoire | Contenu |
| --- | --- |
| [01 — IA traditionnelle](01-traditional-ia/README.md) | Bases de l'intelligence artificielle traditionnelle et du machine learning. Contenu à venir. |
| [02 — IA générative](02-generative-ia/README.md) | Modèles génératifs et applications. Contenu à venir. |
| [03 — Agents IA](03-agent-ia/README.md) | Agents et automatisation à l'aide d'outils. Contenu à venir. |
| [04 — MLOps](04-mlops/README.md) | Travaux pratiques sur l'entraînement, MLflow, Airflow, le déploiement avec FastAPI et Docker, et le monitoring avec Evidently. |
| [Projet fil rouge](projet/README.md) | Propositions de sujets pour le projet d'implémentation. |

Les supports MLOps et de déploiement sont regroupés dans `04-mlops`. Le module Data Visualisation ne dispose pas encore de répertoire dédié.

## Apprendre par la pratique

Le parcours MLOps s'appuie sur la prédiction de la durée des trajets Yellow Taxi. Vous partez d'un notebook pour comparer des modèles, suivre vos expériences, automatiser l'entraînement et construire une API de prédiction accompagnée de rapports de monitoring.

Pour démarrer ces travaux pratiques, consultez [l'introduction au MLOps et la préparation de l'environnement](04-mlops/01-intro/README.md).

## Projet fil rouge

Deux pistes sont proposées pour mettre en pratique les compétences du parcours :

- **Un assistant IA d'entreprise** : ingérer des données structurées et non structurées, répondre aux questions avec un système RAG, puis automatiser certaines tâches grâce à des agents IA et déployer la solution.
- **Une plateforme de recrutement intelligente** : analyser des CV, effectuer du matching avec des offres d'emploi, générer des synthèses et assister les recruteurs à l'aide d'agents IA.

Retrouvez les propositions dans le [répertoire du projet](projet/README.md).

## Prérequis

Des bases en Python, Git, HTTP et machine learning vous permettront d'aborder les travaux pratiques. Les premiers supports MLOps vous guident dans la préparation de votre environnement, en local ou avec GitHub Codespaces.
