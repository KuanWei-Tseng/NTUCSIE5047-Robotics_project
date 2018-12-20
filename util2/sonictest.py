from ultrasonic import ultrasonic
import time

sonic = ultrasonic()
while True:
	sonic.measure()
	time.sleep(0.1)
