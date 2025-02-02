# -*- coding: utf-8 -*-
"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This file contains the object for holding data from a row in a del file generated from a LAMMPS pyrolysis simulation

"""

# Needed for values related to elements from the periodic table
from util_src.objects.Elements import Elements


"""
class: ClusterDeleted
desc: An object that holds the cluster data for a cluster that was deleted
      Currently it only works for carbon, hydrogen, and oxygen but could easily be
      expanded.  This class is also capable of returning the weight of individual elements
      in the cluster, and the total weight of the cluster.

init: self,
      clusterStr: The string of a deleted cluster
                  e.g. 'C3H'
      numCluster: the number of clusters deleted
functions: getOxygenWeight(self),
           getCarbonWeight(self),
           getHydrogenWeight(self),
           getTotalWeight(self)
"""
class ClusterDeleted:

    def __init__(self, clusterStr:str, numCluster:int):
        # set the object variables equal to the inputs
        self.clusterStr = clusterStr
        self.numCluster = numCluster

        # elementDict holds the elements in the clusterStr as the keys and
        # the number of that element as the value
        self.elementDict = {}

        for element in Elements:
            elmStr = str(element.name)

            if(clusterStr.__contains__(elmStr)):
                # Checks if there is a value after the element in the string
                # if so, if the value after the element is a number, if it is a number
                # then there are that many atoms of the element in the string
                # otherwise, there is only one atom of that element in the string
                if(clusterStr.__len__() > clusterStr.index(elmStr) + 1):
                    if(clusterStr[clusterStr.index(elmStr) + 1].isdigit()):
                        self.elementDict[elmStr] = int(clusterStr[clusterStr.index(elmStr) + 1])
                    else:
                        self.elementDict[elmStr] = 1
                else:
                    self.elementDict[elmStr] = 1
            else:
                self.elementDict[elmStr] = 0
                

    # Gets the total weight of the oxygen present in the cluster(s)
    def getOxygenWeight(self):
        return float(self.numCluster) * float(self.elementDict[str(Elements.O.name)]) * Elements.O.value
    
    # Gets the total weight of the carbon present in the cluster(s)
    def getCarbonWeight(self):
        return float(self.numCluster) * float(self.elementDict[str(Elements.C.name)]) * Elements.C.value

    # Gets the total weight of the hydrogen present in the cluster(s)
    def getHydrogenWeight(self):
        return float(self.numCluster) * float(self.elementDict[str(Elements.H.name)]) * Elements.H.value

    # # Gets the total weight of the cluster(s)
    def getTotalWeight(self):
        return self.getOxygenWeight() + self.getCarbonWeight() + self.getHydrogenWeight()
