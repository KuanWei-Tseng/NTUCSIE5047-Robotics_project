from AMSpi import AMSpi

class car:
    """
    car action functions
    """
    def __init__(self):
        self.amspi = AMSpi()
        # Calling AMSpi() we will use default pin numbering: BCM (use GPIO numbers)
        # if you want to use BOARD numbering do this: "with AMSpi(True) as amspi:"

        # Set PINs for controlling shift register (GPIO numbering)
        self.amspi.set_74HC595_pins(21, 20, 16)
        # Set PINs for controlling all 4 motors (GPIO numbering)
        self.amspi.set_L293D_pins(5, 6, 13, 19)

    def forward(self, spd = 100):
        print("GO: clockwise")
        self.amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2], clockwise = False, speed = spd)
        self.amspi.run_dc_motors([amspi.DC_Motor_3, amspi.DC_Motor_4], speed = spd)
        
    def stop(self):
        print("Stop")
        self.amspi.stop_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2, amspi.DC_Motor_3, amspi.DC_Motor_4])

    def backward(self, spd = 100):
        print("GO: counterclockwise")
        self.amspi.run_dc_motors([amspi.DC_Motor_1, amspi.DC_Motor_2], speed = spd)
        self.amspi.run_dc_motors([amspi.DC_Motor_3, amspi.DC_Motor_4], clockwise = False, speed = spd)

    def turnRight(self, leftSpd = 100, rightSpd = 50):
        print("Turn right")
        self.amspi.run_dc_motor(amspi.DC_Motor_1, clockwise = False, speed = rightspd)
        self.amspi.run_dc_motor(amspi.DC_Motor_2, clockwise = False, speed = leftspd)
        self.amspi.run_dc_motor(amspi.DC_Motor_3, speed = rightspeed)
        self.amspi.run_dc_motor(amspi.DC_Motor_4, speed = leftSpd)

    def turnLeft(self, leftSpd = 50, rightSpd = 100):
        print("Turn left")
        self.amspi.run_dc_motor(amspi.DC_Motor_1, clockwise = False, speed = rightspd)
        self.amspi.run_dc_motor(amspi.DC_Motor_2, clockwise = False, speed = leftspd)
        self.amspi.run_dc_motor(amspi.DC_Motor_3, speed = rightspeed)
        self.amspi.run_dc_motor(amspi.DC_Motor_4, speed = leftSpd)
