# Recette technique de l'introduction

Vérifications réalisées le 11 septembre 2026 sur Docker Desktop Windows avec conteneurs Linux.

| Vérification | Résultat |
|---|---|
| Construction `docker compose build lab` | Réussie |
| Validation Compose | Réussie |
| Diagnostic du laboratoire | Linux, Python 3.12.14, scikit-learn 1.7.2 |
| Tests automatisés | 2 tests réussis : reproduction, absence de fuite dans le scaler, rechargement, changement de split, refus d'écrasement et entrées invalides |
| Entraînement CLI, seed 42 et alpha 1 | 400 lignes d'entraînement, 100 de validation |
| MAE de référence | 17,4251 minutes |
| MAE du candidat | 2,3804 minutes |
| Prédiction pour 10 km et 2 arrêts | 38,0359 minutes |
| Distance négative | Refus explicite et code de sortie 2 |
| Modèle absent | Erreur de fichier et code de sortie 2 |

Les artefacts de cette recette sont conservés localement dans `artifacts/recette-20260911/`, ignoré par Git. Les métriques concernent uniquement le jeu synthétique.

L'image Python téléchargée lors de la construction correspond au digest `sha256:782412e85d0f0984994c290652577d4018aff08145c85b262bb63dc0c7522254`. Le Dockerfile utilise un tag, donc une reconstruction future peut résoudre une autre image. Les dépendances Python du laboratoire sont fixées explicitement.

La configuration Codespaces est fournie. Aucune session distante n'a été créée durant cette recette ; son démarrage reste à vérifier une fois les fichiers publiés sur la branche distribuée. La durée pédagogique est planifiée mais n'a pas été mesurée avec une promotion. Les supports sont livrés en Markdown ; aucun export PDF n'a encore été produit.
