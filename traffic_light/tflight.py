import numpy as np
import cv2
import copy
from camera import camera
from rawImage import rawImage

def grab_contours(cnts):
    # if the length the contours tuple returned by cv2.findContours
    # is '2' then we are using either OpenCV v2.4, v4-beta, or
    # v4-official
    if len(cnts) == 2:
        cnts = cnts[0]

    # if the length of the contours tuple is '3' then we are using
    # either OpenCV v3, v4-pre, or v4-alpha
    elif len(cnts) == 3:
        cnts = cnts[1]

    # otherwise OpenCV has changed their cv2.findContours return
    # signature yet again and I have no idea WTH is going on
    else:
        raise Exception(("Contours tuple must have length 2 or 3, "
            "otherwise OpenCV changed their cv2.findContours return "
            "signature yet again. Refer to OpenCV's documentation "
            "in that case"))

    # return the actual contours array
    return cnts

class ShapeDetector:
	def __init__(self):
		pass
 
	def detect(self, c):
		# initialize the shape name and approximate the contour
		shape = "unidentified"
		peri = cv2.arcLength(c, True)
		approx = cv2.approxPolyDP(c, 0.04 * peri, True)

				# if the shape is a triangle, it will have 3 vertices
		if len(approx) == 3:
			shape = "triangle"
 
		# if the shape has 4 vertices, it is either a square or
		# a rectangle
		elif len(approx) == 4:
			# compute the bounding box of the contour and use the
			# bounding box to compute the aspect ratio
			(x, y, w, h) = cv2.boundingRect(approx)
			ar = w / float(h)
 
			# a square will have an aspect ratio that is approximately
			# equal to one, otherwise, the shape is a rectangle
			shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
 
		# if the shape is a pentagon, it will have 5 vertices
		elif len(approx) == 5:
			shape = "pentagon"
 
		# otherwise, we assume the shape is a circle
		else:
			shape = "circle"
 
		# return the name of the shape
		return shape
		

def light_detector(sub_img):
	img_hsv = cv2.cvtColor(sub_img, cv2.COLOR_RGB2HSV)
	green_mask_upper = np.array([70, 255, 255])
	green_mask_lower = np.array([36, 0, 0])
	green_mask = cv2.inRange(img_hsv, green_mask_lower, green_mask_upper)
	
	percentage_green = np.count_nonzero(green_mask) / (sub_img.shape[0]*sub_img.shape[1])
	#print(percentage_green)
	if percentage_green > 0.15:
		return "green"
		
	red_mask_upper = np.array([0, 70, 50])
	red_mask_lower = np.array([10, 255, 255])
	red_mask1 = cv2.inRange(img_hsv, red_mask_lower, red_mask_upper)

	red_mask_upper = np.array([170, 70, 50])
	red_mask_lower = np.array([180, 255, 255])
	red_mask2 = cv2.inRange(img_hsv, red_mask_lower, red_mask_upper)
	
	red_mask = red_mask1 + red_mask2
	percentage_red = np.count_nonzero(red_mask) / (sub_img.shape[0]*sub_img.shape[1])
	#print(percentage_red)

	if percentage_red > 0.15:
		return "red"
		
	return "no light"
	


#filename = sys.argv[1]
#img = cv2.imread("test4_7.jpg")
myCar = car()
myCamera = camera()

while True:
    try:
        # get the image from camera
		cap_img = myCamera.capture()
		img = rawImage(cap_img)
		myCamera.trunc()
        row,column = img.shape[0], img.shape[1]
        image = np.zeros((int(row/2),int(column))).astype(np.uint8)
        image = img[0:int(row/2),int(0):column]
        image_buff = copy.copy(image)
        # convert the resized image to grayscale, blur it slightly,
        # and threshold it			
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.threshold(blurred, 100, 255, cv2.cv2.THRESH_BINARY_INV)[1]

        # find contours in the thresholded image and initialize the
        # shape detector
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
	    cv2.CHAIN_APPROX_SIMPLE)
        cnts = grab_contours(cnts)

        sd = ShapeDetector()
        # loop over the contours
        for c in cnts:
	    # compute the center of the contour, then detect the name of the
	    # shape using only the contour
	        shape = sd.detect(c)
	        area = cv2.contourArea(c)
	        if shape == "rectangle" and area >= 500 and area <=5000:
		        (x, y, w, h) = cv2.boundingRect(c)
		        sub_img = np.zeros((int(h),int(w))).astype(np.uint8)
		        sub_img = image_buff[y:y+h, x:x+w]
		        check_black = np.zeros((int(h),int(w))).astype(np.uint8)
		        check_black = np.logical_and(sub_img[:,:,0] < 70, np.logical_and(sub_img[:,:,1] < 70 ,sub_img[:,:,2] < 70))
		        black_count = check_black.sum()
		        black_ratio = black_count / (h*w)
		        #print(black_ratio)
		        if black_ratio > 0.4:
			        signal_light = light_detector(sub_img)
			        print(signal_light)
			        c = c.astype("float")
			        c = c.astype("int")
			        cv2.drawContours(image, [c], -1, (0, 255, 0), 2)

        cv2.imshow("traffic_light", image)

