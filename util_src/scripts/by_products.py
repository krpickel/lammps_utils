import dataframe_image as dfi
import matplotlib.pyplot as plt

from util_src.objects import read_lammps_output as rd
from util_src.objects.DeletedClusterMassPercentOverTime import (
    DeletedClusterMassPercentOverTime,
)

inDir = "C:/Users/asmon/mol_dyn/research/Phenolic_Resin/TP_Reax/4k/H2O/pyro/low_mass_del/rep1"
outDir = inDir + "/analysis/"
df = rd.read_o_file(inDir, outDir)
delTimesteps = rd.read_del_file(inDir, outDir)

initial_mass = df.v_mass_initial[0]

deletedClusterSet = set()
xData = []
yData = []

for timestep in delTimesteps:
    for cluster in delTimesteps[timestep]:
        deletedClusterSet.add(cluster.clusterStr)

        print(cluster.clusterStr)
        print(cluster.numCluster)
        print("weight: " + str(cluster.get_total_weight()))
        yData.append(cluster.get_total_weight())
        xData.append(int(timestep) * 0.1 / 1000)

print(deletedClusterSet)

deletedClusterWeightTotals = {}
deletedClusterMassPercentage = {}
deletedClusterMassPercentageOverTime = {}

name_col_str = "Name"
total_mass_str = "Total Mass (amu)"
mass_percent = "Mass Percentage (%)"

cluster_table = {name_col_str: [], total_mass_str: [], mass_percent: []}
for cluster_name in deletedClusterSet:

    deletedClusterWeightTotals[cluster_name] = 0
    deletedClusterMassPercentageOverTime[cluster_name] = []

    for timestep in delTimesteps:
        # the data goes all the way to 5000K in some files, so we want to
        # only grab up to 3200K which is the 2,900,000 timestep.
        # Can be modified to change the temperature range
        if int(timestep) <= 2900000:
            for cluster in delTimesteps[timestep]:
                if cluster.clusterStr == cluster_name:
                    deletedClusterMassPercentTimestep = (
                        DeletedClusterMassPercentOverTime()
                    )
                    deletedClusterWeightTotals[cluster_name] += cluster.getTotalWeight()
                    deletedClusterMassPercentTimestep.timestep = timestep
                    deletedClusterMassPercentTimestep.totalMassPercent = 100 * (
                            deletedClusterWeightTotals[cluster_name] / initial_mass
                    )
                    deletedClusterMassPercentageOverTime[cluster_name].append(
                        deletedClusterMassPercentTimestep
                    )

    deletedClusterWeightTotals[cluster_name] = round(
        deletedClusterWeightTotals[cluster_name], 2
    )
    deletedClusterMassPercentage[cluster_name] = round(
        100 * deletedClusterWeightTotals[cluster_name] / initial_mass, 2
    )

    for key in cluster_table.keys():
        if name_col_str == key:
            cluster_table[key].append(cluster_name)
        elif total_mass_str == key:
            cluster_table[key].append(deletedClusterWeightTotals[cluster_name])
        elif mass_percent == key:
            cluster_table[key].append(deletedClusterMassPercentage[cluster_name])

deletedXData = {}
deletedYData = {}

for key in deletedClusterMassPercentageOverTime:
    tempX = []
    tempY = []
    temp = deletedClusterMassPercentageOverTime[key]
    for timestep in temp:
        tempX.append(float(timestep.timestep) * 0.1 / float(1000))
        tempY.append(timestep.totalMassPercent)
    deletedXData[key] = tempX
    deletedYData[key] = tempY

cluster_table = cluster_table.sort_values(by=[mass_percent], ascending=False)
dfi.export(cluster_table, outDir + "deletedClusters.png", dpi=300)

overOnePercent = set()

for cluster in deletedClusterSet:
    if deletedClusterMassPercentage[cluster] > 1:
        overOnePercent.add(cluster)

fig, ax = plt.subplots()
ax.set_xlabel("Time (ps)")
ax.set_ylabel("Mass Percent Deleted (%)")

for key in deletedYData:
    if not key == "O" and not key == "H":
        xData = deletedXData[key]
        yData = deletedYData[key]

    ax.plot(xData, yData, label=key)

plt.legend()
plt.savefig(outDir + "clusters_deleted_No_Oxy_No_Hydro.png", dpi=300)
