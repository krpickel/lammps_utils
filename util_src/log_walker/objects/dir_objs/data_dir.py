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

from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.objects.dir_objs.directory import Directory
from util_src.log_walker.objects.file_objs.del_file import DelFile
from util_src.log_walker.objects.file_objs.o_file import OFile
from util_src.log_walker.objects.file_objs.pos_file import PosFile


class DataDirectory(Directory):
    data_files: {}
    o_number: str
    pyro_bool: bool

    def __init__(self, path):
        super().__init__(path)
        self.data_files = {}
        self.o_number = ""
        self.pyro_bool = False
        self.setupDataDirectory()

    def setupDataDirectory(self):

        non_o_data_files = []
        # kind of weird but I want to get the O file processed first in the case of pyrolysis, so I can use the
        # o number for the unique ids for all data files in the directory
        for file in self.files:
            fileStr = str(file)
            if DataFileIndicators.is_data_file(fileStr):
                if DataFileIndicators.OFILE.is_file_type(fileStr):
                    self.populate_o_file(file)
                else:
                    non_o_data_files.append(file)

        # not populate non o files now that we have the o number
        for file in non_o_data_files:
            fileStr = str(file)
            if DataFileIndicators.DELFILE.is_file_type(fileStr):
                self.populate_del_file(file)
                if not self.pyro_bool:
                    self.pyro_bool = True
            elif DataFileIndicators.POSFILE.is_file_type(fileStr):
                self.populate_pos_file(file)
                if not self.pyro_bool:
                    self.pyro_bool = True

    def populate_o_file(self, file: Path):

        file_name = file.name
        unique_id = file_name.split("sh.")[1]

        self.o_number = unique_id

        self.data_files[unique_id] = OFile(str(file.parent), file_name, unique_id, "." + unique_id)

    def populate_del_file(self, file: Path):
        file_name = file.name
        extn = ".del"
        unique_id = self.o_number + "_del"

        self.data_files[unique_id] = DelFile(str(file.parent), file_name, unique_id, extn)

    def populate_pos_file(self, file):
        file_name = file.name
        extn = ".pos"
        unique_id = self.o_number + "_pos"

        self.data_files[unique_id] = PosFile(str(file.parent), file_name, unique_id, extn)
