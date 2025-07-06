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
    conn = external_conn or await pool.acquire()
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(query, params or ())
            if fetch:
                columns = [col[0] for col in cursor.description]
                rows = await cursor.fetchall()
                resultado = [dict(zip(columns, row)) for row in rows]
                return resultado
            if not external_conn:
                await conn.commit()
            return None
    except Exception as e:
        if not external_conn:
            try:
                await conn.rollback()
            except Exception:
                pass
        raise
    finally:
        if not external_conn:
            try:
                await pool.release(conn)
            except Exception:
                pass
