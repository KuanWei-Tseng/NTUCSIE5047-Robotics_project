import cv2
import numpy as np

class rawImage:
    
    # 3-5-5-5-3 octogonal kernel
    _kernel = np.ones((5, 5), np.uint8)
    _kernel[0,0] = _kernel[4,0] = _kernel[0,4] = kernel[4,4] = 0

    def __init__(self, img):
        self._row, self._column = img.shape[0], img.shape[1]
        self._img = np.copy(img)

    # returns the course deviation in pixel count
    def find_deviation(self):
        
        # yellow and white markings detection
        color_mark = np.logical_and(self._img[:,:,1] > 180, self._img[:,:,2] > 180).astype(np.uint8)

        # close then open
        color_mark = cv2.morphologyEx(cv2.morphologyEx(color_mark, cv2.MORPH_CLOSE, self._kernel), cv2.MORPH_OPEN, self._kernel)

        # gray scale canny edge detection
        gray = cv2.cvtColor(self._img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        edges = cv2.Canny(blur, 50, 150, apertureSize = 3)

        #cv2.imwrite('canny.jpg', edges)

        # intersection of canny and road markings
        intersection = (edges * color_mark > 0).astype(np.uint8)

        # Hough line detection
        lines = cv2.HoughLines(intersection,1,np.pi/180,80)

        # records the rightmost line on the lefthand side and the leftmost line on the righthand side
        left_max, right_min = 0, self._column

        for i in range(0, len(lines)):
            for rho,theta in lines[i]:
                # lines that are in 60-degree difference to vertical line
                if theta < 60*np.pi/180 or (np.pi - theta) < 60*np.pi/180:

                    x0 = rho * np.cos(theta)
                    y0 = rho * np.sin(theta)
                    
                    offset = int(x0-np.tan(theta)*(self._row-y0))
                    if offset > self._column/2 and offset < right_min:
                        right_min = offset
                    elif offset < self._column/2 and offset > left_max:
                        left_max = offset

        return right_min + left_max - self._column
