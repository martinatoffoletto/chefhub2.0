from typing import Optional, List, Dict
from pydantic import BaseModel
from app.config.db import ejecutar_consulta

class Calificacion(BaseModel):
    idCalificacion: Optional[int] = None
    idusuario: int
    idReceta: int
    calificacion: int
    comentarios: Optional[str] = None

# CRUD operations for Calificacion

def crear_calificacion(calificacion: Calificacion) -> Dict:
    query = """INSERT INTO calificaciones 
               (idusuario, idReceta, calificacion, comentarios) 
               VALUES (?, ?, ?, ?)"""
    params = (
        calificacion.idusuario,
        calificacion.idReceta,
        calificacion.calificacion,
        calificacion.comentarios
    )
    ejecutar_consulta(query, params)
    # Obtener el último registro insertado
    result = ejecutar_consulta("SELECT TOP 1 * FROM calificaciones ORDER BY idCalificacion DESC", fetch=True)
    return result[0] if result else None

def obtener_calificaciones_por_receta(id_receta: int) -> List[Dict]:
    query = "SELECT * FROM calificaciones WHERE idReceta = ?"
    result = ejecutar_consulta(query, (id_receta,), fetch=True)
    return result if result else []

def calcular_promedio_calificaciones(id_receta: int) -> Optional[float]:
    query = "SELECT AVG(calificacion) as promedio FROM calificaciones WHERE idReceta = ?"
    result = ejecutar_consulta(query, (id_receta,), fetch=True)
    return float(result[0]['promedio']) if result and result[0]['promedio'] is not None else None