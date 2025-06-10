from fastapi import APIRouter, HTTPException, Depends
from app.models.curso import *
from app.services import curso_services
from app.services.auth_service import obtener_usuario_actual

router = APIRouter()


############ ENDPOINTS SEDES, CURSOS Y OFERTAS ############ 


#Ver todos los cursos 
@router.get("/curso")
async def get_all_cursos():
    try:
        return curso_services.obtener_todos_los_cursos()
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno")


#Ver un detalle curso por id 
@router.get("/curso/{id}")
async def get_curso(id: str, user=Depends(obtener_usuario_actual)):
    if user["tipo_usuario"] != "Alumno":
        raise HTTPException(status_code=403, detail="Acceso permitido solo a alumnos")
    elif user["tipo_usuario"] == "Alumno":
        curso =  curso_services.obtener_info_curso_por_id(id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
    else: 
        raise HTTPException(status_code=401, detail="Acceso no autorizado")
    return curso

#Ver  cursos por nombre 
@router.get("/curso/search/{nombre}")
async def get_curso_nombre(nombre: str):
    curso =  curso_services.obtener_info_curso_por_nombre(nombre)
    if not curso:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    
    return curso

"""
#Ver todas las ofertas de un curso 
@router.get("/curso/{id}/ofertas")
async def get_sedes_por_ofertas_id(id: str):
    try:
        return await curso_services.obtener_ofertas_por_cursos(id)
    except curso_services.OfertasNoExiste:
        raise HTTPException(status_code=404, detail="Oferta no encontradas")
    except curso_services.ParametroInvalido:
        raise HTTPException(status_code=400, detail="Parámetro inválido")

#Ver todas las sedes de un curso
@router.get("/curso/{id}/sedes")
async def get_sedes_por_curso_id(id: str):
    try:
        return await curso_services.obtener_sedes_por_curso(id)
    except Exception:
        raise HTTPException(status_code=404, detail="Sedes no encontrada")


#Ver todas las sedes 
@router.get("/sedes")
async def get_sedes():
    try:
        return await curso_services.obtener_sedes()
    except curso_services.SedeNoExiste:
        raise HTTPException(status_code=404, detail="Sedes no encontrada")

#Ver cursos de sede 
@router.get("/sedes/{id}")
async def get_cursos_por_sed(id: str):
    try:
        return await curso_services.obtener_cursos_por_sedes(id)
    except curso_services.SedeNoExiste:
        raise HTTPException(status_code=404, detail="Sedes no encontrada")



#Inscribirse a un curso
@router.post("/curso/{oferta_id}/alta")
async def inscribirse_curso(oferta_id: str, user=Depends(obtener_usuario_actual)):
    if user["tipo_usuario"].lower() != "alumno":
        raise HTTPException(status_code=403, detail="Solo los alumnos pueden inscribirse a cursos")
    print("Oferta ID:", oferta_id, "User ID:", user["_id"], "Oferta Type:", type(oferta_id), "User Type:", type(user["_id"]))
    resultado = await curso_services.inscribir_usuario_a_curso(user["_id"], oferta_id)
    return {"mensaje": "Inscripción exitosa", "resultado": resultado}



#Darse de baja de un curso 
@router.post("/curso/{inscripcion_id}/baja")
async def baja_curso(inscripcion_id: str, user=Depends(obtener_usuario_actual)):
    if user["tipo_usuario"] != "Alumno":
        raise HTTPException(status_code=401, detail="No autorizado")
    try:
        await curso_services.darse_de_baja(inscripcion_id)
        return {"mensaje": "Baja exitosa"}
    except curso_services.PlazoVencido:
        raise HTTPException(status_code=403, detail="Plazo vencido para darse de baja")
    except curso_services.NoInscripto:
        raise HTTPException(status_code=404, detail="No está inscripto en el curso")

"""