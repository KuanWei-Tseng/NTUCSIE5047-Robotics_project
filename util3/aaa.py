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
		self.Lspd = 0
		self.Rspd = 0
		self.Ldrt = True
		self.Rdrt = True
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
		if side == 1:
			self.Rspd = speed
			self.pwm1.ChangeDutyCycle(min(speed*11,100))
		else:
			self.Lspd = speed
			self.pwm2.ChangeDutyCycle(max(speed*11,0))

	def change_rotating_direction(self, side, drt):
		if side == 1:
			self.Rdrt = drt
			GPIO.output(self.in1_pin,drt)
			GPIO.output(self.in2_pin,not drt)
			GPIO.output(self.in3_pin,drt)
			GPIO.output(self.in4_pin,not drt)		
		else:
			self.Ldrt = drt
			GPIO.output(self.in5_pin,drt)
			GPIO.output(self.in6_pin,not drt)
			GPIO.output(self.in7_pin,drt)
			GPIO.output(self.in8_pin,not drt)		
			
	def goforward(self, speed):
		self.Lspd = speed
		self.Rspd = speed
		self.Ldrt = True
		self.Rdrt = True
		self.change_rotating_direction(1,True)
		self.change_rotating_direction(-1,True)
		self.change_rotating_speed(1,speed)
		self.change_rotating_speed(-1,speed)

	def reversing(self, speed):
		self.Lspd = speed
		self.Rspd = speed
		self.Ldrt = False
		self.Rdrt = False
		self.change_rotating_direction(1,False)
		self.change_rotating_direction(-1,False)
		self.change_rotating_speed(1,speed)
		self.change_rotating_speed(-1,speed)

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

	def stop(self):
		self.change_rotating_speed(1, 0)
		self.change_rotating_speed(-1, 0)
		
	def turnoff(self):
		self.stop()
		GPIO.cleanup()
		quit()

"""
speed  = 0

while True:
	cmdlist = ['f','r','c']
	keyin = input("Input Command:")
	cmd = keyin[0]
	if cmd not in cmdlist:
		print("Invalid Command. Process Killed.\n")
		GPIO.cleanup()
		quit()
	if cmd == "f":
		mag = int(keyin[1])
		speed = mag*11
		goforward(speed)
	elif cmd == "r":
		mag = int(keyin[1])
		speed = mag*11
		reversing(speed)
	else:
		if len(keyin) < 3 or keyin[2] not in ['+','-']:
			print("Invalid Command. Please input again.\n")
		drt = int(keyin[1])
		mag = int(keyin[2])
		if drt == "+":
			fixdeviation(speed,mag)
		else:
			fixdeviation(speed,-mag)
"""
