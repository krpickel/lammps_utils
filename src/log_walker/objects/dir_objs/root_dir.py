"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is the highest level directory.

"""

from pathlib import Path
from src.log_walker.enums.data_file_indicators import DataFileIndicators
from src.log_walker.objects.dir_objs.directory import Directory
from src.log_walker.utils.file_utils import DirFileUtils


class RootDirectory(Directory):

    dataPresent: bool
    repPresent: bool
    replicateDirs: {}
    dataDirs: {}

    def __init__(self, path: str):
        """
        Constructor class
        """
        # Initialize the super class first
        super().__init__(path)
        self.dataDirs = {}
        self.repDirs = {}
        self.dataPresent = DirFileUtils.isDataDir(self.path.__str__())
        self.repPresent = DirFileUtils.isRepDir(self.path.__str__())

        self.setupDirectory(self.path)

    def setupDirectory(self, rootPath: Path):
        super().setupDirectory(rootPath)
