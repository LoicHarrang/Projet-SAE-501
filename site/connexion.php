<?php
include('includes/header.php');

// Fonction pour se connecter à l'API en utilisant cURL avec JSON
function connexionAPI($login, $password)
{
    $url = "http://192.168.197.129:8080/check_account";
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

?>

<div class="wrapper">
    <div id="formContent" data-aos="zoom-in-down">
        <!-- Icon -->
        <div class="first">
            <img src="img/mamazon.png" id="icon" alt="Mamazon" />
            <h1>Connexion</h1>
        </div>

        <!-- Login Form -->
        <form method="POST" action="<?php echo $_SERVER['PHP_SELF']; ?>">
            <!-- Si un formulaire a déjà été rempli, on conserve le login mais pas le mot de passe -->
            <input type="text" id="login" class="second" name="login" required placeholder="username" value="<?php if (isset($_POST["login"])) echo $_POST["login"]; ?>">
            <input type="password" id="password" class="third" required name="password" placeholder="password">
            <input type="submit" class="fourth" value="Connexion" name="connexion">
        </form>
        
        <?php
        // Si on a reçu des données en post on peut afficher un résultat
        if ($_POST) {
            // on vérifie que toutes les champs sont bien arrivés
            if (
                empty($_SESSION)
                && !empty($_POST["connexion"])
                && isset($_POST["login"])
                && isset($_POST["password"])
            ) {
                $etatConnexion = connexionAPI($_POST["login"], $_POST["password"]);
                if (isset($etatConnexion['status']) && $etatConnexion['status'] === 'success') {
                    $_SESSION["login"] = $etatConnexion["user"]["login"];
                    $_SESSION["statut"] = $etatConnexion["user"]["statut"];

                    echo '<p id="connexionOk">' . "\n";
                    echo "Connexion réussie <br />\n";
                    echo "Redirection...<br />\n";
                    echo "</p>\n";
                } else {
                    echo '<p id="connexionPasOk">' . "\n";
                    echo "Login/Mot de passe Incorrect\n";
                    echo "</p>\n";
                }
                 // on rentre les informations dans les logs dans tous les cas
                 logsConnexion();
                 // on redirige 
                 // si la session est créée alors on sera redirigé vers l'index, sinon on reste sur connexion
                 redirect();
            }
        }
        ?>

    </div>
</div>

<?php
include('includes/footer.php');
?>
