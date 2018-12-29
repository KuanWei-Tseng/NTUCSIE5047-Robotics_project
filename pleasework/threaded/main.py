from core import core
import sys

def main(mode, debug):
    input("press ENTER to start:")
    # startup Picore
    if mode == "auto":
        myCore = core(True, debug)
    elif mode == "manual":
        myCore = core(False, debug)
    else:
        print("manual or auto?")
    return

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
