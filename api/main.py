from fastapi import FastAPI, HTTPException, Depends, status
import asyncpg
from asyncpg import Connection
import mysql.connector
from mysql.connector import connection
from pydantic import BaseModel

app = FastAPI()

# Configuration de la connexion à la base de données PostgreSQL
async def get_db_conn_psql():
    conn = await asyncpg.connect(
        user="loic",
        password="123456789",
        database="site",
        host="psql",
    )
    try:
        yield conn
    finally:
        await conn.close()
        


# EXTRAIT DE CHAT GPT A MODIFIER (JUSQU'A LA FIN DU FICHIER)
# EXTRAIT DE CHAT GPT A MODIFIER (JUSQU'A LA FIN DU FICHIER)
# EXTRAIT DE CHAT GPT A MODIFIER (JUSQU'A LA FIN DU FICHIER)
# EXTRAIT DE CHAT GPT A MODIFIER (JUSQU'A LA FIN DU FICHIER)
# EXTRAIT DE CHAT GPT A MODIFIER (JUSQU'A LA FIN DU FICHIER)
# EXTRAIT DE CHAT GPT A MODIFIER (JUSQU'A LA FIN DU FICHIER)


# Route pour la connexion à la base de données
@app.get("/connexion_psql")
async def connexion_bd(conn: Connection = Depends(get_db_conn_psql)):
    return {"message": "Connexion à la base de données établie avec succès"}

# Modèle Pydantic pour les produits
class Product(BaseModel):
    nom: str
    description: str
    prix: float

# Créer un produit
@app.post("/produits/", response_model=Product)
async def create_product(product: Product, conn: Connection = Depends(get_db_conn_psql)):
    query = "INSERT INTO produits (nom, description, prix) VALUES($1, $2, $3) RETURNING id, nom, description, prix"
    result = await conn.fetchrow(query, product.nom, product.description, product.prix)
    return result

# Obtenir un produit par ID
@app.get("/produits/{product_id}", response_model=Product)
async def read_product(product_id: int, conn: Connection = Depends(get_db_conn_psql)):
    query = "SELECT id, nom, description, prix FROM produits WHERE id = $1"
    product = await conn.fetchrow(query, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return product

# Mettre à jour un produit
@app.put("/produits/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product, conn: Connection = Depends(get_db_conn_psql)):
    query = "UPDATE produits SET nom=$1, description=$2, prix=$3 WHERE id = $4 RETURNING id, nom, description, prix"
    result = await conn.fetchrow(query, product.nom, product.description, product.prix, product_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return result

# Supprimer un produit
@app.delete("/produits/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int, conn: Connection = Depends(get_db_conn_psql)):
    query = "DELETE FROM produits WHERE id = $1"
    result = await conn.execute(query, product_id)
    if result == "DELETE 0":
        raise HTTPException(status_code=404, detail="Produit non trouvé")


