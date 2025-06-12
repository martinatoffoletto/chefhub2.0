from fastapi import APIRouter, HTTPException, status, Depends, Body
from app.services import auth_service
from app.services.auth_service import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from pydantic import BaseModel
import redis
import random
import bcrypt
import json
from app.models.usuario import Usuario

redis_client = redis.Redis(host='localhost', port=6379)
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

        await redis.set(f"registro_temp:{email}", json.dumps(datos_temporales), ex=86400)

        return {"status": "ok", "message": "Código enviado al mail"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error en registro primer paso: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")

    
@router.post('/register/code-verification')
async def verify_code(email: str=Body(...), code:str=Body(...)):
    try:
        data_raw = await redis.get(f"registro_temp:{email}")
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


@router.post("/register/create.password")
async def create_password(password: str = Body(...), email:str=Body(...)):
    try:
        success = await auth_service.create_password(password, email)
        if not success:
            raise HTTPException(status_code=500, detail="Error creando la contraseña")

        data_raw = await redis.get(f"registro_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=404, detail="Datos temporales no encontrados")

        data = json.loads(data_raw)
        data["password"] = password #podemos guardar la contra hasheada, esto es temporal

        await redis.set(f"registro_temp:{email}", json.dumps(data), ex=86400)

        return {"status": "ok", "message": "Contraseña creada correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creando contraseña: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")
    
@router.post('/register/avatar')
async def chosen_avatar(email:str=Body(...), avatar:int=Body(...)):
    try:
        data_raw = await redis.get(f"registro_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=404, detail="Datos temporales no encontrados")

        data = json.loads(data_raw)
        data["avatar"]=avatar

        await redis.set(f"registro_Temp:{email}", json.dumps(data), ex=86400)

        return {"status": "ok", "message": "Avatar asignado correctamente"}

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error creando avatar: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")

    
@router.post('/register/tipo_usuario')
async def create_user(email:str=Body(...), password:str=Body(...)):
    try:
        data_raw=await redis.get(f"registro_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=404, detail="Datos temporales no encontrados")
        
        data=json.loads(data_raw)

        usuario = Usuario(
            mail = data['mail'],
            nickname = data['nickname'],
            habilitado = True,
            avatar = data.get('avatar', '')
        )

        id_user = await auth_service.create_user(usuario, password)

        return {"status": "ok", "idUsuario": id_user}

    except Exception as e:
        print(f"Error creando usuario: {e}")
        raise HTTPException(status_code=500, detail="Error creando usuario")

@router.put("/forgot_password")
async def forgot_password():
    return {"message": "Forgot password endpoint"}

@router.get("/alias_sugerido")
async def alias_sugerido():
    return {"message": "Alias sugerido endpoint"}
