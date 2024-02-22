from typing import List
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect


# Variable booleana inicial
estado = False

# Lista de clientes conectados
clientes: List[WebSocket] = []


# Función para enviar el estado actual a todos los clientes conectados
async def enviar_estado(ws: WebSocket):
    await ws.send_json({"estado": estado})


async def websocket_endpoint(websocket: WebSocket):
    global estado
    await websocket.accept()
    clientes.append(websocket)
    print('Cliente conectado')

    # Enviar el estado actual al cliente cuando se conecta
    await enviar_estado(websocket)

    try:
        while True:
            data = await websocket.receive_text()
            print('Mensaje recibido:', data)  # Imprimir el mensaje recibido en consola

            # Cambiar el estado de acuerdo al mensaje recibido
            estado = not estado

            print('estado:', estado)

            # Enviar el nuevo estado a todos los clientes
            for cliente in clientes:
                await enviar_estado(cliente)
    except WebSocketDisconnect:
        print('Cliente desconectado')
        clientes.remove(websocket)