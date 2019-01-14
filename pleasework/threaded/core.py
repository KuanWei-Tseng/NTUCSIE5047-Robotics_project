from car import car
from camera import camera
from rawImage import rawImage
from obws import obws
from control import control
from lightDetection import lightDetection
from map import map
import vars
import numpy as np
import time
import cv2
import threading

class core:
    
    def __init__(self, auto, debug):
        # initialize car object
        self.myCar = car()
        # initialize current state
        self.state = "f"
        # initialize map
        self.myMap = map()
        # initialize action counter
        self.actioncounter = 0
        # initialize camera
        self.myCamera = camera()
        # initialize global variables
        vars.init()
        # debug or not
        self.debug = debug

        # get ready
        time.sleep(1)
        
        print("myCar and myCamera startup completed")

        if auto:
            # auto drive
            print("autoDrive mode")
            self.autoDrive()

        else:
            # manual drive
            print("manualDrive mode")
            self.manualDrive()

    def get_action(self):
        # get current speed
        rightSpd, leftSpd = self.myCar.getSpeed()

        print("current rightSpd = {}".format(rightSpd))
        print("current leftSpd = {}".format(leftSpd))

        # running into obstacles
        if vars.message == 0:
            # stop
            print("Running into obstacles, stop")
            rightSpd, leftSpd = 0, 0

        # both lines found, calculate new rightSpd and leftSpd to fix the deviation
        elif ((self.state == "l" or self.state == "r") and self.actioncounter >=9):

            rightSpd, leftSpd = self.myCtl.adaptive_control(50, 50, vars.deviation, vars.theta, vars.line_type)
            self.state = "f"
            self.actioncounter = 0
            
        elif vars.line_type == "b" and (self.state == "f" or self.state == "s"):
            rightSpd, leftSpd = self.myCtl.adaptive_control(rightSpd, leftSpd, vars.deviation, vars.theta, vars.line_type)
            self.state = "f"
            self.actioncounter = 0
            
        # should stop
        elif self.state == "stop":
            rightSpd, leftSpd = 0, 0

        # should go straight
        elif self.state == "s":
            rightSpd, leftSpd = 50, 40
            self.actioncounter = 0
            
        elif self.state == "f":
            print("should go forward, but found less than one line")
            """
            # prepare to turn right
            if vars.line_type == "y":
                self.actioncounter = 0
                self.state = "r"
                rightSpd, leftSpd = 40, 40
            # prepare to turn left
            elif vars.line_type == "w":
                self.actioncounter = 0
                self.state = "l"
                rightSpd, leftSpd = 40, 40
            # error
            else:
                print("error")
                rightSpd, leftSpd = 0, 0
            self.state = "stop"
            """
            rightSpd, leftSpd = self.myCtl.adaptive_control(rightSpd, leftSpd, vars.deviation, vars.theta, vars.line_type)

        # turning session
        elif self.state == "r" or self.state == "l":
            # going straight
            if self.actioncounter < 1:
                rightSpd, leftSpd = 0, 0
            elif self.actioncounter == 1:
                rightSpd, leftSpd = 0, 100
                self.actioncounter += 1
            else:
                # turning
                if (self.actioncounter - 2) % 5 == 0 or (self.actioncounter - 2) % 5 == 1:
                    # right
                    rightSpd, leftSpd = 0, 70
                    # left
                    if self.state == "l":
                        rightSpd, leftSpd = 70, 10
                # stop
                elif (self.actioncounter - 2) % 5 == 2:
                    rightSpd, leftSpd = 0, 0

                # going straight
                elif (self.actioncounter - 2) % 5 == 3:
                    rightSpd, leftSpd = 60, 40

                # stop
                else:
                    rightSpd, leftSpd = 0, 0
            self.actioncounter += 1
            
        print("new rightSpd = {}".format(rightSpd))
        print("new leftSpd = {}".format(leftSpd))

        # pass speed arguments to myCar
        if self.debug == "False":
            self.myCar.setSpeed(rightSpd, leftSpd)
            
        print("current state = {}".format(self.state))
        
    def get_vars_type(self):
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

        elif vars.line_type == "n":
            # nothing found
            print("nothing found")

    def get_vars_blue(self):
        if vars.blue == True and self.state == "f":
            # check traffic light
            print("blue line spotted")
            if vars.light == "green":
                # safe to go
                print("green light")
                self.state = self.myMap.update()
            elif vars.light == "red":
                # stop the car
                print("red light, stop")
                self.state = "stop"
            else:
                # no light found, turning
                print("no traffic light found, turning")
                if self.myMap.get_pos() == 1:
                    self.state = "l"
                elif self.myMap.get_pos() == 4:
                    self.state = "r"
                    
        elif self.state == "stop" and vars.light == "green":
            print("green light")
            self.state = self.myMap.update()

    def autoDrive(self, elapse = 0.2):
        print("autoDrive activated")
        # initialize control 
        self.myCtl = control()
        # initialize obws
        myObws = obws()
        # enable radar
        vars.shutdown = False
        vars.blue = False
        vars.light = "NULL"
        # start up radar
        t_obws = threading.Thread(target = myObws.safedriving, args = ())
        print("camera warmup started")
        t_obws.start()
        # camera warm up
        for i in range(0, 5):
            img = self.myCamera.capture()
            self.myCamera.trunc()
            time.sleep(0.2)

        # start going forward
        if self.debug == "False":
            self.myCar.setSpeed(40, 40)
        rightSpd, leftSpd = 60, 50

        img_buff = []
        while True:
            try:
                # get the image from camera
                img = self.myCamera.capture()
                img_buff.append(img)
                # init rawImage
                raw = rawImage(img)
                # init lightDetection
                ld = lightDetection(img)
                # truncate stream
                self.myCamera.trunc()
                # init thread to find deviation
                dthread = threading.Thread(target = raw.findDeviation, args = ())
                # init thread to find blue line
                bthread = threading.Thread(target = raw.find_b, args = ())
                # init thread to find traffic light
                tthread = threading.Thread(target = ld.find_light, args = ())
                # start threads
                vars.light = "NULL"
                dthread.start()
                bthread.start()
                tthread.start()
                # wait elapsed time
                time.sleep(elapse)
                # join threads
                dthread.join()
                bthread.join()
                tthread.join()
                
                print("================================")
                self.get_vars_blue()
                self.get_vars_type()
                self.get_action()

            except KeyboardInterrupt:
                print("keyboard interrupt signal caught, exit")
                vars.shutdown = True
                self.myCar.turnoff()
                self.myCamera.exit()
                t_obws.join()
                for i, img in enumerate(img_buff):
                    cv2.imwrite("../pic/" + i + ".jpg", img)
                break

        return

    def manualDrive(self):
        pass
