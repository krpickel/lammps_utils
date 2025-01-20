"""
inDir = 'C:\\Users\\asmon\\eclipse-workspace\\lammps_utils\\test_files\\oFiles\\Stress_Strain'
name = 'x_Strain.script.sh'
uniqueID = 'o177356'
extn = '.o177356'

oFile = oFile(inDir, name, uniqueID, extn)
"""

from pathlib import Path

from src.log_walker.enums.data_file_indicators import DataFileIndicators
from src.log_walker.log_walker import LogWalker
from src.log_walker.objects.dir_objs.root_dir import RootDirectory
from src.log_walker.objects.o_file import OFile
from src.log_walker.utils.file_utils import DirFileUtils


inDir = "C:\\Users\\asmon\\eclipse-workspace\\lammps_utils\\test_files\\log_walk_test\\"

# s LogWalker(inDir)

print(DataFileIndicators.OFILE.isFileType(".sh.516512.del"))

p = Path("C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TP_Reax\\4k\\H2O\\pyro")

rootDir = RootDirectory(
    "C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TP_Reax\\4k\\H2O\\pyro\\"
)

print(rootDir.dataPresent)
print(rootDir.repPresent)
print(rootDir.path)
print(rootDir.files)
print(rootDir.subDirs)

repDir = DirFileUtils.isRepDir(
    "C:\\Users\\asmon\\mol_dyn\\research\\Phenolic_Resin\\TP_Reax\\4k\\H2O\\pyro\\"
)

print(repDir)

string = "hello123"

endNum = ""
repBaseName = None
for i in range(1, string.__len__()):
    character = string[string.__len__() - i]

    if character.isdigit():
        endNum = character + endNum
    elif character.isalpha():
        repBaseName = string[: string.__len__() - i + 1]
        break

repNum = int(endNum)
print(repNum)
print(repBaseName)

print(string[-2])
print(string[string.__len__() - 1])
