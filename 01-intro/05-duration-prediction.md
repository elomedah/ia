# TP 05 : prédire la durée d'un trajet

Vous allez construire un premier modèle qui estime la durée d'un trajet Yellow Taxi. Créez le notebook `05-duration-prediction.ipynb` à la racine du dépôt, puis copiez et exécutez les cellules dans l'ordre.

Ce TP peut être réalisé dans Codespaces ou avec l'environnement Conda local `mlops`.

> **Travail indispensable**
>
> Réalisez réellement chaque étape du TP et assurez-vous de comprendre le rôle de chaque partie du code. Ne vous limitez pas à copier les cellules ou à lire les résultats. Les prochains chapitres reprendront la préparation des données, l'entraînement, l'évaluation et la sauvegarde du modèle réalisés ici.

## 1. Installer les bibliothèques

Dans un terminal, activez l'environnement et installez les dépendances :

```bash
conda activate mlops
conda install -c conda-forge pandas pyarrow scikit-learn matplotlib seaborn jupyterlab xgboost -y
```

Relancez JupyterLab si les bibliothèques ont été installées pendant son exécution.

## 2. Importer les bibliothèques

Copiez cette première cellule :

```python
from pathlib import Path
import pickle

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from sklearn.feature_extraction import DictVectorizer
from sklearn.linear_model import Lasso, LinearRegression
from sklearn.metrics import root_mean_squared_error
from xgboost import XGBRegressor
```

`pandas` lit et prépare les données. `DictVectorizer` transforme les variables en matrice numérique. Les deux modèles serviront à comparer deux entraînements.

## 3. Localiser le fichier Parquet

Le notebook et le dossier `data` se trouvent à la racine du dépôt. Copiez :

```python
data_path = Path("data/yellow_tripdata_2026-05.parquet")

if not data_path.exists():
    raise FileNotFoundError(f"Fichier introuvable : {data_path}")

data_path
```

La dernière ligne doit afficher le chemin du fichier.

## 4. Lire les données

Copiez :

```python
df = pd.read_parquet(data_path)
df.shape
```

Affichez les colonnes utiles :

```python
columns = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime",
    "PULocationID",
    "DOLocationID",
    "trip_distance",
]

df[columns].head()
```

Les colonnes utilisées sont les suivantes :

| Colonne | Description | Utilisation |
| --- | --- | --- |
| `tpep_pickup_datetime` | Date et heure de prise en charge du passager | Début du trajet et séparation chronologique |
| `tpep_dropoff_datetime` | Date et heure de dépôt du passager | Fin du trajet |
| `PULocationID` | Identifiant de la zone de prise en charge | Variable catégorielle de départ |
| `DOLocationID` | Identifiant de la zone de dépôt | Variable catégorielle d'arrivée |
| `trip_distance` | Distance du trajet indiquée par le compteur, en miles | Variable numérique |

La différence entre les dates de départ et d'arrivée formera la cible `duration`, exprimée en minutes. `PU` signifie *pick-up* et `DO` signifie *drop-off*.

## 5. Calculer la durée

Copiez :

```python
df["duration"] = (
    df["tpep_dropoff_datetime"] - df["tpep_pickup_datetime"]
).dt.total_seconds() / 60

df["duration"].describe()
```

La durée est exprimée en minutes. Observez les valeurs minimales, maximales et les quartiles.

## 6. Filtrer et préparer les variables

Nous conservons les trajets dont la durée est comprise entre 1 et 60 minutes :

```python
df = df[df["duration"].between(1, 60)].copy()

categorical = ["PULocationID", "DOLocationID"]
numerical = ["trip_distance"]

df[categorical] = df[categorical].astype(str)
df["PU_DO"] = df["PULocationID"] + "_" + df["DOLocationID"]

df.shape
```

`PU_DO` représente une combinaison entre la zone de départ et la zone d'arrivée.

Pour limiter la mémoire utilisée, conservez un échantillon reproductible :

```python
sample_size = min(200_000, len(df))
df = df.sample(n=sample_size, random_state=42)
df = df.sort_values("tpep_pickup_datetime").reset_index(drop=True)
```

La valeur `random_state=42` permet d'obtenir le même échantillon lors d'une nouvelle exécution.

## 7. Séparer entraînement et validation

Copiez :

```python
split_index = int(len(df) * 0.8)

df_train = df.iloc[:split_index].copy()
df_val = df.iloc[split_index:].copy()

len(df_train), len(df_val)
```

Les premières observations servent à l'entraînement. Les observations les plus récentes servent à la validation.

## 8. Transformer les variables

Copiez :

```python
features = ["PU_DO", "trip_distance"]

train_dicts = df_train[features].to_dict(orient="records")
val_dicts = df_val[features].to_dict(orient="records")

dv = DictVectorizer()
X_train = dv.fit_transform(train_dicts)
X_val = dv.transform(val_dicts)

y_train = df_train["duration"].to_numpy()
y_val = df_val["duration"].to_numpy()

X_train.shape, X_val.shape
```

`fit_transform` apprend les catégories sur l'entraînement. `transform` applique la même transformation à la validation.

Nous utilisons `DictVectorizer` pour simplifier la préparation des données. Il reçoit directement une liste de dictionnaires, transforme les variables catégorielles en colonnes binaires et conserve les variables numériques. Il produit ainsi une matrice exploitable par le modèle sans créer manuellement une colonne pour chaque catégorie.

D'autres encodeurs peuvent être utilisés selon le besoin :

- `OneHotEncoder` crée une colonne binaire pour chaque catégorie et s'intègre facilement dans un pipeline scikit-learn ;
- `OrdinalEncoder` remplace les catégories par des nombres entiers et convient surtout lorsqu'elles possèdent un ordre réel ;
- `TargetEncoder` utilise la relation entre une catégorie et la cible, avec des précautions pour éviter les fuites de données ;
- `FeatureHasher` limite la taille de la représentation lorsque le nombre de catégories est très élevé.

Le choix de l'encodeur dépend du modèle, du nombre de catégories et du risque de produire une matrice trop volumineuse.

## 9. Entraîner la régression linéaire

La **régression linéaire** apprend une relation linéaire entre les variables et la durée. Elle est rapide et constitue une référence simple pour évaluer les modèles suivants.

Copiez :

```python
linear_model = LinearRegression()
linear_model.fit(X_train, y_train)

linear_predictions = linear_model.predict(X_val)
linear_rmse = root_mean_squared_error(y_val, linear_predictions)

linear_rmse
```

La RMSE mesure l'écart entre les durées prédites et les durées réelles. Elle est exprimée en minutes. Une valeur plus faible indique une erreur moyenne mieux maîtrisée, avec une pénalisation plus forte des grandes erreurs.

## 10. Comparer les distributions

Copiez :

```python
plt.figure(figsize=(8, 4))
sns.histplot(y_val, label="Durée réelle", stat="density", bins=50, alpha=0.5)
sns.histplot(
    linear_predictions,
    label="Durée prédite",
    stat="density",
    bins=50,
    alpha=0.5,
)
plt.xlabel("Durée en minutes")
plt.legend()
plt.show()
```

Comparez la position et l'étalement des deux distributions. Ce graphique complète la métrique sans montrer l'erreur de chaque trajet.

## 11. Entraîner un modèle Lasso

Le modèle **Lasso** est une régression linéaire régularisée. Le paramètre `alpha` pénalise les coefficients et peut ramener certains d'entre eux à zéro. Cette propriété peut réduire l'influence de variables peu utiles.

Copiez :

```python
lasso_model = Lasso(alpha=0.01, max_iter=10_000)
lasso_model.fit(X_train, y_train)

lasso_predictions = lasso_model.predict(X_val)
lasso_rmse = root_mean_squared_error(y_val, lasso_predictions)

lasso_rmse
```

Comparez cette valeur à celle de la régression linéaire.

## 12. Exercice : entraîner un modèle XGBoost

**XGBoost** construit successivement plusieurs arbres de décision. Chaque nouvel arbre cherche à corriger une partie des erreurs commises par les arbres précédents. Le modèle peut apprendre des relations non linéaires, mais son entraînement demande davantage de ressources et de paramètres à contrôler.

Copiez et exécutez cette cellule :

```python
xgb_model = XGBRegressor(
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1,
    objective="reg:squarederror",
    random_state=42,
    n_jobs=-1,
)

xgb_model.fit(X_train, y_train)

xgb_predictions = xgb_model.predict(X_val)
xgb_rmse = root_mean_squared_error(y_val, xgb_predictions)

xgb_rmse
```

Les principaux paramètres sont :

- `n_estimators` : nombre d'arbres construits ;
- `max_depth` : profondeur maximale de chaque arbre ;
- `learning_rate` : contribution de chaque nouvel arbre ;
- `random_state` : valeur utilisée pour rendre l'entraînement reproductible.

Comparez les trois modèles :

```python
results = pd.DataFrame(
    {
        "model": ["LinearRegression", "Lasso", "XGBoost"],
        "rmse": [linear_rmse, lasso_rmse, xgb_rmse],
    }
).sort_values("rmse")

results
```

Le meilleur résultat de ce TP est celui dont la RMSE de validation est la plus faible. La comparaison doit utiliser le même jeu de validation pour les trois modèles.

## 13. Sauvegarder le modèle retenu

Le module Python `pickle` permet de **sérialiser** un objet, c'est-à-dire de convertir son état en données enregistrables dans un fichier. Le fichier peut ensuite être chargé dans une autre exécution Python sans entraîner de nouveau le modèle.

Dans ce TP, nous enregistrons ensemble :

- `dv`, le `DictVectorizer` qui connaît les colonnes créées pendant l'entraînement ;
- `selected_model`, le modèle qui utilise ces colonnes pour effectuer une prédiction.

Conserver uniquement le modèle ne suffit pas. Les nouvelles données doivent subir exactement la même transformation que les données d'entraînement.

Un fichier `pickle` dépend des classes et des versions de bibliothèques utilisées pour le créer. Il ne doit être chargé que depuis une source de confiance, car son chargement peut exécuter du code Python.

Copiez :

```python
models = {
    "LinearRegression": (linear_model, linear_rmse),
    "Lasso": (lasso_model, lasso_rmse),
    "XGBoost": (xgb_model, xgb_rmse),
}

selected_name = min(models, key=lambda name: models[name][1])
selected_model, selected_rmse = models[selected_name]

models_dir = Path("models")
models_dir.mkdir(exist_ok=True)
model_path = models_dir / "duration_model.bin"

with model_path.open("wb") as output_file:
    pickle.dump((dv, selected_model), output_file)

selected_name, selected_rmse, model_path
```

Le fichier contient le transformateur et le modèle. Ces deux objets sont nécessaires pour reproduire une prédiction.

## 14. Vérifier le fichier sauvegardé

Rechargez le fichier dans une nouvelle cellule :

```python
with model_path.open("rb") as input_file:
    loaded_dv, loaded_model = pickle.load(input_file)

example = [{"PU_DO": "161_236", "trip_distance": 3.2}]
example_matrix = loaded_dv.transform(example)
prediction = loaded_model.predict(example_matrix)[0]

prediction
```

La cellule doit retourner une durée estimée en minutes.

## 15. Travail à réaliser

1. Remplacez `alpha=0.01` par deux autres valeurs.
2. Entraînez un modèle Lasso pour chaque valeur.
3. Modifiez un paramètre de XGBoost et relancez son entraînement.
4. Notez la RMSE de validation de chaque essai.
5. Identifiez le modèle retenu et justifiez votre choix.
6. Listez les informations qu'il faudrait conserver pour reproduire chaque essai.

Le chapitre suivant utilisera MLflow pour enregistrer ces informations sans gérer manuellement une collection de résultats et de fichiers.

## 16. Enregistrer le notebook

Dans le terminal :

```bash
git add 05-duration-prediction.ipynb
git commit -m "Ajoute la prediction de duree des trajets"
git push
```

Ne versionnez pas les fichiers Parquet.
