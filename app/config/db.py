# En app/config/db.py

import mysql.connector
from mysql.connector import Error
from typing import Any, Tuple, Optional, List, Dict, Union

# Variables globales de configuración
HOST = "localhost"
USER = "root"
PASSWORD = "2003"
DATABASE = "chefhub"

# Variable global para la conexión
conexion = None

def conectar_bd():
    global conexion
    try:
        conexion = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )
        if conexion.is_connected():
            print("Conexión exitosa")
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        conexion = None

def cerrar_bd():
    global conexion
    if conexion is not None and conexion.is_connected():
        conexion.close()
        print("Conexión cerrada")
        conexion = None

def get_conexion():
    global conexion
    if conexion is None or not conexion.is_connected():
        conectar_bd()
    return conexion

def ejecutar_consulta(query: str, params: Optional[Tuple[Any, ...]] = None, fetch: bool = False) -> Union[List[Dict], None]:
    conn = get_conexion()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, params)
        if fetch:
            return cursor.fetchall()
        else:
            conn.commit()
            return None
    except Error as e:
        print(f"Error ejecutando consulta: {e}")
        return None
    finally:
        cursor.close()
