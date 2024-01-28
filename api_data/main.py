
from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer
import mysql.connector
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor


app = FastAPI()

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
        cursor.execute("SELECT nofournisseur FROM Fournisseur WHERE nomfournisseur = %s", (fournisseur_nom,))
        result = cursor.fetchone()
        return result['nofournisseur'] if result else None
    
def getIdMateriel(description: str, db_conn):
    with db_conn.cursor(cursor_factory=RealDictCursor) as cursor:  # db_conn doit être une connexion à la base de données
        cursor.execute("SELECT nomateriel FROM Materiel WHERE description = %s", (description,))
        result = cursor.fetchone()
        return result['nomateriel'] if result else None
    

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
        
@app.get("/materiels/query")
async def query_materiels(description: Optional[str] = Query(None), db_conn=Depends(get_db_conn_psql)):
    # Vérifier si une description a été fournie
    if description is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La description est requise pour cette requête.")

    cursor = db_conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = "SELECT NoMateriel FROM Materiel WHERE Description = %s"
        cursor.execute(query, (description,))  # Notez l'utilisation d'une virgule pour créer un tuple avec un seul élément
        materiels = cursor.fetchall()

        if not materiels:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Aucun matériel trouvé avec cette description.")

        return {"status": "success", "materiels": materiels}
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
        
# Route pour insérer un nouveau matériel
@app.post("/materiels")
async def ajouter_materiel(materiel: Materiel, db_conn=Depends(get_db_conn_psql)):
    try:
        with db_conn.cursor() as cursor:
            # Insérer le matériel
            cursor.execute(
                "INSERT INTO Materiel(type_mat, marque, description, image) VALUES (%s, %s, %s, %s)",
                (materiel.type, materiel.marque, materiel.description, materiel.nom_image)
            )

            # Récupérer les identifiants
            idFournisseur = getIdFournisseur(materiel.fournisseur, db_conn)
            # Veuillez vous assurer que la fonction getIdFournisseur est définie de manière similaire à getIdMateriel
            idMateriel = getIdMateriel(materiel.description, db_conn)

            # Insérer dans la table Propose si nécessaire, ajustez en fonction de votre schéma de base de données
            cursor.execute(
                "INSERT INTO Propose(nomateriel, nofournisseur, prix) VALUES (%s, %s, %s)",
                (idMateriel, idFournisseur, materiel.prix)
            )

            db_conn.commit()

        return {"status": "success", "message": "Matériel ajouté avec succès"}
    except Exception as e:  # Il est préférable d'utiliser une exception plus spécifique si possible
        db_conn.rollback()
        return {"status": "error", "message": f"Erreur lors de l'insertion du matériel : {e}"}

@app.put("/materiels/{id_materiel}")
async def update_materiel(id_materiel: int, materiel: MaterielUpdate, db_conn=Depends(get_db_conn_psql)):
    try:
        # Mise à jour de la table Materiel
        with db_conn.cursor() as cursor:
            cursor.execute("""
            UPDATE Materiel 
            SET type_mat = %s, marque = %s, description = %s 
            WHERE NoMateriel = %s
            """, (materiel.type, materiel.marque, materiel.description, id_materiel))
        
        # Mise à jour de la table Propose
        id_fournisseur = getIdFournisseur(materiel.fournisseur, db_conn)  # Passez db_conn ici
        with db_conn.cursor() as cursor:
            cursor.execute("""
            UPDATE Propose 
            SET NoFournisseur = %s, Prix = %s
            WHERE NoMateriel = %s
            """, (id_fournisseur, materiel.prix, id_materiel))

        db_conn.commit()
        return {"status": "success", "message": "Matériel mis à jour avec succès"}
    except psycopg2.Error as e:  # Utilisez psycopg2.Error ici au lieu de mysql.connector.Error
        db_conn.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erreur lors de la mise à jour du matériel : {e}")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8081)