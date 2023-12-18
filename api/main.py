from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
import mysql.connector
from pydantic import BaseModel

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

# Modèle Pydantic pour la création et la mise à jour d'un compte
class CompteCreate(BaseModel):
    login: str
    password: str
    statut: str

class CompteUpdate(BaseModel):
    password: str
    statut: str

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
