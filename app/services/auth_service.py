from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from app.models.usuario import *  
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status


SECRET_KEY = "secret"
ALGORITHM = "HS256"

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login") ##para extraer token de la cabecera de la peticion

def crear_tokens(usuario):
    expire_access = datetime.now(timezone.utc) + timedelta(minutes=60)  
    expire_refresh = datetime.now(timezone.utc) + timedelta(days=7)    

    payload_access = {
        "sub": str(usuario["_id"]),
        "tipo_usuario": usuario["tipo_usuario"],
        "exp": expire_access
    }
    
    payload_refresh = {
        "sub": str(usuario["_id"]),
        "exp": expire_refresh
    }
    
    access_token = jwt.encode(payload_access, SECRET_KEY, algorithm=ALGORITHM)
    refresh_token = jwt.encode(payload_refresh, SECRET_KEY, algorithm=ALGORITHM)
    
    return access_token, refresh_token



def autenticar_usuario(email: str, password: str) -> dict | None:
    usuario = buscar_usuario_por_mail(email)

    if not usuario or usuario["password"] != password:
        return None

    # Definir tipo_usuario según la presencia de 'numeroTarjeta'
    tipo_usuario = "Alumno" if usuario.get("numeroTarjeta") else "Usuario"
    usuario["tipo_usuario"] = tipo_usuario  # agregar para usar en crear_tokens

    access_token, refresh_token = crear_tokens(usuario)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "user": {
            "id": str(usuario["_id"]),
            "email": usuario["mail"],  # corregido a "mail", que es el campo que usás
            "tipo_usuario": tipo_usuario
        }
    }


def obtener_usuario_actual(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Token inválido")

        usuario =  buscar_usuario_por_id(user_id)
        print("Usuario encontrado: ",usuario)
        if usuario is None:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        print(f"Usuario actual: {usuario['idUsuario']}")
        return usuario

    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
