"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This class contains all the data in an o file

"""

import copy

from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.objects.file_objs.log_file import LogFile


class OFile(LogFile):
    errors: {}
    sections: {}
    data_section_ids: []
    type: DataFileIndicators
    warnings: {}

    def __init__(self, dir_path, name, unique_id, extn):
        super().__init__(dir_path, name, unique_id, extn)

        self.data_section_ids = []
        self.errors = {}
        self.sections = {}
        self.warnings = {}
        self.type = DataFileIndicators.OFILE

        print("Reading o file: " + unique_id)
        # start_file_time = time.time()
        self.split_sections()
        # end_time = time.time()
        print("Done reading: " + unique_id)
        # print("OFile read time: " + str(end_time - start_file_time) + " s")

    def split_sections(self):

        # TODO: alphabetize
        preDataHeaderLine = "Per MPI rank"
        headerNext = False
        inData = False
        dataSect = None
        inHeader = False
        headerSec = None
        headers = []
        warningID = 0
        errorID = 0
        sectionID = 1

        with open(self.get_full_file_path(), "r") as file:
            previousData = []
            for line in file:
                # if inHeader:
                #    if headerSec == None:
                #        headerSec = HeaderSection(0)
                if line.strip() != "" and not line is None:
                    if inData:
                        line = line.strip().split()
                        if not previousData:
                            if headers != line:
                                dataSect = DataSection(sectionID)
                                sectionID += 1
                                dataSect.setDataHeaders(line)
                                headers = line
                                previousData = line
                            else:
                                previousData = dataSect.get_previous_row()

                        elif line[0] == "WARNING:":
                            self.warnings[warningID] = line
                            warningID = +1
                        elif line[0] == "ERROR:":
                            self.errors[errorID] = line
                            errorID = +1
                        elif "Loop" == line[0]:
                            inData = False

                            previousData = []
                            # Need to use copy or else the value in the dictionary
                            # will keep referencing dataSect and will be overridden
                            self.sections[dataSect.unique_id] = copy.copy(dataSect)

                        elif line[0] != previousData[0] and line != headers:
                            dataSect.add_data_row(line)
                            previousData = line

                    if "LAMMPS" in line:
                        # TODO: capture meaningful header section data
                        inHeader = True
                    elif preDataHeaderLine in line:
                        inData = True
                    if "WARNING" in line[0]:
                        self.warnings[warningID] = line
                        warningID = +1
                    elif "ERROR" in line[0]:
                        self.errors[errorID] = line
                        errorID = +1

    def get_type(self):
        return self.type


class Section(object):
    unique_id: int
    section_type: str

    def __init__(self, uniqueID, sectType):
        self.unique_id = uniqueID
        self.section_type = sectType


class DataSection(Section):
    data: {}
    header_order: {}

    def __init__(self, uniqueID):
        super().__init__(uniqueID, "data")
        self.header_order = {}
        self.data = {}

    def setDataHeaders(self, headers: []):
        header_num = 0
        for header in headers:
            self.header_order[header] = header_num
            self.data[header] = []
            header_num += 1

    def add_data_row(self, new_row: []):

        for key in self.header_order.keys():
            data = new_row[self.header_order[key]]
            try:
                self.data[key].append(int(data))
            except ValueError:
                try:
                    self.data[key].append(float(data))
                except ValueError:
                    self.data[key].append(data)

    def get_previous_row(self):
        numRows = len(self.data["Step"])
        return_row = []

        for key in self.header_order.keys():
            return_row.append(self.data[key][numRows - 1])

        return return_row


class SimBox:
    boxType: str
    posX: int
    negX: int
    posY: int
    negY: int
    posZ: int
    negZ: int

    def __init__(self, line):
        pass


class HeaderSection(Section):
    header_atoms: int
    velocities: int
    bonds: int
    angles: int
    dihedrals: int
    impropers: int
    simBox: SimBox

    def __init__(self, uniqueID):
        Section.__init__(uniqueID, "header")

        self.populateSection(self)

    def populateBox(self, line):
        self.simBox = SimBox(line)
