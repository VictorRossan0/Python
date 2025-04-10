from dotenv import load_dotenv
import os
import mysql.connector

# Carregar o .env
load_dotenv()

def get_connection():
    """
    Estabelece uma conexão com o banco de dados.
    
    Returns:
        connection (mysql.connector.connection.MySQLConnection): Objeto de conexão.
    """
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )
