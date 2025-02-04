"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is the class for accessing LUNAR functions outside of LUNAR

"""

from src.log_analysis.main import Analysis


class LUNARUtils:

    @staticmethod
    def __get_bogus_lunar_mode_dict():
        # Make a bogus mode dictionary for the LUNAR analysis object

        return {"parent_directory": "", "logfile": "", "keywords": [], "sections": [], "xdata": [], "ydata": [],
                "xcompute": "", "ycompute": ""}

    @classmethod
    def get_lunar_butterworth_filtered_data(cls, stress, strain):
        """
        Description: Uses LUNAR's Analysis class to get Butterworth filtered stress and strain data

        Inputs:
                stress(array): An array of stress data
                strain(array): An array of strain data
        Output:
            filtered_strain(array): An array of filtered strain data from LUNAR
            filtered_stress(array): An array of filtered stress data from LUNAR
        """
        lunar_analyzer = Analysis(cls.__get_bogus_lunar_mode_dict())

        # Most of these values from the LUNAR defaults in the UI
        # modify them as you would the UI values
        return lunar_analyzer.butterworth_lowpass(strain,
                                                  stress,
                                                  min(strain),
                                                  max(strain),
                                                  "op",  # wn
                                                  2,  # order
                                                  "msr",  # qm
                                                  "y",  # axis y = stress axis, x = strain axis
                                                  True,  # psd
                                                  False,  # write_data
                                                  False,  # save_fig
                                                  "",  # fig_name
                                                  300,  # dpi
                                                  )

    # TODO implement Poisson's ratio
    # t1 and t2 should be arrays that have strain data in them
    @classmethod
    def get_lunar_km_modulus(
            cls, stress, strain, file_path: str, t1=None, t2=None
    ):
        """
        Description: Uses LUNAR's Analysis class to get Kemppainen-Muzzy modulus from stress-strain data

        Inputs:
                stress(array): An array of stress data
                strain(array): An array of strain data
                file_path(string): A string of the full file path including the file name
                t1(array): An optional array of strain data in a different direction than the strain from input 2
                t2(array): An optional array of strain data in a different direction than the strain from t1 and input 2
        Output:
            See LUNAR's log_analysis.kemppainen_muzzy_modulus for outputs
        """
        if t1 is None:
            t1 = []
        if t2 is None:
            t2 = []
        lunar_analyzer = Analysis(cls.__get_bogus_lunar_mode_dict())

        # I got most of these values from the LUNAR defaults in the UI
        # modify them as you would the UI values
        return lunar_analyzer.kemppainen_muzzy_modulus(
            strain,
            stress,
            min(strain),  # xlo
            max(strain),  # xhi
            0.005,  # minxhi
            0.0,  # maxxhi
            "rfs",  # xlo_method
            1,  # yp
            0.0,  # offset
            t1,  # t1
            t2,  # t2
            False,  # write_data
            True,  # save_fig
            file_path,  # fig_name
            300,  # dpi
        )
