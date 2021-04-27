'''
Thin walled approximation for Combined Profile
'''
from Profile import Profile
from Node    import Node
from Element import Element
from math    import *

class CombinedProfile(Profile):

    # constructor
    #                  |profile name
    #                       |length of long plate of L-Profile
    #                          |length of short plate of L-Profile
    #                             |thickness of L-Profile
    #                                |Outer diameter of O-Profile
    #                                   |thickness of O-Profile
    def __init__(self,name, k, b, z, d, Tt):

        # read parameters form file
        file = None
        if file is not None:
            if not self.read(file): return
            Profile.__init__(self,self._name)  # store profile name

        # use constructor parameters
        else:
            Profile.__init__(self, name)  # store profile name
            self._k  = float(k)           # length of long plate of L-profile
            self._b  = float(b)           # length of short plate of L-profile
            self._z  = float(z)           # thickness of L-Profile
            self._d  = float(d)           # Outer diameter of O-Profile
            self._Tt = float(Tt)          # thickness of O-Profile

        # check the input parameter
        self.checkParam()

        # create system
        self.create()

        # calculate section value
        self.getResults()

    # check paramaeter
    def checkParam(self):

        nDim = 0.   # minimal dimension

        if self._k < nDim:
            raise Exception ("> Invalid length of long plate of L-Profile : %f" % self._k)
        if self._b < nDim:
            raise Exception ("> Invalid length of short plate of L-Profile : %f" % self._b)
        if self._z < nDim:
            raise Exception ("> Thickness of L-Profile : %f" % self._z)
        if self._d < nDim:
            raise Exception ("> Outer diameter of O-Profile : %f" % self._d)
        if self._Tt < nDim:
            raise Exception ("> Thickness of O-Profile : %f" % self._Tt)

    # create the geometry (nodes and elements)
    def create(self):

        # introduce helpers
        # O Profile
        self._r  = self._d/2.
        no_e     = 20
        theta  = (2*pi)/no_e

        # create nodes
        # L Profile
        nodes = [Node(1,  -self._r - self._k, self._z/2.),
                 Node(2,  -self._r , self._z/2.),
                 Node(3,  -self._r , self._b),
                 Node(4,   self._r , self._b),
                 Node(5,   self._r , self._z/2.),
                 Node(6,   self._r + self._k, self._z/2.)]

        # O Profile
        angle = 90.*(pi/180.)
        for i in range(6, no_e+6):
            nodes += [Node(i+1, self._r*cos(angle), self._b + self._r*sin(angle)),]
            angle += theta
        for node in nodes:
            node.listData()

        # create elements
        # L Profile
        elem = [Element(1,nodes[0],nodes[1],self._z),
                Element(2,nodes[1],nodes[2],self._z),
                Element(3,nodes[3],nodes[4],self._z),
                Element(4,nodes[4],nodes[5],self._z)]

        # O Profile
        for i in range(6, no_e+6):
            if i == (no_e+6)-1:
                elem += [Element(i+1, nodes[i], nodes[6], self._Tt),]
            else:
                elem += [Element(i+1, nodes[i], nodes[i+1], self._Tt),]#

        # insert elements into the profile
        for e in elem:
            self.addElement(e)

