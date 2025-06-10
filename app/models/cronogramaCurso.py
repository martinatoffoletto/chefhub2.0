from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import date
from app.config.db import ejecutar_consulta_async

class CronogramaCursos(BaseModel):
    idCronograma: Optional[int] = None
    idSede: int
    idCurso: int
    fechaInicio: Optional[date] = None
    fechaFin: Optional[date] = None
    vacantesDisponibles: Optional[int] = None


# CRUD. Queries para acceder a la base de datos

async def crear_cronograma(cronograma: CronogramaCursos) -> Dict:
    query = """INSERT INTO cronogramaCursos 
               (idSede, idCurso, fechaInicio, fechaFin, vacantesDisponibles) 
               VALUES (?, ?, ?, ?, ?)"""
    params = (
        cronograma.idSede,
        cronograma.idCurso,
        cronograma.fechaInicio,
        cronograma.fechaFin,
        cronograma.vacantesDisponibles
    )
    await ejecutar_consulta_async(query, params)
    # Obtener el último registro insertado
    result = await ejecutar_consulta_async("SELECT TOP 1 * FROM cronogramaCursos ORDER BY idCronograma DESC", fetch=True)
    return result[0] if result else None

async def listar_cronogramas() -> List[Dict]:
    query = "SELECT * FROM cronogramaCursos"
    result = await ejecutar_consulta_async(query, fetch=True)
    return result if result else []

async def obtener_cronograma_por_id(id_cronograma: int) -> Optional[Dict]:
    query = "SELECT * FROM cronogramaCursos WHERE idCronograma = ?"
    result = await ejecutar_consulta_async(query, (id_cronograma,), fetch=True)
    return result[0] if result else None

async def obtener_cronogramas_por_curso(id_curso: int) -> List[Dict]:
    query = "SELECT * FROM cronogramaCursos WHERE idCurso = ?"
    result = await ejecutar_consulta_async(query, (id_curso,), fetch=True)
    return result if result else []

async def obtener_cronogramas_por_sede(id_sede: int) -> List[Dict]:
    query = "SELECT * FROM cronogramaCursos WHERE idSede = ?"
    result = await ejecutar_consulta_async(query, (id_sede,), fetch=True)
    return result if result else []

async def aumentar_vacantes(id_cronograma: int, cantidad: int) -> Optional[Dict]:
    query = """UPDATE cronogramaCursos 
               SET vacantesDisponibles = vacantesDisponibles + ? 
               WHERE idCronograma = ?"""
    await ejecutar_consulta_async(query, (cantidad, id_cronograma))
    # Devolver el registro actualizado
    result = await ejecutar_consulta_async("SELECT * FROM cronogramaCursos WHERE idCronograma = ?", (id_cronograma,), fetch=True)
    return result[0] if result else None

async def disminuir_vacantes(id_cronograma: int, cantidad: int) -> Optional[Dict]:
    query = """UPDATE cronogramaCursos 
               SET vacantesDisponibles = CASE 
                   WHEN vacantesDisponibles - ? < 0 THEN 0
                   ELSE vacantesDisponibles - ?
               END
               WHERE idCronograma = ?"""
    await ejecutar_consulta_async(query, (cantidad, cantidad, id_cronograma))
    # Devolver el registro actualizado
    result = await ejecutar_consulta_async("SELECT * FROM cronogramaCursos WHERE idCronograma = ?", (id_cronograma,), fetch=True)
    return result[0] if result else None