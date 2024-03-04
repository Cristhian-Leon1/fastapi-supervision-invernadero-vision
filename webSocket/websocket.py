from typing import List
from fastapi import WebSocket
from starlette.websockets import WebSocketDisconnect

estado_valvula1 = False
estado_valvula2 = False

clientes: List[WebSocket] = []


async def enviar_estado(ws: WebSocket):
    await ws.send_json({"estado_valvula1": estado_valvula1, "estado_valvula2": estado_valvula2})


async def websocket_endpoint(websocket: WebSocket):
    global estado_valvula1, estado_valvula2
    await websocket.accept()
    clientes.append(websocket)
    print('Cliente conectado')

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

            for cliente in clientes:
                await enviar_estado(cliente)
    except WebSocketDisconnect:
        print('Cliente desconectado')
        clientes.remove(websocket)
        estado_valvula1 = False
        estado_valvula2 = False
