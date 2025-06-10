from typing import Optional, List, Dict
from pydantic import BaseModel
from app.config.db import ejecutar_consulta_async

#clase principal


class Curso(BaseModel):
    id_curso: Optional[int] 
    descripcion: str
    contenidos: str
    requerimientos: str
    duracion: int
    precio: int
    modalidad: str  # presencial, remoto, virtual

#CRUD. consultas a la base de datos

async def listar_cursos() -> List[Dict]:
    query = "SELECT * FROM cursos"
    result = await ejecutar_consulta_async(query, fetch=True)
    return result if result else []

async def obtener_curso_por_id(id_curso: int) -> Optional[Dict]:
    query = "SELECT * FROM cursos WHERE idCurso = ?"
    result = await ejecutar_consulta_async(query, (id_curso,), fetch=True)
    return result[0] if result else None

async def buscar_curso_por_nombre(nombre: str) -> List[Dict]:
    # En SQL Server, usar LIKE para búsquedas por patrón
    query = "SELECT * FROM cursos WHERE descripcion LIKE ?"
    pattern = f"%{nombre}%"
    result = await ejecutar_consulta_async(query, (pattern,), fetch=True)
    return result if result else []
