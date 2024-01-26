from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import mysql.connector
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()

# Configuration de la connexion à la base de données MySQL
def get_db_conn_mysql():
    conn = mysql.connector.connect(
        user="loic",
        password="123456789",
        database="site",
        host="mariadb",
    )
    return conn

def get_db_conn_psql():
    conn = psycopg2.connect(
        user="loic",
        password="123456789",
        database="site",
        host="psql",
        cursor_factory=RealDictCursor
    )
    return conn

def getIdFournisseur(fournisseur_nom: str, db_conn):
    with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("SELECT NoFournisseur FROM Fournisseur WHERE NomFournisseur = %s", (fournisseur_nom,))
        result = cursor.fetchone()
        return result['NoFournisseur'] if result else None


# Modèle Pydantic pour la création et la mise à jour d'un compte
class CompteCreate(BaseModel):
    login: str
    password: str
    statut: str

class CompteUpdate(BaseModel):
    password: str
    statut: str
    
class Materiel(BaseModel):
    type: str
    marque: str
    fournisseur: str
    description: str
    nom_image: str
    prix: float


class MaterielUpdate(BaseModel):
    type: str
    marque: str
    fournisseur: str
    description: str
    prix: float
    id_materiel: int

@app.get("/materiels/exist")
async def check_existence(marque: str, fournisseur: str, description: str, db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
        SELECT * FROM Materiel AS m
        INNER JOIN Propose as P ON p.nomateriel = m.nomateriel
        INNER JOIN Fournisseur AS f ON f.nofournisseur = p.nofournisseur
        WHERE m.marque = %s AND m.description = %s AND f.nomFournisseur = %s
        """, (marque, description, fournisseur))
        produit = cursor.fetchone()
        return {"status": "success", "exists": bool(produit)}
    finally:
        cursor.close()
        
# Opération CRUD : Lire un compte par login
@app.get("/comptes/{login}", response_model=dict)
async def read_compte(login: str, db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "SELECT login, password, statut FROM comptes WHERE login = %s"
        cursor.execute(query, (login,))
        compte = cursor.fetchone()
        if compte:
            return {"status": "success", "compte": compte}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable")
    finally:
        cursor.close()

@app.get("/fournisseurs")
async def get_fournisseurs(db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = "SELECT NomFournisseur FROM Fournisseur ORDER BY NomFournisseur ASC"
        cursor.execute(query)
        fournisseurs = cursor.fetchall()
        return {"status": "success", "fournisseurs": fournisseurs}
    finally:
        cursor.close()
        
@app.get("/materiels")
async def get_materiels(db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
        SELECT m.NoMateriel AS "Id", Type_mat AS "Type de matériel", Marque, Description, 
               p.prix AS "Prix", Image, nomfournisseur AS "Vendu par" 
        FROM Materiel AS m 
        INNER JOIN Propose as P ON p.nomateriel = m.nomateriel 
        INNER JOIN Fournisseur AS f ON f.nofournisseur = p.nofournisseur 
        ORDER BY m.NoMateriel ASC;
        """
        cursor.execute(query)
        materiels = cursor.fetchall()
        return {"status": "success", "materiels": materiels}
    finally:
        cursor.close()
        
@app.get("/fournisseurs/{nom_fournisseur}")
async def get_id_fournisseur(nom_fournisseur: str, db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT NoFournisseur FROM Fournisseur WHERE NomFournisseur = %s", (nom_fournisseur,))
        fournisseur = cursor.fetchone()
        if fournisseur:
            return {"status": "success", "id": fournisseur["NoFournisseur"]}
        else:
            raise HTTPException(status_code=404, detail="Fournisseur introuvable")
    finally:
        cursor.close()
        
@app.get("/materiels/{description}")
async def get_id_materiel(description: str, db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT NoMateriel FROM Materiel WHERE Description = %s", (description,))
        materiel = cursor.fetchone()
        if materiel:
            return {"status": "success", "id": materiel["NoMateriel"]}
        else:
            raise HTTPException(status_code=404, detail="Matériel introuvable")
    finally:
        cursor.close()

@app.get("/materiels/ids")
async def get_liste_id_materiel(db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("SELECT NoMateriel FROM Materiel")
        materiels = cursor.fetchall()
        return {"status": "success", "ids": materiels}
    finally:
        cursor.close()
        

@app.get("/materiels/type/{type_mat}")
async def get_produits_par_type(type_mat: str, db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        cursor.execute("""
        SELECT m.NoMateriel AS "Id", Type_mat AS "Type de matériel", Marque, Description, p.prix AS "Prix", Image, nomfournisseur AS "Vendu par"
        FROM Materiel AS m
        INNER JOIN Propose as P ON p.nomateriel = m.nomateriel
        INNER JOIN Fournisseur AS f ON f.nofournisseur = p.nofournisseur
        WHERE type_mat = %s;
        """, (type_mat,))
        produits = cursor.fetchall()
        return {"status": "success", "produits": produits}
    finally:
        cursor.close()
        
# Route pour vérifier l'existence d'un compte avec des données JSON
@app.post("/check_account")
async def check_account(data: dict, db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Nom d'utilisateur et mot de passe requis")

    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "SELECT login, password, statut FROM comptes WHERE login = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()

        if user:
            return {"status": "success", "message": "Compte existant", "user": user}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable")
    finally:
        cursor.close()

# Route pour insérer un nouveau matériel
@app.post("/materiels")
async def ajouter_materiel(materiel: Materiel, db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor()
    try:
        # Insérer le matériel
        cursor.execute("INSERT INTO Materiel(type_mat, marque, description, image) VALUES (%s, %s, %s, %s)", 
                       (materiel.type, materiel.marque, materiel.description, materiel.nom_image))
        # Récupérer les identifiants
        idFournisseur = getIdFournisseur(materiel.fournisseur, cursor)
        idMateriel = getIdMateriel(materiel.description, cursor)
        # Insérer dans la table Propose
        cursor.execute("INSERT INTO Propose VALUES (%s, %s, %s)", (idMateriel, idFournisseur, materiel.prix))
        db_conn.commit()
        return {"status": "success", "message": "Matériel ajouté avec succès"}
    except mysql.connector.Error as e:
        db_conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur lors de l'insertion du matériel : {e}")
    finally:
        cursor.close()

# Opération CRUD : Créer un compte
@app.post("/comptes/", response_model=dict)
async def create_compte(compte: CompteCreate, db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "INSERT INTO comptes (login, password, statut) VALUES (%s, %s, %s)"
        cursor.execute(query, (compte.login, compte.password, compte.statut))
        db_conn.commit()
        return {"status": "success", "message": "Compte créé avec succès", "compte": compte.dict()}
    except mysql.connector.Error as e:
        return {"status": "error", "message": f"Erreur lors de la création du compte : {e}"}
    finally:
        cursor.close()

# Opération CRUD : Mettre à jour un compte par login
@app.put("/comptes/{login}", response_model=dict)
async def update_compte(login: str, compte_update: CompteUpdate, db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "UPDATE comptes SET password = %s, statut = %s WHERE login = %s"
        cursor.execute(query, (compte_update.password, compte_update.statut, login))
        db_conn.commit()
        return {"status": "success", "message": "Compte mis à jour avec succès"}
    except mysql.connector.Error as e:
        return {"status": "error", "message": f"Erreur lors de la mise à jour du compte : {e}"}
    finally:
        cursor.close()

@app.put("/materiels/{id_materiel}")
async def update_materiel(id_materiel: int, materiel: MaterielUpdate, db_conn=Depends(get_db_conn_psql)):
    cursor = db_conn.cursor()
    try:
        # Mise à jour de la table Materiel
        cursor.execute("""
        UPDATE Materiel 
        SET type_mat = %s, marque = %s, description = %s 
        WHERE NoMateriel = %s
        """, (materiel.type, materiel.marque, materiel.description, id_materiel))
        
        # Mise à jour de la table Propose
        id_fournisseur = getIdFournisseur(materiel.fournisseur, cursor)
        cursor.execute("""
        UPDATE Propose 
        SET NoFournisseur = %s, Prix = %s
        WHERE NoMateriel = %s
        """, (id_fournisseur, materiel.prix, id_materiel))

        db_conn.commit()
        return {"status": "success", "message": "Matériel mis à jour avec succès"}
    except mysql.connector.Error as e:
        db_conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur lors de la mise à jour du matériel : {e}")
    finally:
        cursor.close()

# Opération CRUD : Supprimer un compte par login
@app.delete("/comptes/{login}", response_model=dict)
async def delete_compte(login: str, db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "DELETE FROM comptes WHERE login = %s"
        cursor.execute(query, (login,))
        db_conn.commit()
        return {"status": "success", "message": "Compte supprimé avec succès"}
    except mysql.connector.Error as e:
        return {"status": "error", "message": f"Erreur lors de la suppression du compte : {e}"}
    finally:
        cursor.close()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
