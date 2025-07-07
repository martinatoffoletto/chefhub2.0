from typing import Optional
from pydantic import BaseModel

class Calificacion(BaseModel):
    idCalificacion: Optional[int] = None
    idusuario: Optional[int] = None
    idReceta: Optional[int] = None
    calificacion: int
    comentarios: Optional[str] = None


