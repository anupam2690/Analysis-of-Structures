'''
 - A AList class extends python's build-In class List
 - List class - Python's Build-In list container
'''
from Base import Base

class AList(Base, list):
    # constructor
    def __init__(self):
        Base.__init__(self)         # call constructor of parent Base class

        # add Instances
        #         | object number, index = no - l
        #             | object
    def add(self, no, obj):
        # check the container length
        index  = no - 1
        # check list length
        #        | length of the container
        uBound = len(self) - 1

        if index > uBound:
            # extend the list until upper bound == index
            for i in range(uBound+1, index+1):
                self += [None,]

        # store objects in container
        self[index] = obj

    # list container data
    def list(self):
        objC = 0                 # counter initialization

        for obj in self:
            try:
                obj.listData()
            except:
                self.appendlog("> Object %d is unprintable!" % objC)
            objC += 1            # counter increment
