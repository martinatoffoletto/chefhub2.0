from typing import Optional
from pydantic import BaseModel



#acessos a bd agregar actualizar, eliminar, etc

class Usuario(BaseModel):
    idUsuario: Optional[int] = None  # se autogenera en la BD
    mail: str
    nickname: str
    habilitado: str  # 'Si' o 'No'
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    avatar: Optional[str] = None  # URL

class Alumno(BaseModel):
    idAlumno: Optional[int]  # FK hacia usuarios.idUsuario
    numeroTarjeta: Optional[str] = None
    dniFrente: Optional[str] = None
    dniFondo: Optional[str] = None
    tramite: Optional[str] = None
    cuentaCorriente: Optional[float] = None

class Password(BaseModel):
    idpassword: int  # FK hacia usuarios.idUsuario
    password: str
        
class DatosUpgradeAlumno(BaseModel):
    numeroTarjeta: str
    tramite: str
    email: Optional[str] = None

