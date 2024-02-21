from pydantic import BaseModel
from datetime import datetime


class InvernaderoDataModel(BaseModel):
    sensor1: float = None
    sensor2: float = None
    sensor3: float = None
    sensor4: float = None
    sensor5: float = None
    timestamp: datetime = None
