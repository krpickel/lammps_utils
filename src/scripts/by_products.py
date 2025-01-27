import dataframe_image as dfi
import matplotlib.pyplot as plt
import pandas as pd
from src.objects import read_lammps_output as rd
from src.objects.DeletedClusterMassPercentOverTime import (
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
        print("weight: " + str(cluster.getTotalWeight()))
        yData.append(cluster.getTotalWeight())
        xData.append(int(timestep) * 0.1 / 1000)

print(deletedClusterSet)

deletedClusterWeightTotals = {}
deletedClusterMassPercentage = {}
deletedClusterMassPercentageOverTime = {}

nameColStr = "Name"
totalMassStr = "Total Mass (amu)"
massPercent = "Mass Percentage (%)"
clusterTable = pd.DataFrame({nameColStr: [], totalMassStr: [], massPercent: []})
for clusterName in deletedClusterSet:
    deletedClusterWeightTotals[clusterName] = 0

    deletedClusterMassPercentageOverTime[clusterName] = []
    for timestep in delTimesteps:
        if int(timestep) <= 2900000:
            for cluster in delTimesteps[timestep]:
                if cluster.clusterStr == clusterName:
                    deletedClusterMassPercentTimestep = (
                        DeletedClusterMassPercentOverTime()
                    )
                    deletedClusterWeightTotals[clusterName] += cluster.getTotalWeight()
                    deletedClusterMassPercentTimestep.timestep = timestep
                    deletedClusterMassPercentTimestep.totalMassPercent = 100 * (
                        deletedClusterWeightTotals[clusterName] / initial_mass
                    )
                    deletedClusterMassPercentageOverTime[clusterName].append(
                        deletedClusterMassPercentTimestep
                    )

    deletedClusterWeightTotals[clusterName] = round(
        deletedClusterWeightTotals[clusterName], 2
    )
    deletedClusterMassPercentage[clusterName] = round(
        100 * deletedClusterWeightTotals[clusterName] / initial_mass, 2
    )

    tableRow = {
        nameColStr: clusterName,
        totalMassStr: deletedClusterWeightTotals[clusterName],
        massPercent: deletedClusterMassPercentage[clusterName],
    }

    clusterTable = clusterTable._append(tableRow, ignore_index=True)

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

clusterTable = clusterTable.sort_values(by=[massPercent], ascending=False)
dfi.export(clusterTable, outDir + "deletedClusters.png", dpi=300)

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
