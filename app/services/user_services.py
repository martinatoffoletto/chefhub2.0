from app.models.usuario import *
from app.models.asistenciaCurso import *
from app.models.cronogramaCurso import *
from app.models.curso import *
from datetime import datetime

############ SE USA EN AUTH SERVICE Y CONTROLLER ############

#registro de usuario
async def crear_usuario(usuario: Usuario, password: str) -> Optional[int]:
    query_user = """
        INSERT INTO usuarios (mail, nickname, habilitado, nombre, direccion, avatar)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    await ejecutar_consulta_async(query_user, (
        usuario.mail,
        usuario.nickname,
        usuario.habilitado,
        usuario.nombre,
        usuario.direccion,
        usuario.avatar
    ))

    id_user_result = await ejecutar_consulta_async("SELECT TOP 1 idUsuario as id FROM usuarios ORDER BY idUsuario DESC", fetch=True)
    id_user = id_user_result[0]['id'] if id_user_result else None
    if password:
        query_pass = "INSERT INTO passwords (idpassword, password) VALUES (?, ?)"
        await ejecutar_consulta_async(query_pass, (id_user, password))

    return id_user

#registro alumno
async def crear_alumno(alumno:Alumno)-> Optional[int]:
    query_user="""
        INSERT INTO alumnos (idAlumno, numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente)
        VALUES(?,?,?,?,?,?)
    """

    await ejecutar_consulta_async(query_user, (
        alumno.idAlumno,
        alumno.numeroTarjeta,
        alumno.dniFrente,
        alumno.dniFondo,
        alumno.tramite,
        alumno.cuentaCorriente
    ))

    id_user_result=await ejecutar_consulta_async("SELECT TOP 1 idAlumno as id FROM alumnos ORDER BY idAlumno DESC", fetch=True)
    id_user=id_user_result[0]['id'] if id_user_result else None

    return id_user


# Buscar usuario por ID (con datos de alumno y contraseña)
async def buscar_usuario_por_id(id_usuario: int) -> Optional[Dict]:
    query_user = "SELECT * FROM usuarios WHERE idUsuario = ?"
    usuario = await ejecutar_consulta_async(query_user, (id_usuario,), fetch=True)
    
    if not usuario:
        return None

    user_data = dict(usuario[0]) 

    # Buscar password
    query_pass = "SELECT password FROM passwords WHERE idpassword = ?"
    pass_result = await ejecutar_consulta_async(query_pass, (id_usuario,), fetch=True)
    if pass_result:
        user_data['password'] = pass_result[0]['password']

    # Buscar si es alumno
    query_alumno = """
        SELECT numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente
        FROM alumnos WHERE idAlumno = ?
    """
    alumno_result = await ejecutar_consulta_async(query_alumno, (id_usuario,), fetch=True)
    if alumno_result:
        user_data.update(alumno_result[0]) 

    return user_data

# Buscar usuario por mail
async def buscar_usuario_por_mail(mail: str) -> Optional[Dict]:
    query_user = "SELECT * FROM usuarios WHERE mail = ?"
    usuario = await ejecutar_consulta_async(query_user, (mail,), fetch=True)
    
    if not usuario:
        return None

    user_data = dict(usuario[0])
    id_usuario = user_data['idUsuario']


    query_pass = "SELECT password FROM passwords WHERE idpassword = ?"
    pass_result = await ejecutar_consulta_async(query_pass, (id_usuario,), fetch=True)
    if pass_result:
        user_data['password'] = pass_result[0]['password']


    query_alumno = """
        SELECT numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente
        FROM alumnos WHERE idAlumno = ?
    """
    alumno_result = await ejecutar_consulta_async(query_alumno, (id_usuario,), fetch=True)
    if alumno_result:
        user_data.update(alumno_result[0])

    return user_data

# Cambiar contraseña
async def cambiar_contrasena(pass_obj: Password) -> bool:
    first_query="""SELECT password FROM passwords WHERE idpassword= ?"""
    old_psswd=await ejecutar_consulta_async(first_query, (pass_obj.idpassword,), fetch=True)
    if old_psswd:
        print("Contraseña vieja:", old_psswd[0]["password"])
    else:
        print("No se encontró ninguna contraseña con ese ID")

    query = """
        UPDATE passwords SET password = ? WHERE idpassword = ?
    """
    await ejecutar_consulta_async(query, (pass_obj.password, pass_obj.idpassword))

    new_query = "SELECT password FROM passwords WHERE idpassword = ?"
    result = await ejecutar_consulta_async(new_query, (pass_obj.idpassword,), fetch=True)

    if result:
        print("Contraseña actualizada:", result[0]["password"])
    else:
        print("No se encontró ninguna contraseña con ese ID")

    return True

#buscar usuario por alias
async def buscar_usuario_por_alias(username: str):
    query_user="SELECT * FROM usuarios WHERE nickname = ?"
    usuario= await ejecutar_consulta_async(query_user, (username,), fetch=True)

    if usuario:
        return True
    return False


# Obtener el nickname de un usuario por su ID
async def obtener_nickname_por_id(id_usuario: int) -> Optional[str]:
    query = "SELECT nickname FROM usuarios WHERE idUsuario = ?"
    resultado = await ejecutar_consulta_async(query, [id_usuario], fetch=True)
    return resultado[0]["nickname"] if resultado else None



############ ENDPOINTS USUARIOS ############
# Ver recetas favoritas de usuario
async def obtener_recetas_favoritas(id_usuario: int) -> List[Dict]:
    query = """
        SELECT 
            r.idReceta,
            r.nombreReceta,
            r.descripcionReceta,
            r.fotoPrincipal,
            u.nickname,
            u.avatar,
            ISNULL(AVG(c.calificacion), 0) AS promedioCalificacion
        FROM recetas r
        JOIN usuarios u ON r.idUsuario = u.idUsuario
        LEFT JOIN calificaciones c ON r.idReceta = c.idReceta
        WHERE r.idReceta IN (
            SELECT rf.idReceta FROM recetasFavoritas rf WHERE rf.idCreador = ?
        )
        GROUP BY r.idReceta, r.nombreReceta, r.descripcionReceta, r.fotoPrincipal, u.nickname, u.avatar
    """
    try:
        recetas = await ejecutar_consulta_async(query, (id_usuario,), fetch=True)
        return recetas
    except Exception as e:
        print(f"Error al obtener favoritas: {e}")
        return []

# Agregar receta favorita
async def agregar_receta_favorita(id_usuario: int, id_receta: int) -> bool:
    query = """
        INSERT INTO recetasFavoritas (idCreador, idReceta)
        VALUES (?, ?)
    """
    try:
        await ejecutar_consulta_async(query, (id_usuario, id_receta))
        return True
    except Exception as e:
        print(f"Error al agregar favorita: {e}")
        return False


# Eliminar receta favorita
async def eliminar_receta_favorita(id_usuario: int, id_receta: int) -> bool:
    query = """
        DELETE FROM recetasFavoritas
        WHERE idCreador = ? AND idReceta = ?
    """
    try:
        await ejecutar_consulta_async(query, (id_usuario, id_receta))
        return True
    except Exception as e:
        print(f"Error al eliminar favorita: {e}")
        return False

#verificar receta favorita
async def verificar_receta_favorita(id_usuario: int, id_receta: int) -> bool:
    query = """
        SELECT COUNT(*) AS total FROM recetasFavoritas
        WHERE idCreador = ? AND idReceta = ?
    """
    resultado = await ejecutar_consulta_async(query, (id_usuario, id_receta), fetch=True)
    return resultado[0]['total'] > 0 if resultado else False

#obtener notificaciones
async def obtener_notificaciones_por_usuario(id_usuario: int):
    query = """
        SELECT idNotificacion, descripcion, fecha_envio
        FROM notificaciones
        WHERE idUsuario = ?
        ORDER BY fecha_envio DESC
    """
    return await ejecutar_consulta_async(query, (id_usuario,), fetch=True)

# Convertir usuario a alumno
async def upgradear_a_alumno(alumno, current_user) -> bool:
    query = """
        INSERT INTO alumnos (idAlumno, numeroTarjeta, tramite, cuentaCorriente)
        VALUES (?, ?, ?, 0)
    """
    await ejecutar_consulta_async(query, (
        current_user,
        alumno["numeroTarjeta"],
        alumno["tramite"]
    ))
    return True

# Obtener cursos por ID de usuario
async def obtener_cursos_by_user_id(current_user: dict) -> List[Dict]:
    query = """
            SELECT 
            c.idCurso,
            c.descripcion AS nombreCurso,
            c.duracion,
            c.precio AS precioBase,
            cr.idCronograma,
            cr.fechaInicio,
            cr.fechaFin,
            s.nombreSede,
            s.bonificacionCursos,
            s.tipoPromocion,
            s.promocionCursos,
            -- Precio final aplicando bonificaciones y promociones multiplicativamente
            c.precio 
            * (1 - ISNULL(s.bonificacionCursos, 0) / 100)
            * (1 - ISNULL(s.promocionCursos, 0) / 100) AS precioFinal,
            (
                SELECT COUNT(*) 
                FROM asistenciaCursos a2 
                WHERE a2.idCronograma = cr.idCronograma 
                AND a2.idAlumno = a.idAlumno
            ) AS totalAsistencias
        FROM asistenciaCursos a
        JOIN cronogramaCursos cr ON a.idCronograma = cr.idCronograma
        JOIN cursos c ON cr.idCurso = c.idCurso
        JOIN sedes s ON cr.idSede = s.idSede
        WHERE a.idAlumno = ?

    """
    return await ejecutar_consulta_async(query, [current_user["idUsuario"]], fetch=True)


async def guardar_dni(user_id: int, path: str, campo: str):
    query = f"UPDATE alumnos SET {campo} = ? WHERE idAlumno = ?"
    await ejecutar_consulta_async(query, (path, user_id))

async def asignar_avatar_a_usuario(user_id: int, avatar: str) -> bool:
    query = "UPDATE usuarios SET avatar = ?, habilitado = 'Si' WHERE idUsuario = ?"
    try:
        await ejecutar_consulta_async(query, (avatar, user_id))
        return True
    except Exception as e:
        print(f"Error al asignar avatar: {e}")
        return False

    
async def asignar_password_a_usuario(idUsuario: str, password: str) -> bool:
    query = """
    INSERT INTO passwords (idpassword, password)
    VALUES (?, ?)
    """
    try:
        await ejecutar_consulta_async(query, (idUsuario, password))
        return True
    except Exception as e:
        print(f"Error al asignar contraseña: {e}")
        return False
