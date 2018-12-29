from core import core
import sys

def main(mode):
    input("press ENTER to start:")
    # startup Picore
    if mode == "auto":
        myCore = core(True)
    elif mode == "manual":
        myCore = core(False)
    else:
        print("manual or auto?")
    return

if __name__ == "__main__":
    main(sys.argv[1])
