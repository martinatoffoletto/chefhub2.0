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

# Función para cerrar la app
async def shutdown():
    global pool
    try:
        print("Cerrando la conexión a la base de datos...")
        pool.close()
        await pool.wait_closed()
        print("Conexión cerrada.")
    except Exception as e:
        print("Error al cerrar la conexión:", e)


# Función asíncrona para ejecutar consultas
async def ejecutar_consulta_async(
    query: str,
    params: Optional[Tuple[Any, ...]] = None,
    fetch: bool = False
) -> Union[List[Dict[str, Any]], None]:
    try:
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                print("📤 Ejecutando query")
                if params:
                    await cursor.execute(query, params)
                else:
                    await cursor.execute(query)

                if fetch:
                    columns = [column[0] for column in cursor.description]
                    rows = await cursor.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    await conn.commit()
                    print("✅ Commit exitoso.")
                    return None

    except Exception as e:
        try:
            await conn.rollback()
            print("♻️ Rollback ejecutado debido a error.")
        except Exception:
            pass

        print(f"❌ Error ejecutando consulta:\n{query}\nCon parámetros: {params}\nError: {e}")
        raise
