from rawImage import rawImage
import cv2

f = open("dev.txt", "w")

for j in range(1, 6):
    img = cv2.imread("../test/test1_" + str(j) + ".jpg")
    raw = rawImage(img)
    dev, y, w = raw.findDeviation()
    f.write("1_" + str(j) + ":\n")
    f.write("dev = " + str(dev) + "\n")
    if y == 1:
        f.write("yellow line found\n")
    elif y == 0:
        f.write("y_offset too small\n")
    else:
        f.write("can't find y_lines\n")
    if w == 1:
        f.write("white line found\n")
    elif y == 0:
        f.write("w_offset too big\n")
    else:
        f.write("can't find w_lines\n")

for i in range(2, 5):
    for j in range(1, 11):
        img = cv2.imread("../test/test" + str(i) + "_" + str(j) + ".jpg")
        raw = rawImage(img)
        dev, y, w = raw.findDeviation()
        f.write(str(i) + "_" + str(j) + ":\n")
        f.write("dev = " + str(dev) + "\n")
        if y == 1:
            f.write("yellow line found\n")
        elif y == 0:
            f.write("y_offset too small\n")
        else:
            f.write("can't find y_lines\n")
        if w == 1:
            f.write("white line found\n")
        elif y == 0:
            f.write("w_offset too big\n")
        else:
            f.write("can't find w_lines\n")
