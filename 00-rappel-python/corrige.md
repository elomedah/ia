# Corrigé des manipulations

Exécutez ces réponses après les cellules correspondantes du support.

## 1. Variables

Pour obtenir 22,50 €, affectez `5` à `quantite` avant de recalculer `montant`.

Pour approfondir : [nombres, variables et calculs en Python](https://docs.python.org/fr/3/tutorial/introduction.html#numbers).

## 2. Fonction

```python
total_stylos = calculer_montant(1.5, 8)
print(total_stylos)  # 12.0
```

Pour approfondir : [définir une fonction et renvoyer un résultat](https://docs.python.org/fr/3/tutorial/controlflow.html#defining-functions).

## 3. Objet

```python
autre_vente = Vente("Classeur", 6, 2)
print(autre_vente.montant())  # 12
```

Pour approfondir : [classes, instances et méthodes](https://docs.python.org/fr/3/tutorial/classes.html).

## 4. Fichiers et filtre

```python
stylos = ventes_valides[ventes_valides["produit"] == "Stylo"]
print(stylos)
print(len(stylos))  # 4
```

Pour approfondir : [sélectionner des lignes avec pandas](https://pandas.pydata.org/docs/getting_started/intro_tutorials/03_subset_data.html), [traiter les valeurs manquantes](https://pandas.pydata.org/docs/user_guide/missing_data.html).

## 5. Lire le graphique des montants

Les deux fichiers contiennent 12 lignes au total, dont une sans quantité. Après exclusion de cette ligne, le chiffre d'affaires connu est de **168 €**.

| Produit | Chiffre d'affaires connu | Quantité connue |
| --- | ---: | ---: |
| Classeur | 60 € | 10 |
| Carnet | 54 € | 12 |
| Stylo | 54 € | 36 |

Les classeurs génèrent le plus de chiffre d'affaires connu, mais les stylos représentent le plus d'unités vendues. L'ordre entre Carnet et Stylo dans le classement du chiffre d'affaires n'a pas d'importance puisqu'ils sont à égalité.

Pour approfondir : [construire un graphique en barres](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar.html).

## 6. Mini-défi

```python
quantites_produit = (
    ventes_valides.groupby("produit")["quantite"]
    .sum()
    .sort_values(ascending=False)
)
print(quantites_produit)

fig, ax = plt.subplots(figsize=(7, 4))
ax.bar(quantites_produit.index, quantites_produit.values)
ax.set_title("Quantité connue vendue par produit")
ax.set_xlabel("Produit")
ax.set_ylabel("Quantité (articles)")
fig.tight_layout()
plt.show()
```

Les résultats sont incomplets parce que la quantité d'une vente de carnets est manquante : son montant et ses articles ne sont pas comptabilisés.

Pour approfondir : [regrouper et agréger avec pandas](https://pandas.pydata.org/docs/user_guide/groupby.html), [personnaliser une figure Matplotlib](https://matplotlib.org/stable/tutorials/lifecycle.html). Pour relire le nuage de points du support : [paramètres de seaborn.scatterplot](https://seaborn.pydata.org/generated/seaborn.scatterplot.html).
