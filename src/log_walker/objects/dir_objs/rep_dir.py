"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class represents a directory with replicate directories in it.  It shouldn't have any data in it.

"""
from src.log_walker.objects.dir_objs.directory import Directory

class ReplicateDirecotry(Directory):
    
    replicateDirs: {}

    def __init__(self, path: str):
        super().__init__(path)
        self.replicateDirs = {}
        
    def setupDirectory(self):
        
    