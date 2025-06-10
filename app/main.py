from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from app.controllers import  user_controller
from app.config.db import conectar_bd, cerrar_bd  # tus funciones async para Mongo


@asynccontextmanager
async def lifespan(app: FastAPI):
    conectar_bd()
    print("DB conectada en lifespan")
    yield 
    cerrar_bd()
    print("DB desconectada en lifespan")

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
"""app.include_router(curso_controller.router, tags=["Cursos"])
app.include_router(auth_controller.router, tags=["Auth"])
app.include_router(receta_controller.router, tags=["Recetas"])"""

app.include_router(user_controller.router, tags=["User"])



