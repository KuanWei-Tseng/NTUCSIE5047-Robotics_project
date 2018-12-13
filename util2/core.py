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
        self.camera.rotation = 180
        self.camera.resolution = (640, 480)
        self.camera.framerate = 32
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
        leftSpd = rightSpd = 70
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
        print(useless)
        screen = curses.initscr()
        curses.noecho()
        curses.curs_set(0)
        screen.nodelay(True)
        screen.keypad(1)
        pre_event = 0
        while True:
            try:
                event = screen.getch()
                if pre_event != event:
                    if event == curses.KEY_UP:
                        screen.addstr(0, 0, "UP")
                        self.myCar.forward(80, 80)

                    elif event == curses.KEY_DOWN:
                        screen.addstr(0, 0, "DOWN")
                        self.myCar.backward(80, 80)

                    elif event == curses.KEY_LEFT:
                        screen.addstr(0, 0, "LEFT")
                        self.myCar.forward(leftSpd = 50, rightSpd = 80)

                    elif event == curses.KEY_RIGHT:
                        screen.addstr(0, 0, "RIGHT")
                        self.myCar.forward(leftSpd = 80, rightSpd = 50)
                    
                    # nothing is pressed
                    elif event == -1:
                        screen.move(0, 0)
                        self.myCar.stop()

                    else:
                        self.myCar.stop()
                        break
                    pre_event = event
                    screen.clrtoeol()
                    screen.refresh()
                time.sleep(0.1)

            except Exception as e:
                pass

        curses.endwin()
        self.myCar.stop()
        print("END")
        self.myCar.end()
        return