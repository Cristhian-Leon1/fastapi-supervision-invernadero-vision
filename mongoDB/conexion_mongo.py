from pymongo import MongoClient
from pymongo.server_api import ServerApi


def establecer_conexion():
    try:
        uri = ("mongodb+srv://admin:adminadmin@invernaderoup.1aeb9rn.mongodb.net/InvernaderoUP_DB?retryWrites=true&w"
               "=majority")
        client = MongoClient(uri, server_api=ServerApi('1'))

        db = client.get_database()
        sensores_collection = db.Sensores
        client.admin.command('ping')
        print("Ping completado. Conexión establecida correctamente a MongoDB!")
        return sensores_collection
    except Exception as e:
        print(e)

