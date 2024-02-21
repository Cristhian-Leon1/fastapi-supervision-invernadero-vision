import uvicorn
from fastapi import FastAPI
from routes.rutas_invernadero import get_router
from mongoDB.conexion_mongo import establecer_conexion
from routes.rutas_vision import router as vision_router
from fastapi.middleware.cors import CORSMiddleware

sensores_collection = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)


def start_application():
    global sensores_collection
    sensores_collection = establecer_conexion()
    app.include_router(get_router(sensores_collection), prefix="/api")
    app.include_router(vision_router, prefix="/vision", tags=["vision"])
