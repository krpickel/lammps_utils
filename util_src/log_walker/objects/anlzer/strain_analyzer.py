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
from util_src.log_walker.enums.data_cols import DataColumns
from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.enums.strain_direction import StrainDirection
from util_src.log_walker.objects.anlzer.analizer import Analyzer
from util_src.log_walker.objects.dir_objs.data_dir import DataDirectory
from util_src.log_walker.objects.dir_objs.directory import Directory
from util_src.log_walker.objects.dir_objs.strain_dir import StrainDirectory
from util_src.log_walker.utils.lunar_utils import LUNARUtils


class StrainAnalyzer(Analyzer):
    # Setup variables for object
    strain_dir: StrainDirectory
    x_dir: DataDirectory
    y_dir: DataDirectory
    z_dir: DataDirectory
    x_dir_elastic_mod: float
    y_dir_elastic_mod: float
    z_dir_elastic_mod: float
    xyz_elastic_mod: float
    x_dir_yield_strength: float
    y_dir_yield_strength: float
    z_dir_yield_strength: float
    xyz_yield_strength: float
    x_dir_unique_id: str
    y_dir_unique_id: str
    z_dir_unique_id: str
    x_strain_section_data: DataFrame
    y_strain_section_data: DataFrame
    z_strain_section_data: DataFrame

    def __init__(self, path):
        """
        Constructor
        """
        super().__init__()
        strain_dir = None
        if isinstance(path, Path):
            strain_dir = StrainDirectory(path)
        elif isinstance(path, StrainDirectory):
            strain_dir = path
        else:
            print("Incorrect input.  Input must be a pathlib.Path or a StrainDirectory obj")
            raise Exception

        self.strain_dir = strain_dir
        self.x_dir = strain_dir.getXDataDir()
        self.y_dir = strain_dir.getYDataDir()
        self.z_dir = strain_dir.getZDataDir()

        self.strain_dir.create_analysis_dir()
        self.x_dir.create_analysis_dir()
        self.y_dir.create_analysis_dir()
        self.z_dir.create_analysis_dir()

        self.x_dir_elastic_mod = 0.0
        self.y_dir_elastic_mod = 0.0
        self.z_dir_elastic_mod = 0.0
        self.xyz_elastic_mod = 0.0

        self.x_dir_yield_strength = 0.0
        self.y_dir_yield_strength = 0.0
        self.z_dir_yield_strength = 0.0
        self.xyz_yield_strength = 0.0

        self.setup_relevant_data()

    def setup_relevant_data(self):
        strainDirs = [self.x_dir, self.y_dir, self.z_dir]

        for dataDir in strainDirs:
            for key in dataDir.dataFiles.keys():

                file = dataDir.dataFiles[key]
                if file.getType() != DataFileIndicators.OFILE:
                    print("Not an o file_objs, can't analyze")
                    break
                for sectKey in file.sections.keys():
                    section = file.sections[sectKey]
                    # section.data is already a DataFrame but this is a more explicit way
                    # of showing that.  It also lets IDEs autocomplete easier
                    data = DataFrame(section.data)

                    if DataColumns.X_STRAIN.value in data.columns:
                        if dataDir.path.name.lower() == StrainDirection.X.value:
                            self.x_strain_section_data = data
                            self.x_dir_unique_id = key
                        elif dataDir.path.name.lower() == StrainDirection.Y.value:
                            self.y_strain_section_data = data
                            self.y_dir_unique_id = key
                        elif dataDir.path.name.lower() == StrainDirection.Z.value:
                            self.z_strain_section_data = data
                            self.z_dir_unique_id = key

    """
    Start Plotters
    """

    def plot_x_dir_x_data(self):

        x_file = self.get_file_path(
            StrainDirection.X.value, self.x_dir.analysis_path, self.x_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_x_dir_x_strain(), self.get_x_dir_x_stress(), StrainDirection.X.value, x_file
        )
        self.save_plot(plot, self.x_dir, StrainDirection.X.value, self.x_dir_unique_id)

    def plot_x_dir_y_data(self):

        y_file = self.get_file_path(
            StrainDirection.Y.value, self.x_dir.analysis_path, self.x_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_x_dir_y_strain(), self.get_x_dir_y_stress(), StrainDirection.Y.value, y_file
        )
        self.save_plot(plot, self.x_dir, StrainDirection.Y.value, self.x_dir_unique_id)

    def plot_x_dir_z_data(self):

        z_file = self.get_file_path(
            StrainDirection.Z.value, self.x_dir.analysis_path, self.x_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_x_dir_z_strain(), self.get_x_dir_z_stress(), StrainDirection.Z.value, z_file
        )
        self.save_plot(plot, self.x_dir, StrainDirection.Z.value, self.x_dir_unique_id)

    """
    End X Directory Plotters
    """

    def plot_y_dir_x_data(self):

        x_file = self.get_file_path(
            StrainDirection.X.value, self.y_dir.analysis_path, self.y_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_y_dir_x_strain(), self.getYDirXStress(), StrainDirection.X.value, x_file
        )
        self.save_plot(plot, self.y_dir, StrainDirection.X.value, self.y_dir_unique_id)

    def plot_y_dir_y_data(self):

        y_file = self.get_file_path(
            StrainDirection.Y.value, self.y_dir.analysis_path, self.y_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_y_dir_y_strain(), self.get_y_dir_y_stress(), StrainDirection.Y.value, y_file
        )
        self.save_plot(plot, self.y_dir, StrainDirection.Y.value, self.y_dir_unique_id)

    def plot_y_dir_z_data(self):

        z_file = self.get_file_path(
            StrainDirection.Z.value, self.y_dir.analysis_path, self.y_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_y_dir_z_strain(), self.get_y_dir_z_stress(), StrainDirection.Z.value, z_file
        )
        self.save_plot(plot, self.y_dir, StrainDirection.Z.value, self.y_dir_unique_id)

    """
    End Y Directory Plotters
    """

    def plot_z_dir_x_data(self):

        x_file = self.get_file_path(
            StrainDirection.X.value, self.z_dir.analysis_path, self.z_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_z_dir_x_strain(), self.get_z_dir_x_stress(), StrainDirection.X.value, x_file
        )
        self.save_plot(plot, self.z_dir, StrainDirection.X.value, self.z_dir_unique_id)

    def plot_z_dir_y_data(self):

        y_file = self.get_file_path(
            StrainDirection.Y.value, self.z_dir.analysis_path, self.z_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_z_dir_y_strain(), self.get_z_dir_y_stress(), StrainDirection.Y.value, y_file
        )
        self.save_plot(plot, self.z_dir, StrainDirection.Y.value, self.z_dir_unique_id)

    def plot_z_dir_z_data(self):

        z_file = self.get_file_path(
            StrainDirection.Z.value, self.z_dir.analysis_path, self.z_dir_unique_id
        )

        plot = self.plot_stress_strain_data(
            self.get_z_dir_z_strain(), self.get_z_dir_z_stress(), StrainDirection.Z.value, z_file
        )
        self.save_plot(plot, self.z_dir, StrainDirection.Z.value, self.z_dir_unique_id)

    """
    End Z Directory Plotters
    """

    def plot_everything(self):
        self.plot_xyz_ave()
        self.plot_x_dir_x_data()
        self.plot_x_dir_y_data()
        self.plot_x_dir_z_data()
        self.plot_y_dir_x_data()
        self.plot_y_dir_y_data()
        self.plot_y_dir_z_data()
        self.plot_z_dir_x_data()
        self.plot_z_dir_y_data()
        self.plot_z_dir_z_data()

    def plot_strain_directions_only(self):
        self.plot_xyz_ave()
        self.plot_x_dir_x_data()
        self.plot_y_dir_y_data()
        self.plot_z_dir_z_data()

    def plot_xyz_ave(self):
        x_stresses = self.get_x_dir_x_stress()
        y_stresses = self.get_y_dir_y_stress()
        z_stresses = self.get_z_dir_z_stress()

        xyz_unique_id = self.x_dir_unique_id + "_" + self.y_dir_unique_id + "_" + self.z_dir_unique_id

        file = self.get_file_path(
            StrainDirection.XYZ.value, self.strain_dir.analysis_path,
            xyz_unique_id
        )
        ave_stresses = []

        if len(x_stresses) == len(y_stresses) and len(x_stresses) == len(z_stresses) and len(y_stresses) == len(
                z_stresses):
            for i in range(0, len(x_stresses)):
                ave_stresses.append(mean([x_stresses[i], y_stresses[i], z_stresses[i]]))
        else:
            print("The lengths don't all match.  Check data")

        plot = self.plot_stress_strain_data(self.get_x_dir_x_strain(), ave_stresses, StrainDirection.XYZ.value, file)
        self.save_plot(plot, self.strain_dir, StrainDirection.XYZ.value, xyz_unique_id)

        pass

    def plot_stress_strain_data(
            self, strain: [], stress: [], strain_direction: StrainDirection, save_dir: str
    ):

        strain_butter, stress_butter = LUNARUtils.get_lunar_butterworth_filtered_data(
            stress, strain
        )

        lunar_out = LUNARUtils.get_lunar_km_modulus(
            stress_butter, strain_butter, save_dir + "_kmMod"
        )

        ys_point = lunar_out[2]

        yield_strength = ys_point[1]
        elastic_mod = lunar_out[6]

        if StrainDirection.X.value == strain_direction:
            self.x_dir_elastic_mod = elastic_mod
            self.x_dir_yield_strength = yield_strength
        elif StrainDirection.Y.value == strain_direction:
            self.y_dir_elastic_mod = elastic_mod
            self.y_dir_yield_strength = yield_strength
        elif StrainDirection.Z.value == strain_direction:
            self.z_dir_elastic_mod = elastic_mod
            self.z_dir_yield_strength = yield_strength
        elif StrainDirection.XYZ.value == strain_direction:
            self.xyz_elastic_mod = elastic_mod
            self.xyz_yield_strength = yield_strength

        x_reg = lunar_out[7]
        y_reg = lunar_out[8]

        fig, ax1 = plt.subplots()

        ax1.plot(strain, stress, color="grey")
        ax1.plot(strain_butter, stress_butter, color="blue")

        slope_midpoints = self.get_slope_midpoint(min(x_reg), max(x_reg), min(y_reg), max(y_reg))

        ax1.plot(x_reg, y_reg, color="orange")
        ax1.annotate("E = " + str(round(elastic_mod / 1000, 2)) + " GPa", xy=(slope_midpoints[0], slope_midpoints[1]),
                     xytext=(slope_midpoints[0] + 0.01, slope_midpoints[1]),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.00', color='orange'),
                     font='Arial', color='orange', )

        yield_strain = ys_point[0]

        ax1.plot(yield_strain, yield_strength, "o", color="red")

        ax1.annotate("$\sigma_{ys}$ = " + str(round(yield_strength, 1)) + " MPa", xy=(yield_strain, yield_strength),
                     xytext=(yield_strain + 0.005, yield_strength - 5),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.00', color='r'),
                     font='Arial', color='red',
                     )

        ax1.set_xlabel('Strain')
        ax1.set_ylabel('Stress (MPa)')

        fig.tight_layout()

        return plt

    """
    End Other Plotters
    """

    """
    X directory data getters
    """

    def get_x_dir_x_strain(self):
        return self.x_strain_section_data[DataColumns.X_STRAIN.value].astype(float)

    def get_x_dir_y_strain(self):
        return self.x_strain_section_data[DataColumns.Y_STRAIN.value].astype(float)

    def get_x_dir_z_strain(self):
        return self.x_strain_section_data[DataColumns.Z_STRAIN.value].astype(float)

    def get_x_dir_x_stress_strain(self):
        return self.get_x_dir_x_stress(), self.get_x_dir_x_strain()

    def get_x_dir_y_stress_strain(self):
        return self.get_x_dir_y_stress(), self.get_x_dir_y_strain()

    def get_x_dir_z_stress_strain(self):
        return self.get_x_dir_z_stress(), self.get_x_dir_z_strain()

    def get_x_dir_x_stress(self):
        return self.x_strain_section_data[DataColumns.X_STRESS.value].astype(float)

    def get_x_dir_y_stress(self):
        return self.x_strain_section_data[DataColumns.Y_STRESS.value].astype(float)

    def get_x_dir_z_stress(self):
        return self.x_strain_section_data[DataColumns.Z_STRESS.value].astype(float)

    """
    Y directory data getters
    """

    def get_y_dir_x_strain(self):
        return self.y_strain_section_data[DataColumns.X_STRAIN.value].astype(float)

    def get_y_dir_y_strain(self):
        return self.y_strain_section_data[DataColumns.Y_STRAIN.value].astype(float)

    def get_y_dir_z_strain(self):
        return self.y_strain_section_data[DataColumns.Z_STRAIN.value].astype(float)

    def get_y_dir_x_stress_strain(self):
        return self.getYDirXStress(), self.get_y_dir_x_strain()

    def get_y_dir_y_stress_strain(self):
        return self.get_y_dir_y_stress(), self.get_y_dir_y_strain()

    def get_y_dir_z_stress_strain(self):
        return self.get_y_dir_z_stress(), self.get_y_dir_z_strain()

    def getYDirXStress(self):
        return self.y_strain_section_data[DataColumns.X_STRESS.value].astype(float)

    def get_y_dir_y_stress(self):
        return self.y_strain_section_data[DataColumns.Y_STRESS.value].astype(float)

    def get_y_dir_z_stress(self):
        return self.y_strain_section_data[DataColumns.Z_STRESS.value].astype(float)

    """
    Z directory getters
    """

    def get_z_dir_x_strain(self):
        return self.z_strain_section_data[DataColumns.X_STRAIN.value].astype(float)

    def get_z_dir_y_strain(self):
        return self.z_strain_section_data[DataColumns.Y_STRAIN.value].astype(float)

    def get_z_dir_z_strain(self):
        return self.z_strain_section_data[DataColumns.Z_STRAIN.value].astype(float)

    def get_z_dir_x_stress_strain(self):
        return self.get_z_dir_x_stress(), self.get_z_dir_x_strain()

    def get_z_dir_y_stress_strain(self):
        return self.get_z_dir_y_stress(), self.get_z_dir_y_strain()

    def get_z_dir_z_stress_strain(self):
        return self.get_z_dir_z_stress(), self.get_z_dir_z_strain()

    def get_z_dir_x_stress(self):
        return self.z_strain_section_data[DataColumns.X_STRESS.value].astype(float)

    def get_z_dir_y_stress(self):
        return self.z_strain_section_data[DataColumns.Y_STRESS.value].astype(float)

    def get_z_dir_z_stress(self):
        return self.z_strain_section_data[DataColumns.Z_STRESS.value].astype(float)

    """
    End getters
    """

    @staticmethod
    def get_file_path(directionStr, analysisPath, xDirUniqueID):
        return str(str(analysisPath) + "\\" + directionStr + "_" + xDirUniqueID)

    @staticmethod
    def save_plot(
            plot: plt, directory: Directory, direction: str, uniqueID: str
    ):
        saveDir = str(
            str(directory.path) + "\\analysis" + "\\" + direction + "_" + uniqueID
        )
        plot.savefig(saveDir, dpi=300)

    @staticmethod
    def get_slope_midpoint(x_lo, x_hi, y_lo, y_hi):
        mid_x = (x_hi + x_lo) / 2
        mid_y = (y_hi + y_lo) / 2

        return [mid_x, mid_y]
