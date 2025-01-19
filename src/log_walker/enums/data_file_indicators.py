"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class contains the enum for data file indicators
This is how the program knows which files to parse

"""

from enum import Enum


class DataFileIndicators(Enum):

    OFILE = ".sh.o"
    DELFILE = ".del"

    def isFileType(self, fileName):
        """
        Description: returns true if the file name is the same type as the indicator
                     otherwise returns false.
                     e.g. DataFileIndicators.OFILE.isFileType(fileName)
        Input: fileName(string) - The file name
        Return: bool
        """

        if self.value in fileName:
            return True
        return False

    @classmethod
    def isDataFileinFiles(self, fileNames: []):
        """
        Description: returns true if there is a data file in the group of files given
                     otherwise returns false
        Input: fileNames(Array) - An array of file names
        Return: bool
        """
        for file in fileNames:
            if self.isDataFile(file):
                return True
        return False

    @classmethod
    def isDataFile(self, fileName):
        """
        Description: returns true if the file contains any of the string indicators in this enum
                     otherwise returns false
        Input: fileName(string) - The file name
        Return: bool
        """
        for indicator in self:
            if indicator.value in fileName:
                return True
        return False
