import cv2 as cv

def execute (img):
    #Llevando a escala de grises
    gray_img=cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #cv.imshow('Gray Img',gray_img)
    #cv.waitKey(0)

    #Ecualizando imágen por celdas
    clahe=cv.createCLAHE(clipLimit=3.0,tileGridSize=(8,8)) #Instanciando algoritmo de ecualización
    equalized_img=clahe.apply(gray_img)
    #cv.imshow('Equalized Img',equalized_img)
    #cv.waitKey(0)

    #Extrayendo contornos de imágen aplicando la binarización de OTSU (Halla el valor óptimo del umbral en la imágen)
    _,thresh=cv.threshold(equalized_img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    #cv.imshow('Threshold Img',thresh)
    #cv.waitKey(0)
    return thresh