from app.config.db import ejecutar_consulta_async
from typing import List, Optional, Dict
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

###################acessos a bd agregar actualizar, eliminar, etc###############################
class TipoReceta(BaseModel):
    idTipo: Optional[int]
    descripcion: Optional[str]


class Ingrediente(BaseModel):
    idIngrediente: Optional[int]
    nombre: Optional[str]


class Unidad(BaseModel):
    idUnidad: Optional[int]
    descripcion: Optional[str]


class Conversion(BaseModel):
    idConversion: Optional[int]
    idUnidadOrigen: int
    idUnidadDestino: int
    factorConversiones: float


class Foto(BaseModel):
    idfoto: Optional[int]
    idReceta: int
    urlFoto: str
    extension: Optional[str]


class MultimediaTipo(str, Enum):
    foto = 'foto'
    video = 'video'
    audio = 'audio'


class Multimedia(BaseModel):
    idContenido: Optional[int]
    idPaso: int
    tipo_contenido: MultimediaTipo
    extension: Optional[str]
    urlContenido: str


class Paso(BaseModel):
    idPaso: Optional[int]
    idReceta: int
    nroPaso: int
    texto: str


class Utilizado(BaseModel):
    idUtilizado: Optional[int]
    idReceta: int
    idIngrediente: int
    cantidad: int
    idUnidad: int
    observaciones: Optional[str] = None

class EstadoEnum(str, Enum):
    aprobado = 'aprobado'
    rechazado = 'rechazado'
    pendiente = 'pendiente'

class EstadoReceta(BaseModel):
    idEstado: Optional[int] 
    idReceta: int #fk hacia receta.idReceta
    fecha_creacion: datetime
    estado: EstadoEnum

class Receta(BaseModel):
    idReceta: Optional[int]
    idUsuario: int
    nombreReceta: str
    descripcionReceta: Optional[str] = None
    fotoPrincipal: Optional[str] = None
    porciones: Optional[int] = None
    cantidadPersonas: Optional[int] = None
    idTipo: int


#CRUD

async def crear_receta_completa(
    receta_data: Dict,
    ingredientes_data: List[Dict],
    pasos_data: List[Dict],
    multimedia_data: List[Dict]
) -> Dict:
    """
    Crea una receta completa con todos sus componentes:
    - Datos básicos de la receta
    - Ingredientes (creando nuevos si no existen)
    - Pasos de preparación
    - Multimedia (fotos, videos)
    
    El estado inicial siempre es 'pendiente'
    """
    try:
        # 1. Crear la receta básica
        query_receta = """
            INSERT INTO Receta (
                idUsuario, nombreReceta, descripcionReceta, 
                fotoPrincipal, porciones, cantidadPersonas, idTipo
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params_receta = (
            receta_data['idUsuario'],
            receta_data['nombreReceta'],
            receta_data.get('descripcionReceta'),
            receta_data.get('fotoPrincipal'),
            receta_data.get('porciones'),
            receta_data.get('cantidadPersonas'),
            receta_data['idTipo']
        )
        await ejecutar_consulta_async(query_receta, params_receta)
        receta_creada = await ejecutar_consulta_async("SELECT TOP 1 * FROM Receta ORDER BY idReceta DESC", fetch=True)
        if not receta_creada:
            raise Exception("No se pudo crear la receta")
        id_receta = receta_creada[0]['idReceta']

        # 2. Establecer estado inicial como 'pendiente'
        query_estado = """
            INSERT INTO EstadoReceta (idReceta, estado)
            VALUES (?, ?)
        """
        await ejecutar_consulta_async(query_estado, (id_receta, 'pendiente'))

        # 3. Procesar ingredientes
        for ingrediente in ingredientes_data:
            # Verificar si el ingrediente existe
            query_ingrediente = "SELECT idIngrediente FROM Ingrediente WHERE nombre = ?"
            ingrediente_existente = await ejecutar_consulta_async(
                query_ingrediente, 
                (ingrediente['nombre'],), 
                fetch=True
            )
            id_ingrediente = None
            if ingrediente_existente:
                id_ingrediente = ingrediente_existente[0]['idIngrediente']
            else:
                # Crear nuevo ingrediente
                query_nuevo_ing = """
                    INSERT INTO Ingrediente (nombre) 
                    VALUES (?)
                """
                await ejecutar_consulta_async(query_nuevo_ing, (ingrediente['nombre'],))
                nuevo_ing = await ejecutar_consulta_async("SELECT TOP 1 idIngrediente FROM Ingrediente ORDER BY idIngrediente DESC", fetch=True)
                id_ingrediente = nuevo_ing[0]['idIngrediente']

            # Crear relación Utilizado
            query_utilizado = """
                INSERT INTO Utilizado (
                    idReceta, idIngrediente, cantidad, idUnidad, observaciones
                ) VALUES (?, ?, ?, ?, ?)
            """
            params_utilizado = (
                id_receta,
                id_ingrediente,
                ingrediente['cantidad'],
                ingrediente['idUnidad'],
                ingrediente.get('observaciones')
            )
            await ejecutar_consulta_async(query_utilizado, params_utilizado)

        # 4. Procesar pasos
        for paso in pasos_data:
            query_paso = """
                INSERT INTO Paso (idReceta, nroPaso, texto)
                VALUES (?, ?, ?)
            """
            await ejecutar_consulta_async(query_paso, (id_receta, paso['nroPaso'], paso['texto']))
            paso_creado = await ejecutar_consulta_async("SELECT TOP 1 idPaso FROM Paso ORDER BY idPaso DESC", fetch=True)
            id_paso = paso_creado[0]['idPaso']

            # 5. Procesar multimedia asociada a pasos
            for media in multimedia_data:
                if media['idPaso'] == paso['idPaso']:
                    query_media = """
                        INSERT INTO Multimedia (
                            idPaso, tipo_contenido, extension, urlContenido
                        ) VALUES (?, ?, ?, ?)
                    """
                    await ejecutar_consulta_async(
                        query_media,
                        (
                            id_paso,
                            media['tipo_contenido'].value,
                            media.get('extension'),
                            media['urlContenido']
                        )
                    )

        # Obtener y retornar la receta completa creada
        return await obtener_receta_completa(id_receta)

    except Exception as e:
        print(f"Error al crear receta: {str(e)}")
        raise e

async def obtener_receta_completa(id_receta: int) -> Optional[Dict]:
    """
    Obtiene todos los datos de una receta incluyendo:
    - Datos básicos
    - Ingredientes con cantidades y unidades
    - Pasos con su multimedia asociada
    - Estado actual
    - Fotos principales
    """
    try:
        # 1. Obtener datos básicos de la receta
        query_receta = "SELECT * FROM Recetas WHERE idReceta = ?"
        receta = await ejecutar_consulta_async(query_receta, (id_receta,), fetch=True)
        if not receta:
            return None
        
        receta_data = receta[0]
        
        # 2. Obtener estado actual
        query_estado = """
            SELECT TOP 1 estado FROM EstadoReceta 
            WHERE idReceta = ? 
            ORDER BY idEstado DESC
        """
        estado = await ejecutar_consulta_async(query_estado, (id_receta,), fetch=True)
        receta_data['estado'] = estado[0]['estado'] if estado else None
        
        # 3. Obtener ingredientes con unidades
        query_ingredientes = """
            SELECT u.*, i.nombre as nombre_ingrediente, ut.cantidad, ut.observaciones
            FROM Utilizados ut
            JOIN Ingredientes i ON ut.idIngrediente = i.idIngrediente
            JOIN Unidades u ON ut.idUnidad = u.idUnidad
            WHERE ut.idReceta = ?
        """
        ingredientes = await ejecutar_consulta_async(query_ingredientes, (id_receta,), fetch=True)
        receta_data['ingredientes'] = ingredientes if ingredientes else []
        
        # 4. Obtener pasos con multimedia
        query_pasos = """
            SELECT p.* FROM Pasos p
            WHERE p.idReceta = ?
            ORDER BY p.nroPaso
        """
        pasos = await ejecutar_consulta_async(query_pasos, (id_receta,), fetch=True)
        for paso in pasos:
            query_multimedia = """
                SELECT tipo_contenido, urlContenido, extension
                FROM Multimedia
                WHERE idPaso = ?
            """
            multimedia = await ejecutar_consulta_async(query_multimedia, (paso['idPaso'],), fetch=True)
            paso['multimedia'] = multimedia if multimedia else []
        receta_data['pasos'] = pasos if pasos else []

        # 5. Obtener fotos adicionales (si existen)
        query_fotos = "SELECT * FROM Fotos WHERE idReceta = ?"
        fotos = await ejecutar_consulta_async(query_fotos, (id_receta,), fetch=True)
        receta_data['fotos'] = fotos if fotos else []

        return receta_data

    except Exception as e:
        print(f"Error al obtener receta: {str(e)}")
        raise e

async def listar_recetas(
    tipo_receta: Optional[int] = None,
    contiene_ingrediente: Optional[int] = None,
    excluye_ingrediente: Optional[int] = None,
    id_usuario: Optional[int] = None,
    nombre: Optional[str] = None,
    ordenar_por: str = 'fecha',  # 'fecha' o 'nombre'
    orden: str = 'desc',         # 'asc' o 'desc'
    limit: Optional[int] = None,
    estado: Optional[str] = "aprobado"  # nuevo parámetro
) -> List[Dict]:
    try:
        query = """
            SELECT r.idReceta, r.nombreReceta, r.descripcionReceta, r.fotoPrincipal, r.idUsuario
            FROM dbo.recetas r
            JOIN (
                SELECT idReceta, MAX(fecha_creacion) AS ultima_fecha
                FROM dbo.estadoReceta
                GROUP BY idReceta
            ) er_max ON r.idReceta = er_max.idReceta
            JOIN dbo.estadoReceta er ON er.idReceta = er_max.idReceta AND er.fecha_creacion = er_max.ultima_fecha
            WHERE 1=1
        """
        params = []

        if estado and estado.lower() != "todos":
            query += " AND LOWER(er.estado) = ?"
            params.append(estado.lower())

        if tipo_receta:
            query += " AND r.idTipo = ?"
            params.append(tipo_receta)

        if id_usuario:
            query += " AND r.idUsuario = ?"
            params.append(id_usuario)

        if nombre:
            query += " AND LOWER(r.nombreReceta) LIKE ?"
            params.append(f"%{nombre.lower()}%")

        if contiene_ingrediente:
            query += """
                AND EXISTS (
                    SELECT 1 FROM dbo.utilizados u 
                    WHERE u.idReceta = r.idReceta AND u.idIngrediente = ?
                )
            """
            params.append(contiene_ingrediente)

        if excluye_ingrediente:
            query += """
                AND NOT EXISTS (
                    SELECT 1 FROM dbo.utilizados u 
                    WHERE u.idReceta = r.idReceta AND u.idIngrediente = ?
                )
            """
            params.append(excluye_ingrediente)

        # Ordenamiento
        if ordenar_por == 'nombre':
            query += f" ORDER BY r.nombreReceta {orden.upper()}"
        else:
            query += f" ORDER BY er.fecha_creacion {orden.upper()}"

        if limit:
            query += " OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY"
            params.append(limit)

        recetas = await ejecutar_consulta_async(query, tuple(params), fetch=True)
        return recetas

    except Exception as e:
        print(f"Error al listar recetas filtradas: {str(e)}")
        raise e

async def listar_ingredientes() -> List[Dict]:
    """
    Devuelve todos los ingredientes (id y nombre)
    """
    query = "SELECT idIngrediente, nombre FROM Ingredientes"
    ingredientes = await ejecutar_consulta_async(query, fetch=True)
    return ingredientes if ingredientes else []

async def listar_tipos_receta() -> List[Dict]:
    """
    Devuelve todos los tipos de receta (id y descripcion)
    """
    query = "SELECT idTipo, descripcion FROM TiposReceta"
    tipos = await ejecutar_consulta_async(query, fetch=True)
    return tipos if tipos else []


async def buscar_recetas_por_nombre(nombre: str, limite: int = 10) -> List[Dict]:
    """
    Busca recetas por nombre usando LIKE case insensitive
    """
    try:
        if not nombre.strip():
            return []
        query = """
            SELECT r.*, 
                   (SELECT TOP 1 estado FROM EstadoReceta er 
                    WHERE er.idReceta = r.idReceta 
                    ORDER BY er.idEstado DESC) as estado
            FROM Receta r
            WHERE r.nombreReceta LIKE ?
            ORDER BY r.nombreReceta
            OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
        """
        recetas = await ejecutar_consulta_async(query, (f"%{nombre}%", limite), fetch=True)
        return recetas if recetas else []
    except Exception as e:
        print(f"Error en búsqueda por nombre: {str(e)}")
        raise e

async def buscar_receta_por_usuario_y_nombre(id_usuario: int, nombre: str) -> Optional[Dict]:
    """
    Busca una receta exacta por usuario y nombre (exact match)
    """
    try:
        query = """
            SELECT r.*, 
                   (SELECT TOP 1 estado FROM EstadoReceta er 
                    WHERE er.idReceta = r.idReceta 
                    ORDER BY er.idEstado DESC) as estado
            FROM Receta r
            WHERE r.idUsuario = ? AND r.nombreReceta = ?
        """
        receta = await ejecutar_consulta_async(query, (id_usuario, nombre), fetch=True)
        return receta[0] if receta else None
    except Exception as e:
        print(f"Error en búsqueda exacta: {str(e)}")
        raise e

async def actualizar_estado_receta(id_receta: int, estado: EstadoEnum) -> bool:
    """
    Actualiza el estado de una receta (aprobado, rechazado, pendiente)
    """
    try:
        query = """
            INSERT INTO EstadoReceta (idReceta, estado)
            VALUES (?, ?)
        """
        await ejecutar_consulta_async(query, (id_receta, estado.value))
        return True
    except Exception as e:
        print(f"Error al actualizar estado: {str(e)}")
        return False