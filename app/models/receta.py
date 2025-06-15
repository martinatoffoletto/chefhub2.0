from app.config.db import ejecutar_consulta_async
from typing import List, Optional, Dict
from pydantic import BaseModel
from enum import Enum
from datetime import datetime

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


