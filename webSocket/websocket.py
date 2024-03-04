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
            print('Mensaje recibido:', data)

            if data == 'Encender valvula 1':
                estado = True
            elif data == 'Apagar valvula 1':
                estado = False

            print('estado:', estado)

            for cliente in clientes:
                await enviar_estado(cliente)
    except WebSocketDisconnect:
        print('Cliente desconectado')
        clientes.remove(websocket)
        estado = False
