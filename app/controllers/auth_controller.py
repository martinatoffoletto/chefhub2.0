from fastapi import APIRouter, HTTPException, status, Depends, Body
from app.services import auth_service
from app.services.auth_service import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from pydantic import BaseModel
import redis
import random
import json
from app.models.usuario import Usuario
from app.models.usuario import Alumno

redis_client = redis.Redis(host='localhost', port=6379, db=0)
router = APIRouter()

@router.post("/auth/login")
async def login(email: str = Body(...), password: str = Body(...)):
    resultado = await auth_service.autenticar_usuario(email, password)
    if resultado is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

    return resultado


class RefreshTokenRequest(BaseModel):
    refresh_token: str


@router.post("/auth/refresh")
async def refresh_token(body: RefreshTokenRequest):
    try:
        payload = jwt.decode(body.refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Token inválido")
        
        usuario = await auth_service.buscar_usuario_por_id(int(user_id))
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        tipo_usuario = "Alumno" if usuario.get("numeroTarjeta") else "Usuario"
        usuario["tipo_usuario"] = tipo_usuario

        access_token, new_refresh_token = auth_service.crear_tokens(usuario)
        return {"access_token": access_token, "refresh_token": new_refresh_token}

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
    

@router.post('/register/first-step')
async def register_first_step(username: str=Body(...), email: str=Body(...)):
    try:
        already_registered = await auth_service.buscar_usuario_por_mail(email)
        if already_registered:
            raise HTTPException(status_code=403, detail="Email ya registrado")

        is_available = await auth_service.validar_alias(username=username)
        if not is_available:
            raise HTTPException(status_code=403, detail="Alias no disponible")

        codigo = f"{random.randint(1000, 9999)}"
        email_sent = await auth_service.enviar_codigo_mail(email=email, codigo=codigo)
        if not email_sent:
            raise HTTPException(status_code=500, detail="Error enviando el código")

        datos_temporales = {
            "alias": username,
            "email": email,
            "codigo": codigo
        }

        redis_client.set(f"registro_temp:{email}", json.dumps(datos_temporales), ex=86400)

        return {"status": "ok", "message": "Código enviado al mail"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en registro primer paso: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")

    
@router.post('/register/code-verification')
async def verify_code(email: str=Body(...), code:str=Body(...)):
    try:
        data_raw = redis_client.get(f"registro_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=403, detail="Código no encontrado o expirado")

        data = json.loads(data_raw)
        if data.get("codigo") != code:
            raise HTTPException(status_code=403, detail="Código inválido")

        return {"status": "ok", "message": "Código validado correctamente"}
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en validación de código: {e}")
        raise HTTPException(status_code=500, detail="Error en la validación de código")


@router.post("/register/create-password")
async def create_password(password: str = Body(...), email:str=Body(...)):
    try:
        success = await auth_service.create_password(password, email)
        if not success:
            raise HTTPException(status_code=500, detail="Error creando la contraseña")

        data_raw = redis_client.get(f"registro_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=404, detail="Datos temporales no encontrados")

        data = json.loads(data_raw) 
        data["password"] = password #podemos guardar la contra hasheada, esto es temporal

        redis_client.set(f"registro_temp:{email}", json.dumps(data), ex=86400)

        return {"status": "ok", "message": "Contraseña creada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creando contraseña: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
@router.post('/register/avatar')
async def chosen_avatar(email:str=Body(...), avatar:int=Body(...)):
    try:
        data_raw = redis_client.get(f"registro_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=404, detail="Datos temporales no encontrados")

        data = json.loads(data_raw)
        data["avatar"]=avatar

        redis_client.set(f"registro_Temp:{email}", json.dumps(data), ex=86400)

        return {"status": "ok", "message": "Avatar asignado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creando avatar: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")

    
@router.post('/register/tipo_usuario')
async def create_user(email:str=Body(...), password:str=Body(...), tipo_usuario:str=Body(...)):
    try:
        data_raw=redis_client.get(f"registro_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=404, detail="Datos temporales no encontrados")
        
        data=json.loads(data_raw)
        data["tipo_usuario"] = tipo_usuario 

        if tipo_usuario == "usuario":
            usuario = Usuario(
                mail=data["email"],
                nickname=data["alias"],
                habilitado='Si',
                avatar=data.get("avatar", "")
            )
            id_user = await auth_service.create_user(usuario, password)

 
            redis_client.delete(f"registro_temp:{email}")

            return {"status": "ok", "idUsuario": id_user}

        elif tipo_usuario == "alumno":

            usuario=Usuario(
            mail=data["email"],
            nickname=data["alias"],
            habilitado='Si',
            avatar=data.get("avatar", "")
            )

            id_user = await auth_service.create_user(usuario, password)
            data["id_usuario"] = id_user

            for key, value in data.items():
                if isinstance(value, set):
                    data[key] = list(value)

            redis_client.set(f"registro_temp:{email}", json.dumps(data), ex=86400)
            
            return {
                "status": "pendiente_datos",
                "message": f"Se requiere información adicional para tipo alumno, idUsuario: {id_user}"
            }

        else:
            raise HTTPException(status_code=400, detail="Tipo de usuario inválido")
        
    except Exception as e:
        print(f"Error creando usuario: {e}")
        raise HTTPException(status_code=500, detail="Error creando usuario")

@router.post("/register/payment-method")
async def payment_method(email: str=Body(...), card_number: str=Body(...), complete_name: str =Body(...), expire_date: str=Body(...), cvv: str=Body(...)):
    try:
        data_raw=redis_client.get(f"registro_temp:{email}")
        print(f"Buscando registro temporal para email: {email}, encontrado: {data_raw}")
        if not data_raw:
            raise HTTPException(status_code=404, detail="Datos temporales no encontrados")
        
        data=json.loads(data_raw)
        last_four=card_number[-4:]
        data["payment_method"]={
            "card_number":last_four,
            "complete_name": complete_name,
            "expire_date": expire_date
        }

        redis_client.set(f"registro_temp:{email}", json.dumps(data), ex=86400)
        return {"status": "ok", "message": "Método de pago registrado temporalmente"}
    
    except Exception as e:
        print(f"Error guardando método de pago: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")


@router.post("/register/personal-data")
async def personal_data(email:str=Body(...), frontDNI:str=Body(...), backDNI: str=Body(...), nro_tramite: str=Body(...)):
    try:
        data_raw=redis_client.get(f"registro_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=404, detail="Datos temporales no encontrados")
        
        data=json.loads(data_raw)
        data["pesonal_data"]={
            "front_dni": frontDNI,
            "back_dni":backDNI,
            "nro_tramite":nro_tramite
        }

        redis_client.set(f"registro_temp:{email}", json.dumps(data), ex=86400)

        if data.get("tipo_usuario") != "alumno" or not data.get("id_usuario"):
            raise HTTPException(status_code=400, detail="Usuario no válido para completar como alumno")

        alumno = Alumno(
            idAlumno=data["id_usuario"],
            numeroTarjeta=data["payment_method"]["card_number"],
            dniFrente=frontDNI,
            dniFondo=backDNI,
            tramite=nro_tramite,
            cuentaCorriente=0.0
        )
        await auth_service.create_student(alumno)

        redis_client.delete(f"registro_temp:{email}")

        return {"status": "ok", "message": "Alumno creado correctamente"}
        
    except Exception as e:
        print(f"Error finalizando registro de alumno: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
@router.put("/forgot_password")
async def forgot_password():
    return {"message": "Forgot password endpoint"}

@router.get("/alias_sugerido")
async def alias_sugerido():
    return {"message": "Alias sugerido endpoint"}
