from car import car
from camera import camera
from rawImage import rawImage
from obws import obws
from control import control
from lightDetection import lightDetection
import vars
import numpy as np
import time
import cv2
import threading

class core:
    
    def __init__(self, auto, debug):
        # initialize car object
        self.myCar = car()
        # initialize camera
        self.myCamera = camera()
        # initialize global variables
        vars.init()
        # debug or not
        self.debug = debug

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

    def autoDrive(self, elapse = 0.1):
        print("autoDrive activated")
        # initialize control 
        myCtl = control()
        # initialize obws
        myObws = obws()
        # enable radar
        vars.shutdown = False
        # start up radar
        t_obws = threading.Thread(target = myObws.safedriving, args = ())
        print("started")
        t_obws.start()
        for i in range(0, 5):
            img = self.myCamera.capture()
            self.myCamera.trunc()
            time.sleep(0.2)

        # start going forward
        if self.debug == "False":
            self.myCar.setSpeed(40, 40)
        rightSpd, leftSpd = 40, 40

        while True:
            try:
                # get the image from camera
                img = self.myCamera.capture()
                # init rawImage
                raw = rawImage(img)
                # init lightDetection
                ld = lightDetection(img)
                # truncate stream
                self.myCamera.trunc()
                # init thread to find deviation
                t1 = threading.Thread(target = raw.findDeviation, args = ())
                # init thread to find blue line
                t2 = threading.Thread(target = raw.find_b, args = ())
                # init thread to find traffic light
                # t3 = threading.Thread(target = ld.find_light, args = ())
                # start thread, get the deviation
                t1.start()
                # start thread, get blue lines
                t2.start()
                # start thread, get traffic light
                # t3.start()
                # wait elapsed time
                time.sleep(elapse)
                # join deviation thread
                t1.join()
                # join blue line thread
                t2.join()
                # join traffic light thread
                # t3.join()
                
                print("================================")
                
                if vars.blue == True:
                    print("Blue line found")
                    self.myCar.setSpeed(0, 0)
                    break
                    """
                    # check traffic light
                    if vars.light == "green":
                        # safe to go
                        print("green light")
                    elif vars.light == "red":
                        # stop the car
                        print("red light, stop")
                        self.myCar.setSpeed(0, 0)
                    else:
                        # no light found
                        print("no traffic light found, error")
                    """

                if vars.line_type == "b":
                    # both lines found
                    print("both lines found")
                    print("deviation = {}".format(vars.deviation))

                elif vars.line_type == "y":
                    # only found yellow line
                    print("yellow line found")
                    print("y_theta = {}, y_offset = {}".format(vars.theta, vars.deviation))

                elif vars.line_type == "w":
                    # only found white line
                    print("white line found")
                    print("w_theta = {}, w_offset = {}".format(vars.theta, vars.deviation))

                # get current speed
                if self.debug == "False":
                    rightSpd, leftSpd = self.myCar.getSpeed()

                print("current rightSpd = {}".format(rightSpd))
                print("current leftSpd = {}".format(leftSpd))

                # running into obstacles
                if vars.message == 0:
                    # stop
                    print("Running into obstacles, stop")
                    rightSpd, leftSpd = 0, 0
                else:
                    # calculate new rightSpd and leftSpd to fix the deviation
                    rightSpd, leftSpd = myCtl.adaptive_control(rightSpd, leftSpd, vars.deviation, vars.theta, vars.line_type)

                print("new rightSpd = {}".format(rightSpd))
                print("new leftSpd = {}".format(leftSpd))

                # pass speed arguments to myCar
                if self.debug == "False":
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
