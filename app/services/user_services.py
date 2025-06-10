from app.models.usuario import *
from app.models.asistenciaCurso import *
from app.models.cronogramaCurso import *
from app.models.curso import *
from datetime import datetime

"""
#ver cursos de usuario
async def obtener_cursos_by_user_id(id_user):
    inscripciones=await obtener_inscripciones_por_alumno(id_user["_id"], get_inscripciones_collection())
    cursos=[]
    for inscripcion in inscripciones:
        oferta= await obtener_oferta_curso_por_id(str(inscripcion["oferta_id"]), get_ofertascursos_collection())
        curso= await obtener_curso_por_id(str(oferta["curso_id"]), get_cursos_collection())
        if curso:
            curso["_id"] = str(curso["_id"])
            cursoInscripcion = { 
                "inscripcion_id": str(inscripcion["_id"]),
                "oferta_id": str(oferta["_id"]),
                "curso_id": str(curso["_id"]),
                "nombre_curso": curso["nombre"],   
                "horario": oferta["horario"],
                "fecha_inicio": oferta["fecha_inicio"], 
                "fecha_fin": oferta["fecha_fin"],
                "sede_id": str(oferta["sede_id"]),
                "asistencia": inscripcion.get("asistencia", []),
                }       
            cursos.append(cursoInscripcion)
    return cursos

"""

def obtener_usuario_por_emaill():
   return buscar_usuario_por_id(1)
"""
#ver recetas favoritas de usuario
async def obtener_recetas_favoritas(id_user):
    usuario=await obtener_usuario_por_id(id_user["_id"], get_usuarios_collection())
    return usuario["favoritos"]

#agregar receta favorita
async def agregar_receta_favorita(id_user, receta_id):
    usuario= await agregar_lista(id_user, receta_id,"favoritos", get_usuarios_collection())

#Eliminar receta favorita
async def eliminar_receta_favorita(id_user, receta_id):
    usuario= await eliminar_lista(id_user, receta_id,"favoritos", get_usuarios_collection())


#solicitar upgrade a alumno
async def solicitar_upgrade_alumno(id_user,datos_alumno):
    usuario= await actualizar_usuario_a_alumno(id_user, datos_alumno, get_usuarios_collection())
    return usuario

async def regitrar_asistencia(inscripcion_id):
    asistencia=datetime.now().isoformat()
    await agregar_asistencia(inscripcion_id,asistencia, get_inscripciones_collection())

#ver usuario por id
async def obtene_usuario_por_id(id_user):
    usuario = await obtener_usuario_por_id(id_user, get_usuarios_collection())
    if not usuario:
        return None
    return {
        "id": str(usuario["_id"]),
        "alias": usuario["alias"],
        "email": usuario["email"],
        "tipo_usuario": usuario["tipo_usuario"],
        "avatar": usuario["avatar"],
        "favoritos": usuario["favoritos"]
    }"""