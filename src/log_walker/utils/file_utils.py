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


class DirFileUtils(object):

    def appendFile(self, name: str):
        """
        Description: Creates a file if it doesn't already exist \n
        Input: \n
                name(string) - The name of the file to be appened to \n
        Return: \n
                file(file) - The opened file
        """

        if os.path.isfile(name):
            return self.__openFile__(name, "a")
        else:
            print("This is not a file")
            return 1 / 0

    def createDir(dirPath: str):
        """
        Description: Creates a directory if it doesn't already exist \n
        Input: \n
                dir(string) - The directory to be created
        """
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)

    def createFile(self, name: str):
        """
        Description: Creates a file.  If the file already exists, this will throw an error. \n
        Input: \n
                name(string) - The name of the file to be created \n
        Return: \n
                file(file) - The new file
        """
        return self.__openFile__(name, "x")

    def createOrTruncateFile(self, name: str):
        """
        Description: If a file already exists, this function will truncate it to zero bytes \n
        Input: \n
                name(string) - The name of the file to be created \n
        Return: \n
                file(file) - The new or turncated file
        """

        if os.path.isfile(name):
            f = self.__openFile__(name, "a")
            f.truncate(0)
            return f
        return self.__openFile__(name, "w")

    @classmethod
    def getRepDirs(self, path):
        """
        Description: \n
            Finds replicate dirs.  Each replicate should have a basename followed by a number. \n
            This is due to how getRepRootAndNum() works
            e.g. rep1, rep2, and rep3 have 'rep' as the basename \n
        Input: \n
            path(string or pathlib.Path) - The full path to the directory being checked \n
        Return: \n
            replicateDirs(directory) - A directory with repBaseName as the keys and Path as the value
        """

        if isinstance(path, Path):
            path = path.__str__()
        elif isinstance(path, str):
            pass
        else:
            print("unrecognized type\n")
            print("See documentation for isRepDir")
            return False

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

                    for temp in dirs:
                        if directory == temp:
                            continue
                        elif repBaseName in temp and temp[temp.__len__() - 1].isdigit():
                            repNum = self.getRepNum(temp)
                            if repNum > 0 and temp not in replicateDirs[repBaseName]:
                                replicateDirs[repBaseName].append(temp)
        return replicateDirs

    @classmethod
    def getRepNum(self, dictionaryName: str):
        """
        Description: \n
            Calls getRepRootAndNum but only returns the replicate number \n
        Input: \n
            directoryName(string) - The directory name to be parsed \n
        Return: \n
            int
        """
        return self.getRepRootAndNum(dictionaryName)[1]

    @classmethod
    def getRepRoot(self, dictionary: str):
        """
        Description: \n
            Calls getRepRootAndNum but only returns the replicate root name \n
        Input: \n
            directoryName(string) - The directory name to be parsed \n
        Return: \n
            string
        """
        return self.getRepRootAndNum(dictionary)[0]

    def getRepRootAndNum(directoryName: str):
        """
        Description: \n
            Takes a replicate directory name and gets the base name and the replicate number
            It builds the replicate number by taking the last character and seeing if its a digit
            if it is, append it to the repNum and check the character previous to it.  Once the first alpha
            character is found(starting from the right), use everything up to, and including, that character as the repBaseName

            e.g. rep1, baseName=rep, repNum=1
                 r2_12, baseName=r2_, repNum=12
        Input: \n
            directoryName(string) - The directory name to be parsed \n
        Return: \n
            int
        """
        repNum = None
        repBaseName = None
        nameLen = directoryName.__len__()
        for i in range(1, nameLen):
            character = directoryName[nameLen - i]

            if character.isdigit():
                if repNum == None:
                    repNum = character
                else:
                    repNum = character + repNum
            elif character.isalpha():
                repBaseName = directoryName[: nameLen - i + 1]
                break

        return str(repBaseName), int(repNum)

    @classmethod
    def isRepDir(self, path):
        """
        Description: \n
            Returns true if it finds replicate directories.  See getRepDirs for specifics \n
            on the logic of deciding which directories are replicates
        Input: \n
            path(string or pathlib.Path) - The full path to the directory being checked \n
        Return: \n
            bool
        """
        return self.getRepDirs(path).__len__() > 1

    def isDataDir(path):
        """
        Description: \n
            Checks if the path given is a directory \n
        Input: \n
            path(string or pathlib.Path) - The full path to the directory being checked \n
        Return: \n
            bool
        """

        if isinstance(path, Path):
            pass
        elif isinstance(path, str):
            path = Path(path)
        else:
            print("unrecognized format")
            return 1 / 0

        fileNames = [file.name for file in path.iterdir() if file.is_file()]

        if DataFileIndicators.isDataFileinFiles(fileNames):
            return True
        return False

        if DataFileIndicators.isDataFileinFiles(fileNames):
            return True
        return False

    def isDir(path: str):
        """
        Description: \n
            Checks if the path given is a directory \n
        Input: \n
            path(string) - The full path to the directory being checked \n
        Return: \n
            bool
        """
        return os.path.isdir(path)

    def openFile(name: str, parameter: str):
        """
        Description: If a file already exists, this function will truncate it to zero bytes \n
        Input: \n
                name(string)      - The name of the file to be opened \n
                parameter(string) - How the file will be opened       \n
                                    Accepted values: 'a' - append     \n
                                                     'r' - read       \n
                                                     'w' - write      \n
                                                     'x' - create     \n
        Return: \n
                file(file) - The opened file
        """
        acceptedParameters = ["a", "r", "w", "x"]
        if parameter in acceptedParameters:
            return open(name, parameter)
        else:
            print("Invalid Parameter")
            return 1 / 0
