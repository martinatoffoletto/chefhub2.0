from typing import Optional
from pydantic import BaseModel, constr, condecimal


###################acessos a bd agregar actualizar, eliminar, etc###############################
"""
class TipoReceta(BaseModel):
    id_tipo: Optional[int]
    descripcion: Optional[constr(max_length=250)]

class EstadoReceta(BaseModel):
    id_receta: Optional[int]
    descripcion: Optional[constr(max_length=250)]

class Receta(BaseModel):
    id_receta: Optional[int]
    id_usuario: Optional[int]
    nombre_receta: Optional[constr(max_length=500)]
    descripcion_receta: Optional[constr(max_length=1000)]
    foto_principal: Optional[constr(max_length=300)]  # URL
    porciones: Optional[int]
    cantidad_personas: Optional[int]
    id_tipo: Optional[int]

class EstadoReceta(BaseModel):
    id_estado: Optional[int]        # ID único del estado (PK)
    id_receta: int                  # FK a Receta
    estado: Literal['aprobada', 'rechazada', 'pendiente']
    
    
class Ingrediente(BaseModel):
    id_ingrediente: Optional[int]
    nombre: Optional[constr(max_length=200)]


class Unidad(BaseModel):
    id_unidad: Optional[int]
    descripcion: constr(max_length=50)


class Utilizado(BaseModel):
    id_utilizado: Optional[int]
    id_receta: Optional[int]
    id_ingrediente: Optional[int]
    cantidad: Optional[int]
    id_unidad: Optional[int]
    observaciones: Optional[constr(max_length=500)]


class Conversion(BaseModel):
    id_conversion: Optional[int]
    id_unidad_origen: int
    id_unidad_destino: int
    factor_conversiones: Optional[float]


class Paso(BaseModel):
    id_paso: Optional[int]
    id_receta: Optional[int]
    nro_paso: Optional[int]
    texto: Optional[constr(max_length=4000)]


class Foto(BaseModel):
    id_foto: Optional[int]
    id_receta: int
    url_foto: Optional[constr(max_length=300)]
    extension: Optional[constr(max_length=5)]


class Multimedia(BaseModel):
    id_contenido: Optional[int]
    id_paso: int
    tipo_contenido: Optional[constr(max_length=10)]  # foto, video, audio
    extension: Optional[constr(max_length=5)]
    url_contenido: Optional[constr(max_length=300)]

#CRUD y consultas a la base de datos
async def crear_receta(receta: Receta,recetas_collection):
    receta_dict = receta.model_dump()
    result = await recetas_collection.insert_one(receta_dict)
    receta_dict["_id"] = str(result.inserted_id)
    return receta_dict
 
async def listar_recetas(
    recetas_collection,
    tipo: Optional[str] = None,
    usuario: Optional[str] = None,
    nombre: Optional[str] = None,
    contiene_ingrediente: Optional[str] = None,
    excluye_ingrediente: Optional[str] = None,
    sort: str = "nombre",
    order: str = "asc",
    limit: int = 10000
):
    query = {"estado": "Aprobada"}

    if contiene_ingrediente and excluye_ingrediente:
        query["$and"] = [
            {"ingredientes": {"$elemMatch": {"nombre": {"$regex": contiene_ingrediente, "$options": "i"}}}},
            {"ingredientes": {"$not": {"$elemMatch": {"nombre": {"$regex": excluye_ingrediente, "$options": "i"}}}}}
        ]
    elif contiene_ingrediente:
        query["ingredientes.nombre"] = {"$regex": contiene_ingrediente, "$options": "i"} 
    elif excluye_ingrediente:
        query["ingredientes"] = {"$not": {"$elemMatch": {"nombre": {"$regex": excluye_ingrediente, "$options": "i"}}}}


    if tipo:
        query["tipo"] ={"$regex": tipo, "$options": "i"} 

    if usuario:
        query["usuarioCreador"] = {"$regex": usuario, "$options": "i"} 
        
    if nombre:
        query["nombre"] = {"$regex": nombre, "$options": "i"}  # "i" para que sea case-insensitive


    sort_order = ASCENDING if order == "asc" else DESCENDING

    cursor = recetas_collection.find(query).sort(sort, sort_order).limit(limit)
    resultados = await cursor.to_list(length=limit)
    return resultados
    


async def obtener_receta_por_id(receta_id: str,recetas_collection):
    return await recetas_collection.find_one({"_id": ObjectId(receta_id)})

async def actualizar_receta(receta_id: str, receta_data: Receta, collection):
    await collection.update_one(
        {"_id": ObjectId(receta_id)},
        {"$set": receta_data.model_dump()} 
    )

async def eliminar_receta(receta_id: str,recetas_collection):
    result = await recetas_collection.delete_one({"_id": ObjectId(receta_id)})
    return result.deleted_count > 0

#buscar por parte nombre (varias recetas)
async def buscar_recetas_por_nombre_parcial(value: str, recetas_collection):
    return await recetas_collection.find({
        "nombre": {"$regex": value, "$options": "i"}
    }).to_list(length=None)

#buscar por nombre exacto, tipo o usuarioCreador (x nombre , por tipo y usuariosCreador devuelve varias)
async def buscar_recetas_por_campo_exacto(campo: str, valor: str, recetas_collection):

    return await recetas_collection.find({
        campo: valor
    }).to_list(length=None)


async def buscar_por_ingrediente(nombre_ingrediente: str, recetas_collection):
    return await recetas_collection.find({
        "ingredientes.nombre": {"$regex": nombre_ingrediente, "$options": "i"}
    }).to_list(length=None)

async def excluir_ingrediente(nombre_ingrediente: str, recetas_collection):
    return await recetas_collection.find({
        "ingredientes": {
            "$not": {
                "$elemMatch": {
                    "nombre": {"$regex": nombre_ingrediente, "$options": "i"}
                }
            }
        }
    }).to_list(length=None)

    
    """