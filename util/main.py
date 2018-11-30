from Pi import Pi
import sys

def main(type):
    if type == "auto":
        pipi = Pi()
    else:
        pipi = Pi(manual = True)
    
    return

if __name__ == "__main__":
    main(sys.argv[1])

