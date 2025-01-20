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


class Directory:

    path: Path
    subDirs: []
    files: []

    def __init__(self, path: str):
        self.files = []
        self.subDirs = []
        # don't @me
        self.path = Path(path)

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
