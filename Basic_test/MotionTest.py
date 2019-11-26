import time
from car import car
import RPi.GPIO as GPIO

Mycar = car()
while True:
	cmdlist = ['f','r','c']
	keyin = input("Input Command:")
	cmd = keyin[0]
	if cmd not in cmdlist:
		print("Invalid Command. Process Killed.\n")
		GPIO.cleanup()
		quit()
	if cmd == "f":
		Mycar.setSpeed(50,50);
		time.sleep(0.4)
		for i in range(0,6):
			Mycar.setSpeed(100,0);
			time.sleep(0.4)
			Mycar.setSpeed(0,0);
			time.sleep(0.2)
			Mycar.setSpeed(50,50);
			time.sleep(0.2)
		Mycar.setSpeed(50,50);
	elif cmd == "r":
		Mycar.setSpeed(50,50)
		time.sleep(0.5)
		for i in range(0,3):
			Mycar.setSpeed(0,100);
			time.sleep(0.4)
			Mycar.setSpeed(0,0);
			time.sleep(0.2)
			Mycar.setSpeed(50,50);
			time.sleep(0.2)
		Mycar.setSpeed(50,50);
		time.sleep(0.5)
	else:
		Mycar.setSpeed(50,50);
		time.sleep(0.2)
		Mycar.setSpeed(0,0);
