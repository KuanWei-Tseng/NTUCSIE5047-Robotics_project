from rawImage import rawImage
import numpy as np
import cv2

img = cv2.imread("img2.jpg")
raw = rawImage(img)

print (raw.findDeviation())
