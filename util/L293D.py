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

def clockwise():
    GPIO.output(in1_pin, True)
    GPIO.output(in2_pin, False)
    GPIO.output(in3_pin, True)
    GPIO.output(in4_pin, False)
    GPIO.output(in5_pin, True)
    GPIO.output(in6_pin, False)
    GPIO.output(in7_pin, True)
    GPIO.output(in8_pin, False)

def counter_clockwise():
    GPIO.output(in1_pin, False)
    GPIO.output(in2_pin, True)
    GPIO.output(in3_pin, False)
    GPIO.output(in4_pin, True)
    GPIO.output(in6_pin, True)
    GPIO.output(in5_pin, False)
    GPIO.output(in8_pin, True)
    GPIO.output(in7_pin, False)
    
while True:
    cmd = input("Condition: f:forward,b:backward, 0-9. Ex. f9:")
    direction = cmd[0]
    if direction == "f":
        clockwise()
    elif direction == "b":
        counter_clockwise()
    else:
        GPIO.cleanup()
        quit()
    speed = int(cmd[1]) * 11
    pwm1.ChangeDutyCycle(speed)
    pwm2.ChangeDutyCycle(speed)



