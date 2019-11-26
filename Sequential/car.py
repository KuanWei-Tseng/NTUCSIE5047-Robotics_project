import RPi.GPIO as GPIO

class car:
	enable1_pin = 17
	enable2_pin = 13
	in1_pin = 27
	in2_pin = 22
	in3_pin = 18
	in4_pin = 23
	in5_pin = 26
	in6_pin = 19
	in7_pin = 16
	in8_pin = 20

	def __init__(self):
		"""
		set the pins and init speed parameters
		"""
		self.Rspd = 0
		self.Lspd = 0
		self.Rdrt = True
		self.Ldrt = True
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.enable1_pin, GPIO.OUT)
		GPIO.setup(self.enable2_pin, GPIO.OUT)
		GPIO.setup(self.in1_pin, GPIO.OUT)
		GPIO.setup(self.in2_pin, GPIO.OUT)
		GPIO.setup(self.in3_pin, GPIO.OUT)
		GPIO.setup(self.in4_pin, GPIO.OUT)
		GPIO.setup(self.in5_pin, GPIO.OUT)
		GPIO.setup(self.in6_pin, GPIO.OUT)
		GPIO.setup(self.in7_pin, GPIO.OUT)
		GPIO.setup(self.in8_pin, GPIO.OUT)
		self.pwm1 = GPIO.PWM(self.enable1_pin, 500)
		self.pwm2 = GPIO.PWM(self.enable2_pin, 500)
		self.pwm1.start(0)
		self.pwm2.start(0)

	def change_rotating_speed(self, side, speed):
		"""
		set the rotating speed
		side = 1 -> right wheels
		side = -1 -> left wheels
		"""
		# speed is out of bound
		if speed > 100 or speed < 0:
			print("speed input is {}, out of bound".format(speed))

		# set right speed
		if side == 1:
			self.Rspd = speed
			self.pwm1.ChangeDutyCycle(speed)

		# set left speed
		else:
			self.Lspd = speed
			self.pwm2.ChangeDutyCycle(speed)

	def change_rotating_direction(self, side, drt):
		"""
		set the rotating direction
		side = 1 -> right wheels
		side = -1 -> left wheels
		drt = True -> forward
		drt = False -> backward
		"""
		# invalid direction
		if drt != True and drt != False:
			print("drt is {}, should be True or False".format(drt))

		# set right direction
		if side == 1:
			self.Rdrt = drt
			GPIO.output(self.in1_pin,drt)
			GPIO.output(self.in2_pin,not drt)
			GPIO.output(self.in3_pin,drt)
			GPIO.output(self.in4_pin,not drt)		
		# set left direction
		else:
			self.Ldrt = drt
			GPIO.output(self.in5_pin,drt)
			GPIO.output(self.in6_pin,not drt)
			GPIO.output(self.in7_pin,drt)
			GPIO.output(self.in8_pin,not drt)		
			
	def forward(self, speed):
		"""
		go forward with spd = speed
		"""
		self.change_rotating_direction(1,True)
		self.change_rotating_direction(-1,True)
		self.change_rotating_speed(1,speed)
		self.change_rotating_speed(-1,speed)

	def backward(self, speed):
		"""
		go backward with spd = speed
		"""
		self.change_rotating_direction(1,False)
		self.change_rotating_direction(-1,False)
		self.change_rotating_speed(1,speed)
		self.change_rotating_speed(-1,speed)

	def stop(self):
		"""
		stop the car
		"""
		self.change_rotating_speed(1, 0)
		self.change_rotating_speed(-1, 0)
		self.change_rotating_direction(1, True)
		self.change_rotating_direction(-1, True)

	def setSpeed(self, rightSpd, leftSpd):
		"""
		set the speed and the rotating direction of the left and right wheels
		leftSpd and rightSpd could be negative numbers between -100 and 100
		negative number means reversing
		"""
		# right reversing
		if rightSpd < 0:
			self.change_rotating_direction(1, False)
			self.change_rotating_speed(1, -rightSpd)
		# right forwarding
		else:
			self.change_rotating_direction(1, True)
			self.change_rotating_speed(1, rightSpd)
			
		# left reversing
		if leftSpd < 0:
			self.change_rotating_direction(-1, False)
			self.change_rotating_speed(-1, -leftSpd)
		# left forwarding
		else:
			self.change_rotating_direction(-1, True)
			self.change_rotating_speed(-1, leftSpd)
	
	def getSpeed(self):
		"""
		return rightSpd and leftSpd
		"""
		rightSpd, leftSpd = self.Rspd, self.Lspd
		# right reversing
		if self.Rdrt == False:
			rightSpd = -self.Rspd

		# left reversing
		if self.Ldrt == False:
			leftSpd = -self.Lspd
		
		return rightSpd, leftSpd

	def fixdeviation(self, devlev):
		# devlev positive: right deviation / negative: left deviation
		# devlev(1-5): 5:totally out of control. Emergency Stop.

		# go forward
		if devlev == 0:
			self.goforward(self.Lspd)
			return

		# side > 0: should go left
		# side < 0: should go right
		side = devlev/abs(devlev)

		if abs(devlev) >= 5:
			self.change_rotating_speed(1,0)
			self.change_rotating_speed(-1,0)
			self.pwm1.ChangeDutyCycle(0)
			self.pwm2.ChangeDutyCycle(0)
			print("Stop! Wait for next command. \n")

		if side > 0:
			a = self.Rspd
			b = self.Lspd
		else:
			a = self.Lspd
			b = self.Rspd

		if (abs(devlev) == 1 and a <= b) or (abs(devlev) >= 2 and abs(devlev) <= 4):
			self.change_rotating_speed(side,max(a+abs(devlev), 9))
			self.change_rotating_speed(-side,min(b-abs(devlev), 0))

	def turnoff(self):
		"""
		called to stop the car and cleanup GPIO
		"""
		self.stop()
		GPIO.cleanup()
		quit()
