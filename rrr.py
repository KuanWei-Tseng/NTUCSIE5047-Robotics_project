import curses
import time
screen = curses.initscr()
curses.noecho()
curses.curs_set(0)
screen.nodelay(True)
screen.keypad(1)
counter = 0
#screen.addstr("Press a key")
while True:
    try:
        event = screen.getch()
        if event == curses.KEY_LEFT:
            screen.addstr(0, 0, "Left Arrow Key pressed")
        elif event == curses.KEY_RIGHT:
            screen.addstr(0, 0, "Right Arrow Key pressed")
        elif event == curses.KEY_UP:
            screen.addstr(0, 0, "UP Arrow Key pressed")
        elif event == curses.KEY_DOWN:
            screen.addstr(0, 0, "DOWN Arrow Key pressed")
        elif event == -1:
            screen.move(0, 0)
        else:
            break
        screen.clrtoeol()
        screen.refresh()
        time.sleep(0.5)
    except Exception as e:
        # No input
        pass

curses.endwin()
