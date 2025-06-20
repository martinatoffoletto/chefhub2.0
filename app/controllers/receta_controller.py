from fastapi import APIRouter, HTTPException, status, Depends, Body, Path, Query, UploadFile, File
from typing import List, Optional
from app.services import receta_service  
from app.models.receta import *
from app.models.calificacion import *
from app.services.auth_service import obtener_usuario_actual, obtener_usuario_actual_opcional
from app.models.appError import AppError
import shutil
import uuid, os

router = APIRouter(prefix="/recetas", tags=["Recetas"])

############ ENDPOINTS RECETAS ############

# Ver todas las recetas con filtros, límites y orden
@router.get("/", status_code=200)
async def get_recetas(
    ordenar_por: str = Query("nombre", regex="^(nombre|reciente|usuario)$"),
    nickname: Optional[str] = Query(None),
    id_ingrediente_incluye: Optional[int] = Query(None),
    id_ingrediente_excluye: Optional[int] = Query(None),
    id_tipo: Optional[int] = Query(None),
    nombre_receta: Optional[str] = Query(None),
    limite: Optional[int] = Query(None),
    user = Depends(obtener_usuario_actual_opcional)
):
    id_usuario_logueado = user["idUsuario"] if user else None
    recetas = await receta_service.listar_recetas(
        ordenar_por=ordenar_por,
        nickname=nickname,
        id_ingrediente_incluye=id_ingrediente_incluye,
        id_ingrediente_excluye=id_ingrediente_excluye,
        id_tipo=id_tipo,
        id_usuario_logueado=id_usuario_logueado,
        nombre_receta=nombre_receta,
        limite=limite
    )
    return recetas





# Obtener todos los ingredientes (id y nombre)
@router.get("/ingredientes", status_code=200)
async def get_ingredientes():
    try:
        ingredientes = await receta_service.listar_ingredientes()
        return ingredientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ingredientes: {str(e)}")


# Obtener todos los tipos de receta (id y descripcion)
@router.get("/tipos", status_code=200)
async def get_tipos_receta():
    try:
        tipos = await receta_service.listar_tipos_receta()
        return tipos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tipos de receta: {str(e)}")

#obtener todas las unidades (id y descripcion)
@router.get("/unidades", status_code=200)   
async def get_unidades():
    try:
        unidades = await receta_service.listar_unidades()
        return unidades
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener unidades: {str(e)}")

#obtener tabla conversiones
@router.get("/conversiones", status_code=200)
async def get_conversiones():
    try:
        conversiones = await receta_service.listar_conversiones()
        return conversiones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener conversiones: {str(e)}")
    
#Ver receta por id
@router.get("/{id}", status_code=200) 
async def get_receta_por_id(id: str = Path(...)):
    receta = await receta_service.obtener_receta_detallada(id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    print(receta)
    return receta


#Verificar receta 
@router.post("/verificar/{nombre}")
async def verify_receta(nombre: str, user=Depends(obtener_usuario_actual)):
    try:
        return await receta_service.verificar_receta(user["idUsuario"], nombre)
    except AppError as e:
        raise HTTPException(status_code=e.code, detail=e.message)


#crear receta
@router.post("/")
async def post_receta(
    receta: CrearRecetaRequest,
    user=Depends(obtener_usuario_actual)
):
    try:
        id_receta = await receta_service.crear_receta_completa(receta, user["idUsuario"])
        return {"mensaje": "Receta creada correctamente", "idReceta": id_receta}
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Ocurrió un error al crear la receta")

#reemplazar receta
@router.put("/reemplazar/{id_receta_antigua}")
async def reemplazar_receta(id_receta_antigua: int, data: CrearRecetaRequest, user=Depends(obtener_usuario_actual)):
    try:
        print("Reemplazando receta:")
        id_nueva = await receta_service.crear_receta_completa(data, user["idUsuario"])
        await receta_service.borrar_receta_completa(id_receta_antigua, user["idUsuario"])
        return {"mensaje": "Receta reemplazada correctamente", "idNuevaReceta": id_nueva}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

#actualizar receta
@router.put("/{id_receta}")
async def actualizar_receta(
    id_receta: int,
    data: CrearRecetaRequest,
    user=Depends(obtener_usuario_actual)
):
    print("payload", data)
    try:
        await receta_service.actualizar_receta_completa(id_receta, data, user["idUsuario"])
        return {"mensaje": "Receta actualizada correctamente", "idReceta": id_receta}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


########## Configuración para manejo de multimedia ################
UPLOAD_FOLDER = "static/img"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@router.post("/upload/")
async def upload_media(file: UploadFile = File(...)):
    extension = file.filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{extension}"
    file_location = f"{UPLOAD_FOLDER}/{filename}"

    try:
        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception:
        raise HTTPException(status_code=500, detail="Error guardando archivo")

    url = f"img/{filename}"
    return {"url": url}

######################################################################



#obtener calificaciones de una receta
@router.get("/{id}/calificaciones", status_code=200)
async def get_calificaciones_receta(id: str = Path(...), user=Depends(obtener_usuario_actual_opcional)):
    try:
        calificaciones = await receta_service.obtener_calificaciones_receta(id,user["idUsuario"] if user else None)
        return calificaciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener calificaciones: {str(e)}")

#calificar receta
@router.post("/{id}/calificar")
async def calificar_receta_endpoint(
    calificacion: Calificacion,
    id: str = Path(...),
    user=Depends(obtener_usuario_actual)
):
    if user is None:
        raise HTTPException(status_code=401, detail="No autorizado")

    resultado = await receta_service.calificar_receta(id, user["idUsuario"], calificacion)

    if resultado.get("error"):
        raise HTTPException(status_code=resultado.get("code", 400), detail=resultado["error"])

    return {"mensaje": "Receta calificada correctamente"}