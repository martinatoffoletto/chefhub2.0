from fastapi import APIRouter, HTTPException, status
from typing import List
from app.models.asistenciaCurso import AsistenciaCursos, crear_asistencia, obtener_asistencia_por_id, \
    obtener_asistencias_por_cronograma, obtener_asistencias_por_alumno, eliminar_inscripcion, obtener_cronogramas_por_alumno

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])

# Crear una asistencia
@router.post("/", response_model=AsistenciaCursos, status_code=status.HTTP_201_CREATED)
async def crear_asistencia_controller(asistencia: AsistenciaCursos):
    nueva_asistencia = await crear_asistencia(asistencia)
    if not nueva_asistencia:
        raise HTTPException(status_code=400, detail="No se pudo crear la asistencia")
    return nueva_asistencia

# Obtener asistencia por ID
@router.get("/{id_asistencia}", response_model=AsistenciaCursos)
async def get_asistencia_por_id(id_asistencia: int):
    asistencia = await obtener_asistencia_por_id(id_asistencia)
    if not asistencia:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    return asistencia

# Obtener todas las asistencias de un cronograma
@router.get("/cronograma/{id_cronograma}", response_model=List[AsistenciaCursos])
async def get_asistencias_por_cronograma(id_cronograma: int):
    asistencias = await obtener_asistencias_por_cronograma(id_cronograma)
    return asistencias

# Obtener todas las asistencias de un alumno
@router.get("/alumno/{id_alumno}", response_model=List[AsistenciaCursos])
async def get_asistencias_por_alumno(id_alumno: int):
    asistencias = await obtener_asistencias_por_alumno(id_alumno)
    return asistencias

# Eliminar inscripción (asistencia) por alumno y cronograma
@router.delete("/alumno/{id_alumno}/cronograma/{id_cronograma}", status_code=status.HTTP_204_NO_CONTENT)
async def eliminar_inscripcion_controller(id_alumno: int, id_cronograma: int):
    exito = await eliminar_inscripcion(id_alumno, id_cronograma)
    if not exito:
        raise HTTPException(status_code=404, detail="Inscripción no encontrada o no eliminada")
    return

# Obtener cronogramas en los que asistió un alumno
@router.get("/cronogramas/alumno/{id_alumno}", response_model=List[dict])
async def get_cronogramas_por_alumno(id_alumno: int):
    cronogramas = await obtener_cronogramas_por_alumno(id_alumno)
    return cronogramas