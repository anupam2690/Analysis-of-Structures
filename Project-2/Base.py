'''
Base class for our Python Script
'''
from datetime import datetime as time

class Base:

    # class properties
    _log = "MPK.log"        # name of log file
    _counter = 0            # instance counter

    # constructor
    def __init__(self, log = ""):
        if len(log) > 0: Base._log = log

        Base._counter += 1
        self.appendLog("%d instances available." % Base._counter)

    # destructor
    def __del__(self):
        self.appendLog("delete object %d..." % Base._counter)
        Base._counter -= 1

    # write something to the log(logging method)
    def appendLog(self,text):
        # create the time step
        t = time.now()
        tstamp = "%2.2d.%2.2d.%2.2d " % (t.hour,t.minute,t.second)
        message = tstamp + text
        # open the file
        f = open(Base._log,"a")
        # write in to the file
        f.write(message + "\n")
        # print to the screen
        print message
