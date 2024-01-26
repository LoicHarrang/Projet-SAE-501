from datetime import datetime, timedelta
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, status
import mysql.connector
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from jose import JWTError, jwt
from fastapi import Header

SECRET_KEY = "sae501"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Header(None, alias="token"), db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Impossible de valider les informations d'identification",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token is None:
        raise credentials_exception
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        cursor = db_conn.cursor(dictionary=True)
        cursor.execute("SELECT login, statut FROM comptes WHERE login = %s", (username,))
        user = cursor.fetchone()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception

# Modèle Pydantic pour la création et la mise à jour d'un compte
class CompteCreate(BaseModel):
    login: str
    password: str
    statut: str

class CompteUpdate(BaseModel):
    password: str
    statut: str
        
# Opération CRUD : Lire un compte par login
@app.get("/comptes/{login}", response_model=dict)
async def read_compte(login: str, current_user: dict = Depends(get_current_user), db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "SELECT login, statut FROM comptes WHERE login = %s"
        cursor.execute(query, (login,))
        compte = cursor.fetchone()
        if compte:
            return {"status": "success", "compte": compte}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable")
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
            access_token = create_access_token(data={"sub": username})
            return {"status": "success", "message": "Compte existant", "user": user, "access_token": access_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compte introuvable")
    finally:
        cursor.close()

# Opération CRUD : Créer un compte
@app.post("/comptes/", response_model=dict)
async def create_compte(compte: CompteCreate, current_user: dict = Depends(get_current_user), db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    # Vérifier si l'utilisateur actuel a les autorisations nécessaires pour créer un compte
    # Par exemple, vérifier si le statut de l'utilisateur est 'admin'
    if current_user["statut"] != "administrateur":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Opération non autorisée")

    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "INSERT INTO comptes (login, password, statut) VALUES (%s, %s, %s)"
        cursor.execute(query, (compte.login, compte.password, compte.statut))
        db_conn.commit()
        return {"status": "success", "message": "Compte créé avec succès", "compte": compte.dict()}
    except mysql.connector.Error as e:
        db_conn.rollback()  # Assurez-vous d'annuler la transaction en cas d'erreur
        return {"status": "error", "message": f"Erreur lors de la création du compte : {e}"}
    finally:
        cursor.close()


# Opération CRUD : Mettre à jour un compte par login
@app.put("/comptes/{login}", response_model=dict)
async def update_compte(login: str, compte_update: CompteUpdate, current_user: dict = Depends(get_current_user), db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    # Vérifier si l'utilisateur actuel a les autorisations nécessaires pour mettre à jour le compte
    # L'utilisateur peut mettre à jour son propre compte ou doit être un admin pour mettre à jour les comptes d'autres utilisateurs
    if current_user["statut"] != "administrateur":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Opération non autorisée")

    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "UPDATE comptes SET password = %s, statut = %s WHERE login = %s"
        cursor.execute(query, (compte_update.password, compte_update.statut, login))
        db_conn.commit()
        return {"status": "success", "message": "Compte mis à jour avec succès"}
    except mysql.connector.Error as e:
        db_conn.rollback()  # Assurez-vous d'annuler la transaction en cas d'erreur
        return {"status": "error", "message": f"Erreur lors de la mise à jour du compte : {e}"}
    finally:
        cursor.close()


# Opération CRUD : Supprimer un compte par login
@app.delete("/comptes/{login}", response_model=dict)
async def delete_compte(login: str, current_user: dict = Depends(get_current_user), db_conn: mysql.connector.connection.MySQLConnection = Depends(get_db_conn_mysql)):
    # Vérifier si l'utilisateur actuel a les autorisations nécessaires pour supprimer le compte
    # L'utilisateur peut supprimer son propre compte ou doit être un admin pour supprimer les comptes d'autres utilisateurs
    if current_user["statut"] != "administrateur":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Opération non autorisée")

    cursor = db_conn.cursor(dictionary=True)
    try:
        query = "DELETE FROM comptes WHERE login = %s"
        cursor.execute(query, (login,))
        db_conn.commit()
        return {"status": "success", "message": "Compte supprimé avec succès"}
    except mysql.connector.Error as e:
        db_conn.rollback()  # Assurez-vous d'annuler la transaction en cas d'erreur
        return {"status": "error", "message": f"Erreur lors de la suppression du compte : {e}"}
    finally:
        cursor.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
