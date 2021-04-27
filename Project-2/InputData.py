'''
Input data to control the calculation
- geometry
- loads
- meshing
- analysis type
'''

from Base import Base
profile_1 = True     # Combination-1  L100x50x6 + O60.3x2.3
profile_2 = False    # Combination-2  L100x75x10 + O60.3x2.3
profile_3 = False    # Combination-3  L120x80x8 + O60.3x2.3

class InputData(Base):
    # constructor
    def __init__(self):
        Base.__init__(self)

        self.prjName = "MPK"
        # profile parameters
        self.load = 27.0        # [kN]

        # mesh parameters
        self.maxNumber = 1000     # student edition limited 1000 nodes
        self.longplateSeed = 8    # number of long plate seeds
        self.shortplateSeed = 4   # number of short plate seeds
        self.tubeSeed = 6         # number of tube seeds
        # number of length seeds
        self.lengthSeed = self.maxNumber/(2.*self.longplateSeed+4.*self.shortplateSeed+1.
                                          *self.tubeSeed+1.)-1.
        self.lengthSeed = int(self.lengthSeed)
        self.longplate  = "longplate"
        self.shortplate = "shortplate"
        self.tube       = "tube"       # tube profile

        # Input Parameters of combined profile
        # =================== Combination-1  L100x50x6 + O60.3x2.3 ===================#
        if profile_1:
            self.k = 100.       # Length of Long plate of L-Profile[mm]
            self.bb = 50.       # Length of short plate of L-Profile[mm]
            self.z = 6.0        # thickness[mm]
            self.d = 60.3       # Outer diameter of O-Profile[mm]
            self.Tt = 2.3       # Thickness of O-Profile[mm]
            self.len = 3200     # length of the profile[mm]

        # =================== Combination-2  L100x75x10 + O60.3x2.3 ===================#
        if profile_2:
            self.k = 100.       # Length of Long plate of L-Profile[mm]
            self.bb = 75.       # Length of short plate of L-Profile[mm]
            self.z = 10.0       # thickness[mm]
            self.d = 60.3       # Outer diameter of O-Profile[mm]
            self.Tt = 2.3       # Thickness of O-Profile[mm]
            self.len = 3200     # length of the profile[mm]

        # =================== Combination-3  L120x80x8 + O60.3x2.3 ===================#
        if profile_3:
            self.k = 120.       # Length of Long plate of L-Profile[mm]
            self.bb = 80.       # Length of short plate of L-Profile[mm]
            self.z = 8.0        # thickness[mm]
            self.d = 60.3       # Outer diameter of O-Profile[mm]
            self.Tt = 2.3       # Thickness of O-Profile[mm]
            self.len = 3200     # length of the profile[mm]

        # material parameters
        self.material = "steel"
        self.yMod = 210000.     # young's modulus [N/mm^2]
        self.nue = 0.3          # poisson's ratio
        self.density = 7.84e-06

        # calculation parameters
        self.LINEAR = 0         # linear elastic calculation
        self.stepType = self.LINEAR
        self.stepName = "Linear"
        self.jobName = None
        self.setHelpers()

    # create helper
    def setHelpers(self):
        self.r = self.d / 2.     # Radius
        self.bk = self.bb - (self.z/2.)
        self.bm = self.bb - self.r
        self.bn = self.bb + self.r

        # calculate the pressure
        self.pressure = (self.load*1.e3)/(2.*self.k*self.len)
        self.check()

    def check(self):
        dMin = 1.  # minimal length

        if self.k < 2 * self.z:
            raise Exception("invalid length of long plate of L-Profile %e" % self.k)
        if self.bb < 2. * self.z:
            raise Exception("invalid length of short plate of L-Profile %e" % self.bb)
        if self.z < dMin:
            raise Exception("invalid thickness of L-Profile %e" % self.z)
        if self.d < 2 * self.z:
            raise Exception("outer diameter of O-Profile %e" % self.d)
        if self.Tt < dMin:
            raise Exception("invalid thickness of O-Profile %e" % self.Tt)

    # read the input data form an input file

    def readData(self):
        pass
