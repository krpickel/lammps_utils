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

from pandas import DataFrame

from util_src.log_walker.enums.dir_type import DirType
from util_src.log_walker.objects.anlzer.analizer import Analyzer
from util_src.log_walker.objects.anlzer.strain_analyzer import StrainAnalyzer
from util_src.log_walker.objects.dir_objs.rep_dir import ReplicateDirectory


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

    def plot_everything_for_all_reps(self):
        elastic_mods = {}
        yield_strengths = {}
        for rep_name in self.rep_dir.replicate_data_dirs.keys():
            replicate_dirs = self.rep_dir.replicate_data_dirs[rep_name]

            for strain_dir in replicate_dirs:
                analyzer = StrainAnalyzer(strain_dir)
                analyzer.plot_strain_directions_only()

                elastic_mods[strain_dir.path.name] = analyzer.xyz_elastic_mod
                yield_strengths[strain_dir.path.name] = analyzer.xyz_yield_strength

            ave_elastic_mod = statistics.mean(elastic_mods.values())
            stdev_elastic_mod = statistics.stdev(elastic_mods.values())

            ave_yield_strength = statistics.mean(yield_strengths.values())
            stdev_yield_strength = statistics.stdev(yield_strengths.values())

            replicate_table = DataFrame({"rep": yield_strengths.keys(), "Elastic Modulus": elastic_mods.values(),
                                         "Yield Strength": yield_strengths.values()})

            replicate_table.to_csv(str(self.rep_dir.analysis_path) + "\\Replicate_props.csv")
            print(elastic_mods)
            print(yield_strengths)
            print("Yield Strength = " + str(ave_yield_strength) + "+-" + str(stdev_yield_strength))
            print("Elastic Mod = " + str(ave_elastic_mod) + "+-" + str(stdev_elastic_mod))
