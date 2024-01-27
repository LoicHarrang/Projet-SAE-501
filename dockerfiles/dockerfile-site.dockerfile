# Utiliser une image de base Python officielle
FROM python:3.9-slim

# Définir le répertoire de travail dans le conteneur
WORKDIR /app

# Copier le fichier de dépendances et installer les dépendances
COPY ./site/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application dans le conteneur
COPY ./site /app

# Exposer le port sur lequel l'application Flask s'exécutera
EXPOSE 5000

# Définir la variable d'environnement pour Flask
ENV FLASK_APP=app.py
ENV FLASK_ENV=development

# Lancer l'application Flask lors du démarrage du conteneur
CMD ["flask", "run", "--host=0.0.0.0"]
