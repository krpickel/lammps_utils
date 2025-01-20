"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class represents a directory with replicate directories in it.  It shouldn't have any data files in it.

"""

from src.log_walker.objects.dir_objs.directory import Directory
from src.log_walker.utils.file_utils import DirFileUtils


class ReplicateDirectory(Directory):

    replicateDirs: {}
    replicateDataDirs: {}

    def __init__(self, path: str):
        Directory.__init__(path)
        self.replicateDirs = {}

    def setupRepDirectory(self):
        self.replicateDirs = DirFileUtils.getRepDirs(self.path)

    def getRepBaseNames(self):
        """
        Description: \n
            Returns every replicate base name in the replicate directory which are the keys
            of the replicateDirs dictionary
        Return: \n
            replicateBaseNames(array) - An array of repBaseNames
        """
        return self.replicateDirs.keys()
