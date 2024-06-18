# src/cn/data_base_connection.py
import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()  # Carga las variables de entorno desde .env

def get_db_connection():
    """Establece una conexión a la base de datos PostgreSQL.

    Returns:
        psycopg2.connection: La conexión a la base de datos.
    """
    try:
        conn = psycopg2.connect(
            host=os.getenv("DATABASE_HOSTNAME"),
            port=os.getenv("DATABASE_PORT"),
            database=os.getenv("DATABASE_NAME"),
            user=os.getenv("DATABASE_USER"),
            password=os.getenv("DATABASE_PASSWORD")
        )
        return conn
    except (Exception, psycopg2.Error) as error:
        print("Error al conectar a la base de datos:", error)
        return None