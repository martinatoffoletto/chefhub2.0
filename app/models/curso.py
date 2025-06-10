from typing import Optional, List, Dict
from pydantic import BaseModel, constr, condecimal
from datetime import date, datetime
from app.config.db import ejecutar_consulta
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
""""""

def listar_cursos() -> List[Dict]:
    query = "SELECT * FROM cursos"
    result = ejecutar_consulta(query, fetch=True)
    return result if result else []


def obtener_curso_por_id(id_curso: int) -> Optional[Dict]:
    query = "SELECT * FROM cursos WHERE idCurso = %s"
    result = ejecutar_consulta(query, (id_curso,), fetch=True)
    return result[0] if result else None


def buscar_curso_por_nombre(nombre: str) -> List[Dict]:
    query = "SELECT * FROM cursos WHERE descripcion REGEXP %s"
    regex = nombre
    result = ejecutar_consulta(query, (regex,), fetch=True)
    return result if result else []
