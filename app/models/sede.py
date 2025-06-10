from typing import Optional
from pydantic import BaseModel, constr, condecimal
from datetime import date, datetime
"""
class Sede(BaseModel):
    id_sede: Optional[int]
    nombre_sede: constr(max_length=150)
    direccion_sede: constr(max_length=250)
    telefono_sede: Optional[constr(max_length=15)]
    mail_sede: Optional[constr(max_length=150)]
    whats_app: Optional[constr(max_length=15)]
    tipo_bonificacion: Optional[constr(max_length=20)]
    bonificacion_cursos: Optional[condecimal(max_digits=10, decimal_places=2)]
    tipo_promocion: Optional[constr(max_length=20)]
    promocion_cursos: Optional[condecimal(max_digits=10, decimal_places=2)]


#CRUD
async def crear_sede(sede: Sede, sedes_collection):
    sede_dict = sede.model_dump()
    result = await sedes_collection.insert_one(sede_dict)
    sede_dict["_id"] = result.inserted_id
    return sede_dict

async def listar_sedes(sedes_collection):
    return await sedes_collection.find().to_list(length=None)

async def obtener_sede_por_id(sede_id: str, sedes_collection):
    return await sedes_collection.find_one({"_id": ObjectId(sede_id)})

async def actualizar_sede(sede_id: str, sede: Sede, sedes_collection):
    sede_dict = sede.model_dump()
    result = await sedes_collection.replace_one({"_id": ObjectId(sede_id)}, sede_dict)
    return result.modified_count > 0

async def eliminar_sede(sede_id: str, sedes_collection):
    result = await sedes_collection.delete_one({"_id": ObjectId(sede_id)})
    return result.deleted_count > 0"""