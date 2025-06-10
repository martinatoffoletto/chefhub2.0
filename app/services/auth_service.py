from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from app.models.usuario import *  

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
            "tipo_usuario": tipo_usuario
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
