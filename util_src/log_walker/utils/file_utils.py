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
from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.enums.strain_direction import StrainDirection


class DirFileUtils(object):

    @classmethod
    def appendFile(cls, name: str):
        """
        Description: Creates a file if it doesn't already exist \n
        Input: \n
                name(string) - The name of the file to be appened to \n
        Return: \n
                file(file) - The opened file
        """

        if os.path.isfile(name):
            return cls.__openFile__(name, "a")
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

    @classmethod
    def createFile(cls, name: str):
        """
        Description: Creates a file.  If the file already exists, this will throw an error. \n
        Input: \n
                name(string) - The name of the file to be created \n
        Return: \n
                file(file) - The new file
        """
        return cls.openFile(name, "x")

    @classmethod
    def createOrTruncateFile(cls, name: str):
        """
        Description: If a file already exists, this function will truncate it to zero bytes \n
        Input: \n
                name(string) - The name of the file to be created \n
        Return: \n
                file(file) - The new or turncated file
        """

        if os.path.isfile(name):
            f = cls.openFile(name, "a")
            f.truncate(0)
            return f
        return cls.openFile(name, "w")

    @classmethod
    def getFiles(cls, path):
        """
        Description: Takes a full directory path and returns the files as \n
                     a list of pathlib.Paths \n
        Input: \n
                path(string or pathlib.Path) - The full path of the directory \n
        Return: \n
                list - A list of pathlib.Path objects
        """

        return cls.getFilesAndSubDirs(path)[0]

    @classmethod
    def getFilesAndSubDirs(cls, path):
        """
        Description: Takes a full directory path and returns the files and subdirectories as \n
                     a list of pathlib.Paths\n
        Input: \n
                path(string or pathlib.Path) - The full path of the directory \n
        Return: \n
                list, list - Both are a list of pathlib.Path objects
        """

        path = cls.getPathObj(path)
        subDirs = []
        files = []

        for entity in path.iterdir():
            if entity.is_dir():
                subDirs.append(entity)
            elif entity.is_file():
                files.append(entity)
        return files, subDirs

    @classmethod
    def getSubDirs(cls, path):
        """
        Description: Takes a full directory path and returns the sub directories as \n
                     a list of pathlib.Paths \n
        Input: \n
                path(string or pathlib.Path) - The full path of the directory \n
        Return: \n
                list - A list of pathlib.Path objects
        """

        return cls.getFilesAndSubDirs(path)[1]

    def getPathObj(path):
        """
        Description: Takes a full directory path and returns a pathlib.Path object of that directory path \n
        Input: \n
                path(string or pathlib.Path) - The full path of the directory \n
        Return: \n
                Path - A pathlib.Path object of the path
        """
        if isinstance(path, Path):
            return path
        return Path(path)

    @classmethod
    def getRepDirs(cls, path):
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

        path = cls.getPathObj(path)

        replicateDirs = {}
        dirs = cls.getSubDirs(path)

        if dirs.__len__() > 1:
            repBaseName = ""
            for directory in dirs:
                if directory.name[len(directory.name) - 1].isdigit():
                    repBaseName = cls.getRepRoot(directory)
                    if repBaseName not in replicateDirs.keys():
                        replicateDirs[repBaseName] = []
                    if directory not in replicateDirs[repBaseName]:
                        replicateDirs[repBaseName].append(directory)

                    for temp in dirs:
                        if directory == temp:
                            continue
                        elif (
                            repBaseName in temp.name
                            and temp.name[len(temp.name) - 1].isdigit()
                        ):
                            repNum = cls.getRepNum(temp)
                            if repNum > 0 and temp not in replicateDirs[repBaseName]:
                                replicateDirs[repBaseName].append(temp)

        # If you try to remove a key from a dictionary while iterating over it
        # it causes an error so use a second for loop after figuring out which keys only hold
        # one directory.s
        popKeys = []
        for key in replicateDirs.keys():
            if not len(replicateDirs[key]) > 1:
                popKeys.append(key)
        if len(popKeys) > 0:
            for popKey in popKeys:
                replicateDirs.pop(popKey, None)
        return replicateDirs

    @classmethod
    def getRepNum(cls, dictionaryName: str):
        """
        Description: \n
            Calls getRepRootAndNum but only returns the replicate number \n
        Input: \n
            directoryName(string) - The directory name to be parsed \n
        Return: \n
            int
        """
        return cls.getRepRootAndNum(dictionaryName)[1]

    @classmethod
    def getRepRoot(cls, dictionary: str):
        """
        Description: \n
            Calls getRepRootAndNum but only returns the replicate root name \n
        Input: \n
            directoryName(string) - The directory name to be parsed \n
        Return: \n
            string
        """
        return cls.getRepRootAndNum(dictionary)[0]

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
        nameLen = len(directoryName.name)
        for i in range(1, nameLen):
            character = directoryName.name[nameLen - i]

            if character.isdigit():
                if repNum == None:
                    repNum = character
                else:
                    repNum = character + repNum
            elif character.isalpha():
                repBaseName = directoryName.name[: nameLen - i + 1]
                break

        return str(repBaseName), int(repNum)

    @classmethod
    def isRepDir(cls, path):
        """
        Description: \n
            Returns true if it finds replicate directories.  See getRepDirs for specifics \n
            on the logic of deciding which directories are replicates
        Input: \n
            path(string or pathlib.Path) - The full path to the directory being checked \n
        Return: \n
            bool
        """

        repDirs = cls.getRepDirs(path)
        isDirRep = len(repDirs) > 0

        return isDirRep

    def isStrainDir(path: Path):
        """
        Description: \n
            Calls the StrainDirection enum and returns it's return.  Kind of redundant but it feels
            like an appropriate method for the utils since isDataDir and isRepDir are also here
        Input: \n
            path(string or pathlib.Path) - The full path to the directory being checked \n
        Return: \n
            bool
        """
        return StrainDirection.isStrainRootDir(path)

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
