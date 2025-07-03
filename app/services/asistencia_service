from typing import List, Dict, Optional
from datetime import datetime
from app.models.asistenciaCurso import AsistenciaCursos, crear_asistencia, obtener_asistencia_por_id, \
    obtener_asistencias_por_cronograma, obtener_asistencias_por_alumno, eliminar_inscripcion, obtener_cronogramas_por_alumno

# Crear una nueva asistencia, validando que no exista una igual antes
async def registrar_asistencia_service(asistencia: AsistenciaCursos) -> Optional[Dict]:
    # Validar si ya existe asistencia para el alumno en ese cronograma y fecha
    asistencias = await obtener_asistencias_por_alumno(asistencia.idAlumno)
    for a in asistencias:
        if a['idCronograma'] == asistencia.idCronograma:
            # opcional: podrías comparar fechas para evitar duplicados
            if asistencia.fecha is None or a.get('fecha') == asistencia.fecha:
                # Ya existe una asistencia para ese alumno y cronograma en esa fecha
                return None

    nueva_asistencia = await crear_asistencia(asistencia)
    return nueva_asistencia

# Obtener asistencia por id
async def obtener_asistencia_service(id_asistencia: int) -> Optional[Dict]:
    return await obtener_asistencia_por_id(id_asistencia)

# Obtener asistencias de un cronograma
async def obtener_asistencias_cronograma_service(id_cronograma: int) -> List[Dict]:
    return await obtener_asistencias_por_cronograma(id_cronograma)

# Obtener asistencias de un alumno
async def obtener_asistencias_alumno_service(id_alumno: int) -> List[Dict]:
    return await obtener_asistencias_por_alumno(id_alumno)

# Eliminar asistencia (inscripción)
async def eliminar_inscripcion_service(id_alumno: int, id_cronograma: int) -> bool:
    return await eliminar_inscripcion(id_alumno, id_cronograma)

# Obtener cronogramas donde asistió alumno
async def obtener_cronogramas_alumno_service(id_alumno: int) -> List[Dict]:
    return await obtener_cronogramas_por_alumno(id_alumno)