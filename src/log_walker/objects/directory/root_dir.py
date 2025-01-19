"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is

"""

import pathlib as Path
from src.log_walker.enums.data_file_indicators import DataFileIndicators
from src.log_walker.objects.directory import Directory
from src.log_walker.utils.file_utils import DirFileUtils


class RootDirectory(Directory):

    dataDir: bool
    repDir: bool

    def __init__(self, rootPath: str):
        self.path = Path(rootPath)
        self.directories = []
        self.files = []
        self.dataDir = DirFileUtils.isDataDir(rootPath)
        self.repDir = DirFileUtils.isRepDir(rootPath)

    def setupDirectory(self, rootPath: Path, directories=[], files=[]):
        for entity in rootPath.iterdir():
            if entity.isdir():
                directories.append(entity)
            elif entity.isfile():
                files.append(entity)
                if not self.dataDir and DataFileIndicators.isDataFile(entity):
                    self.dataDir = True

            else:
                print("unrecognized entity")
        self.files = files
        self.directories = directories
