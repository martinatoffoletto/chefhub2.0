from fastapi import APIRouter, HTTPException, status, Depends, Body, Path, Query
from app.services import user_services
from app.services.auth_service import obtener_usuario_actual
from app.models.usuario import Alumno
router = APIRouter(prefix="/user", tags=["User"])


############# ENDPOINTS USUARIOS ############

## Ver info usuario
@router.get("/me")
async def get_current_user(current_user=Depends(obtener_usuario_actual)):
    return await current_user

#ver cursos de usuario
@router.get("/me/cursos")
async def get_user_cursos(current_user=Depends(obtener_usuario_actual)):
    if current_user["tipo_usuario"] != "Alumno":
        raise HTTPException(status_code=401, detail="No autorizado")
    cursos = await user_services.obtener_cursos_by_user_id(current_user)
    return cursos


##ver recetas favoritas de usuario
@router.get("/me/recetas_favoritas")
async def get_recetas_favoritas( current_user=Depends(obtener_usuario_actual)):
    recetas = await user_services.obtener_recetas_favoritas(current_user)
    return recetas

#agregar receta favorita
@router.post("/me/recetas_favoritas/{receta_id}")
async def add_receta_favorita(receta_id,current_user=Depends(obtener_usuario_actual)):
    try:
        await user_services.agregar_receta_favorita(current_user["_id"], receta_id)
    except user_services.RecetaYaFavoritaError:
        raise HTTPException(status_code=409, detail="Receta ya favorita")
    return {"msg": "Receta agregada a favoritos"}

#eliminar receta favorita
@router.delete("/me/recetas_favoritas/{receta_id}")
async def delete_receta_favorita(receta_id,current_user=Depends(obtener_usuario_actual)):
    try:
        await user_services.eliminar_receta_favorita(current_user["_id"], receta_id)
    except user_services.RecetaNoFavoritaError:
        raise HTTPException(status_code=404, detail="Receta no favorita")
    return {"msg": "Receta eliminada de favoritos"}

"""
#solicitar upgrade a alumno
@router.post("/me/upgrade_alumno")
async def upgrade_alumno(datos_alumno,current_user=Depends(obtener_usuario_actual)):
    try:
        datos_alumno['idAlumno'] = current_user['idAlumno']
        await user_services.solicitar_upgrade_alumno(datos_alumno)
    except user_services.DatosInvalidosError:
        raise HTTPException(status_code=400, detail="Datos incompletos o inválidos")
    except user_services.YaEsAlumnoError:
        raise HTTPException(status_code=403, detail="Ya es alumno")
    return await obtener_usuario_actual()


#registrar asistencia
@router.post("/me/asistencia/{inscripcion_Id}")
async def register_asistence(inscripcion_Id):
    try:
        await user_services.registrar_asistencia()
    except user_services.CodigoInvalidoError:
        raise HTTPException(status_code=400, detail="Código inválido")
    except user_services.CursoOUsuarioNoExisteError:
        raise HTTPException(status_code=404, detail="Curso o usuario inexistente")
    except user_services.AsistenciaYaRegistradaError:
        raise HTTPException(status_code=409, detail="Ya registrada la asistencia")
    return {"msg": "Asistencia registrada"}
"""