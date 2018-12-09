import RPi.GPIO as GPIO
import time

trig_pin = 5
echo_pin = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(trig_pin, GPIO.OUT)
GPIO.setup(echo_pin, GPIO.IN)

def send_trigger_pulse():
    GPIO.output(trig_pin, True)
    time.sleep(0.001)
    GPIO.output(trig_pin, False)

def wait_for_echo(value, timeout):
    count = timeout
    while GPIO.input(echo_pin) != value and count > 0:
        count = count - 1

def get_distance():
    send_trigger_pulse()
    wait_for_echo(True, 5000)
    start = time.time()
    wait_for_echo(False, 5000)
    finish = time.time()
    pulse_len = finish - start
    distance_cm = pulse_len * 340 *100 /2
    distance_in = distance_cm / 2.5
    return (distance_cm, distance_in)

while True:
    print("cm=%f\tinches=%f" % get_distance())
    time.sleep(1)
