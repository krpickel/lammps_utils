"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is the class for analyzing a pyro data directory

"""
from pathlib import Path

from util_src.log_walker.enums.data_cols import DataColumns
from util_src.log_walker.objects.anlzer.analizer import Analyzer
from util_src.log_walker.objects.dir_objs.data_dir import DataDirectory
from util_src.log_walker.objects.file_objs.del_file import DelFile
from util_src.log_walker.objects.file_objs.o_file import OFile
from util_src.log_walker.objects.file_objs.pos_file import PosFile


class PyroAnalyzer(Analyzer):
    pyro_dir: DataDirectory
    o_file: OFile
    del_file: DelFile
    pos_file: PosFile

    def __init__(self, path):
        """
        Constructor
        """
        super().__init__()

        pyro_dir = None
        if isinstance(path, Path):
            pyro_dir = DataDirectory(path)
        elif isinstance(path, DataDirectory):
            pyro_dir = path
        else:
            print("Incorrect input.  Input must be a pathlib.Path or a DataDirectory obj")
            raise Exception

        if not pyro_dir.pyro_bool:
            print("Not a pyrolysis data directory.  Exiting")
            raise Exception

        self.pyro_dir = pyro_dir
        data_files = pyro_dir.data_files
        for data_file in data_files.values():
            if isinstance(data_file, OFile):
                self.o_file = data_file
            elif isinstance(data_file, DelFile):
                self.del_file = data_file
            elif isinstance(data_file, PosFile):
                self.pos_file = data_file

    def plot_char_yield(self):
        o_file = self.o_file

        for section in o_file.sections:
            data = section.data

            if DataColumns.CHAR_YIELD.value in data.keys():
                pass
