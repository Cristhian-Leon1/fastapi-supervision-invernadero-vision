from fastapi import APIRouter, HTTPException
from typing import List
from models.modelo_invernadero import InvernaderoDataModel
from controllers.controladores_invernadero import (create_sensor_data, get_sensor_byID, get_all_sensor_data,
                                                   delete_sensor_byID, update_sensor_byID,
                                                   delete_all_sensor_data, get_last_20_sensor_data,
                                                   get_last_sensor_data)


def get_router(sensores_collection):
    router = APIRouter()

    # Crear registro
    @router.post("/sensores", response_model=dict)
    def create__data(sensor_data: InvernaderoDataModel):
        result = create_sensor_data(sensor_data, sensores_collection)
        if "error" in result:
            raise HTTPException(status_code=500, detail="Error interno del servidor")
        return result

    # Actualizar registro por ID
    @router.put("/sensores/{sensor_id}", response_model=dict)
    def update_sensor(sensor_id: str, updated_data: InvernaderoDataModel):
        result = update_sensor_byID(sensor_id, updated_data, sensores_collection)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result

    # Leer registro por ID
    @router.get("/sensores/{sensor_id}", response_model=InvernaderoDataModel)
    def read_sensor_byID(sensor_id: str):
        sensor_data = get_sensor_byID(sensor_id, sensores_collection)
        if sensor_data:
            return sensor_data
        else:
            raise HTTPException(status_code=404, detail="Sensor no encontrado")

    # Leer todos los registros
    @router.get("/sensores", response_model=List[InvernaderoDataModel])
    def read_all_sensor_data():
        sensor_data_list = get_all_sensor_data(sensores_collection)
        if sensor_data_list:
            return sensor_data_list
        else:
            raise HTTPException(status_code=404, detail="No se encontraron registros de sensores")

    # Leer los últimos 20 registros
    @router.get("/sensores/get/last20", response_model=List[InvernaderoDataModel])
    def read_last_20_sensor_data():
        sensor_data_list = get_last_20_sensor_data(sensores_collection)
        if sensor_data_list:
            return sensor_data_list
        else:
            return []

    # Leer el último registro
    @router.get("/sensores/get/last", response_model=InvernaderoDataModel)
    def read_last_sensor_data():
        sensor_data = get_last_sensor_data(sensores_collection)
        if sensor_data:
            return sensor_data
        else:
            raise HTTPException(status_code=404, detail="No se encontraron registros de sensores")
  
    # Eliminar registro por ID
    @router.delete("/sensores/{sensor_id}", response_model=dict)
    def delete_sensor(sensor_id: str):
        result = delete_sensor_byID(sensor_id, sensores_collection)
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        return result

    # Eliminar todos los registros
    @router.delete("/sensores", response_model=dict)
    def delete_all_sensors():
        result = delete_all_sensor_data(sensores_collection)
        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])
        return result

    return router
