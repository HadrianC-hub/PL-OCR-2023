import numpy
import matplotlib.pyplot as plt
import scipy
import cv2

img_raw=cv2.imread('sample.jpg')

type(img_raw)
numpy.ndarray

img_raw.shape
(1300,1950,3)

img = cv2.cvtColor(img_raw, cv2.COLOR_BGR2RGB)

cv2.imwrite('processed_image.jpg',img)
