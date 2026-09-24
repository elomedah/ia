# Lab : lancer Jupyter et lire un fichier Parquet

Ce laboratoire peut être réalisé dans GitHub Codespaces ou avec Anaconda installé sur votre ordinateur. Dans les deux cas, utilisez l'environnement Conda `mlops` et le dépôt `learning-mlops`.

## 1. Préparer l'environnement

Ouvrez un terminal à la racine du dépôt `learning-mlops`, puis vérifiez son emplacement :

```bash
git status
conda activate mlops
conda install jupyterlab pandas pyarrow ipykernel -y
python -m ipykernel install --user --name mlops --display-name "Python (mlops)"
```

`pandas` manipule les données. `pyarrow` permet de lire le format Parquet. `ipykernel` rend l'environnement `mlops` disponible dans Jupyter.

Enregistrez les dépendances principales :

```bash
conda env export --from-history > environment.yml
```

## 2. Lancer JupyterLab

### Dans GitHub Codespaces

```bash
jupyter lab --no-browser --ip=0.0.0.0 --port=8888
```

Codespaces détecte le port 8888. Cliquez sur **Open in Browser** dans la notification ou ouvrez l'onglet **PORTS**, puis l'adresse associée au port 8888. Conservez la visibilité du port sur **Private**.

### Avec Anaconda sur votre ordinateur

Dans WSL, macOS ou Linux :

```bash
jupyter lab
```

JupyterLab s'ouvre dans le navigateur. S'il ne s'ouvre pas automatiquement, utilisez l'adresse affichée dans le terminal.

Gardez le terminal ouvert pendant l'utilisation de JupyterLab.

## 3. Créer le notebook

Dans JupyterLab :

1. Créez un dossier `notebooks`.
2. Ouvrez ce dossier.
3. Créez un notebook avec le noyau **Python (mlops)**.
4. Nommez-le `04-read-parquet.ipynb`.

## 4. Télécharger les données

Dans la première cellule :

```python
from pathlib import Path
from urllib.request import urlretrieve

data_dir = Path("../data")
data_dir.mkdir(exist_ok=True)

url = "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet"
file_path = data_dir / "yellow_tripdata_2021-01.parquet"

if not file_path.exists():
    urlretrieve(url, file_path)

file_path
```

Exécutez la cellule avec `Shift + Enter`.

Ajoutez `data/` au fichier `.gitignore`. Les données téléchargées ne doivent pas être enregistrées dans Git.

## 5. Lire le fichier Parquet

Dans une nouvelle cellule :

```python
import pandas as pd

df = pd.read_parquet(file_path)
df.head()
```

Examinez ensuite la structure des données :

```python
df.shape
```

```python
df.dtypes
```

Les colonnes `tpep_pickup_datetime` et `tpep_dropoff_datetime` sont déjà lues comme des dates. Le format Parquet conserve les types des colonnes, contrairement à un fichier CSV qui nécessite souvent une conversion explicite.

Affichez les informations principales :

```python
df[["tpep_pickup_datetime", "tpep_dropoff_datetime", "PULocationID", "DOLocationID"]].head()
```

## 6. Enregistrer le notebook

Sauvegardez le notebook, puis revenez au terminal :

```bash
git status
git add .gitignore environment.yml notebooks/04-read-parquet.ipynb
git commit -m "Ajoute le notebook de lecture Parquet"
git push
```

Vérifiez sur GitHub que le notebook est présent et que le dossier `data` ne l'est pas.

## 7. Exercice : lire plusieurs mois

Consultez la page [TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) pour voir l'ensemble des fichiers disponibles par année, par mois et par type de trajet.

Ajoutez le fichier de février 2021 :

```python
urls = {
    "2021-01": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-01.parquet",
    "2021-02": "https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2021-02.parquet",
}

for month, url in urls.items():
    destination = data_dir / f"yellow_tripdata_{month}.parquet"
    if not destination.exists():
        urlretrieve(url, destination)
```

Écrivez ensuite un code Python qui :

1. recherche tous les fichiers `yellow_tripdata_*.parquet` dans `data` ;
2. lit chaque fichier avec `pandas.read_parquet` ;
3. ajoute une colonne `source_month` contenant le mois du fichier ;
4. rassemble les DataFrames avec `pandas.concat` ;
5. affiche le nombre de lignes pour chaque mois.

Point de départ :

```python
files = sorted(data_dir.glob("yellow_tripdata_*.parquet"))
frames = []

for parquet_file in files:
    # Lire le fichier.
    # Extraire le mois depuis parquet_file.stem.
    # Ajouter la colonne source_month.
    # Ajouter le DataFrame à frames.
    pass

trips = pd.concat(frames, ignore_index=True)
```

Vérifiez le résultat :

```python
trips.groupby("source_month").size()
```

Le total des lignes de `trips` doit être égal à la somme des lignes des fichiers lus. Votre code doit continuer à fonctionner lorsqu'un nouveau fichier mensuel est ajouté au dossier `data`.

## Arrêter JupyterLab

Dans le terminal où JupyterLab fonctionne, utilisez `Ctrl + C`, puis confirmez l'arrêt si nécessaire.

Dans Codespaces, arrêtez également le Codespace lorsque vous avez terminé afin de ne pas consommer inutilement votre quota.

Sources : [MLOps Zoomcamp, Reading Parquet Data](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/01-intro/04-read-parquet.md), [JupyterLab, démarrage](https://jupyterlab.readthedocs.io/en/stable/getting_started/starting.html), [pandas.read_parquet](https://pandas.pydata.org/docs/reference/api/pandas.read_parquet.html) et [GitHub Codespaces, redirection des ports](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace).
