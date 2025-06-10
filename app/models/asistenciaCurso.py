from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
from app.config.db import ejecutar_consulta_async

class AsistenciaCursos(BaseModel):
    idAsistencia: Optional[int] = None
    idAlumno: int
    idCronograma: int
    fecha: Optional[datetime] = None


# CRUD

async def crear_asistencia(asistencia: AsistenciaCursos) -> Dict:
    query = """INSERT INTO asistenciaCursos 
               (idAlumno, idCronograma, fecha) 
               VALUES (?, ?, ?)"""
    params = (
        asistencia.idAlumno,
        asistencia.idCronograma,
        asistencia.fecha
    )
    await ejecutar_consulta_async(query, params)
    # Obtener el último id insertado
    result = await ejecutar_consulta_async("SELECT TOP 1 * FROM asistenciaCursos ORDER BY idAsistencia DESC", fetch=True)
    return result[0] if result else None

async def obtener_asistencia_por_id(id_asistencia: int) -> Optional[Dict]:
    query = "SELECT * FROM asistenciaCursos WHERE idAsistencia = ?"
    result = await ejecutar_consulta_async(query, (id_asistencia,), fetch=True)
    return result[0] if result else None

async def obtener_asistencias_por_cronograma(id_cronograma: int) -> List[Dict]:
    query = "SELECT * FROM asistenciaCursos WHERE idCronograma = ?"
    result = await ejecutar_consulta_async(query, (id_cronograma,), fetch=True)
    return result if result else []

async def obtener_asistencias_por_alumno(id_alumno: int) -> List[Dict]:
    query = "SELECT * FROM asistenciaCursos WHERE idAlumno = ?"
    result = await ejecutar_consulta_async(query, (id_alumno,), fetch=True)
    return result if result else []

async def eliminar_inscripcion(id_alumno: int, id_cronograma: int) -> bool:
    query = "DELETE FROM asistenciaCursos WHERE idAlumno = ? AND idCronograma = ?"
    await ejecutar_consulta_async(query, (id_alumno, id_cronograma))
    return True  # Asume que la operación fue exitosa

async def obtener_cronogramas_por_alumno(id_alumno: int) -> List[Dict]:
    query = """SELECT DISTINCT c.* 
               FROM cronogramaCursos c
               JOIN asistenciaCursos a ON c.idCronograma = a.idCronograma
               WHERE a.idAlumno = ?"""
    result = await ejecutar_consulta_async(query, (id_alumno,), fetch=True)
    return result if result else []