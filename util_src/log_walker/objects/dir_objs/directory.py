"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class in an interface for all directory type objects

"""

from pathlib import Path

from util_src.log_walker.enums.dir_type import DirType
from util_src.log_walker.utils.file_utils import DirFileUtils


class Directory(object):
    """
    Description:
        This class the super class for all Directory objects.
    Variables:
        path(pathlib.Path) -A path object for the directory
        subDirs(array) - An array containing the subdirectory names
        files(array) - An array containing all of the file names
    """

    path: Path
    analysisPath: Path
    subDirObjs: {}
    subDirs: []
    files: []
    dataPresent: bool
    repPresent: bool
    strainPresent: bool

    def __init__(self, path):
        """
        Constructor Method
        """
        path = DirFileUtils.getPathObj(path)

        self.path = path
        self.files = DirFileUtils.getFiles(path)
        self.subDirs = DirFileUtils.getSubDirs(path)
        self.subDirObjs = self.setupSubDirObjs()
        self.dataPresent = DirFileUtils.isDataDir(path)
        self.repPresent = DirFileUtils.isRepDir(path)
        self.strainPresent = DirFileUtils.isStrainDir(path)

        self.setupDirectory()

    def getGeneralDirObjs(self):

        return self.subDirObjs[DirType.GENERAL.value]

    def setupDirectory(self):
        subDirs = self.subDirs

        if len(subDirs) > 0:
            for subDir in subDirs:
                if (
                        not DirFileUtils.isDataDir(subDir)
                        and not DirFileUtils.isRepDir(subDir)
                        and not DirFileUtils.isStrainDir(subDir)
                ):
                    self.subDirObjs[DirType.GENERAL.value].append(Directory(subDir))

    def setupSubDirObjs(self):
        subDirObjs = {}

        for dirType in DirType:
            subDirObjs[dirType.value] = []

        return subDirObjs

    def createAnalysisDir(self):
        # This is the correct way to append to a Path object
        path = self.path / "analysis"
        path.mkdir(exist_ok=True)
        self.analysisPath = path
