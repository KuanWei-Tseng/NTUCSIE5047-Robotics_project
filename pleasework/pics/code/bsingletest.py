from brawImage import rawImage
import cv2
import sys

img = cv2.imread("../" + str(sys.argv[1]) + ".jpg")
raw = rawImage(img)
theta, dev, type = raw.findDeviation()

if type == "b":
    print("both lines found")
    print("y_theta = " + str(theta))
    print("dev = " + str(dev))
elif type == "y":
    print("yellow line found")
    print("y_theta = " + str(theta))
    print("y_offset = " + str(dev))
elif type == "w":
    print("white line found")
    print("w_theta = " + str(theta))
    print("w_offset = " + str(dev))
else:
    print("nothing found")
