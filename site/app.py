from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('accueil.html')

@app.route('/connexion', methods=['GET', 'POST'])
def connexion():
    if request.method == 'POST':
        # Ici, vous récupérerez les données du formulaire et effectuerez la logique de connexion
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Remplacez ceci par votre logique d'authentification
        if username == "exemple" and password == "motdepasse":
            return redirect(url_for('accueil'))  # Redirigez vers la page d'accueil en cas de succès
        else:
            return render_template('connexion.html', error="Login/Mot de passe Incorrect")

    return render_template('connexion.html')

if __name__ == '__main__':
    app.run(debug=True)
