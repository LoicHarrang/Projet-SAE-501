<?php

// Fonction pour se connecter à l'API en utilisant cURL avec JSON
function connexionAPI($login, $password)
{
    $url = "api_auth:8080/check_account";
    $data = array('username' => $login, 'password' => $password);

    // Encodage des données en JSON
    $json_data = json_encode($data);

    $ch = curl_init($url);
    
    // Configuration de cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $json_data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);

    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    $json_result = json_decode($result, true);

    return $json_result;
}

$etatConnexion = connexionAPI("loic@client.fr", "loic");

var_dump($etatConnexion);

?>