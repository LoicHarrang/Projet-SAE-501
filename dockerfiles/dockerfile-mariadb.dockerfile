FROM mariadb:latest

ENV MARIADB_ROOT_PASSWORD=123456789
ENV MARIADB_DATABASE="site"
ENV MARIADB_USER="loic"
ENV MARIADB_PASSWORD=123456789

COPY bdd/auth/ /docker-entrypoint-initdb.d/