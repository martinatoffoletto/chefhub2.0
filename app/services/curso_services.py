# curso, sedes, inscripciones, ofertacursos  uso de modelos y logica de negocio
from app.models.curso import *
from app.models.asistenciaCurso import *
from app.models.sede import *
from app.models.cronogramaCurso import *
from datetime import datetime
from fastapi import HTTPException


########### LOGICA DE NEGOCIO CURSOS, SEDES Y OFERTAS ############


async def listar_cursos() -> List[Dict]:
    query = """
        SELECT idCurso, descripcion, duracion, precio, modalidad FROM cursos
    """
    result = await ejecutar_consulta_async(query, fetch=True)
    return result if result else []


async def obtener_curso_por_id(id_curso: int) -> Optional[Dict]:
    query = "SELECT * FROM cursos WHERE idCurso = ?"
    result = await ejecutar_consulta_async(query, (id_curso,), fetch=True)
    return result[0] if result else None

async def buscar_curso_por_nombre(nombre: str) -> List[Dict]:
    query = "SELECT idCurso, descripcion, duracion, precio FROM cursos WHERE descripcion LIKE ?"
    pattern = f"%{nombre}%"
    result = await ejecutar_consulta_async(query, (pattern,), fetch=True)
    return result if result else []


# Ver todas las sedes
async def listar_sedes() -> List[Dict]:
    query = "SELECT idSede, nombreSede FROM sedes"
    result = await ejecutar_consulta_async(query, fetch=True)
    return result if result else []


#Ver cursos de sede 
async def obtener_cursos_por_sede(id_sede: int) -> List[Dict]:
    query = """
        SELECT c.idCurso, c.descripcion, c.duracion, c.precio
        FROM cronogramaCursos cc
        JOIN cursos c ON cc.idCurso = c.idCurso
        WHERE cc.idSede = :id_sede
    """
    params = {"id_sede": id_sede}
    result = await ejecutar_consulta_async(query, params=params, fetch=True)
    return result if result else []

#Ver sedes por curso
async def obtener_sedes_por_curso(id_curso: int) -> List[Dict]:
    query = """
        SELECT s.idSede, s.nombreSede AS nombre, s.direccionSede AS direccion
        FROM cronogramaCursos cc
        JOIN sedes s ON cc.idSede = s.idSede
        WHERE cc.idCurso = ?
    """
    params = (id_curso,)
    result = await ejecutar_consulta_async(query, params=params, fetch=True)
    return result if result else []


#ver si alumno está inscrito a un curso
async def verificar_inscripcion_alumno(id_alumno: int, id_curso: int) -> bool:
    query = """
        SELECT 1 FROM asistenciaCursos 
        WHERE idAlumno = ? AND idCronograma IN (
            SELECT idCronograma FROM cronogramaCursos WHERE idCurso = ?
        )
    """
    params = (id_alumno, id_curso)
    result = await ejecutar_consulta_async(query, params=params, fetch=True)
    print(f"Verificando inscripción: {bool(result)}")
    return bool(result)

# Ver cronogramas de un curso (ofertas de un curso, con fechas y sede, vacantes)
async def obtener_ofertas_de_curso(id_curso: int) -> List[Dict]:
    query = """
        SELECT 
            s.nombreSede,
            s.direccionSede,
            cc.fechaInicio,
            cc.fechaFin,
            c.precio,
            s.bonificacionCursos,
            s.tipoPromocion,
            s.promocionCursos,
            cc.vacantesDisponibles
        FROM cronogramaCursos cc
        JOIN sedes s ON cc.idSede = s.idSede
        JOIN cursos c ON cc.idCurso = c.idCurso
        WHERE cc.idCurso = ?
    """
    params = (id_curso,)
    result = await ejecutar_consulta_async(query, params=params, fetch=True)
    print(result)
    return result if result else []

# Inscribir usuario a un cronograma
async def inscribir_alumno_a_curso(id_alumno: int, id_cronograma: int) -> Dict:
    # 1. Verificar si ya está inscrito
    query_check = """
        SELECT 1 FROM asistenciaCursos 
        WHERE idAlumno = ? AND idCronograma = ?
    """
    params = (id_alumno, id_cronograma)
    resultado = await ejecutar_consulta_async(query_check, params=params, fetch=True)

    if resultado:
        raise HTTPException(status_code=400, detail="El alumno ya está inscrito en este curso.")

    # 2. Insertar inscripción
    query_insert = """
        INSERT INTO asistenciaCursos (idAlumno, idCronograma)
        VALUES (?, ?)
    """
    await ejecutar_consulta_async(query_insert, params=params, fetch=False)

    # 3. Devolver confirmación
    return {
        "mensaje": "Alumno inscrito correctamente",
        "idAlumno": id_alumno,
        "idCronograma": id_cronograma
    }

# Darse de baja de un curso
async def dar_de_baja_alumno_de_curso(id_alumno: int, id_cronograma: int) -> Dict:
    # Verificar si existe la inscripción
    query_check = """
        SELECT 1 FROM asistenciaCursos 
        WHERE idAlumno = ? AND idCronograma = ?
    """
    params = (id_alumno, id_cronograma)
    resultado = await ejecutar_consulta_async(query_check, params=params, fetch=True)

    if not resultado:
        raise HTTPException(status_code=404, detail="El alumno no está inscrito en este curso.")

    # Borrar la inscripción / asistencias
    query_delete = """
        DELETE FROM asistenciaCursos 
        WHERE idAlumno = ? AND idCronograma = ?
    """
    await ejecutar_consulta_async(query_delete, params=params, fetch=False)

    return {
        "mensaje": "Alumno dado de baja correctamente",
        "idAlumno": id_alumno,
        "idCronograma": id_cronograma
    }