from fastapi import APIRouter, HTTPException, status, Body
from app.services import auth_service
from app.services.auth_service import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from pydantic import BaseModel
import redis
import random
import json
from app.models.usuario import Usuario
from app.models.usuario import Password
from app.services.user_services import cambiar_contrasena, asignar_password_a_usuario

redis_client = redis.Redis(host='localhost', port=6379, db=0)
router = APIRouter()

@router.post("/auth/login")
async def login(email: str = Body(...), password: str = Body(...)):
    try:
        resultado = await auth_service.autenticar_usuario(email, password)
    except ValueError as e:
        if "Invalid salt" in str(e):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales inválidas"
            )
        else:
            raise  

    if resultado is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

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
async def register_first_step(username: str=Body(...), email: str=Body(...),nombre: str = Body(...), direccion: str = Body(...)):
    try:
        already_registered = await auth_service.buscar_usuario_por_mail(email)
        print(f"Usuario ya registrado: {already_registered}")
        if already_registered:
            habilitado = already_registered.get("habilitado", "").lower()
            puede_recuperar = habilitado == "si"

            return {
                "status": "usuario_existente",
                "message": "El email ya está registrado.",
                "puede_recuperar": puede_recuperar
            }

        is_available = await auth_service.validar_alias(username=username)
        if not is_available:
            raise HTTPException(status_code=409, detail="Alias no disponible")
        
        usuario = Usuario(
            mail=email,
            nickname=username,
            nombre=nombre,
            direccion=direccion,
            habilitado='No')
        
        await auth_service.create_user(usuario, None)

        codigo = f"{random.randint(1000, 9999)}"
        email_sent = await auth_service.enviar_codigo_mail(email=email, codigo=codigo, subject="Registro")
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
async def creates_password(password: str = Body(...), email: str = Body(...)):
    try:
        hashed_password = await auth_service.create_password(password)
        user = await auth_service.buscar_usuario_por_mail(email)
        await asignar_password_a_usuario(user['idUsuario'], hashed_password)
        return {
            "status": "ok",
            "message": "Contraseña creada correctamente"
        }
    except Exception as e:
        print(f"Error creando contraseña: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")



    
@router.post('/register/avatar')
async def chosen_avatar(email: str = Body(...), avatar: str = Body(...)):
    try:
        user = await auth_service.buscar_usuario_por_mail(email)
        await auth_service.asignar_avatar_a_usuario(user['idUsuario'], avatar)
        return {"status": "ok", "message": "Avatar asignado correctamente"}
    except Exception as e:
        print(f"Error creando avatar: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")


    
@router.post("/forgot_password")
async def forgot_password(email: str = Body(...)):
    try:

        exists= await auth_service.buscar_usuario_por_mail(mail=email)
        if not exists:
            raise HTTPException(status_code=404, detail="Mail no encontrado")

        codigo = f"{random.randint(1000, 9999)}"
        email_sent = await auth_service.enviar_codigo_mail(email=email, codigo=codigo, subject="Olvidé mi contraseña")
        if not email_sent:
            raise HTTPException(status_code=500, detail="Error enviando el código")
        print(f"Código generado: {codigo}")
        datos_temporales = {
            "email": email,
            "codigo": codigo
        }

        redis_client.set(f"forgot_password_temp:{email}", json.dumps(datos_temporales), ex=1800)

        return {"status": "ok", "message": "Código enviado al mail"}

    except HTTPException as http_err:
        raise http_err

    except Exception as e:
        print(f"Error inesperado en forgot_password: {e}")
        raise HTTPException(status_code=500, detail="Error interno en forgot_password")

@router.post("/forgot-password-code-verification")
async def forgot_password_code_verification(email:str=Body(...), code:str=Body(...)):
    try:
        data_raw = redis_client.get(f"forgot_password_temp:{email}")
        if not data_raw:
            raise HTTPException(status_code=403, detail="Código no encontrado o expirado")

        data = json.loads(data_raw)
        if data.get("codigo") != code:
            raise HTTPException(status_code=403, detail="Código inválido")

        return {"status": "ok", "message": "Código validado correctamente"}
    except HTTPException as http_err:
        raise http_err
    
    except Exception as e:
        print(f"Error en validación de código: {e}")
        raise HTTPException(status_code=500, detail="Error en la validación de código")

@router.post("/reset-password")
async def reset_password(email:str=Body(...),password:str=Body(...)):
    try:
        user=await auth_service.buscar_usuario_por_mail(mail=email)
        if user is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        success = await auth_service.create_password(password)
        if not success:
            raise HTTPException(status_code=500, detail="Error creando la contraseña")
        
        id_usuario = int(user['idUsuario'])

        new_password=Password(
            idpassword=id_usuario,
            password=success
        )

        await cambiar_contrasena(pass_obj=new_password)
        
        return("Contraseña cambiada exitosamente")
        
    except Exception as e:
        print(f"Error cambiando contraseña: {e}")
        raise HTTPException(status_code=500, detail="Error en el servidor")

@router.get("/alias-sugerido")
async def alias_sugerido(alias:str):
    exists= await auth_service.validar_alias(alias)
    return {"disponible": exists}
