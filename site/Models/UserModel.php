<?php
class UserModel {
    public function connexionAPI2($login, $password) {
        $url = "http://192.168.197.129:8080/check_account";

        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode(['login' => $login, 'password' => $password]));

        $result = curl_exec($ch);
        if ($result === FALSE) {
            die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
        }

        curl_close($ch);
        return json_decode($result, true);
    }

    function connexion($login, $pass)
    {
        // Appel à la fonction connexionAPI2 avec $this->
        $etatConnexion = $this->connexionAPI2($login, $pass);

        if (isset($etatConnexion['status']) && $etatConnexion['status'] === 'success') {
            // Connexion réussie, création de la session
            $_SESSION["login"] = $etatConnexion["user"]["login"];
            $_SESSION["statut"] = $etatConnexion["user"]["statut"];
            $_SESSION["jwt"] = $etatConnexion["access_token"];
            return true;
        } else {
            // Connexion échouée
            return false;
        }
    }


    public function logsConnexion() {
        // Implémentez la logique pour enregistrer les logs de connexion
    }
}
