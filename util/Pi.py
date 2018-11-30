from car import car
from rawImage import rawImage
import numpy as np
import time
import curses

class Pi:
    """
    highest level of the classes
    init car object then call the car controlling routine
    """
    def __init__(self, manual = False, elapse = 0.1):
        self.myCar = car()
        # manual controll
        if manual:
            self.manualDrive()
        else:
            self.autoDrive(elapse)

    # autodrive until keyboard interrupts
    def autoDrive(self, elapse):
        print("AutoDrive mode started")
        print("Press ENTER to start")
        # fds to listen to 
        inputready, outputready, exceptrdy = select.select([0], [], [])

        while True:
            try:
                for i in inputready:
                    # keyboard input
                    if i == 0:
                        msg = input()
                        print("keyboard interrupt detected, stop and exit.")
                        self.myCar.stop()
                        return
                    
                self.myCar.turnLeft()
                # get the image

                img = rawImage(image)
                deviation = img.findDeviation()
                
                # start running
                
                if (deviation < 0):
                    self.myCar.turnLeft(deviation, deviation)
                elif (deviation > 0):
                    self.myCar.turnRight(deviation, deviation)
                    
                time.sleep(elapse)
            except Exception as e:
                pass

            finally:
                self.myCar.stop()
                break
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
                    self.myCar.forward()

                elif event == curses.KEY_DOWN:
                    screen.addstr(0, 0, "DOWN"):
                    self.myCar.backward()

                elif event == curses.KEY_LEFT:
                    screen.addstr(0, 0, "LEFT")
                    self.myCar.turnLeft(leftSpd = 0, rightSpd = 100)

                elif event == curses.KEY_RIGHT:
                    screen.addstr(0, 0, "RIGHT")
                    self.myCar.turnRight(leftSpd = 100, rightSpd = 0)
                    
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

        return
