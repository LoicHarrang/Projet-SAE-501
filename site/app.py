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
