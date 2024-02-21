from pymongo.errors import PyMongoError
from pymongo.collection import Collection
from typing import List
from datetime import datetime
from models.modelo_invernadero import InvernaderoDataModel


# Crear registro
def create_sensor_data(sensor_data: InvernaderoDataModel, collection: Collection):
    try:
        sensor_data_dict = sensor_data.model_dump()

        if sensor_data_dict["timestamp"] is None:
            sensor_data_dict["timestamp"] = datetime.now()
            sensor_data_dict["timestamp"] = sensor_data_dict["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
        sensor_data_dict["_id"] = collection.count_documents({}) + 1

        result = collection.insert_one(sensor_data_dict)

        return {"message": "Registro creado exitosamente", "id": str(result.inserted_id)}

    except PyMongoError as e:
        return {"error": str(e)}


# Actualizar registro por ID
def update_sensor_byID(sensor_id: str, updated_data: InvernaderoDataModel, collection: Collection) -> dict:
    try:
        sensor_id_num = int(sensor_id)

        current_data = collection.find_one({"_id": sensor_id_num})
        if current_data is None:
            return {"error": f"No se encontró el registro para actualizar con el ID: {sensor_id}"}

        updated_data_dict = updated_data.model_dump()
        for field in updated_data_dict:
            if updated_data_dict[field] is None:
                updated_data_dict[field] = current_data[field]

        if updated_data_dict["timestamp"] is not None:
            updated_data_dict["timestamp"] = updated_data_dict["timestamp"].strftime("%Y-%m-%d %H:%M:%S")

        result = collection.update_one({"_id": sensor_id_num}, {"$set": updated_data_dict})

        if result.modified_count == 1:
            return {"message": "Registro actualizado correctamente"}
        else:
            return {"error": f"No se encontró el registro para actualizar con el ID: {sensor_id}"}
    except Exception as e:
        return {"error": f"Error al intentar actualizar el registro: {str(e)}"}


# Leer registro por ID
def get_sensor_byID(sensor_id: str, collection: Collection):
    try:
        sensor_id_num = int(sensor_id)

        sensor_data = collection.find_one({"_id": sensor_id_num})
        if sensor_data:
            return InvernaderoDataModel(**sensor_data)
        else:
            return None
    except Exception as e:
        print(e)
        return None


# Leer todos los registros
def get_all_sensor_data(collection: Collection) -> List[InvernaderoDataModel]:
    try:
        sensor_data_list = list(collection.find())

        return [InvernaderoDataModel(**sensor_data) for sensor_data in sensor_data_list]
    except Exception as e:
        print(e)
        return []


# Leer los últimos 20 registros
def get_last_20_sensor_data(collection: Collection) -> List[InvernaderoDataModel]:
    try:
        sensor_data_list = list(collection.find().sort([("_id", -1)]).limit(20))

        return [InvernaderoDataModel(**sensor_data) for sensor_data in sensor_data_list]
    except Exception as e:
        print(e)
        return []


# Eliminar registro por ID
def delete_sensor_byID(sensor_id: str, collection: Collection) -> dict:
    try:
        sensor_id_num = int(sensor_id)
        result = collection.delete_one({"_id": sensor_id_num})

        if result.deleted_count == 1:
            return {"message": "Registro eliminado correctamente"}
        else:
            return {"error": "No se encontró el registro para eliminar"}
    except Exception as e:
        print(e)
        return {"error": "Error al intentar eliminar el registro"}


# Eliminar todos los registros
def delete_all_sensor_data(collection: Collection) -> dict:
    try:
        result = collection.delete_many({})

        return {"message": f"Se eliminaron {result.deleted_count} registros correctamente"}
    except Exception as e:
        print(e)
        return {"error": "Error al intentar eliminar los registros"}
