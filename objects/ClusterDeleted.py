# -*- coding: utf-8 -*-
"""
@author: Keith Pickelmann
Revision 1.0
November 12th, 2024
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This file contains 
"""

from objects.Elements import Elements


class ClusterDeleted:

    clusterStr:str
    numOxygen:int
    numHydrogen:int
    numCarbon:int
    numCluster:int
    
    def __init__(self, clusterStr:str, numCluster:int):
        self.clusterStr = clusterStr
        self.numCluster = numCluster
        hydroStr = 'H'
        carbonStr = 'C'
        oxygenStr = 'O'
        
        if(clusterStr.__contains__(hydroStr)):
            if(clusterStr.__len__() > clusterStr.index(hydroStr) + 1):
                if(clusterStr[clusterStr.index(hydroStr) + 1].isdigit()):
                    self.numHydrogen = int(clusterStr[clusterStr.index(hydroStr) + 1])
                else:
                    self.numHydrogen = 1
            else:
                self.numHydrogen = 1
        else:
            self.numHydrogen = 0
        if(clusterStr.__contains__(carbonStr)):
            print(clusterStr.__len__())
            if(clusterStr.__len__() > clusterStr.index(carbonStr) + 1):
                if(clusterStr[clusterStr.index(carbonStr) + 1].isdigit()):
                    self.numCarbon = int(clusterStr[clusterStr.index(carbonStr) + 1])
                else:
                    self.numCarbon = 1
            else:
                self.numCarbon = 1
        else:
            self.numCarbon = 0
        if(clusterStr.__contains__(oxygenStr)):
            print(clusterStr.__len__())
            if(clusterStr.__len__() > clusterStr.index(oxygenStr) + 1):
                if(clusterStr[clusterStr.index(oxygenStr) + 1].isdigit()):
                    self.numOxygen = int(clusterStr[clusterStr.index(oxygenStr) + 1])
                else:
                    self.numOxygen = 1
            else:
                self.numOxygen = 1
        else:
            self.numOxygen = 0

    def getOxygenWeight(self):
        return float(self.numCluster) * float(self.numOxygen) * Elements.O.value
    
    def getCarbonWeight(self):
        return float(self.numCluster) * float(self.numCarbon) * Elements.C.value
    
    def getHydrogenWeight(self):
        return float(self.numCluster) * float(self.numHydrogen) * Elements.H.value
    
    def getTotalWeight(self):
        return self.getOxygenWeight() + self.getCarbonWeight() + self.getHydrogenWeight()
