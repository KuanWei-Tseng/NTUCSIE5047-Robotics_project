from core import core
import sys

def main(type):
    if type == "auto":
        pipi = core()
    else:
        pipi = core(manual = True)
    
    return

if __name__ == "__main__":
    main(sys.argv[1])

