# Utilise la dernière version de l'image officielle PostgreSQL comme image de base
FROM postgres:latest

# Définit le nom d'utilisateur pour l'administrateur de la base de données PostgreSQL.
# Ce sera l'utilisateur utilisé pour se connecter à PostgreSQL et gérer les bases de données.
ENV POSTGRES_USER=loic

# Définit le mot de passe pour l'utilisateur 'loic'.
# Il est crucial de le changer en production pour garantir la sécurité de la base de données.
ENV POSTGRES_PASSWORD=123456789

# Crée une base de données nommée 'site' lors de l'initialisation du conteneur.
# Cela permet de commencer directement avec une base de données prédéfinie au lieu de devoir en créer une manuellement.
ENV POSTGRES_DB=site

# Copie les fichiers de données (comme les scripts SQL) depuis le dossier local 'bdd/data/' 
# vers le dossier '/docker-entrypoint-initdb.d/' dans l'image.
# PostgreSQL exécutera automatiquement tous les scripts SQL ou les fichiers shell présents dans ce dossier
# lors du premier démarrage du conteneur, ce qui permet d'initialiser la base de données avec des structures de tables,
# des données, ou des permissions spécifiques.
COPY bdd/data/ /docker-entry-initdb.d/
