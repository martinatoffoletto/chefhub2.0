# curso, sedes, inscripciones, ofertacursos  uso de modelos y logica de negocio
from app.models.curso import *
from app.models.asistenciaCurso import *
from app.models.sede import *
from app.models.cronogramaCurso import *
from datetime import datetime


########### LOGICA DE NEGOCIO CURSOS, SEDES Y OFERTAS ############

# Ver todos los cursos
async def obtener_todos_los_cursos():
    cursos = await listar_cursos()
    return cursos

# Ver un detalle curso por id
async def obtener_info_curso_por_id(id):
    curso = await obtener_curso_por_id(id)
    return curso if curso else None

# Ver cursos por nombre
async def obtener_info_curso_por_nombre(nombre):
    cursos = await buscar_curso_por_nombre(nombre)
    return cursos if cursos else None

# Ver todas las sedes
async def obtener_sedes():
    sedes = await listar_sedes()
    return sedes


#Ver cursos de sede 
async def obtener_cursos_por_sedes(id_sede):
    cronogramas_id = await obtener_cronogramas_por_sede(id_sede)
    cursos=[]
    for cronograma_id in cronogramas_id:
        curso = await obtener_curso_por_id(cronograma_id['idCurso'])
        if curso:
            cursos.append(curso)
    return cursos 

#Ver sedes por curso
async def obtener_sedes_por_curso(id_curso):
    cronogramas = await obtener_cronogramas_por_curso(id_curso)
    sedes = []
    for cronograma in cronogramas:
        sede = await obtener_sede_por_id(cronograma['idSede'])
        if sede:
            sedes.append(sede)
    return sedes

# Ver cronogramas de un curso (es decir ver las ofertas de un curso, con fechas y sede, vacantes)
async def obtener_ofertas_por_curso(id_curso):
    cronogramas = await obtener_cronogramas_por_curso(id_curso)
    return cronogramas


# Inscribir usuario a un cronograma
async def inscribir_usuario_a_cronograma(id_alumno, id_cronograma, fecha=None):
    asistencia = AsistenciaCursos(
        idAlumno=id_alumno,
        idCronograma=id_cronograma,
        fecha=fecha or datetime.now()
    )
    return await crear_asistencia(asistencia)

# Darse de baja de un cronograma
async def darse_de_baja(id_alumno, id_cronograma):
    return await eliminar_inscripcion(id_alumno, id_cronograma)