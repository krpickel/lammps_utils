#! /bin/bash
# 
# This file contains critical settings for appropriate submission and execution
# of the simulation. Editing this file [and/or its bulk (re-)generation]
# without explicit permission of (or discussion with) the administrators can
# lead to improper use of resources, extended wait times in the queue, etc.,
# and will be grounds for removing your account from the HPC infrastructure.
#
# Refer to HPC 101 Training Camp v2.0 (https://mtu.instructure.com/courses/1374830)
# for additional information.
 
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -q short.q
#$ -pe mpichg 16
# Not an array simulation
#$ -M krpickel@mtu.edu
#$ -m abes
# No dependent simulation
#$ -hard -l mem_free=2G
#$ -hard -l lammps_lic=.0625000000
# Uses traditional CPU
#
#$ -notify

# Load and list modules
source ${HOME}/.bashrc
module load mpi/impi/2018.3.222-iccifort-2018.3.222-GCC-7.3.0-2.30
# module load lammps/2020.10.29-CPU-stable-python
module list

# Input/Output files
INPUT_FOLDER="${PWD}"
INPUT_FILE="TP_z_Strain.script"
OUTPUT_FILE="out.lp"
ARRAY_TASK_ID=""
ADDITIONAL_OPTIONS=""

# Prepare to run the simulation
LAMMPS="/research/${USER}/lammps-29Oct20" 
export LD_LIBRARY_PATH="${LAMMPS}/src:${LD_LIBRARY_PATH}"
cd ${LAMMPS}/build
source myenv/bin/activate
cd ${INPUT_FOLDER}

# Run the simulation
mpirun -n ${NSLOTS} -machine ${TMP}/machines ${LAMMPS}/src/lmp_mpi -log ${INPUT_FOLDER}/${OUTPUT_FILE}${ARRAY_TASK_ID} -in ${INPUT_FOLDER}/${INPUT_FILE}${ARRAY_TASK_ID}

# List modules
module list
