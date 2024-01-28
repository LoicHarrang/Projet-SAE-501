from flask import render_template

def generate_menu(tableau_menu, current_page):
    # Logique pour générer le menu
    return render_template('menu.html', tableau_menu=tableau_menu, current_page=current_page)

def display_insert_form():
    # Logique pour afficher le formulaire d'insertion
    types = ['accessoire', 'écran', 'portable', 'serveur', 'station']
    fournisseurs = retrieve_suppliers()  # Assurez-vous d'avoir une fonction pour récupérer les fournisseurs
    return render_template('insert_form.html', types=types, fournisseurs=fournisseurs)

def display_material_selection_form():
    # Logique pour afficher le formulaire de sélection de matériel
    material_ids = list_material_ids()  # Assurez-vous d'avoir une fonction pour lister les IDs de matériel
    return render_template('select_material_form.html', material_ids=material_ids)

def display_material_modification_form(material_id):
    # Logique pour afficher le formulaire de modification de matériel
    material_details = get_material_details(material_id)  # Assurez-vous d'avoir une fonction pour obtenir les détails du matériel
    types = ['accessoire', 'écran', 'portable', 'serveur', 'station']
    fournisseurs = retrieve_suppliers()  # Assurez-vous d'avoir une fonction pour récupérer les fournisseurs
    return render_template('modify_material_form.html', material_details=material_details, types=types, fournisseurs=fournisseurs)

def display_material_type_form():
    # Logique pour afficher le formulaire de filtrage par type de matériel
    types = ['accessoire', 'écran', 'portable', 'serveur', 'station']
    return render_template('filter_by_type_form.html', types=types)
