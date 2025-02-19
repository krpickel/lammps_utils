import os

cwd = os.getcwd()

print(cwd)

"""
O File Read Testing
"""

# inDir = Path(
#    "C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TriPhenols\\Stress_Strain\\H2No\\rep3"
# )

# inOFile = Path("C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\oFiles\\single_o_files\\react")
# name = "TriPhen_H2O_react.script.sh.o174617"
# uniqueID = "o174617"
# extn = ".o174617"
#
# ofile = OFile(str(inOFile), name, uniqueID, extn)
#
# inOFile = Path("C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\oFiles\\single_o_files\\stress_strain")
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
# inRepDir = Path("C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TriPhenols\\Stress_Strain\\H2O")
# # inRepDir = Path("C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\oFiles\\Rep_stress_strain")
# #
# rep_analyzer = StrainRepAnalyzer(inRepDir)
# rep_analyzer.plot_everything_for_all_reps()
#
# inRepDir = Path("C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TriPhenols\\Stress_Strain\\H2No")
# # inRepDir = Path("C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\oFiles\\Rep_stress_strain")
# #
# rep_analyzer = StrainRepAnalyzer(inRepDir)
# rep_analyzer.plot_everything_for_all_reps()

# anlyzer = StrainAnalyzer(inDir)

# anlyzer.plot_everything()

"""
Del File Testing
"""

# inDelFile = "C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\pyroFiles\\pyro_data"
# name = "heating_TP_ReaxFF_rep_1_del_0-50.del"
# unique_id = "12345"
# extn = ".del"
#
# DelFile(inDelFile, name, unique_id, extn)

"""
Pos File Testing
"""

# inDelFile = "C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\pyroFiles\\pyro_data"
# name = "heating_TP_ReaxFF_rep_1_del_0-50.pos"
# unique_id = "12345"
# extn = ".del"
#
# PosFile(inDelFile, name, unique_id, extn)

"""
pyro analyzer testing
"""

# inPyroDir = Path("C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\pyroFiles\\pyro_data")
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
