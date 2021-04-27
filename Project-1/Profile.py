# -*- coding: utf-8 -*-
'''
 - A Profile class contents all common features os a Profile
 - Containers for the Points and Lines of a Modell
 - Attributes:
   - _name = Profile name
   - _element    = Element container
'''

from Base import Base
from AList import AList                         # Element container
from math import *

class Profile(Base):
    # constructor
    #                  | profile's name
    def __init__(self, name):

        Base.__init__(self)

        self._name       = name                 # Profile name
        self._element    = AList()              # Element container

        # result data (Initialization)
        # element contributions in user coordinate system
        self._a          =  0.                  # Profile area
        self._s          = [0.,0.]              # static moment
        self._iu         = [0.,0.,0.]           # moment of inertia w.r.t user coordinate
        # profile contribution
        self._e          = [0.,0.]              # coordinate of center of mass
        self._ic         = [0.,0.,0.]           # moment of inertia w.r.t center of mass coordinate
        self._ip         = [0.,0.]              # moment of inertia w.r.t principal coordinate
        self._alpha      =  0.                  # rotation angle

    # add Elements into the Profile container
    def addElement(self,e):
        self._element.add(e._no,e)

    # calculate section values of the Profile
    def getResults(self):
        elements = 0
        # check if elements are existing
        # iterate the element container
        for e in self._element:
            # ignore empty slots
            if e is not None:
                # area
                self._a += e.getA()

                # static moment
                for i in range(2):  # [0], [1]
                    self._s[i] += e.getS(i)

                # moment of inertia
                for i in range(3):
                    self._iu[i] += e.getI(i)

                elements += 1               # Element counter

        if self._element < 1:
            raise Exception("***Error: No Elements found!")

        # calculate the coordinates of center of mass (COM)
        for i in range(2):
            self._e[i] = self._s[(i+1)%2]/self._a

        # center of mass
        self._ic[0] = self._iu[0] - self._e[1] ** 2 * self._a
        self._ic[1] = self._iu[1] - self._e[0] ** 2 * self._a
        self._ic[2] = self._iu[2] - self._e[0] * self._e[1] * self._a

            # calculate moment of inertia w.r.t. center of mass coordinate
        if i < 2:
            self._ic[i] = self._iu[i] - (self._e[(i+1)%2]**2 * self._a)
        else:
            self._ic[i] = self._iu[2] - ((self._e[0]*self._e[1])* self._a)

        # calculate the principle values
        self.getPValues()

    # calculate Principle value
    # main axis Transformation
    def getPValues(self):

        # Helpers
        icDel = self._ic[0] - self._ic[1]
        icSum = self._ic[0] + self._ic[1]
        icsqr = sqrt(icDel**2. + 4.*self._ic[2]**2.)

        # Principal values
        self._ip[0] = 0.5 * (icSum + icsqr)             # iEta
        self._ip[1] = 0.5 * (icSum - icsqr)             # iZeta

        # Rotation angle
        self._alpha = 0.5 * atan2(-2.*self._ic[2],icDel)

        # Rotation angle in Degree
        self._alpha *= 180./pi

    # list Profile data
    def listData(self):
        self.appendlog("> Profile name...................: = '%s'" % self._name)
        self.appendlog("> Profile Area...................: = %8.3f cm^2" % (self._a/1.e2))
        self.appendlog("> static moment w.r.t. uc........: = %8.3e %8.3e cm^3" % \
                       (self._s[0]/1.e3, self._s[1]/1.e3))
        self.appendlog("> moment of inertia w.r.t. uc....: = %8.3e %8.3e %8.3e cm^4" % \
                       (self._iu[0]/1.e4, self._iu[1]/1.e4, self._iu[2]/1.e4))
        self.appendlog("> Center of Mass.................: = %8.3f %8.3f cm" % \
                       (self._e[0]/1.e1, self._e[1]/1.e1))
        self.appendlog("> moment of inertia w.r.t. cc....: = %8.3e %8.3e %8.3e cm^4" % \
                       (self._ic[0]/1.e4, self._ic[1]/1.e4, self._ic[2]/1.e4))
        self.appendlog("> moment of inertia w.r.t. pc....: = %8.3e %8.3e cm^4" % \
                       (self._ip[0]/1.e4, self._ip[1]/1.e4))
        self.appendlog("> Rotation angle.................: = %8.3f° " % self._alpha)
        self._element.list()

    # plotting profile using pylab
    def plot(self, viewer = True):
        try:
            import pylab
        except:
            self.appendlog("***Error: pylab package not found!")
            return

        # create list of line Element
        lines = []
        # over all elements
        for e in self._element:
            if e is not None:

                x1 = e._node[0]._x[0]
                x2 = e._node[1]._x[0]
                y1 = e._node[0]._x[1]
                y2 = e._node[1]._x[1]
                #           ----line-------
                lines += [ [[x1,x2],[y1,y2]], ]

        # draw elements
        for line in lines:
            #          | x coordinates
            #                   | y coordinates
            pylab.plot(line[0], line[1], 'k')

        # draw nodes
        for line in lines:
            #          | x coordinates
            #                   | y coordinates
            pylab.plot(line[0], line[1], 'rp')

        # some attributes
        pylab.axis('equal')
        pylab.title(self._name)

        # write png file
        pylab.savefig(self._name + ".png")

        # call viewer
        if viewer: pylab.show()

        # close the pylab
        pylab.close()

