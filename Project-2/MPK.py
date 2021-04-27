'''
main class to control the UGirder analysis
'''
# import abaqus packages
from abaqus import *
from abaqusConstants import *
from caeModules import *

# to improve the development cycle
# reload everything

import Base
reload(Base)

import InputData
reload(InputData)

import ResultData
reload(ResultData)

#    |module     |class
from Base import Base
from InputData import InputData
from ResultData import ResultData
from math import sqrt,fabs

class MPK(Base):

    # constructor
    def __init__(self):
        Base.__init__(self)     # call Base to initialize

        # input data object
        self.input = InputData()

        # result data object
        self.result = ResultData()

        # introduced Helpers
        self.myModel = None

    # create the system
    def createSystem(self):
        self.createModel()
        self.createPart()
        self.createMaterial()
        self.createProperties()
        self.assignSections()
        self.createMesh()
        self.getFiberNodes()
        self.createInstance()

    # create the model
    def createModel(self):
        self.appendLog("> create model '%s'..." % self.input.prjName)
        try:
            del mdb.models[self.input.prjName]
        except:
            pass
        self.myModel = mdb.Model(name=self.input.prjName)

    # create part using a sketch
    def createPart(self):
        self.appendLog("> create part...")
        data = self.input

        # create the sketch
        s = self.myModel.ConstrainedSketch(name=data.prjName,
                                           sheetSize=data.bb)

        xyPoints = (( -data.r - data.k, data.z/2.),
                     (-data.r, data.z/2.),
                     (-data.r, data.bb),
                     (data.r, data.bb),
                     (data.r, data.z/2.),
                     (data.r + data.k, data.z/2.),)

        # sketch lines
        s.Line(point1=xyPoints[0], point2=xyPoints[1])
        s.Line(point1=xyPoints[1], point2=xyPoints[2])
        s.Line(point1=xyPoints[3], point2=xyPoints[4])
        s.Line(point1=xyPoints[4], point2=xyPoints[5])

        # Tube profile
        s.CircleByCenterPerimeter(center=(0., data.bb), point1= (-data.r, data.bb))

        # create the part
        self.myPart = self.myModel.Part(name=data.prjName)
        self.myPart.BaseShellExtrude(sketch=s, depth=data.len)

    # create the material
    def createMaterial(self):
        self.appendLog("> create material...")
        data = self.input
        myMaterial = self.myModel.Material(name=data.material)
        myMaterial.Elastic(table=((data.yMod, data.nue),))
        myMaterial.Density(table=((data.density,),))

    # create the properties(thickness of shells)
    def createProperties(self):
        self.appendLog("> create properties...")
        data = self.input
        self.myModel.HomogeneousShellSection(name=data.longplate,
                                             material=data.material,
                                             thickness=data.z)
        self.myModel.HomogeneousShellSection(name=data.shortplate,
                                             material=data.material,
                                             thickness=data.z)
        self.myModel.HomogeneousShellSection(name=data.tube,
                                             material=data.material,
                                             thickness=data.Tt)

    # assign the sections
    def assignSections(self):
        self.appendLog("> assign sections...")
        data = self.input

        # L-Profile (Long plate)
        faces = self.myPart.faces.findAt((((data.r + data.k)/2., data.z/2., data.len/2.),),
                                         (((-data.r - data.k)/2., data.z/2., data.len/2.),),)

        region = regionToolset.Region(faces=faces)
        self.myPart.SectionAssignment(region=region,
                                      sectionName=data.longplate)
        self.longplateFaces = faces

        # L-Profile (short plate)
        faces = self.myPart.faces.findAt(((-data.r, data.bk/2, data.len/2.),),
                                         ((data.r, data.bk/2, data.len/2.),),)

        region = regionToolset.Region(faces=faces)
        self.myPart.SectionAssignment(region=region,
                                      sectionName=data.shortplate)
        self.shortplateFaces = faces


        # Tube profile
        faces = self.myPart.faces.findAt(((0., data.bn, data.len/2.),),
                                         ((0., data.bm, data.len/2.),),)

        region = regionToolset.Region(faces=faces)
        self.myPart.SectionAssignment(region=region,
                                      sectionName=data.tube)
        self.tubeFaces = faces

    # create the mesh
    def createMesh(self):
        self.appendLog("> create mesh...")
        data = self.input
        # element type assignment
        elemType1 = mesh.ElemType(elemCode=S4R)
        elemType2 = mesh.ElemType(elemCode=S3)
        self.myPart.setElementType(regions=(self.longplateFaces, self.shortplateFaces, self.tubeFaces),
                                   elemTypes=(elemType1, elemType2))

        # assign seeds: long plate
        edges = self.myPart.edges.findAt((((-data.r - data.k)/2., data.z/2., 0.),),
                                         (((data.r + data.k)/2., data.z/2., 0.),),
                                         (((-data.r - data.k)/2., data.z/2., data.len),),
                                         (((data.r + data.k)/2., data.z/2., data.len),),)

        self.myPart.seedEdgeByNumber(edges=edges,
                                     number=data.longplateSeed)

        # assign seeds: short plate
        edges = self.myPart.edges.findAt(((-data.r, data.bk/2., 0.),),
                                        ((-data.r,data.bk/2, data.len),),
                                        ((data.r, data.bk/2., 0.),),
                                        ((data.r, data.bk/2., data.len),),)
        self.myPart.seedEdgeByNumber(edges=edges,
                                     number=data.shortplateSeed)
        # assign seeds: Tube
        edges = self.myPart.edges.findAt(((0., data.bn, 0.),),
                                        ((0., data.bn, data.len),),)
        self.myPart.seedEdgeByNumber(edges = edges,
                                     number = data.tubeSeed)

        # assign seeds: length
        edges = self.myPart.edges.findAt(((-data.r - data.k, data.z/2., data.len/2.),),
                                         ((-data.r, data.z/2., data.len/2.),),
                                         ((-data.r, data.bb, data.len/2.),),
                                         ((data.r, data.bb, data.len/2.),),
                                         ((data.r, data.z/2., data.len / 2.),),
                                         ((data.r + data.k, data.z/2., data.len/2.),),)
        self.myPart.seedEdgeByNumber(edges=edges,
                                      number=data.lengthSeed)

        # generate mesh
        self.myPart.generateMesh()

    # select nodes along a line through the system
    def getFiberNodes(self):
        self.appendLog("> select nodes...")
        data = self.input

        # over all mesh nodes
        for node in self.myPart.nodes:

            # filter nodes
            dst = sqrt((node.coordinates[0] + data.r)**2
                + (node.coordinates[1]- data.z/2.)**2)
            if dst > 1.: continue

            # store node
            self.result.nodePos[node.label] = node.coordinates

        self.appendLog("--no ---------x ---------y ---------z")
        for label in self.result.nodePos:
            node = self.result.nodePos[label]
            self.appendLog("%4d %10.2f %10.2f %10.2f" %
                           (label, node[0], node[1], node[2]))
        self.appendLog("> %d nodes created." % len(self.myPart.nodes))
        self.appendLog("> %d elements created." % len(self.myPart.elements))
        self.appendLog("> %d nodes along fiber." % len(self.result.nodePos))

    # create an instance
    def createInstance(self):
        self.appendLog("create instance...")
        self.myInstance = self.myModel.rootAssembly.Instance(
            name = self.input.prjName,
            part = self.myPart,
            dependent = ON)

    # create a step
    def createStep(self):
        data = self.input
        self.appendLog("> create a '%s' step..." % data.stepName)
        data.stepType = data.LINEAR
        # linear calculation
        self.myModel.StaticStep(name=data.stepName,
                                previous = "Initial")
        self.createBCs()
        self.createLoads()

    # create BCs
    def createBCs(self):
        data = self.input
        self.appendLog("> create BCs...")

        # vertical boundary condition
        edges = self.myInstance.edges.findAt((((-data.r - data.k)/2., data.z/2., 0.),),
                                            (((data.r + data.k)/2., data.z/2., 0.),),
                                            (((-data.r - data.k)/2., data.z/2., data.len),),
                                            (((data.r + data.k)/2., data.z/2., data.len),),)

        self.myModel.DisplacementBC(name='vertical support',
                                    createStepName=data.stepName,
                                    region=(edges,),
                                    u2=0.0)

        # fix rigid body modes
        vertices = self.myInstance.vertices.findAt(((-data.r, data.z/2., 0.),),
                                                   ((data.r, data.z/2., 0.),),)

        self.myModel.DisplacementBC(name='rigid body modes',
                                    createStepName=data.stepName,
                                    region=(vertices,),
                                    u1=0.0,u3=0.0,ur2=0.0)

    # create pressure load
    def createLoads(self):
        data = self.input
        self.appendLog("> create load...")

        selectFace2 = self.myInstance.faces.findAt((((data.r + data.k)/2.,  data.z/2., data.len/2.),),
                                                   (((-data.r - data.k) / 2., data.z / 2., data.len / 2.),),)

        region = regionToolset.Region(side2Faces=selectFace2)

        self.myModel.Pressure(name='Pressure',
                              createStepName=data.stepName,
                              region=region,
                              magnitude=data.pressure)

    # create a job and run the calculation waiting for completion
    def runJob(self):
        data = self.input
        data.jobName = data.prjName + "-" + data.stepName
        self.appendLog("> run job '%s'..." % data.jobName)
        myJob = mdb.Job(name=data.jobName, model=data.prjName)
        myJob.submit()
        myJob.waitForCompletion()  # stop until job is ready

    # set the font size in the plots
    def setFontSize(self, size):
        fsize = int(size) * 10
        self.viewport.viewportAnnotationOptions.setValues(
            triadFont='-*-verdana-medium-r-normal-*-*-%d-*-*-p-*-*-*' % fsize,
            legendFont='-*-verdana-medium-r-normal-*-*-%d-*-*-p-*-*-*' % fsize,
            titleFont='-*-verdana-medium-r-normal-*-*-%d-*-*-p-*-*-*' % fsize,
            stateFont='-*-verdana-medium-r-normal-*-*-%d-*-*-p-*-*-*' % fsize)

    # open result database and do the post processing
    def analyseResults(self):
        data = self.input

        # open database
        data.odbName = data.jobName + ".odb"
        self.appendLog("> open result database '%s'..." % data.odbName)
        self.myOdb = session.openOdb(name=data.odbName)

        # select viewport and assign the result object
        self.viewport = session.viewports["Viewport: 1"]
        self.viewport.setValues(displayedObject=self.myOdb)
        self.setFontSize(9)

        # select vertical displacements
        self.viewport.odbDisplay.display.setValues(
            plotState=CONTOURS_ON_DEF)
        self.viewport.odbDisplay.setPrimaryVariable(
            variableLabel='U',
            outputPosition=NODAL,
            refinement=(COMPONENT, 'U2'), )

        # analysis for linear calculation
        self.analyseLinearStep()

    # analysis of linear calculation
    def analyseLinearStep(self):
        data = self.input
        result = self.result

        # reaction forces
        result.sumRFo = [0., 0., 0.]
        # select the data
        frame = self.myOdb.steps[data.stepName].frames[-1]
        rfo = frame.fieldOutputs['RF']

        # value.nodeLabel -> node number
        # value.data  -> reaction force vector
        for value in rfo.values:
            if sqrt(value.data[0]**2
                        + value.data[1]**2
                        + value.data[2]**2) < 1.e-20: continue
            result.nodeRFo[value.nodeLabel] = value.data
            self.appendLog("%5d %10.3e %10.3e %10.3e" %
                          (value.nodeLabel,
                           value.data[0], value.data[1], value.data[2]))
            for i in range(3): result.sumRFo[i] += value.data[i]

        # print reaction forces
        self.appendLog("> reaction force: %10.3f %10.3f %10.3f kN" %
                   (result.sumRFo[0] / 1000.,
                    result.sumRFo[1] / 1000.,
                    result.sumRFo[2] / 1000.))

        # copy displacements into result container
        disp = frame.fieldOutputs['U']
        for value in disp.values:
            result.nodeDis[value.nodeLabel] = value.data

        # calculate the maximum displacement along the selected line
        maxDisp = 0.
        for label in result.nodePos:
            disp = result.nodeDis[label]
            if fabs(disp[1]) > maxDisp: maxDisp = fabs(disp[1])
        self.appendLog("> max. vertical displacement: %.2f mm" % maxDisp)

        # create result plot files
        varList = ['U1', 'U3', 'U2']

        for var in varList:
            # select the component of the displacements
            self.viewport.odbDisplay.setPrimaryVariable(
                variableLabel='U',
                outputPosition=NODAL,
                refinement=(COMPONENT, var), )

        # fit the plot
            self.viewport.view.fitView()

        # set file name
            png = data.jobName + "-" + var
            self.printPngFile(png)

    # print a png file
    def printPngFile(self, name):
        session.printOptions.setValues(vpBackground=ON)
        session.printToFile(fileName=name,
                            format=PNG,
                            canvasObjects=(self.viewport,))



