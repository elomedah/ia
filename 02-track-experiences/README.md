# TP 02 : suivre les expériences avec MLflow

Dans le chapitre précédent, vous avez chargé des données de trajets dans un notebook. Vous allez maintenant entraîner plusieurs modèles et conserver les informations nécessaires pour comparer leurs résultats.

## Objectifs

À la fin du TP, vous saurez :

- créer une expérience MLflow ;
- enregistrer les paramètres d'un entraînement ;
- enregistrer une métrique d'évaluation ;
- conserver le modèle comme artefact ;
- comparer plusieurs exécutions dans l'interface MLflow.

## Données

Le TP utilise les fichiers Parquet Yellow Taxi publiés par la [NYC Taxi and Limousine Commission](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

Le fichier `data/yellow_tripdata_2026-05.parquet` est fourni dans le dépôt afin de pouvoir travailler si le site est indisponible.

## Progression

1. [Comprendre le suivi des expériences](01-experiment-tracking-intro.md).
2. [Démarrer le suivi avec MLflow](02-tracking.md).
3. [Gérer et enregistrer les modèles](03-modele-registry-management.md).
4. Préparer les données de trajets.
5. Entraîner un premier modèle de référence.
6. Enregistrer les paramètres, la métrique et le modèle.
7. Modifier un paramètre et lancer une nouvelle exécution.
8. Comparer les exécutions dans l'interface MLflow.
9. Sélectionner une exécution et justifier le choix du modèle.

## Résultat attendu

L'interface MLflow doit présenter au moins deux exécutions appartenant à la même expérience. Chaque exécution doit contenir ses paramètres, sa métrique d'évaluation et son modèle.

Source : [MLOps Zoomcamp, Experiment Tracking and Model Management](https://github.com/DataTalksClub/mlops-zoomcamp/tree/main/02-experiment-tracking).
