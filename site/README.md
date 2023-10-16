# Projet-Web
Application WEB par Quentin Noilou et Mathys Person

Adaptation microservice / docker par Loic HARRANG

## Construction et Lancement des containers : 

docker build -f dockerfiles/dockerfile-NOM.dockerfile -t NOM .

docker run -d --network network_etape_X --name NOM {-p 80:80 SEULEMENT POUR SITE} NOM