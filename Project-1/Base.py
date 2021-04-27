'''
 - A Base Class of all TWA Classes
 - In TWA, everything is derived from Base class
 - A Base class is used as an Argument in all other classes
'''

#    | import standard module(Packages)
#                                | keywords
from datetime import datetime as time

class Base:

    # attributes
    _log   = "CombinedProfile.log"          #  global log file name
    _count = 0.                             #  global instance counter

    # constructor
    #            | instance pointer
    #                  | optional parameter
    def __init__(self, log  = ""):

        if len(log) > 0:
            Base._log = log

        Base._count += 1                    # counter increment

    # destructor
    def __del__(self):

        Base._count -= 1                    # counter decrement

    # logging method
    # to log into a file and console window
    def appendlog(self,text):
        T        = time.now()               # get the actual time
        Tstamp   = "%2.2d. %2.2d. %2.2d." % (T.hour, T.minute, T.second)
        textOut  = Tstamp + text            # text to print
        f = file(Base._log,"a")             # use the file object to print with append mode "a"
        f.write(textOut+"\n")
        f.close()
        print textOut