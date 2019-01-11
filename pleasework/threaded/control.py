class control:
    int_dev = 0
    prev_dev = 0
    Kp = 0.5
    Ki = 0
    Kd = 0
    Kw = 1
    Ky = 1
    T = 10
    def __init__(self):
        self.int_dev = 0
        self.dev = 0

    def findPIDval(self,dev):
        # dev: current deviation
        # prev_dev: previous deviation
        # P: Proportional term:
        P = self.Kp * self.dev
        # I: Integral term:
        I = self.Ki * (self.int_dev + self.dev)
        # D: Differential term:
        D = self.Kd * (self.dev - self.prev_dev)
        # Record current data:
        self.int_dev = self.int_dev + self.prev_dev
        self.prev_dev = dev
        # Calculate the PID control power
        PIDval = P + I + D
        return PIDval

    def PIDLanefollower(self,PIDval,centSpd):

        if abs(PIDval) < 20:
            return centSpd,centSpd
        if PIDval < 0:
            rightSpd = max(-100,centSpd-PIDval)
            leftSpd = min(100,centSpd+PIDval)
        else:
            rightSpd = min(100,centSpd+PIDval)
            leftSpd = max(-100,centSpd-PIDval)

        return rightSpd, leftSpd

    def adaptive_control(self,rightSpd,leftSpd,dev,theta,type):
        centSpd = (rightSpd+leftSpd)/2

        if type == "b":
            PIDval = self.findPIDval(dev)

        elif type == "w":
            dev = (-1)*abs(600-dev)* self.Kw  # Case: Turning Left 
            PIDval = self.findPIDval(dev)
            
        elif type == "y":
            dev = abs(dev)* self.Ky
            PIDval = self.findPIDval(dev)

        rightSpd, leftSpd = self.PIDLanefollower(PIDval,centSpd)
        return rightSpd, leftSpd

    def fix(self,rightSpd, leftSpd, dev, theta, type):
        if type == "b":
        # both line found, dev is the deviation
            if dev > 20:
                # should go left
                rightSpd = 80
                leftSpd = 20
            elif dev < -20:
                # should go right
                rightSpd = 20
                leftSpd = 80
            else:
                # go straight
                rightSpd = 50
                leftSpd = 50
        elif type == "y":
        # only found yellow line, dev is y_offset
            if dev > 10:
                # should go right
                rightSpd = 40
                leftSpd = 90
            else:
                # go straight
                rightSpd = 50
                leftSpd = 50

        elif type == "w":
        # only found white line, dev is w_offset
            if dev < 650:
                # should go left
                rightSpd = 90
                leftSpd = 40
            else:
                # go straight
                rightSpd = 50
                leftSpd = 50
        else:
            # stop
            rightSpd = 0
            leftSpd = 0
        return rightSpd, leftSpd
        
