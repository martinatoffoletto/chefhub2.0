from typing import List, Optional
from pydantic import BaseModel

#receta

class Ingredientes(BaseModel):
    nombre: str
    cantidad: float
    idUnidad: int
    observaciones: Optional[str] = None


class Pasos(BaseModel):
    nroPaso: int
    texto: str

class RecetaIn(BaseModel):
    nombreReceta: str
    descripcionReceta: str
    porciones: int
    cantidadPersonas: int
    tipo: str
    ingredientes: List[Ingredientes]
    pasos: List[Pasos]