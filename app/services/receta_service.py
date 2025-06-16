from app.services.user_services import obtener_nickname_por_id
from app.models.receta import *
from app.models.usuario import *
from app.models.appError import AppError
from datetime import datetime

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
        VALUES (%s, %s, %s, %s, %s, %s, %s)
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
    resultado = await ejecutar_consulta_async(query_receta, receta_params)
    id_receta = resultado[0]["idReceta"]

    for ing in data.ingredientes:
        await ejecutar_consulta_async(
            """
            INSERT INTO utilizados (idReceta, idIngrediente, cantidad, idUnidad, observaciones)
            VALUES (%s, %s, %s, %s, %s)
            """,
            (id_receta, ing.idIngrediente, ing.cantidad, ing.idUnidad, ing.observaciones)
        )

    for paso in data.pasos:
        res_paso = await ejecutar_consulta_async(
            """
            INSERT INTO pasos (idReceta, nroPaso, texto)
            OUTPUT INSERTED.idPaso
            VALUES (%s, %s, %s)
            """,
            (id_receta, paso.nroPaso, paso.texto)
        )
        id_paso = res_paso[0]["idPaso"]

        for media in paso.multimedia:
            await ejecutar_consulta_async(
                """
                INSERT INTO multimedia (idPaso, tipo_contenido, extension, urlContenido)
                VALUES (%s, %s, %s, %s)
                """,
                (id_paso, media.tipo_contenido, media.extension, media.urlContenido)
            )

    for foto in data.fotosAdicionales:
        await ejecutar_consulta_async(
            """
            INSERT INTO fotos (idReceta, urlFoto, extension)
            VALUES (%s, %s, %s)
            """,
            (id_receta, foto.urlFoto, foto.extension)
        )

    await ejecutar_consulta_async(
        """
        INSERT INTO estadoReceta (idReceta, fecha_creacion, estado)
        VALUES (%s, GETDATE(), 'pendiente')
        """,
        (id_receta,)
    )

    return id_receta


"""
# Reemplazar receta
async def reemplazar_receta(receta: Receta, user: Usuario):
    await eliminar_receta_por_nombre_y_usuario(receta.nombre, user)
    return await crear_recetas(receta, user)

# Eliminar receta por nombre y usuario
async def eliminar_receta_por_nombre_y_usuario(nombre: str, user: Usuario):
    recetas = await buscar_recetas_por_campo_exacto("nombre", nombre, get_recetas_collection())
    for receta in recetas:
        if receta.get("usuarioCreador") == user.alias:
            await eliminar_receta(str(receta["_id"]), get_recetas_collection())
            return True

# Actualizar receta
async def actualizar_recetas(id: str, receta_data: Receta):
    receta_data.fecha_publicacion = datetime.now().isoformat()
    await actualizar_receta(id, receta_data, get_recetas_collection())
    return {"mensaje": "Receta actualizada. Queda pendiente de aprobación."}
    
    """