"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class represents a directory with replicate directories in it.  It shouldn't have any data in it.

"""

from enum import Enum, auto


class DirType(Enum):

    DATA = auto()
    GENERAL = auto()
    REP = auto()
    STRAIN = auto()
