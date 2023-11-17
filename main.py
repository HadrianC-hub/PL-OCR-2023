#Importando librerías escenciales
import numpy
import matplotlib.pyplot as plt
import scipy
import cv2 as cv
import binarize

#Cargando imágen
img=cv.imread('samples/sample.png')
img2=cv.imread('samples/sample2.jpg')
#cv.imshow('Test Image',img2)
#cv.waitKey(0)

#Binarizando imágen
binarized_img =binarize.execute(img2)