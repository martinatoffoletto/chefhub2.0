from app.services.user_services import obtener_nickname_por_id
from app.models.receta import *
from app.models.usuario import *
from app.models.calificacion import *
import app.config.db as db
from pathlib import Path
from fastapi import UploadFile
from uuid import uuid4
import re
import aiofiles
############ LOGICA DE NEGOCIO RECETAS ############

# Ver todas las recetas por orden alfabético  
async def listar_recetas(
    ordenar_por: str = "nombre",
    nickname: str = None,
    id_ingrediente_incluye: int = None,
    id_ingrediente_excluye: int = None,
    id_tipo: int = None,
    id_usuario_logueado: int = None,
    nombre_receta: str = None,
    limite: int = None
) -> List[Dict]:
    query = """
        SELECT 
            r.idReceta,
            r.nombreReceta,
            r.descripcionReceta,
            r.fotoPrincipal,
            u.nickname,
            u.avatar,
            ISNULL(AVG(c.calificacion), 0) AS promedioCalificacion,
            er.estado
        FROM recetas r
        JOIN usuarios u ON r.idUsuario = u.idUsuario
        LEFT JOIN calificaciones c ON r.idReceta = c.idReceta
        JOIN estadoReceta er ON er.idReceta = r.idReceta
    """

    filtros = []
    params = []

    if id_ingrediente_incluye:
        query += " JOIN utilizados ui ON ui.idReceta = r.idReceta"
        filtros.append("ui.idIngrediente = ?")
        params.append(id_ingrediente_incluye)

    if id_ingrediente_excluye:
        filtros.append("""
            r.idReceta NOT IN (
                SELECT idReceta FROM utilizados WHERE idIngrediente = ?
            )
        """)
        params.append(id_ingrediente_excluye)

    if id_tipo:
        filtros.append("r.idTipo = ?")
        params.append(id_tipo)

    if nickname:
        filtros.append("LOWER(u.nickname) LIKE LOWER(?)")
        params.append(f"%{nickname}%")

    if nombre_receta:
        filtros.append("LOWER(r.nombreReceta) LIKE LOWER(?)")
        params.append(f"%{nombre_receta}%")

    if id_usuario_logueado:
        usuario_logueado_nickname = await obtener_nickname_por_id(id_usuario_logueado)
        if nickname and nickname != usuario_logueado_nickname:
            filtros.append("er.estado = 'aprobado'")
        else:
            filtros.append("""
                (
                    er.estado = 'aprobado'
                    OR r.idUsuario = ?
                )
            """)
            params.append(id_usuario_logueado)
    else:
        filtros.append("er.estado = 'aprobado'")

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    query += """
        GROUP BY r.idReceta, r.nombreReceta, r.descripcionReceta, r.fotoPrincipal, u.nickname, u.avatar, er.estado
    """

    if ordenar_por == "reciente":
        query += " ORDER BY r.idReceta DESC"
    elif ordenar_por == "usuario":
        query += " ORDER BY u.nickname ASC"
    else:
        query += " ORDER BY r.nombreReceta ASC"

    recetas = await db.ejecutar_consulta_async(query, params, fetch=True)

    if limite:
        recetas = recetas[:limite]
    return recetas if recetas else []


#listar todos los ingredientes
async def listar_ingredientes() -> List[Dict]:
    query = "SELECT idIngrediente, nombre FROM Ingredientes"
    ingredientes = await db.ejecutar_consulta_async(query, fetch=True)
    return ingredientes if ingredientes else []

#listar todos los tipos de receta
async def listar_tipos_receta() -> List[Dict]:
    """
    Devuelve todos los tipos de receta (id y descripcion)
    """
    query = "SELECT idTipo, descripcion FROM TiposReceta"
    tipos = await db.ejecutar_consulta_async(query, fetch=True)
    return tipos if tipos else []

#listar todas las unidades
async def listar_unidades() -> List[Dict]:
    """
    Devuelve todas las unidades (id y descripcion)
    """
    query = "SELECT idUnidad, descripcion FROM unidades"
    unidades = await db.ejecutar_consulta_async(query, fetch=True)
    return unidades if unidades else []

#listar conversiones
async def listar_conversiones() -> List[Dict]:
    """
    Devuelve todas las conversiones entre unidades (idUnidadOrigen, idUnidadDestino, factorConversiones)
    """
    query = """
        SELECT 
            idConversion,
            idUnidadOrigen,
            idUnidadDestino,
            factorConversiones
        FROM conversiones
    """
    conversiones = await db.ejecutar_consulta_async(query, fetch=True)
    return conversiones if conversiones else []

#obtener receta por id 
import asyncio
from typing import Optional, Dict

async def obtener_receta_detallada(id_receta: int) -> Optional[Dict]:
    async with db.pool.acquire() as conn:
        receta_query = """
            SELECT 
                r.idReceta,
                r.nombreReceta,
                r.descripcionReceta,
                r.fotoPrincipal,
                r.porciones,
                r.cantidadPersonas,
                u.nickname,
                tr.descripcion AS tipoReceta
            FROM recetas r
            JOIN usuarios u ON r.idUsuario = u.idUsuario
            LEFT JOIN tiposReceta tr ON r.idTipo = tr.idTipo
            WHERE r.idReceta = ?
        """
        receta = await db.ejecutar_consulta_async(receta_query, [id_receta], fetch=True, external_conn=conn)
        if not receta:
            return None
        receta = receta[0]

        ingredientes_query = """
            SELECT 
                i.nombre AS ingrediente,
                un.descripcion AS unidad,
                u.cantidad,
                u.observaciones
            FROM utilizados u
            JOIN ingredientes i ON u.idIngrediente = i.idIngrediente
            JOIN unidades un ON u.idUnidad = un.idUnidad
            WHERE u.idReceta = ?
        """
        ingredientes = await db.ejecutar_consulta_async(ingredientes_query, [id_receta], fetch=True, external_conn=conn)

        pasos_query = """
            SELECT 
                idPaso,
                nroPaso,
                texto AS descripcionPaso
            FROM pasos
            WHERE idReceta = ?
            ORDER BY nroPaso ASC
        """
        pasos = await db.ejecutar_consulta_async(pasos_query, [id_receta], fetch=True, external_conn=conn)

    # Cerramos conexión antes de consultas conflictivas

    # Esperamos un toque para liberar locks y evitar deadlock (opcional)
    await asyncio.sleep(0.1)

    # Consultas de multimedia y calificaciones sin external_conn para no mantener locks
    media_query = """
        SELECT 
            m.idPaso,
            m.urlContenido AS url,
            m.tipo_contenido AS tipo
        FROM multimedia m
        JOIN pasos p ON m.idPaso = p.idPaso
        WHERE p.idReceta = ?
    """
    media_por_paso = await db.ejecutar_consulta_async(media_query, [id_receta], fetch=True)

    calificacion_query = """
        SELECT 
            ISNULL(AVG(calificacion), 0) AS promedio,
            COUNT(*) AS cantidad
        FROM calificaciones
        WHERE idReceta = ?
    """
    calificaciones = await db.ejecutar_consulta_async(calificacion_query, [id_receta], fetch=True)
    calificaciones = calificaciones[0] if calificaciones else {"promedio": 0, "cantidad": 0}

    for paso in pasos:
        paso["multimedia"] = [m for m in media_por_paso if m["idPaso"] == paso["idPaso"]]

    receta_detallada = {
        **receta,
        "ingredientes": ingredientes,
        "pasos": pasos,
        "calificaciones": calificaciones
    }

    return receta_detallada


# Buscar idReceta por usuario y nombre 
async def buscar_receta_por_usuario_y_nombre(id_usuario: int, nombre: str) -> Optional[int]:
    """
    Busca el idReceta de una receta exacta por usuario y nombre (case insensitive).
    Retorna el idReceta o None si no existe.
    """
    try:
        query = """
            SELECT idReceta
            FROM recetas
            WHERE idUsuario = ?
              AND LOWER(nombreReceta) = LOWER(?)
        """
        resultados = await db.ejecutar_consulta_async(query, (id_usuario, nombre), fetch=True)
        if resultados:
            return resultados[0]['idReceta']  
        return None
    except Exception as e:
        print(f"Error en buscar_receta_por_usuario_y_nombre: {e}")
        return None

# Verificar si la receta ya existe para el usuario
async def verificar_receta(id_usuario: int, nombre: str):
    receta_id = await buscar_receta_por_usuario_y_nombre(id_usuario, nombre)
    print(f"Verificando receta '{nombre}' para usuario {id_usuario}: {receta_id}")
    if receta_id:
        print(f"Receta ya existe con ID: {receta_id}")
        return {
            "existe": True,
            "mensaje": "Receta ya existe",
            "receta_id": str(receta_id),
        }
    return {
        "existe": False,
        "mensaje": "Receta nueva. Podés comenzar a cargarla.",
        "nombre": nombre,
    }


# Crear receta
async def crear_receta_completa(data: RecetaIn, id_usuario: int) -> int:
    async with db.pool.acquire() as conn:
        # Buscar o crear tipo
        query_tipo = "SELECT idTipo FROM tiposReceta WHERE descripcion = ?"
        resultado_tipo = await db.ejecutar_consulta_async(query_tipo, (data.tipo,), fetch=True, external_conn=conn)
        if resultado_tipo:
            id_tipo = resultado_tipo[0]["idTipo"]
        else:
            insert_tipo = """
                INSERT INTO tiposReceta (descripcion)
                OUTPUT INSERTED.idTipo
                VALUES (?)
            """
            res_tipo = await db.ejecutar_consulta_async(insert_tipo, (data.tipo,), fetch=True, external_conn=conn)
            id_tipo = res_tipo[0]["idTipo"]

        query_receta = """
            INSERT INTO recetas (idUsuario, nombreReceta, descripcionReceta, porciones, cantidadPersonas, idTipo)
            OUTPUT INSERTED.idReceta
            VALUES (?, ?, ?, ?, ?, ?)
        """
        receta_params = (
            id_usuario,
            data.nombreReceta,
            data.descripcionReceta,
            data.porciones,
            data.cantidadPersonas,
            id_tipo
        )
        resultado = await db.ejecutar_consulta_async(query_receta, receta_params, fetch=True, external_conn=conn)
        if not resultado:
            raise Exception("No se pudo insertar la receta")
        id_receta = resultado[0]["idReceta"]

        # Insertar ingredientes (buscar o crear)
        for ing in data.ingredientes:
            query_ing = "SELECT idIngrediente FROM ingredientes WHERE nombre = ?"
            res_ing = await db.ejecutar_consulta_async(query_ing, (ing.nombre,), fetch=True, external_conn=conn)
            if res_ing:
                id_ingrediente = res_ing[0]["idIngrediente"]
            else:
                insert_ing = """
                    INSERT INTO ingredientes (nombre)
                    OUTPUT INSERTED.idIngrediente
                    VALUES (?)
                """
                nuevo_ing = await db.ejecutar_consulta_async(insert_ing, (ing.nombre,), fetch=True, external_conn=conn)
                id_ingrediente = nuevo_ing[0]["idIngrediente"]

            await db.ejecutar_consulta_async(
                """
                INSERT INTO utilizados (idReceta, idIngrediente, cantidad, idUnidad, observaciones)
                VALUES (?, ?, ?, ?, ?)
                """,
                (id_receta, id_ingrediente, ing.cantidad, ing.idUnidad, ing.observaciones),
                external_conn=conn
            )

        # Insertar pasos (sin multimedia)
        for paso in data.pasos:
            await db.ejecutar_consulta_async(
                """
                INSERT INTO pasos (idReceta, nroPaso, texto)
                VALUES (?, ?, ?)
                """,
                (id_receta, paso.nroPaso, paso.texto),
                external_conn=conn
            )

        # Insertar estado inicial
        await db.ejecutar_consulta_async(
            """
            INSERT INTO estadoReceta (idReceta, fecha_creacion, estado)
            VALUES (?, GETDATE(), 'pendiente')
            """,
            (id_receta,),
            external_conn=conn
        )

        return id_receta

# Reemplazar receta (borra la receta antigua despues de q crea una nueva)
async def borrar_receta_completa(id_receta: int):
    try:
        async with db.pool.acquire() as conn:
            await db.ejecutar_consulta_async("""
                DELETE m
                FROM multimedia m
                JOIN pasos p ON m.idPaso = p.idPaso
                WHERE p.idReceta = ?
            """, (id_receta,), external_conn=conn)

            await db.ejecutar_consulta_async("DELETE FROM pasos WHERE idReceta = ?", (id_receta,), external_conn=conn)
            await db.ejecutar_consulta_async("DELETE FROM fotos WHERE idReceta = ?", (id_receta,), external_conn=conn)
            await db.ejecutar_consulta_async("DELETE FROM utilizados WHERE idReceta = ?", (id_receta,), external_conn=conn)

            await db.ejecutar_consulta_async("""
                DELETE ec
                FROM estadoComentario ec
                JOIN calificaciones c ON ec.idCalificacion = c.idCalificacion
                WHERE c.idReceta = ?
            """, (id_receta,), external_conn=conn)

            await db.ejecutar_consulta_async("DELETE FROM calificaciones WHERE idReceta = ?", (id_receta,), external_conn=conn)
            await db.ejecutar_consulta_async("DELETE FROM estadoReceta WHERE idReceta = ?", (id_receta,), external_conn=conn)
            await db.ejecutar_consulta_async("DELETE FROM recetasFavoritas WHERE idReceta = ?", (id_receta,), external_conn=conn)
            await db.ejecutar_consulta_async("DELETE FROM recetas WHERE idReceta = ?", (id_receta,), external_conn=conn)

        print(f"✅ Receta {id_receta} y todas sus relaciones fueron eliminadas.")
        return True
    except Exception as e:
        print(f"❌ Error al eliminar la receta {id_receta}: {e}")
        return False

# Actualizar receta
async def actualizar_receta_completa(id_receta: int, data: RecetaIn, id_usuario: int) -> bool:
    try:
        async with db.pool.acquire() as conn:
            # Obtener o insertar tipo
            query_tipo = "SELECT idTipo FROM tiposReceta WHERE descripcion = ?"
            resultado_tipo = await db.ejecutar_consulta_async(query_tipo, (data.tipo,), fetch=True, external_conn=conn)

            if resultado_tipo:
                id_tipo = resultado_tipo[0]["idTipo"]
            else:
                insert_tipo = """
                    INSERT INTO tiposReceta (descripcion)
                    OUTPUT INSERTED.idTipo
                    VALUES (?)
                """
                res_tipo = await db.ejecutar_consulta_async(insert_tipo, (data.tipo,), fetch=True, external_conn=conn)
                id_tipo = res_tipo[0]["idTipo"]

            # Actualizar receta principal
            query_update = """
                UPDATE recetas
                SET nombreReceta = ?, descripcionReceta = ?, porciones = ?, cantidadPersonas = ?, idTipo = ?
                WHERE idReceta = ? AND idUsuario = ?
            """
            await db.ejecutar_consulta_async(query_update, (
                data.nombreReceta,
                data.descripcionReceta,
                data.porciones,
                data.cantidadPersonas,
                id_tipo,
                id_receta,
                id_usuario
            ), external_conn=conn)

            # Ingredientes
            await db.ejecutar_consulta_async("DELETE FROM utilizados WHERE idReceta = ?", (id_receta,), external_conn=conn)

            for ing in data.ingredientes:
                query_ing = "SELECT idIngrediente FROM ingredientes WHERE nombre = ?"
                res_ing = await db.ejecutar_consulta_async(query_ing, (ing.nombre,), fetch=True, external_conn=conn)
                if res_ing:
                    id_ingrediente = res_ing[0]["idIngrediente"]
                else:
                    insert_ing = """
                        INSERT INTO ingredientes (nombre)
                        OUTPUT INSERTED.idIngrediente
                        VALUES (?)
                    """
                    nuevo_ing = await db.ejecutar_consulta_async(insert_ing, (ing.nombre,), fetch=True, external_conn=conn)
                    id_ingrediente = nuevo_ing[0]["idIngrediente"]

                await db.ejecutar_consulta_async("""
                    INSERT INTO utilizados (idReceta, idIngrediente, cantidad, idUnidad, observaciones)
                    VALUES (?, ?, ?, ?, ?)
                """, (id_receta, id_ingrediente, ing.cantidad, ing.idUnidad, ing.observaciones), external_conn=conn)

            # Obtener pasos existentes
            pasos_existentes = await db.ejecutar_consulta_async(
                "SELECT idPaso, nroPaso FROM pasos WHERE idReceta = ?",
                (id_receta,),
                fetch=True,
                external_conn=conn
            )
            pasos_db = {p["nroPaso"]: p["idPaso"] for p in pasos_existentes}
            nros_nuevos = set(p.nroPaso for p in data.pasos)
            nros_existentes = set(pasos_db.keys())

            # Eliminar pasos que ya no están
            for nroPaso in nros_existentes - nros_nuevos:
                idPaso = pasos_db[nroPaso]
                await db.ejecutar_consulta_async("DELETE FROM multimedia WHERE idPaso = ?", (idPaso,), external_conn=conn)
                await db.ejecutar_consulta_async("DELETE FROM pasos WHERE idPaso = ?", (idPaso,), external_conn=conn)

            # Insertar o actualizar pasos
            for paso in data.pasos:
                if paso.nroPaso in pasos_db:
                    # Actualizar paso existente
                    idPaso = pasos_db[paso.nroPaso]
                    await db.ejecutar_consulta_async(
                        "UPDATE pasos SET texto = ? WHERE idPaso = ?",
                        (paso.texto, idPaso),
                        external_conn=conn
                    )
                else:
                    # Insertar nuevo paso
                    res = await db.ejecutar_consulta_async("""
                        INSERT INTO pasos (idReceta, nroPaso, texto)
                        OUTPUT INSERTED.idPaso
                        VALUES (?, ?, ?)
                    """, (id_receta, paso.nroPaso, paso.texto), fetch=True, external_conn=conn)
                    idPaso = res[0]["idPaso"]


            # Insertar nuevo estado
            await db.ejecutar_consulta_async("""
                INSERT INTO estadoReceta (idReceta, fecha_creacion, estado)
                VALUES (?, GETDATE(), 'pendiente')
            """, (id_receta,), external_conn=conn)

        print(f"✅ Receta actualizada con ID: {id_receta}")
        return True

    except Exception as e:
        print(f"❌ Error en actualizar_receta_completa: {e}")
        return False



# Obtener calificaciones de una receta
async def obtener_calificaciones_receta(id_receta: str) -> List[Dict]:
    query = """
        SELECT 
            c.idCalificacion,
            c.calificacion,
            c.comentarios,
            u.nickname,
            ec.estado,
            ec.fechaEstado
        FROM calificaciones c
        JOIN usuarios u ON c.idUsuario = u.idUsuario
        LEFT JOIN estadoComentario ec ON c.idCalificacion = ec.idCalificacion
        WHERE c.idReceta = ?
    """
    calificaciones = await db.ejecutar_consulta_async(query, [id_receta], fetch=True)
    return calificaciones if calificaciones else []


#crear calificación de receta
async def calificar_receta(id_receta: str, id_usuario: str, calificacion: Calificacion):
    async with db.pool.acquire() as conn:
        # Verificar si ya existe
        query_existente = "SELECT * FROM calificaciones WHERE idReceta = ? AND idUsuario = ?"
        existente = await db.ejecutar_consulta_async(query_existente, (id_receta, id_usuario), fetch=True, external_conn=conn)

        if existente:
            return {"error": "Ya has calificado esta receta.", "code": 409}

        # Insertar calificación
        query_insert = """
            INSERT INTO calificaciones (idReceta, idUsuario, calificacion, comentarios)
            OUTPUT INSERTED.idCalificacion
            VALUES (?, ?, ?, ?)
        """
        resultado = await db.ejecutar_consulta_async(
            query_insert,
            (id_receta, id_usuario, calificacion.calificacion, calificacion.comentarios),
            fetch=True,
            external_conn=conn
        )

        if not resultado or "idCalificacion" not in resultado[0]:
            print("Error: No se pudo insertar la calificación o recuperar el ID.")
            return {"error": "No se pudo insertar la calificación o recuperar el ID.", "code": 500}

        id_calificacion = resultado[0]["idCalificacion"]

        # Insertar estado del comentario
        query_estado = """
        INSERT INTO estadoComentario (idCalificacion, estado, observaciones)
        VALUES (?, ?, ?)
        """
        await db.ejecutar_consulta_async(query_estado, (id_calificacion, 'pendiente', ''), external_conn=conn)

        return {"success": True, "idCalificacion": id_calificacion}


########################## guardar archivos multimedia ##########################


RAIZ_PROYECTO = Path(__file__).parent.parent.parent.resolve()
RUTA_IMG = RAIZ_PROYECTO / "static" / "img"


async def guardar_archivo(upload_file: UploadFile) -> str:
    extension = Path(upload_file.filename).suffix
    nombre_archivo = f"{uuid4().hex}{extension}"
    ruta_completa = RUTA_IMG / nombre_archivo

    async with aiofiles.open(ruta_completa, "wb") as out_file:
        while content := await upload_file.read(1024 * 1024):  # 1 MB chunk
            await out_file.write(content)

    return f"img/{nombre_archivo}"



def extraer_indice(filename: str) -> int:
    # Buscar el patrón paso_X_ donde X es el número
    match = re.search(r"paso_(\d+)_", filename)
    if match:
        return int(match.group(1))
    else:
        # Por si no se encuentra, podés devolver -1 o lanzar error
        return -1

async def insertar_foto_principal(id_receta: int, url: str):
    query = """
        UPDATE recetas
        SET fotoPrincipal = ?
        WHERE idReceta = ?
    """
    await db.ejecutar_consulta_async(query, (url, id_receta))

async def insertar_foto_adicional(id_receta: int, url: str, extension: str):
    query = """
        INSERT INTO fotos (idReceta, urlFoto, extension)
        VALUES (?, ?, ?)
    """
    await db.ejecutar_consulta_async(query, (id_receta, url, extension))
    
async def insertar_multimedia_paso(id_receta: int, nro_paso: int, url: str, tipo_contenido: str, extension: str):
    async with db.pool.acquire() as conn:
        # Buscar idPaso
        query_buscar = """
            SELECT idPaso FROM pasos
            WHERE idReceta = ? AND nroPaso = ?
        """
        res = await db.ejecutar_consulta_async(query_buscar, (id_receta, nro_paso), fetch=True, external_conn=conn)
        if not res:
            raise Exception("Paso no encontrado")
        id_paso = res[0]["idPaso"]

        # Insertar multimedia
        query_insert = """
            INSERT INTO multimedia (idPaso, tipo_contenido, extension, urlContenido)
            VALUES (?, ?, ?, ?)
        """
        await db.ejecutar_consulta_async(query_insert, (id_paso, tipo_contenido, extension, url), external_conn=conn)
