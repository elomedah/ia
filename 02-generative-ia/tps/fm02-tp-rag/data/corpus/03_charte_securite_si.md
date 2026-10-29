# Charte de sécurité des systèmes d'information

*Orbitale SAS · Direction des Systèmes d'Information · référence SEC-CH-04 · version du 3 mars 2026*

> Document fictif créé pour les besoins pédagogiques du module FM02.

## 1. Objet

La présente charte définit les règles de sécurité applicables à tout utilisateur du système d'information d'Orbitale : collaborateurs, alternants, stagiaires et prestataires.

## 2. Mots de passe et authentification

- Un mot de passe compte au moins **14 caractères** et mélange majuscules, minuscules, chiffres et caractères spéciaux.
- Il est changé tous les **12 mois**, ou immédiatement en cas de suspicion de compromission.
- Les 5 derniers mots de passe ne peuvent pas être réutilisés.
- L'**authentification multifacteur (MFA)** est obligatoire pour la messagerie, le VPN et tous les outils accessibles depuis Internet. L'application d'authentification approuvée est installée sur le téléphone professionnel ou personnel.
- Le compte est verrouillé après **5 tentatives** de connexion échouées ; le déverrouillage se fait via le portail Helpdesk.

L'usage d'un gestionnaire de mots de passe est recommandé : la DSI fournit une licence au coffre-fort d'entreprise **Vault-Orbitale**.

## 3. Classification des données

| Niveau | Exemples | Règle de partage |
|---|---|---|
| Public | Plaquettes commerciales, offres d'emploi | Libre |
| Interne | Procédures, organigramme | Collaborateurs uniquement |
| Confidentiel | Données clients, contrats, paie | Besoin d'en connaître, chiffrement obligatoire |
| Secret | Fusions et acquisitions, incidents majeurs | Liste nominative validée par la direction |

Les données « Confidentiel » et « Secret » ne doivent jamais être copiées sur une clé USB personnelle ni envoyées vers une messagerie personnelle.

## 4. Usage des outils d'IA générative

Il est interdit de saisir des données classées « Confidentiel » ou « Secret » dans un service d'IA générative public. Seul l'assistant interne **Orbi**, hébergé sur l'infrastructure d'Orbitale, est autorisé pour les données internes. Toute nouvelle application d'IA doit être déclarée à la DSI avant usage.

## 5. Postes de travail

- Le poste est verrouillé (touches Windows + L) dès que l'utilisateur s'absente.
- L'installation de logiciels se fait uniquement via le **catalogue logiciel** de la DSI.
- Les mises à jour de sécurité sont installées dans un délai de **7 jours** après leur publication.

## 6. Signalement des incidents

Tout incident ou suspicion d'incident (courriel d'hameçonnage, perte ou vol de matériel, comportement anormal du poste) est signalé **dans l'heure** :

1. par courriel à **securite@orbitale.example** ;
2. ou par un ticket Helpdesk de catégorie **SEC-2** ;
3. en cas de vol ou de perte du matériel, également par téléphone au **01 00 00 42 42** (astreinte 24 h sur 24).

Un courriel d'hameçonnage ne doit pas être transféré : utilisez le bouton « Signaler » de la messagerie.

## 7. Sanctions

Le non-respect de la charte peut entraîner la suspension des accès et des sanctions disciplinaires prévues au règlement intérieur.
