# Ultra Sonic Ranging Sensor: HC-SR04
import RPi.GPIO as GPIO
import time

class ultrasonic:
	trigger_pin = 5
	echo_pin = 6
	temperature = 20 # in Celsius

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(trigger_pin,GPIO.OUT)
		GPIO.setup(echo_pin,GPIO.IN)

	def send_trigger():
		GPIO.output(trigger_pin,True)
		time.sleep(0.001)
		GPIO.output(trigger_pin,False)

	def receive_echo(countout = 5000):
		counter = countout
		# wait for echo(no more than 5000 counts)
		while GPIO.input(echo_pin) == False and counter > 0:
        	counter = counter - 1
		StartTime = time.time()
		counter = countout
		while GPIO.input(echo_pin) == True and counter > 0:
        	counter = counter - 1
		ReceiveTime = time.time()
		range = (ReceiveTime - StartTime)*(331+0.6*temperature)*100/2
		return range

	def measure():
		send_trigger()
		range = receive_echo()
		print("Distance = %f cm" %range)

	













