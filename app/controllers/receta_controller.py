from fastapi import APIRouter, HTTPException, status, Depends, Body, Path, Query, Form, UploadFile, File
from typing import Optional
from app.services import receta_service  
from app.models.receta import *
from app.models.calificacion import *
from app.services.auth_service import obtener_usuario_actual, obtener_usuario_actual_opcional



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
    return receta


#Verificar receta 


@router.post("/verificar/{nombre}")
async def verify_receta(nombre: str, user=Depends(obtener_usuario_actual)):
    try:
        resultado = await receta_service.verificar_receta(user["idUsuario"], nombre)
        if resultado["existe"]:
            raise HTTPException(
                status_code=409,
                detail={
                    "mensaje": "Receta ya existe",
                    "receta_id": resultado["receta_id"]
                }
            )
        return resultado
    except HTTPException as e:
        raise e  
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al verificar receta: {str(e)}")



######################################## CREACION, MODIF, Y REEMPLAZO RECETAS ########################################
#crear receta
@router.post("/", status_code=200)
async def post_receta(receta: RecetaIn,user=Depends(obtener_usuario_actual)):
    try:
        print(receta)
        id_receta = await receta_service.crear_receta_completa(receta, user["idUsuario"])
        print("✅ Receta creada con ID:", id_receta)
        return {
            "mensaje": "Receta creada correctamente",
            "idReceta": id_receta,  
        }
    except Exception as e:
        print("Error:", e)
        raise HTTPException(
            status_code=500, detail="Ocurrió un error al crear la receta"
        )
    

# Reemplazar receta
@router.put("/reemplazar/{idreceta_vieja}", status_code=200)
async def reemplazar_receta(idreceta_vieja: int, receta: RecetaIn, user=Depends(obtener_usuario_actual)):
    try:
        # 1. Crear la nueva receta
        nuevo_id_receta = await receta_service.crear_receta_completa(receta, user["idUsuario"])
        print(f"✅ Receta nueva creada con ID: {nuevo_id_receta}")

        # 2. Eliminar la receta vieja y sus relaciones
        eliminado = await receta_service.borrar_receta_completa(idreceta_vieja)
        if not eliminado:
            raise Exception(f"No se pudo eliminar la receta anterior con ID {idreceta_vieja}")
        print(f"🗑️ Receta vieja con ID {idreceta_vieja} eliminada correctamente")

        # 3. Retornar mensaje y nuevo ID
        return {
            "mensaje": "Receta reemplazada correctamente",
            "idReceta": nuevo_id_receta
        }

    except Exception as e:
        print(f"❌ Error al reemplazar receta: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error al reemplazar la receta")

# Actualizar receta
@router.put("/{id_receta}", status_code=200)
async def actualizar_receta(id_receta: int, receta: RecetaIn, user=Depends(obtener_usuario_actual)):
    try:
        actualizado = await receta_service.actualizar_receta_completa(id_receta, receta, user["idUsuario"])
        if not actualizado:
            raise Exception("La receta no pudo ser actualizada")

        return {
            "mensaje": "Receta actualizada correctamente",
            "idReceta": id_receta
        }

    except Exception as e:
        print(f"❌ Error al actualizar receta: {e}")
        raise HTTPException(status_code=500, detail="Ocurrió un error al actualizar la receta")

#### Subir fotos y multimedia a recetas####
@router.post("/{id_receta}/foto-principal")
async def subir_foto_principal(id_receta: int, archivo: UploadFile = File(...)):
    path = await receta_service.guardar_archivo(archivo)
    await receta_service.insertar_foto_principal(id_receta, path)
    return {"url": path}


@router.post("/{id_receta}/foto-adicional")
async def subir_foto_adicional(id_receta: int, archivo: UploadFile = File(...)):
    path = await receta_service.guardar_archivo(archivo)
    extension = archivo.filename.split(".")[-1]
    await receta_service.insertar_foto_adicional(id_receta, path, extension)
    return {"url": path}



@router.post("/{id_receta}/paso/{nro_paso}/media")
async def subir_multimedia_paso(id_receta: int, nro_paso: int, archivo: UploadFile = File(...)):
    nro_paso_real = nro_paso + 1  
    path = await receta_service.guardar_archivo(archivo)
    print(path)
    tipo = "video" if archivo.content_type.startswith("video") else "foto"
    extension = archivo.filename.split(".")[-1]
    await receta_service.insertar_multimedia_paso(id_receta, nro_paso_real, path, tipo, extension)
    return {
        "url": path,
        "tipo_contenido": tipo,
        "extension": extension
    }

#################################################

#obtener calificaciones de una receta
@router.get("/{id}/calificaciones", status_code=200)
async def get_calificaciones_receta(id: str = Path(...)):
    try:
        calificaciones = await receta_service.obtener_calificaciones_receta(id)
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