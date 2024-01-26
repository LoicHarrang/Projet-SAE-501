<?php

//$fileName = explode("/", $_SERVER['SCRIPT_NAME']);
//$fileName = end($fileName);

//##########################Fonctions utilisées###############################
// Récupération du nom de fichier pour la génération du menu en dynamique
function nomFichier()
{
	$fileName = explode("/", $_SERVER['SCRIPT_NAME']);
	$pageTitle = explode(".", end($fileName));
	return ucwords($pageTitle[0]);
}

// Affichage du nom de l'utilisateur ou demande de connexion en haut à droite du site
function afficheUtilisateur()
{
	$html = '<span id="user">' . "\n";
	// On récupère le prénom depuis l'@ mail de l'utilisateur
	if (empty($_SESSION)) {
		$html .= "Veuillez vous connecter";
	} else {
		$username = explode("@", $_SESSION["login"]);
		$html .= 'Bonjour ' . ucwords($username[0]);
	}
	$html .=  "\n" . '</span>';
	return $html;
}

//****************Connexion de l'utilisateur**************************************
function connexionAPI2($login, $password)
{
    // URL de l'API pour vérifier le compte
    $url = "http://192.168.197.129:8080/check_account";
    
    // Préparation des données à envoyer en JSON
    $data = array('username' => $login, 'password' => $password);
    $json_data = json_encode($data);

    // Initialisation de cURL
    $ch = curl_init($url);
    
    // Configuration des options cURL
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

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function connexion($login, $pass)
{
    // Appel à la fonction connexionAPI
    $etatConnexion = connexionAPI2($login, $pass);

    // Vérification du statut de connexion
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

//****************Génération des logs**************************************
function logsConnexion()
{
	$statutConnexion = "échouée";
	$statut = "Non Connecté";
	$date = new DateTime();
	$date = $date->format("d/m/y h:i:s");
	if (!empty($_SESSION)) {
		$statutConnexion = "réussie";
		$statut = $_SESSION["statut"];
	}
	// 1 : on ouvre le fichier
	$monfichier = fopen('logs/access.log', 'a+');
	// 2 : Ajout des logs
	// {date au format jj/mm/aa} {heure au format hh:mm:ss} : Connexion {échouée|réussie} de {utilisateur} (si réussie : {statut})
	// PHP_EOL = retour à la ligne
	fputs($monfichier, "$date : Connexion $statutConnexion de " . $_POST["login"] . ' depuis ' . $_SERVER['REMOTE_ADDR'] . " Statut = $statut" . PHP_EOL);
	// 3 : quand on a fini de l'utiliser, on ferme le fichier
	fclose($monfichier);
}

//****************Récupération du statut de l'utilisateur**************************************
function getStatutAPI($login)
{
    // URL de votre API pour récupérer les détails d'un compte
    $url = "http://192.168.197.129:8080/comptes/" . urlencode($login);

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function getStatut($login)
{
    // Appel à la fonction getStatutAPI
    $resultatAPI = getStatutAPI($login);

    // Vérification si le résultat est valide
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        // Retour du statut du compte
        return $resultatAPI['compte']['statut'];
    } else {
        // Gestion de l'erreur ou compte introuvable
        return false;
    }
}


//****************Récupération des différents fournisseurs**************************************
function recupFournisseurAPI()
{
    // URL de votre API pour récupérer la liste des fournisseurs
    $url = "http://192.168.197.129:8081/fournisseurs";

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function recupFournisseur()
{
    // Appel à la fonction recupFournisseurAPI
    $resultatAPI = recupFournisseurAPI();

    // Vérification si le résultat est valide
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        // Retour de la liste des fournisseurs
        return $resultatAPI['fournisseurs'];
    } else {
        // Gestion de l'erreur ou liste vide
        return false;
    }
}

//****************Redirection des pages**************************************
function redirect()
{
	$fileName = explode("/", $_SERVER['SCRIPT_NAME']);
	$fileName = end($fileName);
	// On redirige vers la page connexion.php si l'utilisateur n'est pas connecté
	if ($fileName != "connexion.php" && empty($_SESSION)) {
		header("Location: connexion.php");
		exit();
	}
	// Si l'utilisateur est connecté et qu'il est sur connexion.php, alors on le redirige vers l'index
	else if ($fileName == "connexion.php" && !empty($_SESSION)) {
		header("Location: index.php");
		exit();
	} else if (!empty($_SESSION) && $_SESSION["statut"] == 'utilisateur' && ($fileName == "modification.php" || $fileName == "insertion.php")) {
		header("Location: index.php");
		exit();
	}
}

//****************Déconnexion**************************************
function deconnexion()
{
	session_start();
	session_unset(); // == $_SESSION=array()
	session_destroy();
	redirect();
}

//****************Affichage Accès refusé**************************************
function deniedAccess()
{
	header('Location: index.php');
	exit;
}


//*******************************Récupération de toutes les données de matériel de la BDD*************************************************
function listeMaterielAPI()
{
    // URL de votre API pour récupérer la liste du matériel
    $url = "http://192.168.197.129:8081/materiels";

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function listeMateriel()
{
    // Appel à la fonction listeMaterielAPI
    $resultatAPI = listeMaterielAPI();

    // Vérification si le résultat est valide
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        // Retour de la liste du matériel
        return $resultatAPI['materiels'];
    } else {
        // Gestion de l'erreur ou liste vide
        return false;
    }
}

//****************Affichage d'un tableau**************************************
function afficheTableau($tab)
{
    // Vérifier si $tab est un tableau non vide
    if (is_array($tab) && count($tab) > 0) {
        echo '<table>';
        echo '<tr>'; // Les entêtes des colonnes

        // Parcourir le premier élément pour obtenir les en-têtes de colonne
        foreach ($tab[0] as $colonne => $valeur) {
            echo "<th>$colonne</th>";
        }
        echo "</tr>\n";

        // Le corps de la table
        foreach ($tab as $ligne) {
            echo '<tr>';
            foreach ($ligne as $entete => $cellule) {
                if ($entete == "Image") {
                    echo '<td><img class="image_table" src="img/' . $cellule . '" alt="' . $cellule . '"/></td>';
                } else if ($entete == "Prix") {
                    echo "<td>$cellule €</td>";
                } else {
                    echo "<td>$cellule</td>";
                }
            }
            echo "</tr>\n";
        }
        echo '</table>';
    } else {
        // Gérer le cas où $tab n'est pas un tableau ou est vide
        echo "Aucune donnée à afficher.";
    }
}

//*******************************Execution de l'insertion*************************************************
function insertionAPI($type, $marque, $fournisseur, $description, $nom_image, $prix)
{
    $url = "http://192.168.197.129:8081/materiels";

    // Préparation des données à envoyer
    $data = array(
        'type' => $type,
        'marque' => $marque,
        'fournisseur' => $fournisseur,
        'description' => $description,
        'nom_image' => $nom_image,
        'prix' => $prix
    );
    $json_data = json_encode($data);

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
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

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function insertion($type, $marque, $fournisseur, $description, $nom_image, $prix)
{
    // Appel à la fonction insertionAPI
    $resultatAPI = insertionAPI($type, $marque, $fournisseur, $description, $nom_image, $prix);

    // Vérification si l'insertion a réussi
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        return true;
    } else {
        return false;
    }
}


//*******************************Récupération de l'Id du fournisseur à partir du nom*************************************************
function getIdFournisseurAPI($fournisseur)
{
    $url = "http://192.168.197.129:8081/fournisseurs/" . urlencode($fournisseur);

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function getIdFournisseur($fournisseur)
{
    // Appel à la fonction getIdFournisseurAPI
    $resultatAPI = getIdFournisseurAPI($fournisseur);

    // Vérification si le résultat est valide
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        return $resultatAPI['id'];
    } else {
        return false;
    }
}


//*******************************Récupération de l'id du matériel à partir de sa description*************************************************
function getIdMaterielAPI($description)
{
    // Mise à jour de l'URL pour utiliser la route /materiels/query avec un paramètre de requête pour la description
    $url = "http://192.168.197.129:8081/materiels/query?" . http_build_query(['description' => $description]);

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    // Vérifiez si des matériels ont été trouvés et retournez le premier ID trouvé
    if (!empty($json_result['materiels'])) {
        return $json_result['materiels'][0]['Id']; // Supposant que 'Id' est la clé dans le JSON retourné
    } else {
        return null; // Aucun matériel trouvé pour cette description
    }
}


function getIdMateriel($description)
{
    // Appel à la fonction getIdMaterielAPI
    $resultatAPI = getIdMaterielAPI($description);

    // Vérification si le résultat est valide
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        return $resultatAPI['id'];
    } else {
        return false;
    }
}


//*******************************Récupération de tous les id du matériel*************************************************
function listeIdMaterielAPI()
{
    $url = "http://192.168.197.129:8081/materiels/ids";

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function listeIdMateriel()
{
    // Appel à la fonction listeIdMaterielAPI
    $resultatAPI = listeIdMaterielAPI();

    // Vérification si le résultat est valide
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        return $resultatAPI['ids'];
    } else {
        return false;
    }
}


//*******************************Execution des modifications*************************************************
function modificationAPI($type, $marque, $fournisseur, $description, $prix, $idMateriel)
{
    $url = "http://192.168.197.129:8081/materiels/" . $idMateriel;

    // Préparation des données à envoyer
    $data = array(
        'type' => $type,
        'marque' => $marque,
        'fournisseur' => $fournisseur,
        'description' => $description,
        'prix' => $prix,
        'id_materiel' => $idMateriel
    );
    $json_data = json_encode($data);

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
    curl_setopt($ch, CURLOPT_POSTFIELDS, $json_data);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function modification($type, $marque, $fournisseur, $description, $prix, $idMateriel)
{
    // Appel à la fonction modificationAPI
    $resultatAPI = modificationAPI($type, $marque, $fournisseur, $description, $prix, $idMateriel);

    // Vérification si la modification a été réussie
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        return 1;
    } else {
        return 0;
    }
}

//*******************************Filtrage des produits par type*************************************************
function listerProduitParTypeAPI($type_mat)
{
    $url = "http://192.168.197.129:8081/materiels/type/" . urlencode($type_mat);

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function listerProduitParType($type_mat)
{
    // Appel à la fonction listerProduitParTypeAPI
    $resultatAPI = listerProduitParTypeAPI($type_mat);

    // Vérification si le résultat est valide
    if (isset($resultatAPI['status']) && $resultatAPI['status'] === 'success') {
        return $resultatAPI['produits'];
    } else {
        return false;
    }
}


//*******************************Vérifier l'unicité des tables*************************************************
function alreadyExistAPI($marque, $fournisseur, $description)
{
    $url = "http://192.168.197.129:8081/materiels/exist?marque=" . urlencode($marque) . "&fournisseur=" . urlencode($fournisseur) . "&description=" . urlencode($description);

    // Initialisation de cURL
    $ch = curl_init($url);

    // Configuration des options cURL
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, array('Content-Type: application/json'));

    // Exécution de la requête cURL
    $result = curl_exec($ch);
    if ($result === FALSE) {
        die('Erreur lors de la requête vers l\'API : ' . curl_error($ch));
    }

    // Fermeture de la session cURL
    curl_close($ch);

    // Décodage de la réponse JSON
    $json_result = json_decode($result, true);

    return $json_result;
}

function alreadyExist($marque, $fournisseur, $description)
{
    // Appel à la fonction alreadyExistAPI
    $resultatAPI = alreadyExistAPI($marque, $fournisseur, $description);

    // Vérification si le produit existe déjà
    return isset($resultatAPI['status']) && $resultatAPI['status'] === 'success' && $resultatAPI['exists'];
}

