import numpy as np
import cv2
import copy

class LightDetection():
	def __init__(self, img):
		self._row, self._column = img.shape[0], img.shape[1]
		self._img = np.copy(img)
		
	def light_detector(self, sub_img):
		img_hsv = cv2.cvtColor(sub_img, cv2.COLOR_RGB2HSV)
		green_mask_upper = np.array([110, 255, 255])
		green_mask_lower = np.array([80, 0, 0])
		green_mask = cv2.inRange(img_hsv, green_mask_lower, green_mask_upper)
	
		percentage_green = np.count_nonzero(green_mask) / (sub_img.shape[0]*sub_img.shape[1])
		#print("green:")
		#print(percentage_green)
		if percentage_green > 0.3:
			return "green"
		
		red_mask_upper = np.array([30, 255, 255])
		red_mask_lower = np.array([0, 0, 0])
		red_mask1 = cv2.inRange(img_hsv, red_mask_lower, red_mask_upper)

		red_mask_upper = np.array([140, 255, 255])
		red_mask_lower = np.array([110, 0, 0])
		red_mask2 = cv2.inRange(img_hsv, red_mask_lower, red_mask_upper)
	
		red_mask = red_mask1 + red_mask2
		percentage_red = np.count_nonzero(red_mask) / (sub_img.shape[0]*sub_img.shape[1])
		#print("red:")
		#print(percentage_red)

		if percentage_red > 0.3:
			return "red"
		
		return "no light"

	def grab_contours(self, cnts):
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

	def find_light(self):

		image = np.copy(self._img[0:int(3*self._row/7), int(self._column/3):self._column])
		#image = np.copy(self._img)
		# convert the resized image to grayscale, blur it slightly,
		# and threshold it			
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

		blurred = cv2.GaussianBlur(gray, (5, 5), 0)
		
		thresh = cv2.threshold(blurred,225,255,cv2.THRESH_BINARY)[1]

		# find contours in the thresholded image and initialize the
		# shape detector

		cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
		cnts = self.grab_contours(cnts)
		# loop over the contours
		signal = "NULL"
		for c in cnts:
			area = cv2.contourArea(c)
			if area >= 20 and area <= 80:
				(x, y, w, h) = cv2.boundingRect(c)
				sub_img = np.zeros((int(h),int(w))).astype(np.uint8)
				#boundaries of light
				up = max(0, y-15)
				down = min(int(3*self._row/7),y+15)
				left = max(0, x-15)
				right = min(int(2*self._column/3),x+15)
				# debug (whole picture)				
				'''up = max(0, y-15)
				down = min(self._row, y+15)
				left = max(0, x-15)
				right = min(self._column, x+15)'''
				sub_img = image[up:down, left:right]
				signal_light = self.light_detector(sub_img)
				
				if signal_light == "red" or signal_light == "green":
					signal = signal_light
				c = c.astype("float")
				c = c.astype("int")
				
				#cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
				#cv2.imwrite('find.jpg',sub_img)
		return signal
