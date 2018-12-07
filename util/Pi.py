from car import car
from rawImage import rawImage
import numpy as np
import time
import curses
from picamera.array import PiRGBArray
from picamera import PiCamera

class Pi:
    """
    highest level of the classes
    init car object then call the car controlling routine
    """
    def __init__(self, manual = False, elapse = 0.1):
        self.myCar = car()
        # initialize the camera and grab a reference to the raw camera capture
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = rate
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        # allow the camera to warmup
        time.sleep(0.1)

        # manual controll
        if manual:
            self.manualDrive()
        else:
            self.autoDrive(elapse)

    # autodrive until keyboard interrupts
    def autoDrive(self, elapse):
        print("AutoDrive mode started")
        print("Press ENTER to start, press q to exit")
        nothing = raw_input()

        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            try:
                # get the image
                image = frame.array()
                key = cv2.waitKey(1) & 0xFF
                # clear the stream in preparation for the next frame
                self.rawCapture.truncate(0)
                if key == ord('q'):
                    break
                img = rawImage(image)
                deviation = img.findDeviation()
            
                # start running
                if (deviation < 0):
                    self.myCar.turnLeftSharp(deviation, deviation)
                elif (deviation > 0):
                    self.myCar.turnRightSharp(deviation, deviation)

                time.sleep(elapse)
            except:
                print("error happened")

            finally:
                break

        print("ended")
        self.car.stop()

        return

    def manualDrive(self):
        print("press up to go forward\npress down to go backward\npress left to turn left in place\npress right to turn right in place")
        print("press enter to start running")
        useless = raw_input()
        
        screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        screen.nodelay(True)
        screen.keypad(1)
        
        while True:
            try:
                event = screen.getch()
                if event == curses.KEY_UP:
                    screen.addstr(0, 0, "UP")
                    self.myCar.forward(40, 40)

                elif event == curses.KEY_DOWN:
                    screen.addstr(0, 0, "DOWN"):
                    self.myCar.backward(40, 40)

                elif event == curses.KEY_LEFT:
                    screen.addstr(0, 0, "LEFT")
                    self.myCar.forward(leftSpd = 0, rightSpd = 40)

                elif event == curses.KEY_RIGHT:
                    screen.addstr(0, 0, "RIGHT")
                    self.myCar.forward(leftSpd = 40, rightSpd = 0)
                    
                # nothing is pressed
                elif event == -1:
                    screen.move(0, 0)

                else:
                    self.myCar.stop()

                screen.clrtoeol()
                screen.refresh()
                time.sleep(0.5)

            except Exception as e:
                pass

            finally:
                curses.endwin()
                self.myCar.stop()
                print("END")
                break

        return
