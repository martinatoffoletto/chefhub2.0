from typing import Optional
from pydantic import BaseModel, constr, condecimal
from datetime import date, datetime

class AsistenciaCurso(BaseModel):
    id_asistencia: Optional[int]
    id_alumno: int
    id_cronograma: int
    fecha: Optional[datetime]
#CRUD

"""
async def crear_inscripcion(inscripcion: Inscripcion, inscripciones_collection):
    inscripcion_dict = inscripcion.model_dump()
    result = await inscripciones_collection.insert_one(inscripcion_dict)
    inscripcion_dict["_id"] = str(result.inserted_id)
    return inscripcion_dict


async def obtener_inscripcion_por_id(inscripcion_id: str, inscripciones_collection):
    return await inscripciones_collection.find_one({"_id": ObjectId(inscripcion_id)})


async def eliminar_inscripcion(inscripcion_id: str, inscripciones_collection):
    result = await inscripciones_collection.delete_one({"_id": ObjectId(inscripcion_id)})
    return result.deleted_count > 0

#obtener inscripciones por alumno
async def obtener_inscripciones_por_alumno(alumno_id: str, inscripciones_collection):
    inscripcion=await inscripciones_collection.find({"alumno_id": alumno_id}).to_list(length=None)
    print("Inscripciones encontradas:", inscripcion)
    return inscripcion

#agregar asistencia
async def agregar_asistencia(inscripcion_id: str, asistencia: str, inscripciones_collection):
    result = await inscripciones_collection.update_one(
        {"_id": ObjectId(inscripcion_id)},
        {"$addToSet": {"asistencia": asistencia}}
    )
    return result.modified_count > 0
    """