# Analyser les trajets des taxis de New York

Vous disposez de données réelles de trajets de taxis verts à New York. Votre objectif : décrire les trajets observés, examiner leur qualité et représenter leurs durées, leurs distances et leur répartition horaire. Réalisez le travail dans `exercice-taxis-nyc.ipynb`, avec Google Colab ou JupyterLab. Ajoutez vos cellules de code et vos commentaires sous chaque question. Aucun corrigé n'est fourni.

## Préparer le fichier CSV

La [page officielle TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) publie les trajets au format **Parquet**. Un CSV est un fichier texte tabulaire ; Parquet conserve notamment les types et stocke les données par colonnes. Renommer l'extension ne convertit pas le fichier.

Utilisez les **Green Taxi Trip Records de janvier 2025**. La cellule fournie ci-dessous sert uniquement à préparer le fichier de travail : elle télécharge les colonnes utiles, prélève au maximum 10 000 lignes avec une graine fixe et les exporte en CSV. Elle ne nettoie pas les données. La lecture initiale porte sur le mois entier pour ces colonnes ; l'échantillonnage intervient ensuite.

Dans Colab, installez si nécessaire `pandas` et `pyarrow` avec `%pip install pandas pyarrow matplotlib seaborn`. En local, utilisez le terminal de votre environnement avec `python -m pip install pandas pyarrow matplotlib seaborn`.

```python
from pathlib import Path
import pandas as pd

source = "https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-01.parquet"
colonnes = [
    "lpep_pickup_datetime", "lpep_dropoff_datetime",
    "passenger_count", "trip_distance", "fare_amount",
    "total_amount", "payment_type", "PULocationID", "DOLocationID",
]
donnees_source = pd.read_parquet(source, columns=colonnes)
extrait = donnees_source.sample(n=min(10000, len(donnees_source)), random_state=42)
Path("donnees").mkdir(exist_ok=True)
extrait.to_csv("donnees/taxis_verts_2025_01.csv", index=False)
del donnees_source, extrait
```

Exécutez cette cellule une fois par nouvel environnement. Si l'accès réseau échoue, téléchargez le Parquet depuis la page TLC, importez-le dans votre environnement et remplacez `source` par son chemin local. Pour partager exactement les mêmes lignes, conservez le CSV généré : la source peut être révisée.

Consultez le [dictionnaire officiel des taxis verts](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf) pour interpréter les colonnes. `trip_distance` est exprimée en miles et les montants en dollars américains. Les codes de paiement et de zones sont des catégories, même s'ils sont représentés par des nombres. La TLC indique que la précision des données n'est pas garantie.

## 1. Charger et découvrir

1. Chargez **le CSV généré**, avec `pd.read_csv`, dans un DataFrame nommé `trajets`. Ne poursuivez pas l'analyse à partir du Parquet.
2. Affichez les premières lignes, les dimensions, les noms des colonnes et leurs types.
3. Identifiez les deux colonnes de dates. Quel type ont-elles après la lecture du CSV ?
4. Calculez le nombre de valeurs manquantes par colonne et le nombre de lignes entièrement identiques.
5. Décrivez ce que représente une ligne, la période de la source et la méthode de constitution de l'extrait.

Pour vous aider : [read_csv](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html), [info](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.info.html), [isna](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.isna.html), [duplicated](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.duplicated.html).

## 2. Convertir les types et créer des informations

1. Conservez une copie des données brutes avant modification.
2. Convertissez les colonnes de départ et d'arrivée en dates avec `pd.to_datetime`. Utilisez `errors="coerce"` et expliquez ce que devient une valeur impossible à convertir. Comptez séparément les valeurs absentes avant conversion et les valeurs devenues invalides lors de la conversion.
3. Vérifiez que distance, nombre de passagers et montants sont numériques. Convertissez-les seulement si nécessaire, en comptant les valeurs rendues manquantes.
4. Créez une colonne `duree_minutes` à partir de la différence entre arrivée et départ. Utilisez la durée totale en secondes avant de la convertir en minutes.
5. Créez `heure_depart` à partir de l'heure de prise en charge.

Pour vous aider : [to_datetime](https://pandas.pydata.org/docs/reference/api/pandas.to_datetime.html), [to_numeric](https://pandas.pydata.org/docs/reference/api/pandas.to_numeric.html), [dt.total_seconds](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.total_seconds.html), [dt.hour](https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.hour.html).

## 3. Examiner et nettoyer si nécessaire

1. Examinez les statistiques descriptives des durées, distances, montants et nombres de passagers.
2. Recherchez les dates absentes ou invalides, les arrivées antérieures ou égales aux départs, les départs hors janvier 2025 et les distances nulles ou négatives. Un trajet démarré le 31 janvier peut légitimement se terminer le 1er février.
3. Examinez les valeurs extrêmes, les montants négatifs et les doublons potentiels. Distinguez une incohérence d'une valeur inhabituelle : un montant négatif peut nécessiter une interprétation métier et une ligne identique ne prouve pas toujours une erreur de saisie.
4. Définissez vos règles et créez `trajets_nettoyes`. Justifiez chaque exclusion ou conservation. Ne remplacez pas systématiquement les données manquantes par zéro et ne supprimez pas une ligne uniquement parce qu'une colonne inutile à l'analyse est absente.
5. Présentez un bilan avec le nombre de lignes initial, les exclusions à chaque étape et le nombre final. Comptez les exclusions successivement pour ne pas compter deux fois une ligne qui présente plusieurs anomalies. Si aucune correction n'est nécessaire pour une règle, indiquez-le.

Pour vous aider : [describe](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.describe.html), [sélection et filtres](https://pandas.pydata.org/docs/user_guide/indexing.html#boolean-indexing), [dropna](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.dropna.html).

## 4. Manipuler et synthétiser

1. Sélectionnez les dates, la distance, la durée et le montant total ; affichez les dix trajets les plus longs en durée.
2. Affichez les trajets de plus de 5 miles et de plus de 15 minutes.
3. Calculez le nombre de trajets, la durée médiane et la distance moyenne par heure de départ. Triez les heures dans l'ordre chronologique.
4. Exportez les données nettoyées dans `taxis_nettoyes.csv`, sans l'index du DataFrame.

Pour vous aider : [sort_values](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.sort_values.html), [groupby et agrégations](https://pandas.pydata.org/docs/user_guide/groupby.html), [to_csv](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_csv.html).

## 5. Représenter et interpréter

Produisez les trois graphiques suivants, avec un titre et des axes indiquant les unités :

1. **Matplotlib :** histogramme de la durée des trajets. Choisissez le nombre d'intervalles et expliquez votre choix.
2. **Matplotlib :** graphique en barres du nombre de trajets par heure de départ. Représentez les 24 heures, y compris celles sans trajet dans l'extrait nettoyé.
3. **seaborn :** nuage de points de la distance en fonction de la durée. Utilisez de la transparence pour limiter la superposition des points. Si vous sous-échantillonnez pour le graphique, indiquez la taille et fixez une graine.

Enregistrez au moins un graphique en PNG. Pour chaque graphique, rédigez une observation et une limite. Si vous limitez les axes ou excluez des valeurs pour la lisibilité, indiquez-le. Les volumes observés concernent l'extrait et les taxis verts, pas l'ensemble des déplacements à New York.

Pour vous aider : [histogramme](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.hist.html), [barres](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html), [reindex pour compléter les heures](https://pandas.pydata.org/docs/reference/api/pandas.Series.reindex.html), [scatterplot](https://seaborn.pydata.org/generated/seaborn.scatterplot.html), [savefig](https://matplotlib.org/stable/api/_as_gen/matplotlib.figure.Figure.savefig.html).

## Travail à conserver

Votre notebook doit présenter la source et l'échantillonnage, l'exploration, les conversions, les règles de nettoyage et leur bilan, les manipulations et les trois graphiques commentés. Conservez également le CSV nettoyé et l'image PNG. Dans Colab, téléchargez ces fichiers depuis le panneau **Fichiers** avant de quitter l'environnement.
