<?php
class LoginController {
    private $userModel;

    public function __construct() {
        $this->userModel = new UserModel();
    }

    public function login() {
        $login = $_POST['login'] ?? null;
        $password = $_POST['password'] ?? null;
        $message = null;
    
        if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['connexion'])) {
            $etatConnexion = $this->userModel->connexion($login, $password);
    
            // Vérifiez si $etatConnexion est TRUE au lieu de 'success'
            if ($etatConnexion === true) {
                // Supposons que les informations de l'utilisateur soient stockées en session dans la méthode connexion()
                $message = ['id' => 'connexionOk', 'text' => "Connexion réussie <br />Redirection..."];
                // Redirection ici si nécessaire
            } else {
                $message = ['id' => 'connexionPasOk', 'text' => "Login/Mot de passe Incorrect"];
            }
    
            $this->userModel->logsConnexion();
        }
    
        require 'Views/loginView.php';
    }    
}
