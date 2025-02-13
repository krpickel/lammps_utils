"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class is meant to be the super class for oFile, delFile and possibly other log file_objs classes

"""


class LogFile(object):
    """
    TODO: update this to just hold the pathlib.Path object and extract everything else from the Path object
    """

    name: str
    extn: str
    dir_path: str
    unique_id: str

    def __init__(self, dir_path, name, unique_id, extn):
        self.dir_path = dir_path
        self.name = name
        self.unique_id = unique_id
        self.extn = extn

    def get_full_file_path(self):
        return self.dir_path + "\\" + self.name
