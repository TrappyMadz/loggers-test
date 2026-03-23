# MyBank Logging Pipeline (Stack ELK)

Ce projet met en place une infrastructure de monitoring complète pour une application bancaire (FastAPI). Il permet de capturer, transformer et visualiser les transactions financières en temps réel en utilisant la puissance de la suite Elastic.

## Fonctionnalités

Collecte automatisée : Capture des logs stdout via le driver Docker GELF.

Parsing intelligent : Transformation des messages texte en champs numériques (amount, new_balance) via Logstash.

Filtrage : Suppression des logs techniques inutiles pour ne garder que les données métier.

Visualisation : Dashboard Kibana temps réel (Solde actuel, évolution historique, répartition Dépôts/Retraits).

## Architecture Technique

- Application (FastAPI) : Génère des logs structurés en JSON.

- Docker Logging Driver (GELF) : Expédie les logs vers Logstash en UDP.

- Logstash :
  - Reçoit les paquets GELF.

  - Décode le JSON.

  - Utilise des filtres Grok pour extraire les montants des phrases métier.

- Elasticsearch : Stocke et indexe les données structurées.

- Kibana : Interface de visualisation des données.

## Visualisations incluses

D'après les dashboards configurés :

Métrique de Solde : Affiche la dernière valeur connue du champ new_balance.

Historique des Transactions : Histogramme temporel montrant les variations du solde par tranches de 30 secondes.

Analyse des Flux : Graphique en "Donut" montrant la répartition en pourcentage entre les dépôts (deposit) et les retraits (withdrawal).

![Capture d'écran des graphes](https://i.imgur.com/d5DovYo.png)

## Installation et Lancement

Pré-requis

Docker et Docker Compose installés.

### Remplissage des variables

- Créer un fichier `.env` ou remplir les variables d'environnement suivantes :

```
APP_PORT
ELASTIC_PORT
KIBANA_PORT
```

> Par défaut les ports sont respectivement 8000, 9200 et 5601

### Lancer l'ensemble de la stack

```bash
docker compose up -d
```

L'application attend automatiquement que Logstash soit prêt via un système de healthchecks.
Tests

## Commandes utiles

### Effectuer un dépôt

```bash
curl -X POST "http://localhost:<APP_PORT>/deposit" -H "Content-Type: application/json" -d '{"value": <valeur>}'
```

### Effectuer un retrait

```bash
curl -X POST "http://localhost:<APP_PORT>/withdraw" -H "Content-Type: application/json" -d '{"value": <valeur>}'
```

## Configuration Logstash (Aperçu)

Le pipeline Logstash utilise une logique de filtrage par motifs :

    Input : gelf sur le port 5000 (en dur).

    Filter :

        json pour le décodage initial.

        grok pour capturer %{NUMBER:amount:float}.

        mutate pour typer les données et permettre les calculs dans Kibana.
