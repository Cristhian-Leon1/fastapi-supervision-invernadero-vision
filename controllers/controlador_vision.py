import cv2
import base64


def procesar_imagen_base64(imagen_original):
    lista_imagenes = []
    lista_base64 = []
    try:
        imagen_original = cv2.resize(imagen_original, (264, 350))
        imagen_copia = imagen_original.copy()

        canal_azul, canal_verde, canal_rojo = cv2.split(imagen_original)
        _, umbral_verde_planta = cv2.threshold(canal_verde, 200, 255, cv2.THRESH_BINARY)
        contornos_planta, _ = cv2.findContours(umbral_verde_planta, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mayor_contorno_planta = max(contornos_planta, key=cv2.contourArea)
        x1, y1, ancho_planta, largo_planta = cv2.boundingRect(mayor_contorno_planta)

        imagen_recortada = imagen_copia[y1:y1 + largo_planta, x1:x1 + ancho_planta].copy()
        imagen_recortada_proceso = cv2.GaussianBlur(imagen_recortada, (3, 3), 0)

        if ancho_planta > 190 or largo_planta > 130:
            _, umbral_recorte = cv2.threshold(imagen_recortada_proceso[:, :, 2], 186, 255, cv2.THRESH_BINARY)
        else:
            _, umbral_recorte = cv2.threshold(imagen_recortada_proceso[:, :, 1], 235, 255, cv2.THRESH_BINARY)

        contornos_hojas, _ = cv2.findContours(umbral_recorte, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        mayor_contorno_hoja = max(contornos_hojas, key=cv2.contourArea)
        x2, y2, ancho_hoja, largo_hoja = cv2.boundingRect(mayor_contorno_hoja)

        recorte_planta = imagen_copia[y1:y1 + largo_planta, x1:x1 + ancho_planta].copy()
        lista_imagenes.append(recorte_planta)
        recorte_hoja = imagen_copia[y1:y1 + largo_planta, x1:x1 + ancho_planta].copy()
        planta_recorte_hoja = cv2.rectangle(recorte_hoja, (x2, y2), (x2 + ancho_hoja, y2 + largo_hoja),
                                            (255, 255, 255), 2)
        lista_imagenes.append(planta_recorte_hoja)

        for imagen in lista_imagenes:
            _, buffer = cv2.imencode('.jpg', imagen)
            imagen_base64 = base64.b64encode(buffer).decode('utf-8')
            lista_base64.append(imagen_base64)

        return ancho_hoja, largo_hoja, lista_base64[0], lista_base64[1]

    except Exception as e:
        print(f"Ocurrió un error al procesar la imagen: {e}")
        return None
