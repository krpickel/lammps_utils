"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class contains utility functions related to files and dirs

"""

import os
from pathlib import Path

from src.log_walker.enums.data_file_indicators import DataFileIndicators


class DirFileUtils:

    def appendFile(self, name: str):
        """
        Description: Creates a directory if it doesn't already exist
        Input:
                dir(string) - The directory to be appened to
        Return:
                file(file) - The opened file
        """

        if os.path.isfile(name):
            return self.__openFile__(name, "a")
        else:
            print("This is not a file")
            return 1 / 0

    def createDir(dirPath: str):
        """
        Description: Creates a directory if it doesn't already exist
        Input:
                dir(string) - The directory to be created
        """
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)

    def createFile(self, name: str):
        """
        Description: Creates a file.  If the file already exists, this will throw an error.
        Input:
                name(string) - The name of the file to be created
        Return:
                file(file) - The new file
        """
        return self.__openFile__(name, "x")

    def createOrTruncateFile(self, name: str):
        """
        Description: If a file already exists, this function will truncate it to zero bytes
        Input:
                name(string) - The name of the file to be created
        Return:
                file(file) - The new or turncated file
        """

        if os.path.isfile(name):
            f = self.__openFile__(name, "a")
            f.truncate(0)
            return f
        return self.__openFile__(name, "w")

    def isDir(path: str):
        return os.path.isdir(path)

    def openFile(name: str, parameter: str):
        """
        Description: If a file already exists, this function will truncate it to zero bytes
        Input:
                name(string)      - The name of the file to be opened \n
                parameter(string) - How the file will be opened       \n
                                    Accepted values: 'a' - append     \n
                                                     'r' - read       \n
                                                     'w' - write      \n
                                                     'x' - create     \n
        Return:
                file(file) - The opened file
        """
        acceptedParameters = ["a", "r", "w", "x"]
        if parameter in acceptedParameters:
            return open(name, parameter)
        else:
            print("Invalid Parameter")
            return 1 / 0

    def isDataDir(path: str):
        path = Path(path)
        fileNames = [file.name for file in path.iterdir() if file.is_file()]

        if DataFileIndicators.isDataFileinFiles(fileNames):
            return True
        return False

    @classmethod
    def isRepDir(self, path: str):
        entities = os.listdir(path)
        replicateDirs = {}
        dirs = []

        for entity in entities:
            if self.isDir(path + "/" + entity):
                dirs.append(entity)

        if dirs.__len__() > 1:
            repBaseName = ""
            for directory in dirs:
                if directory[directory.__len__() - 1].isdigit():
                    repBaseName = self.getRepRoot(directory)
                    if repBaseName not in replicateDirs.keys():
                        replicateDirs[repBaseName] = []
                    if directory not in replicateDirs[repBaseName]:
                        replicateDirs[repBaseName].append(directory)

                    print(replicateDirs[repBaseName])
                    for temp in dirs:
                        if directory == temp:
                            continue
                        elif repBaseName in temp and temp[temp.__len__() - 1].isdigit():
                            repNum = self.getRepNum(temp)
                            if repNum > 0 and temp not in replicateDirs[repBaseName]:
                                replicateDirs[repBaseName].append(temp)
        if replicateDirs.__len__() > 1:
            return True
        return False

    @classmethod
    def getRepRoot(self, dictionary: str):
        return self.getRepRootAndNum(dictionary)[0]

    @classmethod
    def getRepNum(self, dictionary: str):
        return self.getRepRootAndNum(dictionary)[1]

    @classmethod
    def getRepRootAndNum(self, directory: str):
        endNum = "0"
        repBaseName = None
        for i in range(1, directory.__len__()):
            character = directory[directory.__len__() - i]

            if character.isdigit():
                endNum = character + endNum
            elif character.isalpha():
                repBaseName = directory[: directory.__len__() - i + 1]
                break

        return str(repBaseName), int(endNum)
