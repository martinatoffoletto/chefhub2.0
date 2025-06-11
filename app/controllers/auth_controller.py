from fastapi import APIRouter, HTTPException, status, Depends, Body
from app.services import auth_service
from app.services.auth_service import SECRET_KEY, ALGORITHM
from jose import JWTError, jwt
from pydantic import BaseModel
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
    
@router.post("/register")
async def register():
    return {"message": "Register endpoint"}

@router.put("/forgot_password")
async def forgot_password():
    return {"message": "Forgot password endpoint"}

@router.get("/alias_sugerido")
async def alias_sugerido():
    return {"message": "Alias sugerido endpoint"}
