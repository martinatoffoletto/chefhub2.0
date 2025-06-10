from typing import Optional, Union, Dict
from pydantic import BaseModel
from app.config.db import ejecutar_consulta


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
    idAlumno: int  # FK hacia usuarios.idUsuario
    numeroTarjeta: Optional[str] = None
    dniFrente: Optional[str] = None
    dniFondo: Optional[str] = None
    tramite: Optional[str] = None
    cuentaCorriente: Optional[float] = None

class Password(BaseModel):
    idpassword: int  # FK hacia usuarios.idUsuario
    password: str
        
#Consultas a la base de datos

def crear_usuario(usuario: Usuario, password: str) -> Optional[int]:
    query_user = """
        INSERT INTO usuarios (mail, nickname, habilitado, nombre, direccion, avatar)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    ejecutar_consulta(query_user, (
        usuario.mail,
        usuario.nickname,
        usuario.habilitado,
        usuario.nombre,
        usuario.direccion,
        usuario.avatar
    ))

    id_user = ejecutar_consulta("SELECT TOP 1 idUsuario as id FROM usuarios ORDER BY idUsuario DESC", fetch=True)[0]['id']

    query_pass = "INSERT INTO passwords (idpassword, password) VALUES (?, ?)"
    ejecutar_consulta(query_pass, (id_user, password))

    return id_user


# Buscar usuario por ID (con datos de alumno y contraseña)
def buscar_usuario_por_id(id_usuario: int) -> Optional[Dict]:
    query_user = "SELECT * FROM usuarios WHERE idUsuario = ?"
    usuario = ejecutar_consulta(query_user, (id_usuario,), fetch=True)
    
    if not usuario:
        return None

    user_data = dict(usuario[0]) 

    # Buscar password
    query_pass = "SELECT password FROM passwords WHERE idpassword = ?"
    pass_result = ejecutar_consulta(query_pass, (id_usuario,), fetch=True)
    if pass_result:
        user_data['password'] = pass_result[0]['password']

    # Buscar si es alumno
    query_alumno = """
        SELECT numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente
        FROM alumnos WHERE idAlumno = ?
    """
    alumno_result = ejecutar_consulta(query_alumno, (id_usuario,), fetch=True)
    if alumno_result:
        user_data.update(alumno_result[0]) 

    return user_data


# Buscar usuario por mail
def buscar_usuario_por_mail(mail: str) -> Optional[Dict]:
    query_user = "SELECT * FROM usuarios WHERE mail = ?"
    usuario = ejecutar_consulta(query_user, (mail,), fetch=True)
    
    if not usuario:
        return None

    user_data = dict(usuario[0])
    id_usuario = user_data['idUsuario']


    query_pass = "SELECT password FROM passwords WHERE idpassword = ?"
    pass_result = ejecutar_consulta(query_pass, (id_usuario,), fetch=True)
    if pass_result:
        user_data['password'] = pass_result[0]['password']


    query_alumno = """
        SELECT numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente
        FROM alumnos WHERE idAlumno = ?
    """
    alumno_result = ejecutar_consulta(query_alumno, (id_usuario,), fetch=True)
    if alumno_result:
        user_data.update(alumno_result[0])

    return user_data



# Convertir usuario a alumno
def upgradear_a_alumno(alumno: Alumno) -> bool:
    query = """
        INSERT INTO alumnos (idAlumno, numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    ejecutar_consulta(query, (
        alumno.idAlumno,
        alumno.numeroTarjeta,
        alumno.dniFrente,
        alumno.dniFondo,
        alumno.tramite,
        alumno.cuentaCorriente
    ))
    return True


# Cambiar contraseña
def cambiar_contrasena(pass_obj: Password) -> bool:
    query = """
        UPDATE passwords SET password = ? WHERE idpassword = ?
    """
    ejecutar_consulta(query, (pass_obj.password, pass_obj.idpassword))
    return True