"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class represents a directory with replicate directories in it.  It shouldn't have any data files in it.

"""

import copy

from util_src.log_walker.objects.dir_objs.data_dir import DataDirectory
from util_src.log_walker.objects.dir_objs.directory import Directory
from util_src.log_walker.objects.dir_objs.strain_dir import StrainDirectory
from util_src.log_walker.utils.file_utils import DirFileUtils


class ReplicateDirectory(Directory):
    replicateDirs: {}
    replicateDataDirs: {}
    type: str

    def __init__(self, path):
        super().__init__(path)
        self.replicateDirs = {}

        self.replicateDirs, self.replicateDataDirs = self.setupRepDirectory()

    def setupRepDirectory(self):
        replicateDirs = DirFileUtils.getRepDirs(self.path)
        replicateDataDirs = {}

        for key in replicateDirs.keys():
            repDataDirs = []
            for repDir in replicateDirs[key]:
                if DirFileUtils.isDataDir(repDir):
                    self.type = "data"
                    repDataDirs.append(DataDirectory(repDir))
                elif DirFileUtils.isStrainDir(repDir):
                    self.type = "strain"
                    repDataDirs.append(StrainDirectory)
                else:
                    pass

            replicateDataDirs[key] = copy.deepcopy(repDataDirs)

        return replicateDirs, replicateDataDirs

    def getRepBaseNames(self):
        """
        Description: \n
            Returns every replicate base name in the replicate directory which are the keys
            of the replicateDirs dictionary
        Return: \n
            replicateBaseNames(array) - An array of repBaseNames
        """
        return self.replicateDirs.keys()
