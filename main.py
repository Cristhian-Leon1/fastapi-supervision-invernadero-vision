import uvicorn
from fastapi import FastAPI, WebSocket
from routes.rutas_invernadero import get_router
from mongoDB.conexion_mongo import establecer_conexion
from routes.rutas_vision import router as vision_router
from fastapi.middleware.cors import CORSMiddleware
from webSocket.websocket import websocket_endpoint  # Importa la función del WebSocket

sensores_collection = None

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Puedes ajustar esto según tus necesidades
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

app.websocket("/ws")(websocket_endpoint)  # Agrega la ruta del WebSocket


def start_application():
    global sensores_collection
    sensores_collection = establecer_conexion()
    app.include_router(get_router(sensores_collection), prefix="/api")
    app.include_router(vision_router, prefix="/vision", tags=["vision"])


if __name__ == "__main__":
    start_application()
    uvicorn.run(app, host="0.0.0.0", port=10000)
