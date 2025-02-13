"""
@author: Keith Pickelmann
Revision 1.0
February 8th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class contains all the data in a del file

"""
import time

from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.objects.file_objs.log_file import LogFile
from util_src.log_walker.objects.pyro_objs.cluster import Cluster


class DelFile(LogFile):
    type: DataFileIndicators
    time_steps: {}

    def __init__(self, dir_path, name, unique_id, extn):
        super().__init__(dir_path, name, unique_id, extn)

        self.time_steps = {}
        self.type = DataFileIndicators.DELFILE

        print("Reading del file: " + unique_id)
        start_file_time = time.time()
        self.read_data()
        end_time = time.time()
        print("Done reading: " + unique_id)
        print("Del File read time: " + str(end_time - start_file_time) + " s")

    def read_data(self):
        timestep = {}

        with open(self.dir_path + "\\" + self.name, 'r') as file:
            for line in file:
                clustersDeleted = []
                data = line.split()
                for i in range(2, len(data), 2):

                    if len(data) > i:
                        clustersDeleted.append(Cluster(data[i + 1], int(data[i])))
                self.time_steps[data[1]] = clustersDeleted
