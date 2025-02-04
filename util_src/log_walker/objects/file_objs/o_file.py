"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is meant to be contain all of the data in an o file_objs

"""

import copy

import pandas as pd

from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.objects.file_objs.log_file import LogFile


class OFile(LogFile):
    errors: {}
    sections: {}
    dataSectionIDs: []
    type: DataFileIndicators
    warnings: {}

    def __init__(self, dirPath, name, uniqueID, extn):
        super().__init__(dirPath, name, uniqueID, extn)

        self.dataSectoionIDs = []
        self.errors = {}
        self.sections = {}
        self.warnings = {}
        self.type = DataFileIndicators.OFILE

        print("Reading o file: " + uniqueID)
        self.splitSections()
        print("Done reading: " + uniqueID)

    def splitSections(self):

        # TODO: alphabetize
        preDataHeaderLine = "Per MPI rank"
        headerNext = False
        inData = False
        dataSect = None
        inHeader = False
        headerSec = None
        headers = []
        warningID = 0
        errorID = 0
        sectionID = 1

        with open(self.getFullFilePath(), "r") as file:
            previousData = pd.DataFrame()
            for line in file:
                # if inHeader:
                #    if headerSec == None:
                #        headerSec = HeaderSection(0)
                if line.strip() != "" and not line == None:
                    if inData:
                        line = line.strip().split()
                        if previousData.empty:
                            if headers != line:
                                dataSect = DataSection(sectionID)
                                sectionID += 1
                                dataSect.setDataHeaders(line)
                                headers = line
                                previousData = pd.DataFrame(line)
                            else:
                                previousData = pd.DataFrame(
                                    dataSect.data.loc[len(dataSect.data) - 1]
                                )
                        elif line[0] == "WARNING:":
                            self.warnings[warningID] = line
                            warningID = +1
                        elif line[0] == "ERROR:":
                            self.errors[errorID] = line
                            errorID = +1
                        elif "Loop" == line[0]:
                            inData = False
                            previousData = pd.DataFrame()
                            # Need to use deepcopy or else the value in the dictionary
                            # will keep referencing dataSect and will be overridden
                            self.sections[dataSect.uniqueID] = copy.deepcopy(dataSect)
                            # previousData.iloc[0].iloc[0] gets the first value in the first column
                            # not the cleanest but it works
                        elif (
                                line[0] != previousData.iloc[0].iloc[0] and line != headers
                        ):
                            dataSect.addDataRow(line)
                            previousData = pd.DataFrame(line)

                    if "LAMMPS" in line:
                        # TODO: capture meaningful header section data
                        inHeader = True
                    elif preDataHeaderLine in line:
                        inData = True

                    if "WARNING" in line[0]:
                        self.warnings[warningID] = line
                        warningID = +1
                    elif "ERROR" in line[0]:
                        self.errors[errorID] = line
                        errorID = +1

    def getType(self):
        return self.type


class Section(object):
    uniqueID: int
    sectionType: str

    def __init__(self, uniqueID, sectType):
        self.uniqueID = uniqueID
        self.sectionType = sectType


class DataSection(Section):
    data: pd.DataFrame
    headerOrder: {}

    def __init__(self, uniqueID):
        super().__init__(uniqueID, "data")
        self.data = pd.DataFrame()
        self.headerOrder = {}

    def setDataHeaders(self, headers: []):
        headerNum = 0
        for header in headers:
            self.headerOrder[header] = headerNum
            self.data[header] = []
            headerNum += 1

    def addDataRow(self, newRow: []):
        self.data.loc[len(self.data)] = newRow


class SimBox:
    boxType: str
    posX: int
    negX: int
    posY: int
    negY: int
    posZ: int
    negZ: int

    def __init__(self, line):
        pass


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
