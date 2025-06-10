# curso, sedes, iscripciones, ofertacursos  uso de modelos y logica de negocio
from app.models.curso import *
from app.models.asistenciaCurso import *
from app.models.sede import *
from app.models.cronogramaCurso import *
from datetime import datetime
print("curso_controller cargado")


########### LOGICA DE NEGOCIO CURSOS, SEDES Y OFERTAS ############

#Ver todos los cursos
def obtener_todos_los_cursos(): 
    cursos= listar_cursos()
    
    return cursos

#Ver un detalle curso por id
def obtener_info_curso_por_id(id):
    curso= obtener_curso_por_id(id)
    return {
        "id": str(curso.get("_id")),
        "nombre": curso.get("nombre"),
        "descripcion_completa": curso.get("descripcion_completa"),
        "temas": curso.get("temas"),
        "practicas": curso.get("practicas"),
        "insumos": curso.get("insumos"),
        "precio": curso.get("precio_base"),
        "imagen_curso_url": curso.get("imagen_curso_url")
    }
    
#ver cursos por nombre
async def obtener_info_curso_por_nombre(nombre):
    cursos=  buscar_curso_por_nombre(nombre)
    cursos_filtrados = []
    for curso in cursos:
        cursos_filtrados.append({
            "id": str(curso.get("_id")),
            "nombre": curso.get("nombre"),
            "descripcion_breve": curso.get("descripcion_breve"),
            "imagen_curso_url": curso.get("imagen_curso_url")
        })
    return cursos_filtrados

"""
#Ver todas las ofertas de un curso 
async def obtener_ofertas_por_cursos(id_curso):
    ofertas= await obtener_ofertas_por_curso(id_curso, get_ofertascursos_collection())
    ofertas_filtrados = []
    for oferta in ofertas:
        sede_info= await obtener_sede_por_id(str(oferta.get("sede_id")), get_sedes_collection())
        sede_info = {
            "id": str(sede_info.get("_id")),
            "nombre": sede_info.get("nombre"),
            "direccion": sede_info.get("direccion"),
            "telefono": sede_info.get("telefono"),
            "promocion": sede_info.get("promocion")
        }
        ofertas_filtrados.append({
            "sede_info": sede_info,
            "id": str(oferta.get("_id")),
            "fecha_inicio": oferta.get("fecha_inicio"),
            "fecha_fin": oferta.get("fecha_fin"),
            "modalidad": oferta.get("modalidad"),
            "horario": oferta.get("horario"),
            "vacantes": oferta.get("vacantes"),
            "precio_final": oferta.get("precio_final")
        }) 
    print("Ofertas filtradas:", ofertas_filtrados)
    return ofertas_filtrados

#ver todas las sedes de un curso
async def obtener_sedes_por_curso(id_curso):
    ofertas= await obtener_ofertas_por_curso(id_curso, get_ofertascursos_collection())
    sedes_filtradas = []
    for oferta in ofertas:
        sede_info= await obtener_sede_por_id(str(oferta.get("sede_id")), get_sedes_collection())
        if sede_info not in sedes_filtradas:
            sedes_filtradas.append({
                "id": str(sede_info.get("_id")),
                "nombre": sede_info.get("nombre"),
                "direccion": sede_info.get("direccion"),
                "telefono": sede_info.get("telefono"),
                "promocion": sede_info.get("promocion")
            })
    print("Sedes filtradas:", sedes_filtradas)
    return sedes_filtradas



#Ver todas las sedes 
async def obtener_sedes():
    sedes = await listar_sedes(get_sedes_collection())
    sedes_filtradas = []
    for sede in sedes:
        sedes_filtradas.append({
            "id": str(sede["_id"]),
            "nombre": sede.get("nombre"),
            "direccion": sede.get("direccion"),
            "telefono": sede.get("telefono"),
            "promocion": sede.get("promocion")
        })
    return sedes_filtradas

#Ver cursos de sede
async def obtener_cursos_por_sedes(id):
    cursos= await obtener_ofertas_por_sede(id, get_ofertascursos_collection())
    cursos_filtrados = []
    for curso in cursos:
        curso_info= await obtener_curso_por_id(str(curso.get("curso_id")), get_cursos_collection())
        if curso_info not in cursos_filtrados:
            cursos_filtrados.append({
            "id": str(curso_info["_id"]),
            "nombre": curso_info.get("nombre"),
            "descripcion_breve": curso_info.get("descripcion_breve"),
            "imagen_curso_url": curso_info.get("imagen_curso_url")
        })
    print("Cursos filtrados:", cursos_filtrados)
    return cursos_filtrados


#Inscribirse a un curso
async def inscribir_usuario_a_curso(user_id, oferta_id):
    inscripcion_obj = Inscripcion(
        alumno_id=user_id,
        oferta_id=oferta_id,
        fecha_inscripcion=datetime.now().isoformat(),
        asistencia=[]
    )
    oferta= await obtener_oferta_curso_por_id(oferta_id, get_ofertascursos_collection())
    if oferta.get("vacantes") < 30:
        inscripcion= await crear_inscripcion(inscripcion_obj, get_inscripciones_collection())
        await aumentar_vacantes(oferta_id, get_ofertascursos_collection())
        return inscripcion, oferta.get("vacantes")

#Darse de baja de un curso
async def darse_de_baja(inscripcion_id):
    await disminuir_vacantes(inscripcion_id, get_ofertascursos_collection())
    return await eliminar_inscripcion(inscripcion_id, get_inscripciones_collection())




    

"""