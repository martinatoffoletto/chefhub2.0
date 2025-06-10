from typing import Optional
from pydantic import BaseModel, constr, condecimal

class Calificacion(BaseModel):
    id_calificacion: Optional[int]
    id_usuario: Optional[int]
    id_receta: Optional[int]
    calificacion: Optional[int]
    comentarios: Optional[constr(max_length=500)]
