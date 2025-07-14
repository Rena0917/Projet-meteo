# 📊 Projet Analyse Météo en Python + SQLite

## Description
Ce projet récupère les données météo de plusieurs villes via l'API **Open-Meteo**, les enregistre dans une base de données SQLite, génère des graphiques et exporte des rapports au format CSV et PDF. Une interface web Streamlit permet également de visualiser les relevés et les prévisions.

## Technologies utilisées
- Python 3.12
- SQLite 3
- Requests
- Matplotlib
- FPDF
- Streamlit
- Docker (avec Dockerfile et docker-compose)

## Structure du projet
- `meteo_multi.py` : script principal
- `Dockerfile` et `docker-compose.yml` : configuration Docker
- `previsions.csv` : export des prévisions
- `rapport_previsions.pdf` : rapport PDF généré
- `meteo_multi.db` : base de données SQLite

## Fonctionnalités
- Récupération des températures et du vent
- Prévisions sur 7 jours
- Stockage en base SQLite
- Génération de graphiques et de rapports PDF
- Export CSV des prévisions

## Auteur  
Imanedah