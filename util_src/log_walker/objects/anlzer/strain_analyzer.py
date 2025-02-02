"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is the class for analyzing a strain directory

"""

# Import Python libs
from pathlib import Path
from statistics import mean

# Import external libs
from matplotlib import pyplot as plt
from pandas.core.frame import DataFrame

# Import local libs
from src.log_analysis.main import analysis as LUNARLogAnalysis
from util_src.log_walker.enums.data_cols import DataColumns
from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.enums.strain_direction import StrainDirection
from util_src.log_walker.objects.anlzer.analizer import Analyzer
from util_src.log_walker.objects.dir_objs.data_dir import DataDirectory
from util_src.log_walker.objects.dir_objs.directory import Directory
from util_src.log_walker.objects.dir_objs.strain_dir import StrainDirectory


class StrainAnalyzer(Analyzer):
    # Setup variables for object
    strainDir: StrainDirectory
    xDir: DataDirectory
    yDir: DataDirectory
    zDir: DataDirectory
    xDirUniqueID: str
    yDirUniqueID: str
    zDirUniqueID: str
    xStrainSectionData: DataFrame
    yStrainSectionData: DataFrame
    zStrainSectionData: DataFrame

    def __init__(self, path: Path):
        """ """
        super().__init__()

        self.strainDir = StrainDirectory(path)
        self.xDir = self.strainDir.getXDataDir()
        self.yDir = self.strainDir.getYDataDir()
        self.zDir = self.strainDir.getZDataDir()

        self.strainDir.createAnalysisDir()
        self.xDir.createAnalysisDir()
        self.yDir.createAnalysisDir()
        self.zDir.createAnalysisDir()

        self.setupRelevantData()

    """
    Start Plotters
    """

    def plotXDirXData(self):

        xFile = self.getFilePath(
            StrainDirection.X.value, self.xDir.analysisPath, self.xDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getXDirXStrain(), self.getXDirXStress(), StrainDirection.X.value, xFile
        )
        self.savePlot(plot, self.xDir, StrainDirection.X.value, self.xDirUniqueID)

    def plotXDirYData(self):

        yFile = self.getFilePath(
            StrainDirection.Y.value, self.xDir.analysisPath, self.xDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getXDirYStrain(), self.getXDirYStress(), StrainDirection.Y.value, yFile
        )
        self.savePlot(plot, self.xDir, StrainDirection.Y.value, self.xDirUniqueID)

    def plotXDirZData(self):

        zFile = self.getFilePath(
            StrainDirection.Z.value, self.xDir.analysisPath, self.xDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getXDirZStrain(), self.getXDirZStress(), StrainDirection.Z.value, zFile
        )
        self.savePlot(plot, self.xDir, StrainDirection.Z.value, self.xDirUniqueID)

    """
    End X Directory Plotters
    """

    def plotYDirXData(self):

        xFile = self.getFilePath(
            StrainDirection.X.value, self.yDir.analysisPath, self.yDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getYDirXStrain(), self.getYDirXStress(), StrainDirection.X.value, xFile
        )
        self.savePlot(plot, self.yDir, StrainDirection.X.value, self.yDirUniqueID)

    def plotYDirYData(self):

        yFile = self.getFilePath(
            StrainDirection.Y.value, self.yDir.analysisPath, self.yDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getYDirYStrain(), self.getYDirYStress(), StrainDirection.Y.value, yFile
        )
        self.savePlot(plot, self.yDir, StrainDirection.Y.value, self.yDirUniqueID)

    def plotYDirZData(self):

        zFile = self.getFilePath(
            StrainDirection.Z.value, self.yDir.analysisPath, self.yDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getYDirZStrain(), self.getYDirZStress(), StrainDirection.Z.value, zFile
        )
        self.savePlot(plot, self.yDir, StrainDirection.Z.value, self.yDirUniqueID)

    """
    End Y Directory Plotters
    """

    def plotZDirXData(self):

        xFile = self.getFilePath(
            StrainDirection.X.value, self.zDir.analysisPath, self.zDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getZDirXStrain(), self.getZDirXStress(), StrainDirection.X.value, xFile
        )
        self.savePlot(plot, self.zDir, StrainDirection.X.value, self.zDirUniqueID)

    def plotZDirYData(self):

        yFile = self.getFilePath(
            StrainDirection.Y.value, self.zDir.analysisPath, self.zDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getZDirYStrain(), self.getZDirYStress(), StrainDirection.Y.value, yFile
        )
        self.savePlot(plot, self.zDir, StrainDirection.Y.value, self.zDirUniqueID)

    def plotZDirZData(self):

        zFile = self.getFilePath(
            StrainDirection.Z.value, self.zDir.analysisPath, self.zDirUniqueID
        )

        plot = self.plotStressStrainData(
            self.getZDirZStrain(), self.getZDirZStress(), StrainDirection.Z.value, zFile
        )
        self.savePlot(plot, self.zDir, StrainDirection.Z.value, self.zDirUniqueID)

    """
    End Z Directory Plotters
    """

    def plotEverything(self):
        self.plotXYZAve()
        self.plotXDirXData()
        self.plotXDirYData()
        self.plotXDirZData()
        self.plotYDirXData()
        self.plotYDirYData()
        self.plotYDirZData()
        self.plotZDirXData()
        self.plotZDirYData()
        self.plotZDirZData()

    def plotXYZAve(self):
        xStresses = self.getXDirXStress()
        yStresses = self.getYDirYStress()
        zStresses = self.getZDirZStress()

        xyzUniqueID = self.xDirUniqueID + "_" + self.yDirUniqueID + "_" + self.zDirUniqueID

        file = self.getFilePath(
            StrainDirection.XYZ.value, self.strainDir.analysisPath,
            xyzUniqueID
        )
        aveStresses = []

        if len(xStresses) == len(yStresses) and len(xStresses) == len(zStresses) and len(yStresses) == len(zStresses):
            for i in range(0, len(xStresses)):
                aveStresses.append(mean([xStresses[i], yStresses[i], zStresses[i]]))
        else:
            print("The lengths don't all match.  Check data")

        plot = self.plotStressStrainData(self.getXDirXStrain(), aveStresses, StrainDirection.XYZ.value, file)
        self.savePlot(plot, self.strainDir, StrainDirection.XYZ.value, xyzUniqueID)

        pass

    def plotStressStrainData(
            self, strain: [], stress: [], strainDirection: StrainDirection, saveDir: str
    ):

        strainButter, stressButter = self.getLUNARButterworthFilteredData(
            stress, strain
        )

        self.getLUNARKMModulus(
            stressButter, strainButter, strainDirection, saveDir + "_kmMod"
        )

        fig, ax1 = plt.subplots()
        ax1.plot(strain, stress, color="blue")
        ax1.plot(strainButter, stressButter, color="red")
        fig.tight_layout()

        return plt

    """
    End Other Plotters
    """

    def setupRelevantData(self):
        strainDirs = [self.xDir, self.yDir, self.zDir]

        for dataDir in strainDirs:
            for key in dataDir.dataFiles.keys():

                file = dataDir.dataFiles[key]
                if file.getType() != DataFileIndicators.OFILE:
                    print("Not an o file, can't analyze")
                    break
                for sectKey in file.sections.keys():
                    section = file.sections[sectKey]
                    print(key)
                    # section.data is already a DataFrame but this is a more explicit way
                    # of showing that.  It also lets IDEs autocomplete easier
                    data = DataFrame(section.data)

                    if DataColumns.X_STRAIN.value in data.columns:
                        if dataDir.path.name.lower() == StrainDirection.X.value:
                            self.xStrainSectionData = data
                            self.xDirUniqueID = key
                        elif dataDir.path.name.lower() == StrainDirection.Y.value:
                            self.yStrainSectionData = data
                            self.yDirUniqueID = key
                        elif dataDir.path.name.lower() == StrainDirection.Z.value:
                            self.zStrainSectionData = data
                            self.zDirUniqueID = key
        print()

    """
    X directory data getters
    """

    def getXDirXStrain(self):
        return self.xStrainSectionData[DataColumns.X_STRAIN.value].astype(float)

    def getXDirYStrain(self):
        return self.xStrainSectionData[DataColumns.Y_STRAIN.value].astype(float)

    def getXDirZStrain(self):
        return self.xStrainSectionData[DataColumns.Z_STRAIN.value].astype(float)

    def getXDirXStressStrain(self):
        return self.getXDirXStress(), self.getXDirXStrain()

    def getXDirYStressStrain(self):
        return self.getXDirYStress(), self.getXDirYStrain()

    def getXDirZStressStrain(self):
        return self.getXDirZStress(), self.getXDirZStrain()

    def getXDirXStress(self):
        return self.xStrainSectionData[DataColumns.X_STRESS.value].astype(float)

    def getXDirYStress(self):
        return self.xStrainSectionData[DataColumns.Y_STRESS.value].astype(float)

    def getXDirZStress(self):
        return self.xStrainSectionData[DataColumns.Z_STRESS.value].astype(float)

    """
    Y directory data getters
    """

    def getYDirXStrain(self):
        return self.yStrainSectionData[DataColumns.X_STRAIN.value].astype(float)

    def getYDirYStrain(self):
        return self.yStrainSectionData[DataColumns.Y_STRAIN.value].astype(float)

    def getYDirZStrain(self):
        return self.yStrainSectionData[DataColumns.Z_STRAIN.value].astype(float)

    def getYDirXStressStrain(self):
        return self.getYDirXStress(), self.getYDirXStrain()

    def getYDirYStressStrain(self):
        return self.getYDirYStress(), self.getYDirYStrain()

    def getYDirZStressStrain(self):
        return self.getYDirZStress(), self.getYDirZStrain()

    def getYDirXStress(self):
        return self.yStrainSectionData[DataColumns.X_STRESS.value].astype(float)

    def getYDirYStress(self):
        return self.yStrainSectionData[DataColumns.Y_STRESS.value].astype(float)

    def getYDirZStress(self):
        return self.yStrainSectionData[DataColumns.Z_STRESS.value].astype(float)

    """
    Z directory getters
    """

    def getZDirXStrain(self):
        return self.zStrainSectionData[DataColumns.X_STRAIN.value].astype(float)

    def getZDirYStrain(self):
        return self.zStrainSectionData[DataColumns.Y_STRAIN.value].astype(float)

    def getZDirZStrain(self):
        return self.zStrainSectionData[DataColumns.Z_STRAIN.value].astype(float)

    def getZDirXStressStrain(self):
        return self.getZDirXStress(), self.getZDirXStrain()

    def getZDirYStressStrain(self):
        return self.getZDirYStress(), self.getZDirYStrain()

    def getZDirZStressStrain(self):
        return self.getZDirZStress(), self.getZDirZStrain()

    def getZDirXStress(self):
        return self.zStrainSectionData[DataColumns.X_STRESS.value].astype(float)

    def getZDirYStress(self):
        return self.zStrainSectionData[DataColumns.Y_STRESS.value].astype(float)

    def getZDirZStress(self):
        return self.zStrainSectionData[DataColumns.Z_STRESS.value].astype(float)

    """
    Other getters
    """

    def __getBogusLUNARModeDict(self):
        # Make a bogus mode directory for the LUNAR analysis object
        # We already have all the stress-strain data so
        # all we need it for is to do Butterworth filtering
        # and KM Modulus calculations which don't require anything
        # from the analysis object but the log
        mode = {}
        mode["parent_directory"] = ""
        mode["logfile"] = ""
        mode["keywords"] = []
        mode["sections"] = []
        mode["xdata"] = []
        mode["ydata"] = []
        mode["xcompute"] = ""
        mode["ycompute"] = ""

        return mode

    def getLUNARButterworthFilteredData(self, stress, strain):

        lunarAnlzr = LUNARLogAnalysis(self.__getBogusLUNARModeDict())
        return lunarAnlzr.butterworth_lowpass(
            strain,
            stress,
            min(strain),
            max(strain),
            "op",
            2,
            "msr",
            "y",
            True,
            False,
            False,
            "",
            300,
        )

    def getLUNARKMModulus(
            self, stress, strain, direction: StrainDirection, filePath: str
    ):
        lunarAnlzr = LUNARLogAnalysis(self.__getBogusLUNARModeDict())

        t1 = ""
        t2 = ""

        if StrainDirection.X == direction:
            t1 = DataColumns.Y_STRAIN.value
            t2 = DataColumns.Z_STRAIN.value
        elif StrainDirection.Y == direction:
            t1 = DataColumns.X_STRAIN.value
            t2 = DataColumns.Z_STRAIN.value
        elif StrainDirection.Z == direction:
            t1 = DataColumns.X_STRAIN.value
            t2 = DataColumns.Y_STRAIN.value

        lunarAnlzr.kemppainen_muzzy_modulus(
            strain,
            stress,
            min(strain),
            max(strain),
            0.005,
            0.0,
            "rfs",
            1,
            0.0,
            t1,
            t2,
            False,
            True,
            filePath,
            300,
        )
        pass

    """
    End getters
    """

    def getFilePath(self, directionStr, analysisPath, xDirUniqueID):
        return str(str(analysisPath) + "\\" + directionStr + "_" + xDirUniqueID)

        pass

    def savePlot(
            self, plot: plt, directory: Directory, direction: str, uniqueID: str
    ):
        saveDir = str(
            str(directory.path) + "\\analysis" + "\\" + direction + "_" + uniqueID
        )
        plot.savefig(saveDir, dpi=300)
