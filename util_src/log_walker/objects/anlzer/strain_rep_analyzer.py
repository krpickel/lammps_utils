"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is the class for analyzing replicates of strain directories

"""
import statistics

from util_src.log_walker.enums.dir_type import DirType
from util_src.log_walker.objects.anlzer.analizer import Analyzer
from util_src.log_walker.objects.anlzer.strain_analyzer import StrainAnalyzer
from util_src.log_walker.objects.dir_objs.rep_dir import ReplicateDirectory
from util_src.log_walker.utils.file_utils import DirFileUtils


class StrainRepAnalyzer(Analyzer):
    rep_dir: ReplicateDirectory

    def __init__(self, path):
        super().__init__()
        rep_dir = ReplicateDirectory(path)
        if rep_dir.type != DirType.STRAIN:
            print("Must be a ReplicateDirectory of type STRAIN")
            raise Exception

        self.rep_dir = rep_dir
        rep_dir.create_analysis_dir()

    def plot_xyz_for_all_reps(self):
        directional_elastic_mods = {}
        ave_elastic_mods = {}
        ave_elastic_mods_st_devs = {}
        yield_strengths = {}
        yield_strengths_st_devs = {}

        for rep_name in self.rep_dir.replicate_data_dirs.keys():
            replicate_dirs = self.rep_dir.replicate_data_dirs[rep_name]

            for strain_dir in replicate_dirs:
                dir_name = strain_dir.path.name

                analyzer = StrainAnalyzer(strain_dir)

                analyzer.plot_strain_directions_only()
                analyzer.make_elastic_mod_yield_strength_table()
                directional_elastic_mods[dir_name] = [analyzer.get_x_dir_elastic_mod(),
                                                      analyzer.get_y_dir_elastic_mod(),
                                                      analyzer.get_z_dir_elastic_mod()]

                ave_elastic_mods[dir_name], ave_elastic_mods_st_devs[
                    dir_name] = analyzer.get_ave_elastic_mod_w_st_dev()
                yield_strengths[dir_name], yield_strengths_st_devs[
                    dir_name] = analyzer.get_ave_yield_strength_w_st_dev()

            ave_elastic_mod = statistics.mean(ave_elastic_mods.values())
            stdev_elastic_mod = statistics.stdev(ave_elastic_mods.values())

            ave_yield_strength = statistics.mean(yield_strengths.values())
            stdev_yield_strength = statistics.stdev(yield_strengths.values())

            replicate_table = {"rep": yield_strengths.keys(), "Elastic Modulus": ave_elastic_mods.values(),
                               "Yield Strength": yield_strengths.values()}

            DirFileUtils.write_csv_from_dict(replicate_table, str(self.rep_dir.analysis_path) + "\\Replicate_props.csv")
            print(ave_elastic_mods)
            print(yield_strengths)
            print("Yield Strength = " + str(ave_yield_strength) + "+-" + str(stdev_yield_strength))
            print("Elastic Mod = " + str(ave_elastic_mod) + "+-" + str(stdev_elastic_mod))
