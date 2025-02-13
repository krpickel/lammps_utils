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
    POSFILE = ".pos"

    def is_file_type(self, file_name):
        """
        Description:
            returns true if the file name is the same type as the indicator
            otherwise returns false.
            e.g.
                DataFileIndicators.OFILE.isFileType(file_name)
        Input:
            file_name(string) - The file name
        Return:
            bool
        """

        if self.value in file_name:
            return True
        return False

    @classmethod
    def isDataFileinFiles(cls, file_names: []):
        """
        Description:
            returns true if there is a data file in the group of files given
            otherwise returns false
        Input:
            file_names(Array) - An array of file names
        Return:
            bool
        """
        for file in file_names:
            if cls.is_data_file(file):
                return True
        return False

    @classmethod
    def is_data_file(cls, file_name):
        """
        Description:
            returns true if the file contains any of the string indicators in this enum
            otherwise returns false
        Input:
            fileName(string) - The file name
        Return:
            bool
        """
        for indicator in cls:
            if indicator.value in file_name:
                return True
        return False
