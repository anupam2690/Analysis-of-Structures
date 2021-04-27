'''
main program of the profile calculation

copy command into interpreter window and run it!
execfile(r"F:\ANUPAM\Studies\AoS-WS1617-chakraborty-anupam-3039242-2\Project-2\runMPK.py")
'''

# set work directory
import os
os.chdir(r"F:\ANUPAM\Studies\AoS-WS1617-chakraborty-anupam-3039242-2\Project-2")

import MPK
reload(MPK)

from MPK import MPK

# create Combined Profile(MPK) instance and run methods
sys = MPK()
sys.createSystem()      # geometry, mesh
sys.createStep()        # run linear calculation
sys.runJob()
sys.analyseResults()
