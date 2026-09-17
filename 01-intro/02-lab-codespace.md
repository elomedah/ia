# Lab : préparer son environnement avec GitHub Codespaces

GitHub Codespaces fournit un environnement Linux accessible depuis un navigateur. Votre code et vos fichiers sont conservés dans un dépôt GitHub.

## 1. Créer un compte GitHub

1. Ouvrez [github.com/signup](https://github.com/signup).
2. Créez un compte personnel.
3. Vérifiez votre adresse électronique.
4. Activez l'authentification à deux facteurs.

Consultez la [procédure officielle de création d'un compte](https://docs.github.com/en/account-and-profile/how-tos/account-management/creating-an-account-on-github).

## 2. Créer le dépôt du cours

1. Ouvrez [github.com/new](https://github.com/new).
2. Saisissez exactement `learning-mlops` comme nom du dépôt.
3. Choisissez la visibilité **Public**.
4. Cochez **Add a README file**.
5. Dans **Add .gitignore**, choisissez **Python**.
6. Cliquez sur **Create repository**.

Le fichier README initialise la branche principale. Le dépôt peut ainsi être ouvert dans Codespaces. Consultez la [documentation officielle sur la création d'un dépôt](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository).

## 3. Créer le Codespace

Depuis le dépôt `learning-mlops` :

1. Cliquez sur **Code**.
2. Sélectionnez l'onglet **Codespaces**.
3. Cliquez sur **Create codespace on main**.
4. Attendez l'ouverture de Visual Studio Code dans le navigateur.

Ouvrez ensuite le terminal intégré avec **Terminal > New Terminal**.

Vérifiez le répertoire courant :

```bash
pwd
git status
```

Le terminal doit se trouver dans le dépôt `learning-mlops`. Consultez la [procédure officielle de création d'un Codespace](https://docs.github.com/en/codespaces/developing-in-a-codespace/creating-a-codespace-for-a-repository).

## 4. Installer Anaconda

Le Codespace utilise Linux. Vérifiez son architecture :

```bash
uname -m
```

Pour une architecture `x86_64`, téléchargez l'installateur officiel :

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Linux-x86_64.sh
```

Calculez son empreinte :

```bash
sha256sum Anaconda3-2025.12-2-Linux-x86_64.sh
```

Comparez la valeur avec celle publiée dans les [archives officielles Anaconda](https://repo.anaconda.com/archive/), puis lancez l'installation :

```bash
bash Anaconda3-2025.12-2-Linux-x86_64.sh
```

Pendant l'installation :

1. Lisez et acceptez les conditions d'utilisation.
2. Conservez le chemin d'installation proposé.
3. Acceptez l'initialisation de Conda.

Rechargez le terminal :

```bash
source ~/.bashrc
conda --version
```

La commande doit afficher la version de Conda. La procédure complète est disponible dans la [documentation officielle Anaconda pour Linux](https://www.anaconda.com/docs/getting-started/anaconda/install/linux-install).

## 5. Créer l'environnement du cours

Évitez d'installer les bibliothèques du projet dans l'environnement `base`.

```bash
conda create --name mlops python=3.12 -y
conda activate mlops
python --version
```

Le nom de l'environnement actif apparaît généralement au début de l'invite :

```text
(mlops)
```

Enregistrez sa définition dans le dépôt :

```bash
conda env export --from-history > environment.yml
```

## 6. Enregistrer le travail

```bash
git add environment.yml
git commit -m "Configure l'environnement Conda"
git push
```

Actualisez la page du dépôt et vérifiez que `environment.yml` est présent.

## Résultat attendu

Votre dépôt contient :

```text
learning-mlops/
├── .gitignore
├── README.md
└── environment.yml
```

Le terminal doit reconnaître les commandes suivantes :

```bash
git --version
conda --version
python --version
```

Docker sera installé et utilisé dans un laboratoire séparé.

Sources : [MLOps Zoomcamp, GitHub Codespaces](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/01-intro/02-codespaces.md), [GitHub Docs](https://docs.github.com/en/codespaces) et [Anaconda Docs](https://www.anaconda.com/docs/getting-started/anaconda/install/linux-install).
