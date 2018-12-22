from core import core
import sys

def main(mode):
    input("press ENTER to start:")
    # startup Picore
    if mode == "manual":
        myCore = core(False)
    else:
        myCore = core()
    return

if __name__ == "__main__":
    main(sys.argv[1])
