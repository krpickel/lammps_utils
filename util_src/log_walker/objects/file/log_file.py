"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is meant to be the super class for oFile, delFile and possibly other log file classes

"""


class LogFile(object):
    """
    TODO: update this to just hold the pathlib.Path object and extract everything else from the Path object
    """

    name: str
    extn: str
    dirPath: str
    uniqueID: str

    def __init__(self, dirPath, name, uniqueID, extn):
        self.dirPath = dirPath
        self.name = name
        self.uniqueID = uniqueID
        self.extn = extn

    def getFullFilePath(self):
        return self.dirPath + "\\" + self.name
