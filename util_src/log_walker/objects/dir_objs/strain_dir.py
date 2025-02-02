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

from util_src.log_walker.enums.strain_direction import StrainDirection
from util_src.log_walker.objects.dir_objs.data_dir import DataDirectory
from util_src.log_walker.objects.dir_objs.directory import Directory
from util_src.log_walker.utils.file_utils import DirFileUtils


class StrainDirectory(Directory):

    # TODO: add shear direction directories
    xDataDir: DataDirectory
    yDataDir: DataDirectory
    zDataDir: DataDirectory

    def __init__(self, path):
        """
        Constructor method
        """
        super().__init__(path)

        self.setupStrainDir()

    def setupStrainDir(self):

        directionDirs = StrainDirection.getDirectionStringFromSubDirs(self.subDirs)

        for directionDir in directionDirs:
            lowerDirName = directionDir.name.lower()
            if StrainDirection.X.value == lowerDirName:
                self.xDataDir = DataDirectory(directionDir)
            elif StrainDirection.Y.value == lowerDirName:
                self.yDataDir = DataDirectory(directionDir)
            elif StrainDirection.Z.value == lowerDirName:
                self.zDataDir = DataDirectory(directionDir)

    def getXDataDir(self):
        return self.xDataDir

    def getYDataDir(self):
        return self.yDataDir

    def getZDataDir(self):
        return self.zDataDir
