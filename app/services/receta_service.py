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
                SELECT idReceta FROM estadoReceta WHERE estado = 'Aprobado'
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

# Buscar recetas por usuario y nombre 
async def buscar_receta_por_usuario_y_nombre(id_usuario: int, nombre: str) -> Optional[Dict]:
    """
    Busca una receta exacta por usuario y nombre (exact match)
    """
    try:
        query = """
            SELECT r.*, 
                   (SELECT TOP 1 estado FROM EstadoReceta er 
                    WHERE er.idReceta = r.idReceta 
                    ORDER BY er.idEstado DESC) as estado
            FROM Receta r
            WHERE r.idUsuario = ? AND r.nombreReceta = ?
        """
        receta = await ejecutar_consulta_async(query, (id_usuario, nombre), fetch=True)
        return receta[0] if receta else None
    except Exception as e:
        print(f"Error en búsqueda exacta: {str(e)}")
        raise e

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
            un.nombre AS unidad,
            u.cantidad,
            u.observaciones
        FROM utilizados u
        JOIN ingredientes i ON u.idIngrediente = i.idIngrediente
        JOIN unidades un ON u.idUnidad = un.idUnidad
        WHERE u.idReceta = ?
    """
    ingredientes = await ejecutar_consulta_async(ingredientes_query, [id_receta], fetch=True)

    # Pasos de la receta (si existe tabla pasosReceta)
    pasos_query = """
        SELECT 
            nroPaso,
            descripcionPaso,
            mediaPaso
        FROM pasosReceta
        WHERE idReceta = ?
        ORDER BY nroPaso ASC
    """
    pasos = await ejecutar_consulta_async(pasos_query, [id_receta], fetch=True)

    # Multimedia adicional
    media_query = """
        SELECT 
            url,
            tipo
        FROM multimediaReceta
        WHERE idReceta = ?
    """
    multimedia = await ejecutar_consulta_async(media_query, [id_receta], fetch=True)

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
        "multimedia": multimedia,
        "calificaciones": calificaciones
    }

    return receta_detallada




"""
# Verificar receta
async def verificar_receta(nombre: str, user: Usuario):
    recetas = await buscar_recetas_por_campo_exacto("nombre", nombre, get_recetas_collection())
    for receta in recetas:
        if receta.get("usuarioCreador") == user["alias"]:
            raise AppError(409, {
                "existe": True,
                "mensaje": "Receta ya existe",
                "receta_id": str(receta["_id"]),
            })
    return {"existe": False, "mensaje": "Receta nueva. Podés comenzar a cargarla.", "nombre": nombre}

# Crear receta
async def crear_recetas(receta: Receta, user: Usuario): 
    print("user en receta", user)
    receta.usuarioCreador = user["alias"]
    receta.fecha_publicacion = datetime.now().isoformat()
    return await crear_receta(receta, get_recetas_collection())

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