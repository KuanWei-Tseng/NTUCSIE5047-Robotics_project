from car import car
from camera import camera
from rawImage import rawImage
import control
import numpy as np
import time
import cv2

class core:
    
    def __init__(self, auto = True):
        # initialize car object
        self.myCar = car()
        # initialize camera
        self.myCamera = camera()
        
        # get ready
        time.sleep(2)
        
        print("myCar and myCamera startup completed")

        if auto:
            # auto drive
            print("autoDrive mode")
            self.autoDrive()

        else:
            # manual drive
            print("manualDrive mode")
            self.manualDrive()

    def autoDrive(self, elapse = 0.5):
        print("autoDrive activated")
        
        # start going forward
        self.myCar.goforward(5)
        
        while True:
            try:
                # get the image from camera
                img = self.myCamera.capture()
                # init rawImage
                raw = rawImage(img)
                # get the deviation
                deviation, y, w = raw.findDeviation()
                # get current speed
                rightSpd, leftSpd = self.myCar.getSpeed()
                # calculate new rightSpd and leftSpd to fix the deviation
                rightSpd, leftSpd = control.fix(rightSpd, leftSpd, deviation, y, w)
                # pass speed arguments to myCar
                self.myCar.setSpeed(rightSpd, leftSpd)

            except KeyboardInterrupt:
                print("keyboard interrupt signal caught, exit")
                self.myCar.turnoff()
                break

        return

    def manualDrive(self):
        pass
