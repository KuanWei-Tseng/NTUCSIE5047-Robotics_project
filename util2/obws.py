# Obstacle Warning System:
'''
This is a naive version.
''' 
from ultrasonic import ultrasonic
import time

class obws:
	dist = 0;    # buffer to store distance
	intdist = 0; # integrated distance
	counter = 0;

	def __init__(self):
		self.sonic = ultrasonic()

	def safedriving(self):
		while True:
			try:
				dist1 = self.sonic.measure()
				print("distance: %f"%dist1)
				if dist1 < 30:
					time.sleep(0.1)
					if self.sonic.measure()< 30:
						message = 0; # message: 0->about to crash
						self.sendmesseage(message)
						continue
				if dist1 < self.dist:
					self.intdist += self.dist-dist1
				else:
					self.counter += 1
				if self.counter > 3:
					message = 3 # message: 3->safe,moving away;
					self.intdist = 0
					self.counter = 0 	
				elif self.intdist > 80:
					message = 1 # message: 1->warning, moving in;
				else:
					message = 2 # message: 2->safe
				self.sendmesseage(message)
				self.dist = dist1
				time.sleep(0.1)
			except KeyboardInterrupt:
				print("Process Aborted!")
				quit()

	def sendmesseage(self,message):
		mesdic = {
		0:"Emergency!!! About to crash.",
		1:"Warning!! There is an obstacle",
		2:"Safe Driving!",
		3:"Safe Driving: Moving away from obstacle"
		}
		print(mesdic[message])






