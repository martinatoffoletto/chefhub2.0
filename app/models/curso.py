from typing import Optional
from pydantic import BaseModel, constr, condecimal
from datetime import date, datetime

#clase principal

"""
class Curso(BaseModel):
    id_curso: Optional[int]
    descripcion: Optional[constr(max_length=300)]
    contenidos: Optional[constr(max_length=500)]
    requerimientos: Optional[constr(max_length=500)]
    duracion: Optional[int]
    precio: Optional[condecimal(max_digits=12, decimal_places=2)]
    modalidad: Optional[constr(max_length=20)]  # presencial, remoto, virtual

#CRUD. consultas a la base de datos

async def crear_curso(curso: Curso, cursos_collection):
    curso_dict = curso.model_dump()
    result = await cursos_collection.insert_one(curso_dict)
    curso_dict["_id"] = result.inserted_id
    return curso_dict

async def listar_cursos(cursos_collection):
    cursos = await cursos_collection.find().to_list(length=None)
    return cursos

async def obtener_curso_por_id(curso_id: str, cursos_collection):
    return await cursos_collection.find_one({"_id": ObjectId(curso_id)})

async def actualizar_curso(curso_id: str, curso: Curso, cursos_collection):
    curso_dict = curso.model_dump(by_alias=True)
    result = await cursos_collection.replace_one({"_id": ObjectId(curso_id)}, curso_dict)
    return result.modified_count > 0

async def eliminar_curso(curso_id: str, cursos_collection):
    result = await cursos_collection.delete_one({"_id": ObjectId(curso_id)})
    return result.deleted_count > 0

async def buscar_cursos_por_nombre(nombre: str, cursos_collection):
    cursos = await cursos_collection.find({
        "nombre": {
            "$regex": nombre,
            "$options": "i"  # i = case-insensitive
        }
    }).to_list(length=None)
    return cursos
"""