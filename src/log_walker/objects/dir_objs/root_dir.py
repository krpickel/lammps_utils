"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is the highest level directory.

"""

from src.log_walker.enums.dir_type import DirType
from src.log_walker.objects.dir_objs.data_dir import DataDirectory
from src.log_walker.objects.dir_objs.directory import Directory
from src.log_walker.objects.dir_objs.rep_dir import ReplicateDirectory
from src.log_walker.objects.dir_objs.strain_dir import StrainDirectory
from src.log_walker.utils.file_utils import DirFileUtils


class RootDirectory(Directory):
    """
    Description:
        This class the top level directory of the analysis.
    Variables:
        dataDirs(array) - An array containing all of the data directories in the root
                          directory that are not replicates
        subDirs(array) - An array containing the subdirectory names
        files(array) - An array containing all of the file names
    """

    dataDirs: []
    dataDir: DataDirectory
    repDir: ReplicateDirectory
    strainDirs: []
    subRepDirs: []

    def __init__(self, path: str):
        """
        Constructor class
        """
        # Initialize the super class first
        super().__init__(path)
        self.dataDirs = []
        self.subRepDirs = []
        self.strainDirs = []

        if self.repPresent:
            self.repDir = ReplicateDirectory(self.path)
        if self.dataPresent:
            self.dataDir = DataDirectory(self.path)

        self.setupRootDirectory()

    def setupRootDirectory(self):
        subDirObjs = self.subDirObjs
        for subDir in self.subDirs:
            if DirFileUtils.isDataDir(subDir):
                subDirObjs[DirType.DATA.value].append(DataDirectory(subDir))
            elif DirFileUtils.isRepDir(subDir):
                subDirObjs[DirType.REP.value].append(ReplicateDirectory(subDir))
            elif DirFileUtils.isStrainDir(subDir):
                subDirObjs[DirType.STRAIN.value].append(StrainDirectory(subDir))
            else:
                pass
