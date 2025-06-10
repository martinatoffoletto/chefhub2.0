# En app/config/db.py

import pyodbc
from typing import Any, Tuple, Optional, List, Dict, Union

# Variables globales de configuración
SERVER = "localhost\\SQLEXPRESS"
DATABASE = "chefhub"

# Variable global para la conexión
conexion = None

def conectar_bd():
    global conexion
    try:
        conexion = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={SERVER};"
            f"DATABASE={DATABASE};"
            f"Trusted_Connection=yes;"
        )
        print("Conexión exitosa a SQL Server")
    except Exception as e:
        print(f"Error al conectar a SQL Server: {e}")
        conexion = None

def cerrar_bd():
    global conexion
    if conexion is not None:
        conexion.close()
        print("Conexión cerrada")
        conexion = None

def get_conexion():
    global conexion
    if conexion is None:
        conectar_bd()
    return conexion

def ejecutar_consulta(query: str, params: Optional[Tuple[Any, ...]] = None, fetch: bool = False) -> Union[List[Dict], None]:
    conn = get_conexion()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        if fetch:
            columns = [column[0] for column in cursor.description]
            results = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return results
        else:
            conn.commit()
            return None
    except Exception as e:
        print(f"Error ejecutando consulta: {e}")
        return None
    finally:
        cursor.close()

conectar_bd()