from fastapi import APIRouter,HTTPException, status, Depends, Body
from app.services import auth_service
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
async def refresh_token(data: RefreshTokenRequest):
    try:
        payload = jwt.decode(data.refresh_token, auth_service.SECRET_KEY, algorithms=[auth_service.ALGORITHM])
        print(payload)
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
        
        usuario = await auth_service.obtener_usuario_por_id(user_id, auth_service.get_usuarios_collection())
        if not usuario:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no encontrado")

        access_token, new_refresh_token = auth_service.crear_tokens(usuario)

        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }

    except JWTError as e:
        print("Error JWT:", e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token inválido o expirado")

@router.post("/register")
async def register():
    return {"message": "Register endpoint"}

@router.put("/forgot_password")
async def forgot_password():
    return {"message": "Forgot password endpoint"}


@router.get("/alias_sugerido")
async def alias_sugerido():
    return {"message": "Alias sugerido endpoint"}
