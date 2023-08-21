#!/bin/bash
#SBATCH --job-name=GA_bp_kx      # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G         # memory per cpu-core (4G is default)
#SBATCH --time=0-3:59:00        # total run time limit (HH:MM:SS)
#SBATCH --mail-type=fail        # send email when job fails
#SBATCH --mail-user=kaifengx@princeton.edu

# $1 binary name
# $2 folder name
# $3 trace name
# $4 warmup instruction number
# $5 sim instruction number
BIN=/tigress/kaifengx/ChampSim/bin/champsim_branchonly
# cd /tigress/kaifengx/ChampSim
BP_STATES=$1
TRACE=/scratch/gpfs/kaifengx/nokvm-2023-06-26_-_19-16-36-imageprocessing_test.trace
WARMUP_INSN=1000000
SIM_INSN=9000000

$BIN --warmup_instructions ${WARMUP_INSN} --simulation_instructions ${SIM_INSN} -c -b $1 ${TRACE} > ${1}.out
