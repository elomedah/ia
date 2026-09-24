# TP : exposer le modèle avec FastAPI

Vous allez créer un service web qui charge le modèle `champion` depuis MLflow et retourne la durée estimée d'un trajet.

## 1. Vérifier le modèle à servir

Le registre MLflow doit contenir :

- le modèle enregistré `nyc-taxi-duration-model` ;
- une version associée à l'alias `champion` ;
- un artefact qui contient le pipeline complet avec `DictVectorizer` et le modèle.

Le pipeline complet est nécessaire pour transformer les variables reçues par l'API. Une version qui contient uniquement l'estimateur ne peut pas traiter directement les données du trajet.

Dans l'interface MLflow, ouvrez le modèle et relevez le numéro de la version `champion`.

## 2. Remise à niveau FastAPI

FastAPI est un framework Python utilisé pour créer des API web. Une API reçoit une requête HTTP, exécute un traitement et retourne une réponse, généralement au format JSON.

### Application et route

Une application FastAPI commence par la création d'un objet `FastAPI`. Une route associe une adresse et une méthode HTTP à une fonction Python.

Créez temporairement le fichier `fastapi_demo.py` à la racine du dépôt :

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "API disponible"}
```

Dans `@app.get("/")` :

- `app` représente l'application ;
- `get` indique la méthode HTTP ;
- `/` correspond au chemin de la route ;
- `root` contient le traitement exécuté.

### Méthodes HTTP utilisées

| Méthode | Usage dans le TP |
| --- | --- |
| `GET` | Lire l'état du service ou les informations du modèle |
| `POST` | Envoyer les données d'un trajet et demander une prédiction |

Une requête `GET` ne modifie pas le service. Une requête `POST` peut transporter un objet JSON dans son corps.

### Valider une requête avec Pydantic

Complétez `fastapi_demo.py` :

```python
from pydantic import BaseModel, Field


class NumberInput(BaseModel):
    value: float = Field(gt=0)


@app.post("/double")
def double_number(data: NumberInput):
    return {"result": data.value * 2}
```

`BaseModel` décrit la structure attendue. `Field(gt=0)` impose une valeur strictement positive. FastAPI refuse automatiquement une requête qui ne respecte pas ce contrat.

### Démarrer l'API minimale

Installez FastAPI et son serveur, puis lancez l'application :

```bash
conda activate mlops
python -m pip install fastapi "uvicorn[standard]"
uvicorn fastapi_demo:app --reload --port 8000
```

Dans la commande :

- `fastapi_demo` désigne le fichier sans l'extension `.py` ;
- `app` désigne l'objet FastAPI créé dans ce fichier ;
- `--reload` redémarre le serveur lorsque le code change ;
- `--port 8000` choisit le port du service.

### Tester les routes

Ouvrez [http://127.0.0.1:8000/](http://127.0.0.1:8000/) pour tester la route `GET`.

Ouvrez ensuite [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). FastAPI génère cette interface à partir des routes et des modèles Pydantic. Utilisez-la pour envoyer à `/double` une valeur positive, puis une valeur négative.

Une requête valide retourne le résultat avec un statut HTTP `200`. Une valeur négative provoque une erreur de validation avec un statut `422`.

Arrêtez l'API avec `Ctrl + C`, puis supprimez `fastapi_demo.py`. Le service de prédiction appliquera les mêmes principes avec un contrat plus complet et un modèle MLflow.

Documentation : [FastAPI, premiers pas](https://fastapi.tiangolo.com/tutorial/first-steps/), [corps d'une requête](https://fastapi.tiangolo.com/tutorial/body/) et [validation des champs](https://fastapi.tiangolo.com/tutorial/body-fields/).

## 3. Ajouter le service au projet Python

Complétez la structure du projet :

```text
learning-mlops/
├── src/
│   └── learning_mlops/
│       ├── __init__.py
│       ├── train.py
│       └── api.py
├── pyproject.toml
└── README.md
```

Créez le fichier :

```bash
touch src/learning_mlops/api.py
```

Ajoutez `fastapi` et `uvicorn` dans la liste `dependencies` de `pyproject.toml` :

```toml
dependencies = [
    "fastapi",
    "mlflow",
    "pandas",
    "pyarrow",
    "scikit-learn",
    "uvicorn[standard]",
    "xgboost",
]
```

Réinstallez le projet en mode éditable :

```bash
conda activate mlops
python -m pip install -e .
```

## 4. Importer les composants

Dans `src/learning_mlops/api.py`, copiez :

```python
from contextlib import asynccontextmanager
import logging
import os
from time import perf_counter
from uuid import uuid4

from fastapi import FastAPI, Request
from pydantic import BaseModel, Field
import mlflow
import mlflow.sklearn
from mlflow.tracking import MlflowClient
```

`FastAPI` expose les routes HTTP. Pydantic contrôle les données reçues. MLflow retrouve et charge la version enregistrée.

## 5. Définir la configuration

Ajoutez :

```python
MLFLOW_TRACKING_URI = os.getenv(
    "MLFLOW_TRACKING_URI",
    "http://127.0.0.1:5000",
)
MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "nyc-taxi-duration-model",
)
MODEL_ALIAS = os.getenv("MODEL_ALIAS", "champion")
MODEL_URI = f"models:/{MODEL_NAME}@{MODEL_ALIAS}"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("taxi-duration-api")
```

Les variables d'environnement permettent de changer le serveur MLflow ou la version logique sans modifier le code.

## 6. Définir les contrats de l'API

Ajoutez :

```python
class Ride(BaseModel):
    PULocationID: int = Field(gt=0)
    DOLocationID: int = Field(gt=0)
    trip_distance: float = Field(gt=0)


class Prediction(BaseModel):
    duration_minutes: float
    model_name: str
    model_alias: str
    model_version: str
    request_id: str
```

`Ride` décrit la requête. `Prediction` décrit la réponse. FastAPI utilisera ces classes pour valider les valeurs et produire la documentation de l'API.

## 7. Préparer les variables du modèle

Le pipeline attend `PU_DO` et `trip_distance`. Ajoutez :

```python
def prepare_features(ride: Ride) -> dict:
    return {
        "PU_DO": f"{ride.PULocationID}_{ride.DOLocationID}",
        "trip_distance": ride.trip_distance,
    }
```

La transformation qui crée `PU_DO` appartient au contrat entre l'API et le pipeline. `DictVectorizer`, déjà présent dans le pipeline, effectuera ensuite l'encodage.

## 8. Charger le modèle au démarrage

Ajoutez :

```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    client = MlflowClient(tracking_uri=MLFLOW_TRACKING_URI)

    version = client.get_model_version_by_alias(
        name=MODEL_NAME,
        alias=MODEL_ALIAS,
    )
    model = mlflow.sklearn.load_model(MODEL_URI)

    app.state.model = model
    app.state.model_version = str(version.version)

    logger.info(
        "model_loaded name=%s alias=%s version=%s",
        MODEL_NAME,
        MODEL_ALIAS,
        version.version,
    )

    yield
```

Le modèle est chargé une seule fois au démarrage. Si MLflow est inaccessible ou si l'alias n'existe pas, le service échoue clairement au lieu de démarrer sans modèle.

## 9. Créer l'application et la route de contrôle

Ajoutez :

```python
app = FastAPI(
    title="NYC Taxi Duration API",
    version="0.1.0",
    lifespan=lifespan,
)


@app.get("/health")
def health(request: Request):
    return {
        "status": "ready",
        "model_name": MODEL_NAME,
        "model_alias": MODEL_ALIAS,
        "model_version": request.app.state.model_version,
    }
```

La route `/health` confirme que l'application a démarré avec un modèle. Elle fournit aussi la version effectivement chargée.

## 10. Créer la route de prédiction

Ajoutez :

```python
@app.post("/predict", response_model=Prediction)
def predict(ride: Ride, request: Request):
    request_id = str(uuid4())
    started_at = perf_counter()

    features = prepare_features(ride)
    prediction = request.app.state.model.predict([features])[0]
    latency_ms = (perf_counter() - started_at) * 1000

    logger.info(
        "prediction request_id=%s model_version=%s latency_ms=%.2f",
        request_id,
        request.app.state.model_version,
        latency_ms,
    )

    return Prediction(
        duration_minutes=float(prediction),
        model_name=MODEL_NAME,
        model_alias=MODEL_ALIAS,
        model_version=request.app.state.model_version,
        request_id=request_id,
    )
```

Chaque réponse contient un identifiant de requête et la version du modèle. Les journaux conservent la latence sans enregistrer toutes les données du trajet.

## 11. Démarrer MLflow

Dans un premier terminal, à la racine du dépôt :

```bash
conda activate mlops
mlflow server \
  --host 0.0.0.0 \
  --port 5000 \
  --backend-store-uri sqlite:///mlflow.db \
  --serve-artifacts \
  --artifacts-destination ./mlartifacts
```

Gardez le serveur actif pendant le test du service.

## 12. Démarrer l'API

Dans un deuxième terminal :

```bash
conda activate mlops
export MLFLOW_TRACKING_URI="http://127.0.0.1:5000"
export MODEL_NAME="nyc-taxi-duration-model"
export MODEL_ALIAS="champion"

uvicorn learning_mlops.api:app --host 0.0.0.0 --port 8000
```

Le journal doit contenir `model_loaded` avec le nom, l'alias et le numéro de version.

Dans Codespaces, ouvrez le port 8000 avec une visibilité **Private**.

## 13. Vérifier le service

Dans un troisième terminal, appelez la route de contrôle :

```bash
curl http://127.0.0.1:8000/health
```

La réponse doit indiquer `ready` et présenter la version chargée.

Ouvrez également [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs). FastAPI génère une documentation interactive à partir des routes et des modèles Pydantic.

## 14. Demander une prédiction

Envoyez un trajet valide :

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "PULocationID": 161,
    "DOLocationID": 236,
    "trip_distance": 3.2
  }'
```

La réponse doit contenir la durée estimée, la version du modèle et un identifiant de requête.

## 15. Tester une entrée incorrecte

Envoyez une distance négative :

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "PULocationID": 161,
    "DOLocationID": 236,
    "trip_distance": -3.2
  }'
```

FastAPI doit refuser la requête avant l'appel du modèle et retourner une erreur de validation.

## 16. Changer de version

Attribuez l'alias `champion` à une autre version depuis le registre MLflow, puis redémarrez l'API.

Vérifiez que `/health` affiche le nouveau numéro de version. Le code du service et son URI restent identiques. Le redémarrage est nécessaire, car le modèle est chargé une seule fois au démarrage.

## 17. Exercice

Sans modifier la fonction d'entraînement :

1. ajoutez un champ facultatif `request_id` dans la requête et générez-le lorsqu'il est absent ;
2. ajoutez une route qui retourne uniquement les informations sur le modèle chargé ;
3. envoyez trois requêtes valides avec des distances différentes ;
4. retrouvez leur identifiant, leur latence et leur version dans les journaux ;
5. testez une zone égale à zéro et un champ manquant ;
6. expliquez à quel moment chaque requête est refusée ;
7. déplacez l'alias `champion`, redémarrez le service et vérifiez la version.

### Conseils

- Vérifiez d'abord `/health` avant de tester `/predict`.
- Vérifiez l'alias dans MLflow si le service échoue au démarrage.
- Utilisez un modèle enregistré après la création du pipeline complet.
- Ne rechargez pas le modèle dans la fonction `predict`.
- Ne supposez pas qu'un changement d'alias modifie un processus déjà démarré.

## 18. À retenir

Le registre sépare le code du service de la version du modèle. L'alias fournit une référence stable, tandis que les journaux conservent la version réellement chargée. Le pipeline enregistré réunit la transformation et le modèle afin que l'API puisse traiter directement les variables préparées.

Sources techniques : [FastAPI](https://fastapi.tiangolo.com/), [FastAPI Lifespan](https://fastapi.tiangolo.com/advanced/events/) et [MLflow Model Registry](https://mlflow.org/docs/latest/ml/model-registry/).
