from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Body, Query
from app.services import user_services, receta_service
from app.services.auth_service import obtener_usuario_actual, obtener_usuario_actual_opcional
from app.models.usuario import DatosUpgradeAlumno
from typing import Optional
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
async def upgrade_alumno(datos: DatosUpgradeAlumno, current_user=Depends(obtener_usuario_actual_opcional),  ):

    if not current_user:
        if not datos.email:
            raise HTTPException(status_code=401, detail="Token o email requerido")
        current_user = await user_services.buscar_usuario_por_mail(datos.email)
        if not current_user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    
    datos_alumno = {
        "numeroTarjeta": datos.numeroTarjeta,
        "tramite": datos.tramite
    }

    usuario = await user_services.upgradear_a_alumno(datos_alumno, current_user["idUsuario"])
    if not usuario:
        raise HTTPException(status_code=400, detail="No se pudo realizar el upgrade a alumno")
    return current_user



#imagenes dni
@router.post("/dni/upload")
async def subir_dni(
    campo: str,
    archivo: UploadFile = File(...),
    user=Depends(obtener_usuario_actual_opcional),
    email: Optional[str] =Body(None)
):
    if not user:
        if not email:
            raise HTTPException(status_code=401, detail="Token o email requerido")
        user = await user_services.buscar_usuario_por_mail(email)
        if not user:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    print(user)
    path = await receta_service.guardar_archivo(archivo)
    await user_services.guardar_dni(user["idUsuario"], path, campo)
    return {"url": path}

@router.post("/me/asistencia")
async def registrar_asistencia_usuario(
    sede_id: int = Query(...) ,
    curso_id: int = Query(...) ,
    current_user=Depends(obtener_usuario_actual)
):
    try:
        return await user_services.registrar_asistencia_usuario(
            sede_id=sede_id,
            curso_id=curso_id,
            user=current_user
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
