'''
A Element class contents Element's point data
  _no  = element number
  _n[] = List of point coordinates
  _t   = line thickness

'''
from math import *
from Base import Base
from Node import Node

class Element(Base):
    # constructor
    def __init__(self, no, n1, n2, t):
        Base.__init__(self)
        self._no     = int(no)
        # check the node Instance
        #                     | take into account inheritance (an instance of a derived class is an instance of a base class, too)
        try:
            #                    | class to check
            if not isinstance(n1,Node): raise
            if not isinstance(n2,Node): raise
            self._node = [n1,n2]

        except:
            raise Exception ("*** Error: invalid element data!")
        self._t = float(t)

    # calculate projected length of an element
    #             | dimension
    def delX(self,i):
        #            | node 2nd              | node 1st
        #                     | coordinate          | coordinate
        return self._node[1]._x[i] - self._node[0]._x[i]

    # calculate length of an element
    def getL(self):
        return sqrt(self.delX(0)**2 + self.delX(1)**2)

    # calculate area of an element
    def getA(self):
        return (self.getL()*self._t)

    # calculate center coordinate of an element
    #             | dimension
    def getC(self,i):
        #             | node 2nd            | node 1st
        #                      | coordinate          | coordinate
        return (self._node[1]._x[i] + self._node[0]._x[i])/2.

    # calculate static moment of an element
    #             | dimension
    def getS(self,i):
        return (self.getC((i+1)%2)*self.getA())

    # calculate moment of inertia
    #             | dimension
    def getI(self,i):
        if i < 2:
            j = (i+1)%2
            return (self.delX(j)**2/12. + self.getC(j)**2)*self.getA()
        else:
            return ((self.delX(0)*self.delX(1))/12 + self.getC(0)*self.getC(1)) * self.getA()

    # list element data
    def listData(self):
        self.appendlog("> Element = %d Thickness : = %10.2f mm" % (self._no, self._t))
        for node in self._node:
            node.listData()     # print Node data
        self.appendlog(" Length..................: = %10.2f mm" % self.getL())
        self.appendlog(" Area....................: = %10.2f mm^2" % self.getA())
        self.appendlog(" Center coordinate ......: = %10.2f %10.2f mm" %\
                       (self.getC(0)/1.e1, self.getC(1)/1.e1))
        self.appendlog(" Static moments..........: = %10.2f %10.2f mm^3" % \
                       (self.getS(0), self.getS(1)))
        self.appendlog("Moment of inertia.......: = %10.2f %10.2f %10.2f mm^4" % \
                       (self.getI(0), self.getI(1), self.getI(2)))
