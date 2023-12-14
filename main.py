#Importando librerías escenciales
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy
import cv2 as cv
import pytesseract
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

#------------------------------------------MÉTODOS USADOS------------------------------------------

def binarize (img):
    #Llevando a escala de grises
    gray_img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    #Aplicando un filtro de mediana para minimizar el ruido (manchas, diferencias de iluminación, etc)
    denoised_img = cv.medianBlur(gray_img, 3)

    #Ecualizando imágen por celdas
    #La ecualización es aplicada para garantizar que el ruido minimizado de la imágen desaparezca 
    #casi por completo...
    clahe=cv.createCLAHE(clipLimit=3.0,tileGridSize=(8,8)) #Instanciando algoritmo de ecualización
    equalized_img=clahe.apply(denoised_img)

    #Detectando los bordes de la imágen para corregir la inclinación
    #En el caso en que una imágen no esté en un ángulo de inclinación correcto, se corrige a partir de
    #este método (su funcionamiento depende en gran medida de la evaluación de los ángulos del borde 
    #exterior más destacado)
    edges = cv.Canny(equalized_img, 50, 150, apertureSize=3)
    lines = cv.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)

    #Corrigiendo la inclinación de la imagen
    angle = 0
    for x1, y1, x2, y2 in lines[0]:
        angle = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
        break
    rows, cols = equalized_img.shape[:2]
    M = cv.getRotationMatrix2D((cols/2, rows/2), angle, 1)
    rotated_img = cv.warpAffine(equalized_img, M, (cols, rows), flags=cv.INTER_CUBIC, borderMode=cv.BORDER_REPLICATE)

    #Extrayendo contornos de imágen aplicando la binarización de OTSU (Halla el valor óptimo del umbral en la imágen)
    _,thresh=cv.threshold(rotated_img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    #En este punto obtuvimos la mejor calidad que pudimos extraer de la imagen, ahora convertida a una imagen binaria.
    return thresh

def get_textblocks (binarized_img, img):
    #Encontrar los contornos en la imagen (para poder distinguir cada cuadro)
    d = pytesseract.image_to_data(binarized_img, output_type=Output.DICT)

    #Imprimir las coordenadas y el texto de cada bloque de texto
    #La funcionalidad de este algoritmo radica en delimitar un texto por 4 puntos y luego trazar una línea
    #para conectarlos. Mientras más rectangular sea la figura obtenida, mejor definida estará la línea de texto
    #De igual manera es capaz de delimitar dos bloques de texto contiguos debido al espacio que existe entre
    #ellos y a la diferencia de tamaño de sus correspondientes rectángulos.
    for i in range(len(d['text'])):
        if int(d['conf'][i]) > 60:
            (x, y, w, h) = (d['left'][i], d['top'][i], d['width'][i], d['height'][i])
            cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            text = d['text'][i]
            cv.putText(img, text, (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    cv.imshow('img', img)
    cv.waitKey(0)
    cv.destroyAllWindows()


#------------------------------------------EJECUCIÓN PRINCIPAL DEL PROGRAMA------------------------------------------

#Estableciendo carpeta de contenidos
folder='Content' #Cambiar solo si sabe lo que hace
out='Output'
print('Carpeta predeterminada de entrada: '+folder+'\n')
print('Carpeta predeterminada de salida: '+out+'\n')

#Limpiando directorio de salida
out_f=os.listdir(out)
for file in out_f:
    os.remove(out+'/'+file)
print('Directorio de salida limpiado con éxito'+'\n')

#Revisando directorio de contenido
files = os.listdir(folder)

#Filtramos los archivos .jpg y .png
f_files=[]
for file in files:
    if(file.endswith('.jpg') or file.endswith('.png')):
        f_files.append(file)

#Iterando por cada archivo
for file in files:
    #Cargando imágen
    img=cv.imread(folder+"/"+file)

    #Binarizando imágen
    binarized_img = binarize(img)

    #Encontrando bloques de texto
    #get_textblocks(binarized_img, img)
    #Este algoritmo simula el método de extracción de bloques de texto utilizado por Tesseract, fue la
    #primera implementación de esta funcionalidad y es una alternativa válida que solamente utiliza OpenCV

    #Generando texto a partir de la imágen
    text = pytesseract.image_to_string(binarized_img,lang='spa')

    #Esta línea está comentada porque representa el post-procesamiento de los datos
    #data = data.replace('subcadena a reemplazar', 'subcadena de reemplazo')
    #Este método reemplaza todas las ocurrencias de una subcadena específica en una cadena con otra subcadena.

    #Creación de archivo de datos con el informe del texto extraído
    f=open(out+'/'+file+'.txt','x')
    f.write(file+':\n'+text)
    f.close
    print('Analizado archivo '+file+': Creado informe en '+out+'\n')

input('Ejecución finalizada, presione cualquier tecla para cerrar la consola...')
 