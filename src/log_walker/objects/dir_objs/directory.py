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
    subDirs: []
    files: []

    @classmethod
    def __init__(self, path: str):
        """
        Constructor Method
        """
        self.files = []
        self.subDirs = []
        # don't @me
        self.path = Path(path)

        self.setupDirectory(self.path)

    @classmethod
    def setupDirectory(self, path: Path):
        directories = []
        files = []
        for entity in path.iterdir():
            if entity.is_dir():
                directories.append(entity)
            elif entity.is_file():
                files.append(entity)
            else:
                print("unrecognized entity")
        self.files = files
        self.subDirs = directories
        print(self.files)
        print(self.subDirs)
