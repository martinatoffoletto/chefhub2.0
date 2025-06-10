
from app.models.receta import *
from app.models.usuario import *
from app.models.appError import AppError
from datetime import datetime

############ LOGICA DE NEGOCIO RECETAS ############

# Ver todas las recetas por orden alfabético  
async def obtener_recetas(
    tipo_receta: Optional[int] = None,
    id_usuario: Optional[int] = None,
    nombre: Optional[str] = None,
    tiene_ingrediente: Optional[int] = None,
    no_tiene_ingrediente: Optional[int] = None,
    ordenar_por: str = "fecha",
    orden: str = "DESC",
    limite: Optional[int] = None,
    state: Optional[str] = "aprobado"
) -> List[Dict]:
    recetas = await listar_recetas(
        tipo_receta=tipo_receta,
        contiene_ingrediente=tiene_ingrediente,
        excluye_ingrediente=no_tiene_ingrediente,
        id_usuario=id_usuario,
        nombre=nombre,
        ordenar_por=ordenar_por,
        orden=orden,
        limit=limite,
        estado=state
    )
    return recetas

# Obtener todos los ingredientes (id y nombre)
async def obtener_ingredientes() -> List[Dict]:
    ingredientes = await listar_ingredientes()
    return ingredientes if ingredientes else []

# Obtener todos los tipos de receta (id y descripcion)
async def obtener_tipos_receta() -> List[Dict]:
    tipos = await listar_tipos_receta()
    return tipos if tipos else []


# Ver receta por id
async def obtener_por_id(receta_id):
    receta = await obtener_receta_completa(receta_id)
    print("Receta obtenida por ID:", receta)
    return receta if receta else {}
    


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