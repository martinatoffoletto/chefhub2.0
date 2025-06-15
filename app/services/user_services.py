from app.models.usuario import *
from app.models.asistenciaCurso import *
from app.models.cronogramaCurso import *
from app.models.curso import *
from datetime import datetime


#
# Obtener el nickname de un usuario por su ID
async def obtener_nickname_por_id(id_usuario: int) -> Optional[str]:
    query = "SELECT nickname FROM usuarios WHERE idUsuario = ?"
    resultado = await ejecutar_consulta_async(query, [id_usuario], fetch=True)
    return resultado[0]["nickname"] if resultado else None


# Ver recetas favoritas de usuario
async def obtener_recetas_favoritas(id_user):
    usuario = await obtener_usuario_por_id(id_user["_id"])
    return usuario["favoritos"] if usuario and "favoritos" in usuario else []

# Agregar receta favorita
async def agregar_receta_favorita(id_user, receta_id):
    usuario = await agregar_lista(id_user, receta_id, "favoritos")
    return usuario

# Eliminar receta favorita
async def eliminar_receta_favorita(id_user, receta_id):
    usuario = await eliminar_lista(id_user, receta_id, "favoritos")
    return usuario

# Solicitar upgrade a alumno
async def solicitar_upgrade_alumno(alumno: Alumno):
    usuario = await upgradear_a_alumno(alumno)
    print("Usuario actualizado:", alumno)
    return usuario

# Registrar asistencia
async def regitrar_asistencia(inscripcion_id):
    asistencia = datetime.now().isoformat()
    await agregar_asistencia(inscripcion_id, asistencia)

# Ver usuario por id
async def obtene_usuario_por_id(id_user):
    usuario = await obtener_usuario_por_id(id_user)
    if not usuario:
        return None
    return {
        "id": str(usuario["idUsuario"]),
        "alias": usuario.get("nickname") or usuario.get("alias"),
        "email": usuario.get("mail") or usuario.get("email"),
        "tipo_usuario": usuario.get("tipo_usuario"),
        "avatar": usuario.get("avatar"),
        "favoritos": usuario.get("favoritos", [])
    }