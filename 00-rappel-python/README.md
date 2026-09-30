# Prendre en main Python et analyser des fichiers

Vous allez analyser les ventes d'une petite boutique : quel produit génère le plus de chiffre d'affaires ? Vous utiliserez Python pour les premiers calculs, pandas pour les tableaux, puis Matplotlib et seaborn pour les graphiques.

Les données sont fictives. Aucune connaissance préalable de pandas n'est nécessaire.

## Préparer votre espace

### Option 1 : Google Colab, dans votre navigateur

Vous pouvez réaliser **tout le TP**, y compris l'[exercice sur les taxis NYC](exercice-taxis-nyc.md), dans [Google Colab](https://colab.research.google.com/), sans installer Python sur votre ordinateur.

1. Connectez-vous avec votre compte Google. Importez `rappel-python.ipynb` depuis le menu **Fichier > Importer un notebook** (les libellés peuvent varier selon la langue).
2. Enregistrez une copie du notebook dans votre Drive. Un environnement CPU suffit ; aucun GPU n'est nécessaire.
3. Dans une cellule ajoutée au début, exécutez `%pip install pandas matplotlib seaborn pyarrow`.
4. Dans le panneau **Fichiers** à gauche, créez un dossier `donnees`. Importez dans ce dossier les deux fichiers `ventes_jour1.csv` et `ventes_jour2.csv` fournis dans ce TP. Les chemins du support fonctionneront ainsi sans modification.
5. Exécutez les cellules Python dans l'ordre. Les commandes de terminal de l'option locale ci-dessous ne sont pas à exécuter dans Colab.

Les fichiers de l'environnement Colab sont temporaires. Téléchargez vos CSV et images depuis le panneau **Fichiers**, et votre notebook depuis **Fichier > Télécharger > Télécharger le fichier .ipynb**. L'enregistrement du notebook dans Drive ne sauvegarde pas automatiquement les fichiers de données de l'environnement. Après la suppression de l'environnement, réimportez les CSV et rejouez les cellules.

Documentation : [importer des notebooks et conserver son travail dans Colab](https://research.google.com/colaboratory/faq.html), [importer et exporter des fichiers](https://colab.research.google.com/notebooks/io.ipynb).

### Option 2 : JupyterLab en local ou dans Codespaces

Utilisez votre environnement Python et JupyterLab déjà installé, en local avec Anaconda ou dans votre Codespace. Avant de commencer, exécutez dans son terminal :

```sh
python -m pip install jupyterlab pandas matplotlib seaborn pyarrow
python -m jupyterlab
```

Ouvrez le dossier `00-rappel-python`, puis le notebook `rappel-python.ipynb`. Choisissez le noyau de votre environnement Python. Gardez le sous-dossier `donnees` à côté du notebook. Le support ci-dessous reprend les mêmes étapes : vous pouvez aussi copier chaque bloc Python dans une cellule d'un nouveau notebook placé dans ce dossier.

### Exécuter les cellules

Dans les deux environnements, une cellule de code s'exécute avec **Maj + Entrée**. Exécutez les cellules dans l'ordre : les variables restent en mémoire. Après un redémarrage du noyau, réexécutez les cellules depuis le début.

## 1. Écrire des variables et calculer

Une variable associe un nom à une valeur. `=` affecte une valeur ; `==` compare deux valeurs. Python distingue les majuscules et les minuscules. Un commentaire commence par `#`.

```python
produit = "Carnet"       # str : texte entre guillemets
prix = 4.5               # float : nombre décimal, avec un point
quantite = 3             # int : nombre entier
en_stock = True          # bool : True ou False
montant = prix * quantite
print(produit, montant)  # Carnet 13.5
print(type(prix))
```

`print()` affiche une valeur ; `type()` indique son type. Les parenthèses servent à appeler une fonction. Les opérations usuelles sont `+`, `-`, `*` et `/`.

Une **liste** rassemble des valeurs ordonnées. Un **dictionnaire** associe des clés à des valeurs, comme une petite fiche.

```python
produits = ["Carnet", "Stylo", "Classeur"]
vente = {"produit": "Carnet", "prix": 4.5, "quantite": 3}
print(produits[0])       # Le premier indice est 0
print(vente["prix"])     # Accès par une clé

if quantite >= 3:
    print("Vente de plusieurs articles")

for nom in produits:
    print(nom)
```

`if` exécute un bloc si la condition est vraie ; `for` répète un bloc pour chaque élément. Le `:` et l'indentation de quatre espaces délimitent ces blocs.

**À vous :** changez la quantité de la première cellule pour obtenir un montant de 22,50 €. Réexécutez-la et observez le résultat.

## 2. Définir et appeler une fonction

Une fonction nomme un traitement réutilisable. Ses paramètres reçoivent les valeurs données à l'appel. `return` renvoie un résultat utilisable dans la suite du programme.

```python
def calculer_montant(prix, quantite):
    return prix * quantite

total = calculer_montant(4.5, 3)
print(total)
```

Définir la fonction avec `def` ne déclenche pas le calcul. L'appel `calculer_montant(4.5, 3)` le déclenche. Une fonction qui se contente de `print()` affiche quelque chose, mais ne renvoie pas ce montant.

**À vous :** appelez la fonction pour huit stylos à 1,50 € et stockez le résultat dans `total_stylos`.

## 3. Créer un objet

Un objet regroupe des données, ses **attributs**, et des opérations, ses **méthodes**. Une classe définit comment construire ces objets. Vous utilisez déjà des objets : une liste ou une chaîne de caractères en est un.

```python
class Vente:
    def __init__(self, produit, prix, quantite):
        self.produit = produit
        self.prix = prix
        self.quantite = quantite

    def montant(self):
        return calculer_montant(self.prix, self.quantite)

ma_vente = Vente("Carnet", 4.5, 3)
print(ma_vente.produit)    # Lire un attribut
print(ma_vente.montant()) # Appeler une méthode : 13.5
```

`Vente(...)` crée une instance de la classe. `__init__` initialise ses attributs. `self` désigne l'objet utilisé ; Python le transmet automatiquement à ses méthodes. Un attribut se lit avec un point ; une méthode s'appelle avec un point et des parenthèses.

**À vous :** créez une seconde vente, `autre_vente`, pour deux classeurs à 6 € et affichez son montant.

## 4. Lire et explorer les fichiers avec pandas

Un CSV est un fichier texte contenant un tableau. Ici, la première ligne contient les noms de colonnes et la virgule sépare les valeurs. Les deux fichiers représentent deux jours de ventes et possèdent les mêmes colonnes.

| Colonne | Signification |
| --- | --- |
| `date` | Jour de vente, au format année-mois-jour |
| `produit` | Nom du produit |
| `categorie` | Famille du produit |
| `prix_unitaire` | Prix en euros d'un article |
| `quantite` | Nombre d'articles vendus sur cette ligne |

Une ligne représente une vente. pandas charge ce tableau dans un objet **DataFrame**. Une colonne est une **Series**. `import` charge une bibliothèque ; `as pd` lui donne un nom court.

```python
import pandas as pd

jour1 = pd.read_csv("donnees/ventes_jour1.csv")
jour2 = pd.read_csv("donnees/ventes_jour2.csv")
ventes = pd.concat([jour1, jour2], ignore_index=True)
print(ventes.head())
print(ventes.shape)
ventes.info()
```

`concat` empile les lignes des deux tableaux. `ignore_index=True` recrée leur numérotation. `head()` montre les cinq premières lignes, `shape` donne le nombre de lignes et de colonnes, et `info()` décrit les colonnes et leurs types. Vous retrouvez les attributs et méthodes vus précédemment.

Vous devez obtenir **12 lignes et 5 colonnes**. La colonne `date` reste du texte dans cet exemple ; aucun calcul de dates n'est nécessaire.

```python
print(ventes[["produit", "quantite"]].head())
print(ventes.isna().sum())
```

Les doubles crochets sélectionnent plusieurs colonnes à partir d'une liste de noms. `isna()` repère les valeurs manquantes et `sum()` les compte par colonne. Une quantité manque : ne la remplacez pas par zéro, car vous ignorez combien d'articles ont été vendus.

```python
ventes_valides = ventes.dropna(subset=["quantite"]).copy()
ventes_valides["montant"] = (
    ventes_valides["prix_unitaire"] * ventes_valides["quantite"]
)
print(ventes_valides[["produit", "montant"]].head())
print("Chiffre d'affaires connu :", ventes_valides["montant"].sum(), "EUR")
```

`dropna` retire ici la ligne sans quantité ; `copy()` crée un tableau indépendant que vous pouvez modifier. La multiplication travaille sur toutes les lignes à la fois. Vous n'avez pas besoin d'une boucle `for` ou d'une instance de `Vente` par ligne.

Le résultat porte sur **11 ventes renseignées**. Il ne représente pas le chiffre d'affaires complet de la boutique, car une vente reste inconnue.

```python
grosses_ventes = ventes_valides[ventes_valides["montant"] >= 15]
print(grosses_ventes)

ca_produit = (
    ventes_valides.groupby("produit")["montant"]
    .sum()
    .sort_values(ascending=False)
)
print(ca_produit)
ca_produit.to_csv("chiffre_affaires_par_produit.csv", header=True)
```

Le filtre garde les lignes qui respectent la condition. `groupby` rassemble les ventes du même produit, `sum` additionne leurs montants et `sort_values` classe les résultats. `to_csv` écrit la synthèse dans un nouveau fichier à côté du notebook ; le nom du produit est conservé dans l'index exporté.

**À vous :** affichez seulement les ventes du produit `"Stylo"`. Combien de lignes obtenez-vous ?

## 5. Comparer les produits avec Matplotlib

Un graphique en barres permet de comparer le chiffre d'affaires connu par produit. Matplotlib vous permet de définir les axes, le titre et l'enregistrement de l'image.

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(ca_produit.index, ca_produit.values)
ax.set_title("Chiffre d'affaires connu par produit")
ax.set_xlabel("Produit")
ax.set_ylabel("Chiffre d'affaires (EUR)")
fig.tight_layout()
fig.savefig("chiffre_affaires.png", dpi=150)
plt.show()
```

`fig` est la figure complète et `ax` la zone du graphique. `index` fournit les noms des produits ; `values` fournit les montants. `savefig` crée un fichier image et `show` affiche la figure.

**À vous :** identifiez le produit qui génère le plus de chiffre d'affaires connu. Est-ce nécessairement celui dont on vend le plus d'unités ?

## 6. Explorer une relation avec seaborn

seaborn s'appuie sur Matplotlib et permet de désigner directement les colonnes d'un DataFrame. Ici, chaque point représente une vente renseignée.

```python
import seaborn as sns

fig, ax = plt.subplots(figsize=(7, 4))
sns.scatterplot(
    data=ventes_valides,
    x="quantite",
    y="montant",
    hue="produit",
    ax=ax,
)
ax.set_title("Montant et quantité par vente renseignée")
ax.set_xlabel("Quantité (articles)")
ax.set_ylabel("Montant (EUR)")
fig.tight_layout()
plt.show()
```

`x` et `y` choisissent les colonnes des axes, et `hue` attribue une couleur à chaque produit. Pour un même produit, le montant augmente avec la quantité parce qu'il est calculé à prix unitaire constant. Ce petit jeu fictif ne permet pas de conclure sur les comportements des clients.

## 7. Votre mini-défi

À partir de `ventes_valides`, calculez le nombre total d'articles vendus **par produit**, triez-le du plus grand au plus petit, puis adaptez le graphique Matplotlib pour afficher ces quantités. Changez aussi le titre et l'unité de l'axe vertical.

Conservez votre notebook, le CSV de synthèse et l'image. Expliquez en une phrase pourquoi les résultats sont incomplets. Consultez ensuite le [corrigé](corrige.md).

## En cas de difficulté

Pour prolonger le TP, réalisez l'[exercice d'analyse des trajets NYC](exercice-taxis-nyc.md) : chargement d'un CSV réel, manipulation, nettoyage justifié, conversion des dates et graphiques. Cet exercice ne comporte pas de corrigé. Son énoncé est aussi disponible dans `exercice-taxis-nyc.ipynb`, à ouvrir dans JupyterLab ou à importer dans Colab.

| Message | Vérification |
| --- | --- |
| `NameError` | Exécutez d'abord la cellule qui définit la variable ou la fonction. |
| `IndentationError` | Vérifiez les quatre espaces après `def`, `class`, `if` et `for`. |
| `FileNotFoundError` | Vérifiez que le notebook et le dossier `donnees` sont au même niveau. |
| `ModuleNotFoundError` | Installez la bibliothèque dans l'environnement du noyau sélectionné. |
| `KeyError` | Vérifiez l'orthographe exacte du nom de colonne, y compris les majuscules. |

## Documentation

- [pandas : lire un CSV](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
- [pandas : regrouper et agréger](https://pandas.pydata.org/docs/user_guide/groupby.html)
- [Matplotlib : construire une figure](https://matplotlib.org/stable/tutorials/lifecycle.html)
- [seaborn : nuage de points](https://seaborn.pydata.org/generated/seaborn.scatterplot.html)
