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
from enum import Enum

class Elements(Enum):
    H = 1.008
    C = 12.011
    O = 15.999
    
    @classmethod
    def getWeight(self, atomStr : str):
        hydroStr = 'H'
        carbonStr = 'C'
        oxygenStr = 'O'
        totalWeight = 0

        if(atomStr.__contains__(hydroStr)):
            totalWeight += self.__getElmWeight__(atomStr, hydroStr, self.H.value)

        if(atomStr.__contains__(carbonStr)):
            totalWeight += self.__getElmWeight__(atomStr, carbonStr, self.C.value)
        
        if(atomStr.__contains__(oxygenStr)):
            totalWeight += self.__getElmWeight__(atomStr, oxygenStr, self.O.value)

        return totalWeight

    @classmethod
    def __getElmWeight__(self, atomStr, elmStr, elmWeight):
        weight = 0
        if(atomStr.__len__() > atomStr.index(elmStr)+1):
            if(atomStr[atomStr.index(elmStr)+1].isdigit()):
                weight += int(atomStr[atomStr.index(elmStr)+1]) * elmWeight
            else:
                weight += elmWeight
        else:
            weight += elmWeight
        return weight