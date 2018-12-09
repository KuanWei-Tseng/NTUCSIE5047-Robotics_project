import time
import RPi.GPIO as GPIO

enable1_pin = 17
enable2_pin = 13
in1_pin = 27
in2_pin = 22
in3_pin = 18
in4_pin = 23
in5_pin = 19
in6_pin = 26
in7_pin = 16
in8_pin = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(enable1_pin, GPIO.OUT)
GPIO.setup(enable2_pin, GPIO.OUT)
GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)
GPIO.setup(in5_pin, GPIO.OUT)
GPIO.setup(in6_pin, GPIO.OUT)
GPIO.setup(in7_pin, GPIO.OUT)
GPIO.setup(in8_pin, GPIO.OUT)
pwm1 = GPIO.PWM(enable1_pin, 500)
pwm2 = GPIO.PWM(enable2_pin, 500)
pwm1.start(0)
pwm2.start(0)

def change_rotating_speed(side,speed):
	if side == 1:
		pwm1.ChangeDutyCycle(speed)
	else:
		pwmt.ChangeDutyCycle(speed)

def change_rotating_direction(side,drt):
	if side == 1:
		GPIO.output(in1_pin,drt)
		GPIO.output(in1_pin,not drt)
		GPIO.output(in3_pin,drt)
		GPIO.output(in4_pin,not drt)		
	else:
		GPIO.output(in5_pin,drt)
		GPIO.output(in6_pin,not drt)
		GPIO.output(in7_pin,drt)
		GPIO.output(in8_pin,not drt)		

def goforward(speed):
	change_rotating_direction(1,True)
	change_rotating_direction(-1,True)
	change_rotating_speed(1,speed)
	change_rotating_speed(-1,speed)

def reversing(speed):
	change_rotating_direction(1,False)
	change_rotating_direction(-1,False)
	change_rotating_speed(1,speed)
	change_rotating_speed(-1,speed)

def fixdeviation(speed,devlev):
	# devlev positive: right deviation / negative: left deviation
	# devlev(1-5): 5:totally out of control. Emergency Stop.
	side = devlev/abs(devlev)
	if abs(devlev) >= 5:
		change_rotating_speed(1,0)
		change_rotating_speed(-1,0)
		pwm2.ChangeDutyCycle(0)
		print("Stop! Wait for next command. \n")
	else:
		if speed < 95-abs(devlev)*10:
			delta = 10*devlev
			change_rotating_speed(side,delta)
		else:
			delta = 10*devlev
			change_rotating_speed(side,speed+delta)
			change_rotating_speed(-side,max(speed-delta,0))

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
