#!/bin/bash
#SBATCH --job-name=GA_bp_kx      # create a short name for your job
#SBATCH --nodes=1                # node count
#SBATCH --ntasks=1               # total number of tasks across all nodes
#SBATCH --cpus-per-task=1        # cpu-cores per task (>1 if multi-threaded tasks)
#SBATCH --mem-per-cpu=8G         # memory per cpu-core (4G is default)
#SBATCH --time=0-23:59:00        # total run time limit (HH:MM:SS)
#SBATCH --mail-type=ALL        # send email when job fails
#SBATCH --mail-user=kaifengx@princeton.edu

# $1 binary name
# $2 folder name
# $3 trace name
# $4 warmup instruction number
# $5 sim instruction number
BIN=/tigress/kaifengx/ChampSim/bin/champsim_branchonly_user_ld_noaddrrandom
# cd /tigress/kaifengx/ChampSim
BP_STATES=/tigress/kaifengx/ChampSim/branch/tage/states_useronly_noaddrrandom/
TRACE=/scratch/gpfs/kaifengx/nokvm-2023-06-26_-_19-16-36-imageprocessing_test.trace
WARMUP_INSN=100000000
SIM_INSN=900000000

$BIN --warmup_instructions ${WARMUP_INSN} --simulation_instructions ${SIM_INSN} -c -b ${BP_STATES}insn -n $1 ${TRACE} > ${BP_STATES}useronly_ld_noaddrrandom_${1}.out
