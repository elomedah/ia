# Lab : installer Anaconda et Docker sur son ordinateur

Anaconda gère les environnements Python. Docker exécute les applications dans des conteneurs isolés. Ce laboratoire installe et vérifie les deux outils sur votre ordinateur.

## 1. Vérifier les prérequis

Vous devez disposer :

- d'un accès à votre session utilisateur ;
- d'une connexion internet ;
- de Git pour récupérer votre dépôt `learning-mlops` ;
- des droits nécessaires pour installer un logiciel.

Identifiez votre système d'exploitation, puis suivez la procédure correspondante.

## 2. Installer Anaconda

### Windows avec WSL

Anaconda doit être installé dans Linux, à l'intérieur de WSL.

Ouvrez PowerShell en tant qu'administrateur :

```powershell
wsl --install
wsl --update
```

Redémarrez l'ordinateur si Windows le demande. Ouvrez ensuite **Ubuntu** depuis le menu Démarrer et créez votre utilisateur Linux.

Dans le terminal Ubuntu, vérifiez l'architecture :

```bash
uname -m
```

Pour une architecture `x86_64`, installez Anaconda avec la procédure Linux ci-dessous. Consultez également la [documentation officielle de WSL](https://learn.microsoft.com/en-us/windows/wsl/install).

### Linux et WSL sur une architecture x86_64

Exécutez les commandes dans le terminal Linux ou Ubuntu WSL :

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2025.12-2-Linux-x86_64.sh
sha256sum Anaconda3-2025.12-2-Linux-x86_64.sh
bash Anaconda3-2025.12-2-Linux-x86_64.sh
```

Comparez l'empreinte avec celle des [archives Anaconda](https://repo.anaconda.com/archive/). Acceptez les conditions, conservez le chemin proposé et acceptez l'initialisation de Conda.

Rechargez le terminal :

```bash
source ~/.bashrc
conda --version
```

Pour une autre architecture, utilisez l'installateur indiqué dans la [documentation Anaconda pour Linux](https://www.anaconda.com/docs/getting-started/anaconda/install/linux-install).

### macOS

Téléchargez l'installateur adapté à votre processeur depuis la [page officielle Anaconda](https://www.anaconda.com/download). Dans le terminal, exécutez le fichier téléchargé :

```bash
bash ~/Downloads/Anaconda3-*-MacOSX-*.sh
source ~/.zshrc
conda --version
```

Acceptez les conditions, conservez le chemin proposé et acceptez l'initialisation de Conda. Consultez la [procédure officielle pour macOS](https://www.anaconda.com/docs/getting-started/anaconda/install/mac-install).

### Créer l'environnement du cours

Dans le terminal WSL, macOS ou Linux :

```bash
conda --version
conda create --name mlops python=3.12 -y
conda activate mlops
python --version
```

## 3. Installer Docker sous Windows

Docker Desktop utilise WSL 2 pour exécuter des conteneurs Linux.

Ouvrez PowerShell et vérifiez que votre distribution utilise WSL 2 :

```powershell
wsl --list --verbose
```

Installez ensuite [Docker Desktop pour Windows](https://docs.docker.com/desktop/setup/install/windows-install/) :

1. Téléchargez l'installateur officiel.
2. Lancez `Docker Desktop Installer.exe`.
3. Conservez le moteur WSL 2.
4. Terminez l'installation et démarrez Docker Desktop.
5. Utilisez les conteneurs Linux.

Attendez que Docker Desktop indique que le moteur est démarré.

## 4. Installer Docker sous macOS

Vérifiez le type de processeur dans **Menu Apple > À propos de ce Mac** : Apple Silicon ou Intel.

Installez [Docker Desktop pour Mac](https://docs.docker.com/desktop/setup/install/mac-install/) :

1. Téléchargez l'installateur correspondant au processeur.
2. Ouvrez `Docker.dmg`.
3. Déplacez Docker dans le dossier Applications.
4. Lancez Docker et utilisez les réglages recommandés.

Attendez que Docker Desktop indique que le moteur est démarré.

## 5. Installer Docker sous Ubuntu

Utilisez le dépôt officiel de Docker. La procédure dépend de la version d'Ubuntu et peut évoluer.

1. Ouvrez la [documentation Docker Engine pour Ubuntu](https://docs.docker.com/engine/install/ubuntu/).
2. Supprimez les paquets incompatibles indiqués dans la documentation.
3. Configurez le dépôt `apt` officiel de Docker.
4. Installez Docker Engine, la commande Docker et les plugins Buildx et Compose.
5. Démarrez le service Docker.

Les paquets attendus sont :

```text
docker-ce
docker-ce-cli
containerd.io
docker-buildx-plugin
docker-compose-plugin
```

Pour exécuter Docker sans `sudo`, appliquez la [procédure de post-installation Linux](https://docs.docker.com/engine/install/linux-postinstall/), puis ouvrez une nouvelle session. L'accès au groupe `docker` donne des privilèges importants sur la machine.

## 6. Vérifier Docker

Ouvrez un nouveau terminal : PowerShell sous Windows, Terminal sous macOS ou un shell sous Ubuntu.

```bash
docker version
docker compose version
```

`docker version` doit afficher une section **Client** et une section **Server**. Si la section Server manque, le moteur Docker n'est pas démarré.

Exécutez ensuite un premier conteneur :

```bash
docker run --rm hello-world
```

Docker télécharge l'image `hello-world`, crée un conteneur, exécute son programme puis supprime le conteneur grâce à `--rm`.

## 7. Récupérer le dépôt du cours

Sur la page GitHub de votre dépôt `learning-mlops`, cliquez sur **Code** et copiez son URL HTTPS.

Dans un terminal, placez-vous dans le dossier où vous conservez vos projets :

```bash
git clone https://github.com/VOTRE-COMPTE/learning-mlops.git
cd learning-mlops
git status
```

Remplacez `VOTRE-COMPTE` par votre identifiant GitHub. Les fichiers créés dans Codespaces doivent apparaître dans le dossier local.

## Résultat attendu

Les commandes suivantes s'exécutent sans erreur :

```bash
conda --version
python --version
docker version
docker compose version
docker run --rm hello-world
git status
```

Sources : [documentation Anaconda](https://www.anaconda.com/docs/getting-started/anaconda/install), [Docker Desktop pour Windows](https://docs.docker.com/desktop/setup/install/windows-install/), [Docker Desktop pour Mac](https://docs.docker.com/desktop/setup/install/mac-install/), [Docker Engine pour Ubuntu](https://docs.docker.com/engine/install/ubuntu/) et [installation de Docker Compose](https://docs.docker.com/compose/install/).
