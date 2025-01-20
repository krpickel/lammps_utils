"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is meant to be contain all of the data in an o file

"""

import pandas as pd
from src.log_walker.objects.log_file import LogFile


class OFile(LogFile):

    errors: {}
    sections: {}
    dataSectionIDs: []
    warnings: {}

    def ___init__(dirPath, name, uniqueID, extn):
        LogFile.__init__(dirPath, name, uniqueID, extn)
        print("Here")
        self.errors = {}
        self.sections = {}
        self.dataSectoionIDs = []
        self.warnings = {}

        self.splitSections()
        print()

    def splitSections():
        inDir = self.dirPath
        preDataHeaderLine = "Per MPI rank"

        headerNext = False
        reactData = False
        inData = False
        inHeader = False
        sectType = None
        headerSec = None
        headers = []
        warningID = 0
        errorID = 0
        sectionID = 0
        with open(inDir + "/" + self.name + self.extn, "r") as file:
            previousData = [-1]
            for line in file:
                line = line.strip().split()
                # if inHeader:
                #    if headerSec == None:
                #        headerSec = HeaderSection(0)
                if inData:
                    if previousData == [-1]:
                        dataSect = DataSection(0)
                        dataSect.setDataHeaders(line)
                        headers = line

                    elif line[0] == previousData[0] or line == headers:
                        dataSect.addDataRow(line)
                    elif line[0] == "WARNING":
                        self.warnings[warningID] = line
                        warningID = +1
                    elif line[0] == "ERROR":
                        self.errore[errorID] = line
                        errorID = +1

                if "LAMMPS" in line:
                    # TODO: capture meaningful header data
                    inHeader = True
                elif preDataHeaderLine in line:
                    inData = True

                if "Loop time" in line:
                    inData = False
                    previousData = [-1]
                    self.sections[sectionID] = dataSect

                line = line.strip().split()

                if "WARNING" in line[0]:
                    self.warnings[warningID] = line
                    warningID = +1
                elif "ERROR" in line[0]:
                    self.errore[errorID] = line
                    errorID = +1


class Section:

    uniqueID: int
    sectionType: str

    def __init__(self, uniqueID, sectType):
        self.uniqueID = uniqueID
        self.sectionType = sectType


class DataSection(Section):

    data: pd.DataFrame
    headerOrder: {}

    def __init__(self, uniqueID):
        Section.__init__(uniqueID, "data")
        self.data = pd.DataFrame()
        self.headerOrder = {}

    @classmethod
    def setDataHeaders(self, headers: []):
        headerNum = 0
        for header in headers:
            self.headerOrder[header] = headerNum
            self.data[header] = []
            headerNum = +1

    @classmethod
    def addDataRow(self, row: []):
        pd.concat(self.data, row)


class SimBox:

    boxType: str
    posX: int
    negX: int
    posY: int
    negY: int
    posZ: int
    negZ: int

    def __init__(self, line):

        print(line)


class HeaderSection(Section):

    headerAtoms: int
    velocities: int
    bonds: int
    angles: int
    dihedrals: int
    impropers: int
    simBox: SimBox

    def __init__(self, uniqueID):
        Section.__init__(uniqueID, "header")

        self.populateSection(self)

    def populateBox(self, line):
        self.simBox = SimBox(line)
