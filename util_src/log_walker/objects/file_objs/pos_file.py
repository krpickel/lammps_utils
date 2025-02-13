"""
@author: Keith Pickelmann
Revision 1.0
February 8th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class contains all the data in a pos file

"""
import time

from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.objects.file_objs.log_file import LogFile
from util_src.log_walker.objects.pyro_objs.cluster import Cluster


class PosFile(LogFile):
    type: DataFileIndicators
    time_steps: {}

    def __init__(self, dir_path, name, unique_id, extn):
        super().__init__(dir_path, name, unique_id, extn)

        self.time_steps = {}
        self.type = DataFileIndicators.POSFILE

        print("Reading pos file: " + unique_id)
        start_file_time = time.time()
        self.read_data()
        end_time = time.time()
        print("Done reading: " + unique_id)
        print("Pos file read time: " + str(end_time - start_file_time) + " s")

    def read_data(self):
        timestep = {}

        with open(self.dir_path + "\\" + self.name, 'r') as file:

            pre_header_line = "Timestep"
            post_data_line = "#"
            timestep_num = 0
            clusters_present = []
            in_data = False
            headers = None

            for line in file:
                line = line.split()

                if not in_data and line[0] == pre_header_line:
                    in_data = True
                    timestep_num = line[1]
                elif in_data:
                    if headers is None:
                        headers = line
                    elif headers == line:
                        continue
                    elif post_data_line == line[0]:
                        in_data = False
                        self.time_steps[timestep_num] = clusters_present
                        clusters_present = []
                    else:
                        clusters_present.append(Cluster(line[2], 1))
