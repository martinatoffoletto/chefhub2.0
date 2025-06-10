from typing import List, Dict, Optional
from pydantic import BaseModel
from datetime import datetime
from app.config.db import ejecutar_consulta

class AsistenciaCursos(BaseModel):
    idAsistencia: Optional[int] = None
    idAlumno: int
    idCronograma: int
    fecha: Optional[datetime] = None


# CRUD

def crear_asistencia(asistencia: AsistenciaCursos) -> Dict:
    query = """INSERT INTO asistenciaCursos 
               (idAlumno, idCronograma, fecha) 
               VALUES (?, ?, ?)"""
    params = (
        asistencia.idAlumno,
        asistencia.idCronograma,
        asistencia.fecha
    )
    ejecutar_consulta(query, params)
    # Obtener el último id insertado
    result = ejecutar_consulta("SELECT TOP 1 * FROM asistenciaCursos ORDER BY idAsistencia DESC", fetch=True)
    return result[0] if result else None

def obtener_asistencia_por_id(id_asistencia: int) -> Optional[Dict]:
    query = "SELECT * FROM asistenciaCursos WHERE idAsistencia = ?"
    result = ejecutar_consulta(query, (id_asistencia,), fetch=True)
    return result[0] if result else None

def obtener_asistencias_por_cronograma(id_cronograma: int) -> List[Dict]:
    query = "SELECT * FROM asistenciaCursos WHERE idCronograma = ?"
    result = ejecutar_consulta(query, (id_cronograma,), fetch=True)
    return result if result else []

def obtener_asistencias_por_alumno(id_alumno: int) -> List[Dict]:
    query = "SELECT * FROM asistenciaCursos WHERE idAlumno = ?"
    result = ejecutar_consulta(query, (id_alumno,), fetch=True)
    return result if result else []

def eliminar_inscripcion(id_alumno: int, id_cronograma: int) -> bool:
    query = "DELETE FROM asistenciaCursos WHERE idAlumno = ? AND idCronograma = ?"
    ejecutar_consulta(query, (id_alumno, id_cronograma))
    return True  # Asume que la operación fue exitosa

def obtener_cronogramas_por_alumno(id_alumno: int) -> List[Dict]:
    query = """SELECT DISTINCT c.* 
               FROM cronogramaCursos c
               JOIN asistenciaCursos a ON c.idCronograma = a.idCronograma
               WHERE a.idAlumno = ?"""
    result = ejecutar_consulta(query, (id_alumno,), fetch=True)
    return result if result else []