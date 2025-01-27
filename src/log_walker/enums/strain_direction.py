"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is an enum of strain directions

"""

from enum import Enum
from pathlib import Path


class StrainDirection(Enum):

    X = "x"
    Y = "y"
    Z = "z"

    # TODO: Add shear directions
    @classmethod
    def getDirectionStringFromSubDirs(cls, subDirs: []):
        """
        Description: \n
            Returns an alphabetized string string of strain directions found in the subdirectories
            e.g. returns "xyz" if all three uniaxial strain directories are present
                 returns "xy" if there are only x and y strain direction directories
                 ect...
        Input: \n
            list[pathlib.Path] - A list of subdirectories\n
        Return: \n
            string - An alphabetized string of the directions found in the sub directories
        """

        directionString = ""
        xString = cls.X.value
        yString = cls.Y.value
        zString = cls.Z.value

        for subDir in subDirs:
            lowerSubDir = subDir.name.lower()
            if xString == lowerSubDir:
                directionString += xString
            elif yString == lowerSubDir:
                directionString += yString
            elif zString == lowerSubDir:
                directionString += zString
        return sorted(directionString).__str__()

    @classmethod
    def isStrainRootDir(cls, path: Path):
        """
        Description: \n
            Returns true if there is at least one subdirectory with a strain direction
        Input: \n
            list[pathlib.Path] - A list of subdirectories\n
        Return: \n
            string - An alphabetized string of the directions found in the sub directories
        """
        subDirs = []
        for entity in path.iterdir():
            if entity.is_dir():
                subDirs.append(entity)
        directionString = cls.getDirectionStringFromSubDirs(subDirs)

        if directionString == "":
            return False
        return True
