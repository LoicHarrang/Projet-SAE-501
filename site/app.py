from flask import Flask, render_template, request, session, redirect, url_for
import requests
import utils

app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'

# Fonction équivalente à connexionAPI2() en PHP
def connexion_api2(login, password):
    url = "http://192.168.197.129:8080/check_account"
    response = requests.post(url, json={'username': login, 'password': password})
    if response.ok:
        return response.json()
    else:
        return None

# Fonction pour lister le matériel (équivalent de listeMateriel() en PHP)
def liste_materiel():
    url = "http://192.168.197.129:8081/materiels"
    response = requests.get(url)
    if response.ok:
        return response.json().get('materiels', [])
    else:
        return []

# Fonction pour lister les produits par type (équivalent de listerProduitParType() en PHP)
def lister_produit_par_type(type_mat):
    url = f"http://192.168.197.129:8081/materiels/type/{type_mat}"
    response = requests.get(url)
    if response.ok:
        return response.json().get('produits', [])
    else:
        return []
    
def recup_fournisseur_api():
    # URL de votre API pour récupérer la liste des fournisseurs
    url = "http://192.168.197.129:8081/fournisseurs"

    # Exécution de la requête GET
    response = requests.get(url)

    # Vérification si la requête a réussi
    if response.ok:
        # Décodage de la réponse JSON
        json_result = response.json()
        return json_result
    else:
        print('Erreur lors de la requête vers l\'API')
        return None

def recup_fournisseur():
    # Appel à la fonction recup_fournisseur_api()
    resultat_api = recup_fournisseur_api()

    # Vérification si le résultat est valide
    if resultat_api and 'status' in resultat_api and resultat_api['status'] == 'success':
        # Retour de la liste des fournisseurs
        return resultat_api['fournisseurs']
    else:
        # Gestion de l'erreur ou liste vide
        return []
    
def insertion_api(type_mat, marque, fournisseur, description, nom_image, prix):
    url = "http://192.168.197.129:8081/materiels"

    # Préparation des données à envoyer
    data = {
        'type': type_mat,
        'marque': marque,
        'fournisseur': fournisseur,
        'description': description,
        'nom_image': nom_image,
        'prix': prix
    }
    json_data = json.dumps(data)

    # Configuration de la requête POST
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json_data, headers=headers)

    if response.status_code == 200:
        json_result = response.json()
        return json_result
    else:
        raise Exception(f"Erreur lors de la requête vers l'API : {response.status_code}")

def insertion(type_mat, marque, fournisseur, description, nom_image, prix):
    try:
        result_api = insertion_api(type_mat, marque, fournisseur, description, nom_image, prix)
        if 'status' in result_api and result_api['status'] == 'success':
            return True
        else:
            return False
    except Exception as e:
        raise e


@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        login = request.form.get('login')
        password = request.form.get('password')
        
        # Appel à l'API pour vérifier les identifiants
        response = requests.post('http://192.168.197.129:8080/check_account', json={'username': login, 'password': password})
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'success':
                # Stockez les informations nécessaires dans la session
                session['login'] = data['user']['login']
                session['statut'] = data['user']['statut']
                # Redirection vers la page d'accueil après connexion réussie
                return redirect(url_for('accueil'))
            else:
                error = 'Login/Mot de passe Incorrect'
        else:
            error = 'Erreur lors de la connexion à l\'API'
    else:
        error = None
    return render_template('connexion.html', error=error)

@app.route('/insertion', methods=['GET', 'POST'])
def insertion_route():
    # Vérifier si l'utilisateur est connecté et est un administrateur
    if 'login' not in session or session.get('statut') != 'administrateur':
        return redirect(url_for('connexion'))

    types = ['accessoire', 'écran', 'portable', 'serveur', 'station']
    fournisseurs = recup_fournisseur()  # Assurez-vous que cette fonction est définie et fonctionne correctement
    materiels = liste_materiel()
    res = None  # Initialiser res pour éviter les références avant affectation

    # Logique de traitement du formulaire
    if request.method == 'POST':
        # Extrait les données du formulaire
        type_mat = request.form.get('type_mat')
        fournisseur = request.form.get('fournisseur')
        description = request.form.get('description')
        nom_image = request.form.get('nom_image')
        prix = request.form.get('prix')

        # Appeler la fonction d'insertion et afficher les résultats
        try:
            res = insertion(type_mat, fournisseur, description, nom_image, prix)  # Assurez-vous que cette fonction est définie et fonctionne correctement
        except Exception as e:
            return render_template('insertion.html', types=types, fournisseurs=fournisseurs, error=f"Erreur : {e}")

    # Pour une requête GET ou après le traitement POST, afficher le formulaire avec ou sans le résultat de l'insertion
    return render_template('insertion.html', types=types, fournisseurs=fournisseurs, res=res, materiels=materiels)


@app.route('/', methods=['GET', 'POST'])
def accueil():
    # Vérifie si l'utilisateur est connecté
    if 'login' not in session:
        # Si l'utilisateur n'est pas connecté, redirige vers la page de connexion
        return redirect(url_for('connexion'))

    # Si l'utilisateur est connecté, continue avec la logique de la page d'accueil
    materiels = liste_materiel()
    produits_filtrés = None
    if 'type_mat' in request.form:
        produits_filtrés = lister_produit_par_type(request.form['type_mat'])
    return render_template('accueil.html', materiels=materiels, produits_filtrés=produits_filtrés)

if __name__ == '__main__':
    app.run(debug=True)
