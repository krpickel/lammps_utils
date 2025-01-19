"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is meant to be contain all of the data in an o file

"""

import os

import pandas as pd
from src.log_walker.objects.log_file import LogFile
from src.log_walker.utils.file_utils import DirFileUtils


class OFile(LogFile):

    sections: dict()
    errors: {}
    warnings: {}

    def ___init__(self, dirPath, name, uniqueID, extn):
        self.dirPath = dirPath
        self.name = name
        self.uniqueID = uniqueID
        self.extn = extn

        self.splitSections()

    def splitSections():
        inDir = self.dirPath
        preDataHeaderLine = "Per MPI rank"

        headerNext = False
        dataNext = False
        reactData = False
        inData = False
        inHeader = False
        sectType = None
        headerSec = None
        with open(inDir + "/" + self.name + self.extn, "r") as file:

            for line in file:

                if inHeader:
                    if headerSec == None:
                        headerSec = HeaderSection(0)

                if "LAMMPS" in line:
                    inHeader = True
                    sectType = "header"
                elif preDataHeaderLine in line:
                    inData = True
                    sectType = "data"

                if "Loop time" in line:
                    dataNext = False

                line = line.strip().split()

                if "WARNING" in line[0]:
                    continue
                elif "ERROR" in line[0]:
                    continue


class Section:

    uniqueID: int
    sectionType: str


class DataSection(Section):

    headers: []
    rows: {}

    def __init__(self, uniqueID, sectionType):
        self.uniqueID = uniqueID
        self.sectionType = sectionType


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
        self.uniqueID = uniqueID
        self.sectionType = "Header"

        self.populateSection(self)

    def populateBox(self, line):
        self.simBox = SimBox(line)
