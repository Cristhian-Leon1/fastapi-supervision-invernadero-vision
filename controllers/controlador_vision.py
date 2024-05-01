from ultralytics import YOLO
import cv2
import base64

model = YOLO('cv-medida-hojas_v2.pt')


def procesar_imagen_base64(imagen_frontend):
    lista_imagenes = []
    lista_base64 = []
    resultados = {}
    imagenes_recortadas = {}
    try:
        imagen_copia = imagen_frontend.copy()

        results = model(imagen_copia)
        for result in results:
            boxes = result.boxes

            for i in range(len(boxes)):
                mejor_conf = boxes[i].conf.max()
                mejor_conf_index = boxes[i].conf.argmax()
                mejor_xyxy = boxes[i].xyxy[mejor_conf_index]
                mejor_xyxy_list = mejor_xyxy.tolist()
                clase = boxes[i].cls.item()

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

                _, buffer = cv2.imencode('.jpg', imagen_recorte)
                imagen_base64 = base64.b64encode(buffer).decode('utf-8')
                imagenes_recortadas[clase] = imagen_base64

                ancho_pixeles = abs(mejor_xyxy_list[2] - mejor_xyxy_list[0])
                largo_pixeles = abs(mejor_xyxy_list[3] - mejor_xyxy_list[1])

                ancho_pixeles_original = ancho_pixeles * 3.9
                largo_pixeles_original = largo_pixeles * 3.9

                ancho_centimetros = (ancho_pixeles_original * 13.5) / 3070
                largo_centimetros = (largo_pixeles_original * 18.2) / 4080

                resultado = {
                    'clase': clase,
                    'ancho': ancho_centimetros,
                    'largo': largo_centimetros,
                    'area': ancho_centimetros * largo_centimetros
                }

                if clase in resultados:
                    resultados[clase].append(resultado)
                else:
                    resultados[clase] = [resultado]

        for imagen in lista_imagenes:
            _, buffer = cv2.imencode('.jpg', imagen)
            imagen_base64 = base64.b64encode(buffer).decode('utf-8')
            lista_base64.append(imagen_base64)

        print(resultados)

        max_area_results = {clase: max(resultados_clase, key=lambda x: x['area']) for clase, resultados_clase in
                            resultados.items()}

        max_area_clase = max(max_area_results, key=lambda x: max_area_results[x]['area'])
        max_area_result = max_area_results[max_area_clase]

        return max_area_result['ancho'], max_area_result['largo'], lista_base64[0], imagenes_recortadas[max_area_clase]

    except Exception as e:
        print(f"Ocurrió un error al procesar la imagen: {e}")
        return None
