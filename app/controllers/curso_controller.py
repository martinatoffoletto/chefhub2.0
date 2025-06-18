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
        return await curso_services.listar_cursos()
    except Exception:
        raise HTTPException(status_code=500, detail="Error interno")


#Ver un detalle curso por id 
@router.get("/curso/{id}")
async def get_curso(id: str, user=Depends(obtener_usuario_actual)):
    if user["tipo_usuario"] != "Alumno":
        raise HTTPException(status_code=403, detail="Acceso permitido solo a alumnos")
    elif user["tipo_usuario"] == "Alumno":
        curso =  await curso_services.obtener_curso_por_id(id)
        if not curso:
            raise HTTPException(status_code=404, detail="Curso no encontrado")
    else: 
        raise HTTPException(status_code=401, detail="Acceso no autorizado")
    return curso

#Ver  cursos por nombre 
@router.get("/curso/search/{nombre}")
async def get_curso_nombre(nombre: str):
    curso = await curso_services.buscar_curso_por_nombre(nombre)   
    return curso



#Ver todas las sedes 
@router.get("/sedes")
async def get_sedes():
    try:
        return await curso_services.listar_sedes()
    except Exception:
        raise HTTPException(status_code=404, detail="Sedes no encontrada")

#Ver cursos de sede 
@router.get("/sedes/{id}")
async def get_cursos_por_sed(id: str):
    try:
        return await curso_services.obtener_cursos_por_sede(id)
    except Exception:
        raise HTTPException(status_code=404, detail="Sedes no encontrada")

#Ver todas las sedes de un curso
@router.get("/curso/{id}/sedes")
async def get_sedes_por_curso_id(id: str):
    try:
        return await curso_services.obtener_sedes_por_curso(id)
    except Exception:
        raise HTTPException(status_code=404, detail="Sedes no encontrada")


#Ver si un alumno está inscrito a un curso
@router.get("/curso/{id}/inscripcion")
async def verificar_inscripcion(id: str, user=Depends(obtener_usuario_actual)):
    if user["tipo_usuario"] != "Alumno":
        raise HTTPException(status_code=403, detail="Acceso permitido solo a alumnos")
    try:
        inscripto = await curso_services.verificar_inscripcion_alumno(user["idUsuario"], id)
        return {"inscripto": inscripto}
    except curso_services.CursoNoExiste:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    except curso_services.ParametroInvalido:
        raise HTTPException(status_code=400, detail="Parámetro inválido")

#Ver todas las ofertas de un curso 
@router.get("/curso/{id}/ofertas")
async def get_ofertas_por_curso(id: str):
    try:
        return await curso_services.obtener_ofertas_de_curso(id)
    except curso_services.OfertasNoExiste:
        raise HTTPException(status_code=404, detail="Oferta no encontradas")
    except curso_services.ParametroInvalido:
        raise HTTPException(status_code=400, detail="Parámetro inválido")




#Inscribirse a un curso
@router.post("/curso/{id_cronograma}/alta")
async def inscribirse_curso(id_cronograma: str, user=Depends(obtener_usuario_actual)):
    if user["tipo_usuario"].lower() != "alumno":
        raise HTTPException(status_code=403, detail="Solo los alumnos pueden inscribirse a cursos")
    resultado = await curso_services.inscribir_alumno_a_curso(user["idUsuario"], id_cronograma)
    return {"mensaje": "Inscripción exitosa", "resultado": resultado}



#Darse de baja de un curso 
@router.post("/curso/{id_cronograma}/baja")
async def baja_curso(id_cronograma: str, user=Depends(obtener_usuario_actual)):
    if user["tipo_usuario"] != "Alumno":
        raise HTTPException(status_code=401, detail="No autorizado")

    await curso_services.dar_baja_alumno_de_curso(user["idUsuario"], id_cronograma)
    return {"mensaje": "Baja exitosa"}


