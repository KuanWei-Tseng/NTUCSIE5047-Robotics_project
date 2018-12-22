from car import car
from camera import camera
from rawImage import rawImage
from obws import obws
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


        # initialize obws
        myObws = obws()
        # enable radar
        vars.shutdown = False
        # start up radar
        t_obws = threading.Thread(target = myObws.safedriving, args = ())
        print("started")
        t_obws.start()
        # start going forward
        self.myCar.forward(50)
        
        while True:
            try:
                # get the image from camera
                img = self.myCamera.capture()
                # init rawImage
                raw = rawImage(img)
                # truncate stream
                self.myCamera.trunc()
                # init thread
                t1 = threading.Thread(target = raw.findDeviation, args = ())
                # start thread, get the deviation
                t1.start()
                # wait elapsed time
                time.sleep(elapse)
                # join thread, get the deviation
                t1.join()
                print("deviation = {}, y = {}, w = {}".format(vars.deviation, vars.y, vars.w))

                # get current speed
                rightSpd, leftSpd = self.myCar.getSpeed()

                print("current rightSpd = {}".format(rightSpd))
                print("current leftSpd = {}".format(leftSpd))

                # running into obstacles
                #vars.message = 2
                if vars.message == 0:
                    # stop
                    print("Running into obstacles, stop")
                    rightSpd, leftSpd = 0, 0
                else:
                    # calculate new rightSpd and leftSpd to fix the deviation
                    rightSpd, leftSpd = control.fix(rightSpd, leftSpd, vars.deviation, vars.y, vars.w)

                print("new rightSpd = {}".format(rightSpd))
                print("new leftSpd = {}".format(leftSpd))

                # pass speed arguments to myCar
                self.myCar.setSpeed(rightSpd, leftSpd)

                time.sleep(elapse)

            except KeyboardInterrupt:
                print("keyboard interrupt signal caught, exit")
                vars.shutdown = True
                self.myCar.turnoff()
                self.myCamera.exit()
                t_obws.join()
                break

        return

    def manualDrive(self):
        pass
