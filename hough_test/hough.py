import cv2
import numpy as np

img = cv2.imread('img2.jpg')
row, column = img.shape[0], img.shape[1]
print "row =", row, "column =", column

# yellow and white markings detection
color_mark = np.logical_and(img[:,:,1] > 180, img[:,:,2] > 180).astype(np.uint8)
kernel = np.ones((5, 5), np.uint8)

# 3-5-5-5-3 octogonal kernel
kernel[0][0] = kernel[4][0] = kernel[0][4] = kernel[4][4] = 0

# close then open
color_mark = cv2.morphologyEx(cv2.morphologyEx(color_mark, cv2.MORPH_CLOSE, kernel), cv2.MORPH_OPEN, kernel)
cv2.imwrite('color_mark.jpg', color_mark*255)

# gray scale canny edge detection
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(img, (5, 5), 0)
edges = cv2.Canny(blur,50,150,apertureSize = 3)

cv2.imwrite('canny.jpg', edges)

# intersection of canny and road markings
intersection = (edges * color_mark > 0).astype(np.uint8)

# Hough line detection
lines = cv2.HoughLines(intersection,1,np.pi/180,80)

for i in range(0, len(lines)):
    for rho,theta in lines[i]:
        # ignore horizontal lines
        # only shows lines that are in 60-degree difference to vertical line
        if theta < 60*np.pi/180 or (np.pi - theta) < 60*np.pi/180:
            # draw line
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1200*(-b))
            y1 = int(y0 + 1200*(a))
            x2 = int(x0 - 1200*(-b))
            y2 = int(y0 - 1200*(a))

            cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)
            # draw dot
            cv2.circle(img,(int(x0-np.tan(theta)*(row-y0)),int(row)),7,(0,255,0),5)

cv2.imwrite('all_houghlines.jpg',img)

