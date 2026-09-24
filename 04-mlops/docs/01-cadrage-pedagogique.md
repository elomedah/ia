# Étape 1 - Cadrage des cours IA

## 1. Périmètre

Construire progressivement **Pipelines MLOps (7 h)** et **Déploiement de services IA (14 h)** en suivant l'organisation de [DataTalksClub/mlops-zoomcamp](https://github.com/DataTalksClub/mlops-zoomcamp).

Les quatre syllabus de référence, au format PDF et DOCX complété, ont été consultés. Les volumes concordent. Les 99 h mentionnées dans les PDF concernent le bloc de compétences complet ; notre périmètre couvre **21 h**.

Les objectifs viennent des PDF et le calendrier des DOCX complétés. Les mentions administratives des documents ne constituent pas des actions demandées dans ce travail.

| Module | Dates prévues | Séances | Volume |
|---|---|---:|---:|
| Pipelines MLOps | 3 mars 2027 | 2 × 3 h 30 | 7 h |
| Déploiement de services IA | 24 mars et 14 avril 2027 | 4 × 3 h 30 | 14 h |

MLOps précède Déploiement : une API minimale et un Dockerfile seront fournis pour la première journée, puis approfondis dans le second module. Aucun travail personnel obligatoire ne complétera artificiellement les 21 h.

## 2. Organisation inspirée de MLOps Zoomcamp

Le [README du dépôt](https://github.com/DataTalksClub/mlops-zoomcamp), consulté le 10 septembre 2026, présente sept dossiers thématiques : `01-intro`, `02-experiment-tracking`, `03-orchestration`, `04-deployment`, `05-monitoring`, `06-best-practices` et `07-project`. Le parcours source est annoncé sur neuf semaines et associe notions, exercices pratiques et projet final.

Nous adaptons cette organisation aux deux syllabus. Les chapitres sont des unités thématiques ; les six demi-journées sont les unités du calendrier.

| Chapitre de notre cours | Séances | Résultat attendu dans notre adaptation |
|---|---|---|
| 01 - Introduction et cycle ML | MLOps-01 | Identifier étapes, acteurs, risques et critères de réussite |
| 02 - Expériences et modèles | MLOps-01 | Comparer les expériences et retrouver leur contexte |
| 03 - Pipeline et orchestration | MLOps-02 | Paramétrer une chaîne, observer un échec et reprendre |
| 04 - Déploiement | D1, D2, D3 | Concevoir, tester, conteneuriser, déployer et restaurer |
| 05 - Monitoring | Introduction MLOps-02, pratique D4 | Mesurer le service et analyser une dégradation |
| 06 - Bonnes pratiques et CI/CD | MLOps-02, D2, D3 | Bloquer une livraison incorrecte et conserver les preuves |
| 07 - Mini-projet | Jalons dans les six séances, restitution D4 | Livrer un service documenté et défendre ses choix |

Les bonnes pratiques seront introduites dès les premiers TP. Le mini-projet réunira leurs livrables sans ajouter de journée.

Pour tenir en 21 h : environnement préparé, squelettes ciblés, modèle léger et orchestration d'une chaîne courte avec paramètres, dépendances, traces et reprise. L'outil d'orchestration sera choisi pendant la préparation technique. FastAPI reste retenu conformément aux syllabus complétés.

Streaming, seconde plateforme cloud et infrastructure complète en code seront des prolongements facultatifs. Sécurité, confidentialité, éthique et réglementation restent intégrées aux activités obligatoires des syllabus.

## 3. Cas d'application à définir

Le cas ML sera choisi à l'étape suivante selon ces critères :

- entraînement rapide sur CPU et données de volume maîtrisé ;
- référence simple et qualité mesurable sur des données distinctes de l'entraînement ;
- prétraitement et modèle conservés ensemble ;
- contrat de prédiction clair ;
- possibilité de simuler une dégradation et une mise à jour.

Cible, variables disponibles à l'inférence, découpage des données, métriques et limites d'usage seront définis avant le code des TP du mini-projet. L'introduction utilise un exemple autonome de 500 livraisons synthétiques pour apprendre l'entraînement, l'évaluation et la reproduction ; le cas du mini-projet reste ouvert.

## 4. Progression et budget horaire

Chaque séance représente 210 minutes pédagogiques. Les pauses seront positionnées selon les horaires de l'établissement en préservant ce volume.

| Séance | Objectifs et notions | Cours | Démo | TP / projet | Restitution et évaluation | Total |
|---|---|---:|---:|---:|---:|---:|
| MLOps-01 - 03/03 : pipeline reproductible | Cycle ML, données, entraînement, MLflow et versions | 45 | 25 | 115 | 25 | 210 |
| MLOps-02 - 03/03 : orchestration et automatisation | Orchestration, traçabilité, tests, CI/CD, API/Docker fournis, monitoring et gouvernance | 40 | 25 | 120 | 25 | 210 |
| D1 - 24/03 : concevoir le service | Besoin, architecture, batch/API, contrat et transformations | 50 | 25 | 110 | 25 | 210 |
| D2 - 24/03 : API et conteneur | FastAPI, validation, erreurs, tests, Docker et configuration | 35 | 25 | 130 | 20 | 210 |
| D3 - 14/04 : déployer et mettre à jour | Cloud, livraison, disponibilité, scalabilité, vérification et rollback | 45 | 25 | 115 | 25 | 210 |
| D4 - 14/04 : superviser et justifier | Métriques techniques et modèle, incident, sécurité, confidentialité, RGPD et éthique | 40 | 20 | 110 | 40 | 210 |
| **Total** | | **255** | **145** | **700** | **160** | **1 260 = 21 h** |

Les TP représentent 11 h 40 ; pratique et restitution totalisent 14 h 20. Les évaluations sont incluses.

## 5. TP, livrables et critères de réussite

| TP | Travail à réaliser | Livrables et preuves |
|---|---|---|
| MLOps-01 - Expérience reproductible | Contrôler les données, séparer entraînement et évaluation, comparer référence et candidat, suivre deux expériences dans MLflow | Pipeline, manifeste des données/environnement, expériences et analyse ; reproduction dans une tolérance documentée, sans ajuster les transformations sur le test |
| MLOps-02 - Orchestrer et livrer | Relier préparation, entraînement et évaluation ; reprendre après échec ; compléter une CI fournie et vérifier l'API conteneurisée | Définition du pipeline, traces de reprise, contrôles, workflow et manifeste de version ; une modification incorrecte bloque la promotion |
| D1 - Concevoir le service | Comparer deux architectures, définir le contrat et implémenter l'inférence | Schéma, décision argumentée, API ; concordance avec une prédiction locale et cohérence du prétraitement |
| D2 - Tester et conteneuriser | Tester entrées invalides et artefact absent, construire l'image, externaliser la configuration | Tests, Dockerfile et installation ; un autre binôme démarre le service et vérifie que le modèle est prêt |
| D3 - Déployer et restaurer | Déployer sur un cloud pédagogique préparé, mesurer une charge bornée, publier une version puis revenir en arrière | Configuration, latence/débit et preuve de rollback ; ancienne version vérifiée par une requête |
| D4 - Diagnostiquer et présenter | Injecter une dégradation, exploiter logs/métriques, traiter un incident de confidentialité et présenter le service | Supervision, compte rendu, fiche de modèle, analyse des risques et démonstration ; correction vérifiée et limites expliquées |

MLOps-01 disposera d'un extrait de données, d'un dictionnaire et d'un squelette. MLOps-02 disposera d'une API, d'un Dockerfile et de trames d'orchestration/CI. Leur préparation vise à réserver du temps aux décisions et à l'analyse.

Pour D3, un repli local permettra de poursuivre en cas de panne, mais ne remplacera pas la preuve de déploiement cloud attendue. Pour D4, qualité prédictive, dérive des données et performance technique seront distinguées. Les démonstrations seront adaptées à l'effectif, éventuellement en parallèle, dans les 40 minutes prévues.

## 6. Exigences pédagogiques et évaluation proposée

Chaque TP comprendra un socle guidé, une décision autonome et un scénario de panne. La profondeur repose sur la justification, les mesures et l'analyse d'échecs. Les prolongements restent facultatifs.

| Critère MLOps | Points / 20 |
|---|---:|
| Données, absence de fuite et reproductibilité | 6 |
| Expériences et traçabilité | 4 |
| Orchestration, reprise, tests et CI | 6 |
| Documentation, monitoring, sécurité et justification | 4 |

| Critère Déploiement | Points / 20 |
|---|---:|
| Architecture, contrat et cohérence de l'inférence | 4 |
| Tests, conteneur et installation | 5 |
| Déploiement et rollback démontrés | 4 |
| Supervision, diagnostic, sécurité et confidentialité | 4 |
| Démonstration et justification individuelle | 3 |

Ces barèmes sont proposés et distincts des modalités institutionnelles. Le binôme conserve une vérification individuelle de compréhension. Les pondérations avec Skillogs restent à préciser selon les règles de l'établissement.

## 7. Organisation cible des fichiers

```text
README.md                        parcours et correspondance aux syllabus
docs/                            cadrage et calendrier
01-intro/
02-experiment-tracking/
03-orchestration/
04-deployment/
05-monitoring/
06-best-practices/
07-project/
commun/                          données, contrats et code partagé
infra-ia/                        environnement pédagogique
enseignant/                      corrigés, barèmes et déroulés minutés
```

Chaque chapitre regroupera un README de progression, des supports modifiables et exportés, des exemples commentés et des TP. Chaque énoncé indiquera séance, durée, prérequis, résultats et preuves à rendre. Les corrigés seront distribués séparément.

Cette arborescence est une cible. Les supports développeront les notions avec schémas, exemples, questions et références officielles. Le nombre de diapositives dépendra du temps réel de manipulation.

## 8. Construction étape par étape

1. Choisir le cas ML, profiler les données, définir référence et métriques, figer le contrat et préparer l'environnement.
2. Produire intégralement MLOps-01 : cours, TP, code de départ, corrigé et déroulé enseignant ; vérifier le parcours.
3. Produire MLOps-02 : orchestration, automatisation et incidents de validation.
4. Produire D1/D2 puis D3/D4, avec les mêmes interfaces communes.
5. Rejouer depuis un environnement vierge, mesurer les temps, vérifier la couverture des objectifs et préparer les exports.

Hypothèses : Python, Git, HTTP et bases du ML acquis ; binômes ; CPU ; environnement préinstallé. Un diagnostic court sera intégré à MLOps-01. Cloud, accès réseau, effectif et ressources des postes restent à préciser avant les TP concernés.

L'introduction est disponible dans `01-intro/` avec cours, TP progressif, scripts et tests. Elle occupe 120 minutes de MLOps-01, laissant 90 minutes au suivi des expériences. Docker local a été testé ; la configuration Codespaces est préparée et reste à vérifier à distance. Le guide enseignant se trouve dans `enseignant/01-intro-guide.md`. Les autres chapitres restent à produire ; les versions techniques et les références réglementaires seront vérifiées pendant leur rédaction.
