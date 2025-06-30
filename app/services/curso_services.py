# curso, sedes, inscripciones, ofertacursos  uso de modelos y logica de negocio
from app.models.curso import *
from app.models.asistenciaCurso import *
from app.models.sede import *
from app.models.cronogramaCurso import *
from datetime import datetime
from fastapi import HTTPException
from decimal import Decimal


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
        result = await ejecutar_consulta_async(query, fetch=True)
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

    result = await ejecutar_consulta_async(query, params=params, fetch=True)
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


################# SEDES ##################
# Ver todas las sedes
async def listar_sedes() -> List[Dict]:
    query = "SELECT idSede, nombreSede FROM sedes"
    result = await ejecutar_consulta_async(query, fetch=True)
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
    result = await ejecutar_consulta_async(query, params=params, fetch=True)
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
    result = await ejecutar_consulta_async(query, params=params, fetch=True)
    print(result)
    return result if result else []

# Inscribir usuario a un cronograma
async def inscribir_alumno_a_curso(id_alumno: int, id_cronograma: int, precio_abonado: float) -> Dict:
    precio_abonado = Decimal(precio_abonado)
    # 1. Verificar si ya está inscrito
    query_check = """
        SELECT 1 FROM asistenciaCursos 
        WHERE idAlumno = ? AND idCronograma = ?
    """
    params = (id_alumno, id_cronograma)
    resultado = await ejecutar_consulta_async(query_check, params=params, fetch=True)
    if resultado:
        raise HTTPException(status_code=400, detail="El alumno ya está inscrito en este curso.")

    # 2. Verificar vacantes disponibles
    query_vacantes = """
        SELECT vacantesDisponibles FROM cronogramaCursos WHERE idCronograma = ?
    """
    vacantes = await ejecutar_consulta_async(query_vacantes, params=(id_cronograma,), fetch=True)
    if not vacantes or vacantes[0]["vacantesDisponibles"] <= 0:
        raise HTTPException(status_code=400, detail="No hay vacantes disponibles para este curso.")

    # 3. Obtener saldo actual de la cuenta corriente
    query_saldo = "SELECT cuentaCorriente FROM alumnos WHERE idAlumno = ?"
    resultado_saldo = await ejecutar_consulta_async(query_saldo, params=(id_alumno,), fetch=True)
    if not resultado_saldo:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    saldo_actual = resultado_saldo[0].get('cuentaCorriente') or 0
    if not isinstance(saldo_actual, Decimal):
        saldo_actual = Decimal(saldo_actual)

    # 4. Calcular crédito usado y monto a cobrar con tarjeta
    credito_usado = min(saldo_actual, precio_abonado)
    monto_restante = precio_abonado - credito_usado

    # 5. Insertar inscripción
    query_insert = """
        INSERT INTO asistenciaCursos (idAlumno, idCronograma)
        VALUES (?, ?)
    """
    await ejecutar_consulta_async(query_insert, params=(id_alumno, id_cronograma), fetch=False)

    # 6. Disminuir vacantes en 1
    query_update_vacantes = """
        UPDATE cronogramaCursos
        SET vacantesDisponibles = vacantesDisponibles - 1
        WHERE idCronograma = ?
    """
    await ejecutar_consulta_async(query_update_vacantes, params=(id_cronograma,), fetch=False)

    # 7. Restar crédito usado de la cuenta corriente (solo si usa crédito)
    if credito_usado > 0:
        query_update_cuenta = """
            UPDATE alumnos
            SET cuentaCorriente = cuentaCorriente - ?
            WHERE idAlumno = ?
        """
        await ejecutar_consulta_async(query_update_cuenta, params=(credito_usado, id_alumno), fetch=False)

    # 8. Devolver confirmación con detalle de pagos
    return {
        "mensaje": "Alumno inscrito correctamente",
        "idAlumno": id_alumno,
        "idCronograma": id_cronograma,
        "creditoUsado": float(credito_usado),
        "montoRestante": float(monto_restante)  # Este monto debería cobrar la tarjeta
    }


async def dar_baja_alumno_de_curso(id_alumno: int, id_cronograma: int, precio_abonado: float) -> Dict:
    # 1. Verificar inscripción
    query_check = """
        SELECT 1 FROM asistenciaCursos 
        WHERE idAlumno = ? AND idCronograma = ?
    """
    params = (id_alumno, id_cronograma)
    resultado = await ejecutar_consulta_async(query_check, params=params, fetch=True)
    if not resultado:
        raise HTTPException(status_code=404, detail="El alumno no está inscrito en este curso.")

    # 2. Obtener fecha de inicio del curso
    query_fecha_inicio = """
        SELECT fechaInicio FROM cronogramaCursos WHERE idCronograma = ?
    """
    resultado_fecha = await ejecutar_consulta_async(query_fecha_inicio, params=(id_cronograma,), fetch=True)
    if not resultado_fecha:
        raise HTTPException(status_code=404, detail="No se encontró el cronograma del curso.")
    
    fecha_inicio = resultado_fecha[0]["fechaInicio"]

    from datetime import date
    hoy = date.today()
    dias_para_inicio = (fecha_inicio - hoy).days

    # 3. Calcular porcentaje de reintegro
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
    query_delete = """
        DELETE FROM asistenciaCursos 
        WHERE idAlumno = ? AND idCronograma = ?
    """
    await ejecutar_consulta_async(query_delete, params=params, fetch=False)

    # 5. Aumentar vacantes
    query_update_vacantes = """
        UPDATE cronogramaCursos
        SET vacantesDisponibles = vacantesDisponibles + 1
        WHERE idCronograma = ?
    """
    await ejecutar_consulta_async(query_update_vacantes, params=(id_cronograma,), fetch=False)

    # 6. Sumar a cuenta corriente si corresponde
    if monto_reintegro > 0:
        query_update_cc = """
            UPDATE alumnos
            SET cuentaCorriente = cuentaCorriente + ?
            WHERE idAlumno = ?
        """
        await ejecutar_consulta_async(query_update_cc, params=(monto_reintegro, id_alumno), fetch=False)

    return {
        "mensaje": "Baja exitosa",
        "montoReintegrado": float(monto_reintegro),
        "porcentajeReintegro": porcentaje_reintegro,
        "idAlumno": id_alumno,
        "idCronograma": id_cronograma
    }
