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
    XYZ = "xyz"  # to handle when we want to average the x, y, and z directions
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

        directionDirs = []
        xString = cls.X.value
        yString = cls.Y.value
        zString = cls.Z.value

        for subDir in subDirs:
            lowerSubDir = subDir.name.lower()
            if xString == lowerSubDir:
                directionDirs.append(subDir)
            elif yString == lowerSubDir:
                directionDirs.append(subDir)
            elif zString == lowerSubDir:
                directionDirs.append(subDir)

        directionDirs.sort()

        return directionDirs

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
        directionDirs = cls.getDirectionStringFromSubDirs(subDirs)

        if not directionDirs:
            return False
        return True
