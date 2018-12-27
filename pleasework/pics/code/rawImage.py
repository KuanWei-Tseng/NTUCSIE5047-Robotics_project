import cv2
import numpy as np
from expand import expand

class rawImage:
    """
    image processing functions
    """
    # 3x3 kernel
    _kernel = np.ones((3,3), np.uint8)
    _vote = 150

    def __init__(self, img):
        self._row, self._column = img.shape[0], img.shape[1]
        self._img = np.copy(img)

    # returns the course deviation in pixel count
    def findDeviation(self):

        row, column = int(self._row/2), self._column
        # using only the lower half of the image
        img = np.copy(self._img[int(self._row/2):int(self._row), :])
        cv2.imwrite("../result/half.jpg", img)

        # expand the image
        #img = expand(img)
        #cv2.imwrite("../result/expanded.jpg", img)

        # yellow color mark (B < 80, G > 100, R > 100)
        y_cm = np.logical_and(np.logical_and(img[:,:,0] < 80, img[:,:,1] > 100), img[:,:,2] > 100).astype(np.uint8)
        # close then open
        y_cm = cv2.morphologyEx(cv2.morphologyEx(y_cm, cv2.MORPH_CLOSE, self._kernel), cv2.MORPH_OPEN, self._kernel)
        # dilate
        y_cm = cv2.dilate(y_cm, self._kernel, iterations = 1)
        cv2.imwrite("../result/y_mark.jpg", y_cm*255)

        # white color mark (B > 150, G > 150, R > 150)
        w_cm = np.logical_and(np.logical_and(img[:,:,0] > 120, img[:,:,1] > 120), img[:,:,2] > 120).astype(np.uint8)
        # close then open
        w_cm = cv2.morphologyEx(cv2.morphologyEx(w_cm, cv2.MORPH_CLOSE, self._kernel), cv2.MORPH_OPEN, self._kernel)
        # dilate
        w_cm = cv2.dilate(w_cm, self._kernel, iterations = 1)
        cv2.imwrite("../result/w_mark.jpg", w_cm*255)

        # gray scale canny edge detection
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur,50,150,apertureSize = 3)

        cv2.imwrite("../result/canny.jpg", edges)

        # intersection of canny and road markings
        y_inter = (edges * y_cm > 0).astype(np.uint8)
        w_inter = (edges * w_cm > 0).astype(np.uint8)
        y_inter = cv2.dilate(y_inter, self._kernel, iterations = 1)
        w_inter = cv2.dilate(w_inter, self._kernel, iterations = 1)
        cv2.imwrite("../result/y_inter.jpg", y_inter*255)
        cv2.imwrite("../result/w_inter.jpg", w_inter*255)

        # Hough line detection
        y_lines = cv2.HoughLines(y_inter, 1, np.pi/180, self._vote)
        w_lines = cv2.HoughLines(w_inter, 1, np.pi/180, self._vote)

        # find the rightmost yellow line
        y_rho, y_theta, y_offset = 0, 0, -float("inf")

        if y_lines is None:
            #print("can't find yellow lines")
            return 0, -1, -1

        for rho, theta in y_lines[:, 0]:
            # ignore horizontal lines
            # only shows lines that are in 80-degree difference to vertical line
            if theta < 80*np.pi/180 or (np.pi - theta) < 80*np.pi/180:
                offset = int(np.cos(theta)*rho-np.tan(theta)*(row-np.sin(theta)*rho))
                if offset > y_offset:
                    y_rho, y_theta, y_offset = rho, theta, offset

        if y_offset == -float("inf"):
            #print("y_offset is too small")
            return 0, 0, -1

        # find the leftmost white line
        w_rho, w_theta, w_offset = 0, 0, float("inf")

        if w_lines is None:
            #print("can't find white lines")
            return y_offset, 1, -1

        for rho, theta in w_lines[:, 0]:
            # ignore horizontal lines
            # only shows lines that are in 80-degree difference to vertical line
            if theta < 80*np.pi/180 or (np.pi - theta) < 80*np.pi/180:
                offset = int(np.cos(theta)*rho-np.tan(theta)*(row-np.sin(theta)*rho))
                if offset > y_offset and offset < w_offset:
                    w_rho, w_theta, w_offset = rho, theta, offset

        if w_offset == float("inf"):
            #print("w_offset is too big")
            return y_offset, 1, 0

        
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
            cv2.circle(img,(int(y_offset),int(self._row)),7,(0,255,255),5)
        if w_offset < self._column:
            cv2.circle(img,(int(w_offset),int(self._row)),7,(255,255,255),5)

        cv2.imwrite("../result/road_lines.jpg",img)
        
        print("y_offset = {}, w_offset = {}".format(y_offset, w_offset))
        
        error = 0
        middle = column/2 + error
        deviation = middle - int((w_offset + y_offset)/2)
        topy = int(np.cos(y_theta)*y_rho-np.tan(y_theta)*(-np.sin(y_theta)*y_rho))
        topw = int(np.cos(w_theta)*w_rho-np.tan(w_theta)*(-np.sin(w_theta)*w_rho))
        cv2.circle(img,(int(y_offset),int(row)),7,(0,255,255),5)
        cv2.circle(img,(int(w_offset),int(row)),7,(0,255,255),5)
        cv2.circle(img,(int(topy),int(0)),7,(0,255,255),5)
        cv2.circle(img,(int(topw),int(0)),7,(0,255,255),5)
        cv2.imwrite("../result/dots.jpg", img)
        print("topy = {}, topw = {}".format(topy, topw))
        print("y_offset = {}, w_offset = {}".format(y_offset, w_offset))
        """
        print("middle = {}".format(middle))
        print("deviation = {}".format(deviation))

        if deviation > 0:
            print("should go left {} pixels".format(deviation))
        elif deviation < 0:
            print("should go right {} pixels".format(-deviation))
        else:
            print("should go straight")
        """
        #print("deviation = {}".format(deviation))
        return deviation, 1, 1
