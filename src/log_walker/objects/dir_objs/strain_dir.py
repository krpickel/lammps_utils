"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class represents a directory with x, y, z stress strain data directories.  
It shouldn't have any replicate directories in it.

"""

from src.log_walker.enums.strain_direction import StrainDirection
from src.log_walker.objects.dir_objs.directory import Directory
from src.log_walker.utils.file_utils import DirFileUtils


class StrainDirectory(Directory):

    strainDataDirs: {}

    def __init__(self, path):
        super().__init__(path)
        self.strainDataDirs = {}

        self.setupStrainDir(self)

    def setupStrainDir(self):

        directionString = StrainDirection.getDirectionStringFromSubDirs(self.subDirs)

        print()
