"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class in an interface for all directory type objects

"""

from abc import abstractmethod

import pathlib as Path


class Directory:

    path: Path
    subDirs: []
    files: []

    @abstractmethod
    def setupDirectory(path: str):
        pass
