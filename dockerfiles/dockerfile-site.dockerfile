# Base de l'image sur la version PHP 8.2 avec Apache intégré.
FROM php:8.2-apache

# Copie le contenu du dossier 'site' dans l'image au chemin '/var/www/html/', en s'assurant que le propriétaire est 'www-data'.
COPY --chown=www-data:www-data site /var/www/html/

# Met à jour les listes de paquets, installe les dépendances nécessaires pour PDO et PostgreSQL,
# installe les extensions PHP pour PDO et pdo_pgsql, puis nettoie les paquets inutiles et les fichiers temporaires.
RUN apt-get update; \
    apt-get install -y libpq5 libpq-dev; \
    docker-php-ext-install pdo pdo_pgsql; \
    apt-get autoremove --purge -y libpq-dev; \
    apt-get clean ; \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* /usr/share/doc/*

# Installe l'extension PHP pdo_mysql, nécessaire pour utiliser PDO avec MySQL.
RUN docker-php-ext-install pdo_mysql
