from car import car
from camera import camera
from rawImage import rawImage
import control
import vars
import numpy as np
import time
import cv2
import threading

class core:
    
    def __init__(self, auto = True):
        # initialize car object
        self.myCar = car()
        # initialize camera
        self.myCamera = camera()
        # initialize global variables
        vars.init()

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

    def autoDrive(self, elapse = 0.2):
        print("autoDrive activated")
        
        # start going forward
        self.myCar.goforward(50)
        
        while True:
            try:
                # get the image from camera
                img = self.myCamera.capture()
                # init rawImage
                raw = rawImage(img)
                # init thread
                t1 = threading.Thread(target = raw.findDeviation(), args = ())
                threads.append(t1)
                # start thread, get the deviation
                t1.start()
                # wait elapsed time
                time.sleep(elapse)
                # join thread, get the deviation
                t1.join()
                print("deviation = {}, y = {}, w = {}".format(deviation, y, w))

                # get current speed
                rightSpd, leftSpd = self.myCar.getSpeed()

                print("current rightSpd = {}".format(rightSpd))
                print("current leftSpd = {}".format(leftSpd))

                # calculate new rightSpd and leftSpd to fix the deviation
                rightSpd, leftSpd = control.fix(rightSpd, leftSpd, deviation, y, w)

                print("new rightSpd = {}".format(rightSpd))
                print("new leftSpd = {}".format(leftSpd))

                # pass speed arguments to myCar
                self.myCar.setSpeed(rightSpd, leftSpd)

                time.sleep(elapse)

            except KeyboardInterrupt:
                print("keyboard interrupt signal caught, exit")
                self.myCar.turnoff()
                self.myCamera.exit()
                break

        return

    def manualDrive(self):
        pass
