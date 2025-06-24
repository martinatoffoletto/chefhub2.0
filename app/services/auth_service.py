from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.services.user_services import *
import smtplib
import bcrypt
from email.message import EmailMessage

SECRET_KEY = "secret"
ALGORITHM = "HS256"

# Aquí va el auto_error=False para que no lance excepción si no viene token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login", auto_error=False)

async def obtener_usuario_actual_opcional(token: Optional[str] = Depends(oauth2_scheme)):
    if token is None:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            return None
        usuario = await buscar_usuario_por_id(int(user_id))
        if usuario is None:
            return None
        tipo_usuario = "Alumno" if usuario.get("numeroTarjeta") else "Usuario"
        usuario["tipo_usuario"] = tipo_usuario
        return usuario
    except JWTError:
        return None


def crear_tokens(usuario):
    expire_access = datetime.now(timezone.utc) + timedelta(minutes=60)  
    expire_refresh = datetime.now(timezone.utc) + timedelta(days=7)    

    payload_access = {
        "sub": str(usuario["idUsuario"]),
        "tipo_usuario": usuario["tipo_usuario"],
        "exp": expire_access
    }
    
    payload_refresh = {
        "sub": str(usuario["idUsuario"]),
        "exp": expire_refresh
    }
    
    access_token = jwt.encode(payload_access, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(payload_refresh, SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token, refresh_token


async def autenticar_usuario(email: str, password: str) -> dict | None:
    usuario = await buscar_usuario_por_mail(email)

    if not usuario or usuario["password"] != password:
        return None

    tipo_usuario = "Alumno" if usuario.get("numeroTarjeta") else "Usuario"
    usuario["tipo_usuario"] = tipo_usuario

    access_token, refresh_token = crear_tokens(usuario)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(usuario["idUsuario"]),
            "email": usuario["mail"],
            "tipo_usuario": tipo_usuario,
            "nickname": usuario["nickname"],
            "avatar": usuario["avatar"],
        }
    }


async def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    if token is None:
        raise HTTPException(status_code=401, detail="Token requerido")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        usuario = await buscar_usuario_por_id(int(user_id))
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        tipo_usuario = "Alumno" if usuario.get("numeroTarjeta") else "Usuario"
        usuario["tipo_usuario"] = tipo_usuario
        return usuario
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")


async def validar_alias(username: str):
    exists=await buscar_usuario_por_alias(username)
    return not exists

async def enviar_codigo_mail(email: str, codigo: str):
    try:
        sender = "chefhubemail@gmail.com"
        password = "vbqo gjpy pdul rnum"
        subject = "Verificación de Email - ChefHub"
        body = (
            f"¡Hola! Ingresa este código en la aplicación. "
            f"Recuerda: tiene una validez de 24 HORAS.\n\n"
            f"CODIGO: {codigo}\n\n"
            f"Si desconoces esta acción, ignora este mensaje."
        )

        msg = EmailMessage()
        msg['From'] = sender
        msg['To'] = email
        msg['Subject'] = subject
        msg.set_content(body)

        smtp_server = "smtp.gmail.com"
        smtp_port = 587

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)

        print(f"Código {codigo} enviado a {email}")
        return True

    except Exception as e:
        print(f"Error en el envío de mail: {e}")
        return False

async def create_password(password: str, email:str):
    try:
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')
    except Exception as e:
        print(f"Error hasheando contraseña: {e}")
        return False
    
async def create_user(usuario:Usuario, password:str):
    try:
        id_user = await crear_usuario(usuario, password=password)
        if id_user is None:
            raise HTTPException(status_code=500, detail="Error al crear usuario")
        return {id_user}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")


async def create_student(alumno:Alumno):
    try:
        id_user=await crear_alumno(alumno=alumno)
        if id_user is None:
            raise HTTPException(status_code=500, detail="Error al crear alumno")
        return (id_user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")