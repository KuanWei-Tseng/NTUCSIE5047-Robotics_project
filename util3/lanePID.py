# Motor Behavior Calculation and Control Unit
'''
Responisble for calculating the desirable speed(duty cycle) of
two motors and return the value to core.

Input: current speed,deviation,previous deviation
Method: 

'''

import vars

# Gain Factors:
# Kp: proportional gain factor:
Kp = 0.5
# Ki: integral gain factor:
Ki = 0
# Kd: differential gain factor:
Kd = 0

# PID controller threshold:
T = 10

def findPIDval(dev,int_dev,prev_dev):
    # dev: current deviation
    # prev_dev: previous deviation
    # P: Proportional term:
    P = Kp * dev
    # I: Integral term:
    I = Ki * (int_dev + dev)
    # D: Differential term:
    D = Kd * (dev - prev_dev)
    PIDval = P + I + D
    vars

    return PIDval,(int_dev+dev)

def PIDLanefollower(PIDval,centSpd,y,w):
    # PIDval: control variable
    # centSpd: Speed of the center of the car
    # y,w: Lane detection result

    if abs(PIDval) < T:
        return centSpd,centSpd

    if y == 1 and w == 1:
        if PIDval > 0:
            rightSpd = max(0,centSpd-PIDval)
            leftSpd = min(100,centSpd+PIDval)
        else:
            rightSpd = min(100,centSpd+PIDval)
            leftSpd = max(0,centSpd-PIDval)        

    elif y == 1 and w <= 0:
        if PIDval > 0:
            rightSpd = max(0,centSpd-PIDval)
            leftSpd = min(100,centSpd+PIDval)
        else:
            rightSpd = min(100,centSpd+PIDval)
            leftSpd = max(0,centSpd-PIDval)   
    else:
        # Unexpected Error, car should stop.
        rightSpd = 0
        leftSpd = 0

    return rightSpd, leftSpd

# adaptive speed adjustment process based on PID controller.

def adaptive_fix(rightSpd, leftSpd, dev, y, w):
    centSpd = (rightSpd+leftSpd)/2
    int_dev = vars.int_dev
    prev_dev = vars.dev
    PIDval,int_dev = findPIDval(dev,int_dev,prev_dev)
    rightSpd, leftSpd = PIDLanefollower(PIDval,centSpd,y,w)
    vars.int_dev = int_dev
    vars.dev = dev
    return rightSpd, leftSpd

# normal speed adjustment process

def fix(rightSpd, leftSpd, dev, y, w):
    """
    return devised rightSpd and leftSpd to fix the deviation
    """
    if y == 1 and w == 1:
        # both line found, dev is the deviation
        if dev > 10:
            # should go left
            rightSpd = 80
            leftSpd = 20
        elif dev < -10:
            # should go right
            rightSpd = 20
            leftSpd = 80
        else:
            # go straight
            rightSpd = 50
            leftSpd = 50

    elif y == 1 and w <= 0:
        # only found yellow line, dev is y offset
        if dev > 10:
            # should go right
            rightSpd = 20
            leftSpd = 80
        else:
            # go straight
            rightSpd = 50
            leftSpd = 50
    else:
        # stop
        rightSpd = 0
        leftSpd = 0

    return rightSpd, leftSpd





        
