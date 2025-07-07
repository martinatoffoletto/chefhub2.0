import asyncodbc
from typing import Any, Tuple, Optional, List, Dict, Union

# DSN de conexión
DSN = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=chefhub;"
    "Trusted_Connection=yes;"
)

# Pool de conexiones
pool = None

# Función para iniciar la app
async def startup():
    global pool
    print("Iniciando la conexión a la base de datos...")
    pool = await asyncodbc.create_pool(dsn=DSN)
    print("✅ Pool creado.")

async def shutdown():
    global pool
    try:
        print("Cerrando la conexión a la base de datos...")
        if pool:
            pool.close()
            await pool.wait_closed()
            print("✅ Conexión cerrada.")
    except Exception as e:
        print("❌ Error al cerrar la conexión:", e)
        
async def ejecutar_consulta_async(
    query: str,
    params: Optional[Tuple[Any, ...]] = None,
    fetch: bool = False,
    external_conn: Optional[asyncodbc.Connection] = None
) -> Union[List[Dict[str, Any]], None]:
    usar_conn_externa = external_conn is not None
    conn = external_conn or await pool.acquire()
    cursor = None

    try:
        cursor = await conn.cursor()
        await cursor.execute(query, params or ())

        if fetch:
            columns = [col[0] for col in cursor.description]
            rows = await cursor.fetchall()
            return [dict(zip(columns, row)) for row in rows]
        else:
            return None

    except Exception as e:
        try:
            await conn.rollback()
        except Exception as rollback_err:
            print(f"⚠️ Error al hacer rollback: {rollback_err}")
        raise e

    finally:
        try:
            if cursor:
                await cursor.close()
        except Exception as cursor_err:
            print(f"⚠️ Error al cerrar cursor: {cursor_err}")

        if not fetch:
            try:
                await conn.commit()
            except Exception as commit_err:
                print(f"⚠️ Error al hacer commit: {commit_err}")
                raise commit_err

        if not usar_conn_externa:
            try:
                await pool.release(conn)
            except Exception as release_err:
                print(f"⚠️ Error al liberar conexión: {release_err}")
