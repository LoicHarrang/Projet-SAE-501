<?php
class ProductModel {
    // Méthode pour interroger l'API et récupérer la liste du matériel
    private function listeMaterielAPI() {
        $url = "http://192.168.197.129:8081/materiels"; // URL de l'API

        $ch = curl_init($url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, ['Content-Type: application/json']);

        $result = curl_exec($ch);
        if ($result === FALSE) {
            die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
        }

        curl_close($ch);
        return json_decode($result, true);
    }

    // Méthode publique pour obtenir la liste du matériel
    public function listeMateriel() {
        $resultatAPI = $this->listeMaterielAPI();

        if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
            return $resultatAPI['materiels'];
        } else {
            return false;
        }
    }
}
