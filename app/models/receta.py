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
            SELECT 
                r.idReceta, 
                r.nombreReceta, 
                r.descripcionReceta, 
                r.fotoPrincipal, 
                u.nickname,
                ISNULL(c.promedioCalificacion, 0) AS promedioCalificacion
            FROM dbo.recetas r
            JOIN (
                SELECT idReceta, MAX(fecha_creacion) AS ultima_fecha
                FROM dbo.estadoReceta
                GROUP BY idReceta
            ) er_max ON r.idReceta = er_max.idReceta
            JOIN dbo.estadoReceta er ON er.idReceta = er_max.idReceta AND er.fecha_creacion = er_max.ultima_fecha
            LEFT JOIN (
                SELECT idReceta, AVG(CAST(calificacion AS FLOAT)) AS promedioCalificacion
                FROM dbo.calificaciones
                GROUP BY idReceta
            ) c ON c.idReceta = r.idReceta
            JOIN dbo.usuarios u ON r.idUsuario = u.idUsuario
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
                    SELECT 1 FROM dbo.utilizados u2 
                    WHERE u2.idReceta = r.idReceta AND u2.idIngrediente = ?
                )
            """
            params.append(contiene_ingrediente)

        if excluye_ingrediente:
            query += """
                AND NOT EXISTS (
                    SELECT 1 FROM dbo.utilizados u2 
                    WHERE u2.idReceta = r.idReceta AND u2.idIngrediente = ?
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