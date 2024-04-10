# fastapi-supervision-invernadero-vision
This is a backend application in FastAPI for the CRUD operations corresponding to sensor records of humidity, temperature, pH, and CO2. These records will be generated from a Raspberry Pi connected to the FastAPI server.

Additionally, it includes WebSocket functionality to allow the activation of solenoid valves that enable instant remote irrigation to the plants in a crop.

Lastly, it also features the functionality of an artificial vision model (YOLO) for classification through supervised learning. Its purpose is to classify the largest leaf of a plant and, from a controlled environment, measure the length and width of the leaf in order to determine its growth percentage.

Language: Python

Framework: FastAPI

Database: MongoDB Atlas

CV-Model: YOLOv8
