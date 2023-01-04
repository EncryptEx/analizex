from importlib import reload
import sys
import coreAnalizer

debug = True

part1Cache = None
if __name__ == "__main__":
    while True:
        if not part1Cache:
            part1Cache = coreAnalizer.readData()
        coreAnalizer.consoleOutput(part1Cache)
        if(not debug):
            quit()
        print("Press enter to re-run the script, CTRL-C to exit")
        sys.stdin.readline()
        reload(coreAnalizer)
