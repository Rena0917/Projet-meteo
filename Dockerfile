# Image de base Python officielle
FROM python:3.9-slim

# Dossier de travail dans le conteneur
WORKDIR /app

# Copier tout le contenu du dossier local dans /app
COPY . /app

# Installer les librairies nécessaires
RUN pip install requests matplotlib fpdf

# Commande à exécuter au démarrage du conteneur
CMD ["python", "meteo_multi.py"]
