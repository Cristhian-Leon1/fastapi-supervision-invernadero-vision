import cv2
import numpy as np
from click import File
from fastapi import APIRouter, HTTPException, UploadFile
from controllers.controlador_vision import procesar_imagen_base64

router = APIRouter()


@router.post("/procesar_imagen")
async def upload_image(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        np_arr = np.fromstring(contents, np.uint8)
        imagen = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        ancho_centimetros, largo_centimetros, recorte_planta, recorte_hoja = procesar_imagen_base64(imagen)

        return {"ancho_centimetros": ancho_centimetros, "largo_centimetros": largo_centimetros,
                "recorte_planta": recorte_planta, "recorte_hoja": recorte_hoja}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
