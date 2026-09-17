# Parcours MLOps : de l'entraînement au monitoring

Apprenez à construire, suivre, automatiser et déployer un modèle de machine learning. Le fil conducteur est la prédiction de la durée des trajets Yellow Taxi : vous partirez d'un notebook pour arriver à une API et à des rapports de monitoring.

## Prérequis

Vous connaissez les bases de Python, de Git, de HTTP et du machine learning. La première étape vous accompagne dans la préparation de votre environnement de travail.

## Les quatre étapes

Suivez les étapes dans l'ordre : chacune réutilise les données, le code ou les modèles des précédentes.

| Étape | Ce que vous allez apprendre | Résultat attendu |
| --- | --- | --- |
| **[1. Introduction et premiers modèles](01-intro/README.md)** | Comprendre le cycle de vie ML, préparer l'environnement, explorer les données avec Jupyter et comparer plusieurs modèles. | Un notebook de préparation, d'entraînement et d'évaluation. |
| **[2. Suivi des expériences avec MLflow](02-track-experiences/README.md)** | Enregistrer les paramètres, les métriques et les modèles, comparer les exécutions et gérer les versions dans le registre. | Des expériences traçables et une version du modèle associée à l'alias `champion`. |
| **[3. Orchestration de l'entraînement](03-orchestration-deployment/README.md)** | Transformer le notebook en projet Python, rendre l'entraînement paramétrable et orchestrer son exécution avec Airflow. | Un workflow reproductible avec validation du modèle et gestion des échecs. |
| **[4. Déploiement et monitoring](04-deployment/README.md)** | Exposer le modèle avec FastAPI, déployer le service dans Docker et analyser les données et les prédictions avec Evidently. | Une API de prédiction et des rapports de dérive et de qualité du modèle. |

## Accès aux travaux pratiques

### Étape 1. Introduction et premiers modèles

- [Comprendre le MLOps](01-intro/01-introduction.md)
- [Préparer GitHub Codespaces](01-intro/02-lab-codespace.md)
- [Préparer l'environnement local et découvrir Docker](01-intro/03-lab-docker-local.md)
- [Lancer Jupyter et lire les données Parquet](01-intro/04-run-jupyter-notebook.md)
- [Prédire la durée des trajets](01-intro/05-duration-prediction.md)

### Étape 2. Suivi des expériences avec MLflow

- [Comprendre le suivi des expériences](02-track-experiences/01-experiment-tracking-intro.md)
- [Enregistrer et comparer les entraînements](02-track-experiences/02-tracking.md)
- [Gérer les versions et les alias des modèles](02-track-experiences/03-modele-registry-management.md)

### Étape 3. Orchestration de l'entraînement

- [Passer du notebook au projet Python et au workflow](03-orchestration-deployment/01-orchestration-jupyter-to-script.md)
- [Orchestrer le projet avec Airflow](03-orchestration-deployment/02-airflow.md)

### Étape 4. Déploiement et monitoring

- [Exposer le modèle avec FastAPI](04-deployment/01-web-service.md)
- [Déployer le service dans Docker](04-deployment/02-deploy-docker-image.md)
- [Prendre en main Evidently et surveiller le modèle](04-deployment/03-monitoring.md)

Pour commencer, ouvrez [l'étape 1 : introduction au MLOps](01-intro/README.md).
