from typing import Optional, Dict, List
from pydantic import BaseModel
from app.config.db import ejecutar_consulta

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

def listar_sedes() -> List[Dict]:
    query = "SELECT * FROM sedes"
    result = ejecutar_consulta(query, fetch=True)
    return result if result else []

def obtener_sede_por_id(id_sede: int) -> Optional[Dict]:
    query = "SELECT * FROM sedes WHERE idSede = ?"
    result = ejecutar_consulta(query, (id_sede,), fetch=True)
    return result[0] if result else None
