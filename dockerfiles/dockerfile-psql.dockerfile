FROM postgres:latest

ENV POSTGRES_USER=loic
ENV POSTGRES_PASSWORD=123456789
ENV POSTGRES_DB=site

COPY bdd/data/ /docker-entrypoint-initdb.d/