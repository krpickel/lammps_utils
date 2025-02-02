"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is the class for analyzing replicates of strain directories

"""

from util_src.log_walker.objects.anlzer.analizer import Analyzer
from util_src.log_walker.objects.dir_objs.rep_dir import ReplicateDirectory


class StrainRepAnalyzer(Analyzer):

    repDir: ReplicateDirectory

    def __init__(self, repDir: ReplicateDirectory):
        super().__init__()
        self.repDir = repDir
