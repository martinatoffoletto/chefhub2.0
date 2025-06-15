from fastapi import APIRouter, HTTPException, status, Depends, Body, Path, Query
from typing import List, Optional
from app.services import receta_service  
from app.models.receta import *
from app.services.auth_service import obtener_usuario_actual, obtener_usuario_actual_opcional
from app.models.appError import AppError

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
    


#Ver receta por id
@router.get("/{id}", status_code=200) 
async def get_receta_por_id(id: str = Path(...)):
    receta = await receta_service.obtener_receta_detallada(id)
    if not receta:
        raise HTTPException(status_code=404, detail="Receta no encontrada")
    return receta

"""
#Verificar receta 
@router.post("/verificar/{nombre}")
async def verify_receta(nombre: str, user=Depends(obtener_usuario_actual)):
    try:
        return await receta_service.verificar_receta(nombre, user)
    except AppError as e:
        raise HTTPException(status_code=e.code, detail=e.message)

#crear receta
@router.post("/") ##FALTA QUE PASE LOS ARCHVIOS MULTIMEDIA QUE RECIBE. LOS BAJE A STATIC Y PONGA LA REFERENCIA EN LA RECETA
async def post_receta(receta: Receta, user=Depends(obtener_usuario_actual)):
    return await receta_service.crear_recetas(receta, user)
#reemplazar receta
@router.post("/reemplazar")
async def reemplazar_receta(receta: Receta, user=Depends(obtener_usuario_actual)):
    await receta_service.eliminar_receta_por_nombre_y_usuario(receta.nombre, user)
    return await receta_service.reemplazar_receta(receta, user)

#actualizar receta
@router.put("/{id}")
async def editar_receta( receta: Receta, user=Depends(obtener_usuario_actual), id: str = Path()):
    receta.estado = EstadoReceta.pendiente 
    await receta_service.actualizar_recetas(id, receta)
    return {"mensaje": "Receta actualizada. Queda pendiente de aprobación."}

"""