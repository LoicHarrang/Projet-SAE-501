# Utiliser l'image officielle PHP avec Apache
FROM php:8.0-apache

# Installer les extensions PHP nécessaires
RUN docker-php-ext-install pdo pdo_mysql

# Activer le mod_rewrite pour Apache
RUN a2enmod rewrite

# Copier les fichiers source de l'application dans le conteneur
COPY ./site /var/www/html/

# Exposer le port 80
EXPOSE 80
