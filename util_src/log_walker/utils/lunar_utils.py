"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This is the class for accessing LUNAR functions outside of LUNAR

"""
import numpy as np

from src.log_analysis import kemppainen_muzzy_modulus
from src.log_analysis.signal_processing import butter_optimize_wn_with_power_spectrum, butter_lowpass_filter


class LUNARUtils:

    @staticmethod
    def get_lunar_butterworth_filtered_data(stress, strain):
        """
        Description: Uses LUNAR's Analysis class to get Butterworth filtered stress and strain data

        Inputs:
                stress(array): An array of stress data
                strain(array): An array of strain data
        Output:
            filtered_strain(array): An array of filtered strain data from LUNAR
            filtered_stress(array): An array of filtered stress data from LUNAR
        """

        stress = np.array(stress)
        strain = np.array(strain)

        # Most of these values from the LUNAR defaults in the UI
        # modify them as you would the UI values

        wn = butter_optimize_wn_with_power_spectrum(strain,
                                                    stress,
                                                    "op",  # wn
                                                    False,  # write_data
                                                    False,  # save_fig
                                                    "",  # fig_name
                                                    300,  # dpi
                                                    )

        return butter_lowpass_filter(strain,
                                     stress,
                                     wn,  # wn
                                     2,  # order
                                     "msr",  # qm
                                     False,  # write_data
                                     False,  # save_fig
                                     "",  # fig_name
                                     300)  # dpi

    # TODO implement Poisson's ratio
    # t1 and t2 should be arrays that have strain data in them
    @staticmethod
    def get_lunar_km_modulus(
            stress, strain, file_path: str, t1=None, t2=None
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

        stress = list(stress)
        strain = list(strain)

        if t1 is None:
            t1 = []
        if t2 is None:
            t2 = []

        # I got most of these values from the LUNAR defaults in the UI
        # modify them as you would the UI values
        return kemppainen_muzzy_modulus.compute(
            strain,
            stress,
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
