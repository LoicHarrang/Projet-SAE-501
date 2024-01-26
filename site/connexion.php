<?php
include('includes/header.php');
require_once 'includes/fonctions.php';
// Fonction pour se connecter à l'API en utilisant cURL avec JSON


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
                $etatConnexion = connexionAPI2($_POST["login"], $_POST["password"]);
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
