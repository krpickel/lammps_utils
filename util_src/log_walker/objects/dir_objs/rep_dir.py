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

from util_src.log_walker.enums.dir_type import DirType
from util_src.log_walker.objects.dir_objs.data_dir import DataDirectory
from util_src.log_walker.objects.dir_objs.directory import Directory
from util_src.log_walker.objects.dir_objs.strain_dir import StrainDirectory
from util_src.log_walker.utils.file_utils import DirFileUtils


class ReplicateDirectory(Directory):
    replicate_dirs: {}
    replicate_data_dirs: {}
    type: DirType

    def __init__(self, path):
        super().__init__(path)

        self.replicate_dirs = {}
        self.replicate_dirs, self.replicate_data_dirs = self.setup_rep_directory()

    def setup_rep_directory(self):
        replicate_dirs = DirFileUtils.getRepDirs(self.path)
        replicate_data_dirs = {}

        for key in replicate_dirs.keys():
            rep_data_dirs = []
            for repDir in replicate_dirs[key]:

                if DirFileUtils.isDataDir(repDir):
                    print("Creating data directory:" + str(repDir))

                    self.type = DirType.DATA
                    rep_data_dirs.append(DataDirectory(repDir))
                elif DirFileUtils.isStrainDir(repDir):
                    print("Creating strain directory:" + str(repDir))
                    
                    self.type = DirType.STRAIN
                    rep_data_dirs.append(StrainDirectory(repDir))
                else:
                    pass

            replicate_data_dirs[key] = copy.deepcopy(rep_data_dirs)

        return replicate_dirs, replicate_data_dirs
