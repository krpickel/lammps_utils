"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is the highest level directory.

"""

from src.log_walker.objects.dir_objs.directory import Directory
from src.log_walker.objects.dir_objs.rep_dir import ReplicateDirectory
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
    dataPresent: bool
    repDir: ReplicateDirectory
    repPresent: bool

    def __init__(self, path: str):
        """
        Constructor class
        """
        # Initialize the super class first
        Directory.__init__(path)
        self.dataDirs = {}
        self.repDirs = {}
        self.dataPresent = DirFileUtils.isDataDir(self.path)
        self.repPresent = DirFileUtils.isRepDir(self.path)

        self.setupRootDirectory()

    def setupRootDirectory(self):
        if self.repPresent:
            self.repDir = ReplicateDirectory(self.path.__str__())
