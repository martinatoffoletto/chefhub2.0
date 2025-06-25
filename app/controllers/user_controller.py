from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File
from app.services import user_services
from app.services.auth_service import obtener_usuario_actual
from app.models.usuario import Alumno
from app.services import receta_service  
router = APIRouter(prefix="/user", tags=["User"])


############# ENDPOINTS USUARIOS ############

## Ver info usuario
@router.get("/me")
async def get_current_user(current_user=Depends(obtener_usuario_actual)):
    print("Usuario actual:", current_user)
    return  current_user

#ver cursos de usuario
@router.get("/me/cursos")
async def get_user_cursos(current_user=Depends(obtener_usuario_actual)):
    if current_user["tipo_usuario"] != "Alumno":
        raise HTTPException(status_code=401, detail="No autorizado")
    cursos = await user_services.obtener_cursos_by_user_id(current_user)
    print("Cursos del usuario:", cursos)
    return cursos


##ver recetas favoritas de usuario
@router.get("/me/recetas_favoritas")
async def get_recetas_favoritas( current_user=Depends(obtener_usuario_actual)):
    recetas = await user_services.obtener_recetas_favoritas(current_user["idUsuario"])
    return recetas

#agregar receta favorita
@router.post("/me/recetas_favoritas/{receta_id}")
async def add_receta_favorita(receta_id,current_user=Depends(obtener_usuario_actual)):
    try:
        await user_services.agregar_receta_favorita(current_user["idUsuario"], receta_id)
    except user_services.RecetaYaFavoritaError:
        raise HTTPException(status_code=409, detail="Receta ya favorita")
    return {"msg": "Receta agregada a favoritos"}

#eliminar receta favorita
@router.delete("/me/recetas_favoritas/{receta_id}")
async def delete_receta_favorita(receta_id,current_user=Depends(obtener_usuario_actual)):
    try:
        await user_services.eliminar_receta_favorita(current_user["idUsuario"], receta_id)
    except user_services.RecetaNoFavoritaError:
        raise HTTPException(status_code=404, detail="Receta no favorita")
    return {"msg": "Receta eliminada de favoritos"}

#verificar receta favorita
@router.get("/me/recetas_favoritas/{receta_id}")
async def check_receta_favorita(receta_id, current_user=Depends(obtener_usuario_actual)):
    is_favorite = await user_services.verificar_receta_favorita(current_user["idUsuario"], receta_id)
    return {"is_favorite": is_favorite}


#ver notificaciones de usuario
@router.get("/me/notificaciones")
async def obtener_mis_notificaciones(current_user=Depends(obtener_usuario_actual)):
    notificaciones = await user_services.obtener_notificaciones_por_usuario(current_user["idUsuario"])
    print(notificaciones)
    return {"notificaciones": notificaciones}



#solicitar upgrade a alumno
@router.post("/me/upgrade_alumno")
async def upgrade_alumno(datos_alumno: dict, current_user=Depends(obtener_usuario_actual)):
    usuario = await user_services.upgradear_a_alumno(datos_alumno, current_user["idUsuario"])
    if not usuario:
        raise HTTPException(status_code=400, detail="No se pudo realizar el upgrade a alumno")
    return current_user



#imagenes dni
@router.post("/dni/upload")
async def subir_dni(
    campo: str,
    archivo: UploadFile = File(...),
    user=Depends(obtener_usuario_actual)
):
    path = await receta_service.guardar_archivo(archivo)
    await user_services.guardar_dni(user.id, path, campo)
    return {"url": path}



"""
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