from typing import Optional
from pydantic import BaseModel, constr, condecimal
from datetime import date, datetime

class CronogramaCurso(BaseModel):
    id_cronograma: Optional[int]
    id_sede: int
    id_curso: int
    fecha_inicio: Optional[date]
    fecha_fin: Optional[date]
    vacantes_disponibles: Optional[int]

# CRUD. Queries para acceder a la base de datos
"""
async def crear_oferta_curso(oferta: OfertaCurso, ofertas_collection):
    oferta_dict = oferta.model_dump()
    result = await ofertas_collection.insert_one(oferta_dict)
    oferta_dict["_id"] = result.inserted_id
    return oferta_dict

async def listar_ofertas_curso(ofertas_collection):
    return await ofertas_collection.find().to_list(length=None)

#obtener oferta por id
async def obtener_oferta_curso_por_id(oferta_id: str, ofertas_collection):
    return await ofertas_collection.find_one({"_id": ObjectId(oferta_id)})

async def actualizar_oferta_curso(oferta_id: str, oferta: OfertaCurso, ofertas_collection):
    oferta_dict = oferta.model_dump()
    result = await ofertas_collection.replace_one({"_id": ObjectId(oferta_id)}, oferta_dict)
    return result.modified_count > 0

async def eliminar_oferta_curso(oferta_id: str, ofertas_collection):
    result = await ofertas_collection.delete_one({"_id": ObjectId(oferta_id)})
    return result.deleted_count > 0

async def obtener_ofertas_por_curso(curso_id: str, ofertas_collection):
    return await ofertas_collection.find({"curso_id": curso_id}).to_list(length=None)

async def obtener_ofertas_por_sede(sede_id: str, ofertas_collection):
    ofertas= await ofertas_collection.find({"sede_id": sede_id}).to_list(length=None)   
    return ofertas

#aumentar vacantes  
async def aumentar_vacantes(oferta_id: str, ofertas_collection):
    result = await ofertas_collection.update_one(
        {"_id": ObjectId(oferta_id)},
        {"$inc": {"vacantes": 1}}
    )
    return result.modified_count > 0
#disminuir vacantes     
async def disminuir_vacantes(oferta_id: str, ofertas_collection):
    result = await ofertas_collection.update_one(
        {"_id": ObjectId(oferta_id)},
        {"$inc": {"vacantes": -1}}
    )
    return result.modified_count > 0
"""
