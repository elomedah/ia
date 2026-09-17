# TP 03 : surveiller le modèle avec Evidently

Vous allez d'abord apprendre à utiliser Evidently sur un exemple simple, puis comparer des données de référence à des données récentes et relier les résultats au service Yellow Taxi.

## Partie 1. Prendre en main Evidently

### 1.1. Comprendre les objets utilisés

Evidently est une bibliothèque Python qui produit des métriques et des visualisations pour analyser des données et évaluer des modèles. Dans cette première partie, vous allez comparer deux lots de trajets fictifs, sans charger de modèle.

| Notion | Rôle dans la manipulation |
| --- | --- |
| Données de référence | Lot qui sert de point de comparaison |
| Données courantes | Lot que vous souhaitez analyser |
| `DataDefinition` | Décrit les types et les rôles des colonnes |
| `Dataset` | Associe les données pandas à cette définition |
| `Report` | Définit les analyses à exécuter |
| Preset | Regroupe des métriques adaptées à un besoin, comme la détection de dérive |

Une **dérive** est un changement de distribution : par exemple, les trajets deviennent plus longs ou une zone de départ devient plus fréquente. Elle peut être mesurée sans connaître les durées réelles.

### 1.2. Préparer le notebook

Prérequis : l'environnement `mlops`, JupyterLab et son noyau Python sont configurés comme dans le [lab Jupyter](../01-intro/04-run-jupyter-notebook.md). Dans Codespaces, reprenez la commande de lancement et l'ouverture du port indiquées dans ce lab.

Dans le terminal, à la racine du projet, activez l'environnement du cours et installez les dépendances :

```bash
conda activate mlops
python -m pip install "evidently>=0.7,<0.8" pandas numpy
jupyter lab
```

À la racine de votre projet `learning-mlops`, créez le notebook `prise-en-main-evidently.ipynb` et sélectionnez le noyau de l'environnement `mlops`. Exécutez les cellules suivantes dans l'ordre. Cette manipulation utilise uniquement des données synthétiques ; MLflow et l'API ne sont pas nécessaires.

Dans la première cellule :

```python
from pathlib import Path

import numpy as np
import pandas as pd
from evidently import DataDefinition, Dataset, Report
from evidently.presets import DataDriftPreset

reports_dir = Path("reports")
reports_dir.mkdir(exist_ok=True)
```

### 1.3. Construire deux lots comparables

Créez 500 trajets fictifs. `trip_distance` est une distance en miles et `zone` une catégorie :

```python
rng = np.random.default_rng(42)

reference_df = pd.DataFrame({
    "trip_distance": rng.uniform(1, 5, size=500),
    "zone": rng.choice(["A", "B"], size=500, p=[0.7, 0.3]),
})
current_df = reference_df.copy()

reference_df.head()
```

Pour ce premier essai, les deux lots sont identiques : cela permet de vérifier le fonctionnement du rapport avant de modifier les données. Sur le projet réel, ils représenteront deux périodes distinctes.

Déclarez explicitement les types des colonnes et utilisez la même définition pour les deux lots :

```python
definition = DataDefinition(
    numerical_columns=["trip_distance"],
    categorical_columns=["zone"],
)

reference = Dataset.from_pandas(reference_df, data_definition=definition)
current = Dataset.from_pandas(current_df, data_definition=definition)
```

### 1.4. Générer et lire un premier rapport

```python
report = Report([DataDriftPreset()])
result = report.run(current_data=current, reference_data=reference)
result.save_html(str(reports_dir / "decouverte-sans-derive.html"))
result
```

`report` décrit l'analyse à effectuer ; `result` contient les résultats calculés par `run`. La dernière ligne affiche le rapport dans le notebook. Vous pouvez aussi ouvrir `reports/decouverte-sans-derive.html` dans un navigateur, après l'avoir téléchargé si vous utilisez Codespaces.

Dans le rapport, repérez :

1. le nombre de colonnes analysées et la part des colonnes en dérive ;
2. le résultat de détection pour `trip_distance` et `zone` ;
3. les distributions de référence et courantes pour chaque colonne.

**Résultat attendu :** aucune dérive sur ces deux lots identiques. Les distributions se superposent.

### 1.5. Provoquer une dérive et comparer

Augmentez toutes les distances de 10 miles, en conservant les zones :

```python
shifted_df = current_df.copy()
shifted_df["trip_distance"] += 10

shifted = Dataset.from_pandas(shifted_df, data_definition=definition)
shifted_result = report.run(current_data=shifted, reference_data=reference)
shifted_result.save_html(str(reports_dir / "decouverte-avec-derive.html"))
shifted_result
```

Comparez les deux rapports. Une dérive doit apparaître sur `trip_distance`, dont les valeurs passent de l'intervalle [1, 5] à [11, 15]. La distribution de `zone` reste identique.

Pour la distance, relevez la méthode de détection, le score et le seuil affichés. Le score n'est pas toujours une probabilité : sa signification et le sens de comparaison au seuil dépendent de la méthode utilisée. Distinguez aussi le résultat par colonne du résumé global du jeu de données.

Par défaut, Evidently signale une dérive globale lorsque au moins 50 % des colonnes dérivent. Ici, une colonne sur deux suffit à atteindre ce seuil. Ce résumé ne mesure pas l'erreur du modèle.

### 1.6. Vérifier votre compréhension

1. Pourquoi faut-il conserver la même référence pour comparer les deux rapports ?
2. Quelle différence faites-vous entre le DataFrame pandas et le `Dataset` Evidently ?
3. Repartez de `current_df`, remplacez toutes les valeurs de `zone` par `"B"` et générez `reports/decouverte-derive-zone.html`. Quelle colonne est maintenant signalée ?
4. Pouvez-vous conclure que le modèle se trompe davantage avec ces seuls rapports ? Quelles données faudrait-il ajouter pour le vérifier ?

Vous savez maintenant préparer les données, exécuter une analyse et lire un rapport de dérive. Dans la partie suivante, vous réutiliserez ces étapes avec les trajets Yellow Taxi et les prédictions du modèle enregistré dans MLflow.

Références : [créer un rapport](https://docs.evidentlyai.com/docs/library/report), [définir les données](https://docs.evidentlyai.com/docs/library/data_definition) et [analyser la dérive](https://docs.evidentlyai.com/metrics/preset_data_drift).

## Partie 2. Surveiller le modèle Yellow Taxi

### 2.1. Ce que nous allons surveiller

| Dimension | Question | Exemple |
| --- | --- | --- |
| Service | L'API fonctionne-t-elle ? | erreurs HTTP et latence |
| Données | Les entrées ont-elles changé ? | distribution de `trip_distance` et des zones |
| Prédictions | Les sorties ont-elles changé ? | distribution de `prediction` |
| Performance | Les estimations restent-elles justes ? | RMSE et MAE lorsque la durée réelle est disponible |

Evidently analyse les données, les prédictions et la performance. Les indicateurs techniques de l'API proviennent de ses journaux ou d'un outil de supervision du service.

### 2.2. Cas d'utilisation du projet

1. **Dérive des entrées** : comparer des trajets récents aux données de référence.
2. **Dérive des prédictions** : observer les durées estimées avant de connaître la durée réelle.
3. **Qualité de la régression** : calculer RMSE et MAE lorsque la cible est disponible.
4. **Comparaison de versions** : évaluer `champion` et `challenger` sur les mêmes trajets.

Une dérive indique un changement de distribution. Elle ne prouve pas, à elle seule, que le modèle est moins performant.

### 2.3. Préparer le projet

Prérequis : le package `learning_mlops` du TP d'orchestration est installé, le serveur MLflow est accessible et l'alias `champion` du modèle `nyc-taxi-duration-model` désigne un pipeline complet avec `DictVectorizer`. Le fichier Parquet doit être présent dans `data/`. L'API peut rester arrêtée pendant cette analyse historique.

Ajoutez cette ligne à la liste `dependencies` de la section `[project]` dans `pyproject.toml`, en conservant les autres dépendances :

```toml
"evidently>=0.7,<0.8",
```

Créez le module et le dossier des rapports :

```bash
touch src/learning_mlops/monitor.py
mkdir -p reports
```

Ajoutez `reports/` à `.gitignore`, puis installez le projet :

```bash
conda activate mlops
python -m pip install -e .
```

### 2.4. Ajouter les imports

Dans `src/learning_mlops/monitor.py`, copiez :

```python
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

from evidently import DataDefinition, Dataset, Regression, Report
from evidently.presets import DataDriftPreset, RegressionPreset
import mlflow
import mlflow.sklearn
import pandas as pd
```

`Dataset` associe un DataFrame à une définition. `Report` exécute une analyse. Les presets regroupent les métriques et visualisations adaptées à un besoin.

### 2.5. Lire les trajets

Ajoutez :

```python
def read_data(data_path: Path, sample_size: int) -> pd.DataFrame:
    if sample_size < 4:
        raise ValueError("--sample-size doit être supérieur ou égal à 4")
    if not data_path.exists():
        raise FileNotFoundError(f"Fichier introuvable : {data_path}")

    df = pd.read_parquet(data_path)
    required_columns = {
        "tpep_pickup_datetime", "tpep_dropoff_datetime",
        "PULocationID", "DOLocationID", "trip_distance",
    }
    missing_columns = required_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Colonnes absentes : {sorted(missing_columns)}")

    df["target"] = (
        df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60
    df = df[df["target"].between(1, 60)].copy()
    if len(df) < 4:
        raise ValueError("Il faut au moins quatre trajets valides après filtrage")

    selected_size = min(sample_size, len(df))
    df = df.sample(n=selected_size, random_state=42)
    df = df.sort_values("tpep_pickup_datetime").reset_index(drop=True)
    df["PULocationID"] = df["PULocationID"].astype(str)
    df["DOLocationID"] = df["DOLocationID"].astype(str)
    return df
```

`target` contient la durée réelle. Elle sera utilisée pour mesurer la qualité de la régression. Le minimum de quatre lignes évite des lots vides ou réduits à un seul trajet ; il ne garantit pas une analyse statistique fiable. Conservez un échantillon bien plus grand pour interpréter les résultats. Comme à l'entraînement, l'analyse porte uniquement sur les durées comprises entre 1 et 60 minutes.

### 2.6. Ajouter les prédictions

Ajoutez :

```python
def load_model(
    tracking_uri: str,
    model_name: str,
    model_alias: str,
):
    mlflow.set_tracking_uri(tracking_uri)
    version = mlflow.MlflowClient().get_model_version_by_alias(
        model_name, model_alias
    )
    model_uri = f"models:/{model_name}/{version.version}"
    model = mlflow.sklearn.load_model(model_uri)
    metadata = {
        "model_name": model_name,
        "model_alias": model_alias,
        "model_version": str(version.version),
        "run_id": version.run_id,
        "model_uri": model_uri,
        "tracking_uri": tracking_uri,
    }
    return model, metadata


def add_predictions(df: pd.DataFrame, model) -> pd.DataFrame:
    features_df = df[["trip_distance"]].copy()
    features_df["PU_DO"] = (
        df["PULocationID"].astype(str) + "_" + df["DOLocationID"].astype(str)
    )
    features = features_df[["PU_DO", "trip_distance"]].to_dict(orient="records")
    monitored = df[
        ["PULocationID", "DOLocationID", "trip_distance", "target"]
    ].copy()
    monitored["prediction"] = model.predict(features)
    return monitored
```

L'alias est résolu une seule fois, puis le chargement utilise le numéro de version exact. Les rapports et la simulation emploient ainsi le même modèle. `add_predictions` reconstruit `PU_DO` à chaque appel à partir des zones.

### 2.7. Créer la référence et la période courante

Ajoutez :

```python
def split_periods(df: pd.DataFrame):
    if len(df) < 4:
        raise ValueError("Données insuffisantes pour créer les deux lots")
    split_index = len(df) // 2
    reference_df = df.iloc[:split_index].copy()
    current_df = df.iloc[split_index:].copy()
    return reference_df, current_df


def to_dataset(df: pd.DataFrame) -> Dataset:
    return Dataset.from_pandas(
        df,
        data_definition=DataDefinition(
            numerical_columns=["trip_distance"],
            categorical_columns=["PULocationID", "DOLocationID"],
            regression=[Regression(target="target", prediction="prediction")],
        ),
    )
```

La première moitié chronologique sert de référence et la seconde de période courante. Avec plusieurs fichiers, utilisez plutôt un mois de référence et un mois récent.

La déclaration `Regression` associe explicitement la durée réelle et la prédiction à la tâche de régression. Les types des variables sont identiques pour les deux lots, comme dans la première partie.

### 2.8. Créer les rapports

Ajoutez :

```python
def create_reports(
    reference: Dataset,
    current: Dataset,
    reports_dir: Path,
) -> None:
    drift_report = Report([DataDriftPreset()])
    drift_result = drift_report.run(current, reference)
    drift_result.save_html(str(reports_dir / "data-drift.html"))

    regression_report = Report([RegressionPreset()])
    regression_result = regression_report.run(current, reference)
    regression_result.save_html(str(reports_dir / "regression-quality.html"))
```

`DataDriftPreset` compare les distributions. `RegressionPreset` analyse notamment la MAE, la RMSE et les résidus. Le second rapport exige la durée réelle.

Le rapport de dérive inclut ici les entrées, `prediction` et `target`. Une dérive de la cible décrit un changement des durées observées ; elle ne mesure pas directement une hausse des erreurs.

### 2.9. Ajouter les arguments

Ajoutez :

```python
def parse_args():
    parser = argparse.ArgumentParser(description="Produit les rapports Evidently")
    parser.add_argument("--data-path", type=Path, required=True)
    parser.add_argument("--sample-size", type=int, default=100_000)
    parser.add_argument("--tracking-uri", default="http://127.0.0.1:5000")
    parser.add_argument("--model-name", default="nyc-taxi-duration-model")
    parser.add_argument("--model-alias", default="champion")
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    return parser.parse_args()
```

### 2.10. Créer le point d'entrée

Terminez le fichier avec :

```python
def main():
    args = parse_args()

    source = read_data(args.data_path, args.sample_size)
    model, metadata = load_model(
        tracking_uri=args.tracking_uri,
        model_name=args.model_name,
        model_alias=args.model_alias,
    )
    monitored = add_predictions(source, model)
    reference_df, current_df = split_periods(monitored)

    execution_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    reports_dir = args.reports_dir / f"v{metadata['model_version']}-{execution_id}"
    reports_dir.mkdir(parents=True, exist_ok=False)
    metadata.update({
        "execution_id": execution_id,
        "data_path": str(args.data_path.resolve()),
        "sample_size_requested": args.sample_size,
        "sample_size_used": len(source),
        "random_state": 42,
        "split": "chronologique 50/50",
        "reference_rows": len(reference_df),
        "current_rows": len(current_df),
    })
    (reports_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    create_reports(
        to_dataset(reference_df),
        to_dataset(current_df),
        reports_dir,
    )
    print(f"Rapports créés dans : {reports_dir.resolve()}")


if __name__ == "__main__":
    main()
```

### 2.11. Exécuter le monitoring

Le fichier de mai 2026 a déjà servi à l'entraînement dans les TP précédents. Cette première exécution sert à apprendre à générer les rapports : ses métriques ne constituent pas une évaluation indépendante du modèle.

Vérifiez que MLflow fonctionne, puis exécutez depuis la racine du projet :

```bash
conda activate mlops
python -m learning_mlops.monitor \
  --data-path data/yellow_tripdata_2026-05.parquet \
  --model-alias champion
```

Dans le dossier affiché par le script, ouvrez :

```text
data-drift.html
regression-quality.html
metadata.json
```

Chaque exécution crée un sous-dossier contenant la version et un horodatage, sans écraser les rapports précédents. `metadata.json` relie tous les résultats de ce dossier au modèle chargé et aux données utilisées.

Pour une évaluation indépendante, préparez un fichier de trajets provenant d'une période postérieure à l'entraînement et non utilisée pour sélectionner le modèle. Passez son chemin à `--data-path` : ses deux moitiés chronologiques serviront de référence et de période courante. Vérifiez les dates d'entraînement dans l'exécution MLflow avant d'interpréter les métriques.

### 2.12. Interpréter les rapports

Répondez aux questions :

1. Une dérive est-elle détectée sur `trip_distance` ?
2. Les fréquences des zones ont-elles changé ?
3. La distribution des prédictions évolue-t-elle ?
4. La RMSE courante diffère-t-elle de la référence ?
5. Les erreurs sont-elles concentrées sur certains trajets ?
6. Quelle vérification supplémentaire proposez-vous ?

Ne concluez pas à une dégradation du modèle à partir du seul rapport de dérive.

### 2.13. Simuler une dérive

Dans `main()`, après l'appel à `create_reports` et avant le `print` final, insérez ce bloc indenté de quatre espaces :

```python
    shifted_df = current_df.copy()
    shifted_df["trip_distance"] += 10
    shifted_df = add_predictions(shifted_df, model)

    shifted_result = Report([DataDriftPreset()]).run(
        current_data=to_dataset(shifted_df),
        reference_data=to_dataset(reference_df),
    )
    shifted_result.save_html(str(reports_dir / "simulated-drift.html"))
```

Relancez la commande de la section 2.11. Comparez `data-drift.html` et `simulated-drift.html` dans le nouveau dossier : ils utilisent la même référence et la même version du modèle. La variable `PU_DO` est reconstruite par `add_predictions`.

Expliquez quelle colonne a changé, comment Evidently le détecte et si les prédictions évoluent. Cette simulation aide à comprendre le rapport, mais elle ne remplace pas l'observation de données réelles.

Les durées réelles conservées ne correspondent plus aux distances modifiées. Ne calculez pas de performance métier sur ces trajets artificiels.

### 2.14. Relier Evidently au service web

Le service FastAPI journalise déjà l'identifiant de requête, la version et la latence. Pour analyser les données et les prédictions, conservez aussi une trace structurée avec :

- la date de la requête ;
- l'identifiant de requête pour rattacher ensuite la durée réelle ;
- la version du modèle ;
- les variables nécessaires à l'analyse ;
- la prédiction ;
- la durée réelle lorsqu'elle devient disponible.

Ne journalisez pas automatiquement des informations sensibles ou inutiles. Une fenêtre récente pourra ensuite être comparée à la référence avec Evidently.

Le script précédent analyse un historique dont les durées réelles sont connues. En service, la cible peut arriver plus tard : on produit alors uniquement le rapport de dérive, avec les mêmes colonnes pour les deux lots.

Pour expérimenter ce cas, ajoutez aussi ce bloc dans `main()`, avant le `print` final. Il retire volontairement la cible des lots déjà calculés :

```python
    drift_definition = DataDefinition(
        numerical_columns=["trip_distance", "prediction"],
        categorical_columns=["PULocationID", "DOLocationID"],
    )
    reference_without_target = Dataset.from_pandas(
        reference_df.drop(columns="target"), data_definition=drift_definition
    )
    current_without_target = Dataset.from_pandas(
        current_df.drop(columns="target"), data_definition=drift_definition
    )
    drift_only = Report([DataDriftPreset()]).run(
        current_data=current_without_target,
        reference_data=reference_without_target,
    )
    drift_only.save_html(str(reports_dir / "drift-without-target.html"))
```

Relancez le script et ouvrez `drift-without-target.html`. Avec les journaux réels de l'API, constituez ces deux tableaux directement à partir des entrées et des prédictions enregistrées, en sélectionnant la même version du modèle. La lecture du Parquet et le calcul de `target` seront alors remplacés par la lecture des journaux. La régression sera évaluée après rattachement des durées réelles.

### 2.15. Exercice : comparer deux versions

1. Générez les prédictions de `champion` et de `challenger`.
2. Utilisez exactement les mêmes trajets pour les deux versions.
3. Créez un rapport de régression pour chaque modèle.
4. Comparez RMSE, MAE et erreurs extrêmes.
5. Vérifiez la qualité des données avant d'interpréter les métriques.
6. Proposez une décision argumentée sur l'alias `champion`.

Vérifiez d'abord que les deux alias existent et désignent les pipelines à comparer. Relancez la commande de la section 2.11 avec `--model-alias champion --reports-dir reports/champion`, puis avec `--model-alias challenger --reports-dir reports/challenger`. Conservez le même fichier et le même `--sample-size` : la graine fixe reproduit l'échantillon et la séparation. Relevez les versions dans les deux fichiers `metadata.json` et comparez les métriques **courantes** des rapports `regression-quality.html`.

#### Conseils

- Conservez le numéro de version avec chaque prédiction.
- Utilisez une période qui n'a pas servi à l'entraînement.
- Une amélioration moyenne peut masquer une dégradation sur un groupe de trajets.
- Le rapport aide à décider, mais ne déplace pas lui-même l'alias.

### 2.16. À retenir

La dérive peut être mesurée sans cible. La qualité de régression exige la durée réelle. Le monitoring doit relier chaque observation à la version du modèle afin de rendre une alerte interprétable.

Documentation officielle : [Evidently Reports](https://docs.evidentlyai.com/docs/library/report), [Data Definition](https://docs.evidentlyai.com/docs/library/data_definition), [Data Drift Preset](https://docs.evidentlyai.com/metrics/preset_data_drift) et [Regression Preset](https://docs.evidentlyai.com/metrics/preset_regression).
