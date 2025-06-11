from typing import Optional, Dict, List
from pydantic import BaseModel
from app.config.db import ejecutar_consulta_async

class Sedes(BaseModel):
    idSede: Optional[int] = None
    nombreSede: str
    direccionSede: str
    telefonoSede: Optional[str] = None
    mailSede: Optional[str] = None
    whatsApp: Optional[str] = None
    tipoBonificacion: Optional[str] = None
    bonificacionCursos: Optional[float] = None
    tipoPromocion: Optional[str] = None
    promocionCursos: Optional[float] = None


#CRUD

