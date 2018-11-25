from car import car
from rawImage import rawImage
import numpy as np
import time

class Pi:
    """
    highest level of the classes
    """
    def __init__(self, manual = False, elapse = 0.1):
        self.myCar = car()
        # manual controll
        if manual:
            pass
        else:
            self.autoDrive(elapse)

    # autodrive until keyboard interrupts
    def autoDrive(self, elapse):
        # fds to listen to 
        inputready, outputready, exceptrdy = select.select([0], [], [])

        while True:
            for i in inputready:
                # keyboard input
                if i == 0:
                    msg = input()
                    print("keyboard interrupt detected, stop and exit.")
                    self.myCar.stop()
                    return

            # get the image
            
            img = rawImage(image)
            deviation = img.findDeviation()

            # start running
            
            if (deviation < 0):
                self.myCar.turnLeft(deviation, deviation)
            elif (deviation > 0):
                self.myCar.turnRight(deviation, deviation)

            time.sleep(elapse)

        return
