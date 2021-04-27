'''
 - A ProfileDB class use the Python built-In object dictionary
 - A dictionary is used to store instance pointer with an arbitrary access key
'''
from Base import Base

class ProfileDB(Base, dict):
    # constructor
    def __init__(self):
        Base.__init__(self)

    def list(self):
        objC = 0                                # counter initialization

        for name in self:                       # iterate the key of dictionary
            try:
                self[name].listData()           # list an object
            except:
                self.appendlog("> Error: %s profile not found, %d" % (name, objC))
            objC += 1                           # counter increment

    def plot(self):
        objC = 0

        for name in self:
            try:
                self[name].plot(True)          # plot the png file
            except:
                self.appendlog("> Error: %s profile not found, %d" % (name, objC))
            objC += 1
