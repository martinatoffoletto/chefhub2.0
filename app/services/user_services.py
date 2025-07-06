from app.models.usuario import *
from app.models.asistenciaCurso import *
from app.models.cronogramaCurso import *
from app.models.curso import *
from datetime import datetime
import app.config.db as db


############ SE USA EN AUTH SERVICE Y CONTROLLER ############

#registro de usuario
async def crear_usuario(usuario: Usuario, password: str) -> Optional[int]:
    async with db.pool.acquire() as conn:
        try:
            # Inserta el usuario
            query_user = """
                INSERT INTO usuarios (mail, nickname, habilitado, nombre, direccion, avatar)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            await db.ejecutar_consulta_async(query_user, (
                usuario.mail,
                usuario.nickname,
                usuario.habilitado,
                usuario.nombre,
                usuario.direccion,
                usuario.avatar
            ), external_conn=conn)

            # Obtener el id recién insertado
            id_user_result = await db.ejecutar_consulta_async(
                "SELECT TOP 1 idUsuario as id FROM usuarios ORDER BY idUsuario DESC",
                fetch=True,
                external_conn=conn
            )
            id_user = id_user_result[0]['id'] if id_user_result else None

            # Insertar la contraseña
            if password and id_user:
                query_pass = "INSERT INTO passwords (idpassword, password) VALUES (?, ?)"
                await db.ejecutar_consulta_async(query_pass, (id_user, password), external_conn=conn)

            await conn.commit()
            return id_user

        except Exception as e:
            await conn.rollback()
            print("❌ Error creando usuario:", e)
            raise


#registro alumno
async def crear_alumno(alumno: Alumno) -> Optional[int]:
    async with db.pool.acquire() as conn:
        try:
            # Inserta en la tabla alumnos
            query_user = """
                INSERT INTO alumnos (idAlumno, numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            await db.ejecutar_consulta_async(query_user, (
                alumno.idAlumno,
                alumno.numeroTarjeta,
                alumno.dniFrente,
                alumno.dniFondo,
                alumno.tramite,
                alumno.cuentaCorriente
            ), external_conn=conn)

            # Recupera el último id insertado
            id_user_result = await db.ejecutar_consulta_async(
                "SELECT TOP 1 idAlumno as id FROM alumnos ORDER BY idAlumno DESC",
                fetch=True,
                external_conn=conn
            )

            id_user = id_user_result[0]['id'] if id_user_result else None

            await conn.commit()
            return id_user

        except Exception as e:
            await conn.rollback()
            print("❌ Error creando alumno:", e)
            raise

# Buscar usuario por ID (con datos de alumno y contraseña)
async def buscar_usuario_por_id(id_usuario: int) -> Optional[Dict]:
    async with db.pool.acquire() as conn:
        try:
            # Buscar usuario
            query_user = "SELECT * FROM usuarios WHERE idUsuario = ?"
            usuario = await db.ejecutar_consulta_async(query_user, (id_usuario,), fetch=True, external_conn=conn)

            if not usuario:
                return None

            user_data = dict(usuario[0]) 

            # Buscar contraseña
            query_pass = "SELECT password FROM passwords WHERE idpassword = ?"
            pass_result = await db.ejecutar_consulta_async(query_pass, (id_usuario,), fetch=True, external_conn=conn)
            if pass_result:
                user_data['password'] = pass_result[0]['password']

            # Buscar datos de alumno
            query_alumno = """
                SELECT numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente
                FROM alumnos WHERE idAlumno = ?
            """
            alumno_result = await db.ejecutar_consulta_async(query_alumno, (id_usuario,), fetch=True, external_conn=conn)
            if alumno_result:
                user_data.update(alumno_result[0])

            return user_data

        except Exception as e:
            print("❌ Error buscando usuario por ID:", e)
            raise

# Buscar usuario por mail
async def buscar_usuario_por_mail(mail: str) -> Optional[Dict]:
    async with db.pool.acquire() as conn:
        try:
            # Buscar usuario
            query_user = "SELECT * FROM usuarios WHERE mail = ?"
            usuario = await db.ejecutar_consulta_async(query_user, (mail,), fetch=True, external_conn=conn)
            if not usuario:
                return None

            user_data = dict(usuario[0])
            id_usuario = user_data['idUsuario']

            # Buscar contraseña
            query_pass = "SELECT password FROM passwords WHERE idpassword = ?"
            pass_result = await db.ejecutar_consulta_async(query_pass, (id_usuario,), fetch=True, external_conn=conn)
            if pass_result:
                user_data['password'] = pass_result[0]['password']

            # Buscar datos de alumno (si lo es)
            query_alumno = """
                SELECT numeroTarjeta, dniFrente, dniFondo, tramite, cuentaCorriente
                FROM alumnos WHERE idAlumno = ?
            """
            alumno_result = await db.ejecutar_consulta_async(query_alumno, (id_usuario,), fetch=True, external_conn=conn)
            if alumno_result:
                user_data.update(alumno_result[0])

            return user_data

        except Exception as e:
            print("❌ Error buscando usuario por mail:", e)
            raise

# Cambiar contraseña
async def cambiar_contrasena(pass_obj: Password) -> bool:
    async with db.pool.acquire() as conn:
        try:
            # Obtener la contraseña actual
            first_query = "SELECT password FROM passwords WHERE idpassword= ?"
            old_psswd = await db.ejecutar_consulta_async(first_query, (pass_obj.idpassword,), fetch=True, external_conn=conn)
            if old_psswd:
                print("Contraseña vieja:", old_psswd[0]["password"])
            else:
                print("No se encontró ninguna contraseña con ese ID")

            # Actualizar contraseña
            update_query = "UPDATE passwords SET password = ? WHERE idpassword = ?"
            await db.ejecutar_consulta_async(update_query, (pass_obj.password, pass_obj.idpassword), external_conn=conn)

            # Verificar nueva contraseña
            new_query = "SELECT password FROM passwords WHERE idpassword = ?"
            result = await db.ejecutar_consulta_async(new_query, (pass_obj.idpassword,), fetch=True, external_conn=conn)
            if result:
                print("Contraseña actualizada:", result[0]["password"])
            else:
                print("No se encontró ninguna contraseña con ese ID")

            await conn.commit()
            return True

        except Exception as e:
            await conn.rollback()
            print("❌ Error actualizando contraseña:", e)
            raise


#buscar usuario por alias
async def buscar_usuario_por_alias(username: str):
    query_user="SELECT * FROM usuarios WHERE nickname = ?"
    usuario= await db.ejecutar_consulta_async(query_user, (username,), fetch=True)

    if usuario:
        return True
    return False


# Obtener el nickname de un usuario por su ID
async def obtener_nickname_por_id(id_usuario: int) -> Optional[str]:
    query = "SELECT nickname FROM usuarios WHERE idUsuario = ?"
    resultado = await db.ejecutar_consulta_async(query, [id_usuario], fetch=True)
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
        recetas = await db.ejecutar_consulta_async(query, (id_usuario,), fetch=True)
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
        await db.ejecutar_consulta_async(query, (id_usuario, id_receta))
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
        await db.ejecutar_consulta_async(query, (id_usuario, id_receta))
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
    resultado = await db.ejecutar_consulta_async(query, (id_usuario, id_receta), fetch=True)
    return resultado[0]['total'] > 0 if resultado else False

#obtener notificaciones
async def obtener_notificaciones_por_usuario(id_usuario: int):
    query = """
        SELECT idNotificacion, descripcion, fecha_envio
        FROM notificaciones
        WHERE idUsuario = ?
        ORDER BY fecha_envio DESC
    """
    return await db.ejecutar_consulta_async(query, (id_usuario,), fetch=True)

# Convertir usuario a alumno
async def upgradear_a_alumno(alumno, current_user) -> bool:
    query = """
        INSERT INTO alumnos (idAlumno, numeroTarjeta, tramite, cuentaCorriente)
        VALUES (?, ?, ?, 0)
    """
    await db.ejecutar_consulta_async(query, (
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
            s.idSede,
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
    return await db.ejecutar_consulta_async(query, [current_user["idUsuario"]], fetch=True)


async def guardar_dni(user_id: int, path: str, campo: str):
    query = f"UPDATE alumnos SET {campo} = ? WHERE idAlumno = ?"
    await db.ejecutar_consulta_async(query, (path, user_id))

async def asignar_avatar_a_usuario(user_id: int, avatar: str) -> bool:
    query = "UPDATE usuarios SET avatar = ?, habilitado = 'Si' WHERE idUsuario = ?"
    try:
        await db.ejecutar_consulta_async(query, (avatar, user_id))
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
        await db.ejecutar_consulta_async(query, (idUsuario, password))
        return True
    except Exception as e:
        print(f"Error al asignar contraseña: {e}")
        return False

async def registrar_asistencia_usuario(sede_id: int, curso_id: int, user: Dict) -> Dict:
    async with db.pool.acquire() as conn:
        try:
            # Buscar cronograma activo
            query_cronograma = """
                SELECT TOP 1 idCronograma
                FROM cronogramaCursos
                WHERE idSede = ? AND idCurso = ?
            """
            cronogramas = await db.ejecutar_consulta_async(query_cronograma, (sede_id, curso_id), fetch=True, external_conn=conn)
            cronograma = cronogramas[0] if cronogramas else None

            if not cronograma:
                return {"ok": False, "status": 500, "error": "No hay un cronograma activo para este curso y sede."}

            id_cronograma = cronograma["idCronograma"]

            # Verificar inscripción
            query_inscripcion = """
                SELECT 1
                FROM asistenciaCursos
                WHERE idAlumno = ? AND idCronograma = ?
            """
            inscripciones = await db.ejecutar_consulta_async(query_inscripcion, (user["idUsuario"], id_cronograma), fetch=True, external_conn=conn)
            inscripto = inscripciones[0] if inscripciones else None

            if not inscripto:
                return {"ok": False, "status": 403, "error": "El alumno no está inscripto en este curso."}

            # Registrar asistencia
            query_asistencia = """
                INSERT INTO asistenciaCursos (idAlumno, idCronograma, fecha)
                VALUES (?, ?, ?)
            """
            await db.ejecutar_consulta_async(
                query_asistencia,
                (user["idUsuario"], id_cronograma, datetime.now()),
                external_conn=conn
            )

            await conn.commit()
            return {"ok": True, "mensaje": "Asistencia registrada correctamente"}

        except Exception as e:
            await conn.rollback()
            print("❌ Error registrando asistencia:", e)
            return {"ok": False, "status": 500, "error": "Error al registrar asistencia."}