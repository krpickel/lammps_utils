"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is the super class for analyzers

"""

from util_src.log_walker.objects.anlzer.analizer import Analyzer
from util_src.log_walker.objects.dir_objs.root_dir import RootDirectory


class RootAnalyzer(Analyzer):

    rtDir: RootDirectory

    def __init__(self, rtDir: RootDirectory):
        super().__init__()
        self.rtDir = rtDir
