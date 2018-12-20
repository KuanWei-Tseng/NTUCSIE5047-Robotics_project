# Ultra Sonic Ranging Sensor: HC-SR04
import RPi.GPIO as GPIO
import time

class ultrasonic:
	trigger_pin = 5
	echo_pin = 6
	temperature = 20 # in Celsius

	def __init__(self):
		GPIO.setmode(GPIO.BCM)
		GPIO.setup(self.trigger_pin,GPIO.OUT)
		GPIO.setup(self.echo_pin,GPIO.IN)

	def __del__(self):
		GPIO.cleanup()

	def send_trigger(self):
		GPIO.output(self.trigger_pin,True)
		time.sleep(0.001)
		GPIO.output(self.trigger_pin,False)

	def receive_echo(self,countout = 5000):
		counter = countout
		# wait for echo(no more than 5000 counts)
		while GPIO.input(self.echo_pin) == False and counter > 0:
	        	counter = counter-1
		StartTime = time.time()
		counter = countout
		while GPIO.input(self.echo_pin) == True and counter > 0:
        		counter = counter-1
		return StartTime

	def measure(self):
		self.send_trigger()
		StartTime = self.receive_echo()
		ReceiveTime = time.time()
		distance = (ReceiveTime - StartTime)*(331+0.6*self.temperature)*100/2
		# print("Distance = %f cm\n" %distance)
		return distance



	













