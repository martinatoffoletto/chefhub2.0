from app.services.user_services import obtener_nickname_por_id
from app.models.receta import *
from app.models.usuario import *
from app.models.appError import AppError
from datetime import datetime
from app.models.calificacion import *

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
            ISNULL(AVG(c.calificacion), 0) AS promedioCalificacion
        FROM recetas r
        JOIN usuarios u ON r.idUsuario = u.idUsuario
        LEFT JOIN calificaciones c ON r.idReceta = c.idReceta
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
        filtros.append("u.nickname = ?")
        params.append(nickname)

    if nombre_receta:
        filtros.append("LOWER(r.nombreReceta) LIKE LOWER(?)")
        params.append(f"%{nombre_receta}%")

    if id_usuario_logueado:
        usuario_logueado_nickname = await obtener_nickname_por_id(id_usuario_logueado)
        if nickname and nickname != usuario_logueado_nickname:
            filtros.append("""
                r.idReceta IN (
                    SELECT idReceta FROM estadoReceta WHERE estado = 'aprobado'
                )
            """)
        else:
            filtros.append("""
                (
                    r.idReceta IN (SELECT idReceta FROM estadoReceta WHERE estado = 'aprobado')
                    OR r.idUsuario = ?
                )
            """)
            params.append(id_usuario_logueado)
    else:
        filtros.append("""
            r.idReceta IN (
                SELECT idReceta FROM estadoReceta WHERE estado = 'aprobado'
            )
        """)

    if filtros:
        query += " WHERE " + " AND ".join(filtros)

    query += """
        GROUP BY r.idReceta, r.nombreReceta, r.descripcionReceta, r.fotoPrincipal, u.nickname
    """

    if ordenar_por == "reciente":
        query += " ORDER BY r.idReceta DESC"
    elif ordenar_por == "usuario":
        query += " ORDER BY u.nickname ASC"
    else:
        query += " ORDER BY r.nombreReceta ASC"

    recetas = await ejecutar_consulta_async(query, params, fetch=True)

    # Aplico el límite si se especifica
    if limite:
        recetas = recetas[:limite]

    print(f"Recetas encontradas: {len(recetas)}")
    return recetas if recetas else []

#listar todos los ingredientes
async def listar_ingredientes() -> List[Dict]:
    query = "SELECT idIngrediente, nombre FROM Ingredientes"
    ingredientes = await ejecutar_consulta_async(query, fetch=True)
    return ingredientes if ingredientes else []

#listar todos los tipos de receta
async def listar_tipos_receta() -> List[Dict]:
    """
    Devuelve todos los tipos de receta (id y descripcion)
    """
    query = "SELECT idTipo, descripcion FROM TiposReceta"
    tipos = await ejecutar_consulta_async(query, fetch=True)
    return tipos if tipos else []


#listar todas las unidades
async def listar_unidades() -> List[Dict]:
    """
    Devuelve todas las unidades (id y descripcion)
    """
    query = "SELECT idUnidad, descripcion FROM unidades"
    unidades = await ejecutar_consulta_async(query, fetch=True)
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
    conversiones = await ejecutar_consulta_async(query, fetch=True)
    print(conversiones)
    return conversiones if conversiones else []

#obtener receta por id 
async def obtener_receta_detallada(id_receta: int) -> Optional[Dict]:
    # Datos generales de la receta
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
    receta = await ejecutar_consulta_async(receta_query, [id_receta], fetch=True)
    if not receta:
        return None
    receta = receta[0]

    # Ingredientes utilizados
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
    ingredientes = await ejecutar_consulta_async(ingredientes_query, [id_receta], fetch=True)

    # Pasos de la receta
    pasos_query = """
        SELECT 
            idPaso,
            nroPaso,
            texto AS descripcionPaso
        FROM pasos
        WHERE idReceta = ?
        ORDER BY nroPaso ASC
    """
    pasos = await ejecutar_consulta_async(pasos_query, [id_receta], fetch=True)

    # Multimedia adicional por paso
    media_query = """
        SELECT 
            m.idPaso,
            m.urlContenido AS url,
            m.tipo_contenido AS tipo
        FROM multimedia m
        JOIN pasos p ON m.idPaso = p.idPaso
        WHERE p.idReceta = ?
    """
    media_por_paso = await ejecutar_consulta_async(media_query, [id_receta], fetch=True)

    # Asociar multimedia a cada paso
    for paso in pasos:
        paso["multimedia"] = [m for m in media_por_paso if m["idPaso"] == paso["idPaso"]]

    # Calificaciones
    calificacion_query = """
        SELECT 
            ISNULL(AVG(calificacion), 0) AS promedio,
            COUNT(*) AS cantidad
        FROM calificaciones
        WHERE idReceta = ?
    """
    calificaciones = await ejecutar_consulta_async(calificacion_query, [id_receta], fetch=True)
    calificaciones = calificaciones[0] if calificaciones else {"promedio": 0, "cantidad": 0}

    # Consolidar todo
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
        resultados = await ejecutar_consulta_async(query, (id_usuario, nombre), fetch=True)
        if resultados:
            return resultados[0]['idReceta']  
        return None
    except Exception as e:
        print(f"Error en buscar_receta_por_usuario_y_nombre: {e}")
        return None

# Verificar si la receta ya existe para el usuario
async def verificar_receta(id_usuario: int, nombre: str):
    receta_id = await buscar_receta_por_usuario_y_nombre(id_usuario, nombre)
    if receta_id:
        raise AppError(
            409,
            {
                "existe": True,
                "mensaje": "Receta ya existe",
                "receta_id": str(receta_id),
            },
        )
    return {
        "existe": False,
        "mensaje": "Receta nueva. Podés comenzar a cargarla.",
        "nombre": nombre,
    }

# Crear receta
async def crear_receta_completa(data: CrearRecetaRequest, id_usuario: int) -> int:
    # Devuelve el id de la receta creada, o lanza un error si algo falla
    query_receta = """
        INSERT INTO recetas (idUsuario, nombreReceta, descripcionReceta, fotoPrincipal, porciones, cantidadPersonas, idTipo)
        OUTPUT INSERTED.idReceta
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    receta_params = (
        id_usuario,
        data.nombreReceta,
        data.descripcionReceta,
        data.fotoPrincipal,
        data.porciones,
        data.cantidadPersonas,
        data.idTipo
    )
    resultado = await ejecutar_consulta_async(query_receta, receta_params, fetch=True)
    if not resultado:
        raise Exception("No se pudo insertar la receta")
    id_receta = resultado[0]["idReceta"]

    for ing in data.ingredientes:
        await ejecutar_consulta_async(
            """
            INSERT INTO utilizados (idReceta, idIngrediente, cantidad, idUnidad, observaciones)
            VALUES (?, ?, ?, ?, ?)
            """,
            (id_receta, ing.idIngrediente, ing.cantidad, ing.idUnidad, ing.observaciones)
        )

    for paso in data.pasos:
        res_paso = await ejecutar_consulta_async(
            """
            INSERT INTO pasos (idReceta, nroPaso, texto)
            OUTPUT INSERTED.idPaso
            VALUES (?, ?, ?)
            """,
            (id_receta, paso.nroPaso, paso.texto),
            fetch=True
        )
        if not res_paso:
            raise Exception("No se pudo insertar un paso")
        id_paso = res_paso[0]["idPaso"]

        for media in paso.multimedia:
            await ejecutar_consulta_async(
                """
                INSERT INTO multimedia (idPaso, tipo_contenido, extension, urlContenido)
                VALUES (?, ?, ?, ?)
                """,
                (id_paso, media.tipo_contenido, media.extension, media.urlContenido)
            )

    for foto in data.fotosAdicionales or []:
        await ejecutar_consulta_async(
            """
            INSERT INTO fotos (idReceta, urlFoto, extension)
            VALUES (?, ?, ?)
            """,
            (id_receta, foto.urlFoto, foto.extension)
        )

    await ejecutar_consulta_async(
        """
        INSERT INTO estadoReceta (idReceta, fecha_creacion, estado)
        VALUES (?, GETDATE(), 'pendiente')
        """,
        (id_receta,)
    )
    print(f"Receta creada con ID: {id_receta}")
    return id_receta

# Reemplazar receta (borra la receta antigua despues de q crea una nueva)
async def borrar_receta_completa(id_receta: int, id_usuario: int):
    # Eliminar referencias en recetasFavoritas
    await ejecutar_consulta_async("DELETE FROM recetasFavoritas WHERE idReceta = ?", (id_receta,))

    # Eliminar multimedia de pasos
    await ejecutar_consulta_async("""
        DELETE multimedia FROM multimedia 
        INNER JOIN pasos ON multimedia.idPaso = pasos.idPaso 
        WHERE pasos.idReceta = ?
    """, (id_receta,))

    # Eliminar pasos
    await ejecutar_consulta_async("DELETE FROM pasos WHERE idReceta = ?", (id_receta,))

    # Eliminar ingredientes utilizados
    await ejecutar_consulta_async("DELETE FROM utilizados WHERE idReceta = ?", (id_receta,))

    # Eliminar fotos adicionales
    await ejecutar_consulta_async("DELETE FROM fotos WHERE idReceta = ?", (id_receta,))

    # Eliminar estado de receta
    await ejecutar_consulta_async("DELETE FROM estadoReceta WHERE idReceta = ?", (id_receta,))

    # Finalmente eliminar receta
    await ejecutar_consulta_async("DELETE FROM recetas WHERE idReceta = ?", (id_receta,))

# Actualizar receta
async def actualizar_receta_completa(id_receta: int, data: CrearRecetaRequest, id_usuario: int) -> None:
    # 1. Actualizar datos generales en la tabla recetas
    query_update = """
        UPDATE recetas
        SET nombreReceta = ?, descripcionReceta = ?, fotoPrincipal = ?, porciones = ?, cantidadPersonas = ?, idTipo = ?
        WHERE idReceta = ? AND idUsuario = ?
    """
    params_update = (
        data.nombreReceta,
        data.descripcionReceta,
        data.fotoPrincipal,
        data.porciones,
        data.cantidadPersonas,
        data.idTipo,
        id_receta,
        id_usuario
    )
    await ejecutar_consulta_async(query_update, params_update)

    # 2. Borrar ingredientes relacionados
    await ejecutar_consulta_async(
        "DELETE FROM utilizados WHERE idReceta = ?",
        (id_receta,)
    )

    # 3. Borrar multimedia y pasos relacionados
    # Primero borrar multimedia:
    await ejecutar_consulta_async(
        """
        DELETE multimedia 
        FROM multimedia 
        INNER JOIN pasos ON multimedia.idPaso = pasos.idPaso
        WHERE pasos.idReceta = ?
        """,
        (id_receta,)
    )

    # Luego borrar pasos:
    await ejecutar_consulta_async(
        "DELETE FROM pasos WHERE idReceta = ?",
        (id_receta,)
    )

    # 4. Borrar fotos adicionales
    await ejecutar_consulta_async(
        "DELETE FROM fotos WHERE idReceta = ?",
        (id_receta,)
    )

    # 5. Insertar nuevos ingredientes
    for ing in data.ingredientes:
        await ejecutar_consulta_async(
            """
            INSERT INTO utilizados (idReceta, idIngrediente, cantidad, idUnidad, observaciones)
            VALUES (?, ?, ?, ?, ?)
            """,
            (id_receta, ing.idIngrediente, ing.cantidad, ing.idUnidad, ing.observaciones)
        )

    # 6. Insertar nuevos pasos y multimedia
    for paso in data.pasos:
        res_paso = await ejecutar_consulta_async(
            """
            INSERT INTO pasos (idReceta, nroPaso, texto)
            OUTPUT INSERTED.idPaso
            VALUES (?, ?, ?)
            """,
            (id_receta, paso.nroPaso, paso.texto),
            fetch=True
        )
        if not res_paso:
            raise Exception("No se pudo insertar un paso")
        id_paso = res_paso[0]["idPaso"]

        for media in paso.multimedia:
            await ejecutar_consulta_async(
                """
                INSERT INTO multimedia (idPaso, tipo_contenido, extension, urlContenido)
                VALUES (?, ?, ?, ?)
                """,
                (id_paso, media.tipo_contenido, media.extension, media.urlContenido)
            )

    # 7. Insertar fotos adicionales
    for foto in data.fotosAdicionales or []:
        await ejecutar_consulta_async(
            """
            INSERT INTO fotos (idReceta, urlFoto, extension)
            VALUES (?, ?, ?)
            """,
            (id_receta, foto.urlFoto, foto.extension)
        )

    # 8. Actualizar estado a pendiente (o el estado que uses)
    await ejecutar_consulta_async(
        """
        UPDATE estadoReceta SET estado = 'pendiente', fecha_creacion = GETDATE()
        WHERE idReceta = ?
        """,
        (id_receta,)
    )

# Obtener calificaciones de una receta
async def obtener_calificaciones_receta(id_receta: str, id_user: Optional[str] = None) -> List[Dict]:
    if id_user:
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
            AND (
                ec.estado = 'aprobado' OR c.idUsuario = ?
            )
        """
        calificaciones = await ejecutar_consulta_async(query, [id_receta, id_user], fetch=True)
    else:
        query = """
            SELECT 
                c.idCalificacion,
                c.calificacion,
                c.comentarios,
                u.nickname,
                ec.estado
            FROM calificaciones c
            JOIN usuarios u ON c.idUsuario = u.idUsuario
            LEFT JOIN estadoComentario ec ON c.idCalificacion = ec.idCalificacion
            WHERE c.idReceta = ?
            AND ec.estado = 'aprobado'
        """
        calificaciones = await ejecutar_consulta_async(query, [id_receta], fetch=True)
    print(f"Calificaciones encontradas: {calificaciones}")
    return calificaciones if calificaciones else []


#crear calificación de receta
async def calificar_receta(id_receta: str, id_usuario: str, calificacion: Calificacion):
    query_existente = "SELECT * FROM calificaciones WHERE idReceta = ? AND idUsuario = ?"
    existente = await ejecutar_consulta_async(query_existente, (id_receta, id_usuario), fetch=True)

    if existente:
        return {"error": "Ya has calificado esta receta.", "code": 409}

    query_insert = """
        INSERT INTO calificaciones (idReceta, idUsuario, calificacion, comentarios)
        OUTPUT INSERTED.idCalificacion
        VALUES (?, ?, ?, ?)
    """
    resultado = await ejecutar_consulta_async(
        query_insert,
        (id_receta, id_usuario, calificacion.calificacion, calificacion.comentarios),
        fetch=True
    )

    if not resultado:
        return {"error": "No se pudo insertar la calificación.", "code": 500}

    id_calificacion = resultado[0]["idCalificacion"]

    # Insertar el estado inicial como 'pendiente'
    query_estado = """
        INSERT INTO estadoComentario (idCalificacion, estado, fechaEstado)
        VALUES (?, 'pendiente', GETDATE())
    """
    await ejecutar_consulta_async(query_estado, (id_calificacion,))

    return {"success": True, "idCalificacion": id_calificacion}

