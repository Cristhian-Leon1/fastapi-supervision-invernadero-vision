from typing import List
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

# Variables booleanas iniciales
estado_valvula1 = False
estado_valvula2 = False

# Lista de clientes conectados
clientes: List[WebSocket] = []


# Función para enviar el estado actual a todos los clientes conectados
async def enviar_estado(ws: WebSocket):
    await ws.send_json({"estado_valvula1": estado_valvula1, "estado_valvula2": estado_valvula2})


async def websocket_endpoint(websocket: WebSocket):
    global estado_valvula1, estado_valvula2
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
                estado_valvula1 = True
            elif data == 'Apagar valvula 1':
                estado_valvula1 = False
            elif data == 'Encender valvula 2':
                estado_valvula2 = True
            elif data == 'Apagar valvula 2':
                estado_valvula2 = False

            print('estado valvula 1:', estado_valvula1)
            print('estado valvula 2:', estado_valvula2)

            for cliente in clientes:
                await enviar_estado(cliente)
    except WebSocketDisconnect:
        print('Cliente desconectado')
        clientes.remove(websocket)
        estado_valvula1 = False
        estado_valvula2 = False
