"""
Candidate for deletion
it may have worked at one point, but I dont think it does anymore

See read_lammps_output.py for the real implementation
"""

import csv
from enum import Enum
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class Elements(Enum):
    H = 1.008
    C = 12.011
    O = 15.999

    def getWeight(self, atomStr: str):
        hydroStr = "H"
        carbonStr = "C"
        oxygenStr = "O"
        totalWeight = 0

        if atomStr.__contains__(hydroStr):
            print(atomStr.__len__())
            print(hydroStr)
            totalWeight += self.__getElmWeight__(atomStr, hydroStr, self.H.value)

        if atomStr.__contains__(carbonStr):
            print(atomStr.__len__())
            totalWeight += self.__getElmWeight__(atomStr, carbonStr, self.C.value)

        if atomStr.__contains__(oxygenStr):
            print(atomStr.__len__())
            totalWeight += self.__getElmWeight__(atomStr, oxygenStr, self.O.value)

        return totalWeight

    def __getElmWeight(self, atomStr, elmStr, elmWeight):
        weight = 0
        if atomStr.__len__() > atomStr.index(elmStr) + 1:
            if atomStr[atomStr.index(elmStr) + 1].isdigit():
                weight += int(atomStr[atomStr.index(elmStr) + 1]) * elmWeight
            else:
                weight += elmWeight
        else:
            weight += elmWeight
        return weight


class AtomDeleted(object):

    def __init__(self):
        pass

    clusterStr: str
    numOxygen: int
    numHydrogen: int
    numCarbon: int

    def setClusterStr(inClusterStr: str):
        self.clusterStr = inClusterStr
        hydroStr = "H"
        carbonStr = "C"
        oxygenStr = "O"

        if inClusterStr.__contains__(hydroStr):
            if inClusterStr.__len__() > inClusterStr.index(inClusterStr) + 1:
                if inClusterStr[inClusterStr.index(inClusterStr) + 1].isdigit():
                    self.numHydrogen = int(
                        inClusterStr[inClusterStr.index(inClusterStr) + 1]
                    )

        if inClusterStr.__contains__(carbonStr):
            print(inClusterStr.__len__())
            if inClusterStr.__len__() > inClusterStr.index(inClusterStr) + 1:
                if inClusterStr[inClusterStr.index(inClusterStr) + 1].isdigit():
                    self.numCarbon = int(
                        inClusterStr[inClusterStr.index(inClusterStr) + 1]
                    )

        if inClusterStr.__contains__(oxygenStr):
            print(inClusterStr.__len__())
            if inClusterStr.__len__() > inClusterStr.index(inClusterStr) + 1:
                if inClusterStr[inClusterStr.index(inClusterStr) + 1].isdigit():
                    self.numOxygen = int(
                        inClusterStr[inClusterStr.index(inClusterStr) + 1]
                    )

    def getOxygenWeight(self):
        return self.numOxygen * Elements.O.value

    def getCarbonWeight(self):
        return self.numCarbon * Elements.C.value

    def getHydrogenWeight(self):
        return self.numHydrogen * Elements.H.value

    def getTotalWeight(self):
        return (
            self.getOxygenWeight() + self.getCarbonWeight() + self.getHydrogenWeight()
        )


inDir = "C:/Users/asmon/mol_dyn/research/Phenolic_Resin/TP_Reax/4k/H2O/pyro/rep1"
outDir = (
    "C:/Users/asmon/mol_dyn/research/Phenolic_Resin/TP_Reax/4k/H2O/pyro/rep1/analysis"
)

logFiles = []
preHeaderLine = "Per MPI rank"

for files in os.walk(inDir):
    for names in files:
        for name in names:
            if ".del" in name:
                logFiles.append(name)

files = []
for file in logFiles:
    print(file)
    rawFile = None

    if not os.path.exists(outDir):
        os.makedirs(outDir)
    timestep = {}

    fileNo = 1
    with open(inDir + "/" + file, "r") as file:
        for line in file:
            atomDeleted = AtomDeleted()
            atomsDeleted = []
            data = line.split()
            atomDeleted.name = data[3]

            atomsDeleted.append(atomDeleted)
            if data.__len__() > 4:
                atomDeleted.name = data[5]
                atomDeleted.num = data[4]
                atomsDeleted.append(atomDeleted)
            if data.__len__() > 6:
                atomDeleted.name = data[7]
                atomDeleted.num = data[6]
                atomsDeleted.append(atomDeleted)
            if data.__len__() > 8:
                atomDeleted.name = data[9]
                atomDeleted.num = data[8]
                atomsDeleted.append(atomDeleted)
            timestep[data[1]] = atomsDeleted

    xData = []
    yData = []
    for key in timestep:
        atomsDeleted = timestep[key]
        print(key)
        for deleted in atomsDeleted:
            print(deleted.name)
            print(deleted.num)
            print("weight: " + str(Elements.getWeight(deleted.name) * int(deleted.num)))
            yData.append(Elements.getWeight(deleted.name) * int(deleted.num))
            xData.append(int(key) * 0.1 / 1000)

xData.pop(0)
yData.pop(0)

plt.plot(xData, yData, "o")
plt.show()
