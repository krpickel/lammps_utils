"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is the class for analyzing a strain directory.  This is meant to analyze three strain directories, one for each
uniaxial direction (x, y, z).  There should be a directory for x, y, and z strain directions, the directory names should
 also be "x", "y", and "z".  The directories should hold one o file, lammps dump, with strain data.

For valid column names, see the DataColumns enum.

Will be expanded later to do shear analysis as well
"""

# Import Python libs
import statistics
from pathlib import Path

# Import external libs
from matplotlib import pyplot as plt

# Import local libs
from util_src.log_walker.enums.data_cols import DataColumns
from util_src.log_walker.enums.data_file_indicators import DataFileIndicators
from util_src.log_walker.enums.strain_direction import StrainDirection
from util_src.log_walker.objects.anlzer.analizer import Analyzer
from util_src.log_walker.objects.dir_objs.data_dir import DataDirectory
from util_src.log_walker.objects.dir_objs.directory import Directory
from util_src.log_walker.objects.dir_objs.strain_dir import StrainDirectory
from util_src.log_walker.utils.file_utils import DirFileUtils
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
    x_strain_section_data: dict
    y_strain_section_data: dict
    z_strain_section_data: dict

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
            for key in dataDir.data_files.keys():

                file = dataDir.data_files[key]
                if file.get_type() != DataFileIndicators.OFILE:
                    print("Not an o file, can't analyze")
                    break
                for sectKey in file.sections.keys():
                    section = file.sections[sectKey]

                    data = section.data

                    if DataColumns.X_STRAIN.value in data.keys():
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
        self.plot_x_dir_x_data()
        self.plot_y_dir_y_data()
        self.plot_z_dir_z_data()

    def plot_stress_strain_data(
            self, strain: [], stress: [], strain_direction: StrainDirection, save_dir: str
    ):

        stress_butter = LUNARUtils.get_lunar_butterworth_filtered_data(
            stress, strain
        )

        lunar_out = LUNARUtils.get_lunar_km_modulus(
            stress_butter, strain, save_dir + "_kmMod"
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

        # ax1.plot(strain, stress, color="grey")
        ax1.plot(strain, stress_butter, color="blue")

        slope_midpoints = self.get_slope_midpoint(min(x_reg), max(x_reg), min(y_reg), max(y_reg))

        ax1.plot(x_reg, y_reg, color="orange")
        ax1.annotate("E = " + str(round(elastic_mod / 1000, 2)) + " GPa", xy=(slope_midpoints[0], slope_midpoints[1]),
                     xytext=(slope_midpoints[0] + 0.01, slope_midpoints[1]),
                     arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0.00', color='orange'),
                     font='Arial', color='darkorange', )

        yield_strain = ys_point[0]

        ax1.plot(yield_strain, yield_strength, "o", color="red")

        ax1.annotate("$\sigma_{ys}$ = " + str(round(yield_strength, 1)) + " MPa", xy=(yield_strain, yield_strength),
                     xytext=(yield_strain - 0.013, yield_strength + 20),
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
        return list(map(float, self.x_strain_section_data[DataColumns.X_STRAIN.value]))

    def get_x_dir_y_strain(self):
        return list(map(float, self.x_strain_section_data[DataColumns.Y_STRAIN.value]))

    def get_x_dir_z_strain(self):
        return list(map(float, self.x_strain_section_data[DataColumns.Z_STRAIN.value]))

    def get_x_dir_x_stress_strain(self):
        return self.get_x_dir_x_stress(), self.get_x_dir_x_strain()

    def get_x_dir_y_stress_strain(self):
        return self.get_x_dir_y_stress(), self.get_x_dir_y_strain()

    def get_x_dir_z_stress_strain(self):
        return self.get_x_dir_z_stress(), self.get_x_dir_z_strain()

    def get_x_dir_x_stress(self):
        return list(map(float, self.x_strain_section_data[DataColumns.X_STRESS.value]))

    def get_x_dir_y_stress(self):
        return list(map(float, self.x_strain_section_data[DataColumns.Y_STRESS.value]))

    def get_x_dir_z_stress(self):
        return list(map(float, self.x_strain_section_data[DataColumns.Z_STRESS.value]))

    """
    Y directory data getters
    """

    def get_y_dir_x_strain(self):
        return list(map(float, self.y_strain_section_data[DataColumns.X_STRAIN.value]))

    def get_y_dir_y_strain(self):
        return list(map(float, self.y_strain_section_data[DataColumns.Y_STRAIN.value]))

    def get_y_dir_z_strain(self):
        return list(map(float, self.y_strain_section_data[DataColumns.Z_STRAIN.value]))

    def get_y_dir_x_stress_strain(self):
        return self.getYDirXStress(), self.get_y_dir_x_strain()

    def get_y_dir_y_stress_strain(self):
        return self.get_y_dir_y_stress(), self.get_y_dir_y_strain()

    def get_y_dir_z_stress_strain(self):
        return self.get_y_dir_z_stress(), self.get_y_dir_z_strain()

    def getYDirXStress(self):
        return list(map(float, self.y_strain_section_data[DataColumns.X_STRESS.value]))

    def get_y_dir_y_stress(self):
        return list(map(float, self.y_strain_section_data[DataColumns.Y_STRESS.value]))

    def get_y_dir_z_stress(self):
        return list(map(float, self.y_strain_section_data[DataColumns.Z_STRESS.value]))

    """
    Z directory getters
    """

    def get_z_dir_x_strain(self):
        return list(map(float, self.z_strain_section_data[DataColumns.X_STRAIN.value]))

    def get_z_dir_y_strain(self):
        return list(map(float, self.z_strain_section_data[DataColumns.Y_STRAIN.value]))

    def get_z_dir_z_strain(self):
        return list(map(float, self.z_strain_section_data[DataColumns.Z_STRAIN.value]))

    def get_z_dir_x_stress_strain(self):
        return float, self.get_z_dir_x_stress(), self.get_z_dir_x_strain()

    def get_z_dir_y_stress_strain(self):
        return float, self.get_z_dir_y_stress(), self.get_z_dir_y_strain()

    def get_z_dir_z_stress_strain(self):
        return self.get_z_dir_z_stress(), self.get_z_dir_z_strain()

    def get_z_dir_x_stress(self):
        return list(map(float, self.z_strain_section_data[DataColumns.X_STRESS.value]))

    def get_z_dir_y_stress(self):
        return list(map(float, self.z_strain_section_data[DataColumns.Y_STRESS.value]))

    def get_z_dir_z_stress(self):
        return list(map(float, self.z_strain_section_data[DataColumns.Z_STRESS.value]))

    """
    End getters
    """

    def get_x_dir_elastic_mod(self):
        return self.x_dir_elastic_mod

    def get_y_dir_elastic_mod(self):
        return self.y_dir_elastic_mod

    def get_z_dir_elastic_mod(self):
        return self.z_dir_elastic_mod

    def get_x_dir_yield_strength(self):
        return self.x_dir_yield_strength

    def get_y_dir_yield_strength(self):
        return self.y_dir_yield_strength

    def get_z_dir_yield_strength(self):
        return self.z_dir_yield_strength

    def get_ave_elastic_mod_w_st_dev(self):
        return statistics.mean(
            [self.x_dir_elastic_mod, self.y_dir_elastic_mod, self.z_dir_elastic_mod]), statistics.stdev(
            [self.x_dir_elastic_mod, self.y_dir_elastic_mod, self.z_dir_elastic_mod])

    def get_ave_yield_strength_w_st_dev(self):
        return statistics.mean(
            [self.x_dir_yield_strength, self.y_dir_yield_strength, self.z_dir_yield_strength]), statistics.stdev(
            [self.x_dir_yield_strength, self.y_dir_yield_strength, self.z_dir_yield_strength])

    @staticmethod
    def get_file_path(direction_str, analysis_path, dir_unique_id):
        return str(str(analysis_path) + "\\" + direction_str + "_" + dir_unique_id)

    def make_elastic_mod_yield_strength_table(self):
        DirFileUtils.write_csv_from_dict({"direction": ["x", "y", "z"],
                                          "elastic modulus": [self.x_dir_elastic_mod, self.y_dir_elastic_mod,
                                                              self.z_dir_elastic_mod],
                                          "Yield Strength": [self.x_dir_yield_strength, self.y_dir_yield_strength,
                                                             self.z_dir_yield_strength]},
                                         str(self.strain_dir.analysis_path) + "\\mech_props.csv")

    @staticmethod
    def save_plot(
            plot: plt, directory: Directory, direction: str, unique_id: str
    ):
        saveDir = str(
            str(directory.path) + "\\analysis" + "\\" + direction + "_" + unique_id
        )
        plot.savefig(saveDir, dpi=300)

    @staticmethod
    def get_slope_midpoint(x_lo, x_hi, y_lo, y_hi):
        mid_x = (x_hi + x_lo) / 2
        mid_y = (y_hi + y_lo) / 2

        return [mid_x, mid_y]
