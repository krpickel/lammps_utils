from pathlib import Path

from util_src.log_walker.objects.anlzer.strain_analyzer import StrainAnalyzer

# inDir = Path(
#     "C:\\Users\\asmon\\eclipse-workspace\\lammps_data_utils\\test_files\\oFiles"
# )
#
# inDir2 = "C:\\Users\\asmon\\eclipse-workspace\\lammps_data_utils\\test_files\\oFiles"
#
# rootDir = RootDirectory(inDir)

inDir = Path("C:\\Users\\asmon\\mol_dyn\\lammps_data_utils\\test_files\\oFiles\\Stress_Strain")

# inDir = Path(
#    "C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TriPhenols\\Stress_Strain\\H2No\\rep3"
# )

anlyzer = StrainAnalyzer(inDir)

anlyzer.plotEverything()

# inDir = Path(
#    "C:\\Users\\asmon\\eclipse-workspace\\lammps_data_utils\\test_files\\oFiles\\Stress_Strain"
# )

# strain = StrainDirectory(inDir)
print()
# dataDir = DataDirectory(inDir.__str__())
