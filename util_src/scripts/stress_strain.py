from objects import read_lammps_output as rd
import log_analysis

inDir = 'C:/Users/asmon/mol_dyn/research/Phenolic_Resin/TriPhenols/Stress_Strain/H2O/rep1'
outDir = inDir + '/analysis/'

dataX = rd.read_o_file(inDir+'/X', outDir)
dataY = rd.read_o_file(inDir+'/Y', outDir)
dataZ = rd.read_o_file(inDir+'/Z', outDir)

