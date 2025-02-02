"""
@author: Keith Pickelmann
Revision 1.0
January 31st, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This enum is for data columns in a LAMMPS dump file

This is intended to be used as a way to identify columns in a data section
of a dump file

Example usage:

strain_analyzer.py
"""

from enum import Enum


class DataColumns(Enum):
    """
    The data columns you want to identify
    """

    X_STRAIN = "v_etruex"
    Y_STRAIN = "v_etruey"
    Z_STRAIN = "v_etruez"
    X_STRESS = "f_sxx_ave"
    Y_STRESS = "f_syy_ave"
    Z_STRESS = "f_szz_ave"
