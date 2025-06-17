from typing import Optional, List, Dict
from pydantic import BaseModel
from app.config.db import ejecutar_consulta_async

class Calificacion(BaseModel):
    idCalificacion: Optional[int] = None
    idusuario: Optional[int] = None
    idReceta: Optional[int] = None
    calificacion: int
    comentarios: Optional[str] = None


