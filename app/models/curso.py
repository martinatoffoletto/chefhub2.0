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

