# curso, sedes, inscripciones, ofertacursos  uso de modelos y logica de negocio
from datetime import datetime,date
from fastapi import HTTPException
from decimal import Decimal
from typing import Optional, List, Dict
import app.config.db as db

########### LOGICA DE NEGOCIO CURSOS, SEDES Y OFERTAS ############


async def listar_cursos(
    id_sede: Optional[int] = None,
    en_curso: Optional[bool] = None
) -> List[Dict]:
    if id_sede is None and en_curso is None:
        # Caso simple: todos los cursos sin filtro
        query = """
            SELECT idCurso, descripcion, duracion, precio, modalidad FROM cursos
        """
        result = await db.ejecutar_consulta_async(query, fetch=True)
        return result if result else []

    # Caso con filtros: unimos cronogramas y cursos
    query = """
        SELECT c.idCurso, c.descripcion, c.duracion, c.precio, c.modalidad
        FROM cronogramaCursos cc
        JOIN cursos c ON cc.idCurso = c.idCurso
    """
    params = []

    if id_sede is not None:
        query += " WHERE cc.idSede = ?"
        params.append(id_sede)

    condicion_fecha = ""
    if en_curso is True:
        condicion_fecha = "cc.fechaInicio <= GETDATE() AND GETDATE() <= cc.fechaFin"
    elif en_curso is False:
        condicion_fecha = "GETDATE() < cc.fechaInicio"

    if condicion_fecha:
        if id_sede is not None:
            query += f" AND {condicion_fecha}"
        else:
            query += f" WHERE {condicion_fecha}"

    result = await db.ejecutar_consulta_async(query, params=params, fetch=True)
    return result if result else []

async def obtener_curso_por_id(id_curso: int) -> Optional[Dict]:
    query = "SELECT * FROM cursos WHERE idCurso = ?"
    result = await db.ejecutar_consulta_async(query, (id_curso,), fetch=True)
    return result[0] if result else None

async def buscar_curso_por_nombre(nombre: str) -> List[Dict]:
    query = "SELECT idCurso, descripcion, duracion, precio FROM cursos WHERE descripcion LIKE ?"
    pattern = f"%{nombre}%"
    result = await db.ejecutar_consulta_async(query, (pattern,), fetch=True)
    return result if result else []


################# SEDES ##################
# Ver todas las sedes
async def listar_sedes() -> List[Dict]:
    query = "SELECT idSede, nombreSede FROM sedes"
    result = await db.ejecutar_consulta_async(query, fetch=True)
    return result if result else []


# Ver sedes por curso
async def obtener_sedes_por_curso(id_curso: int) -> List[Dict]:
    query = """
        SELECT *
        FROM cronogramaCursos cc
        JOIN sedes s ON cc.idSede = s.idSede
        WHERE cc.idCurso = ?
    """
    params = (id_curso,)
    result = await db.ejecutar_consulta_async(query, params=params, fetch=True)
    return result if result else []


# Ver si alumno está inscrito a un curso
async def verificar_inscripcion_alumno(id_alumno: int, id_curso: int) -> bool:
    query = """
        SELECT 1 FROM asistenciaCursos 
        WHERE idAlumno = ? AND idCronograma IN (
            SELECT idCronograma FROM cronogramaCursos WHERE idCurso = ?
        )
    """
    params = (id_alumno, id_curso)
    result = await db.ejecutar_consulta_async(query, params=params, fetch=True)
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
            s.tipoBonificacion,
            s.tipoPromocion,
            s.promocionCursos,
            cc.idCronograma,
            cc.vacantesDisponibles
        FROM cronogramaCursos cc
        JOIN sedes s ON cc.idSede = s.idSede
        JOIN cursos c ON cc.idCurso = c.idCurso
        WHERE cc.idCurso = ?
    """
    params = (id_curso,)
    result = await db.ejecutar_consulta_async(query, params=params, fetch=True)
    print(result)
    return result if result else []

# Inscribir usuario a un cronograma
async def inscribir_alumno_a_curso(id_alumno: int, id_cronograma: int, precio_abonado: float) -> Dict:
    precio_abonado = Decimal(precio_abonado)

    async with db.pool.acquire() as conn:
        # 1. Verificar inscripción
        query_check = """
            SELECT 1 FROM asistenciaCursos 
            WHERE idAlumno = ? AND idCronograma = ?
        """
        resultado = await db.ejecutar_consulta_async(query_check, (id_alumno, id_cronograma), fetch=True, external_conn=conn)
        if resultado:
            raise HTTPException(status_code=400, detail="El alumno ya está inscrito en este curso.")

        # 2. Verificar vacantes
        query_vacantes = "SELECT vacantesDisponibles FROM cronogramaCursos WHERE idCronograma = ?"
        vacantes = await db.ejecutar_consulta_async(query_vacantes, (id_cronograma,), fetch=True, external_conn=conn)
        if not vacantes or vacantes[0]["vacantesDisponibles"] <= 0:
            raise HTTPException(status_code=400, detail="No hay vacantes disponibles.")

        # 3. Obtener cuenta corriente
        query_saldo = "SELECT cuentaCorriente FROM alumnos WHERE idAlumno = ?"
        resultado_saldo = await db.ejecutar_consulta_async(query_saldo, (id_alumno,), fetch=True, external_conn=conn)
        if not resultado_saldo:
            raise HTTPException(status_code=404, detail="Alumno no encontrado")

        saldo_actual = resultado_saldo[0].get('cuentaCorriente') or 0
        if not isinstance(saldo_actual, Decimal):
            saldo_actual = Decimal(saldo_actual)

        credito_usado = min(saldo_actual, precio_abonado)
        monto_restante = precio_abonado - credito_usado

        # 5. Insertar inscripción
        await db.ejecutar_consulta_async(
            "INSERT INTO asistenciaCursos (idAlumno, idCronograma) VALUES (?, ?)",
            (id_alumno, id_cronograma), external_conn=conn
        )

        # 6. Actualizar vacantes
        await db.ejecutar_consulta_async(
            "UPDATE cronogramaCursos SET vacantesDisponibles = vacantesDisponibles - 1 WHERE idCronograma = ?",
            (id_cronograma,), external_conn=conn
        )

        # 7. Restar crédito si corresponde
        if credito_usado > 0:
            await db.ejecutar_consulta_async(
                "UPDATE alumnos SET cuentaCorriente = cuentaCorriente - ? WHERE idAlumno = ?",
                (credito_usado, id_alumno), external_conn=conn
            )

        return {
            "mensaje": "Alumno inscrito correctamente",
            "idAlumno": id_alumno,
            "idCronograma": id_cronograma,
            "creditoUsado": float(credito_usado),
            "montoRestante": float(monto_restante)
        }


async def dar_baja_alumno_de_curso(id_alumno: int, id_cronograma: int, precio_abonado: float) -> Dict:
    async with db.pool.acquire() as conn:
        # 1. Verificar inscripción
        query_check = "SELECT 1 FROM asistenciaCursos WHERE idAlumno = ? AND idCronograma = ?"
        resultado = await db.ejecutar_consulta_async(query_check, (id_alumno, id_cronograma), fetch=True, external_conn=conn)
        if not resultado:
            raise HTTPException(status_code=404, detail="El alumno no está inscrito en este curso.")

        # 2. Obtener fecha de inicio
        query_fecha = "SELECT fechaInicio FROM cronogramaCursos WHERE idCronograma = ?"
        resultado_fecha = await db.ejecutar_consulta_async(query_fecha, (id_cronograma,), fetch=True, external_conn=conn)
        if not resultado_fecha:
            raise HTTPException(status_code=404, detail="No se encontró el cronograma.")

        fecha_inicio = resultado_fecha[0]["fechaInicio"]
        hoy = date.today()
        dias_para_inicio = (fecha_inicio - hoy).days

        if dias_para_inicio > 10:
            porcentaje_reintegro = 100
        elif 1 <= dias_para_inicio <= 9:
            porcentaje_reintegro = 70
        elif dias_para_inicio == 0:
            porcentaje_reintegro = 50
        else:
            porcentaje_reintegro = 0

        monto_reintegro = precio_abonado * (porcentaje_reintegro / 100)

        # 4. Eliminar inscripción
        await db.ejecutar_consulta_async(
            "DELETE FROM asistenciaCursos WHERE idAlumno = ? AND idCronograma = ?",
            (id_alumno, id_cronograma), external_conn=conn
        )

        # 5. Liberar vacante
        await db.ejecutar_consulta_async(
            "UPDATE cronogramaCursos SET vacantesDisponibles = vacantesDisponibles + 1 WHERE idCronograma = ?",
            (id_cronograma,), external_conn=conn
        )

        # 6. Devolver dinero si corresponde
        if monto_reintegro > 0:
            await db.ejecutar_consulta_async(
                "UPDATE alumnos SET cuentaCorriente = cuentaCorriente + ? WHERE idAlumno = ?",
                (monto_reintegro, id_alumno), external_conn=conn
            )

        return {
            "mensaje": "Baja exitosa",
            "montoReintegrado": float(monto_reintegro),
            "porcentajeReintegro": porcentaje_reintegro,
            "idAlumno": id_alumno,
            "idCronograma": id_cronograma
        }