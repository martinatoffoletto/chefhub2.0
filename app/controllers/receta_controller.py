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
    tipo: Optional[int] = None,
    usuario: Optional[int] = None,
    nombre: Optional[str] = None,
    contiene_ingrediente: Optional[int] = None,
    excluye_ingrediente: Optional[int] = None,
    sort: Optional[str] = Query("fecha"),  # 'fecha' o 'nombre'
    order: Optional[str] = Query("DESC"),  # 'ASC' o 'DESC'
    limit: Optional[int] = Query(None),     # Sin límite si no se pasa
    estado: Optional[str] = "aprobado",
    user=Depends(obtener_usuario_actual_opcional)
):
    try:
        recetas = await receta_service.obtener_recetas(
            tipo_receta=tipo,
            id_usuario=usuario,
            nombre=nombre,
            tiene_ingrediente=contiene_ingrediente,
            no_tiene_ingrediente=excluye_ingrediente,
            ordenar_por=sort,
            orden=order.upper(),
            limite=limit,
            state=estado
        )

        if user is not None:
            recetas_user = await receta_service.obtener_recetas(
                tipo_receta=tipo,
                id_usuario=user["idUsuario"],
                nombre=nombre,
                tiene_ingrediente=contiene_ingrediente,
                no_tiene_ingrediente=excluye_ingrediente,
                ordenar_por=sort,
                orden=order.upper(),
                limite=limit,
                state="todos"
            )

            # Filtrar recetas duplicadas (por idReceta) y que no sean del mismo usuario
            ids_user = {r["idReceta"] for r in recetas_user}
            recetas_aprobadas_otras = [
                r for r in recetas
                if r.get("idReceta") not in ids_user and r.get("idUsuario") != user["idUsuario"]
            ]

            return recetas_user + recetas_aprobadas_otras

        return recetas

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")


# Obtener todos los ingredientes (id y nombre)
@router.get("/ingredientes", status_code=200)
async def get_ingredientes():
    try:
        ingredientes = await receta_service.obtener_ingredientes()
        return ingredientes
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener ingredientes: {str(e)}")

# Obtener todos los tipos de receta (id y descripcion)
@router.get("/tipos", status_code=200)
async def get_tipos_receta():
    try:
        tipos = await receta_service.obtener_tipos_receta()
        return tipos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener tipos de receta: {str(e)}")
    


#Ver receta por id
@router.get("/{id}", status_code=200) 
async def get_receta_por_id(id: str = Path(...)):
    receta = await receta_service.obtener_por_id(id)
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