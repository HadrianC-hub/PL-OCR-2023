#Importando librerías escenciales
import numpy as np
import matplotlib.pyplot as plt
import scipy
import cv2 as cv


#------------------------------------------MÉTODOS USADOS------------------------------------------

def binarize (img):
    #Llevando a escala de grises
    gray_img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #cv.imshow('Gray Img',gray_img)
    #cv.waitKey(0)

    #Aplicando un filtro de mediana para eliminar el ruido
    denoised_img = cv.medianBlur(gray_img, 3)
    #cv.imshow('Denoised Img',denoised_img)
    #cv.waitKey(0)

    #Ecualizando imágen por celdas
    clahe=cv.createCLAHE(clipLimit=3.0,tileGridSize=(8,8)) #Instanciando algoritmo de ecualización
    equalized_img=clahe.apply(denoised_img)
    #cv.imshow('Equalized Img',equalized_img)
    #cv.waitKey(0)

    #Detectando los bordes de la imágen para corregir la inclinación
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
    #cv.imshow('Rotated Img',rotated_img)
    #cv.waitKey(0)

    #Extrayendo contornos de imágen aplicando la binarización de OTSU (Halla el valor óptimo del umbral en la imágen)
    _,thresh=cv.threshold(rotated_img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    cv.imshow('Threshold Img',thresh)
    cv.waitKey(0)
    return thresh

def get_textblocks (binarized_img, img):
    #Encontrar los contornos en la imagen
    cont_img = img
    contours, _ = cv.findContours(binarized_img, cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    for i in range (len(contours)):
        cv.drawContours(cont_img, contours, i, (0, 255, 0), 1)
    cv.imshow('Contornos',cont_img)
    cv.waitKey(0)

    #Inicializar una lista para almacenar los bloques de texto encontrados
    text_blocks = []

    #Recorrer todos los contornos encontrados
    for contour in contours:
        #Obtener el rectángulo delimitador del contorno
        x, y, w, h = cv.boundingRect(contour)
        if (w*h>50):
            text_blocks.append((x, y, w, h))

    #Mostrar los bloques de texto encontrados en la imagen original
    image = img
    for block in text_blocks:
        x, y, w, h = block
        cv.rectangle(image, (x, y), (x + w, y + h), (0, 255, 255), 1)

    cv.imshow('Text Blocks', image)
    cv.waitKey(0)
    cv.destroyAllWindows()


#------------------------------------------EJECUCIÓN PRINCIPAL DEL PROGRAMA------------------------------------------

#Cargando imágen
img=cv.imread('samples/sample.png')

#Binarizando imágen
binarized_img = binarize(img)

#Encontrando bloques de texto
get_textblocks(binarized_img, img)

