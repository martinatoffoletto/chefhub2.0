from app.config.db import ejecutar_consulta
from typing import List, Optional, Union, Dict
from pydantic import BaseModel, Field, constr
from enum import Enum


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

from typing import List, Dict, Optional
from datetime import datetime
import re
from enum import Enum
from pydantic import BaseModel

def crear_receta_completa(
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
        ejecutar_consulta(query_receta, params_receta)
        receta_creada = ejecutar_consulta("SELECT TOP 1 * FROM Receta ORDER BY idReceta DESC", fetch=True)
        if not receta_creada:
            raise Exception("No se pudo crear la receta")
        id_receta = receta_creada[0]['idReceta']

        # 2. Establecer estado inicial como 'pendiente'
        query_estado = """
            INSERT INTO EstadoReceta (idReceta, estado)
            VALUES (?, ?)
        """
        ejecutar_consulta(query_estado, (id_receta, 'pendiente'))

        # 3. Procesar ingredientes
        for ingrediente in ingredientes_data:
            # Verificar si el ingrediente existe
            query_ingrediente = "SELECT idIngrediente FROM Ingrediente WHERE nombre = ?"
            ingrediente_existente = ejecutar_consulta(
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
                ejecutar_consulta(query_nuevo_ing, (ingrediente['nombre'],))
                nuevo_ing = ejecutar_consulta("SELECT TOP 1 idIngrediente FROM Ingrediente ORDER BY idIngrediente DESC", fetch=True)
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
            ejecutar_consulta(query_utilizado, params_utilizado)

        # 4. Procesar pasos
        for paso in pasos_data:
            query_paso = """
                INSERT INTO Paso (idReceta, nroPaso, texto)
                VALUES (?, ?, ?)
            """
            ejecutar_consulta(query_paso, (id_receta, paso['nroPaso'], paso['texto']))
            paso_creado = ejecutar_consulta("SELECT TOP 1 idPaso FROM Paso ORDER BY idPaso DESC", fetch=True)
            id_paso = paso_creado[0]['idPaso']

            # 5. Procesar multimedia asociada a pasos
            for media in multimedia_data:
                if media['idPaso'] == paso['idPaso']:
                    query_media = """
                        INSERT INTO Multimedia (
                            idPaso, tipo_contenido, extension, urlContenido
                        ) VALUES (?, ?, ?, ?)
                    """
                    ejecutar_consulta(
                        query_media,
                        (
                            id_paso,
                            media['tipo_contenido'].value,
                            media.get('extension'),
                            media['urlContenido']
                        )
                    )

        # Obtener y retornar la receta completa creada
        return obtener_receta_completa(id_receta)

    except Exception as e:
        print(f"Error al crear receta: {str(e)}")
        raise e

def obtener_receta_completa(id_receta: int) -> Optional[Dict]:
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
        query_receta = "SELECT * FROM Receta WHERE idReceta = ?"
        receta = ejecutar_consulta(query_receta, (id_receta,), fetch=True)
        if not receta:
            return None
        
        receta_data = receta[0]
        
        # 2. Obtener estado actual
        query_estado = """
            SELECT TOP 1 estado FROM EstadoReceta 
            WHERE idReceta = ? 
            ORDER BY idEstado DESC
        """
        estado = ejecutar_consulta(query_estado, (id_receta,), fetch=True)
        receta_data['estado'] = estado[0]['estado'] if estado else None
        
        # 3. Obtener ingredientes con unidades
        query_ingredientes = """
            SELECT u.*, i.nombre as nombre_ingrediente, ut.cantidad, ut.observaciones
            FROM Utilizado ut
            JOIN Ingrediente i ON ut.idIngrediente = i.idIngrediente
            JOIN Unidad u ON ut.idUnidad = u.idUnidad
            WHERE ut.idReceta = ?
        """
        ingredientes = ejecutar_consulta(query_ingredientes, (id_receta,), fetch=True)
        receta_data['ingredientes'] = ingredientes if ingredientes else []
        
        # 4. Obtener pasos con multimedia
        query_pasos = """
            SELECT p.* FROM Paso p
            WHERE p.idReceta = ?
            ORDER BY p.nroPaso
        """
        pasos = ejecutar_consulta(query_pasos, (id_receta,), fetch=True)
        for paso in pasos:
            query_multimedia = """
                SELECT tipo_contenido, urlContenido, extension
                FROM Multimedia
                WHERE idPaso = ?
            """
            multimedia = ejecutar_consulta(query_multimedia, (paso['idPaso'],), fetch=True)
            paso['multimedia'] = multimedia if multimedia else []
        receta_data['pasos'] = pasos if pasos else []

        # 5. Obtener fotos adicionales (si existen)
        query_fotos = "SELECT * FROM Foto WHERE idReceta = ?"
        fotos = ejecutar_consulta(query_fotos, (id_receta,), fetch=True)
        receta_data['fotos'] = fotos if fotos else []

        return receta_data

    except Exception as e:
        print(f"Error al obtener receta: {str(e)}")
        raise e

def listar_recetas(
    tipo_receta: Optional[int] = None,
    id_usuario: Optional[int] = None,
    nombre: Optional[str] = None,
    tiene_ingrediente: Optional[int] = None,
    no_tiene_ingrediente: Optional[int] = None,
    ordenar_por: str = 'fecha_creacion',
    orden: str = 'DESC',
    limite: int = 10,
    offset: int = 0
) -> List[Dict]:
    """
    Lista recetas con múltiples filtros posibles:
    - Por tipo de receta
    - Por usuario creador
    - Por nombre (coincidencia parcial)
    - Que contengan o no ciertos ingredientes
    - Ordenación por diferentes campos
    - Paginación
    """
    try:
        query = """
            SELECT r.*, 
                   (SELECT TOP 1 estado FROM EstadoReceta er 
                    WHERE er.idReceta = r.idReceta 
                    ORDER BY er.idEstado DESC) as estado,
                   t.descripcion as tipo_receta_desc
            FROM Receta r
            JOIN TipoReceta t ON r.idTipo = t.idTipo
            WHERE 1=1
        """
        params = []

        # Aplicar filtros
        if tipo_receta:
            query += " AND r.idTipo = ?"
            params.append(tipo_receta)

        if id_usuario:
            query += " AND r.idUsuario = ?"
            params.append(id_usuario)

        if nombre:
            query += " AND r.nombreReceta LIKE ?"
            params.append(f"%{nombre}%")

        if tiene_ingrediente:
            query += """
                AND EXISTS (
                    SELECT 1 FROM Utilizado u 
                    WHERE u.idReceta = r.idReceta 
                    AND u.idIngrediente = ?
                )
            """
            params.append(tiene_ingrediente)

        if no_tiene_ingrediente:
            query += """
                AND NOT EXISTS (
                    SELECT 1 FROM Utilizado u 
                    WHERE u.idReceta = r.idReceta 
                    AND u.idIngrediente = ?
                )
            """
            params.append(no_tiene_ingrediente)

        # Ordenación
        orden_campos = {
            'nombre': 'r.nombreReceta',
            'fecha': 'r.fechaCreacion',
            'popularidad': '(SELECT COUNT(*) FROM Favoritos WHERE idReceta = r.idReceta)'
        }
        campo_orden = orden_campos.get(ordenar_por, 'r.fechaCreacion')
        query += f" ORDER BY {campo_orden} {orden}"

        # Paginación (SQL Server: OFFSET ... ROWS FETCH NEXT ... ROWS ONLY)
        query += " OFFSET ? ROWS FETCH NEXT ? ROWS ONLY"
        params.extend([offset, limite])

        recetas = ejecutar_consulta(query, tuple(params), fetch=True)

        # Para cada receta, agregar información básica de ingredientes
        for receta in recetas:
            query_ingredientes = """
                SELECT TOP 3 i.nombre 
                FROM Utilizado u
                JOIN Ingrediente i ON u.idIngrediente = i.idIngrediente
                WHERE u.idReceta = ?
            """
            ingredientes = ejecutar_consulta(
                query_ingredientes, 
                (receta['idReceta'],), 
                fetch=True
            )
            receta['ingredientes'] = [ing['nombre'] for ing in ingredientes] if ingredientes else []

        return recetas if recetas else []

    except Exception as e:
        print(f"Error al listar recetas: {str(e)}")
        raise e

def buscar_recetas_por_nombre(nombre: str, limite: int = 10) -> List[Dict]:
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
        recetas = ejecutar_consulta(query, (f"%{nombre}%", limite), fetch=True)
        return recetas if recetas else []
    except Exception as e:
        print(f"Error en búsqueda por nombre: {str(e)}")
        raise e

def buscar_receta_por_usuario_y_nombre(id_usuario: int, nombre: str) -> Optional[Dict]:
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
        receta = ejecutar_consulta(query, (id_usuario, nombre), fetch=True)
        return receta[0] if receta else None
    except Exception as e:
        print(f"Error en búsqueda exacta: {str(e)}")
        raise e

def actualizar_estado_receta(id_receta: int, estado: EstadoEnum) -> bool:
    """
    Actualiza el estado de una receta (aprobado, rechazado, pendiente)
    """
    try:
        query = """
            INSERT INTO EstadoReceta (idReceta, estado)
            VALUES (?, ?)
        """
        ejecutar_consulta(query, (id_receta, estado.value))
        return True
    except Exception as e:
        print(f"Error al actualizar estado: {str(e)}")
        return False