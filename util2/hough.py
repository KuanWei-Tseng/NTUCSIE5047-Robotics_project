import cv2
import numpy as np
import sys

filename = sys.argv[1]
img = cv2.imread(filename)
row, column = img.shape[0], img.shape[1]
print("row = {}, column = {}".format(row, column))

# intensity equalization
hsl = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#hsl[:,:,2] = cv2.equalizeHist(hsl[:,:,2])
eq = cv2.cvtColor(hsl, cv2.COLOR_HSV2BGR)
cv2.imwrite("equal.jpg", eq)

kernel = np.ones((5, 5), np.uint8)
# 3-5-5-5-3 octogonal kernel
kernel[0][0] = kernel[4][0] = kernel[0][4] = kernel[4][4] = 0
vote = 200
# white and yellow detection
temp = np.logical_and(eq[:,:,1] > 150, eq[:,:,2] > 150)
temp1 = np.logical_and(eq[:,:,1] > 100, eq[:,:,2] > 100)
# yellow color mark
y_cm = np.logical_and(temp1, eq[:,:,0] < 100).astype(np.uint8)
# close then open
y_cm = cv2.morphologyEx(cv2.morphologyEx(y_cm, cv2.MORPH_CLOSE, kernel), cv2.MORPH_OPEN, kernel)
cv2.imwrite("y_mark.jpg", y_cm*255)

# white color mark
w_cm = np.logical_and(temp, eq[:,:,0] > 150).astype(np.uint8)
# close then open
w_cm = cv2.morphologyEx(cv2.morphologyEx(w_cm, cv2.MORPH_CLOSE, kernel), cv2.MORPH_OPEN, kernel)
cv2.imwrite("w_mark.jpg", w_cm*255)

# gray scale canny edge detection
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
edges = cv2.Canny(blur,50,150,apertureSize = 3)

cv2.imwrite("canny.jpg", edges)

# intersection of canny and road markings
y_inter = (edges * y_cm > 0).astype(np.uint8)
w_inter = (edges * w_cm > 0).astype(np.uint8)
y_inter = cv2.dilate(y_inter, kernel, iterations = 1)
w_inter = cv2.dilate(w_inter, kernel, iterations = 1)
cv2.imwrite("y_inter.jpg", y_inter*255)
cv2.imwrite("w_inter.jpg", w_inter*255)

# Hough line detection
y_lines = cv2.HoughLines(y_inter, 1, np.pi/180, vote)
w_lines = cv2.HoughLines(w_inter, 1, np.pi/180, vote)

# find the rightmost yellow line
y_rho, y_theta, y_offset = 0, 0, -float("inf")

for rho, theta in y_lines[:, 0]:
    # ignore horizontal lines
    # only shows lines that are in 80-degree difference to vertical line
    if theta < 80*np.pi/180 or (np.pi - theta) < 80*np.pi/180:
        """
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1200*(-b))
        y1 = int(y0 + 1200*(a))
        x2 = int(x0 - 1200*(-b))
        y2 = int(y0 - 1200*(a))
        cv2.line(img,(x1,y1),(x2,y2),(0,255,255),2)
        """
        offset = int(np.cos(theta)*rho-np.tan(theta)*(row-np.sin(theta)*rho))
        if offset > y_offset:
            y_rho, y_theta, y_offset = rho, theta, offset

# find the leftmost white line
w_rho, w_theta, w_offset = 0, 0, float("1000")

for rho, theta in w_lines[:, 0]:
    # ignore horizontal lines
    # only shows lines that are in 80-degree difference to vertical line
    if theta < 80*np.pi/180 or (np.pi - theta) < 80*np.pi/180:
        """
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1200*(-b))
        y1 = int(y0 + 1200*(a))
        x2 = int(x0 - 1200*(-b))
        y2 = int(y0 - 1200*(a))
        cv2.line(img,(x1,y1),(x2,y2),(255,255,255),2)
        """
        offset = int(np.cos(theta)*rho-np.tan(theta)*(row-np.sin(theta)*rho))
        if offset > y_offset and offset < w_offset:
            w_rho, w_theta, w_offset = rho, theta, offset

# draw line
a = np.cos(y_theta)
b = np.sin(y_theta)
x0 = a * y_rho
y0 = b * y_rho
x1 = int(x0 + 1200*(-b))
y1 = int(y0 + 1200*(a))
x2 = int(x0 - 1200*(-b))
y2 = int(y0 - 1200*(a))

cv2.line(img,(x1,y1),(x2,y2),(0,255,255),2)

# draw line
a = np.cos(w_theta)
b = np.sin(w_theta)
x0 = a * w_rho
y0 = b * w_rho
x1 = int(x0 + 1200*(-b))
y1 = int(y0 + 1200*(a))
x2 = int(x0 - 1200*(-b))
y2 = int(y0 - 1200*(a))

cv2.line(img,(x1,y1),(x2,y2),(255,255,255),2)

# draw two offset dots
if y_offset >= 0:
    cv2.circle(img,(int(y_offset),int(row)),7,(0,255,255),5)
if w_offset < column:
    cv2.circle(img,(int(w_offset),int(row)),7,(255,255,255),5)

cv2.imwrite("road_lines.jpg",img)

print("y_offset = {}, w_offset = {}".format(y_offset, w_offset))

error = 0
middle = column/2 + error
deviation = int((w_offset + y_offset)/2) - middle
print("middle = {}".format(middle))
print("deviation = {}".format(deviation))

if deviation > 0:
    print("should go right {} pixels".format(deviation))
elif deviation < 0:
    print("should go left {} pixels".format(-deviation))
else:
    print("should go straight")
