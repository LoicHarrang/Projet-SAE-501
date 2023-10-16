from fastapi import FastAPI, Depends
import asyncpg
from asyncpg import Connection
import mysql.connector
from mysql.connector import connection

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
        

# def get_db_conn_mariadb():
#     conn = mysql.connector.connect(
#         user="loic",
#         password="123456789",
#         database="site",
#         host="mariadb",
#     )
#     try:
#         yield conn
#     finally:
#         conn.close()

# Route pour la connexion à la base de données
@app.get("/connexion_psql")
async def connexion_bd(conn: Connection = Depends(get_db_conn_psql)):
    return {"message": "Connexion à la base de données établie avec succès"}

# @app.get("/connexion_mariadb")
# async def connexion_bd(conn: connection.MySQLConnection = Depends(get_db_conn_mariadb)):
#     return {"message": "Connexion à la base de données établie avec succès"}


