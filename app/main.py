from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.controllers import user_controller, curso_controller, auth_controller, receta_controller
from app.config.db import startup, shutdown
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()

app = FastAPI(lifespan=lifespan)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir routers
app.include_router(curso_controller.router, tags=["Cursos"])
app.include_router(user_controller.router, tags=["User"])
app.include_router(auth_controller.router, tags=["Auth"])
app.include_router(receta_controller.router, tags=["Recetas"])


