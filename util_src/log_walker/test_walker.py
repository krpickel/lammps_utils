from pathlib import Path

from util_src.log_walker.objects.anlzer.strain_rep_analyzer import StrainRepAnalyzer

# inDir = Path(
#     "C:\\Users\\asmon\\eclipse-workspace\\lammps_data_utils\\test_files\\oFiles"
# )
#
# inDir2 = "C:\\Users\\asmon\\eclipse-workspace\\lammps_data_utils\\test_files\\oFiles"
#
# rootDir = RootDirectory(inDir)

inRepDir = Path("C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\oFiles\\Rep_Stress_Strain")

# inRepDir = Path("C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TriPhenols\\Stress_Strain\\H2O")

# inDir = Path(
#    "C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TriPhenols\\Stress_Strain\\H2No\\rep3"
# )

rep_analyzer = StrainRepAnalyzer(inRepDir)
rep_analyzer.plot_everything_for_all_reps()

# inRepDir = Path("C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TriPhenols\\Stress_Strain\\H2No")

# rep_analyzer = StrainRepAnalyzer(inRepDir)
# rep_analyzer.plot_everything_for_all_reps()

# anlyzer = StrainAnalyzer(inDir)

# anlyzer.plot_everything()

# inDir = Path(
#    "C:\\Users\\asmon\\eclipse-workspace\\lammps_data_utils\\test_files\\oFiles\\Stress_Strain"
# )

# strain = StrainDirectory(inDir)
# dataDir = DataDirectory(inDir.__str__())
