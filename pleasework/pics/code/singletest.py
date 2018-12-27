from rawImage import rawImage
import cv2
import sys

img = cv2.imread("../" + str(sys.argv[1]) + ".jpg")
raw = rawImage(img)
dev, y, w = raw.findDeviation()
print("dev = " + str(dev) + "\n")
if y == 1:
    print("yellow line found\n")
elif y == 0:
    print("y_offset too small\n")
else:
    print("can't find y_lines\n")
if w == 1:
    print("white line found\n")
elif y == 0:
    print("w_offset too big\n")
else:
    print("can't find w_lines\n")
