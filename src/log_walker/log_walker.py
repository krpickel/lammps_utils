"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is meant to be the super class for repWalker and possibly other walker classes

"""

import os

import pathlib as Path
from src.log_walker.enums.data_file_indicators import DataFileIndicators
from src.log_walker.objects.dir_objs.root_dir import RootDirectory
from src.log_walker.objects.o_file import OFile


# from src.log_walker.objects.del_file import DelFile
class LogWalker:

    inDir: str
    dataFiles: []
    rootDir: RootDirectory

    def __init__(self, inDir: str):
        self.inDir = inDir
        self.__logWalk__()

    def __logWalk__(self):
        """
        Description: Walks through all directories looking for LAMMPS log files
                     Currently only looks for o files and del files
        """
        inDir = self.inDir

        logFilePaths = {}
        for dirPath, dirNames, fileNames in os.walk(inDir):
            for fileName in fileNames:
                if (
                    DataFileIndicators.OFILE.value in fileName
                    or DataFileIndicators.DELFILE.value in fileName
                ):
                    logFilePaths[fileName] = str(dirPath).replace("\\", "/")
        self.__populateFiles__(logFilePaths)
        print(logFilePaths)

    def __populateFiles__(self, logFilePaths: dict):
        """
        Description: Populates the log file data into log_file objects
        Input: logFilePaths(dict) - A dictionary containing the log file names as keys
                                    and their directory path as the value
        """
        delFileID = 0
        for fileName in logFilePaths.keys():
            if DataFileIndicators.OFILE.value in fileName:
                # The unique ID of an o file is the o number wich serves as it's extension
                splitName = fileName.split(".")
                uniqueID = splitName[splitName.__len__() - 1]
                extn = "." + uniqueID
                oFile = OFile(logFilePaths[fileName], fileName, uniqueID, extn)
            elif DataFileIndicators.DELFILE.value in fileName:
                delFileID = +1
                uniqueID = "del" + delFileID

                os.rename(logFilePaths[fileName] + "/" + fileName + delFileID)

                extn = "." + uniqueID

                # delFile = DelFile(logFilePaths[fileName], fileName, uniqueID, extn)
