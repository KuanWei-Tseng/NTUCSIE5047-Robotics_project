import time
import RPi.GPIO as GPIO

class car:
    enable1_pin = 17
    enable2_pin = 13
    in1_pin = 27
    in2_pin = 22
    in3_pin = 23
    in4_pin = 18
    in5_pin = 26
    in6_pin = 19
    in7_pin = 20
    in8_pin = 16

    def __init__(self):
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

    def forward(self, leftSpd = 75, rightSpd = 75):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        GPIO.output(self.in3_pin, GPIO.HIGH)
        GPIO.output(self.in4_pin, GPIO.LOW)
        GPIO.output(self.in5_pin, GPIO.HIGH)
        GPIO.output(self.in6_pin, GPIO.LOW)
        GPIO.output(self.in7_pin, GPIO.HIGH)
        GPIO.output(self.in8_pin, GPIO.LOW)
        if leftSpd >= 88:
            leftSpd = 88
        if rightSpd >= 88:
            rightSpd = 88
        self.pwm1.ChangeDutyCycle(leftSpd)
        self.pwm2.ChangeDutyCycle(rightSpd)
        
    def backward(self, leftSpd = 75, rightSpd = 75):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.HIGH)
        GPIO.output(self.in5_pin, GPIO.LOW)
        GPIO.output(self.in6_pin, GPIO.HIGH)
        GPIO.output(self.in7_pin, GPIO.LOW)
        GPIO.output(self.in8_pin, GPIO.HIGH)
        if leftSpd >= 88:
            leftSpd = 88
        if rightSpd >= 88:
            rightSpd = 88
        self.pwm1.ChangeDutyCycle(leftSpd)
        self.pwm2.ChangeDutyCycle(rightSpd)
    
    def stop(self):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.LOW)
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.LOW)
        GPIO.output(self.in5_pin, GPIO.LOW)
        GPIO.output(self.in6_pin, GPIO.LOW)
        GPIO.output(self.in7_pin, GPIO.LOW)
        GPIO.output(self.in8_pin, GPIO.LOW)

    def turnLeftSharp(self, leftSpd = 75, rightSpd = 75):
        GPIO.output(self.in1_pin, GPIO.LOW)
        GPIO.output(self.in2_pin, GPIO.HIGH)
        GPIO.output(self.in3_pin, GPIO.LOW)
        GPIO.output(self.in4_pin, GPIO.HIGH)
        GPIO.output(self.in5_pin, GPIO.HIGH)
        GPIO.output(self.in6_pin, GPIO.LOW)
        GPIO.output(self.in7_pin, GPIO.HIGH)
        GPIO.output(self.in8_pin, GPIO.LOW)
        if leftSpd >= 88:
            leftSpd = 88
        if rightSpd >= 88:
            rightSpd = 88
        self.pwm1.ChangeDutyCycle(leftSpd)
        self.pwm2.ChangeDutyCycle(rightSpd)

    def turnRightSharp(self, leftSpd = 75, rightSpd = 75):
        GPIO.output(self.in1_pin, GPIO.HIGH)
        GPIO.output(self.in2_pin, GPIO.LOW)
        GPIO.output(self.in3_pin, GPIO.HIGH)
        GPIO.output(self.in4_pin, GPIO.LOW)
        GPIO.output(self.in5_pin, GPIO.LOW)
        GPIO.output(self.in6_pin, GPIO.HIGH)
        GPIO.output(self.in7_pin, GPIO.LOW)
        GPIO.output(self.in8_pin, GPIO.HIGH)
        if leftSpd >= 88:
            leftSpd = 88
        if rightSpd >= 88:
            rightSpd = 88
        self.pwm1.ChangeDutyCycle(leftSpd)
        self.pwm2.ChangeDutyCycle(rightSpd)

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self.stop()
            GPIO.cleanup()
        except RuntimeWarning:
            return True
