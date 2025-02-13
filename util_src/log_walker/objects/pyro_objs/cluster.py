# -*- coding: utf-8 -*-
"""
@author: Keith Pickelmann
Revision 1.0
January 15th, 2025
Michigan Technological University
1400 Townsend Dr.
Houghton, MI 49931

This file contains the object for holding data from a row in a del file generated from a LAMMPS pyrolysis simulation

"""

# Needed for values related to elements from the periodic table
from util_src.objects.Elements import Elements


class Cluster:
    """
    class: ClusterDeleted
    desc: An object that holds the cluster data for a cluster that was deleted
          Currently it only works for carbon, hydrogen, and oxygen but could easily be
          expanded.  This class is also capable of returning the weight of individual elements
          in the cluster, and the total weight of the cluster.

    init: self,
          clusterStr: The string of a deleted cluster
                      e.g. 'C3H'
          numCluster: the number of clusters deleted
    functions: getOxygenWeight(self),
               getCarbonWeight(self),
               getHydrogenWeight(self),
               getTotalWeight(self)
    """

    def __init__(self, cluster_str: str, num_cluster: int):
        # set the object variables equal to the inputs
        self.clusterStr = cluster_str
        self.numCluster = num_cluster

        # elementDict holds the elements in the clusterStr as the keys and
        # the number of that element as the value
        self.element_dict = {}

        for element in Elements:
            elm_str = str(element.name)

            if elm_str in cluster_str:
                # Checks if there is a value after the element in the string
                # if so, check if the value after the element is a number, if it is a number
                # then there are that many atoms of the element in the string
                # otherwise, there is only one atom of that element in the string

                index_after_element = cluster_str.index(elm_str) + 1

                if len(cluster_str) > index_after_element:
                    if cluster_str[index_after_element].isdigit():

                        sub_cluster_str = cluster_str[index_after_element:]
                        num_element = None
                        for i in range(0, len(sub_cluster_str)):
                            if sub_cluster_str[i].isdigit():
                                if num_element is None:
                                    num_element = sub_cluster_str[i]
                                else:
                                    num_element = num_element + sub_cluster_str[i]
                            else:
                                break

                        self.element_dict[elm_str] = int(num_element)
                    else:
                        self.element_dict[elm_str] = 1
                else:
                    self.element_dict[elm_str] = 1
            else:
                self.element_dict[elm_str] = 0

    # Gets the total weight of the oxygen present in the cluster(s)
    def get_oxygen_weight(self):
        return self.get_oxygen_count() * Elements.O.value

    # Gets the total weight of the carbon present in the cluster(s)
    def get_carbon_weight(self):
        return self.get_carbon_count() * Elements.C.value

    # Gets the total weight of the hydrogen present in the cluster(s)
    def get_hydrogen_weight(self):
        return self.get_hydrogen_count() * Elements.H.value

    # Gets the total weight of the cluster(s)
    def get_total_weight(self):
        return self.get_oxygen_weight() + self.get_carbon_weight() + self.get_hydrogen_weight()

    def get_oxygen_count(self):
        return float(self.numCluster) * float(self.element_dict[str(Elements.O.name)])

    def get_carbon_count(self):
        return float(self.numCluster) * float(self.element_dict[str(Elements.C.name)])

    def get_hydrogen_count(self):
        return float(self.numCluster) * float(self.element_dict[str(Elements.H.name)])

    def get_atom_count(self):
        return self.get_oxygen_count() + self.get_carbon_count() + self.get_hydrogen_count()
