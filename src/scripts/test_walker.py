"""
inDir = 'C:\\Users\\asmon\\eclipse-workspace\\lammps_utils\\test_files\\oFiles\\Stress_Strain'
name = 'x_Strain.script.sh'
uniqueID = 'o177356'
extn = '.o177356'

oFile = oFile(inDir, name, uniqueID, extn)
"""

"""
inDir = "C:\\Users\\asmon\\eclipse-workspace\\lammps_utils\\test_files\\log_walk_test\\"

# s LogWalker(inDir)

#print(DataFileIndicators.OFILE.isFileType(".sh.516512.del"))

p = Path("C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TP_Reax\\4k\\H2O\\pyro")

rootDir = RootDirectory(
    "C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TP_Reax\\4k\\H2O\\pyro\\"
)

print("Root Data?" + str(rootDir.dataPresent))
print("Root Rep?" + str(rootDir.repPresent))
print(rootDir.path)
print(rootDir.files)
print(rootDir.subDirs)
"""
from pathlib import Path

from src.log_walker.enums.data_file_indicators import DataFileIndicators
from src.log_walker.log_walker import LogWalker
from src.log_walker.objects.dir_objs.data_dir import DataDirectory
from src.log_walker.objects.dir_objs.root_dir import RootDirectory
from src.log_walker.objects.o_file import OFile

inDir = Path(
    "C:\\Users\\asmon\\eclipse-workspace\\lammps_data_utils\\test_files\\oFiles"
)

inDir2 = "C:\\Users\\asmon\\eclipse-workspace\\lammps_data_utils\\test_files\\oFiles"

rootDir = RootDirectory(inDir)
print()
# dataDir = DataDirectory(inDir.__str__())
