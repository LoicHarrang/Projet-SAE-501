<?php
    try{
        // Connexion à la bdd
        $BDD = new PDO('pgsql:host=psql;port=5432;dbname=site;', 'loic', '123456789');
        // Pour éviter de faire PDO::FETCH_ASSOC à chaque fois qu'il faut récupérer des résultats
        $BDD->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
        // Récupère les erreurs dans la variable BDD (plus simple à débug)
        $BDD->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION); // ERRMODE_WARNING | ERRMODE_EXCEPTION | ERRMODE_SILENT
    } 
    catch(Exception $e) {
        echo "Impossible d'accéder à la base de données PSQL : ".$e->getMessage();
        die();
    }

?>