"""
o File example

"""

import os
from pathlib import Path

from matplotlib import pyplot as plt

from util_src.log_walker.enums.data_cols import DataColumns
from util_src.log_walker.objects.anlzer.strain_rep_analyzer import StrainRepAnalyzer
from util_src.log_walker.objects.file_objs.o_file import OFile
from util_src.log_walker.utils.lunar_utils import LUNARUtils

cwd = os.getcwd()

print(cwd)

test_dir = cwd + "\\test_files"

inOFile = Path(test_dir + "\\stress_strain\\single_o_files\\stress_strain")
name = "TP_x_Strain.script.sh.o177356"
uniqueID = "o177356"
extn = ".o177356"

ofile = OFile(str(inOFile), name, uniqueID, extn)

strain = ofile.sections[1].data[DataColumns.X_STRAIN.value]
stress = ofile.sections[1].data[DataColumns.X_STRESS.value]

stress_butter = LUNARUtils.get_lunar_butterworth_filtered_data(stress, strain)

fig, ax1 = plt.subplots()
ax1.plot(strain, stress, color="grey")
ax1.plot(strain, stress_butter, color="blue")

plt.show()

"""
Bulk Strain analysis
"""

inRepDir = Path(test_dir + "\\stress_strain\\Rep_stress_strain")

rep_analyzer = StrainRepAnalyzer(inRepDir)
rep_analyzer.plot_xyz_for_all_reps()

"""
O File Read Testing
"""

# inDir = Path(
#    test_dir + "\\stress_strain"
# )

# inOFile = Path(test_dir + "\\stress_strain\\single_o_files\\react")
# name = "TriPhen_H2O_react.script.sh.o174617"
# uniqueID = "o174617"
# extn = ".o174617"
#
# ofile = OFile(str(inOFile), name, uniqueID, extn)
#
# inOFile = Path(test_dir + \\stress_strain\\single_o_files\\stress_strain")
# name = "TP_x_Strain.script.sh.o177356"
# uniqueID = "o177356"
# extn = ".o177356"
# time_start = time.time()
# ofile2 = OFile(str(inOFile), name, uniqueID, extn)
# time_end = time.time()
# print("OFile time: " + str(time_end - time_start))

"""
Strain Rep Analyzer Testing
"""
# # inRepDir = Path(test_dir + "\\oFiles\\Rep_stress_strain")
# #
# rep_analyzer = StrainRepAnalyzer(inRepDir)
# rep_analyzer.plot_everything_for_all_reps()
#
# inRepDir = Path("C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TriPhenols\\Stress_Strain\\H2No")
# # inRepDir = Path(test_dir + "\\oFiles\\Rep_stress_strain")
# #
# rep_analyzer = StrainRepAnalyzer(inRepDir)
# rep_analyzer.plot_everything_for_all_reps()

# anlyzer = StrainAnalyzer(inDir)

# anlyzer.plot_everything()

"""
Del File Testing
"""

# inDelFile = test_dir + "\\pyroFiles\\pyro_data"
# name = "heating_TP_ReaxFF_rep_1_del_0-50.del"
# unique_id = "12345"
# extn = ".del"
#
# DelFile(inDelFile, name, unique_id, extn)

"""
Pos File Testing
"""

# inDelFile = test_dir + "\\pyroFiles\\pyro_data"
# name = "heating_TP_ReaxFF_rep_1_del_0-50.pos"
# unique_id = "12345"
# extn = ".del"
#
# PosFile(inDelFile, name, unique_id, extn)

"""
pyro analyzer testing
"""

# inPyroDir = Path(test_dir + "\\pyroFiles\\pyro_data")
#
# pyro_analyzer = PyroAnalyzer(inPyroDir)
#
# print()

"""
random
"""
# inOFile = Path("C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TP_Reax\\4k\\H2O\\pyro\\delete_hydro_only\\rep1")
# name = "TP_Pyro.script.sh.o179705"
# uniqueID = "o179705"
# extn = ".o179705"
#
# ofile = OFile(str(inOFile), name, uniqueID, extn)
#
# time = []
# temp = []
#
# for step in ofile.sections[1].data["Step"]:
#     time.append(int(step) * 0.1 / 1000)
#
# for temp_step in ofile.sections[1].data["c_MyTemp"]:
#     temp.append(float(temp_step))
#
# print()
#
# # temp = LUNARUtils.get_lunar_butterworth_filtered_data(temp, time)
#
# fig, ax1 = plt.subplots()
# # ax1.plot(strain, stress, color="grey")
# ax1.plot(time, temp, color="blue")
#
# plt.show()
