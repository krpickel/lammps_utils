"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class represents a directory with data in it.  It shouldn't have any replicate directories in it.

"""

from pathlib import Path

from src.log_walker.enums.data_file_indicators import DataFileIndicators
from src.log_walker.objects.dir_objs.directory import Directory
from src.log_walker.objects.o_file import OFile


class DataDirectory(Directory):

    dataFiles: {}

    def __init__(self, path: str):
        super().__init__(path)
        self.dataFiles = {}

        self.setupDataDirectory()

    def setupDataDirectory(self):
        for file in self.files:
            fileStr = file.__str__()
            if DataFileIndicators.isDataFile(fileStr):
                if DataFileIndicators.OFILE.isFileType(fileStr):
                    self.populateOFile(file)
                elif DataFileIndicators.DELFILE.isFileType(fileStr):
                    self.populateDelFile(file)
                else:
                    print("Not a data file but passed the is data file check.  Huh?")

    def populateOFile(self, file: Path):

        fileName = file.name
        uniqueID = fileName.split("sh.")[1]
        extn = "." + uniqueID
        oFile = OFile(file.parent.__str__(), fileName, uniqueID, extn)
        self.dataFiles[uniqueID] = oFile
        for sectionKey in oFile.sections.keys():
            data = oFile.sections[sectionKey].data
            print(data)

        print(oFile)

    def populateDelFile(self, file: Path):
        pass
