# Motor Behavior Calculation for steering
'''
Responisble for calculating the desirable speed(duty cycle) of
two motors and return the value to core.

Input: current speed, direction

'''

def steering(dir,centSpd):
    # turn right:
    if dir = 1:
        leftSpd = max(centSpd + 20,100)
        rightSpd = max(centSpd - 20,-100)
    else:
        leftSpd = max(centSpd - 20,-100)
        rightSpd = max(centSpd + 20,100)    
    return rightSpd, leftSpd





        
