# -*- coding: utf-8 -*-
"""
@author: Keith Pickelmann
Revision 1.0
November 12th, 2024
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This file contains an enum class for values related to the periodic table of elements
"""
from enum import Enum

"""
class: Elements
desc:  Contains values like weight and name.  Could be expanded to hold more elements and values

current elements: C, H, O
"""
class Elements(Enum):
    
    C = 12.011
    H = 1.008
    O = 15.999