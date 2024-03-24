from ultralytics import YOLO
import cv2
import base64

model = YOLO('/models/vision/cv-medida-hojas_v1.pt')


def procesar_imagen_base64(imagen_frontend):
    largo_centimetros, ancho_centimetros = 0, 0
    lista_imagenes = []
    lista_base64 = []
    try:
        imagen_copia = imagen_frontend.copy()

        results = model(imagen_copia)
        for result in results:
            boxes = result.boxes

            mejor_conf = boxes.conf.max()
            mejor_conf_index = boxes.conf.argmax()
            mejor_xyxy = boxes.xyxy[mejor_conf_index]
            mejor_xyxy_list = mejor_xyxy.tolist()

            imamen_deteccion = cv2.rectangle(imagen_frontend,
                                             (int(mejor_xyxy_list[0]), int(mejor_xyxy_list[1])),
                                             (int(mejor_xyxy_list[2]), int(mejor_xyxy_list[3])),
                                             (0, 0, 255), 4)

            lista_imagenes.append(imamen_deteccion)

            print('Mejor confianza:', mejor_conf)
            print('Mejor xyxy:', mejor_xyxy_list)

            imagen_recorte = imagen_copia[int(mejor_xyxy_list[1]):int(mejor_xyxy_list[3]),
                                            int(mejor_xyxy_list[0]):int(mejor_xyxy_list[2])]
            lista_imagenes.append(imagen_recorte)

            ancho_pixeles = abs(mejor_xyxy_list[2] - mejor_xyxy_list[0])
            largo_pixeles = abs(mejor_xyxy_list[3] - mejor_xyxy_list[1])

            ancho_pixeles_original = ancho_pixeles * 3.9
            largo_pixeles_original = largo_pixeles * 3.9

            ancho_centimetros = (ancho_pixeles_original * 13.5) / 3070
            largo_centimetros = (largo_pixeles_original * 18.2) / 4080

        for imagen in lista_imagenes:
            _, buffer = cv2.imencode('.jpg', imagen)
            imagen_base64 = base64.b64encode(buffer).decode('utf-8')
            lista_base64.append(imagen_base64)

        return ancho_centimetros, largo_centimetros, lista_base64[0], lista_base64[1]

    except Exception as e:
        print(f"Ocurrió un error al procesar la imagen: {e}")
        return None
