# Obstacle Warning System:
'''
This is a naive version.
''' 
from ultrasonic import ultrasonic
import time
import vars

class obws:
	dist = 0;    # buffer to store distance
	intdist = 0; # integrated distance
	counter = 0;

	def __init__(self):
		self.sonic = ultrasonic()
		print("Hello~Are you OK????")

	def safedriving(self):
		while not vars.shutdown:

				dist1 = self.sonic.measure()
				#print("distance: %f"%dist1)
				if dist1 < 50:
					time.sleep(0.1)
					if self.sonic.measure()< 50:
						vars.message = 0; # message: 0->about to crash
						#self.sendmesseage(message)
						continue
				if dist1 < self.dist:
					self.intdist += self.dist-dist1
				else:
					self.counter += 1
				if self.counter > 3:
					vars.message = 3 # message: 3->safe,moving away;
					self.intdist = 0
					self.counter = 0 	
				elif self.intdist > 80:
					vars.message = 1 # message: 1->warning, moving in;
				else:
					vars.message = 2 # message: 2->safe
				#self.sendmesseage(message)
				self.dist = dist1
				time.sleep(0.1)
		print("ended")

	def sendmesseage(self,message):
		mesdic = {
		0:"Emergency!!! About to crash.",
		1:"Warning!! There is an obstacle",
		2:"Safe Driving!",
		3:"Safe Driving: Moving away from obstacle"
		}
		#print(mesdic[message])
