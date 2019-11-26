class control:
    int_dev = 0
    prev_dev = 0
    Kp = 0.5
    Ki = 0
    Kd = 0.1
    Kw = 1
    Ky = 1
    T = 10
    def __init__(self):
        self.int_dev = 0
        self.prev_dev = 0

    def findPIDval(self,dev):
        # dev: current deviation
        # prev_dev: previous deviation
        # P: Proportional term:
        P = self.Kp * dev
        # I: Integral term:
        I = self.Ki * (self.int_dev + dev)
        # D: Differential term:
        D = self.Kd * (dev - self.prev_dev)
        # Record current data:
        self.int_dev = self.int_dev + self.prev_dev
        self.prev_dev = dev
        # Calculate the PID control power
        PIDval = P + I + D
        print("PID:{}".format(PIDval))
        return PIDval

    def PIDLanefollower(self,PIDval,centSpd):
        print("centSpd:{}".format(centSpd))
        if abs(PIDval) < 10:
            centSpd = 50
            return centSpd,centSpd
        if PIDval < 0:
            rightSpd = max(40,centSpd+PIDval)
            leftSpd = min(60,centSpd-PIDval)
        else:
            rightSpd = min(90,centSpd+PIDval)
            leftSpd = max(20,centSpd-PIDval)

        return rightSpd, leftSpd

    def adaptive_control(self,rightSpd,leftSpd,dev,theta,type):
        centSpd = (rightSpd+leftSpd)/2

        if type == "b":
            PIDval = self.findPIDval(dev)

        elif type == "w":
            dev = 500  # Case: Turning Left 
            PIDval = self.findPIDval(dev)
            
        elif type == "y":
            dev = -500
            PIDval = self.findPIDval(dev)
        elif type == "n":
            rightSpd = 50
            leftSped = 40
            return rightSpd, leftSpd
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
        
