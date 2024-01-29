# Utilise l'image officielle de MariaDB comme image de base
FROM mariadb:latest

# Définit le mot de passe root pour MariaDB. À utiliser avec prudence et à changer en production
ENV MARIADB_ROOT_PASSWORD=123456789

# Crée une base de données nommée 'site' lors de l'initialisation du conteneur
ENV MARIADB_DATABASE=site

# Crée un utilisateur 'loic' avec le mot de passe spécifié pour la base de données
ENV MARIADB_USER=loic
ENV MARIADB_PASSWORD=123456789

# Copie les fichiers de script SQL ou les fichiers de commandes shell depuis le dossier local 'bdd/auth/' 
# vers le dossier '/docker-entrypoint-initdb.d/' dans l'image.
# Ces scripts seront exécutés lors de la première initialisation de la base de données.
COPY bdd/auth/ /docker-entrypoint-initdb.d/
